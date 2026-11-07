"""先驱者系列 小红书笔记图 v3 — 修集成版重叠
根因: 内联 SVG 按固有 width/height (980x420) 渲染, 撑破定高 section
修复: .fig 给固定像素高 + svg{width:100%;height:100%} (preserveAspectRatio 默认 meet 自动 letterbox)
      段高重新分配, 合计精确 1920
"""
import os
import sys

sys.path.insert(0, r"D:\B166ER-openclaw\workspace\memory\小红书海报")

from playwright.sync_api import sync_playwright
from _illustrations import solar_svg, plaque_svg, probe_svg

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
OUT = r"C:\Users\ericz\Desktop\小红书_先驱者系列_2026-10-24"
os.makedirs(OUT, exist_ok=True)

THEMES = {
    "space": {"bg": "#0E1626", "fg": "#E8E4DA", "ac": "#D4A74A", "dim": "#6E7A92"},
    "ember": {"bg": "#0B0D12", "fg": "#EDE7DA", "ac": "#E08A4B", "dim": "#6B6A66"},
    "paper": {"bg": "#F4F1EA", "fg": "#16233A", "ac": "#C07C3E", "dim": "#8A8578"},
}
CN = ('"PingFang SC","Microsoft YaHei","Noto Sans SC",'
      '"Source Han Sans SC","SimHei",sans-serif')

# 段高 (合计必须 = 1920)
H = {"s1": 262, "s2": 262, "s3": 418, "s4": 232, "s5": 214, "s6": 262, "s7": 270}
FIG_H = {"probe": 155, "solar": 150, "plaque": 185}

TPL = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<style>
  *{margin:0;padding:0;box-sizing:border-box;}
  body{width:1080px;height:1920px;background:__BG__;color:__FG__;overflow:hidden;
       font-family:__FONT__;}
  .stars{position:absolute;inset:0;z-index:0;}
  .sec{position:relative;z-index:1;width:100%;padding:22px 46px;
       display:flex;flex-direction:column;justify-content:center;gap:6px;overflow:hidden;}
  .s1{height:__H_s1__px;padding-top:52px;}
  .s2{height:__H_s2__px;}
  .s3{height:__H_s3__px;}
  .s4{height:__H_s4__px;}
  .s5{height:__H_s5__px;}
  .s6{height:__H_s6__px;}
  .s7{height:__H_s7__px;justify-content:flex-end;}
  .kicker{font-size:18px;color:__AC__;letter-spacing:5px;font-weight:700;}
  h1{font-size:50px;font-weight:900;line-height:1.14;letter-spacing:0;margin:8px 0 0;}
  h1 .hl{color:__AC__;}
  .sub{font-size:19px;color:__DIM__;line-height:1.4;margin-top:6px;}
  h2{font-size:27px;font-weight:800;color:__FG__;letter-spacing:1px;display:flex;
     align-items:center;gap:9px;margin-bottom:0;}
  h2 .num{font-size:13px;font-weight:700;color:__AC__;background:rgba(212,167,74,.15);
          padding:2px 8px;border-radius:4px;letter-spacing:1px;}
  b{color:__AC__;font-weight:700;}
  /* 图区: 固定高 + SVG 强制 fit */
  .fig{width:100%;display:flex;align-items:center;justify-content:center;overflow:hidden;}
  .fig svg{width:100%;height:100%;display:block;}
  .cap{font-size:13.5px;color:__DIM__;text-align:center;line-height:1.4;}
  .tl{position:relative;padding-left:90px;}
  .tl::before{content:'';position:absolute;left:62px;top:10px;bottom:10px;width:3px;
              background:linear-gradient(180deg,__AC__ 0%,__DIM__ 100%);opacity:.55;}
  .node{position:relative;margin-bottom:6px;}
  .node:last-child{margin-bottom:0;}
  .node .yr{position:absolute;left:-90px;top:0;width:56px;text-align:right;
            font-size:17px;font-weight:900;color:__AC__;}
  .node .dot{position:absolute;left:-20px;top:4px;width:13px;height:13px;border-radius:50%;
             background:__AC__;box-shadow:0 0 0 5px __BG__;}
  .node .who{font-size:18px;font-weight:800;color:__FG__;line-height:1.35;margin-bottom:1px;}
  .node .what{font-size:15px;color:__DIM__;line-height:1.35;}
  .node .why{font-size:15px;color:__FG__;line-height:1.35;margin-top:1px;}
  .node.handoff .dot{background:__FG__;width:17px;height:17px;left:-22px;top:2px;}
  .node.handoff .yr{color:__FG__;}
  .node.handoff .who{color:__AC__;}
  .cmp{width:100%;border-collapse:collapse;}
  .cmp th{font-size:15px;font-weight:800;color:__AC__;text-align:left;padding:7px 9px;
          border-bottom:2px solid __AC__;letter-spacing:1px;}
  .cmp td{font-size:15px;color:__FG__;padding:8px 9px;
          border-bottom:1px solid rgba(140,150,170,.16);line-height:1.3;vertical-align:top;}
  .cmp td.k{color:__DIM__;font-weight:700;font-size:14px;white-space:nowrap;}
  .cmp tr:last-child td{border-bottom:none;}
  .cmp .a{color:__AC__;font-weight:700;}
  .cmp .b2{color:__FG__;font-weight:700;}
  .quote{border-left:5px solid __AC__;padding:4px 0 4px 18px;}
  .quote .q1{font-size:27px;font-weight:800;line-height:1.38;color:__FG__;}
  .quote .q2{font-size:27px;font-weight:800;line-height:1.38;color:__AC__;margin-top:5px;}
  .quote .q3{font-size:16px;color:__DIM__;margin-top:9px;line-height:1.42;}
  .foot{display:flex;align-items:flex-end;justify-content:space-between;
        border-top:2px solid rgba(212,167,74,.4);padding-top:11px;margin-top:10px;}
  .foot .src{font-size:13px;color:__DIM__;line-height:1.5;max-width:470px;}
  .foot .tg{font-size:13px;color:__DIM__;line-height:1.5;letter-spacing:.5px;text-align:right;}
  .brand{position:absolute;top:12px;right:12px;z-index:10;width:56px;height:56px;
         border-radius:9px;background:rgba(212,167,74,.92);border:1.5px solid __BG__;
         display:flex;flex-direction:column;align-items:center;justify-content:center;}
  .brand .bn{font-size:22px;font-weight:900;color:__BG__;line-height:1;}
  .brand .bl{font-size:7px;color:__BG__;letter-spacing:1.2px;margin-top:2px;line-height:1;}
  .wm{position:absolute;bottom:6px;left:14px;z-index:10;font-size:9px;color:__DIM__;opacity:.6;
      letter-spacing:1.7px;font-family:'Courier New',monospace;}
