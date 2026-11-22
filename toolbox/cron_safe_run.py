#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cron_safe_run.py - Cron 任务安全启动器
R296 实现：每个 cron 启动前自动 checkpoint + busy_timeout + WAL 防御
Eric 2026-09-08 15:04 决策编写
"""
import os
import sys
import sqlite3
import subprocess
from pathlib import Path
from datetime import datetime

USER = os.environ.get('USERPROFILE') or os.environ.get('HOME')
OPENCLAW_DB = os.path.join(USER, '.openclaw', 'state', 'openclaw.sqlite')

def checkpoint_all_dbs(timeout=10):
    """所有 OpenClaw SQLite 数据库 PASSIVE checkpoint"""
    db_paths = [
        os.path.join(USER, '.openclaw', 'state', 'openclaw.sqlite'),
        os.path.join(USER, '.openclaw', 'agents', 'main', 'agent', 'openclaw-agent.sqlite'),
        os.path.join(USER, '.openclaw', 'agents', 'anyi', 'agent', 'openclaw-agent.sqlite'),
        os.path.join(USER, '.openclaw', 'agents', 'coder', 'agent', 'openclaw-agent.sqlite'),
    ]
    for db_path in db_paths:
        if not os.path.exists(db_path):
            continue
        try:
            conn = sqlite3.connect(db_path, timeout=timeout)
            conn.execute('PRAGMA busy_timeout = 30000')
            conn.execute('PRAGMA wal_checkpoint(PASSIVE)')
            conn.close()
            print(f'  [OK] checkpoint {db_path}')
        except sqlite3.OperationalError as e:
            print(f'  [WARN] {db_path}: {e}')
        except Exception as e:
            print(f'  [ERR] {db_path}: {e}')

if __name__ == '__main__':
    print(f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] R296 cron safe run starting')
    checkpoint_all_dbs()
    print('Checkpoint done, ready for cron task to run')
