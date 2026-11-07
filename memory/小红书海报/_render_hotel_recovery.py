"""渲染酒店景气度信息图 + DOM 排版检查 + probe (0 token 体检)"""
import os
import random
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from playwright.sync_api import sync_playwright

SRC = Path(r"D:\B166ER-openclaw\workspace\memory\小红书海报\hotel_recovery_v1.html")
OUT = Path(r"C:\Users\ericz\Desktop\小红书_酒店行业景气度判断_2026-10-29")
OUT.mkdir(parents=True, exist_ok=True)

random.seed(20261029)
stars = "".join(
    f'<circle cx="{random.randint(0,1080)}" cy="{random.randint(0,1920)}" '
    f'r="{random.choice([1,1,1.2,1.5,2])}" fill="#FFFFFF" '
    f'opacity="{round(random.uniform(0.08,0.40),2)}"/>' for _ in range(90))

html = SRC.read_text(encoding="utf-8").replace("__STARS__", stars)

CHECK = """
() => {
  const issues = [];
  const W = 1080, H = 1920;
  document.querySelectorAll('*').forEach(el => {
    if (el.children.length === 0 && el.textContent.trim()) {
      if (el.scrollWidth > el.clientWidth + 2)
        issues.push('文字溢出: ' + (el.className||el.tagName) + ' "' + el.textContent.trim().slice(0,26) + '"');
    }
  });
  document.querySelectorAll('.sec, .sec *').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.right > W + 1 || r.bottom > H + 1 || r.left < -1)
      issues.push('超画布: ' + (el.className||el.tagName) + ' b=' + Math.round(r.bottom) + ' r=' + Math.round(r.right));
  });
  const secs = [...document.querySelectorAll('.sec')].map(s => s.getBoundingClientRect());
  for (let i = 1; i < secs.length; i++)
    if (secs[i].top < secs[i-1].bottom - 1)
      issues.push('段落重叠 sec' + i + ' (' + Math.round(secs[i].top) + ' < ' + Math.round(secs[i-1].bottom) + ')');
  document.querySelectorAll('.sec').forEach((s, i) => {
    const sr = s.getBoundingClientRect(); let mb = 0;
    s.querySelectorAll(':scope > *').forEach(c => { const r = c.getBoundingClientRect(); if (r.height>0) mb = Math.max(mb, r.bottom); });
    if (mb > sr.bottom + 2) issues.push('段' + (i+1) + ' 超段 ' + Math.round(mb - sr.bottom) + 'px');
  });
  return issues;
}
"""

with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
    page = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=2)
    page.set_content(html, wait_until="domcontentloaded")
    page.wait_for_timeout(700)
    issues = page.evaluate(CHECK)
    png = OUT / "酒店行业景气度判断_v1.0.png"
    page.screenshot(path=str(png), full_page=False, omit_background=False, timeout=20000)
    page.close()
    b.close()

print(f"渲染: {png.name}  {png.stat().st_size:,} bytes")
if issues:
    print(f"\n⚠️ 排版问题 {len(issues)} 处:")
    for i in issues[:25]:
        print("  -", i)
else:
    print("\n✅ DOM 排版检查: 0 问题")

r = subprocess.run([sys.executable, r"D:\B166ER-openclaw\workspace\tools\visual_check.py", "probe", str(png)],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
print("\n--- probe ---")
for l in ((r.stdout or "") + (r.stderr or "")).strip().splitlines():
    if "DeprecationWarning" not in l and "warnings.warn" not in l:
        print("  " + l[:140])
