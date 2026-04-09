#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import json
import io
import sys

TAVILY_KEY = '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'

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

payload = json.dumps({
    'api_key': TAVILY_KEY,
    'query': '新华渝北酒店',
    'max_results': 5,
    'search_depth': 'advanced',
    'include_answer': True,
}).encode('utf-8')

req = urllib.request.Request(
    'https://api.tavily.com/search',
    data=payload,
    headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
    method='POST',
)

with urllib.request.urlopen(req, timeout=20) as resp:
    result = json.loads(resp.read().decode('utf-8'))

print('=== Tavily API Test ===')
print(f'Query: {result["query"]}')
print(f'Reuslt count: {len(result["results"])}')
print()
if result.get('answer'):
    print(f'Answer: {result["answer"]}')
print()
for i, r in enumerate(result['results'], 1):
    title = r['title'].replace('\n', ' ')
    print(f'{i}. {title}')
    print(f'   {r["url"]}')
