#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""更鲁棒地解析 1688 商品列表"""
import sys, os, json, re
from html import unescape

with open(r'D:\B166ER-OpenClaw\workspace\toolbox\_xiaoland_deepdive.json', 'r', encoding='utf-8') as f:
    deep = json.load(f)

c1688 = deep.get('1688_laserradar', {}).get('content', '')
print(f"1688_laserradar length: {len(c1688)}")

# Save raw HTML for inspection
with open(r'D:\B166ER-OpenClaw\workspace\toolbox\_1688_laserradar_raw.html', 'w', encoding='utf-8') as f:
    f.write(c1688)
print("Saved raw HTML to _1688_laserradar_raw.html")

# 1688 商品列表的常见结构:
# <a href="/offer/xxx.html" title="商品名">商品名</a>
# <div class="...">¥<span>xx.xx</span></div>
# <div class="...">xx 笔成交</div>

# 试着看价格上下文
idx = 0
count = 0
while idx < len(c1688):
    # Find next "￥" in HTML
    pos = c1688.find('￥', idx)
    if pos < 0 or count > 30: break
    snippet = c1688[max(0, pos-300):pos+500]
    # Strip HTML for readability
    snippet_clean = re.sub(r'<[^>]+>', '|', snippet)
    snippet_clean = re.sub(r'\s+', ' ', snippet_clean)
    snippet_clean = unescape(snippet_clean)
    print(f"\n=== Price @{pos} ===")
    print(snippet_clean[:600])
    print()
    idx = pos + 1
    count += 1

# Find all "成交" contexts
print("\n\n=== 成交 contexts ===")
idx = 0
count = 0
while idx < len(c1688):
    pos = c1688.find('成交', idx)
    if pos < 0 or count > 30: break
    snippet = c1688[max(0, pos-200):pos+200]
    snippet_clean = re.sub(r'<[^>]+>', '|', snippet)
    snippet_clean = re.sub(r'\s+', ' ', snippet_clean)
    snippet_clean = unescape(snippet_clean)
    print(f"\n  成交@{pos}: ...{snippet_clean[:300]}...")
    idx = pos + 2
    count += 1