</style></head>
<body>
<svg class="stars" viewBox="0 0 1080 1920">__STARS__</svg>

<div class="sec s1">
  <div class="kicker">先驱者系列 · 1972 — 1992</div>
  <h1>他们替旅行者号推开<span class="hl">每一道门</span><br>然后再没出声</h1>
  <div class="sub">人类深空探索史上最沉默的两位先驱</div>
</div>

<div class="sec s2">
  <h2><span class="num">01</span>他们是谁</h2>
  <div class="fig" style="height:__FIG_probe__px;">__PROBE__</div>
  <div class="cap">先驱者 10 / 11 号 · 1970 年代 NASA · 人类第一代外太阳系探测器</div>
</div>

<div class="sec s3">
  <h2><span class="num">02</span>接力时间线: 他们先走，我们后到</h2>
  <div class="tl">
    <div class="node"><div class="yr">1972</div><div class="dot"></div>
      <div class="who">先驱者 10 号 · 穿越小行星带</div>
      <div class="what">人类此前<b>不知道</b>小行星带能不能穿过去</div>
      <div class="why">他进去、出来了 —— 于是所有人都可以走了</div></div>
    <div class="node"><div class="yr">1973</div><div class="dot"></div>
      <div class="who">先驱者 10 号 · 闯入木星辐射带</div>
      <div class="what">人类此前<b>不知道</b>木星辐射有多致命</div>
      <div class="why">挨了 <b>500 倍</b>致死剂量，把数字带回来 → 旅行者据此重新设计</div></div>
    <div class="node"><div class="yr">1974</div><div class="dot"></div>
      <div class="who">先驱者 11 号 · 更贴近木星</div>
      <div class="what">明知道那里有多毒，<b>还贴得更近</b>、多挨几倍</div>
      <div class="why">只为拐出一个能到土星的弯</div></div>
    <div class="node"><div class="yr">1979</div><div class="dot"></div>
      <div class="who">先驱者 11 号 · 穿越土星环平面</div>
      <div class="what">人类此前<b>不知道</b>穿环平面会不会被打死</div>
      <div class="why">他替旅行者把那条路<b>先走了一遍</b></div></div>
    <div class="node handoff"><div class="yr">1980</div><div class="dot"></div>
      <div class="who">旅行者 1 / 2 号 · 顺利飞过土星</div>
      <div class="what">1980 与 1981 年，<b>先后</b>飞过土星</div>
      <div class="why">1 号拍下<b>暗淡蓝点</b> · 2 号唯一一次看清<b>天王星与海王星</b></div></div>
  </div>
