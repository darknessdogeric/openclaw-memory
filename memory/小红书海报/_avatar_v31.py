"""微信头像 v3.1 — 修 3 处自检缺陷
B: 交点上移居中 (640->545) + 去掉多余外圈
C: 中点从"弧线顶点"移到"弧线中段" + 缩小 + 两端点放大
A: 朱砂印放大 92->108, 位置微调
"""
import os
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OUT = r"C:\Users\ericz\Desktop\微信头像_v3_2026-10-24"
os.makedirs(OUT, exist_ok=True)

PALETTE = {
    "dunhuang": {"bg": "#F5F2EC", "fg": "#1F2422", "ac": "#B5432F"},
    "indigo":   {"bg": "#F2EDE3", "fg": "#1E3A5F", "ac": "#C8963E"},
    "mint":     {"bg": "#EFF5F2", "fg": "#1B3A34", "ac": "#C8963E"},
    "gold":     {"bg": "#1B3A34", "fg": "#E8DCC8", "ac": "#D4A74A"},
}
CN_FONT = ('"PingFang SC","Microsoft YaHei","Noto Sans SC",'
           '"Source Han Sans SC","SimHei",sans-serif')


def scheme_A():
    return '''
<div class="mark">
  <div class="word">实</div>
  <div class="seal"><span>B</span></div>
</div>'''


def scheme_B():
    # 交点视觉居中略偏上, 无外圈
    return '''
<div class="mark">
  <svg viewBox="0 0 1080 1080" width="1080" height="1080">
    <rect width="1080" height="1080" fill="__BG__"/>
    <line x1="140" y1="545" x2="940" y2="545" stroke="__FG__" stroke-width="9" opacity="0.92"/>
    <line x1="520" y1="140" x2="520" y2="900" stroke="__FG__" stroke-width="9" opacity="0.92"/>
    <circle cx="520" cy="545" r="82" fill="__AC__"/>
  </svg>
</div>'''


def scheme_C():
    # 中点放在弧线中段 (不是顶点), 缩小; 两端点放大
    return '''
<div class="mark">
  <svg viewBox="0 0 1080 1080" width="1080" height="1080">
    <rect width="1080" height="1080" fill="__BG__"/>
    <path d="M 250 745 Q 540 395 830 620" fill="none" stroke="__FG__" stroke-width="10"
          stroke-linecap="round" opacity="0.9"/>
    <circle cx="250" cy="745" r="62" fill="__FG__"/>
    <circle cx="830" cy="620" r="62" fill="__FG__"/>
    <circle cx="560" cy="508" r="70" fill="__AC__"/>
  </svg>
</div>'''


def scheme_D():
    return '''
<div class="mark">
  <div class="word">实</div>
</div>'''


TPL = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<style>
  *{margin:0;padding:0;box-sizing:border-box;}
  body{width:1080px;height:1080px;background:__BG__;overflow:hidden;
       font-family:__FONT__;display:flex;align-items:center;justify-content:center;}
  .mark{width:1080px;height:1080px;position:relative;display:flex;
        align-items:center;justify-content:center;}
  .word{font-size:600px;font-weight:900;color:__FG__;line-height:1;letter-spacing:-14px;}
  .seal{position:absolute;right:196px;bottom:192px;width:108px;height:108px;
        background:__AC__;border-radius:6px;display:flex;align-items:center;
        justify-content:center;}
  .seal span{font-size:54px;font-weight:900;color:__BG__;line-height:1;}
</style></head>
<body>__BODY__</body></html>"""

JOBS = [
    ("A_墨与朱印", scheme_A, ["dunhuang"]),
    ("B_定位十字", scheme_B, ["dunhuang", "indigo", "mint"]),
    ("C_双点弧线", scheme_C, ["dunhuang", "indigo", "mint"]),
    ("D_纯印极简", scheme_D, ["gold"]),
]


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


jobs = []
for sname, fn, themes in JOBS:
    for t in themes:
        p = PALETTE[t]
        html = (TPL.replace("__BODY__", fn())
                    .replace("__BG__", p["bg"]).replace("__FG__", p["fg"])
                    .replace("__AC__", p["ac"]).replace("__FONT__", CN_FONT))
        assert "__" not in html.split("<body>")[0], "占位符残留"
        hname = f"头像v3_{sname}_{t}.html"
        with open(os.path.join(OUT, hname), "w", encoding="utf-8") as f:
            f.write(html)
        jobs.append((hname, f"头像v3_{sname}_{t}.png", p))

with sync_playwright() as pw:
    browser = pw.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
    from PIL import Image
    for hn, pn, pal in jobs:
        with open(os.path.join(OUT, hn), encoding="utf-8") as f:
            c = f.read()
        page = browser.new_page(viewport={"width": 1080, "height": 1080}, device_scale_factor=2)
        page.set_content(c, wait_until="domcontentloaded")
        page.wait_for_timeout(400)
        path = os.path.join(OUT, pn)
        page.screenshot(path=path, full_page=False, omit_background=False, timeout=15000)
        page.close()
        im = Image.open(path).convert("RGB")
        w, h = im.size
        want = hex2rgb(pal["bg"])
        corners = [im.getpixel((6, 6)), im.getpixel((w - 7, 6)),
                   im.getpixel((6, h - 7)), im.getpixel((w - 7, h - 7))]
        ok = all(sum(abs(a - b) for a, b in zip(px, want)) < 18 for px in corners)
        # 强调色上屏校验: 统计强调色像素数
        acc = hex2rgb(pal["ac"])
        n_acc = sum(1 for y in range(0, h, 8) for x in range(0, w, 8)
                    if sum(abs(a - b) for a, b in zip(im.getpixel((x, y)), acc)) < 40)
        print(f"{'OK ' if ok else 'BAD'} {pn:34} bg✓ 强调色像素占比 {n_acc/((h//8)*(w//8))*100:.1f}%")
    browser.close()
print("DONE")
