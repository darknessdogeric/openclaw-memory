# -*- coding: utf-8 -*-
"""
OTA-Scraper 主引擎
编排整个抓取流程: 平台识别 → 后端选择 → 抓取 → 解析 → 标准化输出
"""
from __future__ import annotations
import time
import logging
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, field

from .core import (
    OTAHotel, OTAResult, OTAPrice, OTAReview, ScrapeStatus,
    ScrapeAttempt, BackendType
)
from .backends import create_backends, CacheManager
from .platforms import get_platform, resolve_platform, list_platforms, get_all_platforms
from .pipeline import DataPipeline
from .adaptive import adaptive_select, infer_selectors, ADAPTIVE_SELECTORS

# 日志
logging.basicConfig(level=logging.INFO, format='[OTA-Scraper] %(levelname)s: %(message)s')
logger = logging.getLogger("ota_scraper")


@dataclass
class ScrapeTask:
    """单次抓取任务"""
    url: str
    platform_id: str = ""
    task_type: str = "search"          # search(列表) / detail(详情) / review(评论)
    max_pages: int = 1
    city: str = ""
    hotel_name: str = ""
    options: dict = field(default_factory=dict)


class OTAScraper:
    """
    OTA抓取引擎

    用法:
        scraper = OTAScraper()
        result = scraper.scrape("https://hotels.ctrip.com/hotel/beijing.html")
        print(f"抓取到 {len(result.hotels)} 家酒店")

    or simplified:
        from ota_scraper import scrape_ota
        result = scrape_ota("https://hotels.ctrip.com/hotel/beijing.html")
    """

    def __init__(self, cache_dir: str = None, output_dir: str = None):
        self.cache = CacheManager(cache_dir)
        self.backends = create_backends(self.cache)
        self.pipeline = DataPipeline()

        if output_dir:
            import os
            os.makedirs(output_dir, exist_ok=True)
        self.output_dir = output_dir

        logger.info(f"OTA-Scraper v1.0 初始化完成")
        logger.info(f"可用后端: {list(self.backends.keys())}")
        logger.info(f"已注册平台: {len(get_all_platforms())}")

    # ──────────────────────────────────────────
    # 主入口
    # ──────────────────────────────────────────
    def scrape(self, url: str = None, platform_id: str = None,
               city: str = "", hotel_name: str = "",
               max_pages: int = 1, task_type: str = "search",
               **kwargs) -> OTAResult:
        """
        主抓取方法

        Args:
            url: 目标URL (自动识别平台)
            platform_id: 平台ID (如 'ctrip', 'meituan')
            city: 城市名(用于构造搜索URL)
            hotel_name: 酒店名(用于详情)
            max_pages: 最大翻页数
            task_type: search(列表页) / detail(详情页) / review(评论)

        Returns:
            OTAResult with hotels
        """
        t_start = time.time()

        # 1. 平台识别
        if platform_id:
            platform = get_platform(platform_id)
            if not platform:
                return self._error_result(platform_id, url or "", f"未知平台: {platform_id}")
        elif url:
            platform_id = resolve_platform(url)
            if not platform_id:
                return self._error_result("unknown", url, f"无法识别URL的平台: {url}")
            platform = get_platform(platform_id)
        else:
            return self._error_result("unknown", "", "必须提供url或platform_id")

        logger.info(f">> 平台: {platform['name']} ({platform_id}) | 类型: {task_type} | 翻页: {max_pages}")

        # 2. 构造URL
        if not url:
            url = self._build_url(platform, city, task_type)

        # 3. 创建结果容器
        result = OTAResult(
            platform=platform_id,
            url=url,
            status=ScrapeStatus.FAILED,
            scraped_at=datetime.now().isoformat(),
        )

        # 4. 执行抓取
        all_hotels = []
        for page in range(1, max_pages + 1):
            page_url = self._paginate_url(url, page, platform)

            # 检查缓存
            if kwargs.get("use_cache", True):
                cached = self.cache.get(page_url, max_age_seconds=kwargs.get("cache_ttl", 300))
                if cached:
                    logger.info(f"  [page {page}] 使用缓存")
                    html = cached
                else:
                    html = self._do_fetch(page_url, platform, result, **kwargs)
                    if html:
                        self.cache.set(page_url, html)
            else:
                html = self._do_fetch(page_url, platform, result, **kwargs)

            if not html:
                logger.warning(f"  [page {page}] 抓取失败")
                if page == 1:
                    result.errors.append(f"首页抓取失败")
                    break
                continue

            # 5. 解析数据
            if task_type == "search":
                hotels = self.pipeline.parse_hotel_list(html, platform_id, platform)
            else:
                hotel = self.pipeline.parse_hotel_detail(html, platform_id, platform)
                hotels = [hotel] if hotel else []

            logger.info(f"  [page {page}] 解析到 {len(hotels)} 家酒店")
            all_hotels.extend(hotels)

            # 速率限制
            delay = platform["rate_limit"].get("delay_seconds", 3)
            if page < max_pages:
                time.sleep(delay)

        # 6. 汇总结果
        result.hotels = all_hotels
        result.status = ScrapeStatus.SUCCESS if all_hotels else ScrapeStatus.PARTIAL
        result.total_count = len(all_hotels)
        result.page = max_pages
        result.duration_seconds = round(time.time() - t_start, 2)

        logger.info(f"<< 完成: {len(all_hotels)} 家酒店, 耗时 {result.duration_seconds}s, "
                   f"质量 {result.data_quality:.0%}")

        return result

    def _do_fetch(self, url: str, platform: dict, result: OTAResult, **kwargs) -> Optional[str]:
        """执行单次抓取，按优先级尝试后端"""
        backends_config = platform.get("backends", [])
        force_backends = kwargs.pop("force_backends", None)

        if force_backends:
            backends_config = [{"type": b, "priority": i+1} for i, b in enumerate(force_backends)]

        selectors = platform.get("selectors", {})

        for be_config in backends_config:
            be_type = be_config["type"]
            be_priority = be_config.get("priority", 99)

            if be_type not in self.backends:
                logger.debug(f"    后端 {be_type} 不可用，跳过")
                continue

            backend = self.backends[be_type]
            t0 = time.time()

            try:
                logger.info(f"    尝试 {be_type} (优先级 {be_priority})...")

                be_kwargs = {k: v for k, v in be_config.items()
                           if k not in ("type", "priority")}
                if not be_kwargs.get("css_selector") and selectors.get("hotel_list"):
                    be_kwargs["css_selector"] = selectors["hotel_list"]
                # 传递字段选择器用于结构化提取
                card_sels = {k.replace("hotel_", ""): v for k, v in selectors.items()
                            if k.startswith("hotel_") and k != "hotel_list"}
                if card_sels:
                    be_kwargs["card_selectors"] = card_sels
                be_kwargs.update(kwargs)

                response = backend.fetch(url, **be_kwargs)
                duration_ms = (time.time() - t0) * 1000

                if response.content and len(response.content) > 200:
                    # 检测是否被拦截
                    if self._is_blocked(response.content):
                        logger.warning(f"    {be_type}: 被反爬拦截")
                        result.attempts.append(ScrapeAttempt(
                            backend=BackendType(be_type) if be_type in [b.value for b in BackendType] else BackendType.DIRECT,
                            status=ScrapeStatus.BLOCKED,
                            duration_ms=duration_ms,
                            content_length=len(response.content),
                            error="blocked by anti-bot"
                        ))
                        continue

                    logger.info(f"    ✓ {be_type}: {len(response.content)} chars, {duration_ms:.0f}ms")
                    result.attempts.append(ScrapeAttempt(
                        backend=BackendType(be_type) if be_type in [b.value for b in BackendType] else BackendType.DIRECT,
                        status=ScrapeStatus.SUCCESS,
                        duration_ms=duration_ms,
                        content_length=len(response.content),
                    ))
                    return response.content
                else:
                    logger.warning(f"    {be_type}: 内容过短 ({len(response.content)} chars)")
                    result.attempts.append(ScrapeAttempt(
                        backend=BackendType(be_type) if be_type in [b.value for b in BackendType] else BackendType.DIRECT,
                        status=ScrapeStatus.PARTIAL,
                        duration_ms=duration_ms,
                        content_length=len(response.content),
                        error="content too short"
                    ))

            except Exception as e:
                duration_ms = (time.time() - t0) * 1000
                logger.error(f"    ✗ {be_type}: {str(e)[:100]}")
                result.attempts.append(ScrapeAttempt(
                    backend=BackendType(be_type) if be_type in [b.value for b in BackendType] else BackendType.DIRECT,
                    status=ScrapeStatus.FAILED,
                    duration_ms=duration_ms,
                    error=str(e)[:200]
                ))

        return None

    def _is_blocked(self, content: str) -> bool:
        """检测是否被反爬拦截"""
        blocked_patterns = [
            "请点击下方按钮进行验证",
            "请完成以下验证",
            "请输入验证码",
            "滑块验证",
            "captcha",
            "verify you are a human",
            "Access Denied",
            "403 Forbidden",
            "请先登录",
            "系统检测到异常访问",
            "Please enable JavaScript",
            "请开启JavaScript",
            "您的IP已被限制",
            "访问过于频繁",
            "too many requests",
            "请稍后再试",
            "blocked",
        ]
        content_lower = content[:2000].lower()
        return any(p.lower() in content_lower for p in blocked_patterns)

    # ──────────────────────────────────────────
    # 快捷键
    # ──────────────────────────────────────────
    def search_hotels(self, platform_id: str, city: str,
                      max_pages: int = 1, **kwargs) -> OTAResult:
        """搜索城市酒店"""
        return self.scrape(platform_id=platform_id, city=city,
                          task_type="search", max_pages=max_pages, **kwargs)

    def get_hotel_detail(self, url: str, **kwargs) -> OTAResult:
        """获取酒店详情"""
        return self.scrape(url=url, task_type="detail", **kwargs)

    def compare_prices(self, city: str, platforms: list[str] = None,
                       **kwargs) -> list[OTAResult]:
        """跨平台价格对比"""
        if platforms is None:
            platforms = ["ctrip", "meituan", "qunar", "fliggy", "tongcheng"]

        results = []
        for pid in platforms:
            logger.info(f"\n{'='*50}")
            logger.info(f"抓取 {get_platform(pid)['name']}...")
            result = self.scrape(platform_id=pid, city=city,
                               task_type="search", max_pages=1, **kwargs)
            results.append(result)
            if pid != platforms[-1]:
                time.sleep(2)
        return results

    def batch_scrape(self, tasks: list[ScrapeTask], **kwargs) -> list[OTAResult]:
        """批量抓取"""
        results = []
        for task in tasks:
            r = self.scrape(
                url=task.url,
                platform_id=task.platform_id,
                city=task.city,
                hotel_name=task.hotel_name,
                max_pages=task.max_pages,
                task_type=task.task_type,
                **{**task.options, **kwargs}
            )
            results.append(r)
            time.sleep(1)
        return results

    # ──────────────────────────────────────────
    # 工具方法
    # ──────────────────────────────────────────
    def _build_url(self, platform: dict, city: str, task_type: str) -> str:
        """构造搜索URL"""
        if task_type == "search" and city:
            return platform["search_url"].format(city=city)
        return platform["base_url"]

    def _paginate_url(self, url: str, page: int, platform: dict) -> str:
        """翻页URL处理"""
        if page <= 1:
            return url
        # 常见翻页模式
        if "ctrip.com" in url:
            return url.replace(".html", f"/p{page}.html") if ".html" in url else f"{url}/p{page}"
        if "meituan.com" in url:
            return f"{url}?page={page}"
        if "booking.com" in url:
            return f"{url}&offset={(page-1)*25}"
        # 通用
        return f"{url}?page={page}"

    def _error_result(self, platform_id: str, url: str, error: str) -> OTAResult:
        return OTAResult(
            platform=platform_id, url=url,
            status=ScrapeStatus.FAILED,
            errors=[error],
            scraped_at=datetime.now().isoformat(),
        )

    def report(self) -> dict:
        """系统状态报告"""
        return {
            "version": "1.0.0",
            "backends": {name: {"type": be.backend_type.value} for name, be in self.backends.items()},
            "platforms": len(get_all_platforms()),
            "platform_list": [{"id": pid, "name": p["name"], "level": p["anti_bot_level"], "desc": p["description"]}
                            for pid, p in get_all_platforms().items()],
        }

    def healthcheck(self) -> dict:
        """健康检查 - 测试各后端"""
        results = {}
        for name, be in self.backends.items():
            try:
                t0 = time.time()
                # 使用轻量测试URL，只检查basic连通性
                resp = be.fetch("https://httpbin.org/get", timeout=10, stealth=False, wait_ms=1000)
                results[name] = {"status": "ok", "latency_ms": round((time.time()-t0)*1000)}
            except Exception as e:
                results[name] = {"status": "error", "error": str(e)[:100]}
        return results


# ──────────────────────────────────────────────
# 快捷函数（与 __init__.py 导出对齐）
# ──────────────────────────────────────────────
_default_scraper: Optional[OTAScraper] = None

def get_scraper(**kwargs) -> OTAScraper:
    global _default_scraper
    if _default_scraper is None:
        _default_scraper = OTAScraper(**kwargs)
    return _default_scraper

def scrape_ota(url: str = None, platform_id: str = None,
               city: str = "", **kwargs) -> OTAResult:
    """快捷抓取函数"""
    return get_scraper().scrape(url=url, platform_id=platform_id, city=city, **kwargs)
