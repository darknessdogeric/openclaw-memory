# -*- coding: utf-8 -*-
"""
Step 1: Find correct hotel URLs on each OTA platform
Step 2: Test data extraction on working URLs
"""
import asyncio, json, re, sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Known hotel - 锦江嘉州宾馆 (from previous research)
# Try multiple URL patterns to find the right one
TEST_URLS = [
    # Ctrip - try different URL patterns
    ("Ctrip-pattern1", "https://you.ctrip.com/hotel/leshan38.html"),
    ("Ctrip-pattern2", "https://hotels.ctrip.com/hotel/leshan38.html"),
    ("Ctrip-pattern3", "https://you.ctrip.com/hotel/china/leshan/leshan38.html"),
    # Qunar 
    ("Qunar-pattern1", "https://www.qunar.com/hotel/leshan/"),
    ("Qunar-pattern2", "https://hotel.qunar.com/city/leshan/"),
    # Fliggy
    ("Fliggy-pattern1", "https://hotel.fliggy.com/hotel/list.htm?city=leshan"),
    ("Fliggy-pattern2", "https://www.fliggy.com/hotel/leshan/"),
    # Meituan  
    ("Meituan-pattern1", "https://hotel.meituan.com/leshan/"),
    ("Meituan-pattern2", "https://hotel.meituan.com/api/hotel/list?cityId=2384"),
    # 百度搜索入口 - see if we can find real URLs
    ("Baidu-search", "https://www.baidu.com/s?wd=%E9%87%91%E6%B1%9F%E5%98%89%E5%B7%9E%E9%A5%AD%E9%A6%86+%E6%90%BA%E7%A8%8B"),
]

async def find_real_urls(browser, name, url):
    """Try to access page and extract any hotel URLs found"""
    context = None
    try:
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            locale='zh-CN',
        )
        page = await context.new_page()
        
        resp = await page.goto(url, wait_until='domcontentloaded', timeout=20000)
        await page.wait_for_timeout(3000)
        
        status = resp.status if resp else 0
        title = await page.title()
        final_url = page.url
        
        # Extract any hotel URLs from the page
        hotel_urls = []
        try:
            links = await page.query_selector_all('a[href*="hotel"], a[href*="ctrip"], a[href*="qunar"], a[href*="fliggy"]')
            seen = set()
            for link in links[:20]:
                href = await link.get_attribute('href')
                if href and href not in seen and len(href) > 20:
                    seen.add(href)
                    hotel_urls.append(href)
        except:
            pass
        
        # Get visible text
        try:
            body_text = await page.locator('body').inner_text(timeout=3000)
            body_text = body_text[:500]
        except:
            body_text = ''
        
        is_bot = any(k in body_text for k in ['验证', 'Captcha', 'captcha', '人机验证', '访问受限'])
        
        result = {
            'name': name,
            'url': url,
            'status': status,
            'title': title[:80],
            'final_url': final_url,
            'bot_blocked': is_bot,
            'hotel_urls_found': hotel_urls[:5],
            'body_preview': body_text[:200],
            'ok': status == 200 and not is_bot
        }
        
        flag = '[PASS]' if result['ok'] else '[BLOCK]' if is_bot else '[ERROR]'
        print(f'  {flag} {name} | status={status} | {title[:50]}')
        if hotel_urls:
            print(f'       Found {len(hotel_urls)} hotel links, e.g.: {hotel_urls[0][:60]}')
        
        return result
        
    except Exception as e:
        print(f'  [FAIL] {name}: {str(e)[:60]}')
        return {'name': name, 'url': url, 'error': str(e), 'ok': False}
    finally:
        if context:
            await context.close()

async def main():
    print('=' * 60)
    print('OTA Scraper - URL Discovery Phase')
    print('=' * 60)
    
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
        
        results = []
        for name, url in TEST_URLS:
            r = await find_real_urls(browser, name, url)
            results.append(r)
            await asyncio.sleep(1.5)
        
        await browser.close()
    
    print('=' * 60)
    working = [r for r in results if r.get('ok')]
    print(f'Working: {len(working)}/{len(results)}')
    for r in working:
        print(f'  [OK] {r["name"]}: {r["title"][:50]}')
        if r.get('hotel_urls_found'):
            print(f'       Hotel URLs: {r["hotel_urls_found"][:2]}')
    print('=' * 60)
    
    with open('url_discovery.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    return results

if __name__ == '__main__':
    asyncio.run(main())
