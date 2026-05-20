# -*- coding: utf-8 -*-
"""美团酒店 - 终极三路并进"""
import json, re, time, pickle, os

# ═══════════════════════════════════════════
# 路1: undetected-chromedriver 攻 PC 站
# ═══════════════════════════════════════════
print("=" * 60)
print("路1: undetected-chromedriver 攻 PC 站")
print("=" * 60)

try:
    import undetected_chromedriver as uc
    
    options = uc.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--lang=zh-CN')
    
    driver = uc.Chrome(options=options, version_main=None, headless=True)
    
    urls = [
        "https://hotel.meituan.com/xiangyang/",
        "https://hotel.meituan.com/",
        "https://www.meituan.com/",
    ]
    
    for url in urls:
        try:
            t0 = time.time()
            driver.get(url)
            time.sleep(3)
            elapsed = time.time() - t0
            
            title = driver.title
            html = driver.page_source
            status = "OK"
            if "403" in title or "Forbidden" in html[:500]:
                status = "403"
            
            print(f"  [{status}] {url:50s} | {len(html):>8,} chars | {elapsed:.1f}s | {title[:60]}")
            
            if status == "OK" and "酒店" in title:
                # 检查是否有酒店数据
                for kw in ['hotel','poi','price','room','deal']:
                    cnt = html.count(kw)
                    if cnt > 10:
                        print(f"    '{kw}': {cnt} occurrences")
                
                # 保存有效页面
                with open(f"cache/ota_monitor/meituan_uc_{urls.index(url)}.html", "w", encoding="utf-8") as f:
                    f.write(html)
                
                # 保存 cookies
                cookies = driver.get_cookies()
                with open("cache/ota_monitor/meituan_cookies.json", "w") as f:
                    json.dump(cookies, f, ensure_ascii=False, indent=2)
                print(f"    Cookies: {len(cookies)} 已保存")
                    
        except Exception as e:
            print(f"  ❌ {url:50s} | {type(e).__name__}: {str(e)[:80]}")
    
    driver.quit()
    
except Exception as e:
    print(f"  ❌ undetected-chromedriver 失败: {e}")

# ═══════════════════════════════════════════
# 路2: Cookie 偷渡 - Playwright 取 Cookie → 带 Cookie 调 API
# ═══════════════════════════════════════════
print(f"\n{'='*60}")
print("路2: Cookie 偷渡 (PW取Cookie → 调API)")
print("=" * 60)

try:
    from playwright.sync_api import sync_playwright
    from curl_cffi import requests as curl_requests
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--disable-blink-features=AutomationControlled','--no-sandbox'])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
            viewport={"width": 390, "height": 844},
            locale="zh-CN",
        )
        page = context.new_page()
        
        # 步骤1: 加载首页，获取 cookies
        print("  加载首页...")
        page.goto("https://i.meituan.com/hotel/xiangyang/", wait_until="networkidle", timeout=20000)
        page.wait_for_timeout(3000)
        
        # 提取 cookies
        pw_cookies = context.cookies()
        print(f"  PW Cookies: {len(pw_cookies)} 个")
        
        # 转换为 curl_cffi 格式
        cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in pw_cookies])
        
        # 提取关键 header token
        headers_from_page = {}
        try:
            # 获取 localStorage/sessionStorage tokens
            token = page.evaluate("() => localStorage.getItem('token') || sessionStorage.getItem('token') || ''")
            if token:
                headers_from_page['token'] = token
                print(f"  Token: {token[:50]}...")
        except:
            pass
        
        # 步骤2: 尝试调搜索 API (带 cookie)
        print("  测试搜索API...")
        api_headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
            "Cookie": cookie_str,
            "Referer": "https://i.meituan.com/hotel/xiangyang/",
        }
        api_headers.update(headers_from_page)
        
        api_urls = [
            "https://ihotel.meituan.com/hbsearch/HotelSearch?cityId=774&startDate=2026-05-13&endDate=2026-05-14&utm_medium=touch&version=480",
            "https://ihotel.meituan.com/group/v1/poi/nearby?cityId=774&limit=20&utm_medium=touch",
            "https://ihotel.meituan.com/group/v1/poi/recommend?cityId=774&limit=20&utm_medium=touch",
        ]
        
        for url in api_urls:
            try:
                resp = curl_requests.get(url, impersonate="chrome120", headers=api_headers, timeout=10)
                print(f"  [{resp.status_code}] {url.split('?')[0].rsplit('/',1)[-1]:30s} | {len(resp.text):>6,} chars")
                if resp.status_code == 200 and len(resp.text) > 200:
                    try:
                        data = resp.json()
                        data_str = json.dumps(data, ensure_ascii=False)
                        print(f"    {data_str[:300]}")
                    except:
                        print(f"    {resp.text[:200]}")
            except Exception as e:
                print(f"  [ERR] {url.split('?')[0].rsplit('/',1)[-1]:30s} | {type(e).__name__}")
        
        browser.close()

except Exception as e:
    print(f"  ❌ Cookie偷渡失败: {e}")


# ═══════════════════════════════════════════
# 路3: 单酒店详情页 (可能不需要登录)
# ═══════════════════════════════════════════
print(f"\n{'='*60}")
print("路3: 单酒店详情页直连")
print("=" * 60)

try:
    from curl_cffi import requests as curl_requests
    
    # 尝试美团酒店详情页URL模式
    detail_urls = [
        # 襄阳共享国际大酒店 (从Tavily搜索结果找到)
        "https://hotel.meituan.com/xiangyang/gongxiangguojidajiudian/",
        "https://i.meituan.com/hotel/detail/481488",  # 假设 poiId
        # 常见的酒店详情URL模式
        "https://hotel.meituan.com/481488/",
        "https://i.meituan.com/awp/h5/hotel/detail/detail.html?poiId=481488",
        # 携程上常见的襄阳酒店 - 试美团
        "https://hotel.meituan.com/xiangyang/",
        # 直接搜美团上"襄阳共享国际大酒店"
        "https://i.meituan.com/awp/h5/hotel/detail/detail.html?poiid=481488",
    ]
    
    for url in detail_urls:
        try:
            resp = curl_requests.get(url, impersonate="chrome120", 
                                     headers={"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15"},
                                     timeout=10)
            status = resp.status_code
            length = len(resp.text)
            title = ""
            if "<title" in resp.text:
                m = re.search(r'<title[^>]*>(.*?)</title>', resp.text, re.DOTALL)
                if m: title = m.group(1).strip()[:80]
            
            icon = "✅" if status == 200 and length > 5000 else ("⚠️" if status == 200 else "❌")
            print(f"  {icon} [{status}] {url[:70]} | {length:>6,} chars | {title[:60]}")
            
            if status == 200 and length > 5000:
                # 检查数据量
                for kw in ['price','Price','hotel','Hotel','room','Room']:
                    cnt = resp.text.count(kw)
                    if cnt > 0:
                        print(f"    '{kw}': {cnt}")
                        
        except Exception as e:
            print(f"  ❌ {url[:70]} | {type(e).__name__}: {str(e)[:60]}")
        time.sleep(0.3)

except Exception as e:
    print(f"  ❌ 详情页测试失败: {e}")

print(f"\n{'='*60}")
print("测试完成")
print("=" * 60)
