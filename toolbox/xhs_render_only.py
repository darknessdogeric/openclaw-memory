"""Step 1: Render 7 slides — V2 (exec f-strings properly)."""
import subprocess
from pathlib import Path

OUT_DIR = Path(r"D:\B166ER-OpenClaw\workspace\output\xhs_2026-07-16")
OUT_DIR.mkdir(parents=True, exist_ok=True)

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# Execute the master script in a controlled namespace to get the rendered bodies + CSS
SRC = Path(r"D:\B166ER-OpenClaw\workspace\toolbox\xhs_mckinsey.py").read_text(encoding='utf-8')
NS = {}
exec(SRC, NS)

# Pull out the rendered slide bodies (already f-strings evaluated inside the script's namespace)
SLIDE_01 = NS['SLIDE_01']
SLIDE_02 = NS['SLIDE_02']
SLIDE_03 = NS['SLIDE_03']
SLIDE_04 = NS['SLIDE_04']
SLIDE_05 = NS['SLIDE_05']
SLIDE_06 = NS['SLIDE_06']
SLIDE_07 = NS['SLIDE_07']
COMMON_CSS = NS['COMMON_CSS']
bodies = [SLIDE_01, SLIDE_02, SLIDE_03, SLIDE_04, SLIDE_05, SLIDE_06, SLIDE_07]

print(f"Loaded {len(bodies)} slide bodies")

for idx, body in enumerate(bodies, 1):
    html_path = OUT_DIR / f"slide_{idx:02d}.html"
    png_path = OUT_DIR / f"slide_{idx:02d}.png"

    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><title>XHS Slide {idx}</title>
<style>{COMMON_CSS}
</style>
</head>
<body>
<div class="slide">
  <div class="masthead">
    <div class="brand">B166ER · 商业内参</div>
    <div class="date">2026.07.16 · ISSUE NO.001</div>
  </div>
  <div class="content">
    {body}
  </div>
  <div class="footer">
    <div class="source">SOURCE: B166ER · 案例研究</div>
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
    ], capture_output=True, text=True, timeout=45)
    print(f"Slide {idx} render: RC={r.returncode}, size={png_path.stat().st_size if png_path.exists() else 0}")

print("=== Render complete ===")