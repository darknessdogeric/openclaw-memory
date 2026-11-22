# -*- coding: utf-8 -*-
"""先驱者系列 · 小红书多图研报笔记 (6 图)
范式: rules-XHS-多图研报笔记 (R34) + geo_v4_mckinsey.py 的 COMMON_CSS / render / pil_watermark
画布 1080x1440 (3:4) | 白底 #FFFFFF + 深蓝 #0A2540 + 红 #C8102E
"""
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

BOX = Path(r"D:\B166ER-openclaw\workspace\toolbox")
GEO = BOX / "geo_v4_mckinsey.py"
OUT_DIR = Path(r"D:\B166ER-openclaw\workspace\output\xhs_pioneer_2026-11-01")
OUT_DIR.mkdir(parents=True, exist_ok=True)
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# CSS 直接从定稿 master 提取, 不复制粘贴, 避免漂移
_g = GEO.read_text(encoding="utf-8")
COMMON_CSS = _g.split('COMMON_CSS = """', 1)[1].split('"""', 1)[0]

TOTAL = 6
ISSUE = "2026.11.01 · ISSUE NO.001"
SOURCE = "SOURCE: B166ER · 深度探索观察"

SLIDE_01 = """
<div>
  <div class="eyebrow">EXECUTIVE BRIEFING · 摘要</div>
  <h1>他们替旅行者号<br/>推开<span class="red">每一道门</span><br/>然后再没出声</h1>
  <div class="accent-bar"></div>
  <div style="font-size: 28px; color: #5A6B7D; margin-top: 28px; font-style: italic; line-height: 1.5;">
    先驱者 10 / 11 号 —— 人类深空探索史上最沉默的两位先驱
  </div>
</div>
<div class="data-callout">
  <div class="label">THE NUMBERS THAT MATTER</div>
  <div class="value">500<span class="unit">倍致死剂量</span></div>
  <div class="note">先驱者 10 号闯入木星辐射带时挨下的剂量 —— 人类第一次知道木星辐射有多致命。</div>
</div>
<div class="three-col">
  <div class="col">
    <div class="col-num">01 · 先行者</div>
    <div class="col-title">先驱者 10 / 11 号</div>
    <div class="col-body">1970 年代 NASA 人类第一代外太阳系探测器，任务是替后面的人把路走通。</div>
    <div class="col-stat">1972 — 1992</div>
  </div>
  <div class="col">
    <div class="col-num">02 · 探路</div>
    <div class="col-title">三道门</div>
    <div class="col-body">小行星带 · 木星辐射带 · 土星环平面 —— 每一道在当时都没有答案。</div>
    <div class="col-stat">1972 / 1973-74 / 1979</div>
  </div>
  <div class="col muted">
    <div class="col-num">03 · 接力者</div>
    <div class="col-title">旅行者 1 / 2 号</div>
    <div class="col-body">1980 年飞过土星，拍下暗淡蓝点，唯一一次看清天王星与海王星。</div>
    <div class="col-stat">1980 — 至今</div>
  </div>
</div>
"""

SLIDE_02 = """
<div>
  <div class="eyebrow">01 · THE PHENOMENON</div>
  <h2>每一行右侧那个问题，<br/>在当时都<span class="red">没有答案</span></h2>
  <div class="accent-bar"></div>
</div>
<div class="body-text">
  生存压力、地位竞争、资源不确定，长期塑造了人类的动机系统与社会行为。
  当物质条件接近极大满足、生存焦虑大幅消退时 —— 原先驱动行为的核心燃料开始失效。
</div>
<table class="editorial">
  <tr><th>年份</th><th>他们做了什么</th><th>人类此前不知道</th></tr>
  <tr><td>1972</td><td>先驱者 10 号穿越小行星带</td><td>能不能穿过去</td></tr>
  <tr><td>1973</td><td>先驱者 10 号闯入木星辐射带</td><td>辐射有多致命</td></tr>
  <tr><td>1974</td><td>先驱者 11 号更贴近木星</td><td>贴多近会死</td></tr>
  <tr><td>1979</td><td>先驱者 11 号穿越土星环平面</td><td>会不会被打死</td></tr>
  <tr><td>1980</td><td>旅行者 1 / 2 号顺利飞过土星</td><td>—— 门已经开了</td></tr>
</table>
<div style="border-left: 8px solid #C8102E; padding: 24px 30px; background: #FDF3F4;">
  <div style="font-size: 26px; color: #0A2540; line-height: 1.55;">
    人类此前<span class="red">不知道</span>小行星带能不能穿过去。<br/>
    他进去、出来了 —— 于是所有人都可以走了。
  </div>
</div>
"""

