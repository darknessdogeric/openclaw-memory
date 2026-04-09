"""
OTA 价格抓取器 - Playwright + Stealth + 多模态大模型
适用平台：携程/美团/去哪儿/飞猪/Expedia/Agoda/Booking 等
"""

import asyncio
import base64
import json
import random
import time
import os
import re
from datetime import datetime

from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth
from fake_useragent import UserAgent

# ============ 配置区 ============
CONFIG = {
    "openai_api_key": os.environ.get("OPENAI_API_KEY", ""),
    "model": "gpt-4o",  # 或 "gpt-4o-mini" 更便宜
    "request_delay": (10, 30),  # 每次请求间隔（秒）
    "viewport_widths": [1366, 1440, 1920],
    "viewport_height": 768,
    "locale": "zh-CN",
    "timezone": "Asia/Shanghai",
}

# ============ 平台配置 ============
PLATFORMS = {
    "expedia": {
        "url": "https://www.expedia.com/Hotel-Search",
        "search_selector": 'input[id="destination"]',
        "submit_selector": 'button[id="search-button"]',
        "price_selector": '[data-stid="price-summary"]',
        "difficulty": "easy",
    },
    "agoda": {
        "url": "https://www.agoda.com",
        "search_selector": 'input[id="search-input"]',
        "submit_selector": 'button[type="submit"]',
        "price_selector": '.PriceLink',
        "difficulty": "easy",
    },
    "booking": {
        "url": "https://www.booking.com",
        "search_selector": 'input[name="ss"]',
        "submit_selector": 'button[type="submit"]',
        "price_selector": '[data-testid="price-and-discounted-price"]',
        "difficulty": "easy",
    },
    "hotels": {
        "url": "https://www.hotels.com",
        "search_selector": 'input[id="q-destination"]',
        "submit_selector": 'button[id="q-submit"]',
        "price_selector": '.uitk-type-500',
        "difficulty": "easy",
    },
    # 以下待破解
    "ctrip": {
        "url": "https://hotels.ctrip.com",
        "difficulty": "hard",
        "note": "类名随机混淆，需大模型视觉兜底"
    },
    "meituan": {
        "url": "https://hotel.meituan.com",
        "difficulty": "extreme",
        "note": "WASM加密+设备指纹，需住宅IP"
    },
    "qunar": {
        "url": "https://hotel.qunar.com",
        "difficulty": "medium",
    },
    "fliggy": {
        "url": "https://hotel.fliggy.com",
        "difficulty": "medium",
    },
}


