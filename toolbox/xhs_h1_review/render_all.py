"""小红书 12 张连图 · 2026 H1 复盘（含人口结构维度）
基于模板风格（米白底 + 深红 + 深墨蓝 + 金棕）
1080 x 1440 (3:4)
DSF=2 (retina)
"""
import os
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = r"D:\B166ER-OpenClaw\workspace\toolbox\xhs_h1_review"
W, H = 1080, 1440
DSF = 2

SLIDES = [
    ("slide_01.html", "ONE-LINER"),
    ("slide_02.html", "CORE NUMBERS"),
    ("slide_03.html", "3 JUDGMENTS"),
    ("slide_04.html", "BASELINE TRAP"),
    ("slide_05.html", "ROOT CAUSE"),     # ⭐ 人口结构
    ("slide_06.html", "POPULATION IMPACT"),
    ("slide_07.html", "TOP 10 LISTED"),
    ("slide_08.html", "MID-END WAVE"),
    ("slide_09.html", "BIG OPPORTUNITY"),
    ("slide_10.html", "ACTION PLAN"),
    ("slide_11.html", "PRODUCTS"),
    ("slide_12.html", "FINAL WORD"),
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