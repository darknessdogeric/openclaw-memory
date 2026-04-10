import sys, json
sys.path.insert(0, 'C:/Users/ericz/.openclaw/workspace')
from local_semantic_search import search

queries = [
    "Eric的音乐审美 Lube 昭和歌谣",
    "酒店收益管理 动态定价 GOPPAR",
    "创业融资 股权结构 商业计划书",
    "大乐透预测 遗漏值 和值",
]

for q in queries:
    print(f"\n查询: {q}")
    print("=" * 50)
    try:
        results = search(q, n=2)
        for r in results:
            src = r.get('metadata', {}).get('source', 'unknown')
            score = r.get('score', 0)
            preview = r.get('content', '')[:80].replace('\n', ' ')
            print(f"  [{score:.4f}] {src}")
            print(f"    {preview}")
    except Exception as e:
        print(f"  Error: {e}")
