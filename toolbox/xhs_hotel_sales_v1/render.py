"""Render sales V1 - 1 detail + 3 notes."""
import os
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

D = r"D:\B166ER-OpenClaw\workspace\toolbox\xhs_hotel_sales_v1"
W, H = 1080, 1440
DSF = 2

FILES = [
    ("slide_01_detail.html", "01_DETAIL"),
    ("slide_02_note1_pain.html", "02_NOTE1"),
    ("slide_03_note2_solution.html", "03_NOTE2"),
    ("slide_04_note3_samples.html", "04_NOTE3"),
]

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": W, "height": H}, device_scale_factor=DSF)
    for html, name in FILES:
        page = ctx.new_page()
        page.goto(f"file:///{os.path.join(D, html).replace(chr(92), '/')}")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1500)
        png = os.path.join(D, html.replace(".html", ".png"))
        page.screenshot(path=png, type="png", full_page=False)
        # Watermark
        img = Image.open(png).convert("RGBA")
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        text = "(c) ERIC.B166ER . 2026.07.26"
        try:
            font = ImageFont.truetype("arial.ttf", max(int(W*0.012*DSF), 11*DSF))
        except:
            font = ImageFont.load_default()
        bbox = draw.textbbox((0, 0), text, font=font)
        tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
        x = img.size[0] - tw - 120
        y = img.size[1] - th - 120
        draw.rounded_rectangle([x-18, y-10, x+tw+18, y+th+10], radius=10, fill=(26, 31, 58, 200))
        draw.text((x, y), text, fill=(242, 237, 227, 255), font=font)
        final = Image.alpha_composite(img, overlay).convert("RGB")
        wm = os.path.join(D, html.replace(".html", "_wm.png"))
        final.save(wm, "PNG", optimize=True)
        print(f"  rendered: {png} + {wm}")
        page.close()
    browser.close()
print("Done.")