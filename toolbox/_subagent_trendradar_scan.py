"""TrendRadar 全网深扫 - 并行调用6个MCP工具
Subagent: 654091c8-dfa4-41e4-a0f5-4e5291c377f4
Date: 2026-07-28
"""
import asyncio
import json
import sys
import time
import traceback

# 设置trendradar venv路径
TR_ROOT = r"D:\B166ER-OpenClaw\workspace\trendradar"
sys.path.insert(0, TR_ROOT)

from mcp_server import server as _srv

# FastMCP @mcp.tool 把函数包成 FunctionTool；取 .fn 拿到原 async 函数
get_trending_topics = _srv.get_trending_topics.fn
get_latest_news = _srv.get_latest_news.fn
analyze_sentiment = _srv.analyze_sentiment.fn
analyze_topic_trend = _srv.analyze_topic_trend.fn


async def safe_call(name, coro):
    """包装调用 + 异常处理 + 计时"""
    t0 = time.time()
    try:
        raw = await coro
        # 函数返回JSON字符串
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
    print("[SCAN] starting parallel TrendRadar deep scan @ 2026-07-28", flush=True)

    today = {"start": "2026-07-28", "end": "2026-07-28"}
    last4 = {"start": "2026-07-25", "end": "2026-07-28"}

    tasks = [
        safe_call("get_trending_topics",
                  get_trending_topics(top_n=15, mode="daily", extract_mode="auto_extract")),
        safe_call("analyze_sentiment_hotel",
                  analyze_sentiment(topic="酒店", platforms=None, date_range=today,
                                    limit=10, sort_by_weight=True, include_url=False)),
        safe_call("analyze_sentiment_ai",
                  analyze_sentiment(topic="AI", platforms=None, date_range=today,
                                    limit=10, sort_by_weight=True, include_url=False)),
        safe_call("analyze_topic_trend_reits",
                  analyze_topic_trend(topic="酒店REITs", analysis_type="trend",
                                       date_range=last4, granularity="day")),
        safe_call("analyze_topic_trend_oil",
                  analyze_topic_trend(topic="油价", analysis_type="trend",
                                       date_range=last4, granularity="day")),
        safe_call("get_latest_news",
                  get_latest_news(platforms=None, limit=20, include_url=False)),
    ]

    results = await asyncio.gather(*tasks, return_exceptions=False)
    return results


if __name__ == "__main__":
    r = asyncio.run(main())
    # 输出结构化摘要
    print("\n=== SUMMARY ===")
    for x in r:
        if x["ok"]:
            d = x["data"]
            keys = list(d.keys()) if isinstance(d, dict) else type(d).__name__
            print(f"  [OK] {x['name']} ({x['elapsed_ms']}ms) keys={keys}")
        else:
            print(f"  [FAIL] {x['name']} ({x['elapsed_ms']}ms) error={x['error'][:200]}")
    # 落盘
    with open(r"D:\B166ER-OpenClaw\workspace\toolbox\_subagent_trendradar_raw.json", "w", encoding="utf-8") as f:
        json.dump(r, f, ensure_ascii=False, indent=2)
    print("\n[SCAN] raw results dumped to toolbox/_subagent_trendradar_raw.json")