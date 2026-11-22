# -*- coding: utf-8 -*-
"""R320 模型更新同步 — 备份 → 追加 → 验证"""
import json, shutil, datetime, os

cfg_path = os.path.expanduser(r'~\.openclaw\openclaw.json')
stamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
bak_path = f'{cfg_path}.bak-{stamp}'

# 1. 备份
shutil.copy2(cfg_path, bak_path)
print(f'[1] 备份: {bak_path}')

# 2. 读取
with open(cfg_path, 'r', encoding='utf-8') as f:
    cfg = json.load(f)

providers = cfg['models']['providers']

# 3. 检查各 provider 现有模型
for prov in providers:
    ids = [m['id'] for m in providers[prov]['models']]
    print(f'[2] {prov}: {ids}')

# 4. 追加新模型(只追加, 不删除)
added = []

# --- DeepSeek: deepseek-flash (V4.1 Flash, 2026-09-10 发布) ---
ds = providers['deepseek']
if 'deepseek-flash' not in [m['id'] for m in ds['models']]:
    template = dict(ds['models'][0])  # 复用第一个模型的字段结构
    template.update({
        "id": "deepseek-flash",
        "name": "DeepSeek V4.1 Flash",
        "contextWindow": 1000000,
        "maxTokens": 8192,
    })
    ds['models'].insert(0, template)
    added.append('deepseek/deepseek-flash')

# --- Moonshot: kimi-k3 (2026-07-16 发布, 2.8T 参数, 1M 上下文) ---
mo = providers['moonshot']
if 'kimi-k3' not in [m['id'] for m in mo['models']]:
    template = dict(mo['models'][0])
    template.update({
        "id": "kimi-k3",
        "name": "Kimi K3",
        "contextWindow": 1000000,
        "maxTokens": 8192,
    })
    mo['models'].insert(0, template)
    added.append('moonshot/kimi-k3')

print(f'[3] 新增: {added if added else "(无)"}')

# 5. 写回
if added:
    with open(cfg_path, 'w', encoding='utf-8') as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    print(f'[4] 已写入配置')
else:
    print(f'[4] 无需写入')
    # 删除多余备份
    os.remove(bak_path)
    print(f'    (已删除空备份)')

# 6. 验证 JSON 可解析
with open(cfg_path, 'r', encoding='utf-8') as f:
    cfg2 = json.load(f)
print(f'[5] JSON 验证: OK ({len(cfg2["models"]["providers"])} providers)')
for prov in cfg2['models']['providers']:
    ids = [m['id'] for m in cfg2['models']['providers'][prov]['models']]
    print(f'    {prov}: {ids}')
