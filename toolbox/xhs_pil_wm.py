"""Step 2: Add visual watermark to all 7 slides (PIL, no hang)."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT_DIR = Path(r"D:\B166ER-OpenClaw\workspace\output\xhs_2026-07-16")

# Try to find a good font
font_paths = [
    r"C:\Windows\Fonts\arialbd.ttf",
    r"C:\Windows\Fonts\msyhbd.ttc",
    r"C:\Windows\Fonts\msyh.ttc",
    r"C:\Windows\Fonts\arial.ttf",
]
font_main = None
for fp in font_paths:
    if Path(fp).exists():
        font_main = ImageFont.truetype(fp, 22)
        break
if font_main is None:
    font_main = ImageFont.load_default()

font_stamp = None
for fp in font_paths:
    if Path(fp).exists():
        font_stamp = ImageFont.truetype(fp, 26)
        break

for idx in range(1, 8):
    png_path = OUT_DIR / f"slide_{idx:02d}.png"
    wm_path = OUT_DIR / f"slide_{idx:02d}_wm.png"

    img = Image.open(png_path).convert("RGBA")
    w, h = img.size

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Top-left B166ER tag
    draw.rectangle([(0, 0), (240, 60)], fill=(10, 37, 64, 220))
    draw.text((20, 18), "B166ER · ISSUE 001", fill=(255, 255, 255, 255), font=font_main)

    # Bottom-right B166ER stamp
    draw.rectangle([(w-220, h-60), (w, h)], fill=(10, 37, 64, 220))
    draw.text((w-200, h-44), "© B166ER 2026", fill=(255, 255, 255, 255), font=font_main)

    # Center diagonal watermark (very faint)
    if font_stamp:
        wm_text = "B166ER · 2026.07.16"
        bbox = draw.textbbox((0, 0), wm_text, font=font_stamp)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        txt_img = Image.new("RGBA", (tw + 40, th + 40), (0, 0, 0, 0))
        txt_draw = ImageDraw.Draw(txt_img)
        txt_draw.text((20, 20), wm_text, fill=(200, 200, 200, 35), font=font_stamp)
        txt_img = txt_img.rotate(-22, expand=True)
        tx = (w - txt_img.size[0]) // 2
        ty = (h - txt_img.size[1]) // 2
        overlay.paste(txt_img, (tx, ty), txt_img)

    out = Image.alpha_composite(img, overlay).convert("RGB")
    out.save(wm_path, "PNG", optimize=True)
    print(f"Slide {idx} WM: {wm_path.stat().st_size:,} bytes")

print("=== Watermark complete ===")