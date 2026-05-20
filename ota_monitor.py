# -*- coding: utf-8 -*-
"""
Multi-OTA 酒店数据监控 — 第一批4平台
========================================
美团 | 去哪儿 | 飞猪 | 猫途鹰

架构：
  - BasePlatformAdapter: 抽象基类，定义统一采集接口
  - 每个平台一个 Adapter，封装平台特有的反爬策略和 HTML 解析
  - OTAMonitor: 编排器，负责批量采集、重试、结果汇总

依赖：
  - scrap_tools.py (scrapling) — 用于猫途鹰等静态友好平台
  - Playwright + playwright-stealth — 用于美团/去哪儿/飞猪等强反爬平台

Obscura 预留接口，待环境部署后启用。
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
import hashlib
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone, timedelta
from typing import Optional
from enum import Enum

# ──────────────────────────────────────────────
# 0. 路径与常量
# ──────────────────────────────────────────────
_WORKSPACE = os.path.dirname(os.path.abspath(__file__))
_SCRAPE_TOOLS = os.path.join(_WORKSPACE, "scrap_tools.py")
_OBSCURA_BIN = os.path.join(_WORKSPACE, "toolbox", "obscura", "obscura.exe")

# 缓存目录
_CACHE_DIR = os.path.join(_WORKSPACE, "cache", "ota_monitor")
os.makedirs(_CACHE_DIR, exist_ok=True)

# 北京时间
CN_TZ = timezone(timedelta(hours=8))


# ──────────────────────────────────────────────
# 1. 统一数据模型
# ──────────────────────────────────────────────
class Platform(str, Enum):
    MEITUAN = "meituan"
    QUNAR = "qunar"
    FLIGGY = "fliggy"
    TRIPADVISOR = "tripadvisor"
    CTRIP = "ctrip"  # 预留第二批


class ScrapeStatus(str, Enum):
    SUCCESS = "success"
    PARTIAL = "partial"
    FAILED = "failed"
    BLOCKED = "blocked"  # 被反爬拦截
    NOT_IMPLEMENTED = "not_implemented"


@dataclass
class HotelRecord:
    """统一酒店数据记录"""
    platform: str                    # meituan|qunar|fliggy|tripadvisor|ctrip
    hotel_name: str                  # 酒店名称
    price_min: Optional[float] = None   # 最低价 (CNY)
    price_max: Optional[float] = None   # 最高价 (CNY)
    rating: Optional[float] = None      # 评分 (0-5)
    review_count: Optional[int] = None  # 评论数
    room_available: bool = True         # 是否有房
    scraped_at: str = ""               # ISO 8601 timestamp
    url: str = ""                       # 来源URL
    raw_data: dict = field(default_factory=dict)  # 平台特有原始数据

    def __post_init__(self):
        if not self.scraped_at:
            self.scraped_at = datetime.now(CN_TZ).isoformat()


@dataclass
class ScrapeResult:
    """单次采集结果"""
    platform: str
    status: ScrapeStatus
    hotels: list[HotelRecord] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    tool_used: str = ""
    elapsed_ms: int = 0
    url: str = ""


# ──────────────────────────────────────────────
# 2. 抽象基类
# ──────────────────────────────────────────────
class BasePlatformAdapter(ABC):
    """平台采集适配器基类"""

    platform: str = "base"
    name: str = "Base"

    @abstractmethod
    def scrape(self, city: str, **kwargs) -> ScrapeResult:
        """采集指定城市的酒店数据"""
        ...

    def is_available(self) -> bool:
        """检查工具链是否可用"""
        return True

    def get_health(self) -> dict:
        """健康检查"""
        return {
            "platform": self.platform,
            "name": self.name,
            "available": self.is_available(),
        }


# ──────────────────────────────────────────────
# 3. 猫途鹰适配器 (scrap_tools static)
# ──────────────────────────────────────────────
class TripAdvisorAdapter(BasePlatformAdapter):
    """
    猫途鹰 (tripadvisor.cn)
    策略: scrap_tools.py 静态抓取（scrapling Fetcher）
    特点: HTML直接包含酒店列表数据，反爬最弱
    """

    platform = "tripadvisor"
    name = "TripAdvisor (scrapling)"

    # 城市 → geocode 映射（已验证）
    # 获取方法: 在 tripadvisor.cn 搜索城市名 → 从结果URL提取 g{数字}
    # 或 Bing搜索: site:tripadvisor.cn {城市名} 酒店
    CITY_GEOCODE = {
        "襄阳": "g494931",     # ✅ 已验证 (2026-05-12)
        "武汉": "g297437",
        "北京": "g294212",
        "上海": "g308272",
        "广州": "g298555",
        "深圳": "g297415",
        "成都": "g297463",
        "杭州": "g298559",
        "南京": "g294220",
        "重庆": "g294213",
    }

    def is_available(self) -> bool:
        return os.path.exists(_SCRAPE_TOOLS)

    def _get_hotel_url(self, city: str) -> str:
        geocode = self.CITY_GEOCODE.get(city)
        if geocode:
            return f"https://www.tripadvisor.cn/Hotels-{geocode}-Hotels.html"
        # Fallback: 搜索
        from urllib.parse import quote
        return f"https://www.tripadvisor.cn/Search?q={quote(city)}&type=HOTELS"

    def scrape(self, city: str = "襄阳", **kwargs) -> ScrapeResult:
        url = self._get_hotel_url(city)
        t0 = time.time()

        try:
            # 直接导入 fetch_static，避免 subprocess 只能捕获 print 输出
            sys.path.insert(0, os.path.dirname(_SCRAPE_TOOLS))
            from scrap_tools import fetch_static
            html = fetch_static(url)
        except FileNotFoundError:
            return ScrapeResult(
                platform=self.platform,
                status=ScrapeStatus.FAILED,
                errors=["scrap_tools.py not found"],
                url=url,
                elapsed_ms=int((time.time() - t0) * 1000)
            )
        except ImportError as e:
            return ScrapeResult(
                platform=self.platform,
                status=ScrapeStatus.FAILED,
                errors=[f"Import error: {e}"],
                url=url,
                elapsed_ms=int((time.time() - t0) * 1000)
            )
        except Exception as e:
            return ScrapeResult(
                platform=self.platform,
                status=ScrapeStatus.FAILED,
                errors=[str(e)],
                url=url,
                elapsed_ms=int((time.time() - t0) * 1000)
            )

        elapsed_ms = int((time.time() - t0) * 1000)

        # 检查是否被拦截
        if "403" in html[:100] and "Forbidden" in html[:200]:
            return ScrapeResult(
                platform=self.platform,
                status=ScrapeStatus.BLOCKED,
                errors=["403 Forbidden"],
                url=url,
                tool_used="scrap_tools",
                elapsed_ms=elapsed_ms
            )

        # 解析酒店数据
        hotels = self._parse_hotel_list(html, url, city)

        if hotels:
            return ScrapeResult(
                platform=self.platform,
                status=ScrapeStatus.SUCCESS,
                hotels=hotels,
                url=url,
                tool_used="scrap_tools",
                elapsed_ms=elapsed_ms
            )
        else:
            return ScrapeResult(
                platform=self.platform,
                status=ScrapeStatus.PARTIAL,
                hotels=[],
                errors=["no hotels parsed"],
                url=url,
                tool_used="scrap_tools",
                elapsed_ms=elapsed_ms
            )

    def _parse_hotel_list(self, html: str, url: str, city: str) -> list[HotelRecord]:
        """解析猫途鹰酒店列表页"""
        hotels = []

        # 提取价格范围
        price_range_match = re.search(
            r'每日平均价格[：:]\s*[¥￥]\s*([\d,]+)\s*[-–—]\s*[¥￥]\s*([\d,]+)',
            html
        )
        city_price_min = None
        city_price_max = None
        if price_range_match:
            city_price_min = float(price_range_match.group(1).replace(",", ""))
            city_price_max = float(price_range_match.group(2).replace(",", ""))

        # 按"我们比较 N 家网站的优惠价格"分块
        hotel_blocks = re.split(
            r'我们比较\s*\d+\s*家网站的优惠价格',
            html
        )

        # 处理第一个块（包含排名第一的酒店，在所有"我们比较"之前）
        # 第一个块包含排名前N的酒店
        all_text = html
        
        # 提取酒店名+点评+排名的模式
        # 模式: 酒店名(含酒店/宾馆等关键词) 后跟 \d+ 条点评 和/或 排名第 \d+
        # 使用更宽松的匹配
        seen_names = set()
        
        # 方案：从每个block中提取
        for block in hotel_blocks:
            lines = [l.strip() for l in block.split('\n') if l.strip()]
            hotel_name = ""
            review_count = 0
            rank = 0
            
            for j, line in enumerate(lines):
                # 匹配酒店名：包含"酒店/宾馆/民宿/度假村"等的行
                # 跳过非酒店行：标题/导航/统计行
                if not hotel_name and re.search(r'(?:酒店|宾馆|民宿|度假村|客栈|饭店|大厦|山庄|旅社|公寓|套房|旅馆|青旅)', line):
                    candidate = line.strip()
                    # 跳过明显非酒店名的行
                    skip_keywords = [
                        '酒店钻级', '酒店风格', '酒店类型', '品牌', '筛选',
                        '重置', '重设', '住宿', '地图', '低价', '版权所有',
                        '使用条款', '隐私政策', '网站工作', '预订', '日期',
                        '入住', '退房', '顾客', '客房', '成人', '儿童',
                        '猫途鹰', 'Tripadvisor', '排名第', '的酒店(', '酒店预订',
                        '酒店价格', '酒店_', '住宿 -', '酒店和住宿',
                    ]
                    # Also skip bare labels like "XX市酒店" (no brand name)
                    is_bare_label = bool(re.match(r'^.{2,6}(?:市|县)(?:酒店|宾馆|住宿)$', candidate))
                    # Skip hotel type labels (categories, not names)
                    is_type_label = candidate in [
                        '酒店', '宾馆', '民宿', '旅馆', '汽车旅馆', '度假村',
                        '精品酒店', '公寓', '客栈', '青旅', '度假酒店',
                    ]
                    if (candidate not in seen_names 
                            and 4 <= len(candidate) <= 80
                            and not is_bare_label
                            and not is_type_label
                            and not any(kw in candidate for kw in skip_keywords)):
                        hotel_name = candidate
                
                # 匹配点评数（仅当已找到酒店名）
                if hotel_name:
                    review_match = re.search(r'([\d,]+)\s*条点评', line)
                    if review_match:
                        review_count = int(review_match.group(1).replace(',', ''))
                    
                    # 匹配排名
                    rank_match = re.search(r'排名第\s*(\d+)', line)
                    if rank_match:
                        rank = int(rank_match.group(1))
            
            if hotel_name:
                seen_names.add(hotel_name)
                record = HotelRecord(
                    platform=self.platform,
                    hotel_name=hotel_name,
                    price_min=city_price_min,
                    price_max=city_price_max,
                    rating=None,
                    review_count=review_count,
                    room_available=True,
                    url=url,
                    raw_data={
                        "rank": rank if rank > 0 else None,
                        "city": city,
                    }
                )
                hotels.append(record)

        return hotels


# ──────────────────────────────────────────────
# 4. 美团适配器 (Playwright + stealth)
# ──────────────────────────────────────────────
class MeituanAdapter(BasePlatformAdapter):
    """
    美团酒店 (hotel.meituan.com)
    策略: Playwright Chromium + playwright-stealth 反检测
    特点: 反爬最强，403 拦截严格，需模拟正常浏览器
    """

    platform = "meituan"
    name = "Meituan (Playwright+stealth)"

    SEARCH_URL = "https://hotel.meituan.com/search"

    def is_available(self) -> bool:
        try:
            from playwright.sync_api import sync_playwright
            from playwright_stealth import Stealth
            return True
        except ImportError:
            return False

    def scrape(self, city: str = "襄阳", **kwargs) -> ScrapeResult:
        url = f"{self.SEARCH_URL}?city={city}"
        t0 = time.time()

        try:
            from playwright.sync_api import sync_playwright
            from playwright_stealth import Stealth
        except ImportError as e:
            return ScrapeResult(
                platform=self.platform,
                status=ScrapeStatus.NOT_IMPLEMENTED,
                errors=[f"Missing dependency: {e}"],
                url=url,
                elapsed_ms=int((time.time() - t0) * 1000)
            )

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--no-sandbox',
                        '--disable-dev-shm-usage',
                    ]
                )
                page = browser.new_page()

                # 应用反检测
                Stealth().apply_stealth_sync(page)

                # 中文环境
                page.set_extra_http_headers({
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                })

                page.goto(url, timeout=30000, wait_until='domcontentloaded')
                page.wait_for_timeout(kwargs.get('wait_ms', 8000))

                html = page.content()
                text = page.inner_text('body')

                browser.close()

                elapsed_ms = int((time.time() - t0) * 1000)

                # 检查是否被拦截
                if ('403' in text[:100] and 'Forbidden' in text[:200]) or \
                   ('验证' in text[:500] and len(text) < 500):
                    return ScrapeResult(
                        platform=self.platform,
                        status=ScrapeStatus.BLOCKED,
                        errors=["Anti-bot detection triggered"],
                        url=url,
                        tool_used="playwright+stealth",
                        elapsed_ms=elapsed_ms
                    )

                # 解析
                hotels = self._parse_hotel_list(text, html, url, city)

                if hotels:
                    return ScrapeResult(
                        platform=self.platform,
                        status=ScrapeStatus.SUCCESS,
                        hotels=hotels,
                        url=url,
                        tool_used="playwright+stealth",
                        elapsed_ms=elapsed_ms
                    )
                else:
                    return ScrapeResult(
                        platform=self.platform,
                        status=ScrapeStatus.PARTIAL,
                        hotels=[],
                        errors=["no hotels found in rendered page"],
                        url=url,
                        tool_used="playwright+stealth",
                        elapsed_ms=elapsed_ms
                    )

        except Exception as e:
            elapsed_ms = int((time.time() - t0) * 1000)
            return ScrapeResult(
                platform=self.platform,
                status=ScrapeStatus.FAILED,
                errors=[str(e)],
                url=url,
                elapsed_ms=elapsed_ms
            )

    def _parse_hotel_list(self, text: str, html: str, url: str, city: str) -> list[HotelRecord]:
        """解析美团酒店列表"""
        hotels = []

        # 美团酒店名模式: 名称中通常包含"酒店"且前面有多个汉字
        hotel_pattern = re.compile(
            r'([^\n]{4,40}?(?:酒店|宾馆|民宿|客栈|公寓|青旅|旅馆|度假))',
            re.MULTILINE
        )

        # 价格模式: ¥\d+ 或 ￥\d+
        price_pattern = re.compile(r'[¥￥]\s*(\d+)')

        # 评分模式: 评分\s*(\d+\.?\d*) 或 (\d+\.?\d*)\s*分
        rating_pattern = re.compile(r'(?:评分|点评)?\s*(\d+\.?\d*)\s*(?:分|/5)?')

        matches = hotel_pattern.findall(text)
        prices = price_pattern.findall(text)
        ratings = rating_pattern.findall(text)

        seen_names = set()

        for i, name in enumerate(matches):
            name = name.strip()
            if len(name) < 4 or name in seen_names:
                continue
            seen_names.add(name)

            price_val = None
            if i < len(prices):
                try:
                    price_val = float(prices[i])
                except ValueError:
                    pass

            rating_val = None
            # 尝试匹配该酒店附近的评分
            if ratings:
                try:
                    rating_val = float(ratings[0]) if ratings else None
                except ValueError:
                    pass

            record = HotelRecord(
                platform=self.platform,
                hotel_name=name,
                price_min=price_val,
                rating=rating_val,
                room_available=True,
                url=url,
                raw_data={"city": city},
            )
            hotels.append(record)

        return hotels


# ──────────────────────────────────────────────
# 5. 去哪儿适配器 (Playwright)
# ──────────────────────────────────────────────
class QunarAdapter(BasePlatformAdapter):
    """
    去哪儿 (hotel.qunar.com)
    策略: Playwright Chromium（JS渲染页面）
    特点: 内容完全JS动态加载，需等待 networkidle
    """

    platform = "qunar"
    name = "Qunar (Playwright)"

    CITY_URL = "https://hotel.qunar.com/city/{city_pinyin}"

    # 城市拼音映射
    CITY_PINYIN = {
        "襄阳": "xiangyang",
        "武汉": "wuhan",
        "北京": "beijing",
        "上海": "shanghai",
        "广州": "guangzhou",
        "深圳": "shenzhen",
        "成都": "chengdu",
        "杭州": "hangzhou",
    }

    def is_available(self) -> bool:
        try:
            from playwright.sync_api import sync_playwright
            return True
        except ImportError:
            return False

    def scrape(self, city: str = "襄阳", **kwargs) -> ScrapeResult:
        city_pinyin = self.CITY_PINYIN.get(city, city.lower())
        url = self.CITY_URL.format(city_pinyin=city_pinyin)
        t0 = time.time()

        try:
            from playwright.sync_api import sync_playwright
        except ImportError as e:
            return ScrapeResult(
                platform=self.platform,
                status=ScrapeStatus.NOT_IMPLEMENTED,
                errors=[f"Playwright not installed: {e}"],
                url=url,
                elapsed_ms=int((time.time() - t0) * 1000)
            )

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-dev-shm-usage']
                )
                page = browser.new_page()

                page.set_extra_http_headers({
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                })

                # 使用 networkidle 等待JS加载完成
                page.goto(url, timeout=60000, wait_until='networkidle')
                page.wait_for_timeout(kwargs.get('wait_ms', 5000))

                # 尝试滚动加载更多
                page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                page.wait_for_timeout(2000)

                text = page.inner_text('body')
                html = page.content()

                browser.close()

                elapsed_ms = int((time.time() - t0) * 1000)

                # 检查是否实际加载了内容
                if len(text) < 300:
                    return ScrapeResult(
                        platform=self.platform,
                        status=ScrapeStatus.PARTIAL,
                        hotels=[],
                        errors=[f"Page content too short ({len(text)} chars), likely JS not loaded"],
                        url=url,
                        tool_used="playwright",
                        elapsed_ms=elapsed_ms
                    )

                hotels = self._parse_hotel_list(text, html, url, city)

                if hotels:
                    return ScrapeResult(
                        platform=self.platform,
                        status=ScrapeStatus.SUCCESS,
                        hotels=hotels,
                        url=url,
                        tool_used="playwright",
                        elapsed_ms=elapsed_ms
                    )
                else:
                    return ScrapeResult(
                        platform=self.platform,
                        status=ScrapeStatus.PARTIAL,
                        hotels=[],
                        errors=["no hotels parsed"],
                        url=url,
                        tool_used="playwright",
                        elapsed_ms=elapsed_ms
                    )

        except Exception as e:
            elapsed_ms = int((time.time() - t0) * 1000)
            return ScrapeResult(
                platform=self.platform,
                status=ScrapeStatus.FAILED,
                errors=[str(e)],
                url=url,
                elapsed_ms=elapsed_ms
            )

    def _parse_hotel_list(self, text: str, html: str, url: str, city: str) -> list[HotelRecord]:
        """解析去哪儿酒店列表（从渲染后文本提取）"""
        hotels = []

        # 去哪儿酒店名通常较长，包含品牌
        hotel_pattern = re.compile(
            r'([^\n]{5,50}?(?:酒店|宾馆|民宿|客栈|公寓|度假|旅馆))',
            re.MULTILINE
        )
        price_pattern = re.compile(r'[¥￥]\s*(\d+)')
        rating_pattern = re.compile(r'(\d+\.?\d*)\s*(?:分|/5)')

        names = hotel_pattern.findall(text)
        prices = price_pattern.findall(text)
        ratings = rating_pattern.findall(text)
        seen = set()

        for name in names:
            name = name.strip()
            if len(name) < 5 or name in seen:
                continue
            if any(kw in name for kw in ['版权所有', '投诉', '举报', 'ICP', '互联网', '营业执照']):
                continue
            seen.add(name)

        for i, name in enumerate(list(seen)[:20]):
            price_val = float(prices[i]) if i < len(prices) else None
            rating_val = float(ratings[0]) if ratings else None

            record = HotelRecord(
                platform=self.platform,
                hotel_name=name,
                price_min=price_val,
                rating=rating_val,
                room_available=True,
                url=url,
                raw_data={"city": city},
            )
            hotels.append(record)

        # 如果提取到实际数据，返回
        if hotels:
            filtered = [h for h in hotels if h.price_min is not None or h.hotel_name]
            return filtered if filtered else hotels
        return hotels


# ──────────────────────────────────────────────
# 6. 飞猪适配器 (Playwright)
# ──────────────────────────────────────────────
class FliggyAdapter(BasePlatformAdapter):
    """
    飞猪 (fliggy.com)
    策略: Playwright Chromium（阿里系JS渲染）
    特点: 阿里系，可能需要登录态才能看完整数据
    """

    platform = "fliggy"
    name = "Fliggy (Playwright)"

    HOTEL_URL = "https://www.fliggy.com/jiudian/"

    def is_available(self) -> bool:
        try:
            from playwright.sync_api import sync_playwright
            return True
        except ImportError:
            return False

    def scrape(self, city: str = "襄阳", **kwargs) -> ScrapeResult:
        url = self.HOTEL_URL
        t0 = time.time()

        try:
            from playwright.sync_api import sync_playwright
        except ImportError as e:
            return ScrapeResult(
                platform=self.platform,
                status=ScrapeStatus.NOT_IMPLEMENTED,
                errors=[f"Playwright not installed: {e}"],
                url=url,
                elapsed_ms=int((time.time() - t0) * 1000)
            )

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(
                    headless=True,
                    args=['--no-sandbox', '--disable-dev-shm-usage']
                )
                page = browser.new_page()

                page.set_extra_http_headers({
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                })

                page.goto(url, timeout=60000, wait_until='networkidle')
                page.wait_for_timeout(kwargs.get('wait_ms', 5000))

                text = page.inner_text('body')
                html = page.content()

                # 尝试搜索城市
                try:
                    # 查找搜索框并输入城市名
                    search_input = page.locator('input[type="text"], input[placeholder*="搜索"], input[placeholder*="目的地"]').first
                    if search_input:
                        search_input.fill(city)
                        page.wait_for_timeout(2000)
                        page.keyboard.press('Enter')
                        page.wait_for_timeout(5000)
                        text = page.inner_text('body')
                        html = page.content()
                except Exception:
                    pass  # 搜索交互失败，用首页内容

                browser.close()

                elapsed_ms = int((time.time() - t0) * 1000)

                hotels = self._parse_hotel_list(text, html, url, city)

                if hotels:
                    return ScrapeResult(
                        platform=self.platform,
                        status=ScrapeStatus.SUCCESS,
                        hotels=hotels,
                        url=url,
                        tool_used="playwright",
                        elapsed_ms=elapsed_ms
                    )
                else:
                    return ScrapeResult(
                        platform=self.platform,
                        status=ScrapeStatus.PARTIAL,
                        hotels=[],
                        errors=["JS-rendered content may need login or search interaction"],
                        url=url,
                        tool_used="playwright",
                        elapsed_ms=elapsed_ms
                    )

        except Exception as e:
            elapsed_ms = int((time.time() - t0) * 1000)
            return ScrapeResult(
                platform=self.platform,
                status=ScrapeStatus.FAILED,
                errors=[str(e)],
                url=url,
                elapsed_ms=elapsed_ms
            )

    def _parse_hotel_list(self, text: str, html: str, url: str, city: str) -> list[HotelRecord]:
        """解析飞猪酒店列表"""
        hotels = []

        hotel_pattern = re.compile(
            r'([^\n]{5,50}?(?:酒店|宾馆|民宿|客栈|公寓|度假))',
            re.MULTILINE
        )
        price_pattern = re.compile(r'[¥￥]\s*(\d+)')

        names = hotel_pattern.findall(text)
        prices_list = price_pattern.findall(text)
        seen = set()

        for name in names:
            name = name.strip()
            if len(name) < 5 or name in seen:
                continue
            if any(kw in name for kw in ['版权所有', 'ICP', '资质', '营业执照', '合作伙伴', '网站地图']):
                continue
            seen.add(name)

        price_idx = 0
        for name in list(seen)[:20]:
            price_val = None
            if price_idx < len(prices_list):
                try:
                    price_val = float(prices_list[price_idx])
                    price_idx += 1
                except ValueError:
                    pass

            record = HotelRecord(
                platform=self.platform,
                hotel_name=name,
                price_min=price_val,
                room_available=True,
                url=url,
                raw_data={"city": city},
            )
            hotels.append(record)

        return hotels


# ──────────────────────────────────────────────
# 7. Obscura 预留适配器
# ──────────────────────────────────────────────
class ObscuraAdapter(BasePlatformAdapter):
    """
    Obscura 反检测浏览器（预留）
    需先下载: https://github.com/h4ckf0r0day/obscura/releases
    """

    platform = "obscura"
    name = "Obscura (reserved)"

    PLATFORM_MAP = {
        "meituan": "hotel.meituan.com",
        "qunar": "hotel.qunar.com",
        "fliggy": "www.fliggy.com",
    }

    def is_available(self) -> bool:
        return os.path.exists(_OBSCURA_BIN)

    def scrape(self, city: str = "襄阳", **kwargs) -> ScrapeResult:
        if not self.is_available():
            return ScrapeResult(
                platform="obscura",
                status=ScrapeStatus.NOT_IMPLEMENTED,
                errors=["Obscura not installed. Download from GitHub releases."],
            )
        # 预留实现
        return ScrapeResult(
            platform="obscura",
            status=ScrapeStatus.NOT_IMPLEMENTED,
            errors=["Obscura integration pending"],
        )


# ──────────────────────────────────────────────
# 8. 编排器
# ──────────────────────────────────────────────
class OTAMonitor:
    """
    Multi-OTA 酒店数据监控编排器
    支持多平台并发采集、结果汇总、JSON导出
    """

    def __init__(self):
        self.adapters: dict[str, BasePlatformAdapter] = {}

        # 注册适配器（按优先级）
        for adapter_cls in [
            TripAdvisorAdapter,   # 最友好，优先
            MeituanAdapter,        # Playwright+stealth
            QunarAdapter,          # Playwright
            FliggyAdapter,         # Playwright
            ObscuraAdapter,        # 预留
        ]:
            adapter = adapter_cls()
            if adapter.is_available() or adapter.platform == "obscura":
                self.adapters[adapter.platform] = adapter

    def scrape_all(self, city: str = "襄阳", platforms: list[str] = None,
                   **kwargs) -> list[ScrapeResult]:
        """
        批量采集所有（或指定）平台

        Args:
            city: 城市名
            platforms: 平台列表，None=全部
            **kwargs: 传递给各适配器的参数
        """
        results = []
        targets = platforms or list(self.adapters.keys())

        for platform_name in targets:
            if platform_name == "obscura":
                continue  # 跳过预留适配器
            if platform_name not in self.adapters:
                results.append(ScrapeResult(
                    platform=platform_name,
                    status=ScrapeStatus.NOT_IMPLEMENTED,
                    errors=[f"No adapter for {platform_name}"],
                ))
                continue

            adapter = self.adapters[platform_name]
            print(f"[OTA] Scraping {adapter.name} for {city}...")

            try:
                result = adapter.scrape(city, **kwargs)
                results.append(result)

                n_hotels = len(result.hotels)
                print(f"  -> {result.status.value}: {n_hotels} hotels "
                      f"({result.elapsed_ms}ms)")
            except Exception as e:
                results.append(ScrapeResult(
                    platform=platform_name,
                    status=ScrapeStatus.FAILED,
                    errors=[str(e)],
                ))
                print(f"  -> FAILED: {e}")

        return results

    def get_summary(self, results: list[ScrapeResult]) -> dict:
        """生成采集汇总"""
        total_hotels = sum(len(r.hotels) for r in results)
        platforms_ok = sum(1 for r in results if r.status == ScrapeStatus.SUCCESS)
        platforms_partial = sum(1 for r in results if r.status == ScrapeStatus.PARTIAL)
        platforms_failed = sum(1 for r in results if r.status in
                              (ScrapeStatus.FAILED, ScrapeStatus.BLOCKED))

        return {
            "timestamp": datetime.now(CN_TZ).isoformat(),
            "total_platforms": len(results),
            "platforms_ok": platforms_ok,
            "platforms_partial": platforms_partial,
            "platforms_failed": platforms_failed,
            "total_hotels": total_hotels,
            "details": [
                {
                    "platform": r.platform,
                    "status": r.status.value,
                    "hotels": len(r.hotels),
                    "tool": r.tool_used,
                    "elapsed_ms": r.elapsed_ms,
                    "errors": r.errors,
                }
                for r in results
            ]
        }

    def export_json(self, results: list[ScrapeResult], filepath: str = None) -> str:
        """导出为JSON文件"""
        if filepath is None:
            ts = datetime.now(CN_TZ).strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(_CACHE_DIR, f"ota_monitor_{ts}.json")

        all_hotels = []
        for r in results:
            for h in r.hotels:
                all_hotels.append(asdict(h))

        output = {
            "summary": self.get_summary(results),
            "hotels": all_hotels,
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        # 同时保存一份 latest.json
        latest_path = os.path.join(_CACHE_DIR, "latest.json")
        with open(latest_path, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        return filepath

    def health_check(self) -> dict:
        """健康检查所有适配器"""
        return {
            "adapters": [a.get_health() for a in self.adapters.values()],
            "total": len(self.adapters),
        }

    def report(self) -> str:
        """生成人类可读报告"""
        health = self.health_check()
        lines = [
            "=" * 60,
            "  Multi-OTA 酒店数据监控 — 状态报告",
            "=" * 60,
            f"  时间: {datetime.now(CN_TZ).isoformat()}",
            f"  已注册适配器: {health['total']}",
            "",
            "  适配器状态:",
        ]
        for a in health['adapters']:
            status = "✅ 可用" if a['available'] else "⚠️ 不可用"
            lines.append(f"    [{a['platform']:15s}] {a['name']:30s} {status}")

        lines.extend([
            "",
            "  爬虫策略矩阵:",
            "  ┌──────────────┬─────────────────────────┬──────────┐",
            "  │ 平台         │ 策略                    │ 状态     │",
            "  ├──────────────┼─────────────────────────┼──────────┤",
        ])
        matrix = [
            ("猫途鹰", "scrap_tools 静态抓取", "✅ 已验证"),
            ("美团", "Playwright + stealth", "🔄 待验证"),
            ("去哪儿", "Playwright JS渲染", "🔄 待优化"),
            ("飞猪", "Playwright + 搜索交互", "🔄 待优化"),
        ]
        for platform, strategy, status in matrix:
            lines.append(f"  │ {platform:12s} │ {strategy:23s} │ {status:8s} │")
        lines.append("  └──────────────┴─────────────────────────┴──────────┘")
        lines.append("")
        lines.append("  注意: Obscura 反检测浏览器未安装，预留接口已就绪。")
        lines.append("  下载: https://github.com/h4ckf0r0day/obscura/releases")
        lines.append("=" * 60)

        return "\n".join(lines)


# ──────────────────────────────────────────────
# 9. CLI 入口
# ──────────────────────────────────────────────
def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Multi-OTA 酒店数据监控",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python ota_monitor.py                          # 全平台采集（襄阳）
  python ota_monitor.py --city 北京                # 指定城市
  python ota_monitor.py --platform tripadvisor     # 单平台
  python ota_monitor.py --platform meituan,qunar   # 多平台
  python ota_monitor.py --health                   # 健康检查
  python ota_monitor.py --report                   # 输出报告
        """
    )
    parser.add_argument("--city", "-c", default="襄阳", help="目标城市 (默认: 襄阳)")
    parser.add_argument("--platform", "-p", help="平台 (逗号分隔), 默认全部")
    parser.add_argument("--health", action="store_true", help="健康检查")
    parser.add_argument("--report", action="store_true", help="输出状态报告")
    parser.add_argument("--output", "-o", help="JSON输出路径")
    parser.add_argument("--cache-dir", help=f"缓存目录 (默认: {_CACHE_DIR})")

    args = parser.parse_args()

    monitor = OTAMonitor()

    if args.health:
        print(json.dumps(monitor.health_check(), indent=2, ensure_ascii=False))
        return

    if args.report:
        print(monitor.report())
        return

    platforms = None
    if args.platform:
        platforms = [p.strip() for p in args.platform.split(",")]

    print(f"[OTA Monitor] 开始采集 {args.city}...")
    results = monitor.scrape_all(city=args.city, platforms=platforms)

    # 导出
    output_path = monitor.export_json(results, args.output)
    print(f"\n[OTA Monitor] 结果已保存: {output_path}")

    # 汇总
    summary = monitor.get_summary(results)
    print(f"\n[汇总] {summary['platforms_ok']}/{summary['total_platforms']} 平台成功, "
          f"共 {summary['total_hotels']} 家酒店")

    for d in summary['details']:
        icon = "✅" if d['status'] == 'success' else "⚠️" if d['status'] == 'partial' else "❌"
        print(f"  {icon} {d['platform']:15s} {d['status']:8s} {d['hotels']:3d} hotels "
              f"({d['elapsed_ms']}ms)")


if __name__ == "__main__":
    main()
