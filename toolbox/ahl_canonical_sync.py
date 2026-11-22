#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ahl_canonical_sync.py — AHL canonical sync (vault → workspace) with .bak safety net

执行 4 步:
1. 备份 18 个 workspace AHL 文件到 .bak/2026-07-22-AHL-canonical-sync/
2. vault (canonical) → workspace 覆盖
3. MD5 校验
4. 工作根去重回归测试

Eric 2026-07-22 12:38 授权。后悔药保留 3 天 (至 7/25) 自动清理。
"""
import shutil
import hashlib
from pathlib import Path
from datetime import datetime, timedelta

WS = Path(r'D:\B166ER-OpenClaw\workspace')
BAK_DIR = WS / '.bak' / '2026-07-22-AHL-canonical-sync'

AHL_FILES = [
    'AHL-4层架构图.md',
    'AHL-Agent-Skill完整说明书.md',
    'AHL-Agent-Skill技术团队完整说明书.md',
    'AHL-Archive-System.md',
    'AHL-Product-Catalog.md',
    'AHL-数据库关联配置.md',
    'AHL-电梯演讲-一页纸.md',
    'AHL组织架构演进方案.md',
    'AHL试点-岗位问题采集问卷集.md',
    'AHL试点培训材料-全体员工版.md',
    'AHL试点培训材料-内部使用.md',
    'API申请指南.md',
    'B166ER-爬虫能力提升方案.md',
    'ahl-marketing-agent-architecture-v2.md',
    'ahl-marketing-agent-architecture-v3.md',
    'ahl-marketing-member-agent-architecture-v1.md',
    'b-agent-revenue-management-SKILL-v2.md',
    'b-agent-revenue-management-SKILL.md',
]

def md5(p):
    return hashlib.md5(Path(p).read_bytes()).hexdigest()

def main():
    BAK_DIR.mkdir(parents=True, exist_ok=True)

    # Step 1: 备份
    print('[STEP 1] 备份 workspace 18 个文件到 .bak/')
    backed = 0
    for fname in AHL_FILES:
        src = WS / fname
        dst = BAK_DIR / fname
        if src.exists():
            shutil.copy2(src, dst)
            backed += 1
    print(f'  [OK] backed up: {backed}/18 files')
    print(f'  后悔药位置: {BAK_DIR}')

    # Step 2: vault → workspace 覆盖
    print()
    print('[STEP 2] vault (canonical) → workspace 覆盖')
    covered = 0
    for fname in AHL_FILES:
        ws_file = WS / fname
        vault_paths = list((WS / 'obsidian-vault').rglob(fname))
        if not vault_paths:
            print(f'  [WARN] vault no copy: {fname}')
            continue
        vault_file = vault_paths[0]
        shutil.copy2(vault_file, ws_file)
        covered += 1
    print(f'  [OK] 覆盖 {covered}/18 文件')

    # Step 3: MD5 校验
    print()
    print('[STEP 3] MD5 校验 (workspace vs vault)')
    all_match = True
    mismatches = []
    for fname in AHL_FILES:
        ws_file = WS / fname
        vault_paths = list((WS / 'obsidian-vault').rglob(fname))
        if not vault_paths:
            continue
        vault_file = vault_paths[0]
        match = md5(ws_file) == md5(vault_file)
        status = 'MATCH   ' if match else 'MISMATCH'
        print(f'  [{status}] {fname}')
        if not match:
            all_match = False
            mismatches.append(fname)

    # Step 4: 工作根状态回归
    print()
    print('[STEP 4] 工作根回归')
    remaining = []
    for fname in AHL_FILES:
        if (WS / fname).exists():
            remaining.append(fname)
    print(f'  workspace 根仍存在的 AHL 文件: {len(remaining)}/18')

    # 总结
    print()
    print('=' * 60)
    if all_match and len(remaining) == 18:
        print('[OK] 同步成功')
    else:
        print('[WARN] 异常，需人工复核')
        if mismatches:
            print(f'  MD5 不一致: {mismatches}')
    print('=' * 60)
    print(f'后悔药保留至: 2026-07-25')
    print(f'届时无异议 → 我会自动清理 .bak/')
    print(f'发现 vault 漏内容 → 告诉我，我从 .bak/ 恢复')

if __name__ == '__main__':
    main()