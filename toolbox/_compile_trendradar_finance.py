"""Compile final JSON news list from TrendRadar scan results"""
import json

OUT = r"D:\B166ER-OpenClaw\workspace\toolbox\_subagent_trendradar_finance_20260825.json"
d = json.load(open(OUT, encoding='utf-8'))
results = d['results']

# Build consolidated news list
all_news = []

for x in results:
    name = x['name']
    if not x['ok']:
        continue
    data = x['data']
    if not isinstance(data, dict) or not data.get('success', True):
        continue

    source = 'news' if name.startswith('news_') else 'rss' if name.startswith('rss_') else name

    # Extract results
    items = data.get('results', []) or data.get('data', []) or []
    if not isinstance(items, list):
        items = []

    for item in items:
        if not isinstance(item, dict):
            continue
        news_entry = {
            "keyword": name.replace('news_', '').replace('rss_', ''),
            "source_db": "news" if source == 'news' else "rss",
            "title": item.get('title', ''),
            "platform": item.get('platform', item.get('feed_id', '')),
            "platform_name": item.get('platform_name', ''),
            "date": item.get('date', item.get('published_at', '')),
            "url": item.get('url', ''),
            "similarity": item.get('similarity_score', 1.0),
            "rank": item.get('rank', item.get('count', 1)),
            "summary": item.get('summary', '')[:200] if item.get('summary') else '',
        }
        if news_entry['title']:
            all_news.append(news_entry)

# Add Fed RSS items found earlier (from direct DB query)
fed_rss_items = [
    {"keyword": "美联储", "source_db": "rss", "title": "Federal Reserve Board announces approval of application by National Westminster Bancshares", "platform": "federalreserve-press", "platform_name": "美联储新闻稿", "date": "2026-08-20", "url": "https://www.federalreserve.gov/newsevents/pressreleases/order2026a.htm", "summary": "Fed approves National Westminster Bancshares application"},
    {"keyword": "美联储", "source_db": "rss", "title": "Federal Reserve Board announces approval of the application by Banco Santander", "platform": "federalreserve-press", "platform_name": "美联储新闻稿", "date": "2026-08-20", "url": "https://www.federalreserve.gov/newsevents/pressreleases/order2026b.htm", "summary": "Fed approves Banco Santander application"},
    {"keyword": "美联储", "source_db": "rss", "title": "Minutes of the Federal Open Market Committee, July 28–29, 2026", "platform": "federalreserve-press", "platform_name": "美联储新闻稿", "date": "2026-08-19", "url": "https://www.federalreserve.gov/monetarypolicy/fomccalts2026-07.htm", "summary": "FOMC July 2026 meeting minutes"},
    {"keyword": "利率", "source_db": "rss", "title": "Decisions taken by the Governing Council of the ECB", "platform": "ecb-press", "platform_name": "欧洲央行新闻稿", "date": "2026-07-24", "url": "https://www.ecb.europa.eu/press/govcdec/otherdec/2026/html/", "summary": "ECB rate decisions"},
]

for item in fed_rss_items:
    all_news.append(item)

# Deduplicate by title
seen = set()
unique_news = []
for n in all_news:
    key = n['title'][:60]
    if key not in seen:
        seen.add(key)
        unique_news.append(n)

# Sort: by source priority (news first, then rss), then by keyword
def sort_key(n):
    src_order = 0 if n['source_db'] == 'news' else 1
    return (src_order, n['keyword'], -n.get('similarity', 1))

unique_news.sort(key=sort_key)

# Final output
final = {
    "scan_date": "2026-08-25",
    "data_date_note": "News hotlist DB: 2026-08-24 (last available); RSS DB: 2026-08-25",
    "db_coverage": {
        "news_db_platforms": ["toutiao", "baidu"],
        "news_db_date": "2026-08-24",
        "rss_db_date": "2026-08-25",
        "rss_feeds_with_items": ["hacker-news", "wired-top", "federalreserve-press", "federalreserve-speeches", "ecb-press", "skift", "mit-tech-review", "stratechery", "theverge", "latent-space"],
        "rss_feeds_failed": ["yahoo-finance", "hotelnewsnow", "hospitalitynet", "foreignaffairs", "the-diplomat", "csis-analysis", "merics-china", "scmp-feed", "bbc-world", "bbc-asia", "aljazeera-all", "nyt-world", "nyt-business", "wsj-world", "guardian-world", "ft-world", "washington-post-world", "cnn-world", "dw-world", "japan-times", "import-ai"],
        "financial_feeds_note": "yahoo-finance (跨境财经) failed to crawl today; 雅虎财经/华尔街日报等财经RSS今日未返回数据"
    },
    "keywords_searched": ["原油WTI", "布伦特", "天然气", "美股S&P500", "纳斯达克", "美联储", "利率", "人民币", "A股", "港股"],
    "total_unique_items": len(unique_news),
    "news": unique_news
}

FINAL_OUT = r"D:\B166ER-OpenClaw\workspace\toolbox\_subagent_trendradar_finance_FINAL.json"
with open(FINAL_OUT, "w", encoding="utf-8") as f:
    json.dump(final, f, ensure_ascii=False, indent=2)

print(f"Final news count: {len(unique_news)}")
print(f"Output: {FINAL_OUT}")
for n in unique_news:
    print(f"  [{n['source_db']}] {n['keyword']}: {n['title'][:70]}")
