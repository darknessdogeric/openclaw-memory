# -*- coding: utf-8 -*-
import asyncio
from playwright.async_api import async_playwright

async def screenshot_poster():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={'width': 1080, 'height': 1920})
        await page.goto('file:///C:/Users/ericz/.openclaw/workspace/AHL_poster.html')
        await page.wait_for_timeout(1000)
        await page.screenshot(path='C:/Users/ericz/.openclaw/workspace/AHL_poster.png', full_page=True)
        await browser.close()
        print('Screenshot saved to AHL_poster.png')

asyncio.run(screenshot_poster())
