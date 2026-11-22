"""重新渲染 slide 03 (fix overflow)"""
import subprocess, sys
sys.path.insert(0, r'D:\B166ER-OpenClaw\workspace\toolbox')
from pathlib import Path
from watermark_tool import protect_output

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
OUT_DIR = Path(r"D:\B166ER-OpenClaw\workspace\output\xhs_85_2026-08-01_v3")

# 重新渲染所有6张 (因为修了 slide 01 和 03)
for idx in range(1, 7):
    files = list(OUT_DIR.glob(f"0{idx}_p0*.html"))
    if not files:
        print(f"  No HTML for slide {idx}")
        continue
    html_path = files[0]
    png_path = html_path.with_suffix('.png')

    r = subprocess.run([
        EDGE, "--headless=new", "--disable-gpu", "--no-sandbox",
        "--hide-scrollbars", "--force-device-scale-factor=2",
        "--window-size=1080,1440",
        f"--screenshot={png_path}",
        html_path.as_uri(),
    ], capture_output=True, text=True, timeout=60)

    size = png_path.stat().st_size if png_path.exists() else 0
    print(f"  Slide {idx}: RC={r.returncode}, PNG={size:,} bytes")

    if png_path.exists() and size > 0:
        try:
            wm_out = protect_output(str(png_path))
            print(f"    Watermark: {Path(wm_out).stat().st_size:,} bytes")
        except Exception as e:
            print(f"    WM FAIL: {e}")

print("Done")