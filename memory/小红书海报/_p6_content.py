# -*- coding: utf-8 -*-
"""先驱者系列 6 图笔记 - 内容"""
import os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _p6_lib import page, hero_b64, OUT

TAGS = "#深空探索 #先驱者号 #旅行者号 #NASA #科普 #人类探索史 #淡淡的蓝点"

P1 = dict(
  kicker="先驱者系列 · 1972 — 1992",
  title="""
<h1>他们替旅行者号推开<br><span class="hl">每一道门</span><br>然后再没出声</h1>
""",
  sub="人类深空探索史上最沉默的两位先驱",
  body="""
<div class="figw">__HERO__</div>
<div class="row3">
  <div class="g3c acc"><div class="k">先行者</div><div class="v">10 / 11</div>
    <div class="d">人类第一代外太阳系探测器</div></div>
  <div class="g3c"><div class="k">探路年份</div><div class="v">1972</div>
    <div class="d">小行星带、木星辐射带、土星环平面</div></div>
  <div class="g3c"><div class="k">接力者</div><div class="v">1980</div>
    <div class="d">旅行者号随后顺利飞过土星</div></div>
</div>
<div class="card acc"><div class="t">一句话读懂<span class="tag">全文主线</span></div>
  <div class="d">他们不是终点，是<b>探路的</b>。每一道门，都是他们先挨过一遍；
  我们算得出他们飞到哪儿，却再也没法确认 —— 因为确认这件事需要他们说话。</div></div>
""",
  foot_q="走在最前面的那个，往往是<b>被记得最少的那个</b>。",
  foot_s="资料来源：《得到大脑》 · 先驱者 10/11 号 · NASA | " + TAGS,
)

P2 = dict(
  kicker="先驱者系列 · 身份",
  title="""
<h2><span class="num">01</span>他们是谁</h2>
""",
  sub="1970 年代 NASA · 人类第一代外太阳系探测器",
  body="""
<div class="bigline"><div class="n">先驱者 10 / 11 号</div>
  <div class="u">两台被派出去<b>试错</b>的机器，任务只有一个：替后面的人把路走通</div></div>
<div class="row2">
  <div class="card"><div class="t">先驱者 10 号<span class="tag">方向</span></div>
    <div class="d">朝<b>毕宿五</b>。1972 年穿越小行星带，1973 年闯入木星辐射带 ——
    带着 500 倍致死剂量的数字回来。</div></div>
  <div class="card"><div class="t">先驱者 11 号<span class="tag">方向</span></div>
    <div class="d">朝<b>盾牌座</b>。1974 年更贴近木星，1979 年穿越土星环平面 ——
    明知道那里有毒，还是贴得更近。</div></div>
</div>
<div class="card acc"><div class="t">他们为什么沉默<span class="tag">前提</span></div>
  <div class="d">1970 年代的深空探测还<b>没有能跨星际可靠回传的系统</b>。
  这两台机器注定发不回有用的信号 —— 它们出发的那一刻，就已经把「报告」这件事让渡给了后来者。</div></div>
<div class="tl">
  <div class="tlrow"><div class="yr">核心</div><div class="tx">
    <div class="h">他们承担的是「不可逆的试错成本」</div>
    <div class="p">木星辐射有多致命、土星环平面能不能穿 —— <b>在 1970 年代没有答案</b>，
    而答案只能靠真的飞过去、真的挨一次。</div>
    <div class="q">这就是「先驱者」两个字的分量：不是荣誉，是岗位。</div>
  </div></div>
</div>
""",
  foot_q="他们的任务不是抵达，是<b>把「不知道」变成「知道」</b>。",
  foot_s="先驱者 10/11 号 · 1970s · NASA | 资料来源：《得到大脑》",
)

