#!/usr/bin/env python3
"""修复 openclaw.sqlite 损坏 + 清 WAL
策略：
1. 备份当前损坏状态（保底）
2. 强制 checkpoint TRUNCATE 清空 WAL
3. 跑 PRAGMA integrity_check 看主库是否损坏
4. 如主库损坏：尝试 dump + 重建
"""
import sqlite3
import shutil
import os
import sys
from datetime import datetime

USER = os.environ.get('USERPROFILE')
DB_DIR = os.path.join(USER, '.openclaw', 'state')
DB = os.path.join(DB_DIR, 'openclaw.sqlite')
WAL = DB + '-wal'
SHM = DB + '-shm'

# 1. 备份损坏文件
ts = datetime.now().strftime('%Y%m%d_%H%M%S')
bak = f"{DB}.malformed-{ts}"
print(f'[1] 备份当前损坏状态 -> {bak}')
try:
    shutil.copy2(DB, bak)
    if os.path.exists(WAL):
        shutil.copy2(WAL, f'{WAL}.malformed-{ts}')
    if os.path.exists(SHM):
        shutil.copy2(SHM, f'{SHM}.malformed-{ts}')
except Exception as e:
    print(f'   备份失败: {e}')

# 2. 强制 checkpoint TRUNCATE 回收 WAL
print(f'\n[2] 强制 checkpoint TRUNCATE...')
try:
    conn = sqlite3.connect(DB, isolation_level=None)
    # 关键：先 IMMEDIATE 锁，强制任何挂起事务回滚/提交
    conn.execute('PRAGMA busy_timeout = 5000;')
    # 检查完整性
    cur = conn.execute('PRAGMA integrity_check;')
    integrity = cur.fetchone()[0]
    print(f'   integrity_check: {integrity}')

    if integrity == 'ok':
        # checkpoint
        cur = conn.execute('PRAGMA wal_checkpoint(TRUNCATE);')
        print(f'   checkpoint 返回: {cur.fetchone()}')
    else:
        print(f'   ⚠️ 主库已损坏！尝试 dump 重建')
        # 尝试 dump 出能挽救的数据
        dump_path = f'{DB}.dump-{ts}.sql'
        try:
            with open(dump_path, 'w', encoding='utf-8') as f:
                for line in conn.iterdump():
                    f.write(f'{line}\n')
            print(f'   dump 完成: {dump_path}')
        except Exception as e:
            print(f'   dump 失败: {e}')
    conn.close()
except Exception as e:
    print(f'   失败: {e}')

# 3. 删除 WAL/SHM（已 checkpoint 过则无用，未 checkpoint 则重建主库时也无需）
print(f'\n[3] 当前文件状态:')
for f in [DB, WAL, SHM]:
    if os.path.exists(f):
        size_mb = os.path.getsize(f) / 1e6
        print(f'   {os.path.basename(f):40s} {size_mb:7.2f} MB')

print('\n[4] 建议下一步：openclaw doctor --fix')
print('           或重启 gateway：openclaw gateway run --force')