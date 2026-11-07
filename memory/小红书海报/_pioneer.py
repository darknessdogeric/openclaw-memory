"""小红书笔记图 - 先驱者系列 (9:16)
范式: 自建 v3.2 (大字号 + 浅/深底 + 单一强调色 + 5段/6段信息结构)
主题: 深空探测 -> 深空底 + 金线 + 星点
"""
import os
import random
import sys
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

OUT = r"C:\Users\ericz\Desktop\小红书_先驱者系列_2026-10-24"
os.makedirs(OUT, exist_ok=True)

THEMES = {
    "space":  {"bg": "#0E1626", "fg": "#E8E4DA", "ac": "#D4A74A", "dim": "#6E7A92", "card": "#182338"},
    "ember":  {"bg": "#0B0D12", "fg": "#EDE7DA", "ac": "#E08A4B", "dim": "#6B6A66", "card": "#161A22"},
    "paper":  {"bg": "#F4F1EA", "fg": "#16233A", "ac": "#C07C3E", "dim": "#8A8578", "card": "#FFFFFF"},
}

CN = ('"PingFang SC","Microsoft YaHei","Noto Sans SC",'
      '"Source Han Sans SC","SimHei",sans-serif')


def stars(bg, n=90):
    """生成星点 SVG (克制, 不喧宾夺主)"""
    random.seed(1972)
    out = []
    for _ in range(n):
        x = random.randint(0, 1080)
        y = random.randint(0, 1920)
        r = random.choice([1, 1, 1.2, 1.5, 2, 2.6])
        o = round(random.uniform(0.12, 0.55), 2)
        out.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFFFFF" opacity="{o}"/>')
    return "".join(out)


