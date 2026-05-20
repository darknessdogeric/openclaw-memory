# -*- coding: utf-8 -*-
"""美团酒店 - Playwright 点击搜索 + 捕获酒店列表"""
import json, re, time
from playwright.sync_api import sync_playwright

API_RESPONSES = []

def on_response(response):
    url = response.url
    ct = response.headers.get('content-type','')
    if 'json' in ct:
        # 只捕获可能含酒店数据的 API
        for kw in ['search','poi','hotel','list','recommend','deal','hbsearch']:
            if kw in url:
                try:
                    body = response.json()
                    API_RESPONSES.append({'url': url[:150], 'body': body})
                    print(f"  📡 #{len(API_RESPONSES)} {url.split('?')[0].split('/')[-2:]}")
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

    print("=== 1. 加载襄阳酒店页 ===")
    page.goto("https://i.meituan.com/hotel/xiangyang/", wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(2000)
    print(f"  URL: {page.url}")

    # 截图看页面状态
    page.screenshot(path="cache/ota_monitor/meituan_before_click.png")
    print(f"  截图已保存")

    # 尝试点击"查找酒店"按钮
    print("\n=== 2. 点击搜索 ===")
    clicked = False
    for sel in ['button:has-text("查找酒店")', 'button:has-text("搜索")', 
                '[class*="search-btn"]', '.submit-btn', 'button[type="submit"]']:
        try:
            btn = page.query_selector(sel)
            if btn and btn.is_visible():
                text = btn.inner_text()
                print(f"  找到按钮: '{text}' via {sel}")
                btn.click()
                clicked = True
                print(f"  已点击!")
                break
        except Exception as e:
            print(f"  {sel}: {e}")

    if not clicked:
        print("  ❌ 未找到可点击按钮")
        # 尝试触发 form submit
        try:
            page.evaluate("document.querySelector('form')?.submit()")
            print("  尝试提交表单")
        except:
            pass

    # 等待搜索结果
    print("\n=== 3. 等待搜索结果 ===")
    page.wait_for_timeout(8000)
    
    url_after = page.url
    title_after = page.title()
    html_len = len(page.content())
    print(f"  URL: {url_after}")
    print(f"  Title: {title_after}")
    print(f"  HTML: {html_len:,} chars")

    page.screenshot(path="cache/ota_monitor/meituan_after_click.png")
    print(f"  截图已保存")

    # 提取数据
    print("\n=== 4. 提取酒店数据 ===")
    
    # 方法A: 从data属性
    data_els = page.query_selector_all('[data-poiid]')
    if data_els:
        print(f"  data-poiid 元素: {len(data_els)}")
        for el in data_els[:5]:
            poiid = el.get_attribute('data-poiid')
            text = el.inner_text()[:120].replace('\n',' | ')
            print(f"    poiid={poiid}: {text}")
    
    # 方法B: 从React状态
    html = page.content()
    for json_key in ['poiList','hotelList','searchResult','list','hotels','pois']:
        idx = html.find(f'"{json_key}"')
        if idx >= 0:
            chunk = html[max(0,idx-30):idx+500]
            print(f"  ✅ '{json_key}' at byte {idx}: {chunk[:300]}")

    # 方法C: JS执行提取
    try:
        js_data = page.evaluate("""
            () => {
                // 尝试各种 React/Vue 数据存储方式
                const results = {};
                if (window.__NEXT_DATA__) results.__NEXT_DATA__ = true;
                if (window.__NUXT__) results.__NUXT__ = true;
                if (window.__INITIAL_STATE__) results.__INITIAL_STATE__ = true;
                
                // 检查所有 data- 属性元素
                const poiEls = document.querySelectorAll('[data-poiid]');
                results.poiCount = poiEls.length;
                
                // 检查是否有列表项
                const items = document.querySelectorAll('[class*="poi" i], [class*="hotel" i]');
                results.itemCount = items.length;
                
                return results;
            }
        """)
        print(f"  JS提取: {json.dumps(js_data, ensure_ascii=False)}")
    except Exception as e:
        print(f"  JS提取失败: {e}")

    browser.close()

# 分析捕获的API
print(f"\n=== 捕获 {len(API_RESPONSES)} 个API响应 ===")
hotel_apis = []
for item in API_RESPONSES:
    body = item['body']
    body_str = json.dumps(body, ensure_ascii=False)
    
    # 分类
    for data_key in ['data','poiList','hotelList','searchResult','list','pois','hotels','rooms']:
        if isinstance(body, dict) and data_key in body:
            val = body[data_key]
            if isinstance(val, list) and len(val) > 0:
                hotel_apis.append(item)
                print(f"\n  ✅ [{data_key}] {item['url']}")
                print(f"     条目: {len(val)}")
                print(f"     第一条: {json.dumps(val[0], ensure_ascii=False)[:500]}")
                break
            elif isinstance(val, dict) and any(isinstance(v, list) and len(v) > 0 for v in val.values()):
                hotel_apis.append(item)
                print(f"\n  ✅ [{data_key}] {item['url']}")
                for sk, sv in val.items():
                    if isinstance(sv, list) and len(sv) > 0:
                        print(f"     {sk}: {len(sv)} items, first: {json.dumps(sv[0], ensure_ascii=False)[:300]}")
                break

if not hotel_apis:
    print("  ⚠️ 未找到含酒店列表的API响应")
    print("  所有API摘要:")
    for item in API_RESPONSES:
        body_keys = list(item['body'].keys()) if isinstance(item['body'], dict) else type(item['body']).__name__
        print(f"    {item['url'][:80]} | keys={body_keys}")
