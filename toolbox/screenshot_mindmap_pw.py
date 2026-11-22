"""
使用 Playwright 截图（带 JS 等待）
"""
import os
import sys

OUT_DIR = r"D:\B166ER-OpenClaw\workspace\outputs\酒管公司供应链工程-交付包-v1.0\04-思维导图"
HTML_PATH = os.path.join(OUT_DIR, "酒管公司供应链工程-思维导图.html")
PNG_1X = os.path.join(OUT_DIR, "酒管公司供应链工程-思维导图.png")
PNG_2X = os.path.join(OUT_DIR, "酒管公司供应链工程-思维导图-2x.png")

from playwright.sync_api import sync_playwright


def main():
    file_url = "file:///" + HTML_PATH.replace("\\", "/")
    print(f"URL: {file_url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )

        # 1x: 1080x1440
        print("\nGenerating 1x screenshot...")
        ctx1 = browser.new_context(viewport={"width": 1080, "height": 1440}, device_scale_factor=1)
        page1 = ctx1.new_page()
        page1.goto(file_url, wait_until="networkidle", timeout=30000)
        # 额外等待 JS markmap 渲染
        page1.wait_for_timeout(5000)
        page1.screenshot(path=PNG_1X, full_page=False, omit_background=False)
        ctx1.close()
        print(f"  1x: {os.path.getsize(PNG_1X):,} bytes")

        # 2x retina: 2160x2880（用 device_scale_factor=2 + 1080x1440 = 2160x2880）
        print("\nGenerating 2x retina screenshot...")
        ctx2 = browser.new_context(viewport={"width": 1080, "height": 1440}, device_scale_factor=2)
        page2 = ctx2.new_page()
        page2.goto(file_url, wait_until="networkidle", timeout=30000)
        page2.wait_for_timeout(5000)
        page2.screenshot(path=PNG_2X, full_page=False, omit_background=False)
        ctx2.close()
        print(f"  2x: {os.path.getsize(PNG_2X):,} bytes")

        browser.close()

    # 验证尺寸
    from PIL import Image
    img1 = Image.open(PNG_1X)
    img2 = Image.open(PNG_2X)
    print(f"\n1x actual size: {img1.size}")
    print(f"2x actual size: {img2.size}")


if __name__ == "__main__":
    main()