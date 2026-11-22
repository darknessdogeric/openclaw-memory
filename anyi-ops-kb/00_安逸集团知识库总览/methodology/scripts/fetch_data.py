# -*- coding: utf-8 -*-
"""
fetch_data.py - 多源数据抓取（骨架）
历史：methodology/sop-region-analysis.md 引用。v1.0 骨架 — 实际走 Tavily + openclaw:core:web_search。
"""
import sys, json
from pathlib import Path

def fetch(query: str, sources: list = None, max_results: int = 5) -> dict:
    """
    优先 Tavily，回退 openclaw:core:web_search。
    v1.0: 仅做转发，不做归一化。
    """
    if sources is None:
        sources = ['tavily', 'web_search']
    results = {'query': query, 'sources_tried': [], 'results': []}

    # 1. 试 Tavily
    try:
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent.parent))
        from toolbox.tavily_search import search as tavily_search
        r = tavily_search(query, max_results=max_results)
        if r.status.value == 'success':
            results['sources_tried'].append('tavily')
            results['results'].append({'tool': 'tavily', 'content': r.content})
            return results
    except Exception as e:
        results['tavily_error'] = str(e)

    # 2. 试 openclaw:core:web_search via tool_call
    try:
        from openclaw import tool_call
        result = tool_call(id='openclaw:core:web_search', args={'query': query})
        results['sources_tried'].append('web_search')
        results['results'].append({'tool': 'web_search', 'content': str(result)[:2000]})
    except Exception as e:
        results['web_search_error'] = str(e)

    return results

if __name__ == '__main__':
    q = ' '.join(sys.argv[1:]) or '酒店行业 2026 趋势'
    print(json.dumps(fetch(q), ensure_ascii=False, indent=2)[:3000])