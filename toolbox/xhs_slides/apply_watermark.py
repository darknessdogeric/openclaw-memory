import sys
sys.path.insert(0, r"D:\B166ER-OpenClaw\workspace\toolbox")
from watermark_tool import protect_output
import os

OUTPUT_DIR = r"D:\B166ER-OpenClaw\workspace\toolbox\xhs_slides\output"
WATERMARKED_DIR = r"D:\B166ER-OpenClaw\workspace\toolbox\xhs_slides\watermarked"
os.makedirs(WATERMARKED_DIR, exist_ok=True)

files = [
    "01_封面.png",
    "02_要素1_产能识别.png",
    "03_要素2_客群区隔.png",
    "04_要素3_解耦定价.png",
    "05_要素4_消耗加速器.png",
    "06_要素5_边界条件.png",
    "07_成果与方法论.png",
]

for fname in files:
    src = os.path.join(OUTPUT_DIR, fname)
    dst = os.path.join(WATERMARKED_DIR, fname)
    try:
        wm_img = protect_output(src, tag=f"B166ER-{fname[:2]}")
        wm_img.save(dst)
        print(f"Watermarked: {fname} -> saved to {dst}")
    except Exception as e:
        print(f"Error on {fname}: {e}")

print("All watermarks applied!")
