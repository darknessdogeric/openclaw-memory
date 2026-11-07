# -*- coding: utf-8 -*-
import io, os, sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from _g9_page import page

OUT = r"C:\Users\ericz\Desktop\小红书_酒店分级分类_9图v2_2026-10-31"

BODY = """
<div class="row2">
  <div class="card">
    <div class="t">国内五家<span class="tag">自己画档位线</span></div>
    <div class="stack" style="margin-top:10px">
      <div><b style="font-size:18px;color:#1c1917">华住</b> <span style="font-size:14px;color:#8a8074">全谱系</span>
        <div style="font-size:14.5px;color:#6b6259;line-height:1.4;margin-top:2px">经济到高端最广；核心城市高流量直营 + 特许标准化输出，结构均衡</div></div>
      <div><b style="font-size:18px;color:#1c1917">锦江</b> <span style="font-size:14px;color:#8a8074">规模第一</span>
        <div style="font-size:14.5px;color:#6b6259;line-height:1.4;margin-top:2px">12 万+ 间客房；全服务占比高，单店产出与规模不匹配</div></div>
      <div><b style="font-size:18px;color:#1c1917">首旅如家</b> <span style="font-size:14px;color:#8a8074">存量深耕</span>
        <div style="font-size:14.5px;color:#6b6259;line-height:1.4;margin-top:2px">2026H1 直营 RevPAR 290.10 元 +3.89%、净利 +54.04%</div></div>
      <div><b style="font-size:18px;color:#1c1917">亚朵</b> <span style="font-size:14px;color:#8a8074">中高端商旅</span>
        <div style="font-size:14.5px;color:#6b6259;line-height:1.4;margin-top:2px">零售业务抬非房费收入，单店收入结构更健康</div></div>
      <div><b style="font-size:18px;color:#1c1917">格林</b> <span style="font-size:14px;color:#8a8074">经济型联盟</span>
        <div style="font-size:14.5px;color:#6b6259;line-height:1.4;margin-top:2px">经济型规模化 + 联盟输出，覆盖经济到中端</div></div>
    </div>
  </div>
  <div class="card">
    <div class="t">国际五家<span class="tag">各画各的线</span></div>
    <div class="stack" style="margin-top:10px">
      <div><b style="font-size:18px;color:#1c1917">万豪</b> <span style="font-size:14px;color:#8a8074">品牌线最长</span>
        <div style="font-size:14.5px;color:#6b6259;line-height:1.4;margin-top:2px">St. Regis / Ritz-Carlton 到万怡全档；下设 Classic 与 Distinctive 子类</div></div>
      <div><b style="font-size:18px;color:#1c1917">希尔顿</b> <span style="font-size:14px;color:#8a8074">档位最细 · 6 档</span>
        <div style="font-size:14.5px;color:#6b6259;line-height:1.4;margin-top:2px">Luxury → Upper Upscale → Upscale → Upper Midscale → Midscale → Select</div></div>
      <div><b style="font-size:18px;color:#1c1917">洲际 IHG</b> <span style="font-size:14px;color:#8a8074">4 档</span>
        <div style="font-size:14.5px;color:#6b6259;line-height:1.4;margin-top:2px">Luxury &amp; Lifestyle → Premium → Select → Mainstream</div></div>
      <div><b style="font-size:18px;color:#1c1917">雅高</b> <span style="font-size:14px;color:#8a8074">双头</span>
        <div style="font-size:14.5px;color:#6b6259;line-height:1.4;margin-top:2px">从传统奢华（Raffles）一路到生活方式奢华（Banyan Tree）</div></div>
      <div><b style="font-size:18px;color:#1c1917">凯悦</b> <span style="font-size:14px;color:#8a8074">生活方式</span>
        <div style="font-size:14.5px;color:#6b6259;line-height:1.4;margin-top:2px">强调设计感与在地文化（Park Hyatt、Andaz），不按传统奢华分</div></div>
    </div>
  </div>
</div>
<div class="card acc">
  <div class="t">行业通用的概念 · STR Brand Scale<span class="tag">唯一跨集团可比</span></div>
  <div class="d" style="margin-top:8px">按<b>上一年度全系统平均 ADR</b> 把连锁规模切成 6 档：<b>Luxury → Upper Upscale → Upscale → Upper Midscale → Midscale → Economy</b>，独立物业单列。</div>
  <div class="d" style="margin-top:8px">它是<b>唯一</b>能把「十家集团 + 所有非标」放进<b>同一张表</b>比较的语言 —— 也是资产定价、融资谈判与 REIT 化的唯一通用语。</div>
</div>
"""

html = page(5, 9, "02 · 层级二 · 集团分级",
            '十家集团，<br><span class="hl">十种档位线</span>',
            "<div class=sub>国内五家 + 国际五家 —— 集团都自己画线，但行业有一个通用坐标</div>",
            BODY)

CHECK = """
() => {
  const issues = [];
  const W = 1080, H = 1440;
  document.querySelectorAll("*").forEach(el => {
    if (el.children.length === 0 && el.textContent.trim()) {
      if (el.scrollWidth > el.clientWidth + 2)
        issues.push("文字溢出: " + (el.className || el.tagName) + " :: " + el.textContent.trim().slice(0,26));
    }
  });
  document.querySelectorAll(".wrap *").forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.right > W+1 || r.bottom > H+1 || r.left < -1)
      issues.push("超画布: " + (el.className || el.tagName));
  });
  const w = document.querySelector(".wrap").getBoundingClientRect();
  document.querySelectorAll(".wrap > *").forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.bottom > w.bottom + 2) issues.push("超容器: " + (el.className || el.tagName) + " 超" + Math.round(r.bottom - w.bottom) + "px");
  });
  const body = document.querySelector(".body");
  if (body) {
    const br = body.getBoundingClientRect();
    document.querySelectorAll(".body > *").forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.bottom > br.bottom + 2) issues.push("body 溢出: " + (el.className||el.tagName) + " 超" + Math.round(r.bottom - br.bottom) + "px");
    });
  }
  return issues;
}
"""

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox","--disable-dev-shm-usage"])
    pg = b.new_page(viewport={"width":1080,"height":1440}, device_scale_factor=2)
    pg.set_content(html, wait_until="domcontentloaded")
    pg.wait_for_timeout(450)
    iss = pg.evaluate(CHECK)
    out = os.path.join(OUT, "05.png")
    pg.screenshot(path=out, full_page=False, omit_background=False, timeout=20000)
    pg.close()
    b.close()
print(("OK  " if not iss else "WARN"), "05.png", os.path.getsize(out), ("" if not iss else "| " + " ; ".join(iss[:5])))