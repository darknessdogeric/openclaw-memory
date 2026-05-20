# -*- coding: utf-8 -*-
"""美团登录 - Playwright 交互式"""
import json, time, re
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(
        headless=False,  # 可视化，方便观察
        args=['--disable-blink-features=AutomationControlled','--no-sandbox']
    )
    context = browser.new_context(
        user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
        viewport={"width": 390, "height": 844},
        locale="zh-CN",
    )
    page = context.new_page()
    
    # 目标: 登录后直接到襄阳酒店列表
    target_url = "https://i.meituan.com/awp/h5/hotel/list/list.html?cityId=774&checkIn=2026-05-13&checkOut=2026-05-14"
    login_url = f"https://passport.meituan.com/useraccount/ilogin?backurl={target_url}"
    
    print("=== 导航到登录页 ===")
    page.goto(login_url, wait_until="networkidle", timeout=30000)
    page.wait_for_timeout(3000)
    
    print(f"URL: {page.url[:100]}")
    print(f"Title: {page.title()}")
    
    # 截图看登录页
    page.screenshot(path="cache/ota_monitor/meituan_login_01.png")
    print("截图: meituan_login_01.png")
    
    # 找手机号输入框
    phone_input = None
    for sel in ['input[type="tel"]', 'input[type="number"]', 'input[name="phone"]', 
                'input[name="mobile"]', 'input[placeholder*="手机"]', 'input[placeholder*="账号"]',
                'input[class*="phone"]', 'input[class*="mobile"]', 'input']:
        try:
            els = page.query_selector_all(sel)
            for el in els:
                if el.is_visible():
                    attrs = page.evaluate("""
                        el => {
                            const a = {};
                            for (let attr of el.attributes) {
                                a[attr.name] = attr.value;
                            }
                            return a;
                        }
                    """, el)
                    print(f"  Input: {sel} | attrs={json.dumps(attrs, ensure_ascii=False)}")
                    if not phone_input and any(k in str(attrs).lower() for k in ['phone','mobile','tel','手机','账号']):
                        phone_input = el
        except:
            pass
    
    # 如果没找到特定手机输入框，用第一个可见input
    if not phone_input:
        all_visible = page.query_selector_all('input:visible')
        if all_visible:
            phone_input = all_visible[0]
            print(f"  使用第一个可见input: {phone_input}")
    
    if phone_input:
        print(f"\n=== 输入手机号 ===")
        phone_input.click()
        page.wait_for_timeout(500)
        phone_input.fill("17760348653")
        page.wait_for_timeout(500)
        print("  已输入: 17760348653")
        
        # 截图确认
        page.screenshot(path="cache/ota_monitor/meituan_login_02_phone.png")
        print("  截图: meituan_login_02_phone.png")
        
        # 找发送验证码按钮
        btn_found = False
        for sel in ['button:has-text("获取验证码")', 'button:has-text("发送验证码")',
                    'button:has-text("验证码")', 'button:has-text("下一步")',
                    '[class*="send"]', '[class*="code"]', '[class*="sms"]',
                    'span:has-text("获取验证码")', 'span:has-text("发送")']:
            try:
                btn = page.query_selector(sel)
                if btn and btn.is_visible():
                    text = btn.inner_text()
                    print(f"  找到按钮: '{text}' via {sel}")
                    btn.click()
                    btn_found = True
                    break
            except:
                pass
        
        if btn_found:
            print("  已点击发送验证码")
            page.wait_for_timeout(2000)
            page.screenshot(path="cache/ota_monitor/meituan_login_03_code.png")
            print("  截图: meituan_login_03_code.png")
            
            # 保存状态，等待手动输入验证码
            print("\n" + "="*60)
            print("⚠️ 请查看手机短信，获取美团验证码")
            print("   验证码将发送到: 17760348653")
            print("="*60)
            
            # 保存浏览器状态以便后续恢复
            storage = context.storage_state(path="cache/ota_monitor/meituan_state.json")
            print("  浏览器状态已保存: meituan_state.json")
            
            # 保持浏览器打开，等待用户告知验证码
            print("\n  浏览器将保持打开60秒...")
            time.sleep(60)
            
        else:
            print("  ❌ 未找到发送验证码按钮")
            # 打印所有按钮
            all_btns = page.query_selector_all('button, [role="button"], span[class*="btn"]')
            print(f"  页面按钮数: {len(all_btns)}")
            for b in all_btns[:10]:
                try:
                    print(f"    {b.inner_text()[:50]}")
                except:
                    pass
    else:
        print("  ❌ 未找到输入框")
        # 保存页面源码分析
        with open("cache/ota_monitor/meituan_login_page.html", "w", encoding="utf-8") as f:
            f.write(page.content())
        print("  页面源码已保存")
    
    browser.close()
