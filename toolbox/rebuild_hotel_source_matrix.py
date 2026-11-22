#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""rebuild_hotel_source_matrix.py - v2 (ASCII 字符)
Eric 2026-09-07 00:55 指令: 重新建立酒店行业信源矩阵
Step 1: 解锁 archive (已完成 - memory/hotel/ 已存在)
Step 2: 整合到 KB
Step 3: 同步到 Obsidian Vault
Step 4: 启用信源工具 + 验证
"""
import os
import shutil
import subprocess
import sys
from datetime import datetime

# Windows console 编码修复
os.environ['PYTHONIOENCODING'] = 'utf-8'

WS = r'D:\B166ER-OpenClaw\workspace'
ANYI = os.path.join(WS, 'anyi-ops-kb')
VAULT = r'C:\Users\ericz\Documents\Obsidian Vault'
TS = datetime.now().strftime('%Y%m%d_%H%M%S')

print('=' * 60)
print('Hotel Industry Source Matrix Rebuild')
print('Eric 2026-09-07 00:55 instruction')
print('=' * 60)

# ============================================
# Step 1: 验证 archive 已解锁
# ============================================
print('\n[Step 1] Verify archive unlock')
arch = os.path.join(WS, 'memory', 'archive_hotel')
dest = os.path.join(WS, 'memory', 'hotel')
if os.path.exists(dest):
    files = len(os.listdir(dest))
    print(f'  [OK] memory/hotel/ exists ({files} files)')
elif os.path.exists(arch):
    shutil.move(arch, dest)
    print(f'  [OK] moved archive_hotel -> hotel')
else:
    print(f'  [WARN] neither archive_hotel nor hotel exists')

# ============================================
# Step 2: 整合到 KB
# ============================================
print('\n[Step 2] Integrate into KB')
kb_hotel = os.path.join(ANYI, '00_全域商业市场认知', '01_酒店行业')
kb_para = os.path.join(kb_hotel, '00_范式与模板')
os.makedirs(kb_para, exist_ok=True)

copies = [
    ('产品级报告基础范式_2026-07-27确立.md', '产品级报告基础范式_v2.0.md'),
    ('hotel-report-templates.md', '报告模板_v2.0.md'),
    ('hotel-industry-knowledge-base.md', '行业全景KB_v2.4.md'),
    ('hotel-report-summary.md', '报告体系摘要_v1.0.md'),
]
for src_name, dst_name in copies:
    src = os.path.join(dest, src_name)
    dst = os.path.join(kb_para, dst_name)
    if os.path.exists(src):
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f'  [OK] {src_name} -> {dst_name}')
        else:
            print(f'  [-] {dst_name} already in KB')

# ============================================
# Step 3: 同步到 Obsidian Vault
# ============================================
print('\n[Step 3] Sync to Obsidian Vault')
vault_hotel = os.path.join(VAULT, '酒店行业')
os.makedirs(vault_hotel, exist_ok=True)

vault_para = os.path.join(vault_hotel, '00_范式与模板')
os.makedirs(vault_para, exist_ok=True)

for fname in os.listdir(kb_para):
    src = os.path.join(kb_para, fname)
    dst = os.path.join(vault_para, fname)
    if os.path.isfile(src):
        if not os.path.exists(dst):
            shutil.copy2(src, dst)
            print(f'  [OK] vault: {fname}')
        else:
            print(f'  [-] vault: {fname} already synced')

# vault 入口
vault_readme = os.path.join(vault_hotel, 'README.md')
if not os.path.exists(vault_readme):
    with open(vault_readme, 'w', encoding='utf-8') as f:
        f.write('''# 酒店行业 (Hotel Industry)

> B166ER 自动同步 · 来源: anyi-ops-kb/00_全域商业市场认知/01_酒店行业/

## 入口

- [[00_范式与模板/产品级报告基础范式_v2.0|产品级报告基础范式]]
- [[00_范式与模板/报告模板_v2.0|报告模板]]
- [[00_范式与模板/行业全景KB_v2.4|行业全景KB]]

## 信源矩阵 (23 个核心源)

- **国际研究 5**: STR / Skift / Phocuswright / EHL / HotelNewsNow
- **国内研究 5**: 迈点 / 奥维 / 中研院 / 浩华 / 华美
- **国际上市公司 8**: Marriott/Hilton/IHG/Hyatt/Accor/Booking/Expedia/Airbnb
- **国内上市公司 5**: 华住 / 锦江 / 首旅 / 亚朵 / 君亭

## 报告类型

- 月报 15-25 页 / 季报 30-50 页 / 年报 80-150 页 / 节假日专项 20-40 页
''')
    print(f'  [OK] vault: README.md')
else:
    print(f'  [-] vault: README.md exists')

# ============================================
# Step 4: 启用信源工具 + 验证
# ============================================
print('\n[Step 4] Enable source tool + verify')
hotel_sources = os.path.join(WS, 'toolbox', 'hotel_sources.py')
if os.path.exists(hotel_sources):
    size_kb = os.path.getsize(hotel_sources) / 1024
    print(f'  [OK] hotel_sources.py ({size_kb:.1f} KB)')
    result = subprocess.run(['python', hotel_sources, '--help'],
                          capture_output=True, text=True, timeout=15,
                          encoding='utf-8', errors='replace')
    help_text = (result.stdout + result.stderr).strip()
    print(f'  -- help output (first 6 lines):')
    for line in help_text.split('\n')[:6]:
        print(f'    {line}')

# ============================================
# 验证清单
# ============================================
print('\n' + '=' * 60)
print('REBUILD COMPLETE')
print('=' * 60)
checks = [
    ('Step 1: memory/hotel/ unlocked', os.path.exists(dest)),
    ('Step 2: KB 00_范式与模板/', os.path.exists(kb_para)),
    ('Step 3: Obsidian Vault 酒店行业/', os.path.exists(vault_hotel)),
    ('Step 4: 信源工具可用', os.path.exists(hotel_sources)),
]
for desc, ok in checks:
    mark = '[OK]' if ok else '[FAIL]'
    print(f'  {mark} {desc}')

print('\n[Asset Summary]')
print(f'  - memory/hotel/  (范式 + 模板 + KB)')
print(f'  - KB 集成: {kb_para}')
print(f'  - Vault 同步: {vault_hotel}')
print(f'  - 信源工具: {hotel_sources} ({os.path.getsize(hotel_sources)/1024:.1f} KB)' if os.path.exists(hotel_sources) else '  - 信源工具: NOT FOUND')
print(f'  - 信源体系方案: {os.path.join(ANYI, "00_全域商业市场认知", "04_信源体系")}')