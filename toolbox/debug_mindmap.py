"""调试 mindmap 渲染问题"""
import os
from playwright.sync_api import sync_playwright

OUT_DIR = r"D:\B166ER-OpenClaw\workspace\outputs\酒管公司供应链工程-交付包-v1.0\04-思维导图"
HTML_PATH = os.path.join(OUT_DIR, "酒管公司供应链工程-思维导图.html")

file_url = "file:///" + HTML_PATH.replace("\\", "/")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    ctx = browser.new_context(viewport={"width": 1080, "height": 1440})
    page = ctx.new_page()

    # 捕获 console
    page.on("console", lambda msg: print(f"[CONSOLE {msg.type}] {msg.text}"))
    page.on("pageerror", lambda err: print(f"[PAGEERROR] {err}"))

    page.goto(file_url, wait_until="load", timeout=30000)
    page.wait_for_timeout(8000)

    # 检查 SVG 内容
    svg_html = page.evaluate("() => document.getElementById('mindmap').outerHTML.substring(0, 500)")
    print(f"\n[SVG PREVIEW] {svg_html}")

    # 检查 svg 内部子节点数
    child_count = page.evaluate("() => document.getElementById('mindmap').children.length")
    print(f"[SVG CHILDREN] {child_count}")

    # 检查 window.markmap 是否加载
    has_markmap = page.evaluate("() => typeof window.markmap !== 'undefined'")
    print(f"[HAS MARKMAP] {has_markmap}")

    browser.close()