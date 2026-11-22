"""Render V3 HTML 9 pages to PNG using Playwright (sync) - V2 with domcontentloaded fallback."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT_DIR = Path(r"C:/Users/ericz/Desktop/新媒体产品线/2026暑期对冲9图-v3.0/XHS-output")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(viewport={"width": 1080, "height": 1440}, device_scale_factor=2)
    page = ctx.new_page()
    files = sorted(OUT_DIR.glob("[0-9][0-9]_*.html"))
    print(f"Found {len(files)} HTML files")
    for i, html_path in enumerate(files, 1):
        url = f"file:///{html_path.resolve().as_posix()}"
        try:
            try:
                page.goto(url, wait_until="networkidle", timeout=15000)
            except Exception:
                page.goto(url, wait_until="domcontentloaded", timeout=15000)
            # 等待字体加载
            page.wait_for_timeout(3000)
            png_path = OUT_DIR / f"{i:02d}_v3.png"
            page.screenshot(path=str(png_path), full_page=False)
            print(f"  ✅ [{i:02d}/{len(files)}] {png_path.name} ({png_path.stat().st_size/1024:.1f} KB)")
        except Exception as e:
            print(f"  ❌ [{i:02d}] {html_path.name}: {e}")
    browser.close()
print("Done")
