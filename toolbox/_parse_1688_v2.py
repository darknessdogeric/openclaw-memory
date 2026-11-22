#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""精确解析 1688 商品列表 - 标题/价格/成交量三元组"""
import sys, os, json, re
from html import unescape

with open(r'D:\B166ER-OpenClaw\workspace\toolbox\_xiaoland_deepdive.json', 'r', encoding='utf-8') as f:
    deep = json.load(f)

# 1688 商品列表 HTML 结构(已观察):
# <a href="..." title="完整商品标题">...</a>...¥|price|...成交|count|笔

def extract_products(html, source_name):
    """Extract (title, price, transactions) triples from 1688 search page."""
    products = []
    # 找带 title 的 a 标签 (1688 商品)
    # Pattern: title="([^"]+)" [^<]* ... 楼 \| ([\d.]+) \| [^成交]* 成交 \| (\d+) \| 笔
    # Use lazy quantifier
    
    # 用一个更宽容的pattern:title -> 楼 price -> 成交 count 笔 (within ~1500 chars)
    pattern = re.compile(
        r'title="([^"]{15,150})".*?楼\|([\d.]+)\|.*?成交\|(\d+)\|笔',
        re.DOTALL
    )
    
    matches = pattern.findall(html)
    for title, price, tx in matches:
        products.append({
            'title': unescape(title),
            'price': float(price),
            'transactions': int(tx),
            'source': source_name,
        })
    return products

# === 1688 智驾蓝色装饰灯 (beginPage=3) ===
c1 = deep.get('1688_zhijia_blue', {}).get('content', '')
p1 = extract_products(c1, '1688_zhijia_blue')
print(f"1688_zhijia_blue: {len(p1)} products")

# === 1688 激光雷达装饰灯 ===
c2 = deep.get('1688_laserradar', {}).get('content', '')
p2 = extract_products(c2, '1688_laserradar')
print(f"1688_laserradar: {len(p2)} products")

# Print results
print("\n=== 1688 智驾蓝色装饰灯 ===")
for p in p1:
    print(f"  ¥{p['price']:>8.2f} | {p['transactions']:>5} 笔 | {p['title'][:60]}")

print("\n=== 1688 激光雷达装饰灯 ===")
for p in p2:
    print(f"  ¥{p['price']:>8.2f} | {p['transactions']:>5} 笔 | {p['title'][:60]}")

# === Save ===
out = {
    '1688_zhijia_blue': p1,
    '1688_laserradar': p2,
}
with open(r'D:\B166ER-OpenClaw\workspace\toolbox\_1688_products.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(f"\nSaved {len(p1)+len(p2)} products to _1688_products.json")

# === Aggregate stats ===
all_1688 = p1 + p2
if all_1688:
    prices = [p['price'] for p in all_1688]
    txs = [p['transactions'] for p in all_1688]
    print(f"\n1688 价格区间: ¥{min(prices)} - ¥{max(prices)}, 中位数: ¥{sorted(prices)[len(prices)//2]:.2f}")
    print(f"1688 总成交笔数: {sum(txs)}")
    print(f"1688 单品最高成交: {max(txs)}笔 ({next(p['title'][:40] for p in all_1688 if p['transactions']==max(txs))})")
    
    # 按关键词过滤"小蓝灯/智驾"
    xiaoland_products = [p for p in all_1688 if any(kw in p['title'] for kw in ['智驾', '蓝灯', '智驾蓝灯', '领航灯'])]
    print(f"\n1688 含'智驾/蓝灯'关键词的商品: {len(xiaoland_products)}")
    for p in xiaoland_products[:15]:
        print(f"  ¥{p['price']:>8.2f} | {p['transactions']:>5} 笔 | {p['title'][:60]}")