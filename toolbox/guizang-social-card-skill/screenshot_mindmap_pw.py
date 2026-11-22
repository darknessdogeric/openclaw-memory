"""
v4.0 简化版:
- 不强制改 viewBox (避免破坏 SVG)
- viewport 给超大值, 让 markmap fit() 决定 SVG 尺寸
- 截 full_page (Playwright 自动捕获 body 实际尺寸)
"""
import os
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, r"D:\B166ER-OpenClaw\workspace\toolbox")
from watermark_tool import protect_output

OUT_DIR = r"D:\B166ER-OpenClaw\workspace\outputs\酒管公司供应链工程-交付包-v1.0\04-思维导图"
HTML_PATH = os.path.join(OUT_DIR, "酒管公司供应链工程-思维导图.html")
PNG_1X = os.path.join(OUT_DIR, "酒管公司供应链工程-思维导图.png")
PNG_2X = os.path.join(OUT_DIR, "酒管公司供应链工程-思维导图-2x.png")
PNG_3X = os.path.join(OUT_DIR, "酒管公司供应链工程-思维导图-3x.png")

from playwright.sync_api import sync_playwright


def shoot(browser, w, h, scale, out_path, label):
    ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=scale)
    page = ctx.new_page()
    file_url = "file:///" + HTML_PATH.replace("\\", "/")
    page.goto(file_url, wait_until="networkidle", timeout=60000)
    # 等 markmap fit() 完成 (脚本里有 5 次 500ms fit)
    page.wait_for_timeout(8000)
    page.screenshot(path=out_path, full_page=True, omit_background=False)
    ctx.close()
    size = os.path.getsize(out_path)
    print(f"  {label}: viewport={w}x{h}@{scale}x -> {size:,} bytes")


def main():
    file_url = "file:///" + HTML_PATH.replace("\\", "/")
    print(f"URL: {file_url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )

        # 1x baseline: 横向 viewport (宽 > 高) 让 markmap 选横向放射
        print("\n[1/3] 1x baseline (4800x2700)")
        shoot(browser, 4800, 2700, 1, PNG_1X, "1x")

        # 2x retina
        print("\n[2/3] 2x retina (4800x2700 @ 2x)")
        shoot(browser, 4800, 2700, 2, PNG_2X, "2x")

        # 3x ultra HD
        print("\n[3/3] 3x ultra HD (6400x3600 @ 3x)")
        shoot(browser, 6400, 3600, 3, PNG_3X, "3x")

        browser.close()

    # 关闭 PIL decompression bomb 限制
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None

    for label, p in [("1x", PNG_1X), ("2x", PNG_2X), ("3x", PNG_3X)]:
        img = Image.open(p)
        print(f"  {label} actual: {img.size}")

    print("\nWatermarking final 3x...")
    final_wm = os.path.join(OUT_DIR, "酒管公司供应链工程-思维导图-3x-wm.png")
    protect_output(PNG_3X, final_wm, tag="B166ER-20260711")
    print(f"  OK: {final_wm}")


if __name__ == "__main__":
    main()