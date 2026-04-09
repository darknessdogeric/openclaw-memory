#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import json
import sys
import io

NEW_KEY = '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'

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

payload = json.dumps({
    'api_key': NEW_KEY,
    'query': 'AHL有限服务酒店管理',
    'max_results': 3,
    'search_depth': 'advanced',
    'include_answer': True,
}).encode('utf-8')

req = urllib.request.Request(
    'https://api.tavily.com/search',
    data=payload,
    headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
    method='POST',
)

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        result = json.loads(resp.read().decode('utf-8'))
    print('=== NEW KEY TEST ===')
    print(f'Query: {result["query"]}')
    print(f'Reuslts: {len(result["results"])}')
    if result.get('answer'):
        print(f'Answer: {result["answer"][:200]}')
    for i, r in enumerate(result['results'][:3], 1):
        print(f'{i}. {r["title"][:60]}')
except Exception as e:
    print(f'ERROR: {e}')
