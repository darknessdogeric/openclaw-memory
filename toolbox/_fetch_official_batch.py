"""批量抓取国家统计局 7/15 发布的官方原文页面，提取纯文本。"""
from playwright.sync_api import sync_playwright
import re
import sys
import json

URLS = [
    # 7/15 当日发布
    ("2026年6月份规模以上工业增加值", "https://www.stats.gov.cn/sj/zxfb/202607/t20260715_1964123.html"),
    ("2026年1—6月份全国固定资产投资", "https://www.stats.gov.cn/sj/zxfb/202607/t20260715_1964124.html"),
    ("2026年1—6月份全国房地产市场", "https://www.stats.gov.cn/sj/zxfb/202607/t20260715_1964126.html"),
    ("2026年上半年社会消费品零售总额", "https://www.stats.gov.cn/sj/zxfb/202607/t20260715_1964127.html"),
    ("2026年6月份能源生产情况", "https://www.stats.gov.cn/sj/zxfb/202607/t20260715_1964128.html"),
    ("2026年上半年居民收入和消费支出", "https://www.stats.gov.cn/sj/zxfb/202607/t20260715_1964129.html"),
    ("2026年二季度全国工业产能利用率", "https://www.stats.gov.cn/sj/zxfb/202607/t20260715_1964130.html"),
    ("2026年6月份70城商品住宅销售价格", "https://www.stats.gov.cn/sj/zxfb/202607/t20260715_1964115.html"),
    # 7/9 发布（CPI/PPI）
    ("2026年6月份CPI", "https://www.stats.gov.cn/sj/zxfb/202607/t20260709_1964084.html"),
    ("2026年6月份PPI", "https://www.stats.gov.cn/sj/zxfb/202607/t20260709_1964083.html"),
    # 6/30 发布（PMI）
    ("2026年6月PMI运行情况", "https://www.stats.gov.cn/sj/zxfb/202606/t20260630_1964032.html"),
]

results = {}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    
    for label, url in URLS:
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=20000)
            page.wait_for_load_state("networkidle", timeout=10000)
            
            # 提取正文（去 script/style/nav）
            text = page.evaluate("""() => {
                // 移除噪音
                document.querySelectorAll('script, style, nav, header, footer, .nav, .header, .footer').forEach(el => el.remove());
                
                // 尝试找主要内容容器
                let main = document.querySelector('.TRS_Editor, .article-content, .content, .main-content, article, .TRS_PreAppend');
                if (!main) main = document.body;
                
                let txt = main ? main.innerText : document.body.innerText;
                // 规范化空白
                txt = txt.replace(/[\\u00A0\\s]+/g, ' ').trim();
                return txt;
            }""")
            
            results[label] = {
                "url": url,
                "status": "OK",
                "length": len(text),
                "text": text
            }
            print(f"[OK] {label}: {len(text)} chars")
        except Exception as e:
            results[label] = {
                "url": url,
                "status": f"FAIL: {e}"
            }
            print(f"[FAIL] {label}: {e}")
    
    browser.close()

# 保存到 JSON
with open("D:/B166ER-OpenClaw/workspace/toolbox/_official_data_2026_06.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"\nTotal: {len(results)} pages")
print(f"OK: {sum(1 for r in results.values() if r.get('status') == 'OK')}")
print(f"FAIL: {sum(1 for r in results.values() if r.get('status') != 'OK')}")