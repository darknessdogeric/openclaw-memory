# -*- coding: utf-8 -*-
"""美团 - Playwright 拦截登录重定向 + 直接导航 backurl"""
import json, re, time
from urllib.parse import unquote, parse_qs, urlparse
from playwright.sync_api import sync_playwright

API_RESPONSES = []
REDIRECT_URLS = []

def on_response(response):
    url = response.url
    ct = response.headers.get('content-type','')
    if 'json' in ct:
        for kw in ['search','poi','hotel','list','recommend','deal','hbsearch','nearby']:
            if kw in url:
                try:
                    body = response.json()
                    API_RESPONSES.append({'url': url[:150], 'body': body})
                except:
                    pass
                break

def on_request(request):
    # 记录重定向URL
    if 'passport' in request.url or 'login' in request.url.lower():
        parsed = urlparse(request.url)
        params = parse_qs(parsed.query)
        if 'backurl' in params:
            backurl = unquote(params['backurl'][0])
            REDIRECT_URLS.append(backurl)
            print(f"  🔗 backurl: {backurl[:120]}")

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=['--disable-blink-features=AutomationControlled','--no-sandbox']
    )
    context = browser.new_context(
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
        viewport={"width": 390, "height": 844},
        locale="zh-CN",
    )
    page = context.new_page()
    page.on("response", on_response)
    page.on("request", on_request)

    # ═══ 策略A: 拦截 passport 跳转，直接跟随 backurl ═══
    print("=== 策略A: 拦截登录 → 跟随 backurl ===")
    
    page.goto("https://i.meituan.com/hotel/xiangyang/", wait_until="networkidle", timeout=20000)
    page.wait_for_timeout(2000)
    
    # 点击搜索
    try:
        btn = page.query_selector('button:has-text("查找酒店")')
        if btn:
            btn.click()
            page.wait_for_timeout(5000)
    except:
        pass
    
    # 如果有 backurl，直接导航过去（带当前cookies）
    if REDIRECT_URLS:
        backurl = REDIRECT_URLS[0]
        print(f"\n  发现 backurl: {backurl[:120]}")
        
        # 修改 backurl 中的 cityId 到襄阳 (774)
        import re as regex
        backurl_xy = regex.sub(r'cityId=\d+', 'cityId=774', backurl)
        print(f"  修改后: {backurl_xy[:120]}")
        
        # 直接导航到 backurl（带现有 cookies）
        try:
            resp = page.goto(backurl_xy, wait_until="networkidle", timeout=20000)
            page.wait_for_timeout(5000)
            status = resp.status if resp else "?"
            title = page.title()
            length = len(page.content())
            print(f"  [{status}] {title[:60]} | {length:,} chars")
            
            # 检查是否又跳转登录
            if 'passport' in page.url or 'login' in page.url.lower():
                print(f"  ⚠️ 再次跳登录: {page.url[:100]}")
            else:
                # 成功了！提取数据
                poi_els = page.query_selector_all('[data-poiid]')
                print(f"  POI元素: {len(poi_els)}")
                if poi_els:
                    for el in poi_els[:10]:
                        try:
                            pid = el.get_attribute('data-poiid')
                            txt = el.inner_text()[:120].replace('\n',' | ')
                            print(f"    [{pid}] {txt}")
                        except:
                            pass
                page.screenshot(path="cache/ota_monitor/meituan_backurl_result.png")
        except Exception as e:
            print(f"  ❌ {type(e).__name__}: {str(e)[:80]}")

    # ═══ 策略B: 页面内执行 JS 搜索 ═══
    print("\n=== 策略B: JS直接构造导航 ===")
    
    page.goto("https://i.meituan.com/hotel/xiangyang/", wait_until="networkidle", timeout=20000)
    page.wait_for_timeout(2000)
    
    # 尝试直接在页面中执行导航，绕过按钮点击
    try:
        # 构造列表页 URL 并导航
        list_url = "https://i.meituan.com/awp/h5/hotel/list/list.html?cityId=774&checkIn=2026-05-13&checkOut=2026-05-14"
        
        # 先设置一些可能会被检查的 localStorage
        page.evaluate("""
            () => {
                localStorage.setItem('cityId', '774');
                localStorage.setItem('cityName', '襄阳');
                document.cookie = 'ci=774; path=/';
            }
        """)
        
        resp = page.goto(list_url, wait_until="networkidle", timeout=20000)
        page.wait_for_timeout(5000)
        
        status = resp.status if resp else "?"
        title = page.title()
        length = len(page.content())
        print(f"  [{status}] {title[:60]} | {length:,} chars | url={page.url[:100]}")
        
        if 'passport' not in page.url:
            poi_els = page.query_selector_all('[data-poiid]')
            print(f"  POI元素: {len(poi_els)}")
            if poi_els:
                for el in poi_els[:10]:
                    pid = el.get_attribute('data-poiid')
                    txt = el.inner_text()[:120].replace('\n',' | ')
                    print(f"    [{pid}] {txt}")
                page.screenshot(path="cache/ota_monitor/meituan_js_nav_result.png")
    except Exception as e:
        print(f"  ❌ {type(e).__name__}: {str(e)[:80]}")

    # ═══ 策略C: 尝试H5 detail 页面 (可能包含价格) ═══
    print("\n=== 策略C: H5 酒店详情页 ===")
    
    # 不同的 detail URL 模式
    detail_urls = [
        "https://i.meituan.com/awp/h5/hotel/detail/481488",
        "https://i.meituan.com/awp/h5/hotel/detail/481488.html",
        "https://i.meituan.com/hotel/481488.html",
        # 带完整路径
        "https://i.meituan.com/awp/h5/hotel/detail/index.html?poiid=481488",
    ]
    
    for url in detail_urls:
        try:
            resp = page.goto(url, wait_until="domcontentloaded", timeout=15000)
            page.wait_for_timeout(2000)
            status = resp.status if resp else "?"
            title = page.title()
            length = len(page.content())
            print(f"  [{status}] {url[:70]} | {length:,} chars | {title[:60]}")
            
            if status == 200 and length > 5000:
                for kw in ['price','Price','房价','¥','￥','元起']:
                    cnt = page.content().count(kw)
                    if cnt > 0:
                        print(f"    '{kw}': {cnt} occurrences")
        except Exception as e:
            print(f"  ❌ {url[:70]} | {type(e).__name__}")

    browser.close()

# 分析捕获的API
print(f"\n=== API 捕获: {len(API_RESPONSES)} ===")
for item in API_RESPONSES:
    body = item['body']
    body_str = json.dumps(body, ensure_ascii=False)
    # 找酒店列表数据
    if isinstance(body, dict):
        for key in body:
            val = body[key]
            if isinstance(val, list) and len(val) > 0:
                print(f"\n  {item['url'][:80]}")
                print(f"  {key}: {len(val)} items")
                print(f"  first: {json.dumps(val[0], ensure_ascii=False)[:300]}")
            elif isinstance(val, dict):
                for sk, sv in val.items():
                    if isinstance(sv, list) and len(sv) > 0:
                        print(f"\n  {item['url'][:80]}")
                        print(f"  {key}.{sk}: {len(sv)} items")
                        print(f"  first: {json.dumps(sv[0], ensure_ascii=False)[:300]}")
