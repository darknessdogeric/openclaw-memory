# -*- coding: utf-8 -*-
import requests, sys
sys.stdout.reconfigure(encoding='utf-8')

sites = [
    ('500.com lottery', 'https://datachart.500.com/dlt/history/newinc/history.php'),
    ('Baidu home', 'https://www.baidu.com'),
    ('Bing China', 'https://cn.bing.com/search?q=lotte'),
    ('Tencent lottery', 'https://www.17500.cn/dlt/'),
    ('Zhongcai lottery', 'https://www.zhcw.com/'),
]

for name, url in sites:
    try:
        r = requests.head(url, timeout=8, headers={'User-Agent': 'Mozilla/5.0'}, allow_redirects=True)
        print(f'OK {r.status_code} [{name}] -> {r.url[:60]}')
    except Exception as e:
        print(f'FAIL [{name}]: {str(e)[:60]}')
