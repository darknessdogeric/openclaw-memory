# -*- coding: utf-8 -*-
"""美团酒店 - Playwright 完整交互：搜索 + 提取"""
import json, re, time
from playwright.sync_api import sync_playwright

API_RESPONSES = []

def on_response(response):
    url = response.url
    if 'json' in (response.headers.get('content-type','')):
        if any(k in url for k in ['search','poi','hotel','list','recommend','deal']):
            try:
                body = response.json()
                API_RESPONSES.append({'url': url[:120], 'body': body})
                print(f"  📡 {len(API_RESPONSES)}. {url.split('?')[0].split('/')[-1]:30s} {len(json.dumps(body,ensure_ascii=False)):,} chars")
            except:
                pass

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

    # 加载酒店移动端搜索页 (带城市参数)
    print("=== 加载搜索页 ===")
    page.goto("https://i.meituan.com/hotel/xiangyang/?ci=774", wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(3000)
    print(f"  Title: {page.title()}")

    # 尝试点击搜索/确认按钮
    print("\n=== 尝试触发搜索 ===")
    # 常见美团搜索按钮选择器
    for sel in [
        'button', '[class*="search"]', '[class*="Search"]',
        'input[type="submit"]', '[class*="confirm"]', '[class*="btn"]',
        '.search-btn', '.submit-btn', 'a[class*="search"]',
    ]:
        try:
            btn = page.query_selector(sel)
            if btn:
                text = (btn.inner_text() or '')[:30]
                visible = btn.is_visible()
                print(f"  {sel}: '{text}' visible={visible}")
        except:
            pass

    # 尝试直接导航到带搜索参数的URL
    print("\n=== 直接搜索URL ===")
    search_urls = [
        "https://i.meituan.com/hotel/xiangyang/search?checkin=2026-05-13&checkout=2026-05-14",
        "https://i.meituan.com/hotel/list/774?checkin=2026-05-13&checkout=2026-05-14",
        "https://hotel.meituan.com/xiangyang/?checkin=2026-05-13&checkout=2026-05-14",
    ]
    for url in search_urls:
        try:
            resp = page.goto(url, wait_until="domcontentloaded", timeout=15000)
            page.wait_for_timeout(3000)
            title = page.title()
            length = len(page.content())
            status = resp.status if resp else "?"
            print(f"  [{status}] {title[:60]} | {length:,} chars")
        except Exception as e:
            print(f"  [ERR] {type(e).__name__}: {str(e)[:60]}")

    # 检查DOM中的酒店数据
    print("\n=== DOM 数据提取 ===")
    html = page.content()
    
    # 搜索 JSON-LD 或 inline JSON
    for pattern in [r'window\.__NEXT_DATA__\s*=\s*({.+?});', r'__NUXT__\s*=\s*({.+?});',
                    r'window\.__INITIAL_STATE__\s*=\s*({.+?});', r'"poiList"\s*:\s*(\[.+?\])',
                    r'"hotelList"\s*:\s*(\[.+?\])']:
        m = re.search(pattern, html, re.DOTALL)
        if m:
            print(f"  ✅ matched: {m.group(0)[:200]}")

    # 提取数据属性
    data_els = page.query_selector_all('[data-poiid], [data-hotelid], [data-id]')
    print(f"  data-poiid/hotelid elements: {len(data_els)}")
    
    # 检查是否有酒店卡片
    for cls in ['hotel-card','poi-card','hotel-item','list-item','card','[class*="Hotel"]','[class*="hotel"]']:
        try:
            els = page.query_selector_all(cls)
            if len(els) > 0:
                print(f"  {cls}: {len(els)} elements")
                if len(els) > 0:
                    txt = els[0].inner_text()[:200].replace('\n',' | ')
                    print(f"    first: {txt}")
        except:
            pass

    browser.close()

# 分析捕获的 API
print(f"\n=== 捕获 {len(API_RESPONSES)} 个API响应 ===")
for i, item in enumerate(API_RESPONSES):
    body = item['body']
    body_str = json.dumps(body, ensure_ascii=False)
    # 检查是否有酒店数据
    has_poi = 'poi' in body_str.lower()
    has_hotel = 'hotel' in body_str.lower()
    has_list = 'list' in body_str.lower() or 'items' in body_str.lower()
    
    tags = []
    if has_poi: tags.append('POI')
    if has_hotel: tags.append('HOTEL')
    if has_list: tags.append('LIST')
    
    print(f"  {i+1}. [{','.join(tags) if tags else '?'}] {item['url']}")
    if tags:
        print(f"     Sample: {body_str[:400]}")
        # 如果有列表数据，尝试提取
        if has_list:
            try:
                data = body.get('data', {})
                for k in ['poiList','hotelList','list','items','pois','hotels','searchResult']:
                    if k in data:
                        lst = data[k]
                        print(f"     >>> data.{k}: {len(lst) if isinstance(lst, list) else type(lst).__name__} entries")
                        if isinstance(lst, list) and len(lst) > 0:
                            print(f"     >>> first entry keys: {list(lst[0].keys()) if isinstance(lst[0], dict) else type(lst[0]).__name__}")
            except:
                pass
