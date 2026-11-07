import os
import sys
from playwright.sync_api import sync_playwright

SRC = r"D:\B166ER-openclaw\workspace\memory\小红书海报"
files = [
    "hotel_location_brand_orange.html",
    "hotel_location_xhs_sakura.html",
    "hotel_location_luxe_gold.html",
]
out_dir = SRC
log = []

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-web-security"])
        for html_name in files:
            png_name = html_name.replace(".html", ".png")
            src_path = os.path.join(SRC, html_name)
            dst_path = os.path.join(out_dir, png_name)
            with open(src_path, "r", encoding="utf-8") as f:
                html = f.read()
            page = browser.new_page(viewport={"width": 1080, "height": 1440}, device_scale_factor=2)
            page.set_content(html, wait_until="domcontentloaded")
            page.wait_for_timeout(300)
            page.screenshot(path=dst_path, full_page=False, omit_background=False, timeout=15000)
            size = os.path.getsize(dst_path)
            log.append(f"OK {png_name} {size} bytes")
            page.close()
        browser.close()
    log.append("DONE")
except Exception as e:
    import traceback
    log.append(f"ERROR: {type(e).__name__}: {e}")
    log.append(traceback.format_exc())

for line in log:
    print(line, flush=True)
