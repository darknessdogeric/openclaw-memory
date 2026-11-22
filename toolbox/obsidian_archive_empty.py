#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase 5: 归档空 vault + 重建索引"""
import sys, shutil
from pathlib import Path
import subprocess
sys.stdout.reconfigure(encoding='utf-8')

EMPTY_VAULT = Path(r"C:\Users\ericz\Documents\Obsidian Vault")
MAIN_VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")
ARCHIVE = MAIN_VAULT / "00-Inbox-待整理" / "_archived-Obsidian-Vault"

# 1) 移动 (shutil.move) 整个空 vault 到 main vault 内归档
if EMPTY_VAULT.exists():
    # 如果目标位置已存在, 加时间戳
    target = ARCHIVE
    i = 1
    while target.exists():
        target = ARCHIVE.with_name(f"_archived-Obsidian-Vault-{i}")
        i += 1
    target.mkdir(parents=True, exist_ok=True)
    # 逐个搬(避免长路径问题)
    for p in EMPTY_VAULT.iterdir():
        dest = target / p.name
        if p.is_dir():
            shutil.copytree(str(p), str(dest))
        else:
            shutil.copy2(str(p), str(dest))
    print(f"[归档] 副本 -> {target}")
    # 原位置保留(用 Obsidian 友好的标记)
    marker = EMPTY_VAULT / "_ARCHIVED-2026-07-28.txt"
    marker.write_text(
        f"此 Vault 已被 B166ER 归档到:\n{target}\n\n"
        f"原内容 (5 文件):\n- 欢迎.md\n- .obsidian/\n\n"
        f"主 Vault 现在是:\n{MAIN_VAULT}\n",
        encoding="utf-8"
    )
    print(f"[标记] {marker}")
else:
    print("[跳过] 空 vault 不存在")
