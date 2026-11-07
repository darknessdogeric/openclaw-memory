"""端到端验证: Scrapling 0.5 + Tavily (.env 加载)"""
import os, sys
from pathlib import Path

# 1. Scrapling 0.5 import verify
print("=== 1. Scrapling 0.5 ===")
try:
    import scrapling
    print(f"  [OK] scrapling {scrapling.__version__}")
    from scrapling.fetch import Fetcher
    print("  [OK] scrapling.fetch.Fetcher import OK")
except Exception as e:
    print(f"  [X]  scrapling: {type(e).__name__}: {e}")

# 2. .env 文件读取
print("\n=== 2. .env file ===")
env_file = Path(r"D:\B166ER-openclaw\config\.env")
print(f"  path: {env_file}")
print(f"  size: {env_file.stat().st_size} bytes")
for line in env_file.read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if not line or line.startswith("#"):
        continue
    k, _, val = line.partition("=")
    os.environ[k.strip()] = val.strip()
    masked = val.strip()[:6] + "..." + f"({len(val.strip())} chars)"
    print(f"  loaded: {k.strip()}={masked}")

# 3. Tavily 实测 (用 .env key)
print("\n=== 3. Tavily 实测 (厚海 MSI) ===")
try:
    from tavily import TavilyClient
    client = TavilyClient(api_key=os.environ["TAVILY_API_KEY"])
    r = client.search(query="厚海 MSI 2026 Q3 酒店景气指数", max_results=2)
    results = r.get("results", [])
    print(f"  [OK] tavily 返回 {len(results)} 条")
    for i, item in enumerate(results, 1):
        title = item.get("title", "N/A")
        url = item.get("url", "N/A")
        snippet = (item.get("content") or "")[:100]
        print(f"    {i}. {title[:70]}")
        print(f"       URL: {url[:70]}")
        print(f"       snippet: {snippet}")
except Exception as e:
    print(f"  [X]  tavily: {type(e).__name__}: {e}")

# 4. Scrapling 实战 (gov.cn 抓页面)
print("\n=== 4. Scrapling stealth fetch (mct.gov.cn) ===")
try:
    from scrapling.fetch import Fetcher
    page = Fetcher.get("https://www.mct.gov.cn/whzx/whywh/", stealth=True, timeout=15)
    print(f"  [OK] scrapling fetch OK")
    print(f"  status: {page.status if hasattr(page, 'status') else 'N/A'}")
except Exception as e:
    print(f"  [X]  scrapling: {type(e).__name__}: {e}")