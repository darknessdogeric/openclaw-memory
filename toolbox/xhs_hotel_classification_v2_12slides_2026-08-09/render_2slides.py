"""只重渲染 slide_11 和 slide_12"""
import os
from playwright.sync_api import sync_playwright
from PIL import Image

OUT_DIR = r"D:\B166ER-OpenClaw\workspace\toolbox\xhs_hotel_classification_v2_12slides_2026-08-09"
W, H = 1080, 1440
DSF = 2

SLIDES = [
    ("slide_11_lifestyle.html", "Lifestyle 跨越分级分类矩阵"),
    ("slide_12_final.html",     "酒店项目定位 · AI 化"),
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
    print("Done. 2 slides re-rendered.")