"""TrendRadar AI科技新闻搜索 - 2026-08-25
并行调用 search_news + search_rss，覆盖关键词：
AI大模型、OpenAI、ChatGPT、Anthropic、Claude、通用人工智能AGI、科技公司动态
"""
import asyncio
import json
import sys
import time
import traceback

TR_ROOT = r"D:\B166ER-OpenClaw\workspace\trendradar"
sys.path.insert(0, TR_ROOT)

from mcp_server import server as _srv

get_trending_topics = _srv.get_trending_topics.fn
get_latest_news = _srv.get_latest_news.fn
search_news = _srv.search_news.fn
search_rss = _srv.search_rss.fn

TODAY = {"start": "2026-08-25", "end": "2026-08-25"}
KEYWORDS = [
    "AI大模型",
    "OpenAI",
    "ChatGPT",
    "Anthropic",
    "Claude",
    "通用人工智能AGI",
    "科技公司动态",
]


async def safe_call(name, coro):
    t0 = time.time()
    try:
        raw = await coro
        try:
            parsed = json.loads(raw)
        except Exception:
            parsed = {"raw": raw}
        elapsed = round((time.time() - t0) * 1000, 1)
        return {"ok": True, "name": name, "elapsed_ms": elapsed, "data": parsed}
    except Exception as e:
        elapsed = round((time.time() - t0) * 1000, 1)
        return {
            "ok": False,
            "name": name,
            "elapsed_ms": elapsed,
            "error": str(e),
            "traceback": traceback.format_exc(),
        }


async def main():
    print("[AI-NEWS] TrendRadar AI科技新闻搜索 @ 2026-08-25", flush=True)

    # 1. search_news 并行搜所有关键词
    news_tasks = [
        safe_call(
            f"search_news:{kw}",
            search_news(
                query=kw,
                search_mode="keyword",
                date_range=TODAY,
                platforms=None,
                limit=20,
                sort_by="weight",
                include_url=True,
                include_rss=True,
                rss_limit=20,
            )
        )
        for kw in KEYWORDS
    ]

    # 2. search_rss 并行搜所有关键词
    rss_tasks = [
        safe_call(
            f"search_rss:{kw}",
            search_rss(
                keyword=kw,
                feeds=None,
                days=7,
                limit=20,
                include_summary=True,
            )
        )
        for kw in KEYWORDS
    ]

    # 3. get_trending_topics 总览
    trending_task = safe_call(
        "get_trending_topics",
        get_trending_topics(top_n=20, mode="daily", extract_mode="auto_extract"),
    )

    # 4. get_latest_news 今日最新
    latest_task = safe_call(
        "get_latest_news",
        get_latest_news(platforms=None, limit=30, include_url=True),
    )

    all_tasks = news_tasks + rss_tasks + [trending_task, latest_task]
    results = await asyncio.gather(*all_tasks, return_exceptions=False)

    # 汇总
    summary = {}
    for x in results:
        if x["ok"]:
            summary[x["name"]] = {"ok": True, "elapsed_ms": x["elapsed_ms"], "keys": list(x["data"].keys()) if isinstance(x["data"], dict) else type(x["data"]).__name__}
        else:
            summary[x["name"]] = {"ok": False, "elapsed_ms": x["elapsed_ms"], "error": x["error"][:200]}

    # 输出摘要
    print("\n=== RESULTS SUMMARY ===")
    for name, s in summary.items():
        status = "OK" if s["ok"] else "FAIL"
        info = s.get("keys", s.get("error", ""))
        print(f"  [{status}] {name} ({s['elapsed_ms']}ms) {info}")

    # 整理输出JSON
    output = {
        "date": "2026-08-25",
        "keywords": KEYWORDS,
        "summary": summary,
        "results": results,
    }

    out_path = r"D:\B166ER-OpenClaw\workspace\toolbox\_subagent_trendradar_ai_news.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\n[SAVED] {out_path}")
    return output


if __name__ == "__main__":
    r = asyncio.run(main())
