"""同程收购万达酒管 —— 交易事实核查 (五维框架第一步: 事实)"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# 运行时从 .env 取 key, 脚本内不出现任何字面量
env_path = Path(r"D:\B166ER-openclaw\config\.env")
API_KEY = ""
for raw in env_path.read_text(encoding="utf-8").splitlines():
    line = raw.strip()
    if not line or line.startswith("#") or "=" not in line:
        continue
    k, v = line.split("=", 1)
    if k.strip().upper() == "TAVILY_API_KEY":
        API_KEY = v.strip().strip('"').strip("'")
        break
if not API_KEY:
    print("[X] 未在 .env 找到 TAVILY_API_KEY")
    raise SystemExit(1)

from tavily import TavilyClient

client = TavilyClient(api_key=API_KEY)

QUERIES = [
    "同程旅行 收购 万达酒店管理 交易金额 股权比例",
    "同程 万达酒管 收购 估值 评估增值率 业绩承诺",
    "万达酒店管理 2017 融创 68亿 出售 历史 估值",
    "万达酒店 门店数量 客房数 2025 规模 营收",
    "同程收购万达酒管 争议 买贵了 分析 点评",
    "同程旅行 2025 财报 酒店业务 收入 增长 酒店预订",
]

for q in QUERIES:
    print("\n" + "=" * 78)
    print(f"Q: {q}")
    try:
        r = client.search(query=q, max_results=5, search_depth="advanced")
        for item in r.get("results", [])[:5]:
            print(f"\n  [{item.get('score')}] {(item.get('title') or '')[:90]}")
            print(f"      {(item.get('url') or '')[:105]}")
            print(f"      {(item.get('content') or '')[:460]}")
    except Exception as e:
        print(f"  [X] {type(e).__name__}: {e}")
