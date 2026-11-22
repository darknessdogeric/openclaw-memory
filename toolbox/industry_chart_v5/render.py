import os
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

HTML = r"D:\B166ER-OpenClaw\workspace\toolbox\industry_chart_v5\cycle_forecast_v5.html"
OUT = r"D:\B166ER-OpenClaw\workspace\toolbox\industry_chart_v5\output.png"
WM = r"D:\B166ER-OpenClaw\workspace\toolbox\industry_chart_v5\watermarked.png"

# 9:16 mobile - 1080 x 1920 (viewport size)
W, H = 1080, 1920
DSF = 2  # device scale factor for retina (Eric 2026-05-21 明确要求)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": W, "height": H}, device_scale_factor=DSF)
    page = context.new_page()
    page.goto(f"file:///{HTML.replace(chr(92), '/')}")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1200)
    page.screenshot(path=OUT, type="png", full_page=False)
    browser.close()
print(f"Captured: {OUT}")

# Watermark - FIX: 必须用实际图像尺寸计算位置（retina 下是 W*DSF x H*DSF）
img = Image.open(OUT).convert("RGBA")
W_img, H_img = img.size  # 实际是 2160 x 3840
print(f"Image actual size: {W_img}x{H_img}")

overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)
text = "© B166ER-20260721"

# 字号按 retina 调整（× DSF）
font_size = max(int(W * 0.022 * DSF), 18 * DSF)
try:
    font = ImageFont.truetype("arial.ttf", font_size)
except:
    font = ImageFont.load_default()

bbox = draw.textbbox((0, 0), text, font=font)
tw = bbox[2] - bbox[0]
th = bbox[3] - bbox[1]

# 关键修复：用实际图像尺寸算右下角位置
margin = 30 * DSF
x = W_img - tw - margin
y = H_img - th - margin

draw.rounded_rectangle(
    [x - 12*DSF, y - 10*DSF, x + tw + 12*DSF, y + th + 10*DSF],
    radius=10*DSF,
    fill=(201, 169, 97, 200)
)
draw.text((x, y), text, fill=(13, 27, 42, 255), font=font)

final = Image.alpha_composite(img, overlay).convert("RGB")
final.save(WM, "PNG", optimize=True)
print(f"Saved: {WM}")
print(f"Final size: {final.size}")
print(f"Watermark position: x={x}, y={y} (bottom-right corner of {W_img}x{H_img})")