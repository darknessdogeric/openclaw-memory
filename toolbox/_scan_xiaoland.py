#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""小蓝灯电商平台穷尽式扫描 - B166ER 子任务"""
import sys
import os
import json
import re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Force UTF-8
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['PYTHONUTF8'] = '1'

from scrape_matrix import scrape, scrape_search, matrix_report

KEYWORDS = [
    "小蓝灯 新能源",
    "智驾小蓝灯",
    "辅助驾驶指示灯",
    "自动驾驶灯 外挂",
    "智驾指示灯 后装",
    "ADB 蓝灯 汽车",
    "激光雷达装饰灯",
    "智能驾驶灯 装饰",
]

PLATFORMS = {
    "taobao":    "site:taobao.com",
    "pdd":       "site:pinduoduo.com",
    "jd":        "site:jd.com",
    "1688":      "site:1688.com",
    "douyin":    "site:xiaohongshu.com OR site:jinritemai.com OR site:shop.douyin.com",
    "xhs":       "site:xiaohongshu.com 商城",
    "xianyu":    "site:goofish.com OR site:xianyu",
    "suning":    "site:suning.com",
    "dewu":      "site:dewu.com",
}

results = {}

# Step 1: Run searches per platform x keyword combination
print(f"[*] 启动: 矩阵状态")
print(matrix_report())
print(f"\n[*] 关键词数: {len(KEYWORDS)}")
print(f"[*] 平台数: {len(PLATFORMS)}")
print(f"[*] 总搜索组合: {len(KEYWORDS) * len(PLATFORMS)}")
print("=" * 80)

# Save results to a JSON file as we go
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_xiaoland_scan.json')

def run_search(platform_label, query):
    """Run a Tavily-style search via scrape_matrix."""
    try:
        r = scrape_search(query, max_results=8)
        return {
            "tool": r.tool_used,
            "url": r.url if hasattr(r, 'url') else "",
            "content": r.content if hasattr(r, 'content') else "",
            "ok": r.ok if hasattr(r, 'ok') else True,
        }
    except Exception as e:
        return {"tool": "ERROR", "error": str(e), "ok": False}

# Step 2: Platform-by-platform deep search
for platform_label, site_filter in PLATFORMS.items():
    print(f"\n\n========== 平台: {platform_label} ==========")
    results[platform_label] = {
        "queries": [],
        "top_products": [],
        "comments_samples": [],
        "platform_url_attempts": [],
    }

    # 2a. Each keyword with site filter
    for kw in KEYWORDS:
        q = f"{site_filter} {kw}"
        print(f"\n[{platform_label}] 关键词: {kw}")
        print(f"  query: {q}")
        r = run_search(platform_label, q)
        results[platform_label]["queries"].append({
            "keyword": kw,
            "query": q,
            "result_count": len(r.get("content", "")),
            "tool": r.get("tool"),
            "snippet_preview": r.get("content", "")[:600],
            "ok": r.get("ok"),
        })
        # Print short preview
        preview = r.get("content", "")[:300].replace("\n", " | ")
        print(f"  -> tool: {r.get('tool')}, preview: {preview[:200]}...")

    # Save incrementally
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"\n[SAVE] 已写入 {out_path}")

print("\n\n[DONE] 全平台扫描完成")