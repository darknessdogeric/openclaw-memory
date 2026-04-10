# -*- coding: utf-8 -*-
import asyncio
from playwright.async_api import async_playwright

async def main():
    html_path = r"C:\Users\ericz\.openclaw\workspace\test_poster.html"
    output_path = r"C:\Users\ericz\Desktop\西部酒店生态分析报告_v2.png"

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )
        page = await browser.new_page(viewport={'width': 1080, 'height': 1920})
        await page.goto(f'file:///{html_path}', wait_until='networkidle')
        await asyncio.sleep(1)  # wait for fonts to load
        await page.screenshot(path=output_path, full_page=True, type='png')
        await browser.close()
        print(f"Saved: {output_path}")

if __name__ == '__main__':
    asyncio.run(main())
