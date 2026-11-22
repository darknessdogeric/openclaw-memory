#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""最后一波: 拼多多数字旮旯销量+京东数字旮旯商品+抖音商品"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ['PYTHONIOENCODING'] = 'utf-8'

from scrape_matrix import scrape_search

# 1. PDD 销量破解 - 找分析文章
print("=" * 80)
print("拼多多 小蓝灯 销量数据 - 间接源")
print("=" * 80)
pdd_qs = [
    "拼多多 小蓝灯 销量",
    "拼多多 智驾灯 销量 月销",
    "拼多多 数字旮旯 小米",
    "拼多多 新能源 装饰灯 月销",
    "拼多多 防追尾 激光灯 销量",
    "site:pinduoduo.com 小蓝灯",
    "pdd 智驾灯 评论",
    "拼多多 月销榜 智驾灯",
    "多多 智驾灯 数据",
]
pdd_results = []
for q in pdd_qs:
    print(f"\n[搜索] {q}")
    r = scrape_search(q, max_results=8)
    pdd_results.append({
        'q': q,
        'tool': r.tool_used,
        'content': r.content,
    })
    preview = r.content[:600].replace('\n', ' | ')
    print(f"  -> {r.tool_used}, len={len(r.content)}")
    print(f"  {preview[:400]}")

# 2. 京东 数字旮旯 具体商品
print("\n\n" + "=" * 80)
print("京东 数字旮旯 - 商品 + 销量 + 评价")
print("=" * 80)
jd_shuzhigala_qs = [
    "京东 数字旮旯 智驾灯 评价",
    "数字旮旯 智驾灯 京东 销量",
    "数字旮旯 小米 SU7 京东 商品",
    "数字旮旯 智驾灯 价格 399",
    "数字旮旯 YU7 评价",
    "site:item.jd.com 数字旮旯",
    "京东 智驾小蓝灯 排行榜",
    "京东 智驾小蓝灯 月销",
]
jd_results = []
for q in jd_shuzhigala_qs:
    print(f"\n[搜索] {q}")
    r = scrape_search(q, max_results=8)
    jd_results.append({
        'q': q,
        'tool': r.tool_used,
        'content': r.content,
    })
    preview = r.content[:600].replace('\n', ' | ')
    print(f"  -> {r.tool_used}, len={len(r.content)}")
    print(f"  {preview[:400]}")

# 3. 抖音/小红书 商城 数字旮旯 / 小蓝灯
print("\n\n" + "=" * 80)
print("抖音商城 + 小红书商城 - 小蓝灯 / 数字旮旯")
print("=" * 80)
dy_xhs_qs = [
    "抖音商城 小蓝灯",
    "抖音商城 智驾灯 价格",
    "抖音商城 数字旮旯 小米",
    "抖音商城 智驾小蓝灯",
    "抖音 商品 数字旮旯 销量",
    "小红书商城 小蓝灯",
    "小红书 智驾灯",
    "小红书商城 数字旮旯",
    "shop.douyin.com 小蓝灯",
    "小红书 智驾灯 月销",
]
dy_results = []
for q in dy_xhs_qs:
    print(f"\n[搜索] {q}")
    r = scrape_search(q, max_results=6)
    dy_results.append({
        'q': q,
        'tool': r.tool_used,
        'content': r.content,
    })
    preview = r.content[:500].replace('\n', ' | ')
    print(f"  -> {r.tool_used}, len={len(r.content)}")
    print(f"  {preview[:300]}")

# 4. 闲鱼/苏宁/得物 数据
print("\n\n" + "=" * 80)
print("闲鱼 / 苏宁 / 得物 - 小蓝灯相关")
print("=" * 80)
oth_qs = [
    "闲鱼 小蓝灯 新能源",
    "闲鱼 智驾灯 改装",
    "闲鱼 数字旮旯",
    "苏宁 小蓝灯",
    "苏宁 智驾灯 销量",
    "得物 小蓝灯",
    "得物 汽车装饰灯",
    "得物 新能源 改装",
]
oth_results = []
for q in oth_qs:
    print(f"\n[搜索] {q}")
    r = scrape_search(q, max_results=6)
    oth_results.append({
        'q': q,
        'tool': r.tool_used,
        'content': r.content,
    })
    preview = r.content[:500].replace('\n', ' | ')
    print(f"  -> {r.tool_used}, len={len(r.content)}")
    print(f"  {preview[:300]}")

# Save all
with open(r'D:\B166ER-OpenClaw\workspace\toolbox\_final_searches.json', 'w', encoding='utf-8') as f:
    json.dump({
        'pdd': pdd_results,
        'jd_shuzhigala': jd_results,
        'dy_xhs': dy_results,
        'other': oth_results,
    }, f, ensure_ascii=False, indent=2)
print(f"\n[SAVE] -> _final_searches.json")