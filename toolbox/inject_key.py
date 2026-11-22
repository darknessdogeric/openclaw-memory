"""Inject working apiclaude key into OpenClaw auth_profile_store"""
import sqlite3
import re
from pathlib import Path

auth_db = Path.home() / '.openclaw' / 'agents' / 'main' / 'agent' / 'openclaw-agent.sqlite'

with open(r'D:\B166ER-OpenClaw\openclaw.json', 'r', encoding='utf-8') as f:
    content = f.read()
m = re.search(r'"apiclaude":\s*\{[^}]*"auth":\s*"([^"]+)"', content, re.DOTALL)
new_key = m.group(1) if m else None
print(f'Key to inject: {new_key[:6]}...{new_key[-4:]} (len={len(new_key)})')

conn = sqlite3.connect(str(auth_db))
cur = conn.cursor()

# Show schema and current rows
print('\nTable schema for auth_profile_store:')
cols = cur.execute('PRAGMA table_info(auth_profile_store)').fetchall()
for c in cols:
    print(f'  {c}')

print('\nCurrent rows:')
rows = cur.execute('SELECT * FROM auth_profile_store').fetchall()
for r in rows:
    safe = []
    for i, v in enumerate(r):
        s = str(v) if v is not None else 'NULL'
        # truncate token-looking fields
        col_name = cols[i][1] if i < len(cols) else ''
        if 'key' in col_name.lower() or 'token' in col_name.lower() or 'auth' in col_name.lower() or 'secret' in col_name.lower() or 'value' in col_name.lower():
            if len(s) > 12:
                s = s[:6] + '...' + s[-4:]
        safe.append(s)
    print(f'  {tuple(safe)}')