#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""正确解析 1688 商品列表 - 实际是 UTF-8 中文"""
import sys, os, json, re
from html import unescape

with open(r'D:\B166ER-OpenClaw\workspace\toolbox\_xiaoland_deepdive.json', 'r', encoding='utf-8') as f:
    deep = json.load(f)

def extract_products(html, source_name):
    """Extract from 1688 HTML structure: title="..." + &yen;PRICE + 成交NUM笔"""
    products = []
    # Find product blocks
    # Pattern: title="(NAME)" ... &yen; PRICE ... 成交 NUM 笔
    pattern = re.compile(
        r'title="([^"]{10,150})"[\s\S]{0,3000}?<i>&yen;</i>([\d.]+)[\s\S]{0,500}?成交\s*<em>(\d+)</em>\s*笔',
        re.DOTALL
    )
    
    for m in pattern.finditer(html):
        title = unescape(m.group(1))
        price = float(m.group(2))
        tx = int(m.group(3))
        products.append({
            'title': title,
            'price': price,
            'transactions': tx,
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
print("\n=== 1688 智驾蓝色装饰灯 (前 30) ===")
for p in sorted(p1, key=lambda x: -x['transactions'])[:30]:
    print(f"  ¥{p['price']:>8.2f} | {p['transactions']:>5} 笔 | {p['title'][:70]}")

print("\n=== 1688 激光雷达装饰灯 (前 30) ===")
for p in sorted(p2, key=lambda x: -x['transactions'])[:30]:
    print(f"  ¥{p['price']:>8.2f} | {p['transactions']:>5} 笔 | {p['title'][:70]}")

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
    print(f"\n1688 价格区间: ¥{min(prices)} - ¥{max(prices)}")
    print(f"1688 中位价: ¥{sorted(prices)[len(prices)//2]:.2f}")
    print(f"1688 总成交笔数: {sum(txs)}")
    print(f"1688 单品最高成交: {max(txs)}笔 ({next(p['title'][:50] for p in all_1688 if p['transactions']==max(txs))})")
    
    # 按关键词过滤
    xiaoland_products = [p for p in all_1688 if any(kw in p['title'] for kw in ['智驾', '蓝灯', '智驾蓝灯', '领航灯'])]
    print(f"\n1688 含'智驾/蓝灯'关键词商品: {len(xiaoland_products)}")
    for p in sorted(xiaoland_products, key=lambda x: -x['transactions'])[:15]:
        print(f"  ¥{p['price']:>8.2f} | {p['transactions']:>5} 笔 | {p['title'][:70]}")
    
    # 按价格排序
    print(f"\n=== 最便宜的 10 个 ===")
    for p in sorted(all_1688, key=lambda x: x['price'])[:10]:
        print(f"  ¥{p['price']:>8.2f} | {p['transactions']:>5} 笔 | {p['title'][:70]}")
    
    print(f"\n=== 最贵的 10 个 ===")
    for p in sorted(all_1688, key=lambda x: -x['price'])[:10]:
        print(f"  ¥{p['price']:>8.2f} | {p['transactions']:>5} 笔 | {p['title'][:70]}")