# -*- coding: utf-8 -*-
"""携程酒店列表 通路探测"""
import sys, asyncio, json, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

TARGETS = [
  ("成都", "https://hotels.ctrip.com/hotels/list?city=28"),
  ("成都(移动)", "https://m.ctrip.com/webapp/hotel/chengdu/"),
]

async def probe():
    async with async_playwright() as p:
        br = await p.chromium.launch(headless=True, args=[
            "--disable-blink-features=AutomationControlled",
            "--no-sandbox", "--disable-dev-shm-usage"])
        ctx = await br.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
            viewport={"width":1440,"height":900}, locale="zh-CN")
        await ctx.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined})")
        for name, url in TARGETS:
            page = await ctx.new_page()
            try:
                r = await page.goto(url, timeout=45000, wait_until="domcontentloaded")
                await page.wait_for_timeout(6000)
                title = await page.title()
                html = await page.content()
                txt = await page.inner_text("body")
                # 提取疑似酒店名+价格
                prices = re.findall(r"[¥￥]\s?(\d{2,5})", txt)
                print(f"--- {name} ---")
                print("URL:", page.url)
                print("STATUS:", r.status if r else "?")
                print("TITLE:", title[:80])
                print("HTML_LEN:", len(html), "TEXT_LEN:", len(txt))
                print("PRICES_FOUND:", len(prices), prices[:15])
                print("TEXT_HEAD:", txt[:300].replace("\n"," / "))
            except Exception as e:
                print(f"--- {name} FAILED: {type(e).__name__}: {str(e)[:200]}")
            finally:
                await page.close()
        await br.close()

asyncio.run(probe())
