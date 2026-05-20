# -*- coding: utf-8 -*-
"""美团登录步骤2: 输入验证码 → 登录 → 抓酒店数据"""
import json, time, re
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
                    API_RESPONSES.append({'url': url[:180], 'body': body})
                except:
                    pass
                break

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=True,
        args=['--disable-blink-features=AutomationControlled','--no-sandbox']
    )
    
    # 恢复之前的登录状态
    context = browser.new_context(
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
        viewport={"width": 390, "height": 844},
        locale="zh-CN",
        storage_state="cache/ota_monitor/meituan_state.json"
    )
    page = context.new_page()
    page.on("response", on_response)
    
    # 回到登录页
    target_url = "https://i.meituan.com/awp/h5/hotel/list/list.html?cityId=774&checkIn=2026-05-13&checkOut=2026-05-14"
    login_url = f"https://passport.meituan.com/useraccount/ilogin?backurl={target_url}"
    
    print("=== 回到登录页 ===")
    page.goto(login_url, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(2000)
    
    # 检查是否需要重新输入手机号
    try:
        phone_input = page.query_selector('#phoneNumInput')
        if phone_input:
            current_val = phone_input.input_value()
            print(f"  手机号输入框当前值: '{current_val}'")
            if not current_val or '177' not in current_val:
                phone_input.fill("17760348653")
                page.wait_for_timeout(500)
        
        # 输入验证码
        code_input = page.query_selector('#codeInput')
        if code_input:
            code_input.click()
            page.wait_for_timeout(300)
            code_input.fill("480597")
            print(f"  已输入验证码: 480597")
            page.wait_for_timeout(500)
            
            page.screenshot(path="cache/ota_monitor/meituan_login_04_code_filled.png")
            
            # 点击登录/确定按钮
            login_btn = None
            for sel in ['button:has-text("登录")', 'button:has-text("确定")',
                        'button:has-text("登 录")', 'button[type="submit"]',
                        '[class*="login-btn"]', '[class*="submit"]',
                        '.iLoginComp-submit', 'button:has-text("进入美团")']:
                try:
                    btn = page.query_selector(sel)
                    if btn and btn.is_visible():
                        text = btn.inner_text()
                        print(f"  找到登录按钮: '{text}' via {sel}")
                        login_btn = btn
                        break
                except:
                    pass
            
            if login_btn:
                login_btn.click()
                print("  已点击登录")
                
                # 等待登录完成 + 跳转
                page.wait_for_timeout(8000)
                print(f"\n  登录后 URL: {page.url[:120]}")
                print(f"  Title: {page.title()}")
                
                page.screenshot(path="cache/ota_monitor/meituan_login_05_after_login.png")
                
                # 检查是否成功到达酒店列表页
                if 'list' in page.url or 'hotel' in page.url:
                    if 'passport' not in page.url:
                        print("\n  ✅ 登录成功！已到达酒店列表页！")
                        
                        # 等待数据加载
                        page.wait_for_timeout(5000)
                        
                        # 提取酒店数据
                        html = page.content()
                        print(f"  页面大小: {len(html):,} chars")
                        
                        # 找 data-poiid
                        poi_els = page.query_selector_all('[data-poiid]')
                        print(f"  POI 元素: {len(poi_els)}")
                        
                        if poi_els:
                            hotels = []
                            for el in poi_els[:30]:
                                try:
                                    pid = el.get_attribute('data-poiid')
                                    txt = el.inner_text()
                                    hotels.append({'poiId': pid, 'text': txt})
                                except:
                                    pass
                            
                            print(f"\n  === 襄阳酒店列表 ({len(hotels)} 家) ===")
                            for h in hotels:
                                lines = h['text'].replace('\n',' | ')[:150]
                                print(f"  [{h['poiId']}] {lines}")
                            
                            # 保存
                            with open("cache/ota_monitor/meituan_xiangyang_hotels.json", "w", encoding="utf-8") as f:
                                json.dump(hotels, f, ensure_ascii=False, indent=2)
                            print(f"\n  数据已保存: meituan_xiangyang_hotels.json")
                        
                        # 保存完整 HTML
                        with open("cache/ota_monitor/meituan_list_loggedin.html", "w", encoding="utf-8") as f:
                            f.write(html)
                        
                        # 保存登录后的 cookies
                        cookies = context.cookies()
                        with open("cache/ota_monitor/meituan_cookies_loggedin.json", "w") as f:
                            json.dump(cookies, f, ensure_ascii=False, indent=2)
                        print(f"  Cookies: {len(cookies)} 已保存")
                    else:
                        print(f"\n  ⚠️ 仍在登录页")
                else:
                    print(f"\n  ⚠️ 未知页面: {page.url[:120]}")
                    
            else:
                print("  ❌ 未找到登录按钮")
                # 列所有按钮
                all_btns = page.query_selector_all('button, [role="button"]')
                for b in all_btns[:10]:
                    try:
                        if b.is_visible():
                            print(f"    按钮: '{b.inner_text()[:50]}'")
                    except:
                        pass
        else:
            print("  ❌ 未找到验证码输入框")
    except Exception as e:
        print(f"  ❌ 登录流程出错: {e}")
        import traceback
        traceback.print_exc()
    
    # 分析拦截的API
    print(f"\n=== 拦截 API: {len(API_RESPONSES)} ===")
    for item in API_RESPONSES:
        body = item['body']
        body_str = json.dumps(body, ensure_ascii=False)
        
        # 找酒店列表数据
        if isinstance(body, dict):
            for key in body:
                val = body[key]
                if isinstance(val, list) and len(val) > 0:
                    print(f"\n  ✅ {item['url'][:100]}")
                    print(f"  {key}: {len(val)} items")
                    print(f"  first: {json.dumps(val[0], ensure_ascii=False)[:400]}")
                elif isinstance(val, dict):
                    for sk, sv in val.items():
                        if isinstance(sv, list) and len(sv) > 0:
                            print(f"\n  ✅ {item['url'][:100]}")
                            print(f"  {key}.{sk}: {len(sv)} items")
                            print(f"  first: {json.dumps(sv[0], ensure_ascii=False)[:400]}")

    browser.close()
