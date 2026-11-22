import sys, os, json
sys.path.insert(0, r'D:\B166ER-OpenClaw\workspace\trendradar')
import sqlite3

db_path = r'D:\B166ER-OpenClaw\workspace\trendradar\output\news\2026-08-24.db'
conn = sqlite3.connect(db_path)
cur = conn.cursor()

# List tables
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cur.fetchall()
print('tables:', [t[0] for t in tables])

# Sample each table
for t in tables:
    tname = t[0]
    cur.execute(f"SELECT * FROM {tname} LIMIT 2")
    rows = cur.fetchall()
    col_names = [desc[0] for desc in cur.description]
    print(f'\n[{tname}] cols={col_names}')
    for row in rows[:2]:
        print(f'  {row}')
conn.close()
