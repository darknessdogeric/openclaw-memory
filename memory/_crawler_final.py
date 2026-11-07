"""最终 e2e 测试 (避免代码被对话屏蔽规则污染)"""
import os, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Step 1: 加载 .env
env_path = Path(r"D:\B166ER-openclaw\config\.env")
for line in env_path.read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if line and not line.startswith("#"):
        k, _, v = line.partition("=")
        os.environ[k.strip()] = v.strip()

api_key = os.environ.get("TAVILY_API_KEY", "")
print(f"=== .env loaded: TAVILY_API_KEY len={len(api_key)} chars ===")

# Step 2: Tavily 实测 (3 个 query)
print("\n=== Tavily search ===")
try:
    from tavily import TavilyClient
    client = TavilyClient(api_key=api_key)
    queries = [
        "厚海 MSI 2026 Q3 中国酒店景气",
        "Anyi 1244 战略 国资文旅",
        "锦著 欢朋 经济型酒店 2026",
    ]
    for q in queries:
        r = client.search(query=q, max_results=1)
        results = r.get("results", [])
        if results:
            item = results[0]
            print(f"  Q: {q[:35]}")
            print(f"    → {item['title'][:60]}")
            print(f"    {item['url'][:60]}")
    print(f"  [OK] 3 queries done")
except Exception as e:
    print(f"  [X] {type(e).__name__}: {e}")

# Step 3: Scrapling 0.5 StealthyFetcher
print("\n=== Scrapling 0.5 StealthyFetcher ===")
try:
    from scrapling import StealthyFetcher
    page = StealthyFetcher.fetch("https://www.mct.gov.cn/whzx/whywh/", headless=True, timeout=20)
    status = getattr(page, "status", "?")
    text = page.get_text() if hasattr(page, "get_text") else str(page)[:200]
    print(f"  [OK] status={status}, text_len={len(text)}")
    print(f"  preview: {text[:120].replace(chr(10), ' ')}")
except Exception as e:
    print(f"  [X] StealthyFetcher: {type(e).__name__}: {e}")

# Step 4: Scrapling 0.5 普通 Fetcher
print("\n=== Scrapling 0.5 Fetcher (普通) ===")
try:
    from scrapling import Fetcher
    page = Fetcher.get("https://example.com", timeout=10)
    status = getattr(page, "status", "?")
    text = page.get_text() if hasattr(page, "get_text") else str(page)[:200]
    print(f"  [OK] status={status}, text_len={len(text)}")
except Exception as e:
    print(f"  [X] Fetcher: {type(e).__name__}: {e}")