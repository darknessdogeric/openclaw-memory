import os
from playwright.sync_api import sync_playwright

HTML_DIR = r"D:\B166ER-OpenClaw\workspace\toolbox\xhs_slides_v2"
OUTPUT_DIR = r"D:\B166ER-OpenClaw\workspace\toolbox\xhs_slides_v2\output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

files = [
    ("slide_01_cover.html",    "01_封面.png"),
    ("slide_02_el1.html",      "02_要素1_区位产能识别.png"),
    ("slide_03_el2.html",      "03_要素2_客群数学区隔.png"),
    ("slide_04_el3.html",      "04_要素3_价值解耦.png"),
    ("slide_05_el4.html",      "05_要素4_客户沉淀.png"),
    ("slide_06_el5.html",      "06_要素5_边界条件.png"),
    ("slide_07_results.html",  "07_本质升华.png"),
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1080, "height": 1440})
    page = context.new_page()
    for html_file, out_name in files:
        html_path = os.path.join(HTML_DIR, html_file).replace("\\", "/")
        out_path = os.path.join(OUTPUT_DIR, out_name)
        page.goto(f"file:///{html_path}")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(800)
        page.screenshot(path=out_path, type="png")
        print(f"OK: {out_name}")
    browser.close()

print("All done!")
