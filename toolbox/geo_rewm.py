"""Re-apply watermark only (no re-render)."""
import sys
from pathlib import Path
sys.path.insert(0, r'D:\B166ER-OpenClaw\workspace\toolbox')
from geo_v4_mckinsey import pil_watermark

OUT_DIR = Path(r"D:\B166ER-OpenClaw\workspace\output\geo_2026-07-16")
for png in sorted(OUT_DIR.glob("slide_*_wm.png")):
    png.unlink()
    print(f"Deleted: {png.name}")

for png in sorted(OUT_DIR.glob("slide_*.png")):
    if "_wm" in png.name:
        continue
    wm = pil_watermark(png)
    print(f"Re-WM: {Path(wm).name}")