P3 = dict(
  kicker="先驱者系列 · 接力时间线",
  title="""
<h2><span class="num">02</span>接力时间线：他们先走，我们后到</h2>
""",
  sub="每一步，都是先替后面的人把「不知道」走成「知道」",
  body="""
<div class="tl">
  <div class="tlrow"><div class="yr">1972</div><div class="tx">
    <div class="h">先驱者 10 号 · 穿越小行星带</div>
    <div class="p">人类此前<b>不知道</b>小行星带能不能穿过去</div>
    <div class="q">他进去、出来了 —— 于是所有人都可以走了</div>
  </div></div>
  <div class="tlrow"><div class="yr">1973</div><div class="tx">
    <div class="h">先驱者 10 号 · 闯入木星辐射带</div>
    <div class="p">人类此前<b>不知道</b>木星辐射有多致命</div>
    <div class="q">挨了 500 倍致死剂量，把数字带回来 → 旅行者据此重新设计</div>
  </div></div>
  <div class="tlrow"><div class="yr">1974</div><div class="tx">
    <div class="h">先驱者 11 号 · 更贴近木星</div>
    <div class="p">明知道那里有多毒，<b>还贴得更近、多挨几倍</b></div>
    <div class="q">只为拐出一个能到土星的弯</div>
  </div></div>
  <div class="tlrow"><div class="yr">1979</div><div class="tx">
    <div class="h">先驱者 11 号 · 穿越土星环平面</div>
    <div class="p">人类此前<b>不知道</b>穿环平面会不会被打死</div>
    <div class="q">他替旅行者把那条路先走了一遍</div>
  </div></div>
  <div class="tlrow"><div class="yr">1980</div><div class="tx">
    <div class="h">旅行者 1 / 2 号 · 顺利飞过土星</div>
    <div class="p">1980 与 1981 年，先后飞过土星</div>
    <div class="q">1 号拍下暗淡蓝点 · 2 号唯一一次看清天王星与海王星</div>
  </div></div>
</div>
<div class="card acc"><div class="t">这条线的形状<span class="tag">看懂它</span></div>
  <div class="d">他们走的不是同一条路，是<b>一条一条把未知清空</b>：小行星带 → 木星辐射 → 土星环。
  旅行者号之所以敢去，是因为前面每一次都有人替它把「会死」这件事试成了具体数字。</div></div>
""",
  foot_q="他们先走，我们后到 —— <b>差别只在于谁替谁挨过</b>。",
  foot_s="先驱者 10/11 号 · 1972—1981 · NASA | 资料来源：《得到大脑》",
)

SOLAR_SVG = """
<svg viewBox="0 0 900 236" width="900" height="236" xmlns="http://www.w3.org/2000/svg">
  <line x1="30" y1="112" x2="880" y2="112" stroke="rgba(233,228,218,.16)" stroke-width="1"/>
  <g text-anchor="middle" font-size="15" fill="#a8a094" font-family="Noto Sans SC">
    <text x="48" y="86">太阳</text>
    <text x="152" y="86">水星</text>
    <text x="252" y="86">金星</text>
    <text x="352" y="86">地球</text>
    <text x="452" y="86">火星</text>
    <text x="600" y="86">木星</text>
    <text x="730" y="86">土星</text>
  </g>
  <circle cx="48" cy="112" r="17" fill="#e8b478" opacity="0.9"/>
  <circle cx="152" cy="112" r="5" fill="#c3bcb0"/>
  <circle cx="252" cy="112" r="8" fill="#c3bcb0"/>
  <circle cx="352" cy="112" r="8" fill="#6fa8c7"/>
  <circle cx="452" cy="112" r="6" fill="#c0705a"/>
  <circle cx="600" cy="112" r="17" fill="#c9a06a"/>
  <circle cx="730" cy="112" r="14" fill="#d8c08a"/>
  <ellipse cx="730" cy="112" rx="30" ry="8" fill="none" stroke="#d8c08a" stroke-width="1.5" opacity="0.7"/>
  <path d="M730 132 L730 172" stroke="#d8a06a" stroke-width="2"/>
  <path d="M846 132 L846 172" stroke="#6fa8c7" stroke-width="2"/>
  <path d="M724 166 L730 176 L736 166 Z" fill="#d8a06a"/>
  <path d="M840 166 L846 176 L852 166 Z" fill="#6fa8c7"/>
  <g text-anchor="middle" font-size="16" font-family="Noto Sans SC">
    <text x="730" y="200" fill="#d8a06a" font-weight="700">先驱者 · 推门者 · 已失联</text>
    <text x="846" y="200" fill="#6fa8c7" font-weight="700">旅行者 · 仍在发信号</text>
  </g>
  <text x="30" y="226" font-size="14" fill="#8e867a" font-family="Noto Sans SC">太阳系剖面示意（不按比例）</text>
</svg>
"""

