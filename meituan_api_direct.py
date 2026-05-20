# -*- coding: utf-8 -*-
"""美团酒店 - 直接API调用方案"""
import json, time
from curl_cffi import requests as curl_requests

HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Accept": "application/json",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "https://i.meituan.com/hotel/xiangyang/",
    "Origin": "https://i.meituan.com",
}

# 第一步：获取襄阳 cityId
print("=== Step 1: 获取襄阳 cityId ===")
city_search_urls = [
    "https://ihotel.meituan.com/group/v1/city/search?keyword=襄阳&version=480",
    "https://ihotel.meituan.com/group/v1/city/search?keyword=%E8%A5%84%E9%98%B3",
    "https://www.meituan.com/ptapi/getprovincecityinfo",
]

for url in city_search_urls:
    try:
        resp = curl_requests.get(url, impersonate="chrome120", headers=HEADERS, timeout=10)
        print(f"  {url[:80]} | status={resp.status_code} | {len(resp.text)} chars")
        if resp.status_code == 200 and len(resp.text) > 50:
            data = resp.json()
            print(f"  Sample: {json.dumps(data, ensure_ascii=False)[:300]}")
            break
    except Exception as e:
        print(f"  ❌ {type(e).__name__}: {str(e)[:60]}")

# 第二步：尝试直接搜索酒店
print("\n=== Step 2: 酒店搜索 ===")

# 常见的美团酒店搜索 API (移动端)
search_configs = [
    # 方案A: ihotel 搜索
    {
        "url": "https://ihotel.meituan.com/hbsearch/HotelSearch",
        "params": {
            "cityId": 774,  # 尝试襄阳
            "startDate": "2026-05-13",
            "endDate": "2026-05-14",
            "utm_medium": "touch",
            "version": "480",
        }
    },
    # 方案B: 简化参数
    {
        "url": "https://ihotel.meituan.com/hbsearch/HotelSearch",
        "params": {
            "utm_medium": "touch", 
            "version_name": "10.12",
            "version": "480",
            "ci": "774",
            "startDate": "2026-05-13",
            "endDate": "2026-05-14",
        }
    },
    # 方案C: group API
    {
        "url": "https://ihotel.meituan.com/group/v1/deal/search",
        "params": {
            "ci": 774,
            "startDate": "2026-05-13",
            "endDate": "2026-05-14",
            "limit": 20,
            "offset": 0,
            "utm_medium": "touch",
        }
    },
    # 方案D: poi 列表
    {
        "url": "https://ihotel.meituan.com/group/v1/poi/search",
        "params": {
            "ci": 774,
            "startDate": "2026-05-13",
            "endDate": "2026-05-14",
            "limit": 20,
            "offset": 0,
            "utm_medium": "touch",
        }
    },
]

for cfg in search_configs:
    try:
        resp = curl_requests.get(
            cfg["url"],
            impersonate="chrome120",
            params=cfg["params"],
            headers=HEADERS,
            timeout=15,
        )
        data = resp.json() if resp.headers.get('content-type','').startswith('application/json') else resp.text[:300]
        status = resp.status_code
        print(f"  [{status}] {cfg['url'].split('/')[-1]:20s} | {len(resp.text):>6,} chars | {json.dumps(data, ensure_ascii=False)[:200]}")
    except Exception as e:
        print(f"  [ERR] {cfg['url'].split('/')[-1]:20s} | {type(e).__name__}: {str(e)[:60]}")
    time.sleep(0.3)

# 第三步: 尝试 POST 方式
print("\n=== Step 3: POST 搜索 ===")
post_configs = [
    {
        "url": "https://ihotel.meituan.com/hbsearch/HotelSearch",
        "body": {
            "cityId": 774,
            "checkIn": "2026-05-13",
            "checkOut": "2026-05-14",
            "pageNum": 1,
            "pageSize": 20,
            "utm_medium": "touch",
        }
    },
    {
        "url": "https://ihotel.meituan.com/group/v1/poi/list",
        "body": {
            "cityId": 774,
            "startDate": "2026-05-13",
            "endDate": "2026-05-14",
            "page": 1,
            "pageSize": 20,
            "utm_medium": "touch",
        }
    },
    # 模仿真实请求
    {
        "url": "https://ihotel.meituan.com/hbsearch/HotelSearch",
        "body": {
            "utm_medium": "touch",
            "version_name": "10.12.0",
            "platform": "1",
            "os": "2",
            "app": "group",
            "ci": 774,
            "checkIn": "2026-05-13",
            "checkOut": "2026-05-14",
            "ste": "",  # SEO tag
        }
    },
]

for cfg in post_configs:
    try:
        resp = curl_requests.post(
            cfg["url"],
            impersonate="chrome120",
            json=cfg["body"],
            headers=HEADERS,
            timeout=15,
        )
        text = resp.text
        status = resp.status_code
        print(f"  [{status}] {cfg['url'].split('/')[-1]:20s} | {len(text):>6,} chars")
        if status == 200 and len(text) > 100:
            try:
                data = resp.json()
                print(f"  {json.dumps(data, ensure_ascii=False)[:400]}")
            except:
                print(f"  {text[:300]}")
    except Exception as e:
        print(f"  [ERR] {cfg['url'].split('/')[-1]:20s} | {type(e).__name__}: {str(e)[:60]}")
    time.sleep(0.3)
