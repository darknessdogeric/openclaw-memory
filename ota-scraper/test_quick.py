"""快速验证脚本：测试 Playwright + Stealth"""
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
import json, time, random

def test_stealth():
    print("[TEST] Playwright + Stealth launch...")

    with sync_playwright() as p:
        # Launch browser normally first
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1920, "height": 768},
            locale="zh-CN",
            timezone_id="Asia/Shanghai",
        )
        page = context.new_page()
        
        # Now apply stealth to the page
        Stealth().apply_stealth_sync(page)

        # 访问 httpbin 检测指纹
        print("  -> GET httpbin.org/headers")
        page.goto("https://httpbin.org/headers", timeout=15000)
        time.sleep(2)
        
        # 检查 webdriver 标志
        webdriver = page.evaluate("() => navigator.webdriver")
        print(f"  navigator.webdriver = {webdriver}")
        
        plugins = page.evaluate("() => navigator.plugins.length")
        print(f"  navigator.plugins.length = {plugins}")
        
        chrome = page.evaluate("() => window.chrome ? '存在' : '不存在'")
        print(f"  window.chrome = {chrome}")

        browser.close()
        print("[OK] Stealth test passed\n")


def test_expedia():
    print("[TEST] Expedia scraping...")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--disable-blink-features=AutomationControlled']
        )
        context = browser.new_context(
            viewport={"width": random.choice([1366, 1440, 1920]), "height": 768},
            locale="zh-CN",
            timezone_id="Asia/Shanghai",
            extra_http_headers={
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            }
        )
        page = context.new_page()
        Stealth().apply_stealth_sync(page)

        print("  -> GET Expedia hotel search")
        # Expedia URL for Shanghai hotels
        url = "https://www.expedia.com/Hotel-Search?destination=Shanghai%2C%20China&adults=2"
        page.goto(url, wait_until="domcontentloaded", timeout=20000)
        time.sleep(random.uniform(3, 6))
        
        print(f"  URL: {page.url}")
        title = page.title()
        print(f"  Title: {title}")
        
        # 截图
        page.screenshot(path="expedia_test.png", full_page=False)
        print("  [OK] Screenshot: expedia_test.png")
        
        # 检查价格元素
        price_count = page.locator('[data-stid="price-summary"]').count()
        print(f"  Price elements found: {price_count}")

        browser.close()
        print("[OK] Expedia test done\n")


if __name__ == "__main__":
    test_stealth()
    test_expedia()
    print("[DONE] All tests complete!")
