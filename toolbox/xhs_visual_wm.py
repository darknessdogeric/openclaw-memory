"""Visual watermark for slides 5/6/7 (PIL, fast, no hang)."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

OUT_DIR = Path(r"D:\B166ER-OpenClaw\workspace\output\xhs_2026-07-16")

for idx in [5, 6, 7]:
    png_path = OUT_DIR / f"slide_{idx:02d}.png"
    wm_path = OUT_DIR / f"slide_{idx:02d}_wm.png"

    img = Image.open(png_path).convert("RGBA")
    w, h = img.size

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Top-left B166ER tag
    try:
        font = ImageFont.truetype("arial.ttf", 28)
    except:
        font = ImageFont.load_default()
    draw.rectangle([(0, 0), (220, 56)], fill=(10, 37, 64, 200))
    draw.text((20, 14), "B166ER · ISSUE 001", fill=(255, 255, 255, 255), font=font)

    # Bottom-right B166ER stamp
    draw.rectangle([(w-200, h-56), (w, h)], fill=(10, 37, 64, 200))
    draw.text((w-180, h-42), "© B166ER 2026", fill=(255, 255, 255, 255), font=font)

    # Center diagonal watermark (light)
    big_font = ImageFont.truetype("arial.ttf", 72) if Path("C:/Windows/Fonts/arial.ttf").exists() else ImageFont.load_default()
    wm_text = "B166ER · 2026.07.16"
    bbox = draw.textbbox((0, 0), wm_text, font=big_font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    # 45-degree rotation via paste of rotated text
    txt_img = Image.new("RGBA", (tw + 20, th + 20), (0, 0, 0, 0))
    txt_draw = ImageDraw.Draw(txt_img)
    txt_draw.text((10, 10), wm_text, fill=(200, 200, 200, 50), font=big_font)
    txt_img = txt_img.rotate(-22, expand=True)
    tx = (w - txt_img.size[0]) // 2
    ty = (h - txt_img.size[1]) // 2
    overlay.paste(txt_img, (tx, ty), txt_img)

    out = Image.alpha_composite(img, overlay).convert("RGB")
    out.save(wm_path, "PNG", optimize=True)
    print(f"Slide {idx} visual WM: {wm_path.stat().st_size:,} bytes")

print("Done.")