import sys
sys.path.insert(0, 'C:/Users/ericz/.openclaw/workspace')

from local_semantic_search import search

tests = [
    ('大乐透预测', 5),
    ('酒店收益管理', 3),
    ('审美 品位', 3),
    ('创业融资', 3),
]

results_out = []
for q, n in tests:
    r = search(q, n=n)
    for item in r:
        src = item.get('metadata', {}).get('source', 'unknown') if isinstance(item, dict) else 'N/A'
        score = item.get('score', 0) if isinstance(item, dict) else 0
        content = item.get('content', '')[:80] if isinstance(item, dict) else str(item)[:80]
        results_out.append(f"[{score:.4f}] {src}\n  {content}\n")

with open('C:/Users/ericz/.openclaw/workspace/search_test_out.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(results_out))

print("Done. Results written to search_test_out.txt")
