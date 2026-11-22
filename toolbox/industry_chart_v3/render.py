import os
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

HTML = r"D:\B166ER-OpenClaw\workspace\toolbox\industry_chart_v3\cycle_forecast.html"
OUT = r"D:\B166ER-OpenClaw\workspace\toolbox\industry_chart_v3\output.png"
WM = r"D:\B166ER-OpenClaw\workspace\toolbox\industry_chart_v3\watermarked.png"

# 9:16 mobile - 1080 x 1920
W, H = 1080, 1920

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": W, "height": H})
    page = context.new_page()
    page.goto(f"file:///{HTML.replace(chr(92), '/')}")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1000)
    page.screenshot(path=OUT, type="png")
    browser.close()
print("Captured")

# Watermark (bottom-right)
img = Image.open(OUT).convert("RGBA")
overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)
text = "© B166ER"
try:
    font = ImageFont.truetype("arial.ttf", max(int(W * 0.018), 16))
except:
    font = ImageFont.load_default()
bbox = draw.textbbox((0, 0), text, font=font)
tw = bbox[2] - bbox[0]; th = bbox[3] - bbox[1]
x, y = W - tw - 24, H - th - 24
draw.rounded_rectangle([x-10, y-10, x+tw+10, y+th+10], radius=8, fill=(201,169,97,180))
draw.text((x, y), text, fill=(13,27,42,255), font=font)
final = Image.alpha_composite(img, overlay).convert("RGB")
final.save(WM, "PNG")
print(f"Saved: {WM}")
