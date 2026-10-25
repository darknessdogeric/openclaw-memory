#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

来源: 本文件是 cron「B166ER-DailyDataCollection」实际运行的权威版本，
      原位于 C:\Users\ericz\.openclaw\data-acquisition\data_collector.py（不在版本控制内，
      存在「改了坏了无法回滚」风险）。2026-10-25 原样收编入 git；
      同名旧版仍在 toolbox\data_collector.py 与 skills\hotel-report\data_collector.py（三方漂移）。
酒店行业数据采集器 v2.0
基于 Scrapling 0.5 异步 API（AsyncStealthySession）

v1.0 -> v2.0 修复:
  1. Sync StealthyFetcher 在 asyncio loop 内调用 -> 改用 AsyncStealthySession
  2. fetch timeout 单位为毫秒（原代码误当秒用）
  3. 每个数据源独立异常隔离，单源失败不影响其他源
  4. 真实解析页面标题/链接，输出可读条目而非占位字符串
"""

import json
import asyncio
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

try:
    from scrapling.fetchers import AsyncStealthySession
    SCRAPLING_AVAILABLE = True
except ImportError:
    SCRAPLING_AVAILABLE = False
    print("警告: Scrapling未安装，将使用备用方案", file=sys.stderr)


# ---------------------------------------------------------------- helpers

_NOISE = re.compile(r"^(首页|登录|注册|更多|详情|下载|返回|English|中文|下一页|上一页|关于我们|联系我们|隐私政策)$")


def _clean(text: Optional[str], min_len: int = 8) -> str:
    if not text:
        return ""
    t = re.sub(r"\s+", " ", str(text)).strip()
    return t if len(t) >= min_len else ""


def _safe_links(page, limit: int = 25) -> List[Dict[str, str]]:
    """防御式抽取页面链接；文本节点不触碰 .attrib，避免 Text-node 异常。"""
    out: List[Dict[str, str]] = []
    seen = set()
    try:
        nodes = page.css("a")
    except Exception:
        return out
    for el in nodes:
        try:
            text = _clean(el.text)
            href = el.attrib.get("href", "") or ""
        except Exception:
            continue  # 文本节点/属性缺失 -> 跳过
        if not text or _NOISE.match(text) or text in seen:
            continue
        if not href or href.startswith(("#", "javascript:")):
            continue
        seen.add(text)
        out.append({"text": text, "href": href})
        if len(out) >= limit:
            break
    return out


def _page_title(page) -> str:
    try:
        t = page.css("title::text")
        return _clean(t[0], 4) if t else ""
    except Exception:
        return ""


async def _fetch_one(session, url: str, timeout_ms: int, **fetch_kwargs) -> Dict:
    """抓取单个 URL，返回统一结构。异常隔离在调用方之外。"""
    page = await session.fetch(url, timeout=timeout_ms, **fetch_kwargs)
    return {
        "source_url": url,
        "http_status": getattr(page, "status", None),
        "page_title": _page_title(page),
        "items": _safe_links(page),
        "scraped_at": datetime.now().isoformat(timespec="seconds"),
    }


# ---------------------------------------------------------------- collector

class HotelDataCollector:
    """酒店行业数据采集器（异步）"""

    def __init__(self, timeout_ms: int = 45000, per_page_links: int = 25):
        self.timeout_ms = timeout_ms
        self.per_page_links = per_page_links
        self._session: Optional["AsyncStealthySession"] = None

    async def __aenter__(self):
        if SCRAPLING_AVAILABLE:
            self._session = AsyncStealthySession(max_pages=2)
            await self._session.start()
        return self

    async def __aexit__(self, *exc):
        if self._session:
            try:
                await self._session.close()
            except Exception:
                pass

    async def _collect(self, label: str, url: str, **fetch_kwargs) -> Dict:
        if not SCRAPLING_AVAILABLE or self._session is None:
            return {"source": label, "error": "Scrapling不可用"}
        try:
            res = await _fetch_one(self._session, url, self.timeout_ms, **fetch_kwargs)
            res["source"] = label
            res["item_count"] = len(res["items"])
            res["items"] = res["items"][: self.per_page_links]
            return res
        except Exception as e:
            return {"source": label, "source_url": url, "error": f"{type(e).__name__}: {str(e)[:200]}"}

    # ---- 数据源 ----

    async def collect_str_data(self, start_date: str, end_date: str) -> Dict:
        """STR 数据需官方 API 授权，此处保留占位。"""
        return {
            "source": "STR",
            "period": f"{start_date} to {end_date}",
            "metrics": {"occ": None, "adr": None, "revpar": None},
            "note": "STR数据需要官方API授权（未配置 STR_API_KEY）",
        }

    async def collect_hangyan_data(self) -> Dict:
        # 小牛行研首页有安全验证，需开启 Cloudflare 求解
        return await self._collect("小牛行研", "https://www.hangyan.co/charts",
                                   solve_cloudflare=True)

    async def collect_meadin_data(self) -> Dict:
        # 迈点报告列表为异步渲染，需等待网络空闲
        return await self._collect("迈点研究院", "https://www.meadin.com/report/",
                                   network_idle=True)

    async def collect_traveldaily_data(self) -> Dict:
        return await self._collect("环球旅讯", "https://hub.traveldaily.cn/report/")

    async def collect_stock_data(self, company: str) -> Dict:
        urls = {
            "huazhu": "https://ir.huzhu.com",
            "jinjiang": "http://www.jinjianghotels.com.cn/investor",
            "shoulv": "http://www.bthhotels.com/investor",
            "atour": "https://ir.atour.com",
        }
        url = urls.get(company)
        if not url:
            return {"source": company, "error": f"未知公司: {company}"}
        return await self._collect(f"财报:{company}", url)

    async def collect_all(self, config: Dict) -> Dict:
        results: Dict = {}
        async with self:
            tasks = {}
            if config.get("str", {}).get("enabled"):
                c = config["str"]
                results["str"] = await self.collect_str_data(
                    c.get("start_date", "2026-01-01"), c.get("end_date", "2026-03-31")
                )
            if config.get("hangyan", {}).get("enabled"):
                tasks["hangyan"] = self.collect_hangyan_data()
            if config.get("meadin", {}).get("enabled"):
                tasks["meadin"] = self.collect_meadin_data()
            if config.get("traveldaily", {}).get("enabled"):
                tasks["traveldaily"] = self.collect_traveldaily_data()
            for comp in config.get("stocks", []):
                tasks[f"stock_{comp}"] = self.collect_stock_data(comp)

            if tasks:
                done = await asyncio.gather(*tasks.values(), return_exceptions=True)
                for key, val in zip(tasks.keys(), done):
                    results[key] = val if not isinstance(val, Exception) else {"error": str(val)[:200]}
        return results


# ---------------------------------------------------------------- processor

class DataProcessor:
    @staticmethod
    def calculate_yoy(current: float, previous: float) -> Optional[float]:
        if not previous:
            return None
        return round((current - previous) / abs(previous) * 100, 2)

    @staticmethod
    def calculate_mom(current: float, previous: float) -> Optional[float]:
        if not previous:
            return None
        return round((current - previous) / abs(previous) * 100, 2)

    @staticmethod
    def calculate_revpar(occ: float, adr: float) -> float:
        return round(occ * adr, 2)


# ---------------------------------------------------------------- CLI

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="酒店行业数据采集工具 v2.0")
    parser.add_argument("--source", choices=["str", "hangyan", "meadin", "traveldaily", "all"],
                        default="all", help="数据源")
    parser.add_argument("--output", default="hotel_data.json", help="输出文件")
    parser.add_argument("--start-date", help="开始日期 (YYYY-MM-DD)")
    parser.add_argument("--end-date", help="结束日期 (YYYY-MM-DD)")
    parser.add_argument("--timeout", type=int, default=45000, help="单页超时(毫秒)")
    args = parser.parse_args()

    config = {
        "str": {"enabled": args.source in ["str", "all"],
                "start_date": args.start_date or "2026-01-01",
                "end_date": args.end_date or "2026-03-31"},
        "hangyan": {"enabled": args.source in ["hangyan", "all"]},
        "meadin": {"enabled": args.source in ["meadin", "all"]},
        "traveldaily": {"enabled": args.source in ["traveldaily", "all"]},
    }

    collector = HotelDataCollector(timeout_ms=args.timeout)
    results = asyncio.run(collector.collect_all(config))
    results["_meta"] = {"collected_at": datetime.now().isoformat(timespec="seconds"), "version": "2.0"}

    output_path = Path(args.output)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    ok = sum(1 for k, v in results.items()
             if isinstance(v, dict) and v.get("item_count", 0) > 0 and "error" not in v)
    fail = [k for k, v in results.items() if isinstance(v, dict) and v.get("error")]
    print(f"数据采集完成: 成功 {ok} 源 / 失败 {len(fail)} 源 {fail or ''}")
    print(f"结果保存至: {output_path.absolute()}")