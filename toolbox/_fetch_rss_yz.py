"""Fetch RSS items for 2026-08-25 matching financial keywords"""
import sys, os
sys.path.insert(0, r'D:\B166ER-OpenClaw\workspace\trendradar')
import sqlite3, json

rss_db = r'D:\B166ER-OpenClaw\workspace\trendradar\output\rss\2026-08-25.db'
conn = sqlite3.connect(rss_db)
cur = conn.cursor()

# Check which feeds actually have items
cur.execute("""
    SELECT feed_id, COUNT(*) as cnt 
    FROM rss_items 
    GROUP BY feed_id 
    ORDER BY cnt DESC
""")
feed_counts = cur.fetchall()
print("Feed item counts:")
for f, c in feed_counts:
    print(f"  {f}: {c}")

# Check specific financial feeds
financial_keywords = ['原油', 'WTI', '布伦特', '天然气', '石油', 'oil', 'gas', 
                     '美联储', 'Fed', '利率', 'interest rate',
                     '美股', 'S&P', '纳斯达克', 'Nasdaq',
                     '人民币', 'RMB', '港股', 'A股', '上证', '深证',
                     '原油', '期货', '大宗商品', '商品']

print("\n--- Financial keyword matches ---")
all_results = {}
for kw in financial_keywords:
    cur.execute("""
        SELECT title, feed_id, published_at, url, summary 
        FROM rss_items 
        WHERE title LIKE ? OR summary LIKE ?
        LIMIT 20
    """, (f'%{kw}%', f'%{kw}%'))
    rows = cur.fetchall()
    if rows:
        all_results[kw] = rows
        print(f"\n[{kw}] {len(rows)} matches:")
        for row in rows[:5]:
            print(f"  [{row[1]}] {row[0][:80]}")
            print(f"    pub: {row[2]} | url: {row[3][:60]}")

conn.close()
