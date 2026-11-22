"""Diagnose apiclaude auth mismatch between openclaw.json and auth store"""
import re
import urllib.request
import urllib.error
import ssl
import json
import sqlite3
from pathlib import Path

# 1. Read openclaw.json current auth
print('=' * 60)
print('STEP 1: openclaw.json 里配置的 apiclaude key')
print('=' * 60)
with open(r'D:\B166ER-OpenClaw\openclaw.json', 'r', encoding='utf-8') as f:
    content = f.read()
m = re.search(r'"apiclaude":\s*\{[^}]*"auth":\s*"([^"]+)"', content, re.DOTALL)
if m:
    cfg_key = m.group(1)
    print(f'Prefix: {cfg_key[:6]}, Suffix: ...{cfg_key[-4:]}, len={len(cfg_key)}')
    if cfg_key.startswith('REPLACE'):
        print('STATUS: placeholder still in file')
else:
    print('apiclaude key not found')
    raise SystemExit(0)

# 2. Read OpenClaw auth store (SQLite)
print()
print('=' * 60)
print('STEP 2: OpenClaw auth store 里实际用的 key')
print('=' * 60)
auth_db = Path.home() / '.openclaw' / 'agents' / 'main' / 'agent' / 'openclaw-agent.sqlite'
print(f'DB: {auth_db}')
print(f'exists: {auth_db.exists()}')
if auth_db.exists():
    try:
        conn = sqlite3.connect(str(auth_db))
        cur = conn.cursor()
        # try common tables for storing keys
        for tbl in ['profiles', 'auth_profiles', 'credentials']:
            try:
                rows = cur.execute(f'SELECT * FROM {tbl}').fetchall()
                if rows:
                    print(f'\nTable {tbl}:')
                    for r in rows[:5]:
                        print(f'  {r}')
            except Exception as e:
                pass
        conn.close()
    except Exception as e:
        print(f'SQLite error: {e}')

# 3. Test the key directly with same payload style as OpenClaw uses
print()
print('=' * 60)
print('STEP 3: 直接调用 apiclaude.cc 验证 key 有效')
print('=' * 60)
data = json.dumps({
    'model': 'claude-opus-4-8',
    'max_tokens': 32,
    'system': 'You are a test assistant.',
    'messages': [{'role': 'user', 'content': 'Reply with the single word: PONG'}]
}).encode('utf-8')
req = urllib.request.Request(
    'https://apiclaude.cc/v1/messages',
    data=data,
    headers={
        'x-api-key': cfg_key,
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json',
    }
)
try:
    resp = urllib.request.urlopen(req, timeout=20, context=ssl.create_default_context())
    body = resp.read().decode('utf-8')
    print(f'HTTP {resp.status} OK')
    print(f'Response: {body[:400]}')
except urllib.error.HTTPError as e:
    body = e.read().decode('utf-8', errors='replace')
    print(f'HTTP {e.code}')
    print(f'Body: {body[:600]}')
except Exception as e:
    print(f'EXCEPTION: {type(e).__name__}: {e}')