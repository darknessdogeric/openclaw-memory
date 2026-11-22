"""Parallel GEO research - 5 angles, all in one batch."""
import sys, json
sys.path.insert(0, r'D:\B166ER-OpenClaw\workspace')
from tavily_search import search

QUERIES = [
    # 1. 定义与学术起源
    "GEO Generative Engine Optimization original paper Aggarwal 2023 Princeton",
    # 2. 产业链与服务商
    "GEO 服务商 2026 中国 AI搜索排名优化 大模型SEO",
    # 3. 文旅/旅游行业应用
    "GEO 文旅 酒店 OTA AI搜索优化 2026",
    # 4. 批评与争议
    "GEO criticism AI pollution spam generative engine optimization issues",
    # 5. 替代范式 - AI Agent 决策
    "AI Agent travel planning 2026 personal agent vs recommendation search",
]

results = {}
for q in QUERIES:
    print(f"\n=== Searching: {q} ===")
    try:
        d = search(q, max_results=6)
        ans = d.get('answer', '')
        items = d.get('results', [])
        results[q] = {
            "answer": ans,
            "items": [{"title": i.get('title'), "url": i.get('url'), "score": i.get('score', 0), "content": i.get('content', '')[:400]} for i in items]
        }
        print(f"  Answer: {ans[:200] if ans else '(none)'}")
        print(f"  Got {len(items)} results")
        for i in items[:3]:
            print(f"  [{i.get('score', 0):.2f}] {i.get('title', '')[:80]}")
    except Exception as e:
        print(f"  ERR: {e}")
        results[q] = {"error": str(e)}

# Save raw results
out = r"D:\B166ER-OpenClaw\workspace\geo_research_raw.json"
with open(out, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"\n\nSaved to: {out}")