import os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from scrapling import StealthyFetcher

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
OUT = r"D:\B166ER-openclaw\workspace\memory\_sse_reits.html"

for url in ["https://www.sse.com.cn/reits/announcements/info", "https://www.sse.com.cn/reits/info/"]:
    try:
        page = StealthyFetcher.fetch(url, headless=True, network_idle=True, timeout=45000,
                                    retries=1, user_agent=UA, disable_resources=False)
        html = page.html_content if hasattr(page, "html_content") else str(page)
        open(OUT, "w", encoding="utf-8").write(html)
        print("OK", url, "len", len(html))
        break
    except Exception as e:
        print("FAIL", url, type(e).__name__, str(e)[:80])