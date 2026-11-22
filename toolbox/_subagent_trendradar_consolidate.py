"""Consolidate TrendRadar scan results into the requested JSON shape"""
import json
from datetime import datetime

RAW = r"D:\B166ER-OpenClaw\workspace\toolbox\_subagent_trendradar_raw.json"
OUT = r"D:\B166ER-OpenClaw\workspace\toolbox\_subagent_trendradar_consolidated_v2.json"

raw = json.load(open(RAW, encoding="utf-8"))
by_name = {x["name"]: x for x in raw}

# ---- top_events ----
topics_data = by_name["get_trending_topics"]["data"]
top_events = []
for t in topics_data["topics"]:
    top_events.append({
        "rank": len(top_events) + 1,
        "keyword": t["keyword"],
        "frequency": t["frequency"],
        "matched_news": t["matched_news"],
        "trend": t["trend"],
        "weight_score": t.get("weight_score", 0),
    })

# ---- hotel_sentiment ----
hotel_raw = by_name["analyze_sentiment_hotel"]["data"]
hotel_sentiment = {
    "success": hotel_raw.get("success", False),
    "error": hotel_raw.get("error"),
    "note": "今日(2026-07-28) TrendRadar 监控源中未出现「酒店」关键词相关新闻",
}

# ---- ai_sentiment ----
ai_raw = by_name["analyze_sentiment_ai"]["data"]
ai_news = ai_raw.get("data", [])
ai_sentiment = {
    "success": ai_raw.get("success", False),
    "topic": ai_raw.get("summary", {}).get("topic", "AI"),
    "time_range": ai_raw.get("summary", {}).get("time_range", "2026-07-28"),
    "total_found": ai_raw.get("summary", {}).get("total_found", len(ai_news)),
    "platforms": ai_raw.get("summary", {}).get("platforms", []),
    "sorted_by_weight": ai_raw.get("summary", {}).get("sorted_by_weight", True),
    "news": ai_news,
    "method": ai_raw.get("method"),
    "usage_note": ai_raw.get("usage_note"),
    "ai_prompt_preview": (ai_raw.get("ai_prompt") or "")[:200] + "..." if ai_raw.get("ai_prompt") else None,
}

# ---- reits_trend ----
reits_raw = by_name["analyze_topic_trend_reits"]["data"]
reits_trend = {
    "success": reits_raw.get("success", False),
    "topic": reits_raw.get("summary", {}).get("topic", "酒店REITs"),
    "date_range": reits_raw.get("summary", {}).get("date_range"),
    "granularity": reits_raw.get("summary", {}).get("granularity", "day"),
    "total_mentions": reits_raw.get("summary", {}).get("total_mentions", 0),
    "average_mentions": reits_raw.get("summary", {}).get("average_mentions", 0),
    "peak_count": reits_raw.get("summary", {}).get("peak_count", 0),
    "peak_time": reits_raw.get("summary", {}).get("peak_time"),
    "change_rate": reits_raw.get("summary", {}).get("change_rate", 0),
    "trend_direction": reits_raw.get("summary", {}).get("trend_direction", "稳定"),
    "daily_series": reits_raw.get("data", []),
    "note": "酒店REITs 关键词在监控源4天内均无命中，关注度极低",
}

# ---- oil_trend ----
oil_raw = by_name["analyze_topic_trend_oil"]["data"]
oil_trend = {
    "success": oil_raw.get("success", False),
    "topic": oil_raw.get("summary", {}).get("topic", "油价"),
    "date_range": oil_raw.get("summary", {}).get("date_range"),
    "granularity": oil_raw.get("summary", {}).get("granularity", "day"),
    "total_mentions": oil_raw.get("summary", {}).get("total_mentions", 0),
    "average_mentions": oil_raw.get("summary", {}).get("average_mentions", 0),
    "peak_count": oil_raw.get("summary", {}).get("peak_count", 0),
    "peak_time": oil_raw.get("summary", {}).get("peak_time"),
    "change_rate": oil_raw.get("summary", {}).get("change_rate", 0),
    "trend_direction": oil_raw.get("summary", {}).get("trend_direction", "稳定"),
    "daily_series": oil_raw.get("data", []),
}

# ---- latest_news ----
ln_raw = by_name["get_latest_news"]["data"]
latest_news = []
for n in ln_raw.get("data", []):
    latest_news.append({
        "title": n.get("title"),
        "platform_id": n.get("platform"),
        "platform_name": n.get("platform_name"),
        "rank": n.get("rank"),
        "timestamp": n.get("timestamp"),
    })

# ---- meta ----
meta = {
    "scan_time": datetime.now().isoformat(timespec="seconds"),
    "scan_date": "2026-07-28",
    "tool_count": 6,
    "parallel": True,
    "latency_ms": {x["name"]: x["elapsed_ms"] for x in raw},
    "data_source": "TrendRadar MCP v6.10.0 (FastMCP 2.12.5)",
}

consolidated = {
    "meta": meta,
    "top_events": top_events,
    "hotel_sentiment": hotel_sentiment,
    "ai_sentiment": ai_sentiment,
    "reits_trend": reits_trend,
    "oil_trend": oil_trend,
    "latest_news": latest_news,
}

# Save
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(consolidated, f, ensure_ascii=False, indent=2)

# Print to stdout
# print(json.dumps(consolidated, ensure_ascii=False, indent=2))

# Also write to a temp file for clean stdout retrieval
import os, tempfile
with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8") as tf:
    json.dump(consolidated, tf, ensure_ascii=False, indent=2)
    tmp_path = tf.name
print("WROTE", tmp_path)