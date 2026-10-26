#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""

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


# ---------------------------------------------------------------- 深度抓取（feed + 详情页）
# 2026-10-25 固化：原 collector 只抓列表页标题、不进详情页 → 结构性漏采
# （10-24 雅高 Q3、10-23 云酒店、10-24 内容即渠道 连三轮漏采，靠临时脚本补漏才找回）。
# 现把 meadin 的 9 个 feed + 详情页正文抓取正式并入 collector，不再依赖临时脚本。

# 2026-10-26 修正：原列表中 6 个 slug 早已 404（/news/ /hotel/ /travel/ /sc/ /yd/ /zs/），
# 它们静默返回 0 链接，等于「深抓覆盖了 6 个不存在的频道」——误以为有 9 个 feed 兜底，
# 实际只有 / 与 /jd/ /report/ 三条在跑。已按站点真实导航 slug 全量替换（逐个实测 HTTP 200 + 有详情链接）：
#   wl(文旅) jq(精品) cx(创新) gyl(供应链) mdzb(目的地) yj(研究) zl(专栏) gy(行业)
#   ICTE(科技) MDGJ(目的地管理) ydpd(目的地盘点) jd(酒店) report(报告) + 首页
# 另：/zt/ 与 /jdxm/ 虽 200 但 0 条详情链接，不纳入。
# 教训同「深抓固化」：静默失败=结构性漏采，feed 必须带 HTTP 状态可观测（见 collect_meadin_deep）。
MEADIN_FEEDS = [
    "https://www.meadin.com/",
    "https://www.meadin.com/jd/",
    "https://www.meadin.com/report/",
    "https://www.meadin.com/wl/",
    "https://www.meadin.com/jq/",
    "https://www.meadin.com/cx/",
    "https://www.meadin.com/gyl/",
    "https://www.meadin.com/mdzb/",
    "https://www.meadin.com/yj/",
    "https://www.meadin.com/zl/",
    "https://www.meadin.com/gy/",
    "https://www.meadin.com/ICTE/",
    "https://www.meadin.com/MDGJ/",
    "https://www.meadin.com/ydpd/",
]

_DETAIL_URL_RE = re.compile(r"^https?://www\.meadin\.com/[a-zA-Z]+/(\d+)\.html", re.I)
_PUB_DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}(?::\d{2})?)")
_BODY_DIV_RE = re.compile(
    r'<div[^>]+class="[^"]*(?:article|content|detail|txt|main)[^"]*"[^>]*>(.*?)</div>\s*(?:<div|</section)',
    re.S | re.I)


def _strip_html(s: str) -> str:
    if not s:
        return ""
    t = re.sub(r"(?is)<script.*?</script>", " ", s)
    t = re.sub(r"(?is)<style.*?</style>", " ", t)
    t = re.sub(r"(?is)<!--.*?-->", " ", t)
    t = re.sub(r"<[^>]+>", " ", t)
    for a, b in (("&nbsp;", " "), ("&amp;", "&"), ("&quot;", '"'), ("&ldquo;", "“"),
                 ("&rdquo;", "”"), ("&hellip;", "…")):
        t = t.replace(a, b)
    return re.sub(r"\s+", " ", t).strip()


def _page_html(page) -> str:
    for attr in ("html_content", "body", "text"):
        v = getattr(page, attr, None)
        if isinstance(v, str) and v:
            return v
    try:
        return str(page)
    except Exception:
        return ""


def _extract_pub_date(html: str) -> str:
    m = _PUB_DATE_RE.search(html or "")
    if not m:
        return ""
    d = m.group(1).replace("T", " ")
    if len(d) == 16:
        d += ":00"
    return d


def _extract_body(html: str, title: str) -> str:
    best = ""
    for m in _BODY_DIV_RE.finditer(html or ""):
        cand = _strip_html(m.group(1))
        if len(cand) > len(best):
            best = cand
    if len(best) < 200:
        best = _strip_html(html)
    if title and best.startswith(title):
        best = best[len(title):].strip()
    return best


