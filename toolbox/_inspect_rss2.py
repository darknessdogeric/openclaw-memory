import sys, os, json
sys.path.insert(0, r'D:\B166ER-OpenClaw\workspace\trendradar')
import sqlite3

rss_db = r'D:\B166ER-OpenClaw\workspace\trendradar\output\rss\2026-08-25.db'
conn = sqlite3.connect(rss_db)
cur = conn.cursor()

# Check rss_items structure
cur.execute("SELECT * FROM rss_items LIMIT 3")
rows = cur.fetchall()
cols = [d[0] for d in cur.description]
print('[rss_items] cols:', cols)
for row in rows:
    print(f'  {row}')
print()

# Check feeds status
cur.execute("SELECT * FROM rss_feeds")
feeds = cur.fetchall()
feed_cols = [d[0] for d in cur.description]
print('[rss_feeds] cols:', feed_cols)
for f in feeds:
    print(f'  {f}')

# Check crawl status
cur.execute("SELECT * FROM rss_crawl_status")
crawl = cur.fetchall()
crawl_cols = [d[0] for d in cur.description]
print('\n[rss_crawl_status] cols:', crawl_cols)
for c in crawl:
    print(f'  {c}')

# Search for financial keywords in RSS
keywords = ['WTI', '布伦特', '原油', '天然气', '美联储', '利率', '纳斯达克', '人民币', '港股', 'A', 'S&P', '美股', '石油', '原油', 'oil', 'gas', 'Fed', 'RMB']
print('\n--- keyword search in rss_items ---')
for kw in keywords:
    cur.execute("SELECT COUNT(*) FROM rss_items WHERE title LIKE ?", (f'%{kw}%',))
    cnt = cur.fetchone()[0]
    if cnt > 0:
        print(f'  {kw}: {cnt} matches')
        cur.execute("SELECT title FROM rss_items WHERE title LIKE ? LIMIT 3", (f'%{kw}%',))
        for row in cur.fetchall():
            print(f'    -> {row[0][:80]}')

conn.close()