</div>

<div class="sec s4">
  <h2><span class="num">03</span>他们推开了哪几道门</h2>
  <div class="fig" style="height:__FIG_solar__px;">__SOLAR__</div>
</div>

<div class="sec s5">
  <h2><span class="num">04</span>两代探测器: 一个沉默，一个仍在线</h2>
  <table class="cmp">
    <tr><th style="width:18%"></th><th style="width:41%">先驱者 10 / 11 号</th><th style="width:41%">旅行者 1 / 2 号</th></tr>
    <tr><td class="k">现在</td><td class="a">仍在飞，但已失联</td><td class="b2">飞出太阳系，仍在发信号</td></tr>
    <tr><td class="k">方向</td><td>朝毕宿五 / 盾牌座</td><td>星际空间深处</td></tr>
    <tr><td class="k">代价</td><td class="a">替所有人试错，自己失联</td><td class="b2">坐享其成，继续向前</td></tr>
  </table>
</div>

<div class="sec s6">
  <h2><span class="num">05</span>那块镀金铝板上刻着什么</h2>
  <div class="fig" style="height:__FIG_plaque__px;">__PLAQUE__</div>
</div>

<div class="sec s7">
  <div class="quote">
    <div class="q1">走在最前面的那个，往往是被记得最少的那个。</div>
    <div class="q2">因为他的工作，就是让后面的路变得不值一提。</div>
    <div class="q3">我们算得出他们大概飞到哪儿，却再也没法确认 —— 因为确认这件事需要他们说话，<br>而他们已经不能说话了。</div>
  </div>
  <div class="foot">
    <div class="src">先驱者 10 / 11 号 · 1972–1992 · NASA<br>资料来源：《得到大脑》</div>
    <div class="tg">#深空探索 #先驱者号 #旅行者号 #NASA<br>#科普 #人类探索史 #淡淡的蓝点</div>
  </div>
</div>

<div class="brand"><div class="bn">B</div><div class="bl">B166ER</div></div>
<div class="wm">B166ER · 2026-10-21 · 先驱者系列</div>
</body></html>"""


def stars(n=110, seed=1972):
    import random
    random.seed(seed)
    out = []
    for _ in range(n):
        x = random.randint(0, 1080)
        y = random.randint(0, 1920)
        r = random.choice([1, 1, 1.2, 1.5, 2, 2.6])
        o = round(random.uniform(0.10, 0.5), 2)
        out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF" opacity="{o}"/>')
    return "".join(out)


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


assert sum(H.values()) == 1920, f"段高合计 {sum(H.values())} != 1920"

jobs = []
for tname, p in THEMES.items():
    html = (TPL.replace("__STARS__", stars())
                .replace("__PROBE__", probe_svg(fg=p["fg"], dim=p["dim"], ac=p["ac"]))
                .replace("__SOLAR__", solar_svg(fg=p["fg"], dim=p["dim"], ac=p["ac"]))
                .replace("__PLAQUE__", plaque_svg())
                .replace("__BG__", p["bg"]).replace("__FG__", p["fg"])
                .replace("__AC__", p["ac"]).replace("__DIM__", p["dim"])
                .replace("__FONT__", CN))
    for k, v in H.items():
        html = html.replace(f"__H_{k}__", str(v))
    for k, v in FIG_H.items():
        html = html.replace(f"__FIG_{k}__", str(v))
    assert "__" not in html.split("<body>")[0], "占位符残留: " + str(
        [t for t in ["__H_", "__FIG_", "__BG__", "__FG__", "__AC__", "__DIM__", "__FONT__", "__BODY__", "__STARS__"] if t in html])
    hname = f"先驱者_{tname}.html"
    with open(os.path.join(OUT, hname), "w", encoding="utf-8") as f:
        f.write(html)
    jobs.append((hname, f"先驱者_{tname}.png", p))

with sync_playwright() as pw:
    browser = pw.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
    from PIL import Image
    for hn, pn, p in jobs:
        with open(os.path.join(OUT, hn), encoding="utf-8") as f:
            c = f.read()
        page = browser.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=2)
        page.set_content(c, wait_until="domcontentloaded")
        page.wait_for_timeout(600)
        path = os.path.join(OUT, pn)
        page.screenshot(path=path, full_page=False, omit_background=False, timeout=20000)
        page.close()
        im = Image.open(path).convert("RGB")
        w, h = im.size
        want = hex2rgb(p["bg"])
        c1 = im.getpixel((5, 5))
        ok = sum(abs(a - b) for a, b in zip(c1, want)) < 22
        print(f"{'OK ' if ok else 'BAD'} {pn}  {im.size}  bg={c1}")
    browser.close()
print("DONE ->", OUT)
