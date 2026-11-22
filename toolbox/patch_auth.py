"""Inject working apiclaude key into OpenClaw auth_profile_store (overwrite anthropic:default)"""
import sqlite3
import re
import json
import time
from pathlib import Path

auth_db = Path.home() / '.openclaw' / 'agents' / 'main' / 'agent' / 'openclaw-agent.sqlite'

with open(r'D:\B166ER-OpenClaw\openclaw.json', 'r', encoding='utf-8') as f:
    content = f.read()
m = re.search(r'"apiclaude":\s*\{[^}]*"auth":\s*"([^"]+)"', content, re.DOTALL)
new_key = m.group(1) if m else None
print(f'New key: {new_key[:6]}...{new_key[-4:]} (len={len(new_key)})')

conn = sqlite3.connect(str(auth_db))
cur = conn.cursor()

# Read current store_json
row = cur.execute("SELECT store_json FROM auth_profile_store WHERE store_key='primary'").fetchone()
store = json.loads(row[0])

# Update anthropic:default profile with new key
if 'anthropic:default' in store.get('profiles', {}):
    old_key = store['profiles']['anthropic:default']['key']
    print(f'Old anthropic key in store: {old_key[:6]}...{old_key[-4:]} (len={len(old_key)})')
    store['profiles']['anthropic:default']['key'] = new_key
    print(f'New anthropic key: {store["profiles"]["anthropic:default"]["key"][:6]}...{store["profiles"]["anthropic:default"]["key"][-4:]}')
else:
    print('No anthropic:default profile found, creating...')
    if 'profiles' not in store:
        store['profiles'] = {}
    store['profiles']['anthropic:default'] = {
        'type': 'api_key',
        'provider': 'anthropic',
        'key': new_key
    }

# Write back
new_json = json.dumps(store)
now_ms = int(time.time() * 1000)
cur.execute(
    "UPDATE auth_profile_store SET store_json=?, updated_at=? WHERE store_key='primary'",
    (new_json, now_ms)
)
conn.commit()
print(f'\nUpdated auth_profile_store at {now_ms}')

# Verify
row = cur.execute("SELECT store_json FROM auth_profile_store WHERE store_key='primary'").fetchone()
verify = json.loads(row[0])
print(f'Verified anthropic key: {verify["profiles"]["anthropic:default"]["key"][:6]}...{verify["profiles"]["anthropic:default"]["key"][-4:]}')

conn.close()
print('\nDONE. Now restart gateway with: openclaw gateway restart')