P4 = dict(
  kicker="先驱者系列 · 三道门",
  title="""
<h2><span class="num">03</span>他们推开了哪几道门</h2>
""",
  sub="每一扇门，都是一次「先挨打」换来的通行许可",
  body="""
<div class="figw">__SOLAR__</div>
<div class="gate"><div class="gh">第一道门 · 小行星带（1972）</div>
  <div class="gp">此前<b>不知道能不能穿过去</b>。先驱者 10 号穿过去了，
  于是后面所有探测器都能把这儿当路。</div></div>
<div class="gate"><div class="gh">第二道门 · 木星辐射带（1973—1974）</div>
  <div class="gp">此前<b>不知道辐射有多致命</b>。先驱者 10 号挨了 500 倍致死剂量把数字带回来，
  11 号又贴得更近 —— 只为多挨几倍，换一个能拐向土星的弯。</div></div>
<div class="gate"><div class="gh">第三道门 · 土星环平面（1979）</div>
  <div class="gp">此前<b>不知道穿环平面会不会被打死</b>。先驱者 11 号替旅行者把那条路先走了一遍。</div></div>
""",
  foot_q="旅行者号不是第一个到土星的人 —— <b>只是第一个活着到的人</b>。",
  foot_s="先驱者 10/11 号 · 1972—1979 · NASA | 资料来源：《得到大脑》",
)

P5 = dict(
  kicker="先驱者系列 · 两代对照",
  title="""
<h2><span class="num">04</span>两代探测器：一个沉默，一个仍在线</h2>
""",
  sub="同一个方向，两种命运；同一段路，两种账",
  body="""
<div class="cmp">
  <div class="ch"></div>
  <div class="cc a"><b>先驱者 10 / 11 号</b></div>
  <div class="cc"><b>旅行者 1 / 2 号</b></div>
  <div class="c0">现在</div>
  <div class="cc a">仍在飞，但已失联</div>
  <div class="cc">飞出太阳系，仍在发信号</div>
  <div class="c0">方向</div>
  <div class="cc a">朝毕宿五 / 盾牌座</div>
  <div class="cc">星际空间深处</div>
  <div class="c0">代价</div>
  <div class="cc a">替所有人试错，自己失联</div>
  <div class="cc">坐享其成，继续向前</div>
</div>
<div class="card acc"><div class="t">旅行者号的成就里，藏着先驱者的账<span class="tag">被推迟支付</span></div>
  <div class="d">旅行者 1 号拍下<b>暗淡蓝点</b>、2 号唯一一次看清天王星与海王星 ——
  这些「第一次」之所以能成立，是因为前面有两台机器，已经替它把每一种死法都试成了数字。</div></div>
<div class="card"><div class="t">但账不会自己结清<span class="tag">代价</span></div>
  <div class="d">先驱者还在飞，只是不再说话。我们知道它们大概在哪儿，
  却<b>永远无法确认</b> —— 因为确认这件事，需要它们自己开口。</div></div>
""",
  foot_q="坐享其成的那一方，<b>不必替前人记账</b> —— 但前人的账，是它能坐享其成的本金。",
  foot_s="先驱者 10/11 号 · 旅行者 1/2 号 · NASA | 资料来源：《得到大脑》",
)

