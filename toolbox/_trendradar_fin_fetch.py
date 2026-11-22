"""
TrendRadar 金融市场+能源新闻综合搜索 (2026-08-25)
整合: news DB (2026-08-24) + RSS DB (2026-08-25)
关键词: 原油WTI、布伦特、天然气、美股S&P500、纳斯达克、美联储、利率、人民币、A股、港股
"""
import sys, os, json, asyncio
sys.path.insert(0, r'D:\B166ER-OpenClaw\workspace\trendradar')

from mcp_server import server as _srv

KEYWORDS = [
    "原油WTI", "布伦特", "天然气",
    "美股S&P500", "纳斯达克",
    "美联储", "利率",
    "人民币", "A股", "港股"
]

TODAY = {"start": "2026-08-25", "end": "2026-08-25"}
YESTERDAY = {"start": "2026-08-24", "end": "2026-08-24"}
LIMIT = 20

async def safe_call(name, coro):
    try:
        raw = await coro
        parsed = json.loads(raw) if isinstance(raw, str) else raw
        return {"ok": True, "name": name, "data": parsed}
    except Exception as e:
        import traceback
        return {"ok": False, "name": name, "error": str(e), "traceback": traceback.format_exc()}


async def main():
    print("[TRENDRADAR] Fetching financial + energy news from news DB + RSS DB", flush=True)

    tasks = []

    # Search news DB (2026-08-24) - keyword search (热榜)
    for kw in KEYWORDS:
        tasks.append(safe_call(
            f"news_{kw}",
            _srv.search_news.fn(
                query=kw, search_mode="keyword",
                date_range=YESTERDAY, limit=LIMIT,
                sort_by="weight", include_url=False,
                include_rss=False, rss_limit=0
            )
        ))

    # Search RSS DB (2026-08-25) - keyword search
    for kw in KEYWORDS:
        tasks.append(safe_call(
            f"rss_{kw}",
            _srv.search_rss.fn(
                keyword=kw, feeds=None,
                days=1, limit=LIMIT,
                include_summary=False
            )
        ))

    # Also grab trending topics + latest news for context
    tasks.append(safe_call("trending", _srv.get_trending_topics.fn(
        top_n=20, mode="daily", extract_mode="auto_extract")))
    tasks.append(safe_call("latest_news", _srv.get_latest_news.fn(
        platforms=None, limit=LIMIT, include_url=False)))

    results = await asyncio.gather(*tasks, return_exceptions=False)
    return results


if __name__ == "__main__":
    r = asyncio.run(main())

    OUT = r"D:\B166ER-OpenClaw\workspace\toolbox\_subagent_trendradar_finance_20260825.json"

    output = {
        "date": "2026-08-25",
        "data_date_note": "News DB: 2026-08-24 (last available), RSS DB: 2026-08-25",
        "keywords": KEYWORDS,
        "results": r
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n[SUMMARY] {len(r)} tasks completed", flush=True)
    for x in r:
        name = x['name']
        if x['ok']:
            d = x['data']
            if isinstance(d, dict):
                success = d.get('success', True)
                total = d.get('total', d.get('rss_total', d.get('data', []).__len__() if 'data' in d else 0))
                print(f"  [OK] {name}: total={total}", flush=True)
            else:
                print(f"  [OK] {name}", flush=True)
        else:
            print(f"  [FAIL] {name}: {x['error'][:100]}", flush=True)

    print(f"\n[OUTPUT] {OUT}", flush=True)
