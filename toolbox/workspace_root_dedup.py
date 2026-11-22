#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
workspace_root_dedup.py — 工作根文件去重决策器
依据：Eric 2026-07-22 「不丢信息」原则
  - 字节级重复 (md5 match) → 标记，可安全删
  - 仅同名相近 (size diff) → vault 是新规范，保留两边不同步（避免覆盖）
  - 完全唯一 (vault 无) → 推荐同步
"""
import os
import sys
import json
import hashlib
from pathlib import Path

WORKSPACE = Path(r'D:\B166ER-OpenClaw\workspace')
VAULT = WORKSPACE / 'obsidian-vault'
INDEX = WORKSPACE / 'toolbox' / '.vault_index.json'

def md5(p):
    return hashlib.md5(Path(p).read_bytes()).hexdigest()

def scan_files(target):
    out = {}
    for f in target.rglob('*.md'):
        rel = f.relative_to(target)
        out[str(rel).replace('\\', '/')] = str(f)
    for f in target.rglob('*.pdf'):
        rel = f.relative_to(target)
        out[str(rel).replace('\\', '/')] = str(f)
    return out

# BOOTSTRAP 文件保留在工作根，不参与去重
BOOTSTRAP = {
    'HEARTBEAT.md', 'MEMORY.md', 'DREAMS.md', 'TOOLS.md',
    'AGENTS.md', 'SOUL.md', 'USER.md', 'IDENTITY.md',
    'B166ER-STYLE.md', 'B166ER-底层理论架构-V2.2.md',
    'PROJECT-TRACKING.md',
}

def main():
    ws_files = {}
    for f in WORKSPACE.iterdir():
        if f.is_file() and f.suffix in {'.md', '.pdf'} and f.name not in BOOTSTRAP:
            ws_files[f.name] = str(f)

    # 全 vault md5 索引
    print('Scanning vault...')
    vault_index = {}  # name -> (md5, full_path)
    for f in VAULT.rglob('*.md'):
        vault_index[str(f.relative_to(VAULT)).replace('\\', '/')] = (
            md5(f), str(f)
        )
    print(f'Vault indexed: {len(vault_index)} files')

    decisions = {'exact_dup': [], 'version_diff': [], 'unique': []}

    for name, ws_path in sorted(ws_files.items()):
        ws_h = md5(ws_path)

        # 1. 字节级重复：精确同名文件 md5 一致
        for vp, (vm, _) in vault_index.items():
            if vp.endswith('/' + name) and vm == ws_h:
                decisions['exact_dup'].append({
                    'name': name,
                    'ws': ws_path,
                    'vault': vp,
                    'md5': ws_h,
                })
                break
        else:
            # 2. 同名但 md5 不同：vault 是不同版本
            same_name_found = False
            for vp, (vm, _) in vault_index.items():
                if vp.endswith('/' + name):
                    ws_size = Path(ws_path).stat().st_size
                    vt_size = Path(VAULT / vp).stat().st_size
                    decisions['version_diff'].append({
                        'name': name,
                        'ws_path': ws_path,
                        'vault_path': vp,
                        'ws_size': ws_size,
                        'vault_size': vt_size,
                        'vault_is_bigger': vt_size > ws_size,
                    })
                    same_name_found = True
                    break
            if not same_name_found:
                # 3. vault 里完全没这个文件
                decisions['unique'].append({
                    'name': name,
                    'ws_path': ws_path,
                    'size': Path(ws_path).stat().st_size,
                })

    # Output
    print()
    print('=' * 70)
    print('EXACT DUPLICATES (md5 match, safe to delete from workspace)')
    print('=' * 70)
    for d in decisions['exact_dup']:
        print(f"  {d['name']}")
        print(f"    ws:   {d['ws']}")
        print(f"    vault:{d['vault']}")
        print(f"    md5:  {d['md5']}")

    print()
    print('=' * 70)
    print('VERSION DIFFERENT (vault has newer/larger canonical, KEEP BOTH)')
    print('=' * 70)
    for d in decisions['version_diff']:
        marker = '[vault BIGGER]' if d['vault_is_bigger'] else '[workspace BIGGER ← sync to vault]'
        print(f"  {marker} {d['name']}")
        print(f"    ws:   {d['ws_size']:>10,}B  {d['ws_path']}")
        print(f"    vault:{d['vault_size']:>10,}B  {d['vault_path']}")

    print()
    print('=' * 70)
    print('UNIQUE IN WORKSPACE (not in vault, sync recommended)')
    print('=' * 70)
    for d in decisions['unique']:
        print(f"  {d['name']:60s} {d['size']:>10,}B")
        print(f"    ws: {d['ws_path']}")

    # Summary
    print()
    print('=' * 70)
    print('SUMMARY')
    print('=' * 70)
    print(f"  exact duplicates (md5 match):       {len(decisions['exact_dup'])}")
    print(f"  version-diff (same name, diff md5): {len(decisions['version_diff'])}")
    print(f"  unique to workspace (sync needed):  {len(decisions['unique'])}")

if __name__ == '__main__':
    main()
