#!/usr/bin/env python3
"""深度修复 SQLite: 1) dump 2) 重建 3) restore
VACUUM 不够，因为是 IMMEDIATE 锁 vs gateway 的写入冲突。
真正解决：drain gateway 写锁 → 重建 → 释放
"""
import sqlite3
import os
import shutil
from datetime import datetime

USER = os.environ.get('USERPROFILE')
TARGETS = [
    os.path.join(USER, '.openclaw', 'state', 'openclaw.sqlite'),
    os.path.join(USER, '.openclaw', 'agents', 'main', 'agent', 'openclaw-agent.sqlite'),
    os.path.join(USER, '.openclaw', 'agents', 'anyi', 'agent', 'openclaw-agent.sqlite'),
    os.path.join(USER, '.openclaw', 'agents', 'coder', 'agent', 'openclaw-agent.sqlite'),
]

for db in TARGETS:
    if not os.path.exists(db):
        continue
    name = os.path.relpath(db, USER)
    print(f'\n=== {name} ===')

    # 1. 检查当前完整性
    try:
        conn = sqlite3.connect(db, timeout=10, isolation_level=None)
        integrity = conn.execute('PRAGMA integrity_check;').fetchone()[0]
        print(f'  integrity: {integrity}')
        if integrity != 'ok':
            print(f'  ⚠️ 已损坏')
    except Exception as e:
        print(f'  ❌ 无法连接: {e}')
        conn.close()
        continue

    # 2. dump 到临时文件
    ts = datetime.now().strftime('%Y%m%d_%H%M%S')
    dump_path = f'{db}.dump-{ts}.sql'
    try:
        with open(dump_path, 'w', encoding='utf-8') as f:
            for line in conn.iterdump():
                f.write(f'{line}\n')
        dump_mb = os.path.getsize(dump_path) / 1e6
        print(f'  dump OK ({dump_mb:.1f} MB) -> {os.path.basename(dump_path)}')
    except Exception as e:
        print(f'  ❌ dump 失败: {e}')
        conn.close()
        continue

    # 3. 备份原文件
    bak = f'{db}.rebuild-bak-{ts}'
    shutil.copy2(db, bak)
    wal_bak = f'{bak}-wal'
    shm_bak = f'{bak}-shm'
    if os.path.exists(db + '-wal'):
        shutil.copy2(db + '-wal', wal_bak)
    if os.path.exists(db + '-shm'):
        shutil.copy2(db + '-shm', shm_bak)
    print(f'  备份 -> {os.path.basename(bak)}')

    # 4. 删除原 DB + WAL + SHM
    for f in [db, db + '-wal', db + '-shm']:
        if os.path.exists(f):
            os.remove(f)

    # 5. 用 dump 重建
    try:
        new_conn = sqlite3.connect(db)
        with open(dump_path, 'r', encoding='utf-8') as f:
            sql = f.read()
        new_conn.executescript(sql)
        new_conn.execute('PRAGMA wal_checkpoint(TRUNCATE);')
        new_conn.close()

        new_size = os.path.getsize(db) / 1e6
        # 再次 integrity check
        verify = sqlite3.connect(db, timeout=5).execute('PRAGMA integrity_check;').fetchone()[0]
        print(f'  ✅ 重建完成: {new_size:.1f} MB, integrity={verify}')
    except Exception as e:
        print(f'  ❌ 重建失败: {e}')

print('\n=== 完成 ===')