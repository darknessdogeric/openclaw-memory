"""TrendRadar 地缘政治新闻扫描 v2 - 2026-08-25
换用英文关键词搜7天RSS
"""
import asyncio
import json
import sys
import time
import traceback

TR_ROOT = r"D:\B166ER-OpenClaw\workspace\trendradar"
sys.path.insert(0, TR_ROOT)

from mcp_server import server as _srv

search_news = _srv.search_news.fn
search_rss  = _srv.search_rss.fn

# 中英双轨 + 英文放宽到7天
QUERIES = [
    # (keyword, days, limit)
    ("伊朗",      1, 20),
    ("以色列",    1, 20),
    ("乌克兰",    1, 20),
    ("俄罗斯",    1, 20),
    ("中东",      1, 20),
    ("台海",      1, 20),
    ("南海",      1, 20),
    ("中美关系",  1, 20),
    # 英文放宽
    ("Iran",      7, 20),
    ("Israel",    7, 20),
    ("Ukraine",   7, 20),
    ("Russia",    7, 20),
    ("Middle East", 7, 20),
    ("Taiwan",    7, 20),
    ("South China Sea", 7, 20),
    ("China US relations", 7, 20),
    ("geopolitics", 7, 20),
]

DATE_RANGE = {"start": "2026-08-25", "end": "2026-08-25"}


async def safe_call(name, coro):
    t0 = time.time()
    try:
        raw = await coro
        try:
            parsed = json.loads(raw)
        except Exception:
            parsed = {"raw": raw[:500]}
        elapsed = round((time.time() - t0) * 1000, 1)
        return {"ok": True, "name": name, "elapsed_ms": elapsed, "data": parsed}
    except Exception as e:
        elapsed = round((time.time() - t0) * 1000, 1)
        return {
            "ok": False, "name": name, "elapsed_ms": elapsed,
            "error": str(e)[:200], "traceback": traceback.format_exc()[-300:],
        }


async def main():
    print("[GEO v2] TrendRadar 地缘政治扫描 @ 2026-08-25", flush=True)

    tasks = []
    for kw, days, limit in QUERIES:
        tasks.append(safe_call(
            f"news:{kw}",
            search_news(query=kw, date_range=DATE_RANGE, limit=limit,
                        include_url=False, include_rss=True, rss_limit=limit)
        ))
        tasks.append(safe_call(
            f"rss:{kw}",
            search_rss(keyword=kw, days=days, limit=limit, include_summary=True)
        ))

    results = await asyncio.gather(*tasks, return_exceptions=False)
    return results


if __name__ == "__main__":
    t0_global = time.time()
    raw_results = asyncio.run(main())

    print(f"\n扫描完成 | 耗时 {round((time.time()-t0_global)*1000)}ms")

    # 去重收集所有新闻
    seen_titles = set()
    all_items = []

    # 按关键词聚合输出
    by_kw = {}
    for r in raw_results:
        parts = r["name"].split(":", 1)
        kind = parts[0]
        kw   = parts[1] if len(parts) > 1 else "?"
        if kw not in by_kw:
            by_kw[kw] = {}
        by_kw[kw][kind] = r

    for kw, sources in by_kw.items():
        print(f"\n### {kw}")

        # search_news 结果
        news_r = sources.get("news", {})
        if news_r.get("ok"):
            d = news_r["data"]
            hot = d.get("hot", []) if isinstance(d, dict) else []
            rss = d.get("rss", []) if isinstance(d, dict) else []
            print(f"  热榜: {len(hot)} 条 | RSS(in-news): {len(rss)} 条")
            for it in hot[:5]:
                t = it.get("title", "")
                p = it.get("platform_name", it.get("platform", ""))
                s = it.get("summary", it.get("content", ""))
                if t and t not in seen_titles:
                    seen_titles.add(t)
                    all_items.append({"keyword": kw, "source": "hot", "title": t,
                                      "platform": p, "summary": s[:200]})
                    print(f"    [HOT:{p}] {t[:70]}")
            for it in rss[:3]:
                t = it.get("title", "")
                p = it.get("feed_name", it.get("feed_id", ""))
                s = it.get("summary", "")
                if t and t not in seen_titles:
                    seen_titles.add(t)
                    all_items.append({"keyword": kw, "source": "rss_hot", "title": t,
                                      "platform": p, "summary": s[:200]})
                    print(f"    [RSS_HOT:{p}] {t[:70]}")
        else:
            print(f"  热榜 FAIL: {news_r.get('error','?')[:100]}")

        # 独立 RSS 结果
        rss_r = sources.get("rss", {})
        if rss_r.get("ok"):
            d = rss_r["data"]
            items = d.get("data", []) if isinstance(d, dict) else []
            print(f"  独立RSS: {len(items)} 条")
            for it in items[:5]:
                t = it.get("title", "")
                p = it.get("feed_name", it.get("feed_id", ""))
                s = it.get("summary", "")
                if t and t not in seen_titles:
                    seen_titles.add(t)
                    all_items.append({"keyword": kw, "source": "rss", "title": t,
                                      "platform": p, "summary": s[:200]})
                    print(f"    [RSS:{p}] {t[:70]}")
        else:
            print(f"  独立RSS FAIL: {rss_r.get('error','?')[:100]}")

    # 输出 JSON
    out = {
        "date": "2026-08-25",
        "keywords_searched": [q[0] for q in QUERIES],
        "total_unique_items": len(all_items),
        "news": all_items
    }

    out_path = r"D:\B166ER-OpenClaw\workspace\toolbox\_subagent_geopolitics_20260825_v2.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"\n[OUTPUT] -> {out_path}")
    print(f"[DONE] 去重后共 {len(all_items)} 条")
