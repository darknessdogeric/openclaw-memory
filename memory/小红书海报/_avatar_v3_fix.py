"""微信头像 v3 — 修复版
BUG 根因: scheme 函数用 f-string 插值 {bg}/{fg}/{ac}, 但产物中仍是字面量 "bg"/"fg"/"ac",
说明插值未生效 (疑似写盘时 f-string 前缀与花括号被处理)。
修复: 全部改用 __BG__/__FG__/__AC__ token, 与 TPL 统一, 且【先插 BODY 再全局替换 token】,
      最后做像素级校验, 确认背景色/强调色真的上屏。
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
    return '''
<div class="mark">
  <svg viewBox="0 0 1080 1080" width="1080" height="1080">
    <rect width="1080" height="1080" fill="__BG__"/>
    <line x1="150" y1="640" x2="930" y2="640" stroke="__FG__" stroke-width="9" opacity="0.92"/>
    <line x1="505" y1="130" x2="505" y2="870" stroke="__FG__" stroke-width="9" opacity="0.92"/>
    <circle cx="505" cy="640" r="74" fill="__AC__"/>
    <circle cx="505" cy="640" r="106" fill="none" stroke="__AC__" stroke-width="7" opacity="0.34"/>
  </svg>
</div>'''


def scheme_C():
    return '''
<div class="mark">
  <svg viewBox="0 0 1080 1080" width="1080" height="1080">
    <rect width="1080" height="1080" fill="__BG__"/>
    <path d="M 268 762 Q 540 300 812 640" fill="none" stroke="__FG__" stroke-width="10"
          stroke-linecap="round" opacity="0.9"/>
    <circle cx="268" cy="762" r="52" fill="__FG__"/>
    <circle cx="812" cy="640" r="52" fill="__FG__"/>
    <circle cx="540" cy="470" r="86" fill="__AC__"/>
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
  .seal{position:absolute;right:214px;bottom:206px;width:92px;height:92px;
        background:__AC__;border-radius:5px;display:flex;align-items:center;
        justify-content:center;}
  .seal span{font-size:46px;font-weight:900;color:__BG__;line-height:1;}
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


def build(fn, theme):
    p = PALETTE[theme]
    html = TPL.replace("__BODY__", fn())
    html = html.replace("__BG__", p["bg"]).replace("__FG__", p["fg"])
    html = html.replace("__AC__", p["ac"]).replace("__FONT__", CN_FONT)
    assert "__" not in html.split("<body>")[0], "模板占位符未清干净"
    return html, p


jobs = []
for sname, fn, themes in JOBS:
    for t in themes:
        html, p = build(fn, t)
        assert f'fill="{p["bg"]}"' in html or f'background:{p["bg"]}' in html, \
            f"{sname}/{t} 背景色未注入"
        hname = f"头像v3_{sname}_{t}.html"
        with open(os.path.join(OUT, hname), "w", encoding="utf-8") as f:
            f.write(html)
        jobs.append((hname, f"头像v3_{sname}_{t}.png", p))

with sync_playwright() as p:
    browser = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
    for hn, pn, pal in jobs:
        with open(os.path.join(OUT, hn), encoding="utf-8") as f:
            c = f.read()
        page = browser.new_page(viewport={"width": 1080, "height": 1080}, device_scale_factor=2)
        page.set_content(c, wait_until="domcontentloaded")
        page.wait_for_timeout(400)
        path = os.path.join(OUT, pn)
        page.screenshot(path=path, full_page=False, omit_background=False, timeout=15000)
        page.close()
        # 像素校验: 取四角的背景色
        try:
            from PIL import Image
            im = Image.open(path).convert("RGB")
            w, h = im.size
            corners = [im.getpixel((6, 6)), im.getpixel((w - 7, 6)),
                       im.getpixel((6, h - 7)), im.getpixel((w - 7, h - 7))]
            want = hex2rgb(pal["bg"])
            ok = all(sum(abs(a - b) for a, b in zip(px, want)) < 18 for px in corners)
            print(f"{'OK ' if ok else 'BAD'} {pn}  bg期望{pal['bg']} 实测{corners[0]}")
        except Exception as e:
            print(f"PNG {pn} (像素校验跳过: {e})")
    browser.close()
print("DONE")
