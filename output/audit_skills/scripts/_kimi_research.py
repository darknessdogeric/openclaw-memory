"""调研 Kimi 的 PPT / 图片生成能力: 官方 API + 网页端请求结构"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

env_path = Path(r"D:\B166ER-openclaw\config\.env")
API_KEY = env_path.read_text(encoding="utf-8").strip().split("=", 1)[1].strip()

from tavily import TavilyClient
client = TavilyClient(api_key=API_KEY)

QUERIES = [
    "Kimi 幻灯片 PPT 生成 API 文档 月之暗面",
    "Moonshot AI Kimi API 文档 图像生成 vision image generation",
    "Kimi K2 开源 API 端点 定价 2026",
    "Kimi PPT 生成 原理 模板 大模型 排版",
    "Kimi 图片生成 功能 豆包 即梦 对比 2026",
    "moonshotai platform.moonshot.cn api docs models list",
]

for q in QUERIES:
    print("\n" + "=" * 76)
    print(f"Q: {q}")
    try:
        r = client.search(query=q, max_results=5, search_depth="advanced")
        for item in r.get("results", [])[:5]:
            print(f"\n  [{item.get('score')}] {(item.get('title') or '')[:88]}")
            print(f"      {(item.get('url') or '')[:100]}")
            print(f"      {(item.get('content') or '')[:340]}")
    except Exception as e:
        print(f"  [X] {type(e).__name__}: {e}")