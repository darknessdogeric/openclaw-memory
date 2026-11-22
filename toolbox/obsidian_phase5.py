#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase 5a: 处理空的 C:\\Users\\ericz\\Documents\\Obsidian Vault\\
策略: 备份到 main vault 后, 删除空 vault 整个目录
"""
import sys, shutil
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

EMPTY_VAULT = Path(r"C:\Users\ericz\Documents\Obsidian Vault")
MAIN_VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")

# 1) 看空 vault 有什么
print(f"=== {EMPTY_VAULT} 内容 ===")
if EMPTY_VAULT.exists():
    for p in EMPTY_VAULT.rglob("*"):
        if p.is_file():
            print(f"  FILE  {p.relative_to(EMPTY_VAULT)} ({p.stat().st_size}B)")
        else:
            print(f"  DIR   {p.relative_to(EMPTY_VAULT)}")
else:
    print("  (不存在)")

# 2) Dry-run: 移到 main vault 的 备份目录
backup_dir = MAIN_VAULT / "00-Inbox-待整理" / "_archived-Obsidian-Vault"
print(f"\n计划: 备份到 {backup_dir}")

# 不实际执行(交给主流程决定) - 标记在交付报告里给 Eric 看
print("\n  (需要 Eric 显式确认才能删除 - 这里只做信息汇总)")

# 删/留决策: 把"是否删除"留给 Eric 看
# 默认推荐: 删 (减少混淆)
