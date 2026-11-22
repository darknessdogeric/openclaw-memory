# -*- coding: utf-8 -*-
"""封面渲染 — 3:4 / 1080×1440 retina 2x"""
import sys
from pathlib import Path
from invisible_playwright import InvisiblePlaywright

OUT_DIR = Path(r"D:\B166ER-OpenClaw\workspace\toolbox\xhs_groups_trends")
HTML = OUT_DIR / "slide_00_cover.html"
PNG  = OUT_DIR / "slide_00_cover.png"

W, H, DSF = 1080, 1440, 2

URL = HTML.resolve().as_uri()

with InvisiblePlaywright() as browser:
    ctx = browser.new_context(viewport={"width": W, "height": H}, device_scale_factor=DSF)
    page = ctx.new_page()
    page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(800)
    page.screenshot(path=str(PNG), full_page=False, omit_background=False, type="png")

print(f"已输出: {PNG}")
print(f"实际像素: {W*DSF}x{H*DSF}")