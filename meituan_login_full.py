# -*- coding: utf-8 -*-
"""美团登录 - 完整流程：输手机→发验证码→等用户给码→登录→抓数据"""
import json, time, re, sys
from playwright.sync_api import sync_playwright

# 从命令行参数获取验证码（如果有）
CODE = sys.argv[1] if len(sys.argv) > 1 else None

API_RESPONSES = []

def on_response(response):
    url = response.url
    ct = response.headers.get('content-type','')
    if 'json' in ct:
        for kw in ['search','poi','hotel','list','recommend','deal','hbsearch']:
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
    context = browser.new_context(
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
        viewport={"width": 390, "height": 844},
        locale="zh-CN",
    )
    page = context.new_page()
    page.on("response", on_response)
    
    # 目标URL
    target = "https://i.meituan.com/awp/h5/hotel/list/list.html?cityId=774&checkIn=2026-05-13&checkOut=2026-05-14"
    login_url = f"https://passport.meituan.com/useraccount/ilogin?backurl={target}"
    
    print("=== Step 1: 登录页 ===")
    page.goto(login_url, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(3000)
    
    # 填手机号
    phone_input = page.query_selector('#phoneNumInput')
    if not phone_input:
        print("❌ 找不到手机号输入框")
        browser.close()
        sys.exit(1)
    
    phone_input.click()
    page.wait_for_timeout(300)
    for c in "17760348653":
        phone_input.type(c, delay=50)
    page.wait_for_timeout(500)
    print(f"  手机号: {phone_input.input_value()}")
    
    # 点击获取验证码
    code_btn = page.query_selector('[class*="send"]')
    if not code_btn:
        # 找其他可能的按钮
        for sel in ['button:has-text("获取验证码")', 'span:has-text("获取验证码")', 
                    'button:has-text("发送")', '[class*="getCode"]']:
            code_btn = page.query_selector(sel)
            if code_btn: break
    
    if not code_btn:
        print("❌ 找不到获取验证码按钮")
        page.screenshot(path="cache/ota_monitor/meituan_debug.png")
        browser.close()
        sys.exit(1)
    
    code_btn.click()
    print("  已点击获取验证码")
    page.wait_for_timeout(3000)
    page.screenshot(path="cache/ota_monitor/meituan_code_sent.png")
    
    # 如果有命令行参数验证码，直接继续
    if CODE:
        print(f"\n=== Step 2: 输入验证码 {CODE} ===")
    else:
        print(f"\n{'='*50}")
        print(f"⚠️ 请输入手机 17760348653 收到的验证码: ", end="", flush=True)
        CODE = input().strip()
    
    # 输入验证码
    code_input = page.query_selector('#codeInput')
    if not code_input:
        print("❌ 找不到验证码输入框")
        browser.close()
        sys.exit(1)
    
    code_input.click()
    page.wait_for_timeout(300)
    for c in CODE:
        code_input.type(c, delay=80)
    page.wait_for_timeout(500)
    print(f"  验证码: {code_input.input_value()}")
    
    # 点击登录
    login_btn = None
    for sel in ['button:has-text("登录")', '#loginBtn', '[class*="login-btn"]',
                'button[type="submit"]', '.iLoginComp-submit']:
        login_btn = page.query_selector(sel)
        if login_btn and login_btn.is_visible():
            break
    
    if not login_btn:
        print("❌ 找不到登录按钮")
        browser.close()
        sys.exit(1)
    
    login_btn.click()
    print("  已点击登录")
    
    # 等待跳转
    print("\n=== Step 3: 等待登录完成 ===")
    page.wait_for_timeout(5000)
    
    # 可能中间有过渡页或直接跳转
    for _ in range(5):
        page.wait_for_timeout(2000)
        current_url = page.url
        print(f"  URL: {current_url[:120]}")
        if 'passport' not in current_url and 'login' not in current_url.lower():
            break
    
    current_url = page.url
    print(f"\n  最终 URL: {current_url[:150]}")
    print(f"  Title: {page.title()}")
    page.screenshot(path="cache/ota_monitor/meituan_after_login.png")
    
    # 检查是否成功
    if 'passport' in current_url or 'login' in current_url.lower():
        print("\n❌ 登录失败，仍在登录页")
        # 检查错误信息
        err = page.query_selector('[class*="error"], [class*="err"], [class*="toast"], [class*="tip"]')
        if err:
            print(f"  错误提示: {err.inner_text()}")
        page.screenshot(path="cache/ota_monitor/meituan_login_fail.png")
        browser.close()
        sys.exit(1)
    
    # 如果没有自动到列表页，手动导航
    if 'list' not in current_url:
        print(f"\n  手动导航到酒店列表...")
        page.goto(target, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(5000)
        current_url = page.url
        print(f"  导航后 URL: {current_url[:150]}")
    
    # 提取酒店数据
    print(f"\n=== Step 4: 提取酒店数据 ===")
    html = page.content()
    print(f"  页面大小: {len(html):,} chars")
    
    poi_els = page.query_selector_all('[data-poiid]')
    print(f"  data-poiid 元素: {len(poi_els)}")
    
    if poi_els:
        hotels = []
        for el in poi_els:
            try:
                pid = el.get_attribute('data-poiid')
                txt = el.inner_text()
                hotels.append({'poiId': pid, 'text': txt})
            except:
                pass
        
        print(f"\n  === 襄阳酒店列表 ({len(hotels)} 家) ===")
        for h in hotels[:30]:
            lines = h['text'].replace('\n',' | ')[:150]
            print(f"  [{h['poiId']}] {lines}")
        
        with open("cache/ota_monitor/meituan_xiangyang_hotels.json", "w", encoding="utf-8") as f:
            json.dump(hotels, f, ensure_ascii=False, indent=2)
        print(f"\n  数据已保存: meituan_xiangyang_hotels.json")
    else:
        print("  ⚠️ 页面无 data-poiid，尝试其他选择器...")
        for cls in ['[class*="poi"]', '[class*="hotel"]', '[class*="card"]', 
                    '[class*="list-item"]', '[class*="item"]']:
            els = page.query_selector_all(cls)
            if len(els) > 3:
                print(f"  {cls}: {len(els)} elements")
                for el in els[:3]:
                    try:
                        txt = el.inner_text()[:100].replace('\n',' | ')
                        print(f"    {txt}")
                    except:
                        pass
    
    # 保存 cookies 和完整 HTML
    cookies = context.cookies()
    with open("cache/ota_monitor/meituan_loggedin_cookies.json", "w") as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)
    with open("cache/ota_monitor/meituan_list_loggedin.html", "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  Cookies ({len(cookies)}个) 和 HTML 已保存")
    
    # 分析API
    print(f"\n=== API 拦截: {len(API_RESPONSES)} ===")
    for item in API_RESPONSES:
        body = item['body']
        body_str = json.dumps(body, ensure_ascii=False)
        if isinstance(body, dict):
            for key in body:
                val = body[key]
                if isinstance(val, dict):
                    for sk, sv in val.items():
                        if isinstance(sv, list) and len(sv) > 0:
                            print(f"\n  ✅ {item['url'][:120]}")
                            print(f"  {key}.{sk}: {len(sv)} items")
                            print(f"  first: {json.dumps(sv[0], ensure_ascii=False)[:400]}")
                elif isinstance(val, list) and len(val) > 0:
                    print(f"\n  ✅ {item['url'][:120]}")
                    print(f"  {key}: {len(val)} items")
                    print(f"  first: {json.dumps(val[0], ensure_ascii=False)[:400]}")
    
    browser.close()
    print("\n✅ 流程完成")
