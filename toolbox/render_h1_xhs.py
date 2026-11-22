"""Render 12 张 2026 H1 酒店行业 小红书 麦肯锡风 滑片"""
import subprocess
from pathlib import Path

OUT_DIR = Path(r"D:\B166ER-OpenClaw\workspace\output\hotel_h1_xhs_mckinsey")
OUT_DIR.mkdir(parents=True, exist_ok=True)

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

SRC = Path(r"D:\B166ER-OpenClaw\workspace\toolbox\hotel_h1_xhs_master.py").read_text(encoding='utf-8')
NS = {}
exec(SRC, NS)

bodies = [NS['SLIDE_01'], NS['SLIDE_02'], NS['SLIDE_03'], NS['SLIDE_04'],
          NS['SLIDE_05'], NS['SLIDE_06'], NS['SLIDE_07'], NS['SLIDE_08'],
          NS['SLIDE_09'], NS['SLIDE_10'], NS['SLIDE_11'], NS['SLIDE_12']]
COMMON_CSS = NS['COMMON_CSS']

ISSUE = "26-322-HOTEL"

EDGE_CMD = [
    EDGE, "--headless=new", "--disable-gpu", "--no-sandbox",
    "--hide-scrollbars", "--force-device-scale-factor=2",
    "--window-size=1080,1440",
]

print(f"Loaded {len(bodies)} slide bodies")
print(f"Output: {OUT_DIR}")

for idx, body in enumerate(bodies, 1):
    html_path = OUT_DIR / f"slide_{idx:02d}.html"
    png_path = OUT_DIR / f"hotel_h1_xhs_{idx:02d}.png"

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>Hotel H1 XHS Slide {idx}</title>
<style>{COMMON_CSS}
</style>
</head>
<body>
<div class="slide">
  <div class="masthead">
    <div class="brand">ERIC的B166ER出品</div>
    <div class="meta">ISSUE {ISSUE}</div>
  </div>
  <div class="masthead-rule"></div>
  <div class="content">
    {body}
  </div>
  <div class="footer-rule"></div>
  <div class="footer">
    <div>
      <div class="source">SOURCE: B166ER · 2026 H1 酒店行业全景 · 9 大维度</div>
      <div class="version">V1.0 · 58 信源框架 · 置信度标注</div>
    </div>
    <div class="page">{idx:02d} / 12</div>
  </div>
</div>
</body>
</html>"""

    html_path.write_text(html_content, encoding='utf-8')

    cmd = EDGE_CMD + [f"--screenshot={png_path}", html_path.as_uri()]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    sz = png_path.stat().st_size if png_path.exists() else 0
    print(f"Slide {idx:02d}: RC={r.returncode}, {sz:,} bytes")

print("=== Render complete ===")