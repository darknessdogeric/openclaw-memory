"""Test apiclaude.cc connectivity with the real key from openclaw.json"""
import urllib.request
import urllib.error
import ssl
import json
import re

# Read the key from openclaw.json
with open(r'D:\B166ER-OpenClaw\openclaw.json', 'r', encoding='utf-8') as f:
    content = f.read()

m = re.search(r'"apiclaude":\s*\{[^}]*"auth":\s*"([^"]+)"', content, re.DOTALL)
if not m:
    print('FAIL: cannot extract apiclaude auth from openclaw.json')
    raise SystemExit(1)
key = m.group(1)
print(f'Key length: {len(key)}, prefix: {key[:6]}, suffix: ...{key[-4:]}')
if key.startswith('REPLACE'):
    print('FAIL: key still placeholder')
    raise SystemExit(1)

# Test 1: models endpoint
print('\n=== TEST 1: GET /v1/models ===')
req = urllib.request.Request(
    'https://apiclaude.cc/v1/models',
    headers={
        'x-api-key': key,
        'anthropic-version': '2023-06-01',
    }
)
try:
    resp = urllib.request.urlopen(req, timeout=15, context=ssl.create_default_context())
    body = resp.read().decode('utf-8')
    print(f'HTTP {resp.status} OK')
    print(f'Body: {body[:400]}')
except urllib.error.HTTPError as e:
    body = e.read().decode('utf-8', errors='replace')
    print(f'HTTP {e.code}: {body[:400]}')
except Exception as e:
    print(f'EXCEPTION: {type(e).__name__}: {e}')

# Test 2: minimal messages request
print('\n=== TEST 2: POST /v1/messages (minimal) ===')
data = json.dumps({
    'model': 'claude-opus-4-8',
    'max_tokens': 16,
    'messages': [{'role': 'user', 'content': 'hi'}]
}).encode('utf-8')
req = urllib.request.Request(
    'https://apiclaude.cc/v1/messages',
    data=data,
    headers={
        'x-api-key': key,
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json',
    }
)
try:
    resp = urllib.request.urlopen(req, timeout=20, context=ssl.create_default_context())
    body = resp.read().decode('utf-8')
    print(f'HTTP {resp.status} OK')
    print(f'Body: {body[:400]}')
except urllib.error.HTTPError as e:
    body = e.read().decode('utf-8', errors='replace')
    print(f'HTTP {e.code}: {body[:600]}')
except Exception as e:
    print(f'EXCEPTION: {type(e).__name__}: {e}')