import sys, os, json
sys.path.insert(0, r'D:\B166ER-OpenClaw\workspace\trendradar')
import sqlite3

# Check RSS DB for 2026-08-25
rss_db = r'D:\B166ER-OpenClaw\workspace\trendradar\output\rss\2026-08-25.db'
conn = sqlite3.connect(rss_db)
cur = conn.cursor()

cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [t[0] for t in cur.fetchall()]
print('RSS tables:', tables)

for t in tables:
    cur.execute(f"SELECT * FROM {t} LIMIT 2")
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    print(f'\n[{t}] cols={cols}')
    for row in rows:
        print(f'  {row}')
    break

conn.close()
