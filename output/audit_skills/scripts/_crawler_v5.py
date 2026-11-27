"""端到端: Scrapling 0.5 (正确 API) + Tavily (.env 无 BOM)"""
import os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# 1. .env 加载 (无 BOM)
print("=== 1. .env load ===")
from pathlib import Path
for line in Path(r"D:\B166ER-openclaw\config\.env").read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if line and not line.startswith("#"):
        k, _, v = line.partition("=")
        os.environ[k.strip()] = v.strip()
        print(f"  loaded: {k.strip()} (val len={len(v.strip())} chars)")

# 2. Tavily 实测
print("\n=== 2. Tavily search ===")
try:
    from tavily import TavilyClient
    client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
    r = client.search(query="厚海 MSI 2026 Q3 中国酒店景气指数", max_results=2)
    for i, item in enumerate(r["results"], 1):
        print(f"  {i}. {item['title'][:70]}")
        print(f"     {item['url'][:70]}")
    print(f"  [OK] {len(r['results'])} 条结果")
except Exception as e:
    print(f"  [X] {type(e).__name__}: {e}")

# 3. Scrapling 0.5 (正确 API)
print("\n=== 3. Scrapling 0.5 Fetcher ===")
try:
    from scrapling import Fetcher
    page = Fetcher.get("https://www.mct.gov.cn/whzx/whywh/", stealth=True, timeout=15)
    status = getattr(page, "status", "?")
    text = page.get_text() if hasattr(page, "get_text") else str(page)[:200]
    print(f"  [OK] status={status}, text_len={len(text)}")
    print(f"  preview: {text[:150].replace(chr(10), ' ')}")
except Exception as e:
    print(f"  [X] {type(e).__name__}: {e}")