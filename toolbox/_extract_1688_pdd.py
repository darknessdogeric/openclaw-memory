#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""解析 1688 / 京东/拼多多 真实商品数据"""
import sys, os, json, re
from html import unescape

with open(r'D:\B166ER-OpenClaw\workspace\toolbox\_xiaoland_deepdive.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def clean_html(content):
    text = re.sub(r'<script.*?</script>', ' ', content, flags=re.DOTALL)
    text = re.sub(r'<style.*?</style>', ' ', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = unescape(text)
    text = re.sub(r'\s+', ' ', text)
    return text

# === 1688 智驾蓝色装饰灯 - 131KB ===
print("=" * 80)
print("1688 智驾蓝色装饰灯 (beginPage=3)")
print("=" * 80)
c1688 = data.get('1688_zhijia_blue', {}).get('content', '')
t1688 = clean_html(c1688)

# 找价格 ¥x.x
prices = re.findall(r'￥\s*([\d.]+)', t1688)
print(f"Total ¥ prices found: {len(prices)}")
print(f"Sample: {prices[:40]}")
print()

# 找标题 (商品名前后的关键词)
# 1688 has "title=" attributes with the product name
titles = re.findall(r'title="([^"]{15,80})"', c1688)
print(f"\nFound {len(titles)} titles in title= attribute. Sample:")
for t in titles[:30]:
    print(f"  - {t}")

# Find 成交 X 笔
transactions = re.findall(r'成交\s*(\d+)\s*笔', t1688)
print(f"\nFound {len(transactions)} '成交 X 笔' phrases. Sample: {transactions[:30]}")

# Find 评价
reviews = re.findall(r'(\d+)\s*条评价', t1688)
print(f"\nFound {len(reviews)} '条评价' phrases. Sample: {reviews[:30]}")

# Find 蓝灯 / 智驾 / 装饰 关键词上下文
print("\n=== 蓝灯/智驾上下文 ===")
for kw in ['智驾蓝灯', '智驾小蓝灯', '蓝灯', '太阳能LED', '激光雷达']:
    idx = 0
    count = 0
    while idx < len(t1688):
        found = t1688.find(kw, idx)
        if found < 0 or count > 5: break
        snippet = t1688[max(0, found-80):found+150]
        print(f"  [{kw}]: ...{snippet}...")
        idx = found + len(kw)
        count += 1

# === 1688 激光雷达装饰灯 - 133KB ===
print("\n\n" + "=" * 80)
print("1688 激光雷达装饰灯")
print("=" * 80)
c1688b = data.get('1688_laserradar', {}).get('content', '')
t1688b = clean_html(c1688b)

prices_b = re.findall(r'￥\s*([\d.]+)', t1688b)
print(f"Total ¥ prices: {len(prices_b)}")
print(f"Sample: {prices_b[:50]}")

titles_b = re.findall(r'title="([^"]{15,80})"', c1688b)
print(f"\nTitles ({len(titles_b)}):")
for t in titles_b[:30]:
    print(f"  - {t}")

trans_b = re.findall(r'成交\s*(\d+)\s*笔', t1688b)
print(f"\nTransactions: {trans_b[:30]}")

print("\n=== 激光雷达装饰上下文 ===")
for kw in ['激光雷达', '防追尾', '智驾']:
    idx = 0
    count = 0
    while idx < len(t1688b):
        found = t1688b.find(kw, idx)
        if found < 0 or count > 5: break
        snippet = t1688b[max(0, found-80):found+150]
        print(f"  [{kw}]: ...{snippet}...")
        idx = found + len(kw)
        count += 1

# === 拼多多 搜索页 - 47KB ===
print("\n\n" + "=" * 80)
print("拼多多 mobile search")
print("=" * 80)
cpdd = data.get('pdd_xiaoland', {}).get('content', '')
tpdd = clean_html(cpdd)
print(f"Length: {len(tpdd)}")
print(f"First 2000: {tpdd[:2000]}")