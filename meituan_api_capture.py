# -*- coding: utf-8 -*-
"""美团酒店数据提取 - Playwright + 网络拦截 + DOM等待"""
import json, re, time

from playwright.sync_api import sync_playwright

HOTEL_DATA = []

def log_response(response):
    """拦截网络响应，抓取酒店数据"""
    url = response.url
    if any(kw in url for kw in ['hotel', 'poi', 'search', 'list', 'recommend']):
        try:
            ct = response.headers.get('content-type', '')
            if 'json' in ct:
                body = response.json()
                body_str = json.dumps(body, ensure_ascii=False)
                HOTEL_DATA.append({
                    'url': url[:120],
                    'size': len(body_str),
                    'body_sample': body_str[:500]
                })
                print(f"  [API] {url[:100]} | {len(body_str)} chars")
        except:
            pass

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=[
            '--disable-blink-features=AutomationControlled',
            '--no-sandbox',
            '--disable-dev-shm-usage',
        ]
    )
    
    context = browser.new_context(
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        viewport={"width": 390, "height": 844},
        locale="zh-CN",
    )
    
    page = context.new_page()
    
    # 拦截网络请求
    page.on("response", log_response)
    
    # 去襄阳酒店搜索
    print("加载页面...")
    page.goto("https://i.meituan.com/hotel/xiangyang/", wait_until="networkidle", timeout=30000)
    
    # 等待额外加载
    print("等待渲染...")
    page.wait_for_timeout(5000)
    
    # 滚动触发懒加载
    for i in range(3):
        page.evaluate("window.scrollBy(0, 800)")
        page.wait_for_timeout(2000)
    
    html = page.content()
    print(f"\n最终页面: {len(html):,} chars")
    
    # 尝试提取DOM中的酒店数据
    # 美团移动端常用 class 名
    for selector in [
        '.hotel-item', '.poi-item', '.list-item', 
        '[class*="hotel"]', '[class*="Hotel"]',
        '.card-item', '.search-result-item',
        '[data-poiid]', '[data-hotelid]',
    ]:
        try:
            els = page.query_selector_all(selector)
            if els:
                print(f"  {selector}: {len(els)} elements")
                for el in els[:3]:
                    text = el.inner_text()[:100].replace('\n', ' | ')
                    print(f"    → {text}")
        except:
            pass
    
    browser.close()

print(f"\n=== 网络拦截捕获 {len(HOTEL_DATA)} 个API响应 ===")
for item in HOTEL_DATA:
    print(f"\n  URL: {item['url']}")
    print(f"  Size: {item['size']:,} chars")
    print(f"  Sample: {item['body_sample'][:300]}")
