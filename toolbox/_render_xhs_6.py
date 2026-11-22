"""Render 6 HTML files to PNG via Playwright."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT_DIR = Path(r"C:/Users/ericz/Desktop/小红书产品线/2026十五五酒店业6图-v1.0/XHS-output")

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    ctx = b.new_context(viewport={"width": 1080, "height": 1440}, device_scale_factor=2)
    page = ctx.new_page()
    files = sorted(OUT_DIR.glob("[0-9][0-9]_*.html"))
    print(f"Found {len(files)} files")
    for i, html_path in enumerate(files, 1):
        try:
            page.goto(f"file:///{html_path.resolve().as_posix()}", wait_until="domcontentloaded", timeout=15000)
        except Exception:
            page.goto(f"file:///{html_path.resolve().as_posix()}", wait_until="load", timeout=15000)
        page.wait_for_timeout(3000)
        png_path = OUT_DIR / f"{i:02d}_xhs.png"
        page.screenshot(path=str(png_path), full_page=False)
        print(f"  ✅ [{i:02d}/{len(files)}] {png_path.name} ({png_path.stat().st_size/1024:.1f} KB)")
    b.close()
print("Done")
