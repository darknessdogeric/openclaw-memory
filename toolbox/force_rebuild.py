#!/usr/bin/env python3
"""force_rebuild.py - 强制重建 agent session store
执行步骤：
1. 停 gateway (taskkill)
2. 备份原 DB
3. dump → 重建 → VACUUM
4. gateway 自动重启
"""
import sqlite3
import os
import shutil
import subprocess
import time
from datetime import datetime

USER = os.environ.get('USERPROFILE')
DB = os.path.join(USER, '.openclaw', 'agents', 'main', 'agent', 'openclaw-agent.sqlite')
TS = datetime.now().strftime('%Y%m%d_%H%M%S')
BAK = f'{DB}.rebuild-bak-{TS}'

print(f'=== 强制重建 {os.path.relpath(DB, USER)} ===\n')

# 1. 找 gateway PID
print('[1] 找 gateway 进程...')
result = subprocess.run(['powershell', '-NoProfile', '-Command',
    '(Get-Process -Name node -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -match "openclaw.mjs gateway" }).Id'],
    capture_output=True, text=True)
pids = [int(p.strip()) for p in result.stdout.strip().split('\n') if p.strip().isdigit()]
print(f'    找到 PID: {pids}')

# 2. 停 gateway
print(f'\n[2] 停 gateway...')
for pid in pids:
    subprocess.run(['taskkill', '/PID', str(pid), '/F'], capture_output=True)
time.sleep(3)
# 验证
result = subprocess.run(['powershell', '-NoProfile', '-Command',
    '(Get-Process -Name node -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -match "openclaw.mjs gateway" }).Id'],
    capture_output=True, text=True)
new_pids = [int(p.strip()) for p in result.stdout.strip().split('\n') if p.strip().isdigit()]
print(f'    停后剩余 PID: {new_pids}')

# 3. 备份
print(f'\n[3] 备份原 DB...')
if os.path.exists(DB):
    shutil.copy2(DB, BAK)
    for suffix in ['-wal', '-shm']:
        if os.path.exists(DB + suffix):
            shutil.copy2(DB + suffix, BAK + suffix)
    print(f'    -> {os.path.basename(BAK)}')

# 4. 删 WAL/SHM (因为我们要重建)
print(f'\n[4] 删 WAL/SHM...')
for suffix in ['-wal', '-shm']:
    if os.path.exists(DB + suffix):
        os.remove(DB + suffix)
        print(f'    删 {suffix}')

# 5. dump 当前 main DB
print(f'\n[5] dump 主库...')
DUMP = f'{DB}.dump-{TS}.sql'
try:
    src = sqlite3.connect(DB, timeout=10)
    with open(DUMP, 'w', encoding='utf-8') as f:
        for line in src.iterdump():
            f.write(f'{line}\n')
    src.close()
    print(f'    -> {os.path.basename(DUMP)} ({os.path.getsize(DUMP)/1e6:.1f} MB)')
except Exception as e:
    print(f'    ❌ dump 失败: {e}')
    exit(1)

# 6. 删原 DB
print(f'\n[6] 删原 DB (准备重建)...')
os.remove(DB)

# 7. 重建
print(f'\n[7] 从 dump 重建...')
try:
    new = sqlite3.connect(DB)
    with open(DUMP, 'r', encoding='utf-8') as f:
        new.executescript(f.read())
    new.execute('PRAGMA wal_checkpoint(TRUNCATE);')
    new.close()
    new_size = os.path.getsize(DB) / 1e6
    verify = sqlite3.connect(DB, timeout=5).execute('PRAGMA integrity_check;').fetchone()[0]
    print(f'    ✅ 重建完成: {new_size:.1f} MB, integrity={verify}')
except Exception as e:
    print(f'    ❌ 重建失败: {e}')
    exit(1)

# 8. 同样重建 state DB
print(f'\n[8] 同样重建 state/openclaw.sqlite...')
STATE_DB = os.path.join(USER, '.openclaw', 'state', 'openclaw.sqlite')
STATE_BAK = f'{STATE_DB}.rebuild-bak-{TS}'
STATE_DUMP = f'{STATE_DB}.dump-{TS}.sql'
if os.path.exists(STATE_DB):
    shutil.copy2(STATE_DB, STATE_BAK)
    for suffix in ['-wal', '-shm']:
        if os.path.exists(STATE_DB + suffix):
            shutil.copy2(STATE_DB + suffix, STATE_BAK + suffix)
            os.remove(STATE_DB + suffix)
    src = sqlite3.connect(STATE_DB, timeout=10)
    with open(STATE_DUMP, 'w', encoding='utf-8') as f:
        for line in src.iterdump():
            f.write(f'{line}\n')
    src.close()
    os.remove(STATE_DB)
    new = sqlite3.connect(STATE_DB)
    with open(STATE_DUMP, 'r', encoding='utf-8') as f:
        new.executescript(f.read())
    new.execute('PRAGMA wal_checkpoint(TRUNCATE);')
    new.close()
    print(f'    ✅ state 重建完成: {os.path.getsize(STATE_DB)/1e6:.1f} MB')

# 9. 删 dump 文件 (节省空间)
print(f'\n[9] 清理...')
for f in [DUMP, STATE_DUMP]:
    if os.path.exists(f):
        os.remove(f)
        print(f'    删 {os.path.basename(f)}')

# 10. gateway 应该自动重启 (schtasks)
print(f'\n[10] 等待 gateway 自动重启...')
time.sleep(5)
result = subprocess.run(['powershell', '-NoProfile', '-Command',
    '(Get-Process -Name node -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -match "openclaw.mjs gateway" }).Id'],
    capture_output=True, text=True)
final_pids = [int(p.strip()) for p in result.stdout.strip().split('\n') if p.strip().isdigit()]
print(f'    最终 PID: {final_pids}')

print(f'\n=== 重建完成 ===')
print(f'备份保留: {os.path.basename(BAK)}, {os.path.basename(STATE_BAK)}')