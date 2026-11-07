# -*- coding: utf-8 -*-
"""渲染 9 图 + DOM 排版检查"""
import os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playwright.sync_api import sync_playwright
from _g9_page import page
from _g9_data import PAGES

OUT = r"C:\Users\ericz\Desktop\小红书_酒店分级分类_9图v2_2026-10-31"
os.makedirs(OUT, exist_ok=True)

CHECK = """
() => {
  const issues = [];
  const W = 1080, H = 1440;
  document.querySelectorAll("*").forEach(el => {
    if (el.children.length === 0 && el.textContent.trim()) {
      if (el.scrollWidth > el.clientWidth + 2) {
        issues.push("文字溢出: " + (el.className || el.tagName) + " :: " + el.textContent.trim().slice(0,26));
      }
    }
  });
  document.querySelectorAll(".wrap *").forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.right > W+1 || r.bottom > H+1 || r.left < -1) {
      issues.push("超画布: " + (el.className || el.tagName) + " b=" + Math.round(r.bottom) + " r=" + Math.round(r.right));
    }
  });
  const w = document.querySelector(".wrap").getBoundingClientRect();
  document.querySelectorAll(".wrap > *").forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.bottom > w.bottom + 2) {
      issues.push("超容器: " + (el.className || el.tagName) + " 超" + Math.round(r.bottom - w.bottom) + "px");
    }
  });
  return issues;
}
"""

total = len(PAGES)
with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
    for i, d in enumerate(PAGES, 1):
        html = page(i, total, d["kicker"], d["title"], d.get("sub", ""), d["body"],
                    d.get("foot_q", ""), d.get("foot_s", ""))
        fn = os.path.join(OUT, "%02d.png" % i)
        pg = b.new_page(viewport={"width":1080,"height":1440}, device_scale_factor=2)
        pg.set_content(html, wait_until="domcontentloaded")
        pg.wait_for_timeout(400)
        iss = pg.evaluate(CHECK)
        pg.screenshot(path=fn, full_page=False, omit_background=False, timeout=20000)
        pg.close()
        print(("OK  " if not iss else "WARN"), "%02d.png" % i, os.path.getsize(fn),
              ("" if not iss else "| " + " ; ".join(iss[:4])))
    b.close()
print("DONE ->", OUT)