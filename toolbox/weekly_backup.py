# -*- coding: utf-8 -*-
"""
B166ER 每周全量备份脚本
- 备份目标: D:\B166ER-Backup\weekly\{YYYY-MM-DD}\
- 备份内容: workspace + obsidian-vault
- 排除: node_modules, .git, __pycache__, cache, .backups 等大文件/临时文件
- 清理: 保留最近 8 周(约 60 天)的备份

用法:
    python weekly_backup.py             # 正常备份
    python weekly_backup.py --dry-run   # 仅显示计划,不执行
"""
import os
import shutil
import json
import subprocess
import sys
from datetime import datetime, timedelta

WORKSPACE = r'D:\B166ER-OpenClaw\workspace'
VAULT = r'D:\B166ER-OpenClaw\workspace\obsidian-vault'
DST_BASE = r'D:\B166ER-Backup\weekly'
TODAY = datetime.now().strftime('%Y-%m-%d')
DST_TODAY = os.path.join(DST_BASE, TODAY)
WS_DST = os.path.join(DST_TODAY, 'workspace')
VAULT_DST = os.path.join(DST_TODAY, 'obsidian-vault')

# 排除模式 (按目录名/文件名,不区分大小写)
EXCLUDE_DIRS = [
    'node_modules', '.git', '__pycache__', '.next', '.nuxt',
    'cache', '.cache', '.backups', '.openclaw-cache',
    'venv', '.venv', 'env', '.env', 'dist', 'build',
    'tmp', '.tmp', '.scratch', '.playwright-cli',
    'temp_extracted', 'temp_pdf_images', '.edge-screenshot',
    '.last30days-skill', 'output', 'outputs', 'media_preview',
    '.iflow', '.clawhub', 'log', 'logs',
    'ppt_output', 'temp_bp', 'tobox',  # 输出类
]
EXCLUDE_FILES = [
    '*.pyc', '*.log', '*.tmp', '*.swp', '*.bak',
    'Thumbs.db', '.DS_Store', '*.pid',
    'skills-lock.json',  # 锁文件,会冲突
]

# Robocopy exclusion flags (FIX R-eve-20260913: 加斜杠, 之前 XD 不识别 → 被当文件名过滤器)
EXCLUDE_DIR_FLAGS = ' '.join([f'/XD "{d}"' for d in EXCLUDE_DIRS])
EXCLUDE_FILE_FLAGS = '/XF ' + ' '.join(EXCLUDE_FILES)


def get_dir_size(path):
    """获取目录大小(字节)"""
    total = 0
    for dp, _, fn in os.walk(path):
        for f in fn:
            try:
                total += os.path.getsize(os.path.join(dp, f))
            except OSError:
                pass
    return total


