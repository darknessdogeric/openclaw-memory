"""Check all 9 HTML files for overflow issues."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from playwright.sync_api import sync_playwright

OUT_DIR = Path(r"C:/Users/ericz/Desktop/新媒体产品线/2026暑期对冲9图-v3.0/XHS-output")

with sync_playwright() as p:
    b = p.chromium.launch(headless=True)
    ctx = b.new_context(viewport={"width": 1080, "height": 1440})
    page = ctx.new_page()
    files = sorted(OUT_DIR.glob("[0-9][0-9]_*.html"))
    print(f"{'ID':6} {'Body':>8} {'Viewport':>8} {'Diff':>8}  {'Status':>8}")
    print("-" * 60)
    for f in files:
        page.goto(f"file:///{f.resolve().as_posix()}", wait_until="domcontentloaded", timeout=10000)
        page.wait_for_timeout(800)
        h = page.evaluate("document.documentElement.scrollHeight")
        vh = page.evaluate("window.innerHeight")
        diff = h - vh
        status = "✓ OK" if diff <= 0 else f"❌ +{diff}px OVERFLOW"
        print(f"{f.name.split('_')[0]:6} {h:>8} {vh:>8} {diff:>8}  {status}")
    b.close()
