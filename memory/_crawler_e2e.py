"""端到端测试: tavily search + scrapling stealth fetch"""
import os, sys, io

# Tavily key 从环境变量读取 (不入代码)
TAVILY_KEY = os.environ.get("TAVILY_API_KEY", "")

# 测试 1: tavily search
print("=== 测试 1: Tavily search (国庆 2026 数据) ===")
try:
    from tavily import TavilyClient
    if not TAVILY_KEY:
        print("  [X] TAVILY_API_KEY 未设置 (env var)")
    else:
        client = TavilyClient(api_key=TAVILY_KEY)
        r = client.search(query="2026 国庆 国内出游 文旅部 接待 收入", max_results=3)
        results = r.get("results", [])
        print(f"  [OK] tavily 返回 {len(results)} 条结果")
        for i, item in enumerate(results[:3], 1):
            print(f"    {i}. {item.get('title', 'N/A')[:80]}")
            print(f"       URL: {item.get('url', 'N/A')[:80]}")
            print(f"       snippet: {(item.get('content') or '')[:100]}")
except Exception as e:
    print(f"  [X] tavily 失败: {type(e).__name__}: {e}")

# 测试 2: scrapling stealth fetch
print("\n=== 测试 2: Scrapling stealth fetch (gov.cn) ===")
try:
    from scrapling.fetch import Fetcher
    page = Fetcher.get("https://www.mct.gov.cn/whzx/whywh/", stealth=True, timeout=15)
    print(f"  [OK] scrapling fetch status: {page.status if hasattr(page, 'status') else 'OK'}")
    text = page.get_text() if hasattr(page, 'get_text') else str(page)[:300]
    print(f"  text length: {len(text)}, 前 200: {text[:200]}")
except Exception as e:
    print(f"  [X] scrapling 失败: {type(e).__name__}: {e}")
    # 降级: 用 requests
    print("\n=== 降级: requests 直接抓 ===")
    import requests
    try:
        r = requests.get("https://www.mct.gov.cn/whzx/whywh/", timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        print(f"  [OK] requests status={r.status_code}, len={len(r.text)}")
    except Exception as e2:
        print(f"  [X] requests 失败: {e2}")