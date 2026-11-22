"""小红书 10 张连图 · 批量渲染 + 水印
酒店分级分类深度图鉴 · 2026-08-09
1080 x 1440 (3:4)
DSF=2 (retina, Eric 2026-05-21)
"""
import os
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = r"D:\B166ER-OpenClaw\workspace\toolbox\xhs_hotel_classification_10slides_2026-08-09"
W, H = 1080, 1440
DSF = 2

SLIDES = [
    ("slide_01_cover.html",         "封面 · 分级分类"),
    ("slide_02_principle.html",     "Eric 铁律"),
    ("slide_03_history.html",       "150 年 5 段演进"),
    ("slide_04_china_3tiers.html",  "中国三层叠加"),
    ("slide_05_global_grade.html",  "国际评级+集团 Tier"),
    ("slide_06_lifestyle_def.html", "Lifestyle 三个硬指标"),
    ("slide_07_global_lifestyle.html", "国际 Lifestyle 15 品牌"),
    ("slide_08_china_lifestyle.html",  "国内 Lifestyle 第一梯队"),
    ("slide_09_modular.html",       "模块化+单房造价"),
    ("slide_10_final.html",         "未来+金句"),
]

def render():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": W, "height": H}, device_scale_factor=DSF)
        for html_file, name in SLIDES:
            html_path = os.path.join(OUT_DIR, html_file)
            png_path = os.path.join(OUT_DIR, html_file.replace(".html", ".png"))
            print(f"Rendering {html_file} ... {name}")
            page = context.new_page()
            page.goto(f"file:///{html_path.replace(chr(92), '/')}")
            page.wait_for_load_state("networkidle")
            page.wait_for_timeout(1500)
            page.screenshot(path=png_path, type="png", full_page=False)
            page.close()
            print(f"  -> {png_path}")
        browser.close()

def add_watermark():
    for html_file, _ in SLIDES:
        png_path = os.path.join(OUT_DIR, html_file.replace(".html", ".png"))
        wm_path = os.path.join(OUT_DIR, html_file.replace(".html", "_wm.png"))
        img = Image.open(png_path).convert("RGBA")
        W_img, H_img = img.size
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        # 改用水印工具的 tag 格式
        text = "B166ER . 2026.08.09"
        font_size = max(int(W * 0.012 * DSF), 11 * DSF)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        margin = 120
        x = W_img - tw - margin
        y = H_img - th - margin
        # 改用 B166ER 品牌色 + ERIC 的水印
        draw.rounded_rectangle([x - 18, y - 10, x + tw + 18, y + th + 10], radius=10, fill=(200, 16, 46, 200))
        draw.text((x, y), text, fill=(242, 237, 227, 255), font=font)
        final = Image.alpha_composite(img, overlay).convert("RGB")
        final.save(wm_path, "PNG", optimize=True)
        print(f"Watermarked: {wm_path}  ({W_img}x{H_img})")

if __name__ == "__main__":
    render()
    print()
    add_watermark()
    print("Done. 10 watermarked PNGs ready.")