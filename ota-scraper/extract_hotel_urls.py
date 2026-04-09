# -*- coding: utf-8 -*-
"""
Extract real hotel URLs from Baidu search results
Use Playwright to get mu attributes from search result divs
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
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            locale='zh-CN'
        )
        
        page = await context.new_page()
        
        # Search for 乐山酒店 on Baidu
        search_url = "https://www.baidu.com/s?wd=%E4%B9%90%E5%B1%B1%E9%A5%AD%E9%A6%86+%E6%90%BA%E7%A8%8B"
        await page.goto(search_url, wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(2000)
        
        print("Page title: " + await page.title())
        
        # Extract mu attributes from result divs
        result_divs = await page.query_selector_all('div[id][mu], div.c-container[mu]')
        hotel_urls = []
        
        print("\nExtracted hotel URLs from Baidu search:")
        for div in result_divs:
            mu = await div.get_attribute('mu')
            if mu and ('hotel' in mu or 'ctrip' in mu or 'qunar' in mu or 
                       'fliggy' in mu or 'meituan' in mu or 'booking' in mu):
                print("  " + mu[:100])
                hotel_urls.append(mu)
        
        # Also look for data-click mu attributes
        all_divs = await page.query_selector_all('div[id^="20"], div[id^="3"], div[id^="4"], div[id^="5"], div[id^="6"]')
        for div in all_divs:
            mu = await div.get_attribute('mu')
            if mu and ('/hotel/' in mu or 'hotel?' in mu):
                if mu not in hotel_urls:
                    hotel_urls.append(mu)
        
        print("\nAll hotel URLs found:")
        for url in hotel_urls:
            print("  " + url)
        
        # Now test each URL with Jina Reader
        print("\n\n=== Testing Jina Reader on extracted URLs ===")
        for url in hotel_urls:
            if len(url) > 20:
                # Extract hostname for label
                label = url.split('/')[2] if len(url.split('/')) > 2 else url[:30]
                print("\nTesting: " + label[:60])
                
                # Use evaluate_script to fetch via Jina
                try:
                    result = await page.evaluate(""", async (url) => {
                        try {
                            const resp = await fetch('https://r.jina.ai/' + encodeURIComponent(url));
                            const text = await resp.text();
                            return {ok: true, length: text.length, preview: text.substring(0, 200)};
                        } catch(e) {
                            return {ok: false, error: e.message};
                        }
                    }""", url)
                    
                    if result.get('ok'):
                        print("  Jina OK: %d chars" % result['length'])
                        print("  Preview: " + result['preview'][:150].replace('\n', ' '))
                    else:
                        print("  Jina FAIL: " + str(result.get('error', ''))[:50])
                except Exception as e:
                    print("  Error: " + str(e)[:60])
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
