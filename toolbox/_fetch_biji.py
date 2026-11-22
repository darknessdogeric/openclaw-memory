#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""抓 biji.com 页面 — 用 base64 绕开编码问题"""
import sys, io, base64, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from playwright.sync_api import sync_playwright
from pathlib import Path

URL = "https://www.biji.com/note/share_note/5JwRyLwpNQ9Ry"
OUT = Path(r"C:\Users\ericz\AppData\Local\Temp\biji_clean.txt")
OUT_HTML = Path(r"C:\Users\ericz\AppData\Local\Temp\biji_page.html")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    ctx = browser.new_context(
        viewport={"width": 1280, "height": 1024},
        device_scale_factor=1,
        locale="zh-CN",
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    )
    page = ctx.new_page()
    page.goto(URL, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(4000)
    # 用 base64 编码页面文本 + HTML
    payload = page.evaluate("""
        () => {
            const text = document.body.innerText;
            const html = document.documentElement.outerHTML;
            return { text_b64: btoa(unescape(encodeURIComponent(text))),
                     html_b64: btoa(unescape(encodeURIComponent(html))),
                     len: text.length,
                     html_len: html.length };
        }
    """)
    text = base64.b64decode(payload["text_b64"]).decode("utf-8")
    html = base64.b64decode(payload["html_b64"]).decode("utf-8")
    OUT.write_text(text, encoding="utf-8")
    OUT_HTML.write_text(html, encoding="utf-8")
    print(f"[OK] text={payload['len']:,} chars, html={payload['html_len']:,} chars")
    print(f"[saved] {OUT}")
    print("---FIRST 800 CHARS---")
    print(text[:800])
    browser.close()