"""Phase 2: 去重 + 评分 + 读取 Top 文章"""
import sys, json
sys.path.insert(0, r'D:\B166ER-OpenClaw\workspace')
from tavily_search import search

# More targeted queries for fresh 2026 data
QUERIES = [
    "GEO 文旅 酒店 OTA 弊端 问题 案例 2026",
    "GEO AI污染 训练数据 内容农场 问题",
    "AI Agent 旅行 个人助理 vs AI推荐 2026",
    "GEO search engine optimization vs AEO answer engine optimization 2026",
    "旅游行业 大模型 应用 ChatGPT 推荐 决策",
]

all_items = {}
for q in QUERIES:
    print(f"\n=== {q} ===")
    try:
        d = search(q, max_results=8)
        items = d.get('results', [])
        for it in items:
            url = it.get('url', '')
            # Dedup by URL
            if url in all_items:
                continue
            all_items[url] = {
                "title": it.get('title'),
                "url": url,
                "score": it.get('score', 0),
                "content": it.get('content', ''),
                "query": q,
            }
            print(f"  [{it.get('score', 0):.2f}] {it.get('title', '')[:80]}")
    except Exception as e:
        print(f"  ERR: {e}")

# Sort by score
ranked = sorted(all_items.values(), key=lambda x: x['score'], reverse=True)
print(f"\n\n=== Top 10 by score (out of {len(ranked)} unique) ===")
for i, it in enumerate(ranked[:10], 1):
    print(f"\n{i}. [{it['score']:.2f}] {it['title']}")
    print(f"   URL: {it['url']}")
    print(f"   Query: {it['query']}")
    print(f"   Excerpt: {it['content'][:200]}")

out = r"D:\B166ER-OpenClaw\workspace\geo_research_v2.json"
with open(out, 'w', encoding='utf-8') as f:
    json.dump(ranked, f, ensure_ascii=False, indent=2)
print(f"\nSaved {len(ranked)} unique items to {out}")