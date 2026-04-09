# -*- coding: utf-8 -*-
"""
URL Discovery for specific hotel - use Baidu search to find real OTA URLs
Then test data extraction on those URLs
"""
import asyncio, json, re, sys
from playwright.async_api import async_playwright

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

SEARCH_TERM = "锦江嘉州宾馆 携程"

async def search_baidu_hotel(browser, search_term):
    """Search Baidu and extract hotel OTA links"""
    context = None
    try:
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            locale='zh-CN',
        )
        page = await context.new_page()
        
        # Search Baidu
        search_url = f"https://www.baidu.com/s?wd={search_term}"
        print(f"  Searching: {search_term}")
        
        resp = await page.goto(search_url, wait_until='domcontentloaded', timeout=20000)
        await page.wait_for_timeout(3000)
        
        # Extract all hotel-related links from search results
        hotel_links = {}
        
        # Look for hotel links
        try:
            # Get all result links
            results = await page.query_selector_all('h3 a, .c-title a, a[class*="title"]')
            for r in results:
                href = await r.get_attribute('href')
                text = await r.inner_text()
                if href and ('hotel' in href or 'ctrip' in href or 'qunar' in href or 
                             'fliggy' in href or 'meituan' in href or 'booking' in href):
                    if len(href) > 20 and href.startswith('http'):
                        platform = 'unknown'
                        if 'ctrip.com' in href: platform = 'ctrip'
                        elif 'qunar.com' in href: platform = 'qunar'
                        elif 'fliggy.com' in href: platform = 'fliggy'
                        elif 'meituan.com' in href: platform = 'meituan'
                        elif 'booking.com' in href: platform = 'booking'
                        elif 'hotels.com' in href: platform = 'hotels'
                        hotel_links[platform] = href
                        print(f"  Found [{platform}]: {href[:80]}")
        except Exception as e:
            print(f"  Link extraction error: {e}")
        
        # Also try to extract from Baidu rich results (hotel card)
        try:
            # Look for hotel score, price in search results
            cards = await page.query_selector_all('[class*="hotel"], [class*="price"], [class*="score"]')
            for card in cards[:5]:
                txt = await card.inner_text()
                if re.search(r'\d', txt):
                    print(f"  Card text: {txt[:80]}")
        except:
            pass
        
        return {
            'search_term': search_term,
            'status': resp.status if resp else 0,
            'hotel_links': hotel_links,
            'ok': len(hotel_links) > 0
        }
        
    except Exception as e:
        print(f"  Search failed: {e}")
        return {'search_term': search_term, 'error': str(e), 'ok': False}
    finally:
        if context:
            await context.close()

async def test_hotel_page(browser, platform, url):
    """Test data extraction from a hotel page"""
    context = None
    try:
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            locale='zh-CN',
        )
        page = await context.new_page()
        
        print(f"  Testing: {platform} -> {url[:70]}")
        resp = await page.goto(url, wait_until='domcontentloaded', timeout=25000)
        await page.wait_for_timeout(4000)
        
        status = resp.status if resp else 0
        title = await page.title()
        
        # Get page text
        try:
            body = page.locator('body')
            page_text = await body.inner_text(timeout=5000)
        except:
            page_text = ''
        
        is_bot = any(k in page_text[:200] for k in ['验证', 'Captcha', 'captcha', '人机验证', '访问受限', '系统检测'])
        
        # Extract data
        price = ''
        score = ''
        name = ''
        
        # Price patterns
        price_matches = re.findall(r'[¥￥]?\s*(\d{3,5})\s*(?:元|起)?', page_text)
        for p in price_matches:
            if 80 < int(p) < 10000:
                price = p
                break
        
        # Score patterns  
        score_matches = re.findall(r'(\d\.\d)\s*(?:分|分满意)', page_text)
        for s in score_matches:
            if 3 < float(s) < 5.5:
                score = s
                break
        
        # Name from title or heading
        name_match = re.search(r'([^/\n]{2,30})(?:酒店|宾馆|民宿|客栈)', page_text)
        if name_match:
            name = name_match.group(0)[:30]
        
        result = {
            'platform': platform,
            'url': url,
            'status': status,
            'title': title[:80],
            'bot_blocked': is_bot,
            'price': price,
            'score': score,
            'name': name,
            'ok': status == 200 and not is_bot and (price or score)
        }
        
        flag = '[PASS]' if result['ok'] else '[BLOCK]' if is_bot else '[ERROR]'
        print(f"    {flag} status={status} title={title[:50]}")
        if price: print(f"         price=¥{price} score={score} name={name}")
        
        return result
        
    except Exception as e:
        print(f"    [FAIL] {e}")
        return {'platform': platform, 'url': url, 'error': str(e), 'ok': False}
    finally:
        if context:
            await context.close()

async def main():
    print('=' * 60)
    print('Hotel URL Discovery - Step 1: Baidu Search')
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
        
        # Step 1: Find real URLs via Baidu
        search_result = await search_baidu_hotel(browser, SEARCH_TERM)
        
        print('\n' + '=' * 60)
        print('Step 2: Test extracted URLs')
        print('=' * 60)
        
        page_results = []
        for platform, url in search_result.get('hotel_links', {}).items():
            r = await test_hotel_page(browser, platform, url)
            page_results.append(r)
            await asyncio.sleep(2)
        
        await browser.close()
    
    # Summary
    print('\n' + '=' * 60)
    print('FINAL SUMMARY:')
    working = [r for r in page_results if r.get('ok')]
    print(f'  Data extraction: {len(working)}/{len(page_results)} pages OK')
    for r in working:
        print(f'    [OK] {r["platform"]}: ¥{r.get("price","?")} score={r.get("score","?")} name={r.get("name","")[:30]}')
    
    blocked = [r for r in page_results if r.get('bot_blocked')]
    if blocked:
        print(f'\n  Blocked by anti-bot: {len(blocked)}')
        for r in blocked:
            print(f'    [BLOCK] {r["platform"]}: {r.get("title","")[:50]}')
    
    all_results = {
        'search': search_result,
        'pages': page_results
    }
    with open('hotel_url_discovery.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print('\nResults saved to hotel_url_discovery.json')
    return all_results

if __name__ == '__main__':
    asyncio.run(main())
