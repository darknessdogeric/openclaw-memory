"""月度复盘海报渲染器 - 1080x1440 + 水印"""
import os
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

HTML = r"D:\B166ER-OpenClaw\workspace\toolbox\outputs\report-2026-08_v1.html"
OUT_DIR = r"D:\B166ER-OpenClaw\workspace\toolbox\outputs"
W, H = 1080, 1440
DSF = 2

print("[1/3] Rendering HTML → PNG (1080x1440 @2x)...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": W, "height": H}, device_scale_factor=DSF)
    page = context.new_page()
    page.goto(f"file:///{HTML.replace(chr(92), '/')}")
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(1500)
    page.screenshot(path=os.path.join(OUT_DIR, "report-2026-08_v1.png"), type="png", full_page=False)
    browser.close()

print("[2/3] Applying watermark + 双徽章...")
img = Image.open(os.path.join(OUT_DIR, "report-2026-08_v1.png")).convert("RGBA")
W_img, H_img = img.size

# 双徽章 - 左上
overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

# 左上徽章:数据时点
try:
    badge_font = ImageFont.truetype("arial.ttf", 28)
    title_font = ImageFont.truetype("arial.ttf", 22)
except:
    badge_font = ImageFont.load_default()
    title_font = ImageFont.load_default()

badge1_text = "2026.08"
bbox1 = draw.textbbox((0, 0), badge1_text, font=badge_font)
b1w = bbox1[2] - bbox1[0] + 36
b1h = bbox1[3] - bbox1[1] + 24
draw.rounded_rectangle([36, 36, 36+b1w, 36+b1h], radius=14, fill=(201, 169, 110, 235))
draw.text((54, 42), badge1_text, fill=(26, 31, 58, 255), font=badge_font)

# 右上徽章:月报标识
badge2_text = "MONTHLY"
bbox2 = draw.textbbox((0, 0), badge2_text, font=badge_font)
b2w = bbox2[2] - bbox2[0] + 36
b2h = bbox2[3] - bbox2[1] + 24
draw.rounded_rectangle([W_img-36-b2w, 36, W_img-36, 36+b2h], radius=14, fill=(107, 207, 127, 235))
draw.text((W_img-54-b2w+18, 42), badge2_text, fill=(26, 31, 58, 255), font=badge_font)

# 右下水印
text = "(c) ERIC-B166ER · 2026.09.15"
bbox = draw.textbbox((0, 0), text, font=title_font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
margin = 80
x = W_img - tw - margin
y = H_img - th - margin
draw.rounded_rectangle([x-18, y-10, x+tw+18, y+th+10], radius=10, fill=(26, 31, 58, 210))
draw.text((x, y), text, fill=(242, 237, 227, 255), font=title_font)

final = Image.alpha_composite(img, overlay).convert("RGB")
final.save(os.path.join(OUT_DIR, "report-2026-08_v1_wm.png"), "PNG", optimize=True)
print(f"[3/3] Done: {os.path.join(OUT_DIR, 'report-2026-08_v1_wm.png')} ({W_img}x{H_img})")
