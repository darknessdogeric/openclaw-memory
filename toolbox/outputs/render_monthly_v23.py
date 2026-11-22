"""月报海报 2-3 渲染器"""
import os
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

PAIRS = [
    ("report-2026-08_v2.html", "report-2026-08_v2.png", "report-2026-08_v2_wm.png", "CASES"),
    ("report-2026-08_v3.html", "report-2026-08_v3.png", "report-2026-08_v3_wm.png", "RANKING"),
]
OUT_DIR = r"D:\B166ER-OpenClaw\workspace\toolbox\outputs"
W, H = 1080, 1440
DSF = 2

for src, mid, dst, badge_text in PAIRS:
    HTML = os.path.join(OUT_DIR, src)
    print(f"\n[Render] {src}...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": W, "height": H}, device_scale_factor=DSF)
        page = context.new_page()
        page.goto(f"file:///{HTML.replace(chr(92), '/')}")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1200)
        page.screenshot(path=os.path.join(OUT_DIR, mid), type="png", full_page=False)
        browser.close()

    # Watermark
    img = Image.open(os.path.join(OUT_DIR, mid)).convert("RGBA")
    W_img, H_img = img.size
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    try:
        badge_font = ImageFont.truetype("arial.ttf", 28)
        title_font = ImageFont.truetype("arial.ttf", 22)
    except:
        badge_font = ImageFont.load_default()
        title_font = ImageFont.load_default()

    # 左上:数据时点
    bbox1 = draw.textbbox((0, 0), "2026.08", font=badge_font)
    b1w = bbox1[2] - bbox1[0] + 36
    b1h = bbox1[3] - bbox1[1] + 24
    draw.rounded_rectangle([36, 36, 36+b1w, 36+b1h], radius=14, fill=(201, 169, 110, 235))
    draw.text((54, 42), "2026.08", fill=(26, 31, 58, 255), font=badge_font)

    # 右上:板块标识
    bbox2 = draw.textbbox((0, 0), badge_text, font=badge_font)
    b2w = bbox2[2] - bbox2[0] + 36
    b2h = bbox2[3] - bbox2[1] + 24
    draw.rounded_rectangle([W_img-36-b2w, 36, W_img-36, 36+b2h], radius=14, fill=(107, 207, 127, 235))
    draw.text((W_img-54-b2w+18, 42), badge_text, fill=(26, 31, 58, 255), font=badge_font)

    # 右下水印
    text = "(c) ERIC-B166ER · 2026.09.15"
    bbox = draw.textbbox((0, 0), text, font=title_font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    margin = 80
    x = W_img - tw - margin
    y = H_img - th - margin
    draw.rounded_rectangle([x-18, y-10, x+tw+18, y+th+10], radius=10, fill=(26, 31, 58, 210))
    draw.text((x, y), text, fill=(242, 237, 227, 255), font=title_font)

    final = Image.alpha_composite(img, overlay).convert("RGB")
    final.save(os.path.join(OUT_DIR, dst), "PNG", optimize=True)
    print(f"[Saved] {dst} ({W_img}x{H_img})")

print("\nAll 3 posters done.")
