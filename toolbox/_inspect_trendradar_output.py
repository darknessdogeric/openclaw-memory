import json

d = json.load(open(r'D:\B166ER-OpenClaw\workspace\toolbox\_subagent_trendradar_finance_20260825.json', encoding='utf-8'))
results = d['results']

for x in results:
    name = x['name']
    if not x['ok']:
        print(f"[{name}] FAIL: {x['error'][:100]}")
        continue
    data = x['data']
    if not data.get('success'):
        print(f"[{name}] no data: {data.get('message', '')}")
        continue
    total = data.get('total', 0)
    news_count = len(data.get('results', []))
    rss_count = len(data.get('rss_results', []))
    print(f"[{name}] total={total} news={news_count} rss={rss_count}")
    # Print first 2 items as sample
    for item in data.get('results', [])[:2]:
        title = item.get('title', item.get('content', ''))[:60]
        print(f"    -> {title}")
