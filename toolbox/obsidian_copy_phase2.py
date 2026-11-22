#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phase 2: AHL源代码 + 专利系列 + 软著 + 入职物料 + 知局"""
import sys, shutil, hashlib
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

DESK = Path(r"C:\Users\ericz\Desktop")
VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")

def md5f(p):
    h = hashlib.md5()
    try:
        with p.open('rb') as f:
            for c in iter(lambda: f.read(8192), b''): h.update(c)
        return h.hexdigest()
    except: return None

def count_md(p: Path):
    return sum(1 for _ in p.rglob("*.md")) if p.exists() else 0

def copy_md(src: Path, dst: Path, label: str):
    if not src.exists():
        print(f"[跳过] {src.name} 不存在"); return
    if not dst.exists(): dst.mkdir(parents=True, exist_ok=True)
    md_files = list(src.rglob("*.md"))
    copied = same = renamed = 0
    for m in md_files:
        rel = m.relative_to(src)
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            if md5f(m) == md5f(target):
                same += 1
                continue
            target = target.with_name(target.stem + " (source-desktop)" + target.suffix)
            renamed += 1
        shutil.copy2(str(m), str(target))
        copied += 1
    print(f"[{label}] src={len(md_files)} copied={copied} same={same} renamed={renamed} dst_total={count_md(dst)}")

print("=== Phase 2: AHL 源代码 (.md) + 专利系列 + 安逸入职 + 知局 + 软著 ===\n")

# AHL 源代码: 只复制 .md, 不复制代码文件
copy_md(DESK / "AHL源代码", VAULT / "50-外部接入" / "AHL源代码-docs", "AHL源代码-docs")

# 专利 (docx/pdf/png 一堆, 只复制 .md 文档,二进制定向索引)
copy_md(DESK / "专利", VAULT / "50-外部接入" / "AHL专利-原始申请", "AHL专利-原始申请")

copy_md(DESK / "AHL专利申请文件", VAULT / "50-外部接入" / "AHL专利-技术材料", "AHL专利-技术材料")

copy_md(DESK / "专利补正", VAULT / "50-外部接入" / "AHL专利-补正", "AHL专利-补正")

copy_md(DESK / "软著申请材料-AHL", VAULT / "50-外部接入" / "AHL软著申请", "AHL软著申请")

# 安逸集团入职物料 - vault 已有同名目录
copy_md(DESK / "安逸集团_入职物料_20260707",
        VAULT / "50-外部接入" / "01-安逸入职物料-20260707",
        "安逸入职物料 (目标 vault 已存在)")

# 知局 (完整版 v1.0)
copy_md(DESK / "知局_完整版_v1.0", VAULT / "50-外部接入" / "知局-v1.0", "知局-v1.0")

print("\n=== 当前 vault 统计 ===")
total_md = sum(1 for _ in VAULT.rglob("*.md"))
total_files = sum(1 for _ in VAULT.rglob("*") if _.is_file())
print(f"Vault total .md: {total_md}")
print(f"Vault total files: {total_files}")
