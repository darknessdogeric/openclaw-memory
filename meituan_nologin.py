# -*- coding: utf-8 -*-
"""美团酒店 - 无登录方案: 首页数据 + 推荐API + 附近API"""
import json, re, time
from curl_cffi import requests as curl_requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
    "Accept": "application/json",
    "Referer": "https://i.meituan.com/hotel/xiangyang/",
}

# ════════════════════════════
# 方案A: 首页内嵌数据
# ════════════════════════════
print("=== A. 首页内嵌数据 ===")
resp = curl_requests.get("https://i.meituan.com/hotel/xiangyang/", impersonate="chrome120", 
                          headers={"User-Agent": HEADERS["User-Agent"]}, timeout=10)
html = resp.text
print(f"  页面: {len(html):,} chars, status={resp.status_code}")

# 搜所有 JSON 数据块
json_candidates = []
# 提取 script 标签内容
scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
for s in scripts:
    # 找 JSON 对象
    for m in re.finditer(r'\{[^{}]*"(?:poiList|hotelList|hotels|rooms|price|poi|recommend|nearby|featured)"[^{}]*\}', s):
        json_candidates.append(m.group())
    for m in re.finditer(r'\[[^\[\]]*"(?:name|title|price|id|poiId)"[^\[\]]*\]', s):
        if len(m.group()) > 50:
            json_candidates.append(m.group())

print(f"  JSON候选: {len(json_candidates)}")
for c in json_candidates[:5]:
    print(f"  {c[:200]}")

# 也找找 window.xxx 数据
for var in ['__NEXT_DATA__','__NUXT__','__INITIAL_STATE__','__DATA__','__PRELOADED_STATE__']:
    idx = html.find(var)
    if idx >= 0:
        print(f"  ✅ {var} at pos {idx}: {html[idx:idx+300]}")

# ════════════════════════════
# 方案B: 推荐/附近API (无需登录)
# ════════════════════════════
print("\n=== B. 推荐/附近API ===")
apis = [
    # 热门推荐
    "https://ihotel.meituan.com/group/v1/recommend/hot?cityId=774&limit=20&utm_medium=touch",
    # 附近酒店  
    "https://ihotel.meituan.com/group/v1/poi/nearby?cityId=774&lat=32.0090&lng=112.1225&limit=20&utm_medium=touch",
    # 榜单
    "https://ihotel.meituan.com/group/v1/ranking/list?cityId=774&type=hotel&utm_medium=touch",
    # 特价
    "https://ihotel.meituan.com/group/v1/deal/special?cityId=774&limit=20&utm_medium=touch",
    # 首页推荐poi
    "https://ihotel.meituan.com/group/v1/poi/recommend?cityId=774&startDate=2026-05-13&endDate=2026-05-14&limit=20&utm_medium=touch",
    # 猜你喜欢
    "https://ihotel.meituan.com/group/v1/poi/guess?cityId=774&limit=20&utm_medium=touch",
    # 城市热门酒店
    "https://ihotel.meituan.com/group/v1/city/hotpois?cityId=774&limit=20&utm_medium=touch",
    # campaign banner (可能含酒店)
    "https://ihotel.meituan.com/campaigns/v1/richman/batch/hit?app=group&category=1&cityId=774&platform=1&os=2&version=480",
]

for url in apis:
    try:
        resp = curl_requests.get(url, impersonate="chrome120", headers=HEADERS, timeout=10)
        status = resp.status_code
        length = len(resp.text)
        if status == 200 and length > 100:
            try:
                data = resp.json()
                data_str = json.dumps(data, ensure_ascii=False)
                print(f"  [{status}] {url.split('/')[-2]}/{url.split('/')[-1].split('?')[0]:30s} | {length:>6,} chars")
                
                # 找列表
                if isinstance(data, dict):
                    for key in ['data','poiList','hotelList','list','pois','hotels','items','recommendList','rankingList']:
                        if key in data:
                            val = data[key]
                            if isinstance(val, list) and len(val) > 0:
                                print(f"     >>> {key}: {len(val)} 条")
                                print(f"     >>> sample: {json.dumps(val[0], ensure_ascii=False)[:300]}")
                            elif isinstance(val, dict):
                                for sk, sv in val.items():
                                    if isinstance(sv, list) and len(sv) > 0:
                                        print(f"     >>> {key}.{sk}: {len(sv)} 条")
                                        print(f"     >>> sample: {json.dumps(sv[0], ensure_ascii=False)[:300]}")
            except:
                print(f"  [{status}] {url.split('/')[-1][:40]:40s} | {length:>6,} chars (not JSON)")
        else:
            print(f"  [{status}] {url.split('/')[-1][:40]:40s} | {length:>6,} chars")
    except Exception as e:
        print(f"  [ERR] {url.split('/')[-1][:40]:40s} | {type(e).__name__}: {str(e)[:60]}")
    time.sleep(0.2)
