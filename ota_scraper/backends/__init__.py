# -*- coding: utf-8 -*-
"""
OTA-Scraper 抓取后端层
四层策略: Scrapling(Stealth) → Playwright → ScraplingCLI → DirectHTTP
"""
from __future__ import annotations
import asyncio
import concurrent.futures
import json
import os
import random
import time
import hashlib
import subprocess
import tempfile
import urllib.request
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

from ..core import ScrapeStatus, BackendType, ScrapeAttempt


# ──────────────────────────────────────────────
# 工具函数
# ──────────────────────────────────────────────
def _safe_async_run(coro, timeout: int = 30):
    """安全地运行异步协程，自动处理已有事件循环的情况"""
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = None

    if loop is not None:
        # 已有事件循环，在新线程中运行
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(lambda: asyncio.run(coro))
            return future.result(timeout=timeout + 10)
    else:
        return asyncio.run(coro)


# ──────────────────────────────────────────────
# 缓存管理
# ──────────────────────────────────────────────
class CacheManager:
    """简单的文件缓存，避免重复请求"""
    def __init__(self, cache_dir: str = None):
        if cache_dir is None:
            cache_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cache")
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def _key(self, url: str) -> str:
        return hashlib.md5(url.encode()).hexdigest()[:16]

    def get(self, url: str, max_age_seconds: int = 300) -> Optional[str]:
        key = self._key(url)
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        if not os.path.exists(cache_file):
            return None
        age = time.time() - os.path.getmtime(cache_file)
        if age > max_age_seconds:
            return None
        with open(cache_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get("content", "")

    def set(self, url: str, content: str):
        key = self._key(url)
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump({"url": url, "content": content, "ts": time.time()}, f, ensure_ascii=False)


# ──────────────────────────────────────────────
# User-Agent 池
# ──────────────────────────────────────────────
UA_POOL = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.2 Safari/605.1.15",
]

def random_ua() -> str:
    return random.choice(UA_POOL)


# ──────────────────────────────────────────────
# 抽象后端基类
# ──────────────────────────────────────────────
@dataclass
class BackendResponse:
    content: str
    status_code: int = 200
    headers: dict = field(default_factory=dict)
    url: str = ""
    duration_ms: float = 0

class BaseBackend(ABC):
    """所有抓取后端的抽象基类"""
    name: str = "base"
    backend_type: BackendType = BackendType.DIRECT

    def __init__(self, cache: CacheManager = None, timeout: int = 30):
        self.cache = cache or CacheManager()
        self.timeout = timeout

    @abstractmethod
    def fetch(self, url: str, **kwargs) -> BackendResponse:
        ...

    @abstractmethod
    async def fetch_async(self, url: str, **kwargs) -> BackendResponse:
        ...

    def can_handle(self, url: str, platform_profile: dict = None) -> bool:
        return True


