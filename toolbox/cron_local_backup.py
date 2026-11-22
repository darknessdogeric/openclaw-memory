#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cron_local_backup.py - 本地备份 + Obsidian 推送
Eric 2026-09-08 15:14 决策：替换 agentTurn 备份任务
被 heartbeat-main 改用 shell 直接调用此脚本
"""
import os
import sys
import shutil
import json
from datetime import datetime, timezone, timedelta

WS = r'D:\B166ER-OpenClaw\workspace'
BACKUP_ROOT = r'D:\B166ER-Backup'
CRON_TO_OBSIDIAN = r'D:\B166ER-OpenClaw\workspace\toolbox\cron_to_obsidian.py'
TZ = timezone(timedelta(hours=8))

def fmt_size(n):
    if n > 1024**3:
        return f'{n/1024**3:.2f} GB'
    if n > 1024**2:
        return f'{n/1024**2:.2f} MB'
    if n > 1024:
        return f'{n/1024:.2f} KB'
    return f'{n} B'

def main():
    today = datetime.now(TZ).strftime('%Y%m%d_%H%M%S')
    date_dir = datetime.now(TZ).strftime('%Y-%m-%d')
    backup_dir = os.path.join(BACKUP_ROOT, date_dir)
    os.makedirs(backup_dir, exist_ok=True)

    log_lines = [f'# B166ER 本地备份 {today}\n']
    log_lines.append(f'\n## 1. 备份目录: `{backup_dir}`\n')
    total_size = 0
    file_count = 0

    # 备份核心目录
    targets = [
        ('memory', os.path.join(WS, 'memory')),
        ('anyi-ops-kb', os.path.join(WS, 'anyi-ops-kb')),
        ('toolbox/.tmp', os.path.join(WS, 'toolbox', '.tmp')),
        ('AGENTS.md', os.path.join(WS, 'AGENTS.md')),
        ('SOUL.md', os.path.join(WS, 'SOUL.md')),
        ('IDENTITY.md', os.path.join(WS, 'IDENTITY.md')),
        ('USER.md', os.path.join(WS, 'USER.md')),
        ('MEMORY.md', os.path.join(WS, 'MEMORY.md')),
    ]
    for name, src in targets:
        if not os.path.exists(src):
            log_lines.append(f'\n### {name}\n- ❌ 源不存在: `{src}`\n')
            continue
        dst = os.path.join(backup_dir, name)
        try:
            if os.path.isdir(src):
                if os.path.exists(dst):
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
                size = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(dst) for f in fs)
                log_lines.append(f'\n### {name}\n- ✅ 备份 {fmt_size(size)} ({sum(len(fs) for r,_,fs in os.walk(src))} 文件)\n')
                total_size += size
                file_count += sum(len(fs) for r,_,fs in os.walk(src))
            else:
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
                size = os.path.getsize(dst)
                log_lines.append(f'\n### {name}\n- ✅ {fmt_size(size)}\n')
                total_size += size
                file_count += 1
        except Exception as e:
            log_lines.append(f'\n### {name}\n- ❌ 备份失败: {e}\n')

    log_lines.append(f'\n## 2. 备份汇总\n- 总文件: {file_count}\n- 总大小: **{fmt_size(total_size)}**\n- 备份目录: `{backup_dir}`\n')

    # 写备份日志
    log_path = os.path.join(backup_dir, '_backup_log.md')
    with open(log_path, 'w', encoding='utf-8') as f:
        f.writelines(log_lines)
    print(f'[OK] 本地备份完成: {backup_dir} ({fmt_size(total_size)})')

    # 调 cron_to_obsidian.py 推送
    try:
        result = subprocess.run(
            ['python', CRON_TO_OBSIDIAN,
             '--task', '本地备份 02:00 推送',
             '--content-file', log_path,
             '--importance', 'low',
             '--summary', f'本地备份完成 - {file_count} 文件 / {fmt_size(total_size)}',
             '--append-daily'],
            capture_output=True, text=True, timeout=60,
            cwd=r'C:\Users\ericz\.openclaw\state'
        )
        if result.returncode == 0:
            print('[OK] Obsidian 推送成功')
        else:
            print(f'[WARN] Obsidian 推送返回 {result.returncode}: {result.stderr[:200]}')
    except Exception as e:
        print(f'[ERR] Obsidian 推送失败: {e}')

    return 0

if __name__ == '__main__':
    sys.exit(main())
