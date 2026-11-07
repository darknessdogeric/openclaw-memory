"""重渲染 + DOM 级排版检查 (0 token, 替代人眼看图)"""
import os
import random
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

SRC = r"D:\B166ER-openclaw\workspace\memory\小红书海报\token_economy_v1.html"
OUT = r"C:\Users\ericz\Desktop\小红书_计量单位与新范式_2026-10-26"
os.makedirs(OUT, exist_ok=True)

random.seed(20261026)
stars = "".join(
    f'<circle cx="{random.randint(0,1080)}" cy="{random.randint(0,1920)}" '
    f'r="{random.choice([1,1,1.2,1.5,2,2.6])}" fill="#FFFFFF" '
    f'opacity="{round(random.uniform(0.08,0.42),2)}"/>' for _ in range(95))

with open(SRC, encoding="utf-8") as f:
    html = f.read().replace("__STARS__", stars)

# DOM 级排版检查: 文字溢出 / 元素超出画布 / 段落重叠
CHECK = """
() => {
  const issues = [];
  const W = 1080, H = 1920;
  // 1) 文字溢出容器
  document.querySelectorAll('*').forEach(el => {
    if (el.children.length === 0 && el.textContent.trim()) {
      if (el.scrollWidth > el.clientWidth + 2) {
        issues.push('文字溢出: ' + el.className + ' "' + el.textContent.trim().slice(0,28) +
                    '" (' + el.scrollWidth + '>' + el.clientWidth + ')');
      }
    }
  });
  // 2) 元素超出画布
  document.querySelectorAll('.sec, .sec *').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.right > W + 1 || r.bottom > H + 1 || r.left < -1) {
      issues.push('超出画布: ' + (el.className||el.tagName) + ' bottom=' + Math.round(r.bottom) +
                  ' right=' + Math.round(r.right));
    }
  });
  // 3) 段落重叠 (sibling .sec 之间的垂直交叠)
  const secs = [...document.querySelectorAll('.sec')].map(s => s.getBoundingClientRect());
  for (let i = 1; i < secs.length; i++) {
    if (secs[i].top < secs[i-1].bottom - 1) {
      issues.push('段落重叠: sec' + i + ' top=' + Math.round(secs[i].top) +
                  ' < sec' + (i-1) + ' bottom=' + Math.round(secs[i-1].bottom));
    }
  }
  // 4) 每段内容是否超出该段 (被下一段压住)
  document.querySelectorAll('.sec').forEach((s, i) => {
    const sr = s.getBoundingClientRect();
    let maxB = 0;
    s.querySelectorAll(':scope > *').forEach(c => {
      const r = c.getBoundingClientRect();
      if (r.height > 0) maxB = Math.max(maxB, r.bottom);
    });
    if (maxB > sr.bottom + 2) {
      issues.push('段' + (i+1) + ' 内容超段 ' + Math.round(maxB - sr.bottom) + 'px');
    }
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
    png = os.path.join(OUT, "计量单位与新范式_v1.0.png")
    page.screenshot(path=png, full_page=False, omit_background=False, timeout=20000)
    page.close()
    b.close()

print(f"渲染: {os.path.basename(png)}  {os.path.getsize(png):,} bytes")
if issues:
    print(f"\n⚠️ 排版问题 {len(issues)} 处:")
    for i in issues[:25]:
        print("  -", i)
else:
    print("\n✅ DOM 排版检查: 0 问题 (无溢出/无超画布/无段落重叠/无超段)")
