import os
from PIL import Image, ImageDraw, ImageFont

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

def add_watermark(src_path, dst_path, tag_text="B166ER"):
    img = Image.open(src_path).convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Watermark text position: bottom-right
    w, h = img.size
    text = f"© {tag_text}"

    # Try to use a font, fallback to default
    try:
        font_size = max(int(w * 0.018), 16)
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()

    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    padding = 20
    x = w - tw - padding
    y = h - th - padding

    # Semi-transparent dark background
    bg_padding = 8
    bg_box = [x - bg_padding, y - bg_padding, x + tw + bg_padding, y + th + bg_padding]
    draw.rounded_rectangle(bg_box, radius=6, fill=(0, 0, 0, 120))
    draw.text((x, y), text, fill=(255, 255, 255, 230), font=font)

    watermarked = Image.alpha_composite(img, overlay)
    final = watermarked.convert("RGB")
    final.save(dst_path, "PNG")
    print(f"Watermarked: {os.path.basename(dst_path)}")

for fname in files:
    src = os.path.join(OUTPUT_DIR, fname)
    dst = os.path.join(WATERMARKED_DIR, fname)
    if os.path.exists(src):
        add_watermark(src, dst)
    else:
        print(f"Not found: {src}")

print("All watermarks applied!")
