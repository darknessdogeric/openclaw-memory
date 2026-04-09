#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import json
import sys
import io

TAVILY_KEY = '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'

# Set UTF-8 for everything
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

queries = [
    '新华酒店管理公司 两江假日集团 新华渝北酒店',
    '重庆两江假日酒店管理有限公司 旗下品牌 新华',
    '新华渝北酒店 星级 规模 地址',
]

all_results = []

for query in queries:
    print(f'\n========== {query} ==========')
    
    payload = json.dumps({
        'api_key': TAVILY_KEY,
        'query': query,
        'max_results': 8,
        'search_depth': 'advanced',
        'include_answer': True,
    }).encode('utf-8')
    
    req = urllib.request.Request(
        'https://api.tavily.com/search',
        data=payload,
        headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
        method='POST',
    )
    
    with urllib.request.urlopen(req, timeout=30) as resp:
        result = json.loads(resp.read().decode('utf-8'))
    
    answer = result.get('answer')
    if answer:
        print(f'Answer: {answer}')
        all_results.append({'query': query, 'answer': answer})
    
    for r in result.get('results', []):
        score = r.get('score', 0)
        title = r.get('title', '')
        url = r.get('url', '')
        content = r.get('content', '')[:400]
        print(f'\n[{score:.2f}] {title}')
        print(f'URL: {url}')
        print(f'Snippet: {content}')
        all_results.append({'query': query, 'score': score, 'title': title, 'url': url, 'content': content})

# Save to JSON
with open('tavily_search_results.json', 'w', encoding='utf-8') as f:
    json.dump(all_results, f, ensure_ascii=False, indent=2)

print(f'\n[Saved] {len(all_results)} results to tavily_search_results.json')
