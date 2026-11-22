"""小红书 12 张连图 · 10 家集团 + 趋势分析
1080 x 1440 (3:4)
DSF=2 (retina)
"""
import os
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = r"D:\B166ER-OpenClaw\workspace\toolbox\xhs_groups_trends"
W, H = 1080, 1440
DSF = 2

SLIDES = [
    ("slide_01_锦江.html", "JINJIANG"),
    ("slide_02_华住.html", "HUAZHU"),
    ("slide_03_首旅.html", "BTG-HOTELS"),
    ("slide_04_亚朵.html", "ATAT"),
    ("slide_05_格林.html", "GREEN"),
    ("slide_06_万豪.html", "MARRIOTT"),
    ("slide_07_洲际.html", "IHG"),
    ("slide_08_希尔顿.html", "HILTON"),
    ("slide_09_雅高.html", "ACCOR"),
    ("slide_10_凯悦.html", "HYATT"),
    ("slide_11_trends.html", "TRENDS"),
    ("slide_12_structure.html", "STRUCTURE"),
]

def render():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": W, "height": H},
            device_scale_factor=DSF
        )

        for html_file, _ in SLIDES:
            html_path = os.path.join(OUT_DIR, html_file)
            png_path = os.path.join(OUT_DIR, html_file.replace(".html", ".png"))
            print(f"Rendering: {html_file} ...")

            page = context.new_page()
            page.goto(f"file:///{html_path.replace(chr(92), '/')}")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1500)
            page.screenshot(path=png_path, type="png", full_page=False)
            page.close()
            print(f"  -> {png_path}")

        browser.close()
    print("\nAll base PNGs rendered.")

def add_watermark():
    for html_file, _ in SLIDES:
        png_path = os.path.join(OUT_DIR, html_file.replace(".html", ".png"))
        wm_path = os.path.join(OUT_DIR, html_file.replace(".html", "_wm.png"))

        img = Image.open(png_path).convert("RGBA")
        W_img, H_img = img.size

        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        text = "(c) ERIC B166ER / 2026.07.23"

        font_size = max(int(W * 0.015 * DSF), 14 * DSF)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]

        margin = 150
        x = W_img - tw - margin
        y = H_img - th - margin

        draw.rounded_rectangle(
            [x - 18, y - 10, x + tw + 18, y + th + 10],
            radius=10,
            fill=(26, 31, 58, 200)
        )
        draw.text((x, y), text, fill=(242, 237, 227, 255), font=font)

        final = Image.alpha_composite(img, overlay).convert("RGB")
        final.save(wm_path, "PNG", optimize=True)
        print(f"Watermarked: {wm_path}  ({W_img}x{H_img})")

if __name__ == "__main__":
    render()
    print()
    add_watermark()
    print("\n[OK] All done. 12 watermarked PNGs ready.")