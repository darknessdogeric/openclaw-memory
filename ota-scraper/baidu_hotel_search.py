# -*- coding: utf-8 -*-
"""
Use Playwright to search Baidu for '锦江嘉州宾馆 携程'
and extract the real Ctrip URL
"""
import asyncio, json, re, sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

async def main():
    print("Searching Baidu for 锦江嘉州宾馆 on Ctrip...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox', '--disable-setuid-sandbox',
                '--disable-dev-shm-usage', '--no-first-run',
                '--no-zygote', '--disable-gpu',
            ]
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            locale='zh-CN',
        )
        
        page = await context.new_page()
        
        # Go to Baidu
        search_url = "https://www.baidu.com/s?wd=%E9%94%80%E6%B1%9F%E5%98%89%E5%B7%9E%E9%A5%AD%E9%A6%86+%E6%90%BA%E7%A8%8B"
        print("GET: " + search_url)
        
        resp = await page.goto(search_url, wait_until='networkidle', timeout=30000)
        await page.wait_for_timeout(3000)
        
        print("Status: %s" % resp.status)
        title = await page.title()
        print("Title: %s" % title)
        
        # Extract all result URLs
        results = await page.query_selector_all('h3.t a, .c-title a')
        print("Found %d result headings" % len(results))
        
        all_links = []
        for r in results:
            href = await r.get_attribute('href')
            text = await r.inner_text()
            if href:
                all_links.append({'text': text[:60], 'href': href})
                if 'ctrip' in href or 'hotel' in href:
                    print("  HOTEL LINK: %s -> %s" % (text[:50], href[:80]))
        
        # Also check result containers for hotel info
        print("\nChecking result containers...")
        try:
            # Get all visible text from results
            body_text = await page.locator('#content_left, .result').inner_text(timeout=5000)
            
            # Find Ctrip URLs in the page
            ctrip_links = re.findall(r'https?://[^\s"\'<>]*(?:ctrip|hotels\.ctrip)[^\s"\'<>]*', body_text)
            print("\nCtrip URLs found in page: %d" % len(ctrip_links))
            for u in ctrip_links[:10]:
                print("  " + u[:100])
            
            # Find any hotel URLs
            hotel_links = re.findall(r'https?://[^\s"\'<>]*(?:/hotel/)[^\s"\'<>]*', body_text)
            print("\nHotel URLs found: %d" % len(hotel_links))
            for u in hotel_links[:10]:
                print("  " + u[:100])
                
        except Exception as e:
            print("Error getting container text: %s" % e)
        
        # Take screenshot of first screen
        await page.screenshot(path='baidu_search_screenshot.png', full_page=False)
        print("\nScreenshot saved: baidu_search_screenshot.png")
        
        # Try to click on a result that looks like Ctrip hotel
        try:
            ctrip_result = page.locator('h3.t a[href*="ctrip"], h3.t a[href*="hotels.ctrip"]').first
            if await ctrip_result.count() > 0:
                url = await ctrip_result.get_attribute('href')
                print("\nClicking Ctrip result: " + url[:80])
                await ctrip_result.click()
                await page.wait_for_timeout(5000)
                final_url = page.url
                print("Landed on: " + final_url)
                await page.screenshot(path='ctrip_page_screenshot.png')
                print("Screenshot saved: ctrip_page_screenshot.png")
        except Exception as e:
            print("Could not click Ctrip result: %s" % e)
        
        await browser.close()
    
    return all_links

if __name__ == '__main__':
    asyncio.run(main())
