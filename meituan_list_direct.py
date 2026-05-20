# -*- coding: utf-8 -*-
"""美团酒店 - 直接列表页URL + 多策略绕过登录"""
import json, re, time
from playwright.sync_api import sync_playwright

API_RESPONSES = []

def on_response(response):
    url = response.url
    ct = response.headers.get('content-type','')
    if 'json' in ct:
        for kw in ['search','poi','hotel','list','recommend','deal','hbsearch','nearby']:
            if kw in url:
                try:
                    body = response.json()
                    API_RESPONSES.append({'url': url[:150], 'body': body})
                    print(f"  📡 #{len(API_RESPONSES)} {url.split('?')[0].rsplit('/',1)[-1]}")
                except:
                    pass
                break

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=['--disable-blink-features=AutomationControlled','--no-sandbox']
    )
    context = browser.new_context(
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        viewport={"width": 390, "height": 844},
        locale="zh-CN",
    )
    page = context.new_page()
    page.on("response", on_response)

    # 直接访问列表页 (从 backURL 提取的 URL 结构)
    list_urls = [
        # 襄阳 cityId=774
        "https://i.meituan.com/awp/h5/hotel/list/list.html?cityId=774&accommodationType=1&checkIn=2026-05-13&checkOut=2026-05-14&lat=32.0090&lng=112.1225&distance=3000",
        # 更简化参数
        "https://i.meituan.com/awp/h5/hotel/list/list.html?cityId=774&checkIn=2026-05-13&checkOut=2026-05-14",
        # 用 cityName 替代 cityId
        "https://i.meituan.com/awp/h5/hotel/list/list.html?cityName=%E8%A5%84%E9%98%B3&checkIn=2026-05-13&checkOut=2026-05-14",
        # ihotel 域名
        "https://ihotel.meituan.com/awp/h5/hotel/list/list.html?cityId=774&checkIn=2026-05-13&checkOut=2026-05-14",
    ]

    for url in list_urls:
        print(f"\n=== {url[:80]}... ===")
        try:
            resp = page.goto(url, wait_until="networkidle", timeout=20000)
            page.wait_for_timeout(3000)
            status = resp.status if resp else "?"
            title = page.title()
            length = len(page.content())
            print(f"  [{status}] {title[:60]} | {length:,} chars")
            
            # 检查是否跳转登录
            if 'login' in page.url or 'passport' in page.url:
                print(f"  ⚠️ 跳转到登录: {page.url[:100]}")
                continue
            
            # 检查DOM
            poi_els = page.query_selector_all('[data-poiid]')
            hotel_els = page.query_selector_all('[class*="poi" i], [class*="hotel" i], [class*="card" i]')
            print(f"  POI元素: {len(poi_els)}, 酒店类元素: {len(hotel_els)}")
            
            if poi_els:
                for el in poi_els[:5]:
                    try:
                        txt = el.inner_text()[:100].replace('\n',' | ')
                        pid = el.get_attribute('data-poiid')
                        print(f"    [{pid}] {txt}")
                    except:
                        pass
            
            if length > 50000:
                page.screenshot(path=f"cache/ota_monitor/meituan_list_{list_urls.index(url)}.png")
                print(f"  截图已保存")
                
        except Exception as e:
            print(f"  ❌ {type(e).__name__}: {str(e)[:80]}")

    browser.close()

# 分析API
print(f"\n=== API分析 ({len(API_RESPONSES)} responses) ===")
for item in API_RESPONSES:
    body = item['body']
    body_str = json.dumps(body, ensure_ascii=False)
    # 找列表数据
    if isinstance(body, dict):
        for key in ['data','poiList','hotelList','searchResult','list','pois','hotels','rooms','poiInfos']:
            if key in body:
                val = body[key]
                if isinstance(val, list) and len(val) > 0:
                    print(f"\n  ✅ {item['url'][:80]}")
                    print(f"     data.{key}: {len(val)} 条")
                    print(f"     第一条: {json.dumps(val[0], ensure_ascii=False)[:500]}")
                    break
                elif isinstance(val, dict):
                    for sk, sv in val.items():
                        if isinstance(sv, list) and len(sv) > 0:
                            print(f"\n  ✅ {item['url'][:80]}")
                            print(f"     data.{key}.{sk}: {len(sv)} 条")
                            print(f"     第一条: {json.dumps(sv[0], ensure_ascii=False)[:500]}")
                            break
