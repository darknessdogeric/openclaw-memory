"""Search stats.gov.cn/sj/sjjd/ for GDP interpretation page (2026 H1)."""
from playwright.sync_api import sync_playwright
import sys

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # 直接搜 sjjd 栏目
    try:
        page.goto("http://www.stats.gov.cn/sj/sjjd/202607/index.html", wait_until="domcontentloaded", timeout=20000)
        page.wait_for_load_state("networkidle", timeout=10000)
    except Exception as e:
        print(f"sjjd navigation issue: {e}", file=sys.stderr)
    
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
    
    print(f"sjjd/202607 links: {len(links)}")
    print("\n=== All 2026 + GDP-related ===")
    for l in links:
        t = l["text"]
        h = l["href"]
        if "2026" in t and ("GDP" in t or "国民经济" in t or "上半年" in t or "二季度" in t or "经济" in t):
            print(f"[{t}]")
            print(f"  -> {h}")
    
    print("\n=== All 2026 in sjjd (top 30) ===")
    cnt = 0
    for l in links:
        if "2026" in l["text"] and cnt < 30:
            print(f"{l['text']}  ||  {l['href']}")
            cnt += 1
    
    browser.close()