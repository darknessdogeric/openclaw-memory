#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib.request
import json
import sys
import io

TAVILY_KEY = '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'

queries = [
    '金手指 港片 2023 剧情故事 程一言',
    '金手指电影 梁朝伟 刘德华 故事原型 佳宁案',
    '金手指 film synopsis 庄文杰',
]

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
    
    with urllib.request.urlopen(req, timeout=20) as resp:
        result = json.loads(resp.read().decode('utf-8'))
    
    if result.get('answer'):
        print(f'Answer: {result["answer"]}')
    
    for r in result.get('results', []):
        score = r.get('score', 0)
        title = r.get('title', '')
        url = r.get('url', '')
        content = r.get('content', '')[:500]
        print(f'\n[{score:.2f}] {title}')
        print(f'URL: {url}')
        print(f'Snippet: {content}')
