# -*- coding: utf-8 -*-
import os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _g9_page import page

OUT = r"C:\Users\ericz\Desktop\小红书_家具文化_高桌大椅_2026-10-31"
os.makedirs(OUT, exist_ok=True)

BODY = """
<div class="card acc">
  <div class="t">这个词有两义，必须拆开<span class="tag">一条本土 · 一条才叫传入</span></div>
  <div class="d" style="font-size:18.5px;color:#1c1917">A 线：<b>宋代</b>本土成型的高桌高椅<br>B 线：<b>明末清初 17 世纪</b>传入的西式成套家具</div>
</div>
<div class="row2">
  <div class="card">
    <div class="t">A 线 · 宋代本土<span class="tag">不是传入</span></div>
    <div class="d"><b>汉</b> 胡床（西域折叠坐具）<br><b>唐</b> 有靠背扶手者始称「椅」<br><b>宋</b> 交椅成熟 · 席地而坐→垂足坐<br><b>明</b> 交椅 / 圈椅 / 官帽椅 三大椅式<br><br>★ 硬证据：椅子高桌普及后，<b>窗棂被抬高</b>，建筑跟着坐姿改造</div>
  </div>
  <div class="card">
    <div class="t">B 线 · 明末清初<span class="tag">这才是传入</span></div>
    <div class="d"><b>17 世纪</b> 随传教士与澳门广州商船传入，最早落在<b>广州、澳门</b><br><b>18 世纪中叶起</b> 广式家具明确受西方影响，延续至 20 世纪初<br><b>广州十三行</b>为通道，粤匠沿<b>一德水道</b>一带作坊把西式元素融进红木家具<br><b>晚明清初</b> 苏州、松江出现西式家具作坊</div>
  </div>
</div>
<div class="card" style="border-color:#a05f26;border-width:1.5px;background:#fdfaf4">
  <div class="t">一个反直觉的事实</div>
  <div class="d" style="font-size:18px;color:#1c1917">中国 <b>宋代</b>（11–13 世纪）就完成「高桌 + 高背椅 + 围坐」整套形态；<br>欧洲要到 <b>16–17 世纪</b>才从矮长凳转成 dining table + chair。<br>所以真正被「传入」的，是<b>西式的成套比例与装饰语汇</b>（高背、旋木腿、织物坐面），<b>不是形态本身</b>。</div>
</div>
<div class="card">
  <div class="t">空间选型的两条路线</div>
  <div class="kv"><span class="k">中式的体面</span><span class="v a">案 / 几 + 圈椅 / 官帽椅</span></div>
  <div class="kv"><span class="k"></span><span class="v" style="font-weight:400;font-size:15px;color:#6b6259">主位—宾位—侧位 的礼序对称</span></div>
  <div class="kv"><span class="k">西式的松弛</span><span class="v a">长桌 + 高背椅</span></div>
  <div class="kv"><span class="k"></span><span class="v" style="font-weight:400;font-size:15px;color:#6b6259">底子用中式硬木 + 榫卯，比全西式更耐看</span></div>
</div>
"""

html = page(0, 1, "SPACE & FURNITURE · 空间与家具文化",
            '高桌大椅，<br>是 <span class=hl>两条线</span>',
            "<div class=sub>一条宋代的本土源流，一条明末清初的西式传入</div>",
            BODY)

from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox","--disable-dev-shm-usage"])
    pg = b.new_page(viewport={"width":1080,"height":1440}, device_scale_factor=2)
    pg.set_content(html, wait_until="domcontentloaded")
    pg.wait_for_timeout(450)
    out = os.path.join(OUT, "高桌大椅_中西两条线.png")
    pg.screenshot(path=out, full_page=False, omit_background=False, timeout=20000)
    pg.close()
    b.close()
print("OK", os.path.getsize(out))