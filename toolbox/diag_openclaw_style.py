import urllib.request
import urllib.error
import re
import json

with open(r'D:\B166ER-OpenClaw\openclaw.json', 'r', encoding='utf-8') as f:
    content = f.read()
m = re.search(r'"apiclaude":\s*\{[^}]*"auth":\s*"([^"]+)"', content, re.DOTALL)
key = m.group(1)
print(f'openclaw.json 里的 key: {key[:6]}...{key[-4:]} (len={len(k)})' if False else f'Key prefix: {key[:6]}, suffix: ...{key[-4:]} (len={len(key)})')

# Test mimicking OpenClaw's likely request style
req = urllib.request.Request(
    'https://apiclaude.cc/v1/messages',
    method='POST',
    headers={
        'x-api-key': key,
        'anthropic-version': '2023-06-01',
        'anthropic-beta': 'prompt-caching-2024-07-31',
        'content-type': 'application/json',
        'user-agent': 'openclaw/1.0',
    },
    data=json.dumps({
        'model': 'claude-opus-4-8',
        'max_tokens': 16,
        'messages': [{'role': 'user', 'content': 'hi'}]
    }).encode('utf-8')
)
try:
    resp = urllib.request.urlopen(req, timeout=15)
    body = resp.read().decode('utf-8')
    print(f'HTTP {resp.status} OK: {body[:300]}')
except urllib.error.HTTPError as e:
    body = e.read().decode('utf-8', errors='replace')
    print(f'HTTP {e.code}: {body[:500]}')
except Exception as e:
    print(f'EXCEPTION: {type(e).__name__}: {e}')