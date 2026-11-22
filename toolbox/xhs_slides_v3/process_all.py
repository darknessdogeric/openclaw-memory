import os
from playwright.sync_api import sync_playwright
from PIL import Image, ImageDraw, ImageFont

HTML_DIR = r"D:\B166ER-OpenClaw\workspace\toolbox\xhs_slides_v3"
OUTPUT_DIR = r"D:\B166ER-OpenClaw\workspace\toolbox\xhs_slides_v3\output"
WATERMARKED_DIR = r"D:\B166ER-OpenClaw\workspace\toolbox\xhs_slides_v3\watermarked"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(WATERMARKED_DIR, exist_ok=True)

files = [
    ("slide_01_cover.html",    "01_封面.png"),
    ("slide_02_el1.html",      "02_要素1_区位产能识别.png"),
    ("slide_03_el2.html",      "03_要素2_客群数学区隔.png"),
    ("slide_04_el3.html",      "04_要素3_价值解耦.png"),
    ("slide_05_el4.html",      "05_要素4_客户沉淀.png"),
    ("slide_06_el5.html",      "06_要素5_边界条件.png"),
    ("slide_07_results.html",  "07_本质升华.png"),
]

# Step 1: Capture screenshots
print("Step 1: Capturing screenshots...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(viewport={"width": 1080, "height": 1440})
    page = context.new_page()
    for html_file, out_name in files:
        html_path = os.path.join(HTML_DIR, html_file).replace("\\", "/")
        out_path = os.path.join(OUTPUT_DIR, out_name)
        page.goto(f"file:///{html_path}")
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(800)
        page.screenshot(path=out_path, type="png")
        print(f"  OK: {out_name}")
    browser.close()

# Step 2: Apply watermarks
print("\nStep 2: Applying watermarks...")
def add_watermark(src_path, dst_path, tag_text="B166ER"):
    img = Image.open(src_path).convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    w, h = img.size
    text = f"© {tag_text}"
    try:
        font_size = max(int(w * 0.018), 16)
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    padding = 20
    x = w - tw - padding
    y = h - th - padding
    bg_padding = 8
    bg_box = [x - bg_padding, y - bg_padding, x + tw + bg_padding, y + th + bg_padding]
    draw.rounded_rectangle(bg_box, radius=6, fill=(0, 0, 0, 120))
    draw.text((x, y), text, fill=(255, 255, 255, 230), font=font)
    watermarked = Image.alpha_composite(img, overlay)
    final = watermarked.convert("RGB")
    final.save(dst_path, "PNG")
    print(f"  Watermarked: {os.path.basename(dst_path)}")

for _, fname in files:
    src = os.path.join(OUTPUT_DIR, fname)
    dst = os.path.join(WATERMARKED_DIR, fname)
    if os.path.exists(src):
        add_watermark(src, dst)

print("\nAll done!")
