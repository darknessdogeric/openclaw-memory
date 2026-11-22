import os
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont
import numpy as np

OUT_DIR = r'D:\B166ER-OpenClaw\workspace\toolbox\xhs_hotel_7slides'
W, H = 1080, 1440
DSF = 2

SLIDES = [
    'slide_01_cover.html', 'slide_02_why.html', 'slide_03_data.html',
    'slide_04_trap.html', 'slide_05_forecast.html', 'slide_06_kshape.html',
    'slide_07_final.html',
]

print('=== Rendering HTML -> PNG ===')
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={'width': W, 'height': H}, device_scale_factor=DSF)
    for html_file in SLIDES:
        html_path = os.path.join(OUT_DIR, html_file)
        png_path = os.path.join(OUT_DIR, html_file.replace('.html', '.png'))
        page = context.new_page()
        page.goto('file:///' + html_path.replace(chr(92), chr(47)))
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(1500)
        page.screenshot(path=png_path, type='png', full_page=False)
        page.close()
        print('OK render:', html_file)
    browser.close()

print()
print('=== Applying watermark (margin=150) ===')
for html_file in SLIDES:
    png_path = os.path.join(OUT_DIR, html_file.replace('.html', '.png'))
    wm_path = os.path.join(OUT_DIR, html_file.replace('.html', '_wm.png'))
    img = Image.open(png_path).convert('RGBA')
    W_img, H_img = img.size
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    text = '© ERIC & B166ER · 2026.07.21'
    font_size = 26
    font = ImageFont.truetype('arial.ttf', font_size)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2]-bbox[0], bbox[3]-bbox[1]
    margin = 150
    x, y = W_img - tw - margin, H_img - th - margin
    draw.rounded_rectangle([x-18, y-10, x+tw+18, y+th+10], radius=10, fill=(26, 31, 58, 200))
    draw.text((x, y), text, fill=(242, 237, 227, 255), font=font)
    final = Image.alpha_composite(img, overlay).convert('RGB')
    final.save(wm_path, 'PNG', optimize=True)
    print('OK watermark:', os.path.basename(wm_path))

print()
print('=== Measuring bottom distances (slide_06 target: ~28px design) ===')
bg = np.array([242, 237, 227])
for html_file in SLIDES:
    wm_name = html_file.replace('.html', '_wm.png')
    wm = os.path.join(OUT_DIR, wm_name)
    img = np.array(Image.open(wm).convert('RGB'))
    H_img, W_img, _ = img.shape
    not_bg = np.abs(img.astype(int) - bg).sum(axis=2) > 20
    ys, _ = np.where(not_bg)
    content_bottom = H_img - ys.max() if len(ys) > 0 else 0
    design_px = content_bottom / 2
    status = 'OK' if 20 <= design_px <= 80 else ('TIGHT' if design_px < 20 else 'LOOSE')
    print(f'{wm_name:<32} content_bottom: {content_bottom:>4}px (retina) = {design_px:>5.1f}px (design)  [{status}]')