SLIDE_03 = """
<div>
  <div class="eyebrow">02 · THE FRAMEWORK</div>
  <h2>他们交付的从来不是探测器，<br/>是<span class="red">一串数字</span></h2>
  <div class="accent-bar"></div>
</div>
<div class="data-callout">
  <div class="label">THE CONVERSION</div>
  <div class="value" style="font-size: 62px;">未知 → 数字 → 通行许可</div>
  <div class="note">每一道门都是一次「先挨打」换来的通行许可：把「会死」这件模糊的事，试成具体数字，后来的机器才敢按这个数字重新设计。</div>
</div>
<div class="pullquote">
  明知道那里有多毒，还贴得更近、多挨几倍 —— 只为拐出一个能到土星的弯。
</div>
<div class="dark-callout">
  <div class="label">KEY INSIGHT</div>
  <div class="body">
    先驱者 10 号带回来的不是「木星很危险」这种结论，<br/>
    而是<span class="red-text">一个可写进设计图纸的剂量数字</span>。<br/>
    旅行者号据此重新设计 —— 它能成功，是因为有人先替它把危险量化了。
  </div>
</div>
"""

SLIDE_04 = """
<div>
  <div class="eyebrow">03 · THE THREE GATES</div>
  <h2>他们推开了哪三道门</h2>
  <div class="accent-bar"></div>
</div>
<div class="three-col">
  <div class="col">
    <div class="col-num">GATE 01</div>
    <div class="col-title">小行星带</div>
    <div class="col-keyword">能不能穿过去</div>
    <div class="col-body">1972 年先驱者 10 号直接穿了过去。此后再没有探测器需要担心这件事 —— 他们把它变成了路。</div>
    <div class="col-stat">1972 · 先驱者 10 号</div>
  </div>
  <div class="col">
    <div class="col-num">GATE 02</div>
    <div class="col-title">木星辐射带</div>
    <div class="col-keyword">辐射有多致命</div>
    <div class="col-body">1973 年挨了 500 倍致死剂量把数字带回来；1974 年 11 号贴得更近，只为多挨几倍，换一个能拐向土星的弯。</div>
    <div class="col-stat">1973-74 · 先驱者 10 / 11 号</div>
  </div>
  <div class="col">
    <div class="col-num">GATE 03</div>
    <div class="col-title">土星环平面</div>
    <div class="col-keyword">会不会被打死</div>
    <div class="col-body">1979 年先驱者 11 号替旅行者把那条路先走了一遍。1980 年旅行者 1 / 2 号飞过时，它面对的是一条被走通的航线。</div>
    <div class="col-stat">1979 · 先驱者 11 号</div>
  </div>
</div>
<div class="pullquote">
  旅行者号不是第一个到土星的人 —— 只是第一个活着到的人。
</div>
"""

SLIDE_05 = """
<div>
  <div class="eyebrow">04 · THE IMPLICATION</div>
  <h2>他们推开的门，<br/>后来者<span class="red">不必再付代价</span></h2>
  <div class="accent-bar"></div>
</div>
<ol class="editorial">
  <li>他们承担的是不可逆的试错成本 —— 在 1970 年代，答案只能靠真的飞过去、真的挨一次。</li>
  <li>沉默不是失职，是任务本身：1970 年代还没有能跨星际可靠回传的系统，他们注定发不回有用的信号。</li>
  <li>后来者坐享其成 —— 但那份成，是前面两台机器拿失联换来的。</li>
</ol>
<div class="dark-callout">
  <div class="label">UNDERLYING CAUSE</div>
  <div class="body">
    走在最前面的那个，往往是被记得最少的那个。<br/>
    因为他的工作，就是让后面的路<span class="red-text">变得不值一提</span>。
  </div>
</div>
"""

