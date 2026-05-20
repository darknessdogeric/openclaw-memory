# -*- coding: utf-8 -*-
"""美团酒店反爬攻克 - 多方案并行测试"""
import sys, time, json

print("=" * 60)
print("美团酒店反爬攻克 - 三方案并行测试")
print("=" * 60)

# ═══════════════════════════════════════
# 方案1: curl_cffi (TLS指纹模拟Chrome)
# ═══════════════════════════════════════
print("\n[方案1] curl_cffi TLS指纹模拟...")
try:
    from curl_cffi import requests as curl_requests
    
    # 测试酒店列表页
    urls = [
        "https://hotel.meituan.com/xiangyang/",
        "https://hotel.meituan.com/search",
        "https://i.meituan.com/hotel/xiangyang/",  # 移动端可能更松
    ]
    
    for url in urls:
        try:
            t0 = time.time()
            resp = curl_requests.get(
                url,
                impersonate="chrome120",
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                    "Referer": "https://www.meituan.com/",
                },
                timeout=15,
            )
            elapsed = time.time() - t0
            status = resp.status_code
            length = len(resp.text)
            title = ""
            if "<title" in resp.text:
                import re
                m = re.search(r'<title[^>]*>(.*?)</title>', resp.text, re.DOTALL)
                if m:
                    title = m.group(1).strip()[:80]
            
            print(f"  ✅ {url} | status={status} | {length:,} chars | {elapsed:.1f}s")
            if title:
                print(f"     Title: {title}")
            if "酒店" in resp.text or "hotel" in resp.text.lower():
                print(f"     含酒店内容: YES")
            
            # 成功的话保存样本
            if status == 200 and length > 1000:
                with open("cache/ota_monitor/meituan_sample_curl.html", "w", encoding="utf-8") as f:
                    f.write(resp.text)
                print(f"     → 样本已保存")
                break
                
        except Exception as e:
            print(f"  ❌ {url} | {type(e).__name__}: {str(e)[:100]}")
    
except ImportError as e:
    print(f"  ❌ curl_cffi 不可用: {e}")

# ═══════════════════════════════════════
# 方案2: Playwright + stealth (增强版)
# ═══════════════════════════════════════
print("\n[方案2] Playwright + stealth 增强版...")
try:
    from playwright.sync_api import sync_playwright
    
    with sync_playwright() as p:
        # 使用非无头模式的关键参数
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--no-sandbox',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
                '--disable-site-isolation-trials',
                '--disable-infobars',
                '--window-size=1920,1080',
            ]
        )
        
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="zh-CN",
            timezone_id="Asia/Shanghai",
        )
        
        page = context.new_page()
        
        # 注入 stealth 脚本
        page.add_init_script("""
            // 覆盖 navigator.webdriver
            Object.defineProperty(navigator, 'webdriver', { get: () => false });
            // 覆盖 chrome 对象
            window.chrome = { runtime: {} };
            // 覆盖权限
            const originalQuery = window.navigator.permissions.query;
            window.navigator.permissions.query = (parameters) => (
                parameters.name === 'notifications' ?
                Promise.resolve({ state: Notification.permission }) :
                originalQuery(parameters)
            );
            // 覆盖插件
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5],
            });
        """)
        
        urls = [
            "https://hotel.meituan.com/xiangyang/",
            "https://i.meituan.com/hotel/xiangyang/",
        ]
        
        for url in urls:
            try:
                t0 = time.time()
                resp = page.goto(url, wait_until="domcontentloaded", timeout=20000)
                page.wait_for_timeout(3000)
                
                status = resp.status if resp else "N/A"
                title = page.title()[:80]
                content_len = len(page.content())
                
                elapsed = time.time() - t0
                print(f"  ✅ {url} | status={status} | {content_len:,} chars | {elapsed:.1f}s")
                print(f"     Title: {title}")
                
                if "酒店" in page.content() or "hotel" in page.content().lower():
                    print(f"     含酒店内容: YES")
                    with open("cache/ota_monitor/meituan_sample_pw.html", "w", encoding="utf-8") as f:
                        f.write(page.content())
                    print(f"     → 样本已保存")
                    break
                    
            except Exception as e:
                print(f"  ❌ {url} | {type(e).__name__}: {str(e)[:100]}")
        
        browser.close()

except ImportError as e:
    print(f"  ❌ Playwright 不可用: {e}")

# ═══════════════════════════════════════
# 方案3: 美团移动端 API (最轻量)
# ═══════════════════════════════════════
print("\n[方案3] 美团移动端API直连...")
try:
    from curl_cffi import requests as curl_requests
    
    # 美团酒店搜索API (移动端)
    api_urls = [
        "https://ihotel.meituan.com/hbsearch/HotelSearch",
        "https://hotel.meituan.com/api/v2/search",
        "https://www.meituan.com/meishi/api/hotel/search",
    ]
    
    for url in api_urls:
        try:
            t0 = time.time()
            resp = curl_requests.post(
                url,
                impersonate="chrome120",
                json={
                    "cityId": 411,  # 襄阳
                    "cityName": "襄阳",
                    "startDate": "2026-05-13",
                    "endDate": "2026-05-14",
                    "page": 1,
                    "pageSize": 20,
                },
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                    "Referer": "https://hotel.meituan.com/",
                    "Origin": "https://hotel.meituan.com",
                    "Content-Type": "application/json",
                },
                timeout=10,
            )
            elapsed = time.time() - t0
            print(f"  {url} | status={resp.status_code} | {len(resp.text):,} chars | {elapsed:.1f}s")
            if resp.status_code == 200 and len(resp.text) > 50:
                sample = resp.text[:300]
                print(f"     Sample: {sample}")
                break
        except Exception as e:
            print(f"  ❌ {url} | {type(e).__name__}: {str(e)[:80]}")

except ImportError as e:
    print(f"  ❌ curl_cffi 不可用: {e}")

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)
