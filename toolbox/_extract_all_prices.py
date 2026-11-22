#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""综合提取所有平台关键商品数据 → 写入报告用JSON"""
import sys, os, json, re
from html import unescape

with open(r'D:\B166ER-OpenClaw\workspace\toolbox\_xiaoland_deepdive.json', 'r', encoding='utf-8') as f:
    deep = json.load(f)

with open(r'D:\B166ER-OpenClaw\workspace\toolbox\_xiaoland_scan.json', 'r', encoding='utf-8') as f:
    scan = json.load(f)

# === 1688 智驾蓝色装饰灯 - 全量解析 ===
print("=" * 80)
print("1688 智驾蓝色装饰灯 (beginPage=3) - 全量商品")
print("=" * 80)
c = deep.get('1688_zhijia_blue', {}).get('content', '')

# Pattern: 标题... 价 ... ¥x.xx ... 成交 X 笔
# 1688 商品列表格式: <a title="商品名">商品名</a> ... 价格: <span class="...">¥x.xx</span> ... 成交X笔
# Find by tile attributes and their surroundings

# 抓 title 列表 + 价格 + 成交
products = []
# Use regex to find blocks
# Pattern: title="([^"]+)" ... ¥(\d+\.\d+) ... 成交\s*(\d+)\s*笔
block_pat = re.compile(r'title="([^"]{15,100})"[^¥]{0,500}?￥([\d.]+)[^成]{0,200}?成交\s*(\d+)\s*笔', re.DOTALL)
for m in block_pat.finditer(c):
    title = unescape(m.group(1))
    price = m.group(2)
    tx = m.group(3)
    products.append({'title': title, 'price': price, 'transactions': tx, 'source': '1688_zhijia_blue'})

print(f"Found {len(products)} products with title+price+transactions:")
for p in products:
    print(f"  ¥{p['price']:>8} | 成交{p['transactions']:>4}笔 | {p['title'][:60]}")

# === 1688 激光雷达装饰灯 - 全量解析 ===
print("\n\n" + "=" * 80)
print("1688 激光雷达装饰灯 - 全量商品")
print("=" * 80)
c2 = deep.get('1688_laserradar', {}).get('content', '')
products2 = []
for m in block_pat.finditer(c2):
    title = unescape(m.group(1))
    price = m.group(2)
    tx = m.group(3)
    products2.append({'title': title, 'price': price, 'transactions': tx, 'source': '1688_laserradar'})

print(f"Found {len(products2)} products:")
for p in products2:
    print(f"  ¥{p['price']:>8} | 成交{p['transactions']:>4}笔 | {p['title'][:60]}")

# === 拼多多 真实搜索结果 ===
# 拼多多 mobile 页面是 JS 渲染,只有骨架。试试 web_fetch
print("\n\n" + "=" * 80)
print("拼多多 search - 提取标题")
print("=" * 80)
cpdd = deep.get('pdd_xiaoland', {}).get('content', '')
# Look for product patterns
# 拼多多通常在 SSR HTML 中有 goods_name 字段
pdd_names = re.findall(r'goods_name[^"]*"([^"]+)"', cpdd)
print(f"Found {len(pdd_names)} goods_name. Sample: {pdd_names[:10]}")
# 抓 title
pdd_titles = re.findall(r'"title"\s*:\s*"([^"]{5,80})"', cpdd)
print(f"Found {len(pdd_titles)} titles. Sample: {pdd_titles[:10]}")
# 抓 price
pdd_prices = re.findall(r'"price"\s*:\s*([\d.]+)', cpdd)
print(f"Found {len(pdd_prices)} prices. Sample: {pdd_prices[:30]}")
# 抓 sales
pdd_sales = re.findall(r'"sales"\s*:\s*(\d+)', cpdd)
print(f"Found {len(pdd_sales)} sales. Sample: {pdd_sales[:30]}")
# 抓 salesTip
pdd_tip = re.findall(r'"salesTip"\s*:\s*"([^"]+)"', cpdd)
print(f"Found {len(pdd_tip)} salesTip. Sample: {pdd_tip[:10]}")

# Look for any Chinese 商品名 patterns
cn_names = re.findall(r'"([^"]{8,40}小蓝灯[^"]{0,30})"', cpdd)
print(f"\nFound {len(cn_names)} '小蓝灯' mentions in JSON. Sample:")
for n in cn_names[:10]:
    print(f"  - {unescape(n)}")

