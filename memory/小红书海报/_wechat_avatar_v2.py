"""微信头像 v2 — 修正版 (修 S2金线被压 / S3两柱不等高 / S4线不汇聚 / S1线过长)
S3+S4 改用 SVG 精确控制几何
"""
import os
from playwright.sync_api import sync_playwright

OUT = r"C:\Users\ericz\Desktop\微信头像_2026-10-24"
os.makedirs(OUT, exist_ok=True)

THEMES = {
    "indigo": ("#F2EDE3", "#1E3A5F", "#C8963E"),
    "mint":   ("#EFF5F2", "#1B3A34", "#C8963E"),
    "gold":   ("#1B3A34", "#E8DCC8", "#D4A74A"),
}

def s1(bg, main, acc):
    # 十字收短到圆形安全区内, 线加粗
    return """
    <div class="mark">
      <svg viewBox="0 0 1080 1080" width="1080" height="1080">
        <line x1="196" y1="676" x2="884" y2="676" stroke="__MAIN__" stroke-width="7" opacity="0.9"/>
        <line x1="540" y1="196" x2="540" y2="884" stroke="__MAIN__" stroke-width="7" opacity="0.9"/>
        <circle cx="540" cy="676" r="88" fill="__ACC__" stroke="__BG__" stroke-width="34"/>
      </svg>
    </div>"""

def s2(bg, main, acc):
    # 字缩小 + 金线独立下移, 明确间距
    return """
    <div class="mark s2">
      <div class="char">实</div>
      <div class="uline"></div>
    </div>"""

def s3(bg, main, acc):
    # 门: 两柱等高 + 顶横梁 + 门内金点(客流穿门)
    return """
    <div class="mark">
      <svg viewBox="0 0 1080 1080" width="1080" height="1080">
        <rect x="356" y="286" width="54" height="500" fill="__MAIN__"/>
        <rect x="670" y="286" width="54" height="500" fill="__MAIN__"/>
        <rect x="356" y="286" width="368" height="54" fill="__MAIN__"/>
        <circle cx="540" cy="612" r="82" fill="__ACC__" stroke="__BG__" stroke-width="30"/>
      </svg>
    </div>"""

def s4(bg, main, acc):
    # 三点真正汇聚到金点: SVG 精确连线
    import math
    gx, gy, gr = 540, 540, 86
    pts = [(250, 262), (238, 820), (836, 452)]
    lines = []
    for px, py in pts:
        dx, dy = gx - px, gy - py
        L = math.hypot(dx, dy)
        ex, ey = gx - dx / L * (gr + 14), gy - dy / L * (gr + 14)
        lines.append(
            f'<line x1="{px}" y1="{py}" x2="{ex:.1f}" y2="{ey:.1f}" '
            f'stroke="__MAIN__" stroke-width="6" opacity="0.62"/>')
    circles = "".join(
        f'<circle cx="{px}" cy="{py}" r="40" fill="__MAIN__"/>' for px, py in pts)
    return f"""
    <div class="mark">
      <svg viewBox="0 0 1080 1080" width="1080" height="1080">
        {''.join(lines)}
        {circles}
        <circle cx="{gx}" cy="{gy}" r="{gr}" fill="__ACC__" stroke="__BG__" stroke-width="30"/>
      </svg>
    </div>"""

SCHEMES = {"S1_定位落点": s1, "S2_实字": s2, "S3_人流切口": s3, "S4_三点汇聚": s4}

TPL = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<style>
  *{margin:0;padding:0;box-sizing:border-box;}
  body{width:1080px;height:1080px;background:__BG__;
       font-family:"PingFang SC","Microsoft YaHei","Noto Sans SC",sans-serif;
       display:flex;align-items:center;justify-content:center;overflow:hidden;}
  .mark{width:1080px;height:1080px;display:flex;align-items:center;justify-content:center;}
  .s2{flex-direction:column;}
  .s2 .char{font-size:460px;font-weight:900;color:__MAIN__;line-height:1;
            font-family:"PingFang SC","Microsoft YaHei",sans-serif;}
  .s2 .uline{width:150px;height:12px;background:__ACC__;margin-top:56px;border-radius:2px;}
</style></head>
<body>__BODY__</body></html>"""

jobs = []
for sname, fn in SCHEMES.items():
    for tname, (bg, main, acc) in THEMES.items():
        # ⚠️ 顺序: 先插 BODY, 再替换颜色占位符 (否则 SVG 内的 __MAIN__ 不会被替换)
        html = (TPL.replace("__BODY__", fn(bg, main, acc))
                    .replace("__BG__", bg).replace("__MAIN__", main)
                    .replace("__ACC__", acc))
        with open(os.path.join(OUT, f"微信头像_{sname}_{tname}.html"), "w", encoding="utf-8") as f:
            f.write(html)
        jobs.append((f"微信头像_{sname}_{tname}.html", f"微信头像_{sname}_{tname}.png"))

with sync_playwright() as p:
    browser = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
    for hn, pn in jobs:
        with open(os.path.join(OUT, hn), encoding="utf-8") as f:
            c = f.read()
        page = browser.new_page(viewport={"width": 1080, "height": 1080}, device_scale_factor=2)
        page.set_content(c, wait_until="domcontentloaded")
        page.wait_for_timeout(400)
        page.screenshot(path=os.path.join(OUT, pn), full_page=False, omit_background=False, timeout=15000)
        print(f"OK {pn}")
        page.close()
    browser.close()
print("DONE")