TPL = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="UTF-8">
<style>
  *{margin:0;padding:0;box-sizing:border-box;}
  body{width:1080px;height:1920px;background:__BG__;color:__FG__;overflow:hidden;
       font-family:__FONT__;}
  .stars{position:absolute;inset:0;z-index:0;}
  .sec{position:relative;z-index:1;width:100%;padding:26px 50px;
       display:flex;flex-direction:column;justify-content:center;gap:10px;}
  .s1{height:392px;padding-top:58px;}
  .s2{height:440px;}
  .s3{height:320px;}
  .s4{height:250px;}
  .s5{height:318px;}
  .s6{height:200px;justify-content:flex-end;}
  .kicker{font-size:19px;color:__AC__;letter-spacing:5px;font-weight:700;}
  h1{font-size:58px;font-weight:900;line-height:1.16;letter-spacing:1px;margin:10px 0 0;}
  h1 .hl{color:__AC__;}
  .sub{font-size:21px;color:__DIM__;line-height:1.45;margin-top:10px;}
  h2{font-size:31px;font-weight:800;color:__FG__;letter-spacing:1px;display:flex;
     align-items:center;gap:9px;margin-bottom:4px;}
  h2 .num{font-size:13px;font-weight:700;color:__AC__;background:rgba(212,167,74,0.14);
          padding:2px 8px;border-radius:4px;letter-spacing:1px;}
  b{color:__AC__;font-weight:700;}
  /* 时间线 */
  .tl{position:relative;padding-left:96px;margin-top:4px;}
  .tl::before{content:'';position:absolute;left:66px;top:14px;bottom:14px;width:3px;
              background:linear-gradient(180deg,__AC__ 0%,__DIM__ 100%);opacity:.55;}
  .node{position:relative;margin-bottom:13px;}
  .node:last-child{margin-bottom:0;}
  .node .yr{position:absolute;left:-96px;top:0;width:62px;text-align:right;
            font-size:19px;font-weight:900;color:__AC__;}
  .node .dot{position:absolute;left:-22px;top:6px;width:15px;height:15px;border-radius:50%;
             background:__AC__;box-shadow:0 0 0 5px __BG__;}
  .node .who{font-size:20px;font-weight:800;color:__FG__;margin-bottom:2px;}
  .node .what{font-size:16px;color:__DIM__;line-height:1.4;}
  .node .why{font-size:16px;color:__FG__;line-height:1.4;margin-top:2px;}
  .node.handoff .dot{background:__FG__;width:19px;height:19px;left:-24px;top:4px;}
  .node.handoff .yr{color:__FG__;}
  .node.handoff .who{color:__AC__;}
  /* 对照表 */
  .cmp{width:100%;border-collapse:collapse;margin-top:2px;}
  .cmp th{font-size:16px;font-weight:800;color:__AC__;text-align:left;padding:8px 10px;
          border-bottom:2px solid __AC__;letter-spacing:1px;}
  .cmp td{font-size:16px;color:__FG__;padding:9px 10px;border-bottom:1px solid rgba(140,150,170,.16);
          line-height:1.35;vertical-align:top;}
  .cmp td.k{color:__DIM__;font-weight:700;font-size:15px;white-space:nowrap;}
  .cmp tr:last-child td{border-bottom:none;}
  .cmp .a{color:__AC__;font-weight:700;}
  .cmp .b2{color:__FG__;font-weight:700;}
  /* 铝板 */
  .plate{background:__CARD__;border:1px solid rgba(212,167,74,.34);border-radius:10px;
         padding:16px 18px;margin-top:4px;}
  .plate .it{display:flex;align-items:flex-start;gap:11px;padding:7px 0;
             border-bottom:1px solid rgba(140,150,170,.14);}
  .plate .it:last-child{border-bottom:none;}
  .plate .ic{font-size:20px;line-height:1.2;width:30px;flex:0 0 30px;text-align:center;}
  .plate .tx{font-size:17.5px;color:__FG__;line-height:1.4;}
  .plate .tx i{font-style:normal;color:__DIM__;font-size:15px;display:block;margin-top:2px;}
  /* 金句 */
  .quote{border-left:5px solid __AC__;padding:10px 0 10px 20px;}
  .quote .q1{font-size:31px;font-weight:800;line-height:1.42;color:__FG__;}
  .quote .q2{font-size:31px;font-weight:800;line-height:1.42;color:__AC__;margin-top:8px;}
  .quote .q3{font-size:18px;color:__DIM__;margin-top:12px;line-height:1.45;}
  .foot{display:flex;align-items:flex-end;justify-content:space-between;
        border-top:2px solid rgba(212,167,74,.4);padding-top:14px;margin-top:6px;}
  .foot .tg{font-size:14px;color:__DIM__;line-height:1.55;letter-spacing:.5px;text-align:right;}
  .foot .src{font-size:14px;color:__DIM__;line-height:1.5;max-width:520px;}
  .brand{position:absolute;top:12px;right:12px;z-index:10;width:58px;height:58px;
         border-radius:9px;background:rgba(212,167,74,.92);border:1.5px solid __BG__;
         display:flex;flex-direction:column;align-items:center;justify-content:center;}
  .brand .bn{font-size:23px;font-weight:900;color:__BG__;line-height:1;}
  .brand .bl{font-size:7px;color:__BG__;letter-spacing:1.2px;margin-top:2px;line-height:1;}
  .wm{position:absolute;bottom:7px;left:14px;z-index:10;font-size:9.5px;color:__DIM__;opacity:.6;
      letter-spacing:1.7px;font-family:'Courier New',monospace;}
</style></head>
<body>
<svg class="stars" viewBox="0 0 1080 1920">__STARS__</svg>

<div class="sec s1">
  <div class="kicker">先驱者系列 · 1972 — 1992</div>
  <h1>他们替旅行者号<br>推开<span class="hl">每一道门</span><br>然后再没出声</h1>
  <div class="sub">人类深空探索史上最沉默的两位先驱</div>
</div>

<div class="sec s2">
  <h2><span class="num">01</span>接力时间线: 他们先走，我们后到</h2>
  <div class="tl">
    <div class="node">
      <div class="yr">1972</div><div class="dot"></div>
      <div class="who">先驱者 10 号 · 穿越小行星带</div>
      <div class="what">人类此前<b>不知道</b>小行星带能不能穿过去</div>
      <div class="why">他进去、出来了 —— 于是所有人都可以走了</div>
    </div>
    <div class="node">
      <div class="yr">1973</div><div class="dot"></div>
      <div class="who">先驱者 10 号 · 闯入木星辐射带</div>
      <div class="what">人类此前<b>不知道</b>木星辐射有多致命</div>
      <div class="why">挨了 <b>500 倍</b>致死剂量，把数字带回来 → 旅行者据此重新设计</div>
    </div>
    <div class="node">
      <div class="yr">1974</div><div class="dot"></div>
      <div class="who">先驱者 11 号 · 更贴近木星</div>
      <div class="what">明知道那里有多毒，<b>还贴得更近</b>、多挨几倍</div>
      <div class="why">只为拐出一个能到土星的弯</div>
    </div>
    <div class="node">
      <div class="yr">1979</div><div class="dot"></div>
      <div class="who">先驱者 11 号 · 穿越土星环平面</div>
      <div class="what">人类此前<b>不知道</b>穿环平面会不会被打死</div>
      <div class="why">他替旅行者把那条路<b>先走了一遍</b></div>
    </div>
    <div class="node handoff">
      <div class="yr">1980</div><div class="dot"></div>
      <div class="who">旅行者 1 / 2 号 · 顺利飞过土星</div>
      <div class="what">1980 与 1981 年，<b>先后</b>顺利飞过土星</div>
      <div class="why">1 号拍下<b>暗淡蓝点</b> · 2 号唯一一次看清<b>天王星与海王星</b></div>
    </div>
  </div>
