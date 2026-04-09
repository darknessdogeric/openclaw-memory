# -*- coding: utf-8 -*-
"""
OTA Scraper - Playwright Stealth Test
Uses local machine's real IP (no proxy)
"""
import asyncio, json, re, sys
from playwright.async_api import async_playwright

# Set UTF-8 output for stdout
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

TARGETS = [
    ("Ctrip-Leshan-hotel-search", "https://you.ctrip.com/hotel/leshan34.html"),
    ("Ctrip-JJJZ-hotel-detail", "https://you.ctrip.com/hotel/leshan34/138411.html"),
    ("Qunar-home", "https://www.qunar.com/hotel/"),
    ("Meituan-hotel", "https://hotel.meituan.com/"),
    ("Fliggy-hotel", "https://hotel.fliggy.com/"),
]

async def test_page(browser, name, url):
    context = None
    try:
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            locale='zh-CN',
            extra_http_headers={
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Accept': 'text/html,application/xhtml+xml',
            }
        )
        page = await context.new_page()
        await page.route("**/*.map", lambda r: r.abort())
        
        resp = await page.goto(url, wait_until='domcontentloaded', timeout=20000)
        await page.wait_for_timeout(3000)
        
        status = resp.status if resp else 0
        title = await page.title()
        final_url = page.url
        
        # Get page text to check for bot detection
        try:
            body_el = page.locator('body')
            page_text = await body_el.inner_text(timeout=3000)
        except:
            page_text = ''
        
        is_bot = any(k in page_text for k in ['验证', 'Captcha', 'captcha', 'bot', 'Bot', '访问受限', '系统检测', '人机验证'])
        
        # Try to extract hotel data
        hotel_name = ''
        price_val = ''
        score_val = ''
        
        # Hotel name patterns
        try:
            name_el = page.locator('[class*="title"], [class*="name"], [class*="hotel"]').first
            hotel_name = await name_el.inner_text(timeout=2000)
            hotel_name = hotel_name.strip()[:60]
        except:
            pass
        
        # Price patterns
        try:
            price_el = page.locator('[class*="price"]').first
            price_txt = await price_el.inner_text(timeout=2000)
            nums = re.findall(r'\d+', price_txt.replace(',', ''))
            if nums and 50 < int(nums[0]) < 10000:
                price_val = nums[0]
        except:
            pass
        
        # Score patterns  
        try:
            score_el = page.locator('[class*="score"], [class*="rating"]').first
            score_txt = await score_el.inner_text(timeout=2000)
            m = re.search(r'(\d+\.?\d*)', score_txt)
            if m and 3 < float(m.group(1)) < 5.5:
                score_val = m.group(1)
        except:
            pass
        
        result = {
            'name': name,
            'url': url,
            'status': status,
            'title': title[:80],
            'final_url': final_url[:80],
            'bot_blocked': is_bot,
            'hotel_name': hotel_name,
            'price': price_val,
            'score': score_val,
            'ok': not is_bot and status == 200
        }
        
        status_str = '[OK]' if result['ok'] else '[BLOCKED]' if is_bot else '[ERROR]'
        print(f"  {status_str} {name} | status={status} | title={title[:50]}")
        if price_val:
            print(f"         price={price_val} score={score_val}")
        
        return result
        
    except Exception as e:
        print(f"  [FAIL] {name}: {str(e)[:60]}")
        return {'name': name, 'url': url, 'error': str(e), 'ok': False}
    finally:
        if context:
            await context.close()

async def main():
    print('=' * 60)
    print('OTA Scraper - Playwright Stealth Test (Local IP)')
    print('=' * 60)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-setuid-sandbox', 
                '--disable-dev-shm-usage',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu',
                '--window-size=1920,1080',
            ]
        )
        
        results = []
        for name, url in TARGETS:
            r = await test_page(browser, name, url)
            results.append(r)
            await asyncio.sleep(2)
        
        await browser.close()
    
    # Summary
    print('=' * 60)
    print('SUMMARY:')
    passed = [r for r in results if r.get('ok')]
    blocked = [r for r in results if r.get('bot_blocked')]
    failed = [r for r in results if not r.get('ok') and not r.get('bot_blocked')]
    
    print(f'  PASSED: {len(passed)}/{len(results)}')
    for r in passed:
        print(f'    [PASS] {r["name"]}')
    print(f'  BLOCKED: {len(blocked)}/{len(results)}')
    for r in blocked:
        print(f'    [BLOCK] {r["name"]} - {r.get("title","")[:40]}')
    print(f'  FAILED: {len(failed)}/{len(results)}')
    for r in failed:
        print(f'    [FAIL] {r["name"]} - {str(r.get("error",""))[:40]}')
    print('=' * 60)
    
    # Save results
    with open('test_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f'Results saved to test_results.json')
    
    return results

if __name__ == '__main__':
    asyncio.run(main())
