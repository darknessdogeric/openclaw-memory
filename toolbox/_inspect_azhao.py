import json

d = json.load(open(r'D:\B166ER-OpenClaw\workspace\toolbox\_subagent_trendradar_finance_20260825.json', encoding='utf-8'))
results = d['results']

for x in results:
    name = x['name']
    if name != 'search_A股':
        continue
    data = x['data']
    print(f"keys: {list(data.keys())}")
    print(f"success: {data.get('success')}")
    s = data.get('summary', '')
    print(f"summary: {s[:300] if isinstance(s, str) else s}")
    d2 = data.get('data', [])
    print(f"data type: {type(d2).__name__}, len={len(d2) if isinstance(d2, list) else 'N/A'}")
    if isinstance(d2, list) and d2:
        print(f"  sample[0]: {str(d2[0])[:200]}")
    rss = data.get('rss', [])
    print(f"rss type: {type(rss).__name__}, len={len(rss) if isinstance(rss, list) else 'N/A'}")
    if isinstance(rss, list) and rss:
        print(f"  rss[0]: {str(rss[0])[:200]}")
