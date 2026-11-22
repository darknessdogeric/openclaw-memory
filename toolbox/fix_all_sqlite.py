#!/usr/bin/env python3
"""扫描所有 .sqlite 文件，做 integrity_check 并尝试 checkpoint 修复"""
import sqlite3
import os
import glob
import sys
from datetime import datetime

USER = os.environ.get('USERPROFILE')
DB_DIRS = [
    os.path.join(USER, '.openclaw', 'state'),
    os.path.join(USER, '.openclaw', 'agents'),
    os.path.join(USER, '.openclaw', 'flows'),
    os.path.join(USER, '.openclaw', 'tasks'),
    os.path.join(USER, '.openclaw', 'tmp'),
]

results = []
for d in DB_DIRS:
    if not os.path.exists(d):
        continue
    for db in glob.glob(os.path.join(d, '**', '*.sqlite'), recursive=True):
        wal = db + '-wal'
        shm = db + '-shm'
        # 只处理主库文件（不要 .tmp-xxx / .bak / .migrated / .lock / .writer / .memory-reindex-*）
        if any(suffix in db for suffix in ['.tmp-', '.bak', '.migrated', '.lock', '.writer', '.memory-reindex-', 'journal', 'pre-canonical', 'pre-trigger', 'doctor-backup', 'pre-fix', 'pre-migration', '.v2-pre-', 'malformed']):
            continue
        if not os.path.exists(db):
            continue
        size_mb = os.path.getsize(db) / 1e6
        wal_mb = os.path.getsize(wal) / 1e6 if os.path.exists(wal) else 0
        try:
            conn = sqlite3.connect(db, timeout=10, isolation_level=None)
            cur = conn.execute('PRAGMA integrity_check;')
            integrity = cur.fetchone()[0]
            wal_size_before = wal_mb
            if integrity == 'ok' and wal_mb > 1:
                # 尝试 checkpoint TRUNCATE
                cur = conn.execute('PRAGMA wal_checkpoint(TRUNCATE);')
                ckpt = cur.fetchone()
                wal_size_after = os.path.getsize(wal) / 1e6 if os.path.exists(wal) else 0
                results.append((os.path.relpath(db, USER), f'{size_mb:.1f}', f'{wal_size_before:.1f}', f'{wal_size_after:.1f}', f'CHECKPOINT ({ckpt})'))
            elif integrity == 'ok':
                results.append((os.path.relpath(db, USER), f'{size_mb:.1f}', f'{wal_mb:.1f}', '-', 'ok'))
            else:
                results.append((os.path.relpath(db, USER), f'{size_mb:.1f}', f'{wal_mb:.1f}', '-', f'⚠️ CORRUPTED: {integrity[:40]}'))
            conn.close()
        except Exception as e:
            results.append((os.path.relpath(db, USER), f'{size_mb:.1f}', f'{wal_mb:.1f}', '-', f'ERROR: {str(e)[:60]}'))

print(f"{'DB Path':<70} {'DB MB':>8} {'WAL BEFORE':>12} {'WAL AFTER':>11} {'STATUS'}")
print('-' * 130)
for r in results:
    print(f"{r[0]:<70} {r[1]:>8} {r[2]:>12} {r[3]:>11} {r[4]}")
print()
print('说明：只处理主 .sqlite 文件（跳过 .tmp-/.bak/.migrated/.lock 等临时文件）')