# ──────────────────────────────────────────────
# 1. Scrapling Stealth 后端 (主力)
# ──────────────────────────────────────────────
class ScraplingBackend(BaseBackend):
    """
    使用 Scrapling 库的 StealthyFetcher
    - 绕过 Cloudflare/WAF
    - 浏览器指纹伪装
    - JS渲染
    
    Stealth模式使用同步Playwright API，必须在同步上下文中调用
    """
    name = "scrapling"
    backend_type = BackendType.SCRAPLING

    def fetch(self, url: str, **kwargs) -> BackendResponse:
        t0 = time.time()
        try:
            from scrapling.fetchers import StealthyFetcher, Fetcher

            use_stealth = kwargs.get("stealth", True)
            css_selector = kwargs.get("css_selector", "")
            card_selectors = kwargs.get("card_selectors", {})  # {name_sel, price_sel, score_sel, ...}
            wait_time = kwargs.get("wait_ms", 3000)
            solve_cf = kwargs.get("solve_cloudflare", False)

            if use_stealth:
                def _stealth_fetch():
                    return StealthyFetcher.fetch(
                        url, google_search=False, headless=True,
                        solve_cloudflare=solve_cf, wait=wait_time)

                try:
                    loop = asyncio.get_running_loop()
                except RuntimeError:
                    loop = None

                if loop is not None:
                    with concurrent.futures.ThreadPoolExecutor() as ex:
                        page = ex.submit(_stealth_fetch).result(timeout=self.timeout + 10)
                else:
                    page = _stealth_fetch()

                if css_selector:
                    content = self._extract_cards(page, css_selector, card_selectors)
                else:
                    content = page.get_all_text()
            else:
                f = Fetcher()
                resp = f.get(url, stealthy_headers=True,
                           headers={"User-Agent": random_ua(), **kwargs.get("headers", {})})
                if css_selector:
                    content = self._extract_cards(resp, css_selector, card_selectors)
                else:
                    content = resp.get_all_text()

            duration_ms = (time.time() - t0) * 1000
            return BackendResponse(content=content, status_code=200, url=url, duration_ms=duration_ms)

        except Exception as e:
            duration_ms = (time.time() - t0) * 1000
            raise RuntimeError(f"ScraplingBackend error: {e}")

    def _extract_cards(self, page, list_selector: str, field_selectors: dict) -> str:
        """
        用CSS选择器提取结构化酒店卡片
        自适配: 配置选择器0命中时自动扫描候选
        """
        cards = page.css(list_selector)
        
        # 自适配回退: 配置选择器不命中，尝试扫描
        if (not cards or len(cards) == 0) and list_selector:
            try:
                from ..adaptive import adaptive_select
                alt_sel, alt_count = adaptive_select(page, "hotel_list")
                if alt_sel and alt_count > 0:
                    cards = page.css(alt_sel)
            except:
                pass
        
        if not cards or len(cards) == 0:
            return page.get_all_text()

        # 从script JSON提取元数据 (携程: hotelName→star)
        script_meta = self._extract_script_meta(page)

        parts = []
        for card in cards[:30]:
            fields = []
            for field_name, selector in field_selectors.items():
                if not selector:
                    continue
                try:
                    elements = card.css(selector)
                    if elements:
                        value = elements[0].get_all_text().strip()
                        value = " ".join(value.split())
                        if value:
                            fields.append(f"{field_name}: {value}")
                except:
                    pass

            # 注入script JSON元数据 (星级等)
            if script_meta and fields:
                card_text = "\n".join(fields)
                # 找hotel name匹配
                for meta in script_meta:
                    hname = meta.get("hotelName", "")
                    if hname and hname in card_text:
                        star = meta.get("star")
                        if star is not None:
                            fields.append(f"stars: {star}星")
                        hid = meta.get("hotelId")
                        if hid:
                            fields.append(f"hotel_id: {hid}")
                        break

            if fields:
                parts.append("===HOTEL_CARD===\n" + "\n".join(fields) + "\n===END_CARD===")

        if not parts:
            # 如果选择器没匹配到字段，回退到卡片全文
            for card in cards[:30]:
                text = card.get_all_text()
                if text.strip():
                    parts.append("===HOTEL_CARD===\n" + text.strip()[:500] + "\n===END_CARD===")

        return "\n".join(parts)

    async def fetch_async(self, url: str, **kwargs) -> BackendResponse:
        """异步版本：在executor中运行同步fetch"""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: self.fetch(url, **kwargs))

    @staticmethod
    def _extract_script_meta(page) -> list:
        """从页面script标签中提取JSON元数据 (酒店名→星级映射)"""
        import json as _json
        meta_list = []
        try:
            html = page.html_content if hasattr(page, 'html_content') else page.get_all_text()
            import re as _re
            # 找包含hotelName的JSON块
            blocks = _re.findall(r'\{[^{}]*"hotelName"[^{}]*\}', html)
            for block in blocks:
                try:
                    data = _json.loads(block)
                    if data.get('hotelName'):
                        meta_list.append(data)
                except:
                    pass
        except:
            pass
        return meta_list


