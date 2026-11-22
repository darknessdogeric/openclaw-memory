"""Render hotel_benchmark.html → 1920x1080 PNG (Retina 2x)."""
from playwright.sync_api import sync_playwright
from pathlib import Path
import sys

HTML = Path(__file__).parent / "hotel_benchmark.html"
OUT  = Path(__file__).parent / "hotel_benchmark.png"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=2,   # Retina
            locale="zh-CN",
        )
        page = ctx.new_page()
        page.goto(f"file://{HTML.resolve()}", wait_until="networkidle")
        # capture full page bounds (page is exactly 1920x1080)
        page.screenshot(path=str(OUT), clip={"x":0,"y":0,"width":1920,"height":1080})
        browser.close()
    print(f"OK: {OUT}  size={OUT.stat().st_size:,} bytes")

if __name__ == "__main__":
    main()
