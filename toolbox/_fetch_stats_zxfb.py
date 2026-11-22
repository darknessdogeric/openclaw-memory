"""Fetch stats.gov.cn/sj/zxfb via Playwright, extract today's (2026-07-15) release links."""
from playwright.sync_api import sync_playwright
import re
import sys

URL = "http://www.stats.gov.cn/sj/zxfb/"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    try:
        page.goto(URL, wait_until="networkidle", timeout=30000)
    except Exception as e:
        print(f"navigation issue: {e}", file=sys.stderr)
        # 继续，已经能拿到部分内容
    
    # 提取所有 a 标签文本 + href
    links = page.evaluate("""() => {
        const items = [];
        document.querySelectorAll('a').forEach(a => {
            const text = (a.textContent || '').replace(/\\s+/g, ' ').trim();
            const href = a.href || '';
            if (text && href && text.length > 3 && text.length < 200) {
                items.push({text: text, href: href});
            }
        });
        return items;
    }""")
    
    print(f"Total links found: {len(links)}")
    print()
    print("=== Links containing 2026 + 6 / 7 月 / 上半年 ===")
    for l in links:
        t = l["text"]
        h = l["href"]
        if ("2026" in t and ("6月" in t or "7月" in t or "上半年" in t)) or \
           ("6月份" in t) or ("国民经济" in t) or ("房地产" in t):
            print(f"[{t}]")
            print(f"  -> {h}")
            print()
    
    print("=== All 2026-prefixed links (top 50) ===")
    cnt = 0
    for l in links:
        t = l["text"]
        if "2026" in t and cnt < 50:
            print(f"{t}  ||  {l['href']}")
            cnt += 1
    
    browser.close()