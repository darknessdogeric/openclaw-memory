import sys, os
sys.path.insert(0, r'D:\B166ER-OpenClaw\workspace\trendradar')
import sqlite3

db_path = r'D:\B166ER-OpenClaw\workspace\trendradar\output\news\2026-08-24.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

keywords = ['WTI', '布伦特', '原油', '天然气', '美联储', '利率', '纳斯达克', '人民币', '港股', 'A', 'S&P', '美股', '石油']
for kw in keywords:
    cur.execute("SELECT COUNT(*) FROM news_items WHERE title LIKE ?", (f'%{kw}%',))
    cnt = cur.fetchone()[0]
    print(f'{kw}: {cnt} matches')

conn.close()

# Also check RSS DB
rss_db = r'D:\B166ER-OpenClaw\workspace\trendradar\output\rss'
if os.path.exists(rss_db):
    rss_dates = sorted(os.listdir(rss_db))
    print(f'\nRSS dates: {rss_dates[-5:]}')
    if rss_dates:
        latest_rss = os.path.join(rss_db, rss_dates[-1])
        if os.path.isdir(latest_rss):
            feeds = sorted(os.listdir(latest_rss))
            print(f'RSS feeds for {rss_dates[-1]}: {feeds[:10]}')
