# -*- coding: utf-8 -*-
"""
B166ER 每日本地备份 - 2026-08-20 (cron 02:00)
- 备份目标: C:\B166ER-Backup\B166ER-workspace-backup-2026-08-20\
- 备份策略: 关键文件 (避开 11.5 GB 全量)
- 清理: 14 天前的旧备份
"""
import os, shutil, json
from datetime import datetime, timedelta

src = r'D:\B166ER-OpenClaw\workspace'
dst = r'C:\B166ER-Backup\B166ER-workspace-backup-2026-08-20'
today = '2026-08-20'

# 关键文件 (与历史 daily_backup.py 一致)
key_items = [
    'SOUL.md', 'IDENTITY.md', 'USER.md', 'AGENTS.md', 'TOOLS.md', 'MEMORY.md',
    'HEARTBEAT.md', 'BACKUP_README.md', 'WORK.md', 'WORKFLOW.md',
    'DREAMS.md', 'PROJECT-TRACKING.md',
    'B166ER-STYLE.md', 'B166ER-底层理论架构-V2.2.md',
    'AHL-电梯演讲-一页纸.md', '商业计划书_新华酒店管理公司_AHL赋能版.md',
    'memory', 'toolbox', 'skills'
]

# 直接复制到命名目录下
os.makedirs(dst, exist_ok=True)
copied = []
total_size = 0
skipped = []

for item in key_items:
    sp = os.path.join(src, item)
    dp = os.path.join(dst, item)
    if not os.path.exists(sp):
        skipped.append(item)
        continue
    try:
        if os.path.isdir(sp):
            if os.path.exists(dp):
                shutil.rmtree(dp)
            shutil.copytree(sp, dp)
            size = sum(os.path.getsize(os.path.join(d, f)) for d, _, fn in os.walk(dp) for f in fn)
        else:
            d = os.path.dirname(dp)
            if d:
                os.makedirs(d, exist_ok=True)
            shutil.copy2(sp, dp)
            size = os.path.getsize(sp)
        copied.append(item)
        total_size += size
    except Exception as e:
        print(f'[FAIL] {item}: {e}')
        skipped.append(f'{item} (error: {e})')

# 清理 14 天前的旧备份 (2026-08-06 之前)
cutoff = '2026-08-06'
removed = []
for d in os.listdir(r'C:\B166ER-Backup'):
    full = os.path.join(r'C:\B166ER-Backup', d)
    if os.path.isdir(full) and d.startswith('B166ER-workspace-backup-') and d < f'B166ER-workspace-backup-{cutoff}':
        try:
            shutil.rmtree(full)
            removed.append(d)
        except Exception as e:
            print(f'[CLEAN FAIL] {d}: {e}')

# 计数
mem_count = 0
mem_dir = os.path.join(dst, 'memory')
if os.path.isdir(mem_dir):
    for _, _, fn in os.walk(mem_dir):
        mem_count += len(fn)

result = {
    'date': today,
    'destination': dst,
    'copied_count': len(copied),
    'skipped': skipped,
    'total_bytes': total_size,
    'total_mb': round(total_size / 1024 / 1024, 2),
    'memory_files': mem_count,
    'removed_old': removed,
    'items': copied,
}
print(json.dumps(result, ensure_ascii=False, indent=2))

# 写点备份日志到目标目录
log_path = os.path.join(dst, 'BACKUP_LOG.json')
with open(log_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(f'\n[LOG] {log_path}')