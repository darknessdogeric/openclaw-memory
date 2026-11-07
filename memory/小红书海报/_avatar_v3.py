"""微信头像 v3 — 用 open-design craft 规则 + 东方美学重做
规则来源: craft/color.md (中性70-90%, 单一强调色, 对比度>=4.5:1)
         craft/typography.md (字阶/留白)
         taste-skill (反模板化, 不要"标准答案感")
设计目标: 40px 微信列表尺寸仍可辨; 留白>装饰; 一个形说一件事
"""
import os
from playwright.sync_api import sync_playwright

OUT = r"C:\Users\ericz\Desktop\微信头像_v3_2026-10-24"
os.makedirs(OUT, exist_ok=True)

# ── 4 个方案 ──
# A 墨与朱印   : 宣纸白 + 墨黑字 + 朱砂方印 (东方美学, 名字即标识)
# B 定位十字    : 十字坐标不等长 (像地图定位) + 单一朱砂落点 (位置决定命运)
# C 双点弧线    : 两点一弧 (匹配式: 需求→匹配) + 金色中点
# D 纯印极简   : 深墨底 + 米白字, 无任何附加 (侘寂)

PALETTE = {
    "dunhuang": {"bg": "#F5F2EC", "fg": "#1F2422", "ac": "#B5432F"},   # 宣纸/墨/朱砂
    "indigo":   {"bg": "#F2EDE3", "fg": "#1E3A5F", "ac": "#C8963E"},   # 米白/靛蓝/金
    "mint":     {"bg": "#EFF5F2", "fg": "#1B3A34", "ac": "#C8963E"},   # 淡青/松绿/金
    "gold":     {"bg": "#1B3A34", "fg": "#E8DCC8", "ac": "#D4A74A"},   # 深墨/米白/金
}

CN_FONT = ('"PingFang SC","Microsoft YaHei","Noto Sans SC",'
           '"Source Han Sans SC","Source Han Serif SC","SimHei",sans-serif')


def svg_head(bg, fg, ac):
    return f'''<svg viewBox="0 0 1080 1080" width="1080" height="1080" xmlns="http://www.w3.org/2000/svg">
<rect width="1080" height="1080" fill="{bg}"/>'''


def scheme_A(bg, fg, ac):
    """墨与朱印: 超粗「实」+ 右下朱砂方印"""
    return f'''
<div class="mark">
  <div class="word">实</div>
  <div class="seal"><span>B</span></div>
</div>'''


def scheme_B(bg, fg, ac):
    """定位十字: 不等长十字 (地图定位感) + 朱砂落点"""
    return f'''
<div class="mark">
  <svg viewBox="0 0 1080 1080" width="1080" height="1080">
    <rect width="1080" height="1080" fill="{bg}"/>
    <line x1="150" y1="640" x2="930" y2="640" stroke="{fg}" stroke-width="9" opacity="0.92"/>
    <line x1="505" y1="130" x2="505" y2="870" stroke="{fg}" stroke-width="9" opacity="0.92"/>
    <circle cx="505" cy="640" r="74" fill="{ac}"/>
    <circle cx="505" cy="640" r="106" fill="none" stroke="{ac}" stroke-width="7" opacity="0.34"/>
  </svg>
</div>'''


def scheme_C(bg, fg, ac):
    """双点弧线: 需求→匹配 (AHL 匹配式范式)"""
    return f'''
<div class="mark">
  <svg viewBox="0 0 1080 1080" width="1080" height="1080">
    <rect width="1080" height="1080" fill="{bg}"/>
    <path d="M 268 762 Q 540 300 812 640" fill="none" stroke="{fg}" stroke-width="10"
          stroke-linecap="round" opacity="0.9"/>
    <circle cx="268" cy="762" r="52" fill="{fg}"/>
    <circle cx="812" cy="640" r="52" fill="{fg}"/>
    <circle cx="540" cy="470" r="86" fill="{ac}"/>
  </svg>
</div>'''


def scheme_D(bg, fg, ac):
    """纯印极简: 深墨底 + 米白「实」, 无任何附加"""
    return f'''
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

# 方案 -> 配色组合
JOBS = [
    ("A_墨与朱印", scheme_A, ["dunhuang"]),
    ("B_定位十字", scheme_B, ["dunhuang", "indigo", "mint"]),
    ("C_双点弧线", scheme_C, ["dunhuang", "indigo", "mint"]),
    ("D_纯印极简", scheme_D, ["gold"]),
]

jobs = []
for sname, fn, themes in JOBS:
    for t in themes:
        bg, fg, ac = PALETTE[t]
        html = (TPL.replace("__BODY__", fn(bg, fg, ac))
                    .replace("__BG__", bg).replace("__FG__", fg)
                    .replace("__AC__", ac).replace("__FONT__", CN_FONT))
        hname = f"头像v3_{sname}_{t}.html"
        with open(os.path.join(OUT, hname), "w", encoding="utf-8") as f:
            f.write(html)
        jobs.append((hname, f"头像v3_{sname}_{t}.png"))

with sync_playwright() as p:
    browser = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
    for hn, pn in jobs:
        with open(os.path.join(OUT, hn), encoding="utf-8") as f:
            c = f.read()
        page = browser.new_page(viewport={"width": 1080, "height": 1080}, device_scale_factor=2)
        page.set_content(c, wait_until="domcontentloaded")
        page.wait_for_timeout(400)
        page.screenshot(path=os.path.join(OUT, pn), full_page=False,
                        omit_background=False, timeout=15000)
        print(f"OK {pn}")
        page.close()
    browser.close()
print(f"DONE -> {OUT}")
