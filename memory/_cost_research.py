"""校准 AHL 商业模式成本假设: GPU 租用 + 大模型 token 成本"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

env_path = Path(r"D:\B166ER-openclaw\config\.env")
API_KEY = env_path.read_text(encoding="utf-8").strip().split("=", 1)[1].strip()

from tavily import TavilyClient
client = TavilyClient(api_key=API_KEY)

QUERIES = [
    "开源大模型 API token 价格 2026 Qwen DeepSeek 每百万token",
    "GPU 租用 A100 H100 4090 每小时价格 中国 2026",
    "酒店 SaaS PMS 实施成本 中小酒店 收费",
    "B端 SaaS 获客成本 CAC 中国 企业服务 平均",
    "DeepSeek API 定价 输入 输出 token 2026",
]

for q in QUERIES:
    print("\n" + "=" * 72)
    print(f"Q: {q}")
    try:
        r = client.search(query=q, max_results=4, search_depth="advanced")
        for item in r.get("results", [])[:4]:
            print(f"\n  [{item.get('score')}] {(item.get('title') or '')[:85]}")
            print(f"      {(item.get('url') or '')[:95]}")
            print(f"      {(item.get('content') or '')[:260]}")
    except Exception as e:
        print(f"  [X] {type(e).__name__}: {e}")