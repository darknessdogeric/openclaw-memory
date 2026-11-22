import asyncio
import os
from playwright.async_api import async_playwright

HTML_DIR = r"D:\B166ER-OpenClaw\workspace\toolbox\xhs_slides"
OUTPUT_DIR = r"D:\B166ER-OpenClaw\workspace\toolbox\xhs_slides\output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

files = [
    ("slide_01_cover.html", "01_封面.png"),
    ("slide_02_el1.html",   "02_要素1_产能识别.png"),
    ("slide_03_el2.html",   "03_要素2_客群区隔.png"),
    ("slide_04_el3.html",   "04_要素3_解耦定价.png"),
    ("slide_05_el4.html",   "05_要素4_消耗加速器.png"),
    ("slide_06_el5.html",   "06_要素5_边界条件.png"),
    ("slide_07_results.html","07_成果与方法论.png"),
]

async def capture_all():
    async with async_playwright() as p:
        browser = await p.chromium.connect_over_cdp("http://127.0.0.1:9222")
        context = await browser.new_context(viewport={"width": 1080, "height": 1440})
        page = await context.new_page()
        for html_file, out_name in files:
            html_path = os.path.join(HTML_DIR, html_file)
            out_path = os.path.join(OUTPUT_DIR, out_name)
            await page.goto(f"file:///{html_path.replace(chr(92), '/')}")
            await page.wait_for_load_state("networkidle")
            await asyncio.sleep(0.5)
            await page.screenshot(path=out_path, type="png", full_page=False)
            print(f"Captured: {out_name}")
        await browser.close()
    print("All done!")

asyncio.run(capture_all())
