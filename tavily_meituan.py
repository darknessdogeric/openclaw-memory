import json, urllib.request

TAVILY_KEY = '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'

queries = [
    '美团 襄阳 酒店 2026',
    'meituan hotel xiangyang price',
    'site:meituan.com 襄阳酒店',
]

for q in queries:
    payload = json.dumps({
        'api_key': TAVILY_KEY,
        'query': q,
        'max_results': 5,
        'include_answer': True,
        'include_raw_content': False,
    }).encode()
    req = urllib.request.Request(
        'https://api.tavily.com/search',
        data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        data = json.loads(resp.read())
    
    print(f'\n=== {q} ===')
    if data.get('answer'):
        ans = data['answer'][:200]
        print(f'Answer: {ans}')
    for r in data.get('results', [])[:3]:
        title = r['title'][:60]
        url = r['url'][:100]
        content = r.get('content','')[:200]
        print(f'  {title}')
        print(f'  {url}')
        print(f'  {content}')
        print()