async def _fetch_one(session, url: str, timeout_ms: int, **fetch_kwargs) -> Dict:
    """抓取单个 URL，返回统一结构。异常隔离在调用方之外。"""
    page = await session.fetch(url, timeout=timeout_ms, **fetch_kwargs)
    return {
        "source_url": url,
        "http_status": getattr(page, "status", None),
        "page_title": _page_title(page),
        "items": _safe_links(page),
        "scraped_at": datetime.now().isoformat(timespec="seconds"),
        "_html": _page_html(page),
    }


# ---------------------------------------------------------------- collector

class HotelDataCollector:
    """酒店行业数据采集器（异步）"""

    def __init__(self, timeout_ms: int = 45000, per_page_links: int = 25):
        self.timeout_ms = timeout_ms
        self.per_page_links = per_page_links
        self._session: Optional["AsyncStealthySession"] = None
        self._last_html: str = ""

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
            self._last_html = res.pop("_html", "") or ""
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
        res = await self._collect("小牛行研", "https://www.hangyan.co/charts",
                                  solve_cloudflare=True)
        # 2026-10-26 修正：列表页 <a href="/charts/ID"> 的锚文本只有日期（如 2026-10-25），
        # 图表标题在同卡片的 <img alt="标题 - 2026年10月 - 行业研究数据"> 里。
        # 原逻辑只取锚文本 → 每日只有日期、看不到标题，等于采了「有日期没内容」的半条数据。
        titles = self._hangyan_titles()
        if titles:
            for it in res.get("items", []):
                mid = (it.get("href") or "").rstrip("/").rsplit("/", 1)[-1]
                if mid in titles:
                    it["title"] = titles[mid]
            res["title_mapped"] = sum(1 for it in res.get("items", []) if it.get("title"))
            res["title_unmatched"] = sum(1 for it in res.get("items", []) if not it.get("title"))
            res["title_rule"] = ("只认带「- YYYY年M月 - 行业研究数据」后缀的 alt；"
                                 "无匹配则留空（宁可缺标题不可错标题）")
        return res

    def _hangyan_titles(self) -> Dict[str, str]:
        """从 hangyan 列表页 HTML 抽 {chart_id: 图表标题}。
        规则：同一张卡片里 <img alt="标题 - 2026年10月 - 行业研究数据"> 的 alt 去掉尾部后缀即标题；
        该 img 在结构上位于本卡片日期锚点 <a href="/charts/ID">日期</a> 之前，
        故对每个日期锚点向前回溯有限窗口，取最后一个 alt 作为它的标题。"""
        out: Dict[str, str] = {}
        html = self._last_html or ""
        if not html:
            return out
        # 2026-10-26 22:0x 修正（静默给错结论族，与 R-HEAL-24/25/26/27 同源）：
        #   原逻辑取「回溯窗口内最后一个 alt」→ 若该 alt 不带标题后缀（属别的卡片/正文片段）
        #   → 错配（22:00 轮实测 title_mapped 仅 2/4，出现把正文片段当标题）。
        #   改法：**只认带完整后缀**的 alt（「… - YYYY年M月 - 行业研究数据」），
        #   取最近一个匹配的；一个都不匹配 → **留空不映射**。
        #   原则：宁可缺标题，不可错标题（错的标题会污染下游报告的每一条结论）。
        # 2026-10-26 22:0x 修正（静默给错结论族，与 R-HEAL-24/25/26/27 同源）：
        #   原逻辑取「回溯窗口内最后一个 alt」→ 该 alt 若不带标题后缀（属别的卡片/正文片段）
        #   → 错配（22:00 轮实测 title_mapped 仅 2/4，把正文片段当标题）。
        #   第一版修法（只认带后缀的 alt）仍**二次错配**：固定 3000 字回溯窗口会把
        #   **上一张卡片**的 alt 带进来（后一张卡片若无带后缀 alt → 继承上一张的标题）。
        #   现改为**按卡片分段**：片段 = 上一个日期锚点结束 → 本锚点开始，
        #   只在本卡片自己的片段里取带完整后缀的 alt（「… - YYYY年M月 - 行业研究数据」）。
        #   一个都不匹配 → **留空不映射**。原则：宁可缺标题，不可错标题。
        SUF = re.compile(r"^(.{2,180}?)\s*-\s*20\d\d年\d{1,2}月\s*-\s*行业研究数据\s*$")
        _anchors = list(re.finditer(
                r'<a[^>]+href="/charts/(\d+)"[^>]*>(20\d\d-\d\d-\d\d)</a>', html))
        _prev_end = 0
        for _m in _anchors:
            _seg = html[_prev_end:_m.start()]
            _picked = ""
            for _alt in re.findall(r'alt="([^"]{4,200})"', _seg):
                _mm = SUF.match(_alt.strip())
                if _mm:
                    _cand = _mm.group(1).strip()
                    # 2026-10-26 22:3x 二次修正：**后缀合规 ≠ 是标题**。
                    #   实测仍有 alt 的后缀合规但正文部分本身是「少：从北证50高，点以来估值结构来看…」
                    #   这类**正文片段**（含中文逗号/超长/以连接词开头）→ 同样算错配。
                    #   判据（宁缺勿错）：含「，」「。」或长度>40 或以连接词开头 → 判为正文片段，丢弃。
                    if ('，' in _cand or '。' in _cand or len(_cand) > 40
                            or re.match(r'^(少|多|因此|所以|但是|然后|以及|其中|从|在|对|和|与|是|有|将|该|其)', _cand)):
                        continue
                    _picked = _cand
            if _picked:
                out[_m.group(1)] = _picked
            _prev_end = _m.end()
        return out

    async def collect_meadin_data(self) -> Dict:
        # 迈点报告列表为异步渲染，需等待网络空闲
        return await self._collect("迈点研究院", "https://www.meadin.com/report/",
                                   network_idle=True)

    async def collect_meadin_deep(self, since: str = "", max_details: int = 80) -> Dict:
        """深度抓取：9 个 feed 找详情页链接 → 逐篇取正文 → 只保留 since 之后新发布。
        固化自 2026-10-25 的临时补漏脚本（memory/_probe_meadin_2026-10-25_2000.py），
        目的是消灭「只抓列表页标题」的结构性漏采。"""
        out: Dict = {"source": "迈点研究院-深抓", "feeds": MEADIN_FEEDS,
                     "since": since, "scanned": 0, "new": {}, "feed_stats": {}}
        if not SCRAPLING_AVAILABLE or self._session is None:
            out["error"] = "Scrapling不可用"
            return out
        mids: Dict[str, str] = {}
        for feed in MEADIN_FEEDS:
            try:
                page = await self._session.fetch(feed, timeout=self.timeout_ms)
            except Exception as e:
                out["feed_stats"][feed] = "ERR " + str(e)[:80]
                continue
            found = 0
            status = getattr(page, "status", None)
            try:
                nodes = page.css("a")
            except Exception:
                nodes = []
            for el in nodes:
                try:
                    href = el.attrib.get("href", "") or ""
                except Exception:
                    continue
                m = _DETAIL_URL_RE.match(href.strip())
                if m:
                    mids.setdefault(m.group(1), href.strip())
                    found += 1
            # feed 健康度：非 200 或 0 链接必须显式暴露，否则等于静默漏采
            if status != 200:
                out["feed_stats"][feed] = "HTTP{} {}links DEAD".format(status, found)
            elif found == 0:
                out["feed_stats"][feed] = "HTTP200 0links EMPTY"
            else:
                out["feed_stats"][feed] = "HTTP200 {}links".format(found)
        ordered = sorted(mids.items(), key=lambda kv: int(kv[0]), reverse=True)
        out["detail_candidates"] = len(ordered)
        dead = [f for f, s in out["feed_stats"].items() if s.startswith("HTTP") and "DEAD" in s]
        out["dead_feeds"] = dead
        out["feed_health"] = ("OK" if not dead else "DEAD_FEEDS:{}".format(len(dead)))
        for mid, url in ordered[:max_details]:
            try:
                page = await self._session.fetch(url, timeout=self.timeout_ms)
            except Exception:
                continue
            html = _page_html(page)
            date = _extract_pub_date(html)
            title = _page_title(page)
            body = _extract_body(html, title)
            out["scanned"] += 1
            out["new"][mid] = {"url": url, "date": date, "title": title,
                               "snippet": body[:2200], "len": len(body)}
        if since:
            out["new"] = {k: v for k, v in out["new"].items()
                          if v.get("date") and v["date"] >= since}
        out["new_count"] = len(out["new"])
        return out

    async def collect_traveldaily_data(self) -> Dict:
        # 2026-10-26 标注：该源列表页**无发布日期字段**（10-26 实测：其"新增"项多为补采而非新发布）
        # → 本源的结果**不可用于 --since 差分**；显式打标，避免后续被误当"新增"统计
        res = await self._collect("环球旅讯", "https://hub.traveldaily.cn/report/")
        try:
            res["has_publish_date"] = False
            res["delta_comparable"] = False
            res["note_delta"] = ("列表页无发布日期字段 → 不参与 --since 差分；"
                                 "可做内容变化比对，不可做新增计数")
        except Exception:
            pass
        return res

    async def collect_stock_data(self, company: str) -> Dict:
        # 2026-10-26 实测修正（原 4 个 URL：2×404 + 2×SSL EOF，实为休眠 bug）：
        #   锦江/首旅的 /investor 路径 404；华住/亚朵 IR 域 TLS 握手 EOF（需浏览器态）
        #   → 改用可达的官网 IR 入口；仍不可达的显式标注，不静默失败
        urls = {
            "huazhu": "https://ir.huzhu.com/",
            "jinjiang": "http://www.jinjianghotels.com.cn/",
            "shoulv": "http://www.bthhotels.com/",
            "atour": "https://ir.atour.com/",
        }
        url = urls.get(company)
        if not url:
            return {"source": company, "error": f"未知公司: {company}"}
        res = await self._collect(f"财报:{company}", url)
        try:
            res["has_publish_date"] = False
            res["delta_comparable"] = False
            res["note_delta"] = ("IR 页无统一发布日期字段；且 IR 域部分站点 TLS 直连失败"
                                 "（华住/亚朵），需浏览器态 → 不参与 --since 差分")
        except Exception:
            pass
        return res

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
                if config["meadin"].get("deep"):
                    tasks["meadin_deep"] = self.collect_meadin_deep(
                        since=config["meadin"].get("since", ""),
                        max_details=config["meadin"].get("deep_max", 80))
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
    parser.add_argument("--deep", action="store_true",
                        help="启用 meadin 深抓（feed + 详情页正文），补列表页结构性漏采")
    parser.add_argument("--since", default="", help="深抓只保留该时点之后新发布 (YYYY-MM-DD HH:MM:SS)")
    parser.add_argument("--deep-max", type=int, default=80, help="深抓最多抓取详情页数")
    args = parser.parse_args()

    config = {
        "str": {"enabled": args.source in ["str", "all"],
                "start_date": args.start_date or "2026-01-01",
                "end_date": args.end_date or "2026-03-31"},
        "hangyan": {"enabled": args.source in ["hangyan", "all"]},
        "meadin": {"enabled": args.source in ["meadin", "all"],
                   "deep": args.deep, "since": args.since, "deep_max": args.deep_max},
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