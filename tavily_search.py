# -*- coding: utf-8 -*-
import requests
import json

TAVILY_KEY = 'tvly-dev-8KxnA8kQ8nLGqJzMFJqJ3p0D'

queries = [
    '新华酒店管理公司 两江假日集团',
    '新华渝北酒店 两江假日',
    '重庆两江假日酒店管理有限公司 新华渝北',
]

for query in queries:
    print(f'\n========== {query} ==========\n')
    try:
        response = requests.post(
            'https://api.tavily.com/search',
            json={
                'api_key': TAVILY_KEY,
                'query': query,
                'search_depth': 'advanced',
                'max_results': 10,
                'include_answer': True
            },
            timeout=20
        )
        result = response.json()
        
        if 'detail' in result:
            print(f'Error: {result["detail"]}')
            continue
            
        print(f'Found {len(result.get("results", []))} results')
        
        if result.get('answer'):
            print(f'\nAnswer: {result["answer"]}\n')
        
        for r in result.get('results', [])[:8]:
            score = r.get('score', 0)
            print(f'[{score:.2f}] {r["title"]}')
            print(f'  URL: {r["url"]}')
            content = r.get('content', '')[:300]
            print(f'  Content: {content}')
            print()
            
    except Exception as e:
        print(f'Error: {e}')
