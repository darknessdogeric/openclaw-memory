# -*- coding: utf-8 -*-
"""
Use Playwright to search directly on Ctrip
Find the actual hotel page for 锦江嘉州宾馆
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
            locale='zh-CN',
        )
        
        page = await context.new_page()
        
        # Try Ctrip hotel search for 嘉州
        search_url = "https://hotels.ctrip.com/hotel/search?city=%E5%98%89%E5%B7%9E&checkIn=2026-04-15&checkOut=2026-04-16&rooms=1"
        print("Searching Ctrip for: 嘉州")
        print("URL: " + search_url)
        
        resp = await page.goto(search_url, wait_until='domcontentloaded', timeout=25000)
        await page.wait_for_timeout(5000)
        
        print("Status: %s" % resp.status)
        print("Title: " + await page.title())
        print("URL: " + page.url)
        
        # Check for bot detection
        body_text = await page.locator('body').inner_text()
        if any(k in body_text[:200] for k in ['验证', 'Captcha', '人机', '访问受限']):
            print("[BLOCKED] Bot detection triggered")
        
        # Extract hotel links from the page
        # Look for hotel name links  
        all_links = await page.query_selector_all('a[href*="/hotel/"]')
        hotel_pages = []
        seen = set()
        
        for link in all_links:
            href = await link.get_attribute('href')
            text = await link.inner_text()
            if href and '/hotel/' in href and len(text) > 3 and text not in seen:
                if not any(k in text for k in ['登录', '注册', '下载', 'APP', '.cn', '.com']):
                    seen.add(text)
                    hotel_pages.append({'text': text[:40], 'href': href})
                    if len(hotel_pages) <= 20:
                        print("  Hotel link: %s -> %s" % (text[:30], href[:80]))
        
        print("\nTotal hotel links found: %d" % len(hotel_pages))
        
        # Look for 锦江 or 嘉州 in the page text
        if '锦江' in body_text or '嘉州' in body_text:
            print("\n[FOUND] 锦江 or 嘉州 found in page!")
            # Find the snippet
            for kw in ['锦江', '嘉州']:
                if kw in body_text:
                    idx = body_text.find(kw)
                    print("  Context: ..." + body_text[max(0,idx-50):idx+100] + "...")
        
        # Try to extract data for hotels we found
        print("\n\n=== Trying to extract data from first 3 hotels ===")
        for hp in hotel_pages[:3]:
            href = hp['href']
            if href.startswith('/'):
                full_url = 'https://hotels.ctrip.com' + href
            else:
                full_url = href
            
            if 'pic-pid' not in full_url and 'detail' not in full_url:
                continue
                
            print("\nTesting: " + hp['text'][:40])
            print("  URL: " + full_url[:80])
            
            try:
                page2 = await context.new_page()
                resp2 = await page2.goto(full_url, wait_until='domcontentloaded', timeout=20000)
                await page2.wait_for_timeout(3000)
                
                body2 = await page2.locator('body').inner_text()
                is_blocked = any(k in body2[:200] for k in ['验证', 'Captcha', '人机', '访问受限'])
                
                if is_blocked:
                    print("  [BLOCKED]")
                else:
                    print("  [OK] Status: %s" % resp2.status)
                    # Extract prices
                    prices = re.findall(r'¥\s*(\d+)', body2)
                    valid_prices = [p for p in prices if 80 < int(p) < 2000]
                    if valid_prices:
                        print("  Prices: " + ", ".join(valid_prices[:5]))
                    print("  Title: " + (await page2.title())[:60])
                
                await page2.close()
            except Exception as e:
                print("  Error: " + str(e)[:50])
        
        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
