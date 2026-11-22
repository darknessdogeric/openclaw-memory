# -*- coding: utf-8 -*-
"""先驱者系列 · 小红书多图笔记 6 图 (B版: hotel_h1 酒店题材规格, 米白 #F5F1E8)"""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BOX = Path(r"D:\B166ER-openclaw\workspace\toolbox")
SRC = BOX / "hotel_h1_xhs_master.py"
_g = SRC.read_text(encoding="utf-8")
COMMON_CSS = _g.split('COMMON_CSS = """', 1)[1].split('"""', 1)[0]

TOTAL = 6
ISSUE = "2026.11.01"
SOURCE = "SOURCE: B166ER · 深度探索观察"
VERSION = "ISSUE NO.001"

SLIDE_01 = """
<div>
  <div class="eyebrow">EXECUTIVE BRIEFING · 摘要</div>
  <h1>他们替旅行者号推开<br/><span class="accent">每一道门</span><br/>然后再没出声</h1>
</div>
<div class="data-callout">
  <div class="value">500</div>
  <div class="unit">倍致死剂量 · 木星辐射带 · 1973</div>
</div>
<div class="audience-grid">
  <div class="aud-cell">
    <div class="aud-num">01</div>
    <div class="aud-name">先行者</div>
    <div class="aud-desc">先驱者 10 / 11 号，人类第一代外太阳系探测器。</div>
  </div>
  <div class="aud-cell">
    <div class="aud-num">02</div>
    <div class="aud-name">探路者</div>
    <div class="aud-desc">1972—1979，小行星带、木星辐射带、土星环平面。</div>
  </div>
  <div class="aud-cell">
    <div class="aud-num">03</div>
    <div class="aud-name">接力者</div>
    <div class="aud-desc">1980 旅行者 1 / 2 号飞过土星，拍下暗淡蓝点。</div>
  </div>
</div>
<div class="red-bar"><div class="bar-text">人类深空探索史上最沉默的两位先驱 —— <strong>他们不是终点，是探路的</strong>。</div></div>
"""

SLIDE_02 = """
<div>
  <div class="eyebrow">01 · THE PHENOMENON</div>
  <h2>每一行右侧那个问题<br/>在当时都<strong>没有答案</strong></h2>
</div>
<div class="body-text">
  生存压力、地位竞争、资源不确定，长期塑造了人类的动机系统与社会行为。
  当物质条件接近极大满足、生存焦虑大幅消退时 —— 原先驱动行为的核心燃料开始失效。
</div>
<table class="editorial">
  <tr><td>1972</td><td>先驱者 10 号穿越小行星带</td><td class="concl">能不能穿过去</td></tr>
  <tr><td>1973</td><td>先驱者 10 号闯入木星辐射带</td><td class="concl">辐射有多致命</td></tr>
  <tr><td>1974</td><td>先驱者 11 号更贴近木星</td><td class="concl">贴多近会死</td></tr>
  <tr><td>1979</td><td>先驱者 11 号穿越土星环平面</td><td class="concl">会不会被打死</td></tr>
  <tr><td>1980</td><td>旅行者 1 / 2 号顺利飞过土星</td><td class="concl">门已经开了</td></tr>
</table>
<div class="red-bar"><div class="bar-text">人类此前<strong>不知道</strong>小行星带能不能穿过去。<br/>他进去、出来了 —— 于是所有人都可以走了。</div></div>
"""

SLIDE_03 = """
<div>
  <div class="eyebrow">02 · THE FRAMEWORK</div>
  <h2>他们交付的从来不是探测器<br/>是<strong>一串数字</strong></h2>
</div>
<div class="data-callout">
  <div class="value">3</div>
  <div class="unit">道门被推开 · 每一道都先挨过</div>
</div>
<div class="pull-quote">
  未知 → 数字 → 通行许可。<br/>
  他把「会死」这件模糊的事，试成了具体数字，后来的机器才敢按这个数字重新设计。
</div>
<div class="dark-callout">
  <div class="dc-title">KEY INSIGHT</div>
  <div class="dc-body">
    先驱者 10 号带回来的不是「木星很危险」这种结论，<br/>
    而是<strong>一个可写进设计图纸的剂量数字</strong>。<br/>
    旅行者号据此重新设计 —— 它能成功，是因为有人先替它把危险量化了。
  </div>
</div>
"""

SLIDE_04 = """
<div>
  <div class="eyebrow">03 · THE THREE GATES</div>
  <h2>他们推开了哪三道门</h2>
</div>
<div class="audience-grid">
  <div class="aud-cell">
    <div class="aud-num">01</div>
    <div class="aud-name">小行星带</div>
    <div class="aud-desc">1972 年先驱者 10 号直接穿了过去。此后再没有探测器需要担心这件事 —— 他把它变成了路。</div>
  </div>
  <div class="aud-cell">
    <div class="aud-num">02</div>
    <div class="aud-name">木星辐射带</div>
    <div class="aud-desc">1973 年挨了 500 倍致死剂量把数字带回来；1974 年 11 号贴得更近，只为多挨几倍，换一个能拐向土星的弯。</div>
  </div>
  <div class="aud-cell">
    <div class="aud-num">03</div>
    <div class="aud-name">土星环平面</div>
    <div class="aud-desc">1979 年先驱者 11 号替旅行者把那条路先走了一遍。1980 年旅行者飞过时，面对的是一条被走通的航线。</div>
  </div>
</div>
<div class="pull-quote">
  旅行者号不是第一个到土星的人 —— 只是第一个活着到的人。
</div>
"""

SLIDE_05 = """
<div>
  <div class="eyebrow">04 · THE IMPLICATION</div>
  <h2>他们推开的门<br/>后来者<strong>不必再付代价</strong></h2>
</div>
<ol class="editorial">
  <li>他们承担的是<strong>不可逆的试错成本</strong> —— 在 1970 年代，答案只能靠真的飞过去、真的挨一次。</li>
  <li>沉默不是失职，是任务本身：1970 年代还没有能跨星际可靠回传的系统，他们注定发不回有用的信号。</li>
  <li>后来者坐享其成 —— 但那份成，是前面两台机器拿失联换来的。</li>
</ol>
<div class="dark-callout">
  <div class="dc-title">UNDERLYING CAUSE</div>
  <div class="dc-body">
    走在最前面的那个，往往是被记得最少的那个。<br/>
    因为他的工作，就是让后面的路<strong>变得不值一提</strong>。
  </div>
</div>
"""

SLIDE_06 = """
<div>
  <div class="eyebrow">05 · THE TAKEAWAY</div>
  <h2>他们替我们走完了<br/>最难的那一段</h2>
</div>
<div class="dark-callout">
  <div class="dc-title">CORE LAW</div>
  <div class="dc-body">
    先驱者的账，由旅行者付；<br/>
    旅行者的账，由下一个先驱者付。<br/>
    <strong>账只会往下传，不会消失。</strong>
  </div>
</div>
<div class="pull-quote">
  <em>我们算得出他们大概飞到哪儿</em>，<br/>
  却再也没法确认 —— 因为确认这件事需要他们说话，<br/>
  而他们已经不能说话了。
</div>
<div class="red-bar"><div class="bar-text">先驱者 10 / 11 号 · 1972—1992 · NASA · 两台机器，一个方向，同一段路的两种账。</div></div>
<div class="body-text">
  如果你的团队正在替别人走一段没人走过的那段路 —— 这本笔记是写给你的。
</div>
"""

SLIDES = [SLIDE_01, SLIDE_02, SLIDE_03, SLIDE_04, SLIDE_05, SLIDE_06]
