"""小红书 9 张连图 · 批量渲染 + 水印
2026年8月酒店市场预测专题
1080 x 1440 (3:4 小红书)
DSF=2 (retina, Eric 2026-05-21 明确要求)
"""
import os
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = r"D:\B166ER-OpenClaw\workspace\toolbox\xhs_hotel_9slides_aug2026"
W, H = 1080, 1440  # 小红书 3:4
DSF = 2

SLIDES = [
    ("slide_01_cover.html",     "8月定性"),
    ("slide_02_sources.html",   "61信源"),
    ("slide_03_baseline.html",  "现状基线"),
    ("slide_04_headlines.html", "头部集团"),
    ("slide_05_summer_log.html","暑期透支"),
    ("slide_06_predictions.html","三大预测"),
    ("slide_07_structure.html", "结构性分化"),
    ("slide_08_engines.html",   "三大引擎"),
    ("slide_09_final.html",     "终极判断"),
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
            print(f"  → {png_path}")

        browser.close()
    print("\nAll base PNGs rendered.")

def add_watermark():
    """加右下角水印 - 与 7slides 同款"""
    for html_file, _ in SLIDES:
        png_path = os.path.join(OUT_DIR, html_file.replace(".html", ".png"))
        wm_path = os.path.join(OUT_DIR, html_file.replace(".html", "_wm.png"))

        img = Image.open(png_path).convert("RGBA")
        W_img, H_img = img.size

        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        text = "© ERIC & B166ER · 2026.07.25"

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
    print("\n✅ All done. 9 watermarked PNGs ready.")
