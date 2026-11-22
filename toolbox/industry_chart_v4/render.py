import os
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

HTML = r"D:\B166ER-OpenClaw\workspace\toolbox\industry_chart_v4\cycle_forecast_v4.html"
OUT = r"D:\B166ER-OpenClaw\workspace\toolbox\industry_chart_v4\output.png"
WM = r"D:\B166ER-OpenClaw\workspace\toolbox\industry_chart_v4\watermarked.png"

# 9:16 mobile - 1080 x 1920
W, H = 1080, 1920

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": W, "height": H}, device_scale_factor=2)
    page = context.new_page()
    page.goto(f"file:///{HTML.replace(chr(92), '/')}")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1200)
    page.screenshot(path=OUT, type="png", full_page=False)
    browser.close()
print("Captured")

# Watermark (bottom-right, more visible)
img = Image.open(OUT).convert("RGBA")
overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)
text = "© B166ER-20260721"
try:
    font = ImageFont.truetype("arial.ttf", max(int(W * 0.022), 18))
except:
    font = ImageFont.load_default()
bbox = draw.textbbox((0, 0), text, font=font)
tw = bbox[2] - bbox[0]; th = bbox[3] - bbox[1]
x, y = W - tw - 30, H - th - 30
draw.rounded_rectangle([x-12, y-10, x+tw+12, y+th+10], radius=10, fill=(201,169,97,200))
draw.text((x, y), text, fill=(13,27,42,255), font=font)
final = Image.alpha_composite(img, overlay).convert("RGB")
final.save(WM, "PNG", optimize=True)
print(f"Saved: {WM}")
print(f"Size: {final.size}")