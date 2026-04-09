"""
OTA Scraper - Playwright Stealth Test (Local IP)
Uses local machine IP - no proxy needed for initial testing
"""
import asyncio, json, re, sys
from playwright.async_api import async_playwright

# Hotel targets - try multiple platforms
TARGETS = [
    ("携程-锦江嘉州宾馆", "https://you.ctrip.com/hotel/leshan34/138411.html"),
    ("携程-乐山酒店搜索", "https://you.ctrip.com/hotel/leshan34.html"),
    ("去哪儿-首页", "https://www.qunar.com/hotel/"),
    ("美团-酒店", "https://hotel.meituan.com/"),
    ("飞猪-酒店", "https://hotel.fliggy.com/"),
]

async def test_page(browser, name, url):
    """Test a single page with stealth browser"""
    context = None
    try:
        # Launch stealth context
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            locale='zh-CN',
            extra_http_headers={
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            }
        )
        
        page = await context.new_page()
        
        print(f"  -> GET {name}".encode('utf-8', errors='replace').decode('utf-8'))
        resp = await page.goto(url, wait_until='domcontentloaded', timeout=15000)
        await page.wait_for_timeout(2000)
        
        title = await page.title()
        url_final = page.url
        
        # Check for anti-bot
        try:
            body = await page.query_selector('body')
            page_text = await body.inner_text() if body else ''
        except:
            page_text = ''
        is_bot_page = any(k in page_text for k in ['验证', 'Captcha', 'bot', 'Bot', '访问受限', '系统检测'])
        
        status_ok = '[OK]' if not is_bot_page else '[BOT]'
        print(f"     Status: {resp.status if resp else 'N/A'} {status_ok}")
        print(f"     Title: {title[:80]}")
        
        # Extract prices
        try:
            prices = await page.query_selector_all('[class*="price"], [class*="Price"], [class*="money"]')
            price_vals = []
            for p in prices[:5]:
                txt = await p.inner_text()
                nums = re.findall(r'\d+', txt.replace(',', ''))
                if nums and 50 < int(nums[0]) < 10000:
                    price_vals.append(f"Y{nums[0]}")
            if price_vals:
                print(f"     Prices: {', '.join(price_vals[:3])}")
        except:
            pass
        
        # Extract scores  
        try:
            scores = await page.query_selector_all('[class*="score"], [class*="rating"], .score')
            score_vals = []
            for s in scores[:3]:
                txt = await s.inner_text()
                if re.search(r'\d', txt):
                    score_vals.append(txt.strip()[:10])
            if score_vals:
                print(f"     Scores: {', '.join(score_vals[:3])}")
        except:
            pass
        
        return {
            'name': name,
            'status': resp.status if resp else 0,
            'title': title,
            'bot_blocked': is_bot_page,
            'prices': price_vals[:3],
            'scores': score_vals[:3],
            'ok': not is_bot_page and (resp.status if resp else 0) < 400
        }
    except Exception as e:
        print(f"  -> ERROR: {e}")
        return {'name': name, 'error': str(e), 'ok': False}
    finally:
        if context:
            await context.close()

async def run_stealth_tests():
    """Run stealth browser tests on all targets"""
    print("=" * 60)
    print("OTA Scraper - Playwright Stealth Test (Local IP)")
    print("=" * 60)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-accelerated-2d-canvas',
                '--no-first-run',
                '--no-zygote',
                '--disable-gpu',
                '--window-size=1920,1080',
                '--disable-web-security',
            ]
        )
        
        results = []
        for name, url in TARGETS:
            r = await test_page(browser, name, url)
            results.append(r)
            await asyncio.sleep(1)  # polite delay
        
        await browser.close()
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY:")
    for r in results:
        if 'error' in r:
            print(f"  ❌ {r['name']}: ERROR - {r['error'][:50]}")
        elif r.get('ok'):
            print(f"  ✅ {r['name']}: OK (status={r.get('status')})")
        else:
            print(f"  🔴 {r['name']}: BLOCKED (bot={r.get('bot_blocked')})")
    print("=" * 60)
    
    return results

if __name__ == '__main__':
    results = asyncio.run(run_stealth_tests())
    # Save results
    with open('playwright_test_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\nResults saved to playwright_test_results.json")
