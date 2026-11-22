"""TrendRadar 地缘政治新闻扫描 - 2026-08-25
Subagent: b4a40737-a847-4f2d-a840-eef700cffe93
并行搜索8个关键词: 伊朗、以色列、乌克兰、俄罗斯、中东、台海、南海、中美关系
limit=20, include_rss=True
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
search_news         = _srv.search_news.fn
search_rss          = _srv.search_rss.fn


KEYWORDS = [
    "伊朗", "以色列", "乌克兰", "俄罗斯",
    "中东", "台海", "南海", "中美关系"
]
DATE_RANGE = {"start": "2026-08-25", "end": "2026-08-25"}
LIMIT = 20


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
            "ok": False, "name": name, "elapsed_ms": elapsed,
            "error": str(e), "traceback": traceback.format_exc(),
        }


async def main():
    print("[GEO] TrendRadar 地缘政治扫描 @ 2026-08-25", flush=True)

    tasks = []
    for kw in KEYWORDS:
        # search_news (热榜) + search_rss 并行
        tasks.append(safe_call(
            f"news:{kw}",
            search_news(query=kw, date_range=DATE_RANGE, limit=LIMIT,
                        include_url=False, include_rss=True, rss_limit=LIMIT)
        ))
        tasks.append(safe_call(
            f"rss:{kw}",
            search_rss(keyword=kw, days=1, limit=LIMIT, include_summary=True)
        ))

    results = await asyncio.gather(*tasks, return_exceptions=False)

    # 按关键词聚合
    consolidated = {}
    for r in results:
        parts = r["name"].split(":", 1)
        kind = parts[0]   # "news" | "rss"
        kw   = parts[1] if len(parts) > 1 else "?"
        if kw not in consolidated:
            consolidated[kw] = {}
        consolidated[kw][kind] = r

    return consolidated, results


if __name__ == "__main__":
    t0_global = time.time()
    consolidated, raw = asyncio.run(main())

    # 汇总输出
    print(f"\n{'='*60}")
    print(f"扫描完成 | 耗时 {round((time.time()-t0_global)*1000)}ms")
    print(f"{'='*60}")

    all_items = []
    for kw, sources in consolidated.items():
        print(f"\n### {kw}")

        # --- 热榜新闻 ---
        news_r = sources.get("news", {})
        if news_r.get("ok"):
            d = news_r["data"]
            hot  = d.get("hot", [])
            rss  = d.get("rss", [])
            print(f"  热榜命中: {len(hot)} 条")
            for it in hot[:5]:
                title   = it.get("title", "")
                platform = it.get("platform_name", it.get("platform", ""))
                rank    = it.get("rank", "")
                item = {"keyword": kw, "source": "hot", "title": title,
                        "platform": platform, "rank": rank,
                        "summary": it.get("summary", it.get("content", ""))}
                all_items.append(item)
                print(f"    [{platform} #{rank}] {title[:60]}")
            print(f"  RSS命中: {len(rss)} 条")
            for it in rss[:5]:
                title  = it.get("title", "")
                feed   = it.get("feed_name", it.get("feed_id", ""))
                item = {"keyword": kw, "source": "rss_hot", "title": title,
                        "platform": feed,
                        "summary": it.get("summary", it.get("description", ""))}
                all_items.append(item)
                print(f"    [RSS:{feed}] {title[:60]}")
        else:
            print(f"  热榜 FAIL: {news_r.get('error','?')[:80]}")

        # --- 纯RSS源 ---
        rss_r = sources.get("rss", {})
        if rss_r.get("ok"):
            d = rss_r["data"]
            items = d.get("data", []) if isinstance(d, dict) else []
            print(f"  独立RSS命中: {len(items)} 条")
            for it in items[:5]:
                title  = it.get("title", "")
                feed   = it.get("feed_name", it.get("feed_id", ""))
                item = {"keyword": kw, "source": "rss", "title": title,
                        "platform": feed,
                        "summary": it.get("summary", it.get("description", ""))}
                all_items.append(item)
                print(f"    [RSS:{feed}] {title[:60]}")
        else:
            print(f"  独立RSS FAIL: {rss_r.get('error','?')[:80]}")

    # 输出最终 JSON
    out = {
        "date": "2026-08-25",
        "keywords": KEYWORDS,
        "total_items": len(all_items),
        "news": all_items
    }

    out_path = r"D:\B166ER-OpenClaw\workspace\toolbox\_subagent_geopolitics_20260825.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"\n[OUTPUT] → {out_path}")
    print(f"[DONE] 共计 {len(all_items)} 条新闻")
