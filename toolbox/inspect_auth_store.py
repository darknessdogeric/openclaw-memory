"""Update OpenClaw auth store to use the working apiclaude key"""
import sqlite3
import re
from pathlib import Path

auth_db = Path.home() / '.openclaw' / 'agents' / 'main' / 'agent' / 'openclaw-agent.sqlite'
print(f'Auth DB: {auth_db}')

# Read current key from openclaw.json
with open(r'D:\B166ER-OpenClaw\openclaw.json', 'r', encoding='utf-8') as f:
    content = f.read()
m = re.search(r'"apiclaude":\s*\{[^}]*"auth":\s*"([^"]+)"', content, re.DOTALL)
new_key = m.group(1) if m else None
print(f'Key to inject: prefix={new_key[:6]}, suffix=...{new_key[-4:]} (len={len(new_key)})' if new_key else 'No key found')

if not auth_db.exists():
    print(f'Auth DB does not exist: {auth_db}')
    raise SystemExit(1)

# Show all tables and their contents
conn = sqlite3.connect(str(auth_db))
cur = conn.cursor()

print('\nTables in DB:')
tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
for t in tables:
    print(f'  {t[0]}')

# Try to find the right table that holds apiclaude/anthropic keys
print('\nSearching for key-related tables...')
for tbl_row in tables:
    tbl = tbl_row[0]
    try:
        cols = cur.execute(f'PRAGMA table_info({tbl})').fetchall()
        col_names = [c[1] for c in cols]
        if any(c in col_names for c in ['provider', 'profile_id', 'name']) and any(c in col_names for c in ['api_key', 'token', 'value']):
            print(f'\nTable: {tbl}')
            print(f'  Columns: {col_names}')
            rows = cur.execute(f'SELECT * FROM {tbl}').fetchall()
            for r in rows[:20]:
                # Truncate any token-looking fields
                r_show = []
                for i, v in enumerate(r):
                    s = str(v) if v else ''
                    if 'key' in col_names[i].lower() or 'token' in col_names[i].lower() or 'auth' in col_names[i].lower():
                        s = s[:6] + '...' + s[-4:] if len(s) > 12 else s
                    r_show.append(s)
                print(f'  {tuple(r_show)}')
    except Exception as e:
        pass

conn.close()