def human_size(bytes_size):
    """人类可读大小"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f'{bytes_size:.2f} {unit}'
        bytes_size /= 1024.0
    return f'{bytes_size:.2f} PB'


def robocopy_copy(src, dst, label):
    """用 robocopy 复制目录,返回 (退出码, 输出)"""
    os.makedirs(dst, exist_ok=True)
    cmd = (
        f'robocopy "{src}" "{dst}" /E /COPY:DAT /R:3 /W:5 '
        f'/NFL /NDL /NJH /NJS /NP /BYTES /MT:8 '
        f'{EXCLUDE_DIR_FLAGS} {EXCLUDE_FILE_FLAGS}'
    )
    print(f'\n[→] {label}: 开始 robocopy ...')
    print(f'    src: {src}')
    print(f'    dst: {dst}')
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    # robocopy 退出码: 0=无变化, 1=复制成功, 2=有额外文件, 3=复制+额外
    # >=8 才算错误
    if proc.returncode >= 8:
        print(f'[✗] {label}: robocopy 失败 (exit={proc.returncode})')
        print(proc.stdout[-2000:])
        print(proc.stderr[-1000:])
        return False, proc.stdout, proc.stderr
    else:
        print(f'[✓] {label}: robocopy 成功 (exit={proc.returncode})')
        return True, proc.stdout, proc.stderr


def cleanup_old_backups():
    """清理 8 周(56 天)前的备份"""
    cutoff = datetime.now() - timedelta(days=56)
    cutoff_str = cutoff.strftime('%Y-%m-%d')
    removed = []
    if not os.path.isdir(DST_BASE):
        return removed
    for d in os.listdir(DST_BASE):
        if len(d) == 10 and d.startswith('20') and d < cutoff_str:
            p = os.path.join(DST_BASE, d)
            try:
                if os.path.islink(p):
                    os.unlink(p)
                elif os.path.isdir(p):
                    shutil.rmtree(p)
                removed.append(d)
                print(f'[CLEAN] 删除旧备份: {d}')
            except Exception as e:
                print(f'[CLEAN FAIL] {d}: {e}')
    return removed


def backup():
    dry_run = '--dry-run' in sys.argv
    started = datetime.now()

    print(f'================ 周全量备份 · {TODAY} ================')
    print(f'Started:  {started.strftime("%Y-%m-%d %H:%M:%S")}')
    print(f'Workspace: {WORKSPACE}')
    print(f'Vault:     {VAULT}')
    print(f'Destination: {DST_TODAY}')
    print()

    if dry_run:
        print('[DRY-RUN] 仅显示计划,不做实际复制')
        ws_size = get_dir_size(WORKSPACE)
        vault_size = get_dir_size(VAULT) if os.path.isdir(VAULT) else 0
        print(f'  workspace size: {human_size(ws_size)}')
        print(f'  vault size:     {human_size(vault_size)}')
        print(f'  estimated total: {human_size(ws_size + vault_size)}')
        return

    # 1. 创建目标目录
    os.makedirs(DST_TODAY, exist_ok=True)

    # 2. 备份 workspace (排除大目录)
    results = {}
    ok, so, se = robocopy_copy(WORKSPACE, WS_DST, 'workspace')
    results['workspace'] = {'ok': ok}

    # 3. 备份 vault (完整备份,无排除)
    if os.path.isdir(VAULT):
        ok2, so2, se2 = robocopy_copy(VAULT, VAULT_DST, 'obsidian-vault')
        results['vault'] = {'ok': ok2}

    # 4. 计算备份大小
    print('\n[→] 计算备份大小 ...')
    ws_backup_size = get_dir_size(WS_DST)
    vault_backup_size = get_dir_size(VAULT_DST) if os.path.isdir(VAULT_DST) else 0
    total_size = ws_backup_size + vault_backup_size

    print(f'  workspace 备份: {human_size(ws_backup_size)}')
    print(f'  vault 备份:     {human_size(vault_backup_size)}')
    print(f'  总计:           {human_size(total_size)}')

    # 5. 清理旧备份
    print('\n[→] 清理 56 天前的旧备份 ...')
    removed = cleanup_old_backups()

    # 6. 写一份备份日志
    finished = datetime.now()
    elapsed = (finished - started).total_seconds()
    log = {
        'date': TODAY,
        'started': started.isoformat(),
        'finished': finished.isoformat(),
        'elapsed_seconds': round(elapsed, 1),
        'workspace': {
            'src_size': human_size(get_dir_size(WORKSPACE)),
            'backup_size': human_size(ws_backup_size),
            'ok': results.get('workspace', {}).get('ok', False),
        },
        'vault': {
            'src_size': human_size(get_dir_size(VAULT)) if os.path.isdir(VAULT) else 'N/A',
            'backup_size': human_size(vault_backup_size),
            'ok': results.get('vault', {}).get('ok', False),
        },
        'total_backup_size_bytes': total_size,
        'total_backup_size_human': human_size(total_size),
        'removed_old': removed,
        'excluded_dirs': EXCLUDE_DIRS,
    }
    log_path = os.path.join(DST_TODAY, 'BACKUP_LOG.json')
    with open(log_path, 'w', encoding='utf-8') as f:
        json.dump(log, f, ensure_ascii=False, indent=2)
    print(f'\n[LOG] {log_path}')

    print()
    print(f'================ 备份完成 ================')
    print(f'总计: {human_size(total_size)} ({elapsed:.0f}s)')
    return log


if __name__ == '__main__':
    backup()
