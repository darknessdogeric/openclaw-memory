#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""解析 _xiaoland_deepdive.json 中的京东/1688/拼多多数据,提取真实商品价格销量"""
import sys, os, json, re
from html import unescape

OUT = []
with open(r'D:\B166ER-OpenClaw\workspace\toolbox\_xiaoland_deepdive.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 京东 汽车灯光改装 - 25689 bytes
print("=" * 80)
print("京东 汽车灯光改装 chanpin/1712026")
print("=" * 80)
jd1 = data.get('jd_qichezhaungshi', {})
content = jd1.get('content', '')

# Strip HTML
text = re.sub(r'<[^>]+>', ' ', content)
text = unescape(text)
text = re.sub(r'\s+', ' ', text)

# Find product blocks - look for prices, names
# Strategy: find pattern of "title" + "price" pairs
print("Sample (first 3000 chars):")
print(text[:3000])
print("\n\n")

# Find ¥xxx prices
prices = re.findall(r'￥\s*(\d+(?:\.\d+)?)', text)
print(f"\nFound {len(prices)} ¥ prices. Sample: {prices[:30]}")

# Find titles with "蓝灯" or "小蓝灯" or "智驾"
for kw in ['小蓝灯', '智驾', '蓝灯', '装饰灯', '指示灯']:
    idx = 0
    while idx < len(text):
        found = text.find(kw, idx)
        if found < 0: break
        snippet = text[max(0, found-100):found+200]
        print(f"\n  [{kw}] @{found}: ...{snippet}...")
        idx = found + len(kw)