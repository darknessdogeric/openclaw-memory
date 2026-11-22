# -*- coding: utf-8 -*-
"""
B166ER 每日本地备份 - 2026-08-22 (cron 02:00)
- 备份目标: C:\B166ER-Backup\2026-08-22\
- 备份策略: 与 8/21 一致（12 关键文件 + 5 目录）
- 清理: 14 天前的旧备份 (2026-08-08 之前)
"""
import os, shutil, json
from datetime import datetime, timedelta

src = r'D:\B166ER-OpenClaw\workspace'
dst = r'C:\B166ER-Backup\2026-08-22'
today = '2026-08-22'

key_files = [
    'SOUL.md', 'IDENTITY.md', 'USER.md', 'AGENTS.md', 'TOOLS.md', 'MEMORY.md',
    'HEARTBEAT.md', 'DREAMS.md', 'PROJECT-TRACKING.md',
    'B166ER-STYLE.md', 'B166ER-底层理论架构-V2.2.md',
    'AHL-电梯演讲-一页纸.md',
]

key_dirs = [
    'memory', 'toolbox', 'skills', 'obsidian-vault', 'self-improving',
]

os.makedirs(dst, exist_ok=True)
copied_files = []
copied_dirs = []
total_size = 0
skipped = []

# 备份关键文件
for item in key_files:
    sp = os.path.join(src, item)
    dp = os.path.join(dst, item)
    if not os.path.exists(sp):
        skipped.append(f'{item} (missing)')
        continue
    try:
        d = os.path.dirname(dp)
        if d:
            os.makedirs(d, exist_ok=True)
        shutil.copy2(sp, dp)
        size = os.path.getsize(dp)
        copied_files.append({'name': item, 'size_kb': round(size/1024, 1)})
        total_size += size
    except Exception as e:
        skipped.append(f'{item} (error: {e})')

# 备份关键目录
for item in key_dirs:
    sp = os.path.join(src, item)
    dp = os.path.join(dst, item)
    if not os.path.exists(sp):
        skipped.append(f'{item}/ (missing)')
        continue
    try:
        if os.path.exists(dp):
            shutil.rmtree(dp)
        shutil.copytree(sp, dp)
        size = sum(os.path.getsize(os.path.join(d, f)) for d, _, fn in os.walk(dp) for f in fn)
        copied_dirs.append({'name': item, 'size_mb': round(size/1024/1024, 2)})
        total_size += size
    except Exception as e:
        skipped.append(f'{item}/ (error: {e})')

# 计数
mem_count = 0
mem_dir = os.path.join(dst, 'memory')
if os.path.isdir(mem_dir):
    for _, _, fn in os.walk(mem_dir):
        mem_count += len([f for f in fn if f.endswith('.md')])

total_files = 0
for _, _, fn in os.walk(dst):
    total_files += len(fn)

# 清理 14 天前的旧备份
cutoff_date = (datetime.now() - timedelta(days=14)).strftime('%Y-%m-%d')
removed = []
for d in os.listdir(r'C:\B166ER-Backup'):
    full = os.path.join(r'C:\B166ER-Backup', d)
    if not os.path.isdir(full):
        continue
    # 匹配 YYYY-MM-DD 格式目录（与历史命名一致）
    if len(d) == 10 and d.startswith('20') and d[:4].isdigit() and d < cutoff_date:
        try:
            shutil.rmtree(full)
            removed.append(d)
        except Exception as e:
            print(f'[CLEAN FAIL] {d}: {e}')

result = {
    'date': today,
    'destination': dst,
    'copied_files': copied_files,
    'copied_dirs': copied_dirs,
    'copied_count': len(copied_files) + len(copied_dirs),
    'skipped': skipped,
    'total_bytes': total_size,
    'total_mb': round(total_size / 1024 / 1024, 2),
    'memory_md_files': mem_count,
    'total_files': total_files,
    'removed_old': removed,
}
print(json.dumps(result, ensure_ascii=False, indent=2))

# 写备份日志
log_path = os.path.join(dst, 'BACKUP_LOG.json')
with open(log_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
print(f'\n[LOG] {log_path}')

# 写 manifest
manifest_path = os.path.join(dst, 'backup-manifest.md')
with open(manifest_path, 'w', encoding='utf-8') as f:
    f.write(f'---\nB166ER Daily Local Backup (v2)\n')
    f.write(f'Date: {today}\n')
    f.write(f'Source: {src}\n')
    f.write(f'Destination: {dst}\n')
    f.write(f'---\n\n')
    f.write(f'## Root Files ({len(copied_files)})\n')
    for cf in copied_files:
        f.write(f'  [FILE] {cf["name"]} ({cf["size_kb"]} KB)\n')
    f.write(f'\n## Directories ({len(copied_dirs)})\n')
    for cd in copied_dirs:
        f.write(f'  [DIR] {cd["name"]} ({cd["size_mb"]} MB)\n')
    f.write(f'\n---\n')
    f.write(f'Total: {result["total_mb"]} MB\n')
    f.write(f'Total Files: {total_files}\n')
    f.write(f'memory .md files: {mem_count}\n')
    f.write(f'Errors: {len([s for s in skipped if "error" in s])}\n')
    if removed:
        f.write(f'\nCleaned old backups (>14 days): {removed}\n')
    f.write(f'---\n')
print(f'[MANIFEST] {manifest_path}')