SLIDE_06 = """
<div>
  <div class="eyebrow">05 · THE TAKEAWAY</div>
  <h2>他们替我们走完了<br/>最难的那一段</h2>
  <div class="accent-bar"></div>
</div>
<div class="dark-callout">
  <div class="label">CORE LAW</div>
  <div class="body">
    先驱者的账，由旅行者付；<br/>
    旅行者的账，由下一个先驱者付。<br/>
    <span class="red-text">账只会往下传，不会消失。</span>
  </div>
</div>
<div class="pullquote">
  <s style="color: #94A2B0;">我们算得出他们大概飞到哪儿</s><br/>
  却再也没法确认 —— 因为确认这件事需要他们说话，<br/>
  而他们已经不能说话了。
</div>
<div style="background: #F2F4F7; padding: 26px 32px;">
  <div style="font-size: 15px; color: #5A6B7D; letter-spacing: 4px; margin-bottom: 10px;">FORWARD LOOK</div>
  <div style="font-size: 26px; color: #0A2540; line-height: 1.5;">
    先驱者 10 / 11 号 · 1972—1992 · NASA<br/>
    两台机器，一个方向，同一段路的两种账。
  </div>
</div>
<div style="font-size: 21px; color: #5A6B7D; line-height: 1.6;">
  <span style="color: #C8102E; font-weight: 700;">DISCUSSION</span>
  如果你的团队正在替别人走一段没人走过的那段路 —— 这本笔记是写给你的。
</div>
"""

SLIDES = [SLIDE_01, SLIDE_02, SLIDE_03, SLIDE_04, SLIDE_05, SLIDE_06]


def render(idx, body_html):
    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>先驱者 Slide """ + str(idx) + """</title>
<style>""" + COMMON_CSS + """
</style>
</head>
<body>
<div class="slide">
  <div class="masthead">
    <div class="brand">B166ER · 商业内参</div>
    <div class="date">""" + ISSUE + """</div>
  </div>
  <div class="content">""" + body_html + """</div>
  <div class="footer">
    <div class="source">""" + SOURCE + """</div>
    <div class="page">""" + ("%02d / %02d" % (idx, TOTAL)) + """</div>
  </div>
</div>
</body>
</html>"""
    html_path = OUT_DIR / ("slide_%02d.html" % idx)
    png_path = OUT_DIR / ("slide_%02d.png" % idx)
    html_path.write_text(html, encoding="utf-8")
    r = subprocess.run([
        EDGE, "--headless=new", "--disable-gpu", "--no-sandbox",
        "--hide-scrollbars", "--force-device-scale-factor=2",
        "--window-size=1080,1440",
        "--screenshot=" + str(png_path),
        html_path.as_uri(),
    ], capture_output=True, text=True, timeout=60)
    sz = png_path.stat().st_size if png_path.exists() else 0
    print("Slide %02d: RC=%s, size=%s" % (idx, r.returncode, sz))
    return png_path


def pil_watermark(png_path):
    p = Path(png_path)
    wm = p.with_name(p.stem + "_wm.png")
    img = Image.open(p).convert("RGBA")
    w, h = img.size
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    try:
        font = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 22)
        font_tiny = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 18)
        font_big = ImageFont.truetype(r"C:\Windows\Fonts\msyhbd.ttc", 70)
    except Exception:
        font = ImageFont.load_default()
        font_tiny = font
        font_big = font
    draw.rectangle([(0, 50), (200, 100)], fill=(10, 37, 64, 200))
    draw.text((16, 64), "B166ER · GEO", fill=(255, 255, 255, 255), font=font)
    draw.text((w - 220, h - 34), "© B166ER · 2026.11.01", fill=(10, 37, 64, 240), font=font_tiny)
    wm_text = "B166ER · 2026.11.01"
    bbox = draw.textbbox((0, 0), wm_text, font=font_big)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    txt_img = Image.new("RGBA", (tw + 40, th + 40), (0, 0, 0, 0))
    td = ImageDraw.Draw(txt_img)
    td.text((20, 20), wm_text, fill=(200, 200, 200, 40), font=font_big)
    txt_img = txt_img.rotate(-22, expand=True)
    overlay.paste(txt_img, ((w - txt_img.size[0]) // 2, (h - txt_img.size[1]) // 2), txt_img)
    out = Image.alpha_composite(img, overlay).convert("RGB")
    out.save(wm, "PNG", optimize=True)
    return wm


if __name__ == "__main__":
    print("CSS chars:", len(COMMON_CSS))
    for i, b in enumerate(SLIDES, 1):
        p = render(i, b)
        w = pil_watermark(p)
        print("  WM:", w.name, w.stat().st_size)
    print("=== DONE ===", OUT_DIR)
