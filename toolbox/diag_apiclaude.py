import re
import urllib.request
import urllib.error
import ssl
import json

with open(r'D:\B166ER-OpenClaw\openclaw.json', 'r', encoding='utf-8') as f:
    content = f.read()

m = re.search(r'"apiclaude":\s*\{[^}]*"auth":\s*"([^"]+)"', content, re.DOTALL)
if not m:
    print('FAIL: cannot find apiclaude auth in openclaw.json')
    raise SystemExit(1)

key = m.group(1)
print(f'Key found: len={len(key)}, prefix={key[:6]}, suffix=...{key[-4:]}')
print(f'Is placeholder: {key.startswith("REPLACE")}')
if key.startswith('REPLACE'):
    print('\n>>> Please replace the placeholder with your real key first.')
    raise SystemExit(0)

# Test 1: GET /v1/models
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
    print(f'Body: {body[:300]}')
except urllib.error.HTTPError as e:
    body = e.read().decode('utf-8', errors='replace')
    print(f'HTTP {e.code}: {body[:400]}')
except Exception as e:
    print(f'EXCEPTION: {type(e).__name__}: {e}')

# Test 2: POST /v1/messages minimal
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