"""微信头像 4 方案 × 3 配色 = 12 张 (1080x1080 @2x)
设计依据: 浅底高对比 + 极简符号 + 单点金饰 + 圆形裁切安全区
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

def body_s1(bg, main, acc):
    return """
    <div class="mark s1">
      <div class="hline"></div>
      <div class="vline"></div>
      <div class="dot"></div>
    </div>"""

def body_s2(bg, main, acc):
    return """
    <div class="mark s2">
      <div class="char">实</div>
      <div class="uline"></div>
    </div>"""

def body_s3(bg, main, acc):
    return """
    <div class="mark s3">
      <div class="gate">
        <div class="post left"></div>
        <div class="post right"></div>
        <div class="lintel"></div>
      </div>
      <div class="flow"></div>
    </div>"""

def body_s4(bg, main, acc):
    return """
    <div class="mark s4">
      <div class="p1"></div>
      <div class="p2"></div>
      <div class="p3"></div>
      <div class="pl p1l"></div>
      <div class="pl p2l"></div>
      <div class="pl p3l"></div>
      <div class="goal"></div>
    </div>"""

SCHEMES = {
    "S1_定位落点": body_s1,
    "S2_实字":     body_s2,
    "S3_人流切口": body_s3,
    "S4_三点汇聚": body_s4,
}

TPL = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<style>
  *{margin:0;padding:0;box-sizing:border-box;}
  body{
    width:1080px;height:1080px;
    background:__BG__;
    font-family:"PingFang SC","Microsoft YaHei","Noto Sans SC",sans-serif;
    display:flex;align-items:center;justify-content:center;
    position:relative;overflow:hidden;
  }
  .mark{width:100%;height:100%;position:relative;display:flex;
        align-items:center;justify-content:center;}

  .s1 .hline{position:absolute;left:13%;right:13%;top:63%;height:4px;background:__MAIN__;opacity:.88;}
  .s1 .vline{position:absolute;top:15%;bottom:15%;left:47%;width:4px;background:__MAIN__;opacity:.88;}
  .s1 .dot{position:absolute;left:47%;top:63%;width:158px;height:158px;margin:-79px 0 0 -79px;
           background:__ACC__;border-radius:50%;box-shadow:0 0 0 24px __BG__;}

  .s2{flex-direction:column;}
  .s2 .char{font-size:530px;font-weight:900;color:__MAIN__;line-height:.92;letter-spacing:0;}
  .s2 .uline{width:158px;height:12px;background:__ACC__;margin-top:28px;border-radius:2px;}

  .s3{flex-direction:column;}
  .s3 .gate{position:relative;width:410px;height:440px;}
  .s3 .post{position:absolute;bottom:0;width:48px;background:__MAIN__;}
  .s3 .post.left{left:0;height:390px;}
  .s3 .post.right{right:0;height:335px;}
  .s3 .lintel{position:absolute;top:0;left:0;right:0;height:48px;background:__MAIN__;}
  .s3 .flow{width:158px;height:158px;background:__ACC__;border-radius:50%;
            margin-top:66px;box-shadow:0 0 0 22px __BG__;}

  .s4 .p1,.s4 .p2,.s4 .p3{position:absolute;width:78px;height:78px;background:__MAIN__;border-radius:50%;}
  .s4 .p1{left:23%;top:23%;}
  .s4 .p2{left:19%;bottom:25%;}
  .s4 .p3{right:23%;top:45%;}
  .s4 .pl{position:absolute;height:4px;background:__MAIN__;opacity:.6;transform-origin:left center;}
  .s4 .p1l{left:28%;top:30%;width:235px;transform:rotate(20deg);}
  .s4 .p2l{left:26%;bottom:29%;width:255px;transform:rotate(-26deg);}
  .s4 .p3l{right:27%;top:52%;width:225px;transform:rotate(200deg);}
  .s4 .goal{position:absolute;left:50%;top:50%;width:165px;height:165px;margin:-82px 0 0 -82px;
            background:__ACC__;border-radius:50%;box-shadow:0 0 0 22px __BG__;}
</style></head>
<body>__BODY__</body></html>"""

jobs = []
for sname, fn in SCHEMES.items():
    for tname, (bg, main, acc) in THEMES.items():
        html = (TPL.replace("__BG__", bg).replace("__MAIN__", main)
                    .replace("__ACC__", acc).replace("__BODY__", fn(bg, main, acc)))
        fname = f"微信头像_{sname}_{tname}.html"
        with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
            f.write(html)
        jobs.append((os.path.join(OUT, fname), f"微信头像_{sname}_{tname}.png"))

with sync_playwright() as p:
    browser = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
    for src, dstname in jobs:
        png = os.path.join(OUT, dstname)
        with open(src, encoding="utf-8") as f:
            c = f.read()
        page = browser.new_page(viewport={"width": 1080, "height": 1080}, device_scale_factor=2)
        page.set_content(c, wait_until="domcontentloaded")
        page.wait_for_timeout(400)
        page.screenshot(path=png, full_page=False, omit_background=False, timeout=15000)
        print(f"OK {dstname}  {os.path.getsize(png):,} bytes")
        page.close()
    browser.close()

print(f"\nDESKTOP {OUT}")
print("DONE")
