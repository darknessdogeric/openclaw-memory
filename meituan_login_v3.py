# -*- coding: utf-8 -*-
"""美团登录 v3 - 处理弹窗拦截"""
import json, time, sys
from playwright.sync_api import sync_playwright

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
    
    target = "https://i.meituan.com/awp/h5/hotel/list/list.html?cityId=774&checkIn=2026-05-13&checkOut=2026-05-14"
    login_url = f"https://passport.meituan.com/useraccount/ilogin?backurl={target}"
    
    print("=== Step 1: 登录页 ===")
    page.goto(login_url, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(3000)
    
    # 处理可能出现的弹窗
    for sel in ['.yoda-modal-mask', '[class*="modal"]', '[class*="popup"]', '[class*="dialog"]',
                '[class*="overlay"]', '[class*="mask"]', '.yoda-dialog-close',
                '[class*="close"]', '.modal-close', '.dialog-close']:
        try:
            overlay = page.query_selector(sel)
            if overlay and overlay.is_visible():
                print(f"  发现弹窗: {sel}, 尝试关闭...")
                # 尝试点击关闭按钮
                close_btn = page.query_selector('[class*="close"], [class*="Close"], .yoda-dialog-close')
                if close_btn:
                    close_btn.click(force=True)
                    page.wait_for_timeout(1000)
                else:
                    # 尝试点击遮罩层外部
                    overlay.click(position={"x": 10, "y": 10}, force=True)
                    page.wait_for_timeout(1000)
        except:
            pass
    
    page.screenshot(path="cache/ota_monitor/meituan_login_v3_01.png")
    
    # 填手机号 - 用 evaluate 直接设置值绕过可能的交互问题
    page.evaluate('document.getElementById("phoneNumInput").value = "17760348653"')
    page.evaluate('document.getElementById("phoneNumInput").dispatchEvent(new Event("input", {bubbles: true}))')
    page.wait_for_timeout(500)
    print(f"  手机号已填入")
    
    # 点击获取验证码 - 用 evaluate 直接触发点击
    page.evaluate("""
        () => {
            const btn = document.querySelector('[class*="send"]');
            if (btn) btn.click();
        }
    """)
    print("  已点击获取验证码")
    page.wait_for_timeout(3000)
    page.screenshot(path="cache/ota_monitor/meituan_login_v3_02.png")
    
    if not CODE:
        print("❌ 需要验证码参数")
        browser.close()
        sys.exit(1)
    
    print(f"\n=== Step 2: 输入验证码 {CODE} ===")
    
    # 再次处理弹窗
    try:
        page.evaluate("""
            () => {
                const masks = document.querySelectorAll('[class*="modal"], [class*="mask"], [class*="overlay"]');
                masks.forEach(m => { if(m.style.display !== 'none') m.remove(); });
            }
        """)
        page.wait_for_timeout(500)
    except:
        pass
    
    # 用 JS 直接设置验证码
    page.evaluate(f"""
        () => {{
            const input = document.getElementById('codeInput');
            if (input) {{
                input.focus();
                input.value = '{CODE}';
                input.dispatchEvent(new Event('input', {{bubbles: true}}));
                input.dispatchEvent(new Event('change', {{bubbles: true}}));
            }}
        }}
    """)
    page.wait_for_timeout(500)
    print(f"  验证码已填入")
    page.screenshot(path="cache/ota_monitor/meituan_login_v3_03.png")
    
    # 点击登录
    result = page.evaluate("""
        () => {
            const btns = document.querySelectorAll('button');
            for (let b of btns) {
                if (b.textContent.includes('登录') || b.textContent.includes('登 录')) {
                    b.click();
                    return 'clicked: ' + b.textContent;
                }
            }
            // 尝试 submit
            const forms = document.querySelectorAll('form');
            for (let f of forms) {
                f.submit();
                return 'form submitted';
            }
            return 'no button found';
        }
    """)
    print(f"  登录按钮: {result}")
    
    # 等待跳转
    print("\n=== Step 3: 等待登录完成 ===")
    for i in range(8):
        page.wait_for_timeout(2000)
        url = page.url
        title = page.title()
        is_login = 'passport' in url or 'login' in url.lower()
        print(f"  [{i}] {title[:40]} | {'LOGIN_PAGE' if is_login else 'OK'} | {url[:100]}")
        if not is_login:
            break
    
    current_url = page.url
    
    if 'passport' in current_url or 'login' in current_url.lower():
        print("\n❌ 登录失败，检查错误信息")
        page.screenshot(path="cache/ota_monitor/meituan_login_v3_fail.png")
        # 检查错误
        errors = page.evaluate("""
            () => {
                const errs = document.querySelectorAll('[class*="error"], [class*="err"], [class*="toast"], [class*="msg"]');
                const msgs = [];
                errs.forEach(e => { if(e.textContent.trim()) msgs.push(e.textContent.trim()); });
                return msgs;
            }
        """)
        print(f"  错误: {errors}")
        browser.close()
        sys.exit(1)
    
    # 手动导航到列表
    if 'list' not in current_url:
        print("  手动导航到酒店列表...")
        page.goto(target, wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(5000)
        current_url = page.url
        print(f"  导航后: {page.title()}")
    
    # 提取数据
    print(f"\n=== Step 4: 酒店数据 ===")
    html = page.content()
    print(f"  页面: {len(html):,} chars")
    
    poi_els = page.query_selector_all('[data-poiid]')
    print(f"  data-poiid: {len(poi_els)} 个")
    
    if poi_els:
        hotels = []
        for el in poi_els:
            try:
                pid = el.get_attribute('data-poiid')
                txt = el.inner_text()
                hotels.append({'poiId': pid, 'text': txt})
            except:
                pass
        
        print(f"\n  === 襄阳酒店 ({len(hotels)} 家) ===")
        for h in hotels[:30]:
            lines = h['text'].replace('\n',' | ')[:150]
            print(f"  [{h['poiId']}] {lines}")
        
        with open("cache/ota_monitor/meituan_xiangyang_hotels.json", "w", encoding="utf-8") as f:
            json.dump(hotels, f, ensure_ascii=False, indent=2)
        print(f"\n  已保存")
    
    page.screenshot(path="cache/ota_monitor/meituan_login_v3_result.png")
    
    # 保存 cookies
    cookies = context.cookies()
    with open("cache/ota_monitor/meituan_loggedin_cookies.json", "w") as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)
    with open("cache/ota_monitor/meituan_list_loggedin.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    # API分析
    print(f"\n=== API ({len(API_RESPONSES)}) ===")
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
    print("\n✅ 完成")