PLAQUE_SVG = """
<svg viewBox="0 0 860 262" width="860" height="262" xmlns="http://www.w3.org/2000/svg">
  <defs><marker id="ar" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
    <path d="M0,0 L7,3 L0,6 Z" fill="#6fa8c7"/></marker></defs>
  <rect x="1" y="1" width="858" height="260" rx="10" fill="rgba(216,160,106,.10)" stroke="rgba(216,160,106,.55)"/>
  <g stroke="rgba(216,160,106,.75)" fill="none">
    <ellipse cx="150" cy="104" rx="52" ry="20"/>
    <ellipse cx="150" cy="104" rx="52" ry="20" transform="rotate(60 150 104)"/>
    <ellipse cx="150" cy="104" rx="52" ry="20" transform="rotate(-60 150 104)"/>
  </g>
  <circle cx="150" cy="104" r="7" fill="#e8b478"/>
  <g fill="#e8b478">
    <circle cx="352" cy="66" r="4.5"/><circle cx="392" cy="58" r="4"/><circle cx="428" cy="72" r="4.5"/>
    <circle cx="466" cy="60" r="4"/><circle cx="504" cy="74" r="4.5"/><circle cx="340" cy="102" r="4"/>
    <circle cx="382" cy="112" r="4.5"/><circle cx="420" cy="96" r="4"/><circle cx="460" cy="108" r="4.5"/>
    <circle cx="500" cy="98" r="4"/><circle cx="360" cy="140" r="4.5"/><circle cx="404" cy="146" r="4"/>
    <circle cx="448" cy="136" r="4.5"/><circle cx="488" cy="144" r="4"/>
  </g>
  <circle cx="690" cy="104" r="13" fill="#e8b478"/>
  <g stroke="rgba(216,160,106,.6)" fill="none">
    <ellipse cx="690" cy="104" rx="34" ry="12"/>
    <ellipse cx="690" cy="104" rx="58" ry="20"/>
    <ellipse cx="690" cy="104" rx="84" ry="28"/>
  </g>
  <path d="M766 78 L812 60" stroke="#6fa8c7" stroke-width="2" marker-end="url(#ar)"/>
  <text x="430" y="228" text-anchor="middle" font-size="21" fill="#e8b478" font-family="Noto Sans SC">你好 · 也可以是再见</text>
  <text x="430" y="252" text-anchor="middle" font-size="13" fill="#8e867a" font-family="Noto Sans SC">镀金铝板示意（比例与位置均非原样）</text>
</svg>
"""

P6 = dict(
  kicker="先驱者系列 · 尾声",
  title="""
<h2><span class="num">05</span>那块镀金铝板上刻着什么</h2>
""",
  sub="他们能留给人间的，最后只剩下这四样东西",
  body="""
<div class="figw">__PLAQUE__</div>
<div class="plaque">
  <div class="plq"><div class="pn">1</div><div class="pt"><b>氢原子 · 一切的起点</b></div></div>
  <div class="plq"><div class="pn">2</div><div class="pt"><b>14 颗脉冲星 · 指出你在哪</b></div></div>
  <div class="plq"><div class="pn">3</div><div class="pt"><b>太阳系与出航轨迹</b></div></div>
  <div class="plq"><div class="pn">4</div><div class="pt"><b>你好 · 也可以是再见</b></div></div>
</div>
<div class="card acc"><div class="t">走在最前面的那个，往往是被记得最少的那个<span class="tag">落点</span></div>
  <div class="d">因为他的工作，就是让后面的路<b>变得不值一提</b>。<br>
  我们算得出他们大概飞到哪儿，却再也没法确认 —— 因为确认这件事需要他们说话，
  而他们已经不能说话了。</div></div>
""",
  foot_q="他们替我们走完了最难的那一段，<b>然后再没出声</b>。",
  foot_s="先驱者 10/11 号 · 1972–1992 · NASA | 资料来源：《得到大脑》 | " + TAGS,
)

P6["body"] = P6["body"].replace("__PLAQUE__", PLAQUE_SVG)
P4["body"] = P4["body"].replace("__SOLAR__", SOLAR_SVG)
P1["body"] = P1["body"].replace("__HERO__", "")

PAGES = [P1, P2, P3, P4, P5, P6]


def build_all():
    hb = hero_b64()
    out = []
    for i, p in enumerate(PAGES, 1):
        html = page(i, len(PAGES), p["kicker"], p["title"], p["sub"], p["body"], p["foot_q"], p["foot_s"])
        html = html.replace("__HERO__", hb)
        fn = os.path.join(OUT, "先驱者_%02d.html" % i)
        open(fn, "w", encoding="utf-8", newline=chr(10)).write(html)
        out.append((fn, "先驱者_%02d.png" % i))
    return out
