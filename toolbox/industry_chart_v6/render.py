"""v6 海报渲染 + 水印（修复版 retina 水印）"""
import os
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

HTML = r"D:\B166ER-OpenClaw\workspace\toolbox\industry_chart_v6\cycle_forecast_v6.html"
OUT_DIR = r"D:\B166ER-OpenClaw\workspace\toolbox\industry_chart_v6"
W, H = 1080, 1920
DSF = 2

print("[1/2] Rendering HTML to PNG...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": W, "height": H}, device_scale_factor=DSF)
    page = context.new_page()
    page.goto(f"file:///{HTML.replace(chr(92), '/')}")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1500)
    page.screenshot(path=os.path.join(OUT_DIR, "output.png"), type="png", full_page=False)
    browser.close()

print("[2/2] Applying watermark...")
img = Image.open(os.path.join(OUT_DIR, "output.png")).convert("RGBA")
W_img, H_img = img.size
overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)
text = "(c) ERIC-B166ER - 2026.07.21"
font_size = 26
font = ImageFont.truetype("arial.ttf", font_size)
bbox = draw.textbbox((0, 0), text, font=font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
margin = 150
x, y = W_img - tw - margin, H_img - th - margin
draw.rounded_rectangle([x-18, y-10, x+tw+18, y+th+10], radius=10, fill=(26, 31, 58, 200))
draw.text((x, y), text, fill=(242, 237, 227, 255), font=font)
final = Image.alpha_composite(img, overlay).convert("RGB")
final.save(os.path.join(OUT_DIR, "watermarked.png"), "PNG", optimize=True)
print(f"Done: {os.path.join(OUT_DIR, 'watermarked.png')} ({W_img}x{H_img})")