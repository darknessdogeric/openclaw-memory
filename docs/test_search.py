# -*- coding: utf-8 -*-
"""测试直接HTTP请求搜索"""
import requests, sys, re
sys.stdout.reconfigure(encoding='utf-8')

query = '大乐透26035开奖结果'
encoded = requests.utils.quote(query)
url = f'https://www.baidu.com/s?wd={encoded}&rn=5'

print(f"URL: {url}", flush=True)

try:
    r = requests.get(url, timeout=15, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })
    r.encoding = 'utf-8'
    text = r.text
    print(f"Status: {r.status_code}, Length: {len(text)}", flush=True)

    # 提取标题和URL
    results = re.findall(r'h3 class="news-title[^"]*"[^>]*>.*?<a href="([^"]+)"[^>]*>(.*?)</a>', text, re.S)
    if not results:
        results = re.findall(r'<a[^>]+href="(https?://[^"]+)"[^>]*>(.*?)</a>', text, re.S)

    print(f"Found {len(results)} results", flush=True)
    for url, title in results[:5]:
        clean_title = re.sub(r'<[^>]+>', '', title).strip()
        print(f"TITLE: {clean_title}")
        print(f"URL: {url[:100]}")
        print("---")
except Exception as e:
    print(f"Error: {e}", flush=True)