# === 京东 汽车太阳能警示灯 chanpin/3363093 (130KB) ===
print("\n\n" + "=" * 80)
print("京东 汽车太阳能警示灯 chanpin/3363093 - 商品列表")
print("=" * 80)
jd = deep.get('jd_zhinengzhui', {}).get('content', '')
# 京东商品在 JSON 里: window.SEARCH_CONFIG 或 JDA商品数据
# Search for keyword patterns with ¥
jd_titles = re.findall(r'"skuTitle"\s*:\s*"([^"]{5,80})"', jd)
print(f"skuTitle: {len(jd_titles)}")
for t in jd_titles[:30]:
    print(f"  - {unescape(t)}")
# 京东价格通常在 J_price 或 p:
jd_prices = re.findall(r'"p"\s*:\s*"([\d.]+)"', jd)
print(f"\nprices: {len(jd_prices)}. Sample: {jd_prices[:30]}")
# 评论数
jd_comments = re.findall(r'"commentCountStr"\s*:\s*"([^"]+)"', jd)
print(f"\ncommentCountStr: {len(jd_comments)}. Sample: {jd_comments[:30]}")

# Try alt pattern for JD
jd_alt = re.findall(r'j_price">\s*<i>¥</i>\s*<em>([\d.]+)</em>', jd)
print(f"\nj_price alt pattern: {len(jd_alt)}")
jd_alt2 = re.findall(r'class="p-price"[^>]*>\s*<strong[^>]*>¥</strong>\s*<em>([\d.]+)</em>', jd)
print(f"p-price pattern: {len(jd_alt2)}")

# Look for product names with "小蓝灯" / "智驾" / "蓝灯" in JD
print("\nJD keywords:")
for kw in ['小蓝灯', '智驾', '太阳能警示', '智驾小蓝灯', '激光雷达', '领航灯']:
    cn = re.findall(rf'"([^"{{}}]{{5,80}}{re.escape(kw)}[^"{{}}]{{0,30}})"', jd)
    print(f"  [{kw}]: {len(cn)} matches")
    for n in cn[:5]:
        print(f"    - {unescape(n)}")

# === 淘宝 wave 1 抓取 ===
print("\n\n" + "=" * 80)
print("淘宝 wave 1 (来自 Tavily 搜索结果)")
print("=" * 80)
taobao_data = []
for q in scan['taobao']['queries']:
    snippet = q.get('snippet_preview', '')
    # 抓价格
    prices = re.findall(r'￥\s*([\d.]+)', snippet)
    # 抓已售
    sold = re.findall(r'已售\s*(\d+)', snippet)
    # 抓评论
    reviews = re.findall(r'(\d+)\s*条?评价', snippet)
    # 抓100+
    plus = re.findall(r'(\d+\+?)', snippet)
    
    print(f"\n  [{q['keyword']}]: prices={prices}, sold={sold}, reviews={reviews}")
    if '淘宝' in snippet or 'taobao' in q.get('query', '').lower():
        # 提取商品标题 (heuristic)
        titles = re.findall(r'【([^】]{5,60})】', snippet)
        if titles:
            print(f"    titles: {titles[:3]}")
        taobao_data.append({
            'keyword': q['keyword'],
            'prices': prices,
            'sold': sold,
            'reviews': reviews,
            'titles': titles[:3] if titles else [],
            'snippet': snippet[:300],
        })

# === Save all findings ===
out = {
    '1688_zhijia_blue_products': products,
    '1688_laserradar_products': products2,
    'pdd_extracts': {
        'goods_names': pdd_names,
        'prices': pdd_prices,
        'sales': pdd_sales,
        'sales_tip': pdd_tip,
        'titles_with_xiaoland': cn_names,
    },
    'jd_extracts': {
        'sku_titles': jd_titles,
        'prices': jd_prices,
        'comment_count_str': jd_comments,
    },
    'taobao_wave1': taobao_data,
}

with open(r'D:\B166ER-OpenClaw\workspace\toolbox\_xiaoland_extracts.json', 'w', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2)
print(f"\n\n[SAVE] -> _xiaoland_extracts.json")