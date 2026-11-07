# -*- coding: utf-8 -*-
"""6 图渲染器 - DOM 体检"""
import os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _p6_content import build_all, OUT
from playwright.sync_api import sync_playwright

CHECK = """() => {
  const issues = [];
  const W = 1080, H = 1920;
  const R = (e) => e.getBoundingClientRect();
  const tx = (e) => (e.textContent || "").trim();
  document.querySelectorAll("*").forEach(el => {
    if (el.children.length === 0 && tx(el)) {
      if (el.scrollWidth > el.clientWidth + 2)
        issues.push("文字溢出: " + (el.className || el.tagName) + " :: " + tx(el).slice(0,22));
      if (el.clientHeight > 24 && el.scrollHeight > el.clientHeight + 2) {
        const cs = getComputedStyle(el);
        const fs = parseFloat(cs.fontSize) || 16;
        const lh = parseFloat(cs.lineHeight) || 0;
        if (lh > fs * 1.3) issues.push("纵向溢出: " + (el.className || el.tagName) + " :: " + tx(el).slice(0,22));
      }
    }
  });
  document.querySelectorAll(".wrap *").forEach(el => {
    const r = R(el);
    if (r.width === 0 && r.height === 0) return;
    if (r.right > W + 1 || r.bottom > H + 1 || r.left < -1)
      issues.push("出画布: " + (el.className || el.tagName) + " b=" + Math.round(r.bottom));
  });
  if (document.body.scrollHeight > H + 2) issues.push("body 纵向溢出 " + document.body.scrollHeight);
  if (document.body.scrollWidth > W + 2) issues.push("body 横向溢出 " + document.body.scrollWidth);
  const brand = document.querySelector(".brand");
  if (brand) {
    const b = R(brand);
    document.querySelectorAll(".wrap *").forEach(el => {
      if (!tx(el) || el.children.length || brand.contains(el)) return;
      const r = R(el);
      if (r.right > b.left && r.left < b.right && r.bottom > b.top && r.top < b.bottom)
        issues.push("B标压字: " + tx(el).slice(0,20));
    });
  }
  const wm = document.querySelector(".wm");
  const foot = document.querySelector(".foot");
  if (wm && foot) { if (R(wm).top < R(foot).bottom) issues.push("水印压foot"); }
  const bd = document.querySelector(".body");
  if (bd) {
    const kids = [...bd.children].map(k => R(k));
    if (kids.length > 2) {
      const gaps = [];
      for (let i = 1; i < kids.length; i++) gaps.push(kids[i].top - kids[i-1].bottom);
      const mn = Math.min.apply(null, gaps), mx = Math.max.apply(null, gaps);
      if (mx - mn > 60) issues.push("间距不均 极差 " + Math.round(mx-mn) + "px");
    }
    const bb = bd.getBoundingClientRect();
    const last = bd.lastElementChild.getBoundingClientRect();
    if (bb.bottom - last.bottom > 170) issues.push("下部空隙 " + Math.round(bb.bottom - last.bottom) + "px");
  }
  return issues;
}"""

jobs = build_all()
print("built", len(jobs), "html")
bad = 0
with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
    for i, (fn, pn) in enumerate(jobs, 1):
        html = open(fn, encoding="utf-8").read()
        pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=2)
        pg.set_content(html, wait_until="domcontentloaded")
        pg.wait_for_timeout(380)
        iss = pg.evaluate(CHECK)
        out = os.path.join(OUT, pn)
        pg.screenshot(path=out, full_page=False, omit_background=False, timeout=25000)
        pg.close()
        if iss:
            bad += 1
        print("  p%d %s %s %d B %s" % (i, "OK  " if not iss else "WARN", pn, os.path.getsize(out), "" if not iss else "| " + " ; ".join(iss[:5])))
    b.close()
print("DONE ->", OUT, "| pages with issues:", bad)
