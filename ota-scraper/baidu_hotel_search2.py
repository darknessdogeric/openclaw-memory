# -*- coding: utf-8 -*-
"""
Search Baidu specifically for 锦江嘉州宾馆 hotel page on Ctrip
"""
import asyncio, re, sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled',
                  '--no-sandbox', '--disable-setuid-sandbox',
                  '--disable-dev-shm-usage', '--no-first-run',
                  '--no-zygote', '--disable-gpu']
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 3000},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            locale='zh-CN',
        )
        
        page = await context.new_page()
        
        # Search Baidu for 嘉州宾馆 携程
        queries = [
            "嘉州宾馆 携程 酒店",
            "乐山锦江之星 携程", 
            "四川嘉州宾馆 携程",
        ]
        
        for query in queries:
            encoded = query.replace(' ', '+')
            search_url = f"https://www.baidu.com/s?wd={encoded}"
            print("\n" + "="*60)
            print("Searching: " + query)
            print("="*60)
            
            try:
                resp = await page.goto(search_url, wait_until='domcontentloaded', timeout=25000)
                await page.wait_for_timeout(3000)
                
                print("Status: %s" % resp.status)
                print("Title: " + await page.title())
                
                # Extract ALL mu attributes from result divs
                all_divs = await page.query_selector_all('div[id]')
                
                for div in all_divs:
                    mu = await div.get_attribute('mu')
                    if mu and ('ctrip' in mu or 'hotels.ctrip' in mu):
                        print("  CTA: " + mu[:100])
                        
                        # Also get the title of this result
                        try:
                            title_el = await div.query_selector('h3.t, .c-title, [class*="title"]')
                            if title_el:
                                title_text = await title_el.inner_text()
                                print("    Title: " + title_text[:60])
                        except:
                            pass
                
                await page.wait_for_timeout(1000)
            except Exception as e:
                print("Error: " + str(e)[:60])
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
