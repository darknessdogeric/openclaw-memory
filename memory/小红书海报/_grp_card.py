# -*- coding: utf-8 -*-
import os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _g9_page import page

OUT = r"C:\Users\ericz\Desktop\小红书_酒店分级分类_9图v2_2026-10-31"

BODY = """
<div class="card acc">
  <div class="t">十家集团，十条档位线<span class="tag">横向不可比</span></div>
  <div class="d" style="font-size:18.5px;color:#1c1917">国内五家与国际五家，<b>各画各的线</b>。<br>同一家酒店在 A 集团是「高端」、在 B 集团可能只是「中端」—— <b>集团档位线之间没有换算关系</b>。</div>
</div>
<div class="row2">
  <div class="card">
    <div class="t">国内五家</div>
    <div class="d"><b>华住</b> 全谱系 · 经济到高端最广<br>
      <b>锦江</b> 规模第一 · 12万+间 · 全服务占比高<br>
      <b>首旅如家</b> 存量深耕 · 26H1 RevPAR +3.89%<br>
      <b>亚朵</b> 中高端商旅 · 零售抬非房费<br>
      <b>格林</b> 经济型联盟 · 联盟输出</div>
  </div>
  <div class="card">
    <div class="t">国际五家</div>
    <div class="d"><b>万豪</b> 品牌线最长 · 带 Classic/Distinctive 子类<br>
      <b>希尔顿</b> 档位最细 · 6 档<br>
      <b>洲际 IHG</b> 4 档<br>
      <b>雅高</b> 双头 · 传统奢华↔生活方式奢华<br>
      <b>凯悦</b> 生活方式 · 设计感与在地文化</div>
  </div>
</div>
<div class="card" style="border-color:#a05f26;border-width:1.5px;background:#fdfaf4">
  <div class="t">行业通用的概念 · 唯一跨集团可比</div>
  <div class="d" style="font-size:17.5px;color:#1c1917"><b>STR Brand Scale</b>：按上一年度全系统平均 ADR 把连锁规模切 6 档 —— Luxury → Upper Upscale → Upscale → Upper Midscale → Midscale → Economy，独立物业单列。<br>
  <b>它是唯一能把「十家集团 + 所有非标」放进同一张表比较的语言</b>，也是资产定价、融资谈判与 REIT 化的唯一通用语。</div>
</div>
<div class="card soft">
  <div class="t">为什么集团档位线不产生溢价</div>
  <div class="d">2024Q1：品牌集团组 <b>ADR 涨幅最低 +1.5%</b>，却 <b>OCC 涨幅最高 +2.4%</b> —— 集团卖的是<b>位置与确定性</b>，不是最高价。<br>高端（奢华 +4.0% / 中高端 +4.4% 的 ADR）才是定价权所在。</div>
</div>
"""

html = page(0, 1, "GROUPS · 集团分级",
            '十家集团，<br><span class=hl>十种档位线</span>',
            "<div class=sub>横向不可比 —— 所以行业需要一个通用坐标</div>",
            BODY)

from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox","--disable-dev-shm-usage"])
    pg = b.new_page(viewport={"width":1080,"height":1440}, device_scale_factor=2)
    pg.set_content(html, wait_until="domcontentloaded")
    pg.wait_for_timeout(450)
    out = os.path.join(OUT, "13_十家集团对照_单图.png")
    pg.screenshot(path=out, full_page=False, omit_background=False, timeout=20000)
    pg.close()
    b.close()
print("OK", os.path.getsize(out))