import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\B166ER-openclaw\workspace\memory\小红书海报")

from playwright.sync_api import sync_playwright
from _illustrations import solar_svg, plaque_svg, probe_svg

OUT = r"D:\B166ER-openclaw\workspace\memory\小红书海报\头像预览"

TPL = """<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
*{margin:0;padding:0;}body{width:1000px;background:#0E1626;padding:10px;}
</style></head><body>__SVG__</body></html>"""

jobs = [("轨迹图.png", solar_svg()), ("铭牌图.png", plaque_svg()), ("探测器图.png", probe_svg())]
with sync_playwright() as p:
    b = p.chromium.launch(args=["--no-sandbox", "--disable-dev-shm-usage"])
    for name, svg in jobs:
        html = TPL.replace("__SVG__", svg)
        page = b.new_page(viewport={"width": 1000, "height": 460}, device_scale_factor=2)
        page.set_content(html, wait_until="domcontentloaded")
        page.wait_for_timeout(300)
        path = os.path.join(OUT, name)
        page.screenshot(path=path, full_page=True, omit_background=False, timeout=15000)
        print(f"OK {name} {os.path.getsize(path)} bytes")
        page.close()
    b.close()
print("DONE")