# ──────────────────────────────────────────────
# 2. Playwright 后端 (复杂交互)
# ──────────────────────────────────────────────
class PlaywrightBackend(BaseBackend):
    """
    Playwright 浏览器后端
    - 完整浏览器环境
    - 支持登录态
    - 支持复杂交互(翻页/点击/滚动)
    """
    name = "playwright"
    backend_type = BackendType.PLAYWRIGHT

    def fetch(self, url: str, **kwargs) -> BackendResponse:
        return _safe_async_run(self.fetch_async(url, **kwargs), self.timeout)

    async def fetch_async(self, url: str, **kwargs) -> BackendResponse:
        t0 = time.time()
        try:
            from playwright.async_api import async_playwright

            wait_ms = kwargs.get("wait_ms", 5000)
            scroll = kwargs.get("scroll", True)
            css_selector = kwargs.get("css_selector", "")
            wait_selector = kwargs.get("wait_selector", "")
            cookies = kwargs.get("cookies", [])
            geolocation = kwargs.get("geolocation", None)

            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=True,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--disable-web-security',
                        '--no-sandbox',
                        '--lang=zh-CN',
                    ]
                )

                context_options = {
                    "locale": kwargs.get("locale", "zh-CN"),
                    "user_agent": kwargs.get("user_agent", random_ua()),
                }
                if geolocation:
                    context_options["geolocation"] = geolocation
                    context_options["permissions"] = ["geolocation"]

                context = await browser.new_context(**context_options)
                if cookies:
                    await context.add_cookies(cookies)

                page = await context.new_page()

                await page.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                    Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                    Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh', 'en']});
                """)

                await page.goto(url, timeout=30000, wait_until="domcontentloaded")

                if wait_selector:
                    try:
                        await page.wait_for_selector(wait_selector, timeout=wait_ms)
                    except:
                        pass
                await page.wait_for_timeout(min(wait_ms, 5000))

                if scroll:
                    try:
                        await page.evaluate("window.scrollTo(0, document.body.scrollHeight/3)")
                        await page.wait_for_timeout(1000)
                        await page.evaluate("window.scrollTo(0, document.body.scrollHeight*2/3)")
                        await page.wait_for_timeout(1000)
                        await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                        await page.wait_for_timeout(1500)
                    except:
                        pass

                if css_selector:
                    elements = await page.query_selector_all(css_selector)
                    texts = []
                    for el in elements:
                        try:
                            texts.append(await el.inner_text())
                        except:
                            pass
                    content = "\n---\n".join(texts)
                else:
                    content = await page.inner_text("body")

                await browser.close()

            duration_ms = (time.time() - t0) * 1000
            return BackendResponse(content=content, status_code=200, url=url, duration_ms=duration_ms)

        except ImportError:
            raise RuntimeError("Playwright not installed. Run: playwright install chromium")
        except Exception as e:
            duration_ms = (time.time() - t0) * 1000
            raise RuntimeError(f"PlaywrightBackend error: {e}")


# ──────────────────────────────────────────────
# 3. 直接HTTP后端 (speed first)
# ──────────────────────────────────────────────
class DirectHTTPBackend(BaseBackend):
    """
    直接HTTP请求 - 速度最快
    适合: 静态页面、RSS、简单API
    """
    name = "direct"
    backend_type = BackendType.DIRECT

    def fetch(self, url: str, **kwargs) -> BackendResponse:
        t0 = time.time()
        try:
            req = urllib.request.Request(url)
            req.add_header("User-Agent", kwargs.get("user_agent", random_ua()))
            req.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
            req.add_header("Accept-Language", kwargs.get("accept_language", "zh-CN,zh;q=0.9,en;q=0.8"))

            for k, v in kwargs.get("headers", {}).items():
                req.add_header(k, v)

            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                content = resp.read().decode("utf-8", errors="replace")
                status = resp.status

            duration_ms = (time.time() - t0) * 1000
            return BackendResponse(content=content, status_code=status, url=url, duration_ms=duration_ms)

        except Exception as e:
            duration_ms = (time.time() - t0) * 1000
            raise RuntimeError(f"DirectHTTPBackend error: {e}")

    async def fetch_async(self, url: str, **kwargs) -> BackendResponse:
        return self.fetch(url, **kwargs)


# ──────────────────────────────────────────────
# 4. Scrapling CLI 后端 (备用)
# ──────────────────────────────────────────────
class ScraplingCLIBackend(BaseBackend):
    """
    通过 scrapling CLI 命令行调用
    - 独立进程，隔离性好
    - 支持 stealthy-fetch 的完整功能
    """
    name = "scrapling_cli"
    backend_type = BackendType.SCRAPLING

    def fetch(self, url: str, **kwargs) -> BackendResponse:
        t0 = time.time()
        try:
            output_file = tempfile.mktemp(suffix=".txt")
            use_stealth = kwargs.get("stealth", True)
            css_selector = kwargs.get("css_selector", "")

            if use_stealth:
                cmd = ["scrapling", "extract", "stealthy-fetch", url, output_file,
                       "--headless", "--wait", str(kwargs.get("wait_ms", 3000))]
                if kwargs.get("solve_cloudflare"):
                    cmd.append("--solve-cloudflare")
            else:
                cmd = ["scrapling", "extract", "get", url, output_file]

            if css_selector:
                cmd.extend(["-s", css_selector])

            result = subprocess.run(cmd, capture_output=True, timeout=self.timeout + 10,
                                   text=True, errors="replace")

            content = ""
            if os.path.exists(output_file):
                with open(output_file, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                os.unlink(output_file)

            duration_ms = (time.time() - t0) * 1000
            return BackendResponse(content=content, status_code=200, url=url, duration_ms=duration_ms)

        except subprocess.TimeoutExpired:
            raise RuntimeError("ScraplingCLI timed out")
        except Exception as e:
            raise RuntimeError(f"ScraplingCLIBackend error: {e}")

    async def fetch_async(self, url: str, **kwargs) -> BackendResponse:
        return self.fetch(url, **kwargs)


# ──────────────────────────────────────────────
# 后端工厂
# ──────────────────────────────────────────────
def create_backends(cache: CacheManager = None) -> dict:
    """创建所有可用后端"""
    backends = {
        "direct": DirectHTTPBackend(cache=cache),
        "scrapling_cli": ScraplingCLIBackend(cache=cache),
    }

    # Scrapling Python API - 检查可用性
    try:
        from scrapling.fetchers import StealthyFetcher
        backends["scrapling"] = ScraplingBackend(cache=cache)
    except Exception:
        pass

    # Playwright - 检查可用性
    try:
        from playwright.async_api import async_playwright
        backends["playwright"] = PlaywrightBackend(cache=cache)
    except Exception:
        pass

    return backends
