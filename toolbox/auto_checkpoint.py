#!/usr/bin/env python3
"""auto_checkpoint.py - 每 4 分钟对所有 agent SQLite 做 PASSIVE checkpoint（不持锁）
目的：防止 WAL 累积导致 disk image malformed

PASSIVE checkpoint: 不阻塞写入，但能把已经同步的 page 写回主库
"""
import sqlite3
import os
import glob
import sys

USER = os.environ.get('USERPROFILE')
DBS = [
    os.path.join(USER, '.openclaw', 'state', 'openclaw.sqlite'),
    os.path.join(USER, '.openclaw', 'agents', 'main', 'agent', 'openclaw-agent.sqlite'),
    os.path.join(USER, '.openclaw', 'agents', 'anyi', 'agent', 'openclaw-agent.sqlite'),
    os.path.join(USER, '.openclaw', 'agents', 'coder', 'agent', 'openclaw-agent.sqlite'),
]

for db in DBS:
    if not os.path.exists(db):
        continue
    wal = db + '-wal'
    if not os.path.exists(wal):
        continue
    wal_mb = os.path.getsize(wal) / 1e6
    if wal_mb < 1:  # 小于 1MB 跳过
        continue
    try:
        # timeout=0 让它不阻塞，busy 时直接放弃
        conn = sqlite3.connect(db, timeout=2, isolation_level=None)
        # PASSIVE = 不等写锁，能做就做，做不了就跳过
        cur = conn.execute('PRAGMA wal_checkpoint(PASSIVE);')
        ckpt = cur.fetchone()
        new_wal_mb = os.path.getsize(wal) / 1e6 if os.path.exists(wal) else 0
        sys.stderr.write(f'[checkpoint] {os.path.relpath(db, USER)}: {wal_mb:.1f}MB -> {new_wal_mb:.1f}MB ({ckpt[0]},{ckpt[1]},{ckpt[2]})\n')
        conn.close()
    except sqlite3.OperationalError as e:
        # busy_timeout 到了,下次再试
        sys.stderr.writef('[busy] {os.path.relpath(db, USER)}: {e}\n')
    except Exception as e:
        sys.stderr.write(f'[err] {os.path.relpath(db, USER)}: {e}\n')