#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""分析 37 个同名 + 安逸集团详细"""
import json
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

r = json.load(open(r'D:\B166ER-OpenClaw\workspace\toolbox\overlap_report.json', encoding='utf-8'))

print('=== 37 个同名但内容不同样本 (前 20) ===')
for o in r['overlaps_name_only'][:20]:
    print(f"  {o['desktop']}")
    for vp in o['vault_paths'][:1]:
        print(f"    -> {vp}")

print(f"\n... 总共 {len(r['overlaps_name_only'])} 个同名")

print('\n=== 安逸集团_入职物料 11 文件 vs vault 重叠分析 ===')
for f in r['by_dir']['安逸集团_入职物料_20260707']['files']:
    flag = '同名' if f['in_vault'] else '孤'
    md = f.get('md5', '')[:8] if f.get('md5') else 'N/A'
    sz = f['size']
    print(f"  [{flag}] md5={md} size={sz:6d}B  {f['name']}")
    if f['vault_match']:
        for vm in f['vault_match'][:1]:
            print(f"        vault: {vm['path']}  same_md5={vm['same_md5']}")

# 按大小看哪些同名的大
print('\n=== 同名按桌面文件大小排序 (前 15) ===')
sorted_overlaps = sorted(r['overlaps_name_only'],
                         key=lambda x: -sum(1 for _ in []))
# 这个排序没意义,做实在的:按每个overlap的size排序
overlap_with_size = []
for o in r['overlaps_name_only']:
    # 找原始 entry
    for d, info in r['by_dir'].items():
        for f in info['files']:
            if f['rel'] == o['desktop']:
                overlap_with_size.append((f['size'], o['desktop'], o['vault_paths'][0] if o['vault_paths'] else ''))
                break
overlap_with_size.sort(reverse=True)
for sz, d, vp in overlap_with_size[:15]:
    print(f"  {sz:7d}B  {d}")
    print(f"            -> {vp}")
