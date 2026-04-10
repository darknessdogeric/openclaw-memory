# -*- coding: utf-8 -*-
"""
B166ER 专业图片生成器
使用方法: python make_poster.py [html_file] [output_file] [width] [height]
示例: python make_poster.py my_poster.html 我的海报.png 1080 1920
"""
import asyncio
import sys
import os

async def screenshot_full_page(html_path, output_path, width=1080, height=1920):
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        page = await browser.new_page(viewport={'width': width, 'height': height})
        await page.goto(f'file:///{os.path.abspath(html_path)}', wait_until='networkidle')
        await asyncio.sleep(1.5)  # wait for fonts to fully render
        await page.screenshot(path=output_path, full_page=True, type='png')
        await browser.close()
        size = os.path.getsize(output_path)
        print(f"OK: {output_path} ({size//1024}KB)")

if __name__ == '__main__':
    html_file = sys.argv[1] if len(sys.argv) > 1 else "test_poster.html"
    output = sys.argv[2] if len(sys.argv) > 2 else r"C:\Users\ericz\Desktop\output.png"
    w = int(sys.argv[3]) if len(sys.argv) > 3 else 1080
    h = int(sys.argv[4]) if len(sys.argv) > 4 else 1920
    asyncio.run(screenshot_full_page(html_file, output, w, h))
