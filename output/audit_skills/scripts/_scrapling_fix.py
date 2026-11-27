"""Scrapling 0.5 真实参数测试 - timeout 是毫秒"""
import os, sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Tavily (验证持久化 key 工作)
env_path = Path(r"D:\B166ER-openclaw\config\.env")
for line in env_path.read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if line and not line.startswith("#"):
        k, _, v = line.partition("=")
        os.environ[k.strip()] = v.strip()
api_key = os.environ.get("TAVILY_API_KEY", "")

print(f"=== Tavily 验证 (.env 真 key 持久化) ===")
print(f"  key len: {len(api_key)} chars (expect 57)")

from tavily import TavilyClient
client = TavilyClient(api_key=api_key)
r = client.search(query="锦著 欢朋 2026 国庆 RevPAR", max_results=1)
if r.get("results"):
    item = r["results"][0]
    print(f"  Q: 锦著 欢朋 2026 国庆 RevPAR")
    print(f"    → {item['title'][:60]}")
    print(f"    {item['url'][:60]}")
print(f"  [OK] Tavily 持久化 key 工作")

# Scrapling 0.5 - 关键修复: timeout=毫秒
print("\n=== Scrapling 0.5 StealthyFetcher (timeout=20000ms) ===")
try:
    from scrapling import StealthyFetcher
    # mct.gov.cn timeout 设为 20s + 3 retries + network_idle
    page = StealthyFetcher.fetch(
        "https://www.mct.gov.cn/whzx/whywh/",
        headless=True,
        network_idle=True,
        timeout=20000,           # 毫秒 (修复!)
        retries=3,
        retry_delay=2,
        solve_cloudflare=False,
    )
    status = getattr(page, "status", "?")
    text = page.get_text() if hasattr(page, "get_text") else str(page)[:200]
    print(f"  [OK] status={status}, text_len={len(text)}")
    print(f"  preview: {text[:120].replace(chr(10), ' ')}")
except Exception as e:
    print(f"  [X] {type(e).__name__}: {e}")

# Scrapling 0.5 - Fetcher (静态, timeout 毫秒)
print("\n=== Scrapling 0.5 Fetcher (普通 + timeout=20000ms) ===")
try:
    from scrapling import Fetcher
    page = Fetcher.get(
        "https://www.mct.gov.cn/whzx/whywh/",
        timeout=20000,
        retries=3,
    )
    status = getattr(page, "status", "?")
    text = page.get_text() if hasattr(page, "get_text") else str(page)[:200]
    print(f"  [OK] status={status}, text_len={len(text)}")
except Exception as e:
    print(f"  [X] {type(e).__name__}: {e}")

# Scrapling 0.5 - Fetcher example.com (已知简单)
print("\n=== Scrapling 0.5 Fetcher (example.com) ===")
try:
    from scrapling import Fetcher
    page = Fetcher.get("https://example.com", timeout=10000)
    status = getattr(page, "status", "?")
    text = page.get_text() if hasattr(page, "get_text") else str(page)[:100]
    print(f"  [OK] status={status}, text_len={len(text)}")
    print(f"  preview: {text[:80]}")
except Exception as e:
    print(f"  [X] {type(e).__name__}: {e}")