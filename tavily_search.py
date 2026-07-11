# -*- coding: utf-8 -*-
"""Tavily search - POST + Bearer auth (fixed 2026-05-26)"""
import sys, io, json, requests
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

KEY = "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"

def search(query, max_results=8):
    r = requests.post(
        "https://api.tavily.com/search",
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
        json={"query": query, "max_results": max_results, "include_answer": True},
        timeout=30,
    )
    r.raise_for_status()
    return r.json()

if __name__ == '__main__':
    queries = sys.argv[1:] if len(sys.argv) > 1 else ['2026端午酒店预订']
    for q in queries:
        try:
            d = search(q)
            ans = d.get('answer','')
            results = d.get('results',[])
            print(f'\n=== {q} ({len(results)} results) ===')
            if ans: print(f'[A] {ans[:500]}')
            for item in results:
                print(f"  [{item.get('score',0):.2f}] {item.get('title','')[:70]}")
                print(f"    {item.get('url','')[:90]}")
                c = item.get('content','')[:200]
                if c: print(f'    {c}')
        except Exception as e:
            print(f'ERR: {e}')
