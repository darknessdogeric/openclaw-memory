# -*- coding: utf-8 -*-
"""模型更新基线检查 — 不输出任何密钥"""
import json, os, urllib.request, urllib.error

# 1. 读 .env 取 DEEPSEEK_API_KEY(不打印)
keys = {}
env_path = os.path.expanduser(r'~\.openclaw\.env')
with open(env_path, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if '=' in line and not line.startswith('#'):
            k, v = line.split('=', 1)
            keys[k.strip()] = v.strip().strip('"').strip("'")

# 2. 读配置中的模型
with open(os.path.expanduser(r'~\.openclaw\openclaw.json'), 'r', encoding='utf-8') as f:
    cfg = json.load(f)

configured = {}
for prov, pdata in cfg.get('models', {}).get('providers', {}).items():
    configured[prov] = [m.get('id') for m in pdata.get('models', [])]

print('=== 配置中的模型 ===')
for prov, ids in configured.items():
    print(f'  [{prov}] {ids}')
print()

# 3. 查询 DeepSeek /models
def query(url, key, label):
    if not key:
        print(f'[{label}] 无可用 key, 跳过')
        return None
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {key}'})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read().decode('utf-8'))
        return data
    except urllib.error.HTTPError as e:
        print(f'[{label}] HTTP {e.code}: {e.reason}')
    except Exception as e:
        print(f'[{label}] ERR: {type(e).__name__}: {e}')
    return None

print('=== DeepSeek /models 实查 ===')
ds = query('https://api.deepseek.com/models', keys.get('DEEPSEEK_API_KEY'), 'deepseek')
if ds:
    remote = [m.get('id') for m in ds.get('data', [])]
    print(f'  远端可用: {remote}')
    new = [m for m in remote if m not in configured.get('deepseek', [])]
    missing = [m for m in configured.get('deepseek', []) if m not in remote]
    print(f'  ⭐ 新增(需加入): {new if new else "无"}')
    print(f'  ⚠️  配置有但远端无: {missing if missing else "无"}')
