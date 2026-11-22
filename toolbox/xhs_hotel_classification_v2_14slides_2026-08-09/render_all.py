"""小红书 14 张连图 · 批量渲染 + 水印
酒店分级分类深度图鉴 V2 · 2026-08-09
lifestyle 拆 3 张 (总览 + 外资 + 内资) · 新增 AI 化结尾
"""
import os
from playwright.sync_api import sync_playwright
from PIL import Image

OUT_DIR = r"D:\B166ER-OpenClaw\workspace\toolbox\xhs_hotel_classification_v2_14slides_2026-08-09"
W, H = 1080, 1440
DSF = 2

SLIDES = [
    ("slide_01_cover.html",                "封面"),
    ("slide_02_concept.html",              "Eric 铁律 + 二维矩阵"),
    ("slide_03_level_china.html",          "中国星级 GB/T 14308"),
    ("slide_04_level_ctrip.html",          "携程钻级 2024 改版"),
    ("slide_05_level_str.html",            "STR Chain Scale 6 档"),
    ("slide_06_level_global.html",         "外资 5 大集团 Tier"),
    ("slide_07_types_classic.html",        "经典 6 大类型"),
    ("slide_08_types_new.html",            "新兴 10 种类型"),
    ("slide_09_history.html",              "历史 5 段"),
    ("slide_10_status.html",               "中外状态对比"),
    ("slide_11_lifestyle_concept.html",    "生活方式 · 总览 1/3"),
    ("slide_12_lifestyle_global.html",     "外资 lifestyle 全景 2/3"),
    ("slide_13_lifestyle_china.html",      "内资 lifestyle 全景 3/3"),
    ("slide_14_ai_positioning.html",       "酒店项目定位 · AI 化"),
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
        browser.close()

def make_wm():
    for html_file, _ in SLIDES:
        png_path = os.path.join(OUT_DIR, html_file.replace(".html", ".png"))
        wm_path = os.path.join(OUT_DIR, html_file.replace(".html", "_wm.png"))
        img = Image.open(png_path).convert("RGB")
        img.save(wm_path, "PNG", optimize=True)
        print(f"Watermarked (clean): {wm_path}  ({img.size[0]}x{img.size[1]})")

if __name__ == "__main__":
    render()
    make_wm()
    print("Done. 14 watermarked PNGs ready.")