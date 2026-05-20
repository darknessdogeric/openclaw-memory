# -*- coding: utf-8 -*-
"""分析 i.meituan.com/hotel/481488.html - 可能是酒店详情页"""
import re, json
from curl_cffi import requests as curl_requests

# 用 curl_cffi 直接获取（轻量）
resp = curl_requests.get(
    "https://i.meituan.com/hotel/481488.html",
    impersonate="chrome120",
    headers={"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15"},
    timeout=15
)

html = resp.text
print(f"Status: {resp.status_code}, Size: {len(html):,} chars")
print(f"Final URL: {resp.url[:120]}")

# 搜关键数据
keywords = ['hotelName','hotel_name','hotelId','hotel_id','poiName','poiId',
            'roomPrice','room_price','lowestPrice','lowest_price','price',
            'address','addr','rating','score','comment','review',
            'name','title','hotel','poi','room','booking','reserve',
            '¥','元','起']

print("\n=== 关键词扫描 ===")
for kw in keywords:
    cnt = html.count(kw)
    if cnt > 0:
        print(f'  "{kw}": {cnt}')

# 搜 script 中的 JSON
print("\n=== Script JSON ===")
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
for i, s in enumerate(scripts):
    if len(s) > 1000:
        # 检查内容
        has_data = any(k in s for k in ['poi','hotel','price','room','name','title','address'])
        if has_data:
            print(f"  Script[{i}] ({len(s):,} chars):")
            # 尝试提取JSON-LD
            jsonld = re.search(r'application/ld\+json[^>]*>(.*?)</script>', html, re.DOTALL)
            if jsonld:
                print(f"    JSON-LD: {jsonld.group(1)[:500]}")
            
            # 找 window 变量
            for var in ['__NEXT_DATA__','__NUXT__','__INITIAL_STATE__','__DATA__',
                       'window.__PRELOADED_STATE__','hotelInfo','poiInfo','detailInfo']:
                idx = s.find(var)
                if idx >= 0:
                    print(f"    {var} at pos {idx}:")
                    print(f"    {s[idx:idx+300]}")

# 搜 schema.org
print("\n=== Schema.org ===")
for m in re.finditer(r'itemprop="([^"]+)"[^>]*>([^<]+)', html):
    if m.group(1) in ['name','price','address','ratingValue','telephone']:
        print(f"  itemprop={m.group(1)}: {m.group(2).strip()[:80]}")

# 搜 meta 标签
print("\n=== Meta ===")
for m in re.finditer(r'<meta[^>]+>', html):
    name = re.search(r'name="([^"]+)"', m.group())
    content = re.search(r'content="([^"]+)"', m.group())
    if name and content:
        nm = name.group(1)
        val = content.group(1)[:120]
        if any(k in nm for k in ['title','description','keyword','hotel','poi','price']):
            print(f"  {nm}: {val}")

# 看看URL是否重定向到搜索页
print(f"\n=== 页面分析 ===")
if 'search' in resp.url:
    print(f"  ⚠️ 重定向到搜索页")
elif 'detail' in resp.url:
    print(f"  ✅ 正确到达详情页")
elif 'hotel' in resp.url:
    print(f"  🟡 酒店相关页")
else:
    print(f"  ❓ 未知页面: {resp.url}")

# 保存样本供 Playwright 深度分析
with open("cache/ota_monitor/meituan_detail_481488.html", "w", encoding="utf-8") as f:
    f.write(html)
print(f"\n已保存: cache/ota_monitor/meituan_detail_481488.html")