</div>

<div class="sec s3">
  <h2><span class="num">02</span>两代探测器: 一个沉默，一个仍在线</h2>
  <table class="cmp">
    <tr><th style="width:20%"></th><th style="width:40%">先驱者 10 / 11 号</th><th style="width:40%">旅行者 1 / 2 号</th></tr>
    <tr><td class="k">现在</td>
      <td class="a">仍在飞，但已失联</td>
      <td class="b2">飞出太阳系，仍在发信号</td></tr>
    <tr><td class="k">方向</td>
      <td>朝毕宿五 / 盾牌座</td>
      <td>星际空间深处</td></tr>
    <tr><td class="k">铭牌</td>
      <td>两块<b>一模一样的</b>镀金铝板</td>
      <td>—</td></tr>
    <tr><td class="k">代价</td>
      <td class="a">替所有人试错，自己失联</td>
      <td class="b2">坐享其成，继续向前</td></tr>
  </table>
</div>

<div class="sec s4">
  <h2><span class="num">03</span>那块镀金铝板上刻着什么</h2>
  <div class="plate">
    <div class="it"><div class="ic">◉</div><div class="tx">氢原子<i>太阳的成分 · 一切元素的起点</i></div></div>
    <div class="it"><div class="ic">✦</div><div class="tx">14 颗脉冲星<i>在没有参照的深空里，指出你在哪</i></div></div>
    <div class="it"><div class="ic">✋</div><div class="tx">一个举手的人<i>据卡尔·萨根：那是「你好」，也可以理解成「再见」</i></div></div>
  </div>
</div>

<div class="sec s5">
  <h2><span class="num">04</span>他们没能说完的最后一句</h2>
  <div class="quote">
    <div class="q1">走在最前面的那个，</div>
    <div class="q1">往往是被记得最少的那个。</div>
    <div class="q2">因为他的工作，就是让后面的路变得不值一提。</div>
    <div class="q3">我们算得出他们大概飞到哪儿，<br>却再也没法确认 —— 因为确认这件事，需要他们说话，<br>而他们已经不能说话了。</div>
  </div>
</div>

<div class="sec s6">
  <div class="foot">
    <div class="src">先驱者 10 / 11 号<br>1972–1992 · NASA</div>
    <div class="tg">#深空探索 #先驱者号 #旅行者号 #NASA<br>#科普 #人类探索史 #淡淡的蓝点</div>
  </div>
</div>

<div class="brand"><div class="bn">B</div><div class="bl">B166ER</div></div>
<div class="wm">B166ER · 2026-10-24 · 先驱者系列</div>
</body></html>"""


def hex2rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


jobs = []
for tname, p in THEMES.items():
    html = (TPL.replace("__STARS__", stars(p["bg"]))
                .replace("__BG__", p["bg"]).replace("__FG__", p["fg"])
                .replace("__AC__", p["ac"]).replace("__DIM__", p["dim"])
                .replace("__CARD__", p["card"]).replace("__FONT__", CN))
    assert "__" not in html.split("<body>")[0], "占位符残留"
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
        c2 = im.getpixel((w - 6, h - 6))
        ok = sum(abs(a - b) for a, b in zip(c1, want)) < 22 and \
             sum(abs(a - b) for a, b in zip(c2, want)) < 22
        print(f"{'OK ' if ok else 'BAD'} {pn}  size={im.size}  bg实测{c1}")
    browser.close()
print("DONE ->", OUT)
