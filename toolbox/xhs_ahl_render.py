"""Step 1: Render 7 张 AHL 小红书 麦肯锡风 滑片"""
import subprocess
from pathlib import Path

OUT_DIR = Path(r"C:\Users\ericz\Desktop\产业发展部\AHL项目\AHL_小红书12图_v2_mckinsey")
OUT_DIR.mkdir(parents=True, exist_ok=True)

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# 执行 master 拿 slide bodies + CSS
SRC = Path(r"D:\B166ER-OpenClaw\workspace\toolbox\ahl_xhs_mckinsey_master.py").read_text(encoding='utf-8')
NS = {}
exec(SRC, NS)

SLIDE_01 = NS['SLIDE_01']
SLIDE_02 = NS['SLIDE_02']
SLIDE_03 = NS['SLIDE_03']
SLIDE_04 = NS['SLIDE_04']
SLIDE_05 = NS['SLIDE_05']
SLIDE_06 = NS['SLIDE_06']
SLIDE_07 = NS['SLIDE_07']
COMMON_CSS = NS['COMMON_CSS']
bodies = [SLIDE_01, SLIDE_02, SLIDE_03, SLIDE_04, SLIDE_05, SLIDE_06, SLIDE_07]

ISSUE = "26-322"

print(f"Loaded {len(bodies)} slide bodies")

for idx, body in enumerate(bodies, 1):
    html_path = OUT_DIR / f"slide_{idx:02d}.html"
    png_path = OUT_DIR / f"ahl_xhs_{idx:02d}.png"

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>AHL XHS Slide {idx}</title>
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
      <div class="source">SOURCE: B166ER · AHL系列 · 范式四阶</div>
      <div class="version">V1.0 · AHL · 同构分形</div>
    </div>
    <div class="page">{idx:02d} / 07</div>
  </div>
</div>
</body>
</html>"""

    html_path.write_text(html_content, encoding='utf-8')

    r = subprocess.run([
        EDGE, "--headless=new", "--disable-gpu", "--no-sandbox",
        "--hide-scrollbars", "--force-device-scale-factor=2",
        "--window-size=1080,1440",
        f"--screenshot={png_path}",
        html_path.as_uri(),
    ], capture_output=True, text=True, timeout=60)
    sz = png_path.stat().st_size if png_path.exists() else 0
    print(f"Slide {idx} render: RC={r.returncode}, size={sz:,} bytes")

print("=== Render complete ===")
print(f"Output: {OUT_DIR}")
