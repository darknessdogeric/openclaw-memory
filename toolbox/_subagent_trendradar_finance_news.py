"""
TrendRadar 金融市场+能源新闻搜索 (2026-08-25)
Subagent task: 搜索今日金融市场+能源关键词新闻
"""
import asyncio
import json
import sys
import time

TR_ROOT = r"D:\B166ER-OpenClaw\workspace\trendradar"
sys.path.insert(0, TR_ROOT)

from mcp_server import server as _srv

get_trending_topics = _srv.get_trending_topics.fn
get_latest_news = _srv.get_latest_news.fn
analyze_sentiment = _srv.analyze_sentiment.fn
analyze_topic_trend = _srv.analyze_topic_trend.fn

KEYWORDS = [
    "原油WTI", "布伦特", "天然气",
    "美股S&P500", "纳斯达克",
    "美联储", "利率",
    "人民币", "A股", "港股"
]

TODAY = {"start": "2026-08-24", "end": "2026-08-24"}  # 08-25 data not yet crawled; use last available
LIMIT = 20


async def safe_call(name, coro):
    t0 = time.time()
    try:
        raw = await coro
        try:
            parsed = json.loads(raw) if isinstance(raw, str) else raw
        except Exception:
            parsed = {"raw": str(raw)}
        elapsed = round((time.time() - t0) * 1000, 1)
        return {"ok": True, "name": name, "elapsed_ms": elapsed, "data": parsed}
    except Exception as e:
        elapsed = round((time.time() - t0) * 1000, 1)
        import traceback
        return {
            "ok": False, "name": name, "elapsed_ms": elapsed,
            "error": str(e), "traceback": traceback.format_exc()
        }


async def main():
    print(f"[TRENDRADAR] Searching financial + energy news for 2026-08-25", flush=True)

    # Build parallel tasks: one search per keyword + trending + latest
    tasks = []

    for kw in KEYWORDS:
        tasks.append(safe_call(
            f"search_{kw}",
            _srv.search_news.fn(
                query=kw,
                search_mode="keyword",
                date_range=TODAY,
                limit=LIMIT,
                sort_by="weight",
                include_url=False,
                include_rss=True,
                rss_limit=LIMIT
            )
        ))

    # Also grab general trending + latest news as context
    tasks.append(safe_call(
        "trending_topics",
        get_trending_topics(top_n=15, mode="daily", extract_mode="auto_extract")
    ))
    tasks.append(safe_call(
        "latest_news",
        get_latest_news(platforms=None, limit=LIMIT, include_url=False)
    ))

    results = await asyncio.gather(*tasks, return_exceptions=False)

    # Build output JSON
    output = {
        "date": "2026-08-25",
        "keywords": KEYWORDS,
        "results": results
    }

    OUT = r"D:\B166ER-OpenClaw\workspace\toolbox\_subagent_trendradar_finance_20260825.json"
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n[SUMMARY]", flush=True)
    for x in results:
        if x["ok"]:
            d = x["data"]
            keys = list(d.keys()) if isinstance(d, dict) else type(d).__name__
            print(f"  [OK] {x['name']} ({x['elapsed_ms']}ms) keys={keys}", flush=True)
        else:
            print(f"  [FAIL] {x['name']} ({x['elapsed_ms']}ms) error={x['error'][:200]}", flush=True)

    print(f"\n[OUTPUT] {OUT}", flush=True)
    return output


if __name__ == "__main__":
    r = asyncio.run(main())
