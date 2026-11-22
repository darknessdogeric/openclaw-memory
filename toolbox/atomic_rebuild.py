#!/usr/bin/env python3
"""atomic_rebuild.py - 杀进程 + 立即重建
不 sleep，不轮询，一把搞定
"""
import os
import shutil
import sqlite3
import subprocess
from datetime import datetime

USER = os.environ.get('USERPROFILE')
TS = datetime.now().strftime('%Y%m%d_%H%M%S')

DBS = [
    os.path.join(USER, '.openclaw', 'state', 'openclaw.sqlite'),
    os.path.join(USER, '.openclaw', 'agents', 'main', 'agent', 'openclaw-agent.sqlite'),
    os.path.join(USER, '.openclaw', 'agents', 'anyi', 'agent', 'openclaw-agent.sqlite'),
]

# 1. 找所有 node 进程并强杀
print('[1] 杀所有 node 进程...')
subprocess.run(['powershell', '-NoProfile', '-Command',
    'Get-Process -Name node -ErrorAction SilentlyContinue | Stop-Process -Force'],
    capture_output=True)

# 2. 立即 dump + 重建（无 sleep）
print('[2] 立即 dump + 重建...')
for db in DBS:
    if not os.path.exists(db):
        continue
    name = os.path.relpath(db, USER)
    bak = f'{db}.atomic-bak-{TS}'
    dump = f'{db}.atomic-dump-{TS}.sql'
    print(f'\n  → {name}')

    # 备份
    try:
        shutil.copy2(db, bak)
        for s in ['-wal', '-shm']:
            if os.path.exists(db + s):
                shutil.copy2(db + s, bak + s)
    except Exception as e:
        print(f'    ⚠️ 备份失败: {e}')

    # dump
    try:
        src = sqlite3.connect(f'file:{db}?mode=ro', uri=True, timeout=5)
        with open(dump, 'w', encoding='utf-8') as f:
            for line in src.iterdump():
                f.write(f'{line}\n')
        src.close()
        print(f'    dump: {os.path.getsize(dump)/1e6:.1f} MB')
    except Exception as e:
        print(f'    ❌ dump 失败: {e}')
        continue

    # 删 WAL/SHM/原 DB
    for f in [db + '-wal', db + '-shm', db]:
        try:
            if os.path.exists(f):
                os.remove(f)
        except Exception as e:
            print(f'    ⚠️ 删 {os.path.basename(f)} 失败: {e}')

    # 重建
    try:
        new = sqlite3.connect(db)
        with open(dump, 'r', encoding='utf-8') as f:
            new.executescript(f.read())
        new.execute('PRAGMA wal_checkpoint(TRUNCATE);')
        new.close()
        new_size = os.path.getsize(db) / 1e6
        verify = sqlite3.connect(db, timeout=5).execute('PRAGMA integrity_check;').fetchone()[0]
        print(f'    ✅ 重建: {new_size:.1f} MB, integrity={verify}')
    except Exception as e:
        print(f'    ❌ 重建失败: {e}')

    # 清 dump
    if os.path.exists(dump):
        os.remove(dump)

print('\n[3] gateway 应该自动重启...')
# 让 OpenClaw 自己重启 gateway
subprocess.run(['powershell', '-NoProfile', '-Command',
    'Start-Sleep 3; (Get-Process -Name node -ErrorAction SilentlyContinue).Id | ConvertTo-Json'],
    capture_output=True)

print('\n=== 完成 ===')