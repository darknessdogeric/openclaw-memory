"""小红书 12 张连图 · 批量渲染 + 水印
酒店分级分类深度图鉴 V2 · 2026-08-09
1080 x 1440 (3:4)
DSF=2 (retina, Eric 2026-05-21)
范式参考: C:\\Users\\ericz\\Desktop\\xhs_marketcode_2026-08-08\\
"""
import os
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = r"D:\B166ER-OpenClaw\workspace\toolbox\xhs_hotel_classification_v2_12slides_2026-08-09"
W, H = 1080, 1440
DSF = 2

SLIDES = [
    ("slide_01_cover.html",         "封面"),
    ("slide_02_concept.html",       "Eric 铁律 + 二维矩阵"),
    ("slide_03_level_china.html",   "中国星级 GB/T 14308"),
    ("slide_04_level_ctrip.html",   "携程钻级 2024 改版"),
    ("slide_05_level_str.html",     "STR Chain Scale 6 档"),
    ("slide_06_level_global.html",  "外资 5 大集团 Tier"),
    ("slide_07_types_classic.html", "经典 6 大类型"),
    ("slide_08_types_new.html",     "新兴 10 种类型"),
    ("slide_09_history.html",       "历史 5 段"),
    ("slide_10_status.html",        "中外状态对比"),
    ("slide_11_lifestyle.html",     "Lifestyle 各级别位置"),
    ("slide_12_final.html",         "金句 + 未来"),
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
    """不画 PIL 视觉水印。底部品牌条 + B logo 已是品牌标识(R12 语义)。
    _wm 文件 = 原 PNG 干净输出,后续可批量调 watermark_tool 嵌不可见盲水印。"""
    for html_file, _ in SLIDES:
        png_path = os.path.join(OUT_DIR, html_file.replace(".html", ".png"))
        wm_path = os.path.join(OUT_DIR, html_file.replace(".html", "_wm.png"))
        img = Image.open(png_path).convert("RGB")
        img.save(wm_path, "PNG", optimize=True)
        print(f"Watermarked (clean): {wm_path}  ({img.size[0]}x{img.size[1]})")

if __name__ == "__main__":
    render()
    print()
    add_watermark()
    print("Done. 12 watermarked PNGs ready.")