class OTAPriceScraper:
    def __init__(self, api_key: str = ""):
        self.ua = UserAgent()
        self.api_key = api_key
        self.client = None
        if self.api_key:
            try:
                from openai import OpenAI
                self.client = OpenAI(api_key=self.api_key)
            except Exception as e:
                print(f"⚠️ OpenAI 客户端初始化失败: {e}")

    # ---- 浏览器初始化 ----
    def init_browser(self, stealth: bool = True):
        pw = sync_playwright().start()
        
        if stealth:
            s = Stealth().use_sync(pw)
            browser = s.chromium.launch(
                headless=True,
                args=['--disable-blink-features=AutomationControlled']
            )
        else:
            browser = pw.chromium.launch(headless=True)

        context = browser.new_context(
            user_agent=self.ua.random,
            viewport={"width": random.choice(CONFIG["viewport_widths"]), "height": CONFIG["viewport_height"]},
            locale=CONFIG["locale"],
            timezone_id=CONFIG["timezone"],
            extra_http_headers={
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
            }
        )

        # 反检测脚本
        context.set_extra_http_headers({
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        })

        page = context.new_page()
        return pw, browser, page

    # ---- 价格提取（DOM方式）----
    def extract_price_dom(self, page, selector: str):
        try:
            page.wait_for_selector(selector, timeout=5000)
            elements = page.locator(selector).all()
            prices = []
            for el in elements:
                text = el.text_content()
                if text:
                    price = self._parse_price(text)
                    if price:
                        prices.append(price)
            return prices if prices else None
        except:
            return None

    # ---- 价格提取（视觉方式，大模型兜底）----
    def extract_price_vision(self, page, selector: str = None) -> dict:
        if not self.client:
            return {"error": "未配置 OpenAI API Key"}

        # 截取价格区域
        if selector:
            try:
                el = page.locator(selector).first
                screenshot = el.screenshot()
            except:
                screenshot = page.screenshot()
        else:
            screenshot = page.screenshot()

        b64_img = base64.b64encode(screenshot).decode()

        prompt = """从这张酒店页面截图中提取房价信息，返回JSON格式：
{
  "prices": [
    {"price": 数字, "currency": "CNY/USD/EUR", "room_type": "房型名称"},
    ...
  ],
  "hotel_name": "酒店名称（如果有）"
}
只返回JSON，不要其他文字。"""

        try:
            response = self.client.chat.completions.create(
                model=CONFIG["model"],
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_img}"}}
                    ]
                }]
            )
            content = response.choices[0].message.content
            # 提取JSON
            match = re.search(r'\{.*\}', content, re.DOTALL)
            if match:
                return json.loads(match.group())
            return {"raw": content}
        except Exception as e:
            return {"error": str(e)}

    # ---- 搜索酒店 ----
    def search_hotel(self, page, platform: str, hotel_name: str, city: str = ""):
        p = PLATFORMS.get(platform)
        if not p:
            return {"error": f"未知平台: {platform}"}

        url = p.get("url", "")
        print(f"  🌐 访问 {platform}: {url}")

        try:
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
            time.sleep(random.uniform(2, 4))
        except Exception as e:
            return {"error": f"页面加载失败: {e}"}

        # 如果有搜索框，执行搜索
        search_sel = p.get("search_selector")
        submit_sel = p.get("submit_selector")
        if search_sel and submit_sel:
            try:
                page.fill(search_sel, f"{city} {hotel_name}" if city else hotel_name)
                page.click(submit_sel)
                page.wait_for_load_state("networkidle", timeout=10000)
                time.sleep(random.uniform(2, 5))
            except Exception as e:
                print(f"  ⚠️ 搜索失败: {e}")

        return {"status": "ok", "url": page.url}

    # ---- 解析价格文本 ----
    def _parse_price(self, text: str) -> float:
        # 匹配各种货币格式
        patterns = [
            r'¥\s*([\d,]+)',      # 人民币
            r'\$\s*([\d,]+)',      # 美元
            r'€\s*([\d,]+)',       # 欧元
            r'([\d,]+)\s*元',     # 元
        ]
        for p in patterns:
            m = re.search(p, text)
            if m:
                return float(m.group(1).replace(",", ""))
        return 0.0

    # ---- 抓取单个平台 ----
    def scrape_one(self, platform: str, hotel_name: str, city: str = "") -> dict:
        pw, browser, page = self.init_browser()

        try:
            # 搜索
            result = self.search_hotel(page, platform, hotel_name, city)
            if result.get("error"):
                return result

            p = PLATFORMS[platform]
            price_sel = p.get("price_selector")

            # DOM提取
            prices_dom = None
            if price_sel:
                prices_dom = self.extract_price_dom(page, price_sel)

            # 视觉提取（兜底）
            prices_vision = self.extract_price_vision(page, price_sel)

            return {
                "platform": platform,
                "hotel": hotel_name,
                "city": city,
                "timestamp": datetime.now().isoformat(),
                "url": page.url,
                "prices_dom": prices_dom,
                "prices_vision": prices_vision,
                "difficulty": p.get("difficulty", "unknown"),
            }
        finally:
            browser.close()
            pw.stop()

    # ---- 抓取所有平台 ----
    def scrape_all(self, hotel_name: str, city: str = "", platforms: list = None) -> dict:
        if platforms is None:
            platforms = [k for k, v in PLATFORMS.items() if v.get("difficulty") == "easy"]

        results = {}
        for platform in platforms:
            print(f"\n📡 正在抓取: {platform} ({PLATFORMS[platform].get('difficulty', '?')})")
            try:
                result = self.scrape_one(platform, hotel_name, city)
                results[platform] = result
            except Exception as e:
                results[platform] = {"error": str(e)}

            # 频率控制
            delay = random.uniform(*CONFIG["request_delay"])
            print(f"  ⏱ 等待 {delay:.1f} 秒...")
            time.sleep(delay)

        return results


# ============ 主程序 ============
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("用法: python ota_scraper.py <酒店名称> [城市]")
        print("示例: python ota_scraper.py 北京王府半岛酒店 北京")
        sys.exit(0)

    hotel = sys.argv[1]
    city = sys.argv[2] if len(sys.argv) > 2 else ""

    print(f"🔍 开始抓取: {city} {hotel}")
    print(f"⏰ 时间: {datetime.now().isoformat()}")

    scraper = OTAPriceScraper(api_key=CONFIG["openai_api_key"])
    
    # 先用简单平台测试
    test_platforms = ["expedia", "agoda", "booking", "hotels"]
    results = scraper.scrape_all(hotel, city, platforms=test_platforms)

    # 保存结果
    output_file = f"ota_results_{hotel}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 结果已保存: {output_file}")
    print(json.dumps(results, ensure_ascii=False, indent=2))
