"""浅底纸感版 — 颜色 token 替换 + 对比度校验 + DOM 排版检查
纸感三要素: 暖米底 / 低饱和赭石 / 细线分隔 + 极淡纸纤维肌理
"""
import os
import random
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

SRC = r"D:\B166ER-openclaw\workspace\memory\小红书海报\token_economy_v1.html"
OUT = r"C:\Users\ericz\Desktop\小红书_计量单位与新范式_2026-10-26"
os.makedirs(OUT, exist_ok=True)

# 深空 -> 纸感 映射 (左=深空版, 右=纸感版)
MAP = [
    # 底与主字
    ("background:#0E1626", "background:#F5F1E8"),
    ("color:#E8E4DA", "color:#16233A"),
    # 强调金 -> 赭石 (深色, 保对比度)
    ("#D4A74A", "#9A5A22"),
    ("rgba(212,167,74,", "rgba(154,90,34,"),
    # 次级文字
    ("#8A99B3", "#5F6A7A"),
    ("#7E8CA5", "#6E695D"),
    ("#C3B18A", "#6B6152"),
    # 卡片底 (白 -> 极淡墨)
    ("rgba(255,255,255,.045)", "rgba(22,35,58,.035)"),
    ("rgba(255,255,255,.04)", "rgba(22,35,58,.03)"),
    # 边框
    ("rgba(140,155,180,.16)", "rgba(22,35,58,.13)"),
    ("rgba(140,155,180,.18)", "rgba(22,35,58,.14)"),
    # 品牌标
    ("background:rgba(212,167,74,.92)", "background:#9A5A22"),
    ("border:1.5px solid #0E1626", "border:1.5px solid #F5F1E8"),
    ("background:rgba(212,167,74,.92);", "background:#9A5A22;"),
    # 水印
    ("color:#5A6880", "color:#9A9184"),
    # 星点 -> 深色墨点
    ('fill="#FFFFFF"', 'fill="#16233A"'),
]
# 品牌标里的文字色单独处理
MAP += [
    (".brand .bn{font-size:22px;font-weight:900;color:#0E1626;",
     ".brand .bn{font-size:22px;font-weight:900;color:#F5F1E8;"),
    (".brand .bl{font-size:6.8px;color:#0E1626;",
     ".brand .bl{font-size:6.8px;color:#F5F1E8;"),
]
# 纸纤维肌理 (线距放大 3 倍 + 降不透明度 -> PNG 可压缩)
TEXTURE = """
<style>
body::before{content:'';position:absolute;inset:0;z-index:0;pointer-events:none;
  background:
    repeating-linear-gradient(102deg, rgba(154,90,34,.014) 0 2px, transparent 2px 18px),
    repeating-linear-gradient(6deg, rgba(22,35,58,.010) 0 1px, transparent 1px 27px),
    radial-gradient(120% 80% at 50% 0%, rgba(255,255,255,.5), transparent 60%);
}
</style>
"""

with open(SRC, encoding="utf-8") as f:
    html = f.read()
for a, b in MAP:
    html = html.replace(a, b)
html = html.replace("</head>", TEXTURE + "</head>")

random.seed(20261026)
stars = "".join(
    f'<circle cx="{random.randint(0,1080)}" cy="{random.randint(0,1920)}" '
    f'r="{random.choice([1,1,1.2,1.5])}" fill="#16233A" '
    f'opacity="{round(random.uniform(0.03,0.12),2)}"/>' for _ in range(70))
html = html.replace("__STARS__", stars)

# 对比度校验 (WCAG)
def lum(hexs):
    hexs = hexs.lstrip("#")
    ch = []
    for i in (0, 2, 4):
        c = int(hexs[i:i+2], 16) / 255
        ch.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]

def ratio(f, b):
    l1, l2 = lum(f), lum(b)
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)

BG = "#F5F1E8"
PAIRS = [("主字 #16233A", "#16233A"), ("强调 #9A5A22", "#9A5A22"),
         ("次级 #5F6A7A", "#5F6A7A"), ("弱化 #6E695D", "#6E695D"),
         ("棕字 #6B6152", "#6B6152")]
print("=== 纸感版对比度校验 (WCAG, 正文需 >=4.5:1) ===")
worst = 99
for name, c in PAIRS:
    r = ratio(c, BG)
    worst = min(worst, r)
    print(f"  {name:<18} {r:>5.2f}:1  {'OK' if r >= 4.5 else ('大字OK' if r >= 3 else 'FAIL')}")

CHECK = """
() => {
  const issues = [];
  const W = 1080, H = 1920;
  document.querySelectorAll('*').forEach(el => {
    if (el.children.length === 0 && el.textContent.trim()) {
      if (el.scrollWidth > el.clientWidth + 2)
        issues.push('文字溢出: ' + (el.className||el.tagName) + ' "' + el.textContent.trim().slice(0,24) + '"');
    }
  });
  document.querySelectorAll('.sec, .sec *').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.right > W + 1 || r.bottom > H + 1 || r.left < -1)
      issues.push('超画布: ' + (el.className||el.tagName));
  });
  const secs = [...document.querySelectorAll('.sec')].map(s => s.getBoundingClientRect());
  for (let i = 1; i < secs.length; i++)
    if (secs[i].top < secs[i-1].bottom - 1)
      issues.push('段落重叠 sec' + i);
  document.querySelectorAll('.sec').forEach((s, i) => {
    const sr = s.getBoundingClientRect(); let mb = 0;
    s.querySelectorAll(':scope > *').forEach(c => { const r = c.getBoundingClientRect(); if (r.height>0) mb = Math.max(mb, r.bottom); });
    if (mb > sr.bottom + 2) issues.push('段' + (i+1) + ' 超段 ' + Math.round(mb - sr.bottom) + 'px');
  });
  return issues;
}
"""

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
    page = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=2)
    page.set_content(html, wait_until="domcontentloaded")
    page.wait_for_timeout(700)
    issues = page.evaluate(CHECK)
    png = os.path.join(OUT, "计量单位与新范式_纸感版_v1.0.png")
    page.screenshot(path=png, full_page=False, omit_background=False, timeout=20000)
    jpg = os.path.join(OUT, "计量单位与新范式_纸感版_v1.0.jpg")
    page.screenshot(path=jpg, full_page=False, omit_background=False, timeout=20000,
                    type="jpeg", quality=93)
    page.close()
    b.close()

print(f"\n渲染 PNG: {os.path.getsize(png):,} bytes")
print(f"渲染 JPG: {os.path.getsize(jpg):,} bytes")
print("最低对比度:", f"{worst:.2f}:1", "OK" if worst >= 4.5 else "CHECK")
if issues:
    print(f"⚠️ 排版问题 {len(issues)} 处:")
    for i in issues[:20]:
        print("  -", i)
else:
    print("✅ DOM 排版检查: 0 问题")
