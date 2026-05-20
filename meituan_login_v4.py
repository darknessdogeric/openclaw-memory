# -*- coding: utf-8 -*-
"""美团登录 v4 - 先请求验证码 → 保存状态 → 等待用户给码 → 秒提交"""
import json, time, sys
from playwright.sync_api import sync_playwright

CODE = sys.argv[1] if len(sys.argv) > 1 else None

# Phase 1: 请求验证码
if not CODE:
    print("=== Phase 1: 请求验证码 ===")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True,
            args=['--disable-blink-features=AutomationControlled','--no-sandbox'])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
            viewport={"width": 390, "height": 844}, locale="zh-CN")
        page = context.new_page()
        
        target = "https://i.meituan.com/awp/h5/hotel/list/list.html?cityId=774&checkIn=2026-05-13&checkOut=2026-05-14"
        page.goto(f"https://passport.meituan.com/useraccount/ilogin?backurl={target}", 
                  wait_until="networkidle", timeout=30000)
        page.wait_for_timeout(3000)
        
        # 关弹窗
        page.evaluate("document.querySelectorAll('[class*=\"modal\"],[class*=\"mask\"]').forEach(m=>m.remove())")
        page.wait_for_timeout(500)
        
        # 填手机号
        page.evaluate('document.getElementById("phoneNumInput").value="17760348653";'
                      'document.getElementById("phoneNumInput").dispatchEvent(new Event("input",{bubbles:true}))')
        page.wait_for_timeout(500)
        
        # 点获取验证码
        page.evaluate('document.querySelector("[class*=\\"send\\"]")?.click()')
        page.wait_for_timeout(2000)
        
        page.screenshot(path="cache/ota_monitor/meituan_v4_code_sent.png")
        
        # 保存状态
        context.storage_state(path="cache/ota_monitor/meituan_v4_state.json")
        print("  ✅ 验证码已发送到 17760348653")
        print("  ✅ 状态已保存")
        browser.close()
    
    print("\n⚠️ 请提供新验证码，运行: python meituan_login_v4.py <验证码>")
    sys.exit(0)

# Phase 2: 提交登录
print(f"=== Phase 2: 提交登录 (code={CODE}) ===")
API_DATA = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True,
        args=['--disable-blink-features=AutomationControlled','--no-sandbox'])
    context = browser.new_context(
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
        viewport={"width": 390, "height": 844}, locale="zh-CN",
        storage_state="cache/ota_monitor/meituan_v4_state.json")
    page = context.new_page()
    
    # 监听API
    def on_resp(response):
        url = response.url
        ct = response.headers.get('content-type','')
        if 'json' in ct:
            for kw in ['search','poi','hotel','list','deal','hbsearch','recommend']:
                if kw in url:
                    try:
                        API_DATA.append({'u': url[:180], 'b': response.json()})
                    except: pass
                    break
    page.on("response", on_resp)
    
    target = "https://i.meituan.com/awp/h5/hotel/list/list.html?cityId=774&checkIn=2026-05-13&checkOut=2026-05-14"
    page.goto(f"https://passport.meituan.com/useraccount/ilogin?backurl={target}",
              wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(2000)
    
    # 关弹窗
    page.evaluate("document.querySelectorAll('[class*=\"modal\"],[class*=\"mask\"]').forEach(m=>m.remove())")
    page.wait_for_timeout(300)
    
    # 填验证码 + 点登录（一气呵成）
    result = page.evaluate(f"""
        () => {{
            const ci = document.getElementById('codeInput');
            if (!ci) return 'NO_CODE_INPUT';
            ci.focus(); ci.value = '{CODE}';
            ci.dispatchEvent(new Event('input', {{bubbles: true}}));
            ci.dispatchEvent(new Event('change', {{bubbles: true}}));
            
            const btns = document.querySelectorAll('button');
            for (let b of btns) {{
                const t = b.textContent.trim();
                if (t === '登录' || t.includes('登录')) {{
                    b.click(); return 'CLICKED:' + t;
                }}
            }}
            document.querySelector('form')?.submit();
            return 'FORM_SUBMIT';
        }}
    """)
    print(f"  Submit: {result}")
    
    # 等待跳转
    for i in range(6):
        page.wait_for_timeout(2000)
        u = page.url
        ok = 'passport' not in u and 'login' not in u.lower()
        print(f"  [{i}] {'✅ OK' if ok else '⏳ 登录中...'} | {page.title()[:40]}")
        if ok: break
    
    u = page.url
    if 'passport' in u or 'login' in u.lower():
        print("\n❌ 登录失败")
        page.screenshot(path="cache/ota_monitor/meituan_v4_fail.png")
        # 检查错误/验证码过期
        msgs = page.evaluate("""
            () => {
                const all = document.querySelectorAll('[class*="error"],[class*="err"],[class*="toast"],[class*="msg"],[class*="tip"]');
                return Array.from(all).map(e=>e.textContent.trim()).filter(t=>t);
            }
        """)
        print(f"  页面消息: {msgs}")
        browser.close()
        sys.exit(1)
    
    # 到列表页
    if 'list' not in u:
        page.goto(target, wait_until="networkidle", timeout=20000)
        page.wait_for_timeout(5000)
    
    print(f"\n=== 酒店数据 ===")
    html = page.content()
    print(f"  页面: {len(html):,} chars")
    
    pois = page.query_selector_all('[data-poiid]')
    print(f"  data-poiid: {len(pois)} 个")
    
    if pois:
        hotels = []
        for el in pois:
            try:
                pid = el.get_attribute('data-poiid')
                txt = el.inner_text()
                hotels.append({'poiId': pid, 'text': txt})
            except: pass
        
        print(f"\n  襄阳酒店 ({len(hotels)} 家):")
        for h in hotels[:30]:
            print(f"  [{h['poiId']}] {h['text'].replace(chr(10),' | ')[:150]}")
        
        with open("cache/ota_monitor/meituan_xiangyang_hotels.json", "w", encoding="utf-8") as f:
            json.dump(hotels, f, ensure_ascii=False, indent=2)
    
    # 保存
    cookies = context.cookies()
    with open("cache/ota_monitor/meituan_loggedin_cookies.json", "w") as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)
    with open("cache/ota_monitor/meituan_list_loggedin.html", "w", encoding="utf-8") as f:
        f.write(html)
    page.screenshot(path="cache/ota_monitor/meituan_v4_result.png")
    
    # API数据
    print(f"\n=== API ({len(API_DATA)}) ===")
    for a in API_DATA:
        b = a['b']
        bs = json.dumps(b, ensure_ascii=False)
        if isinstance(b, dict):
            for k in b:
                v = b[k]
                if isinstance(v, dict):
                    for sk, sv in v.items():
                        if isinstance(sv, list) and len(sv) > 0:
                            print(f"\n  ✅ {a['u'][:100]}")
                            print(f"  {k}.{sk}: {len(sv)} items, first: {json.dumps(sv[0],ensure_ascii=False)[:300]}")
                elif isinstance(v, list) and len(v) > 0:
                    print(f"\n  ✅ {a['u'][:100]}")
                    print(f"  {k}: {len(v)} items, first: {json.dumps(v[0],ensure_ascii=False)[:300]}")
    
    browser.close()
    print("\n✅ SUCCESS")
