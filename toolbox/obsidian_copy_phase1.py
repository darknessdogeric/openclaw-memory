#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 2: 桌面 -> vault 复制 (复制, 不是移动; 不删除桌面)
目标:
1. 在 vault\50-外部接入\桌面映射\ 建 README 索引
2. 复制张实项目总控 (.md) 到 vault\50-外部接入\张实项目总控\
3. 复制新媒体产品线 (.md) 到 vault\50-外部接入\新媒体产品线\
安全:
- 用 copy2 保留 mtime
- 显式路径
- 完成后立即验证 .md 数
"""
import sys, shutil
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

DESK = Path(r"C:\Users\ericz\Desktop")
VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")
MAP_DIR = VAULT / "00-Inbox-待整理" / "桌面映射"
MAP_DIR.mkdir(parents=True, exist_ok=True)

def count_md(p: Path):
    return sum(1 for _ in p.rglob("*.md")) if p.exists() else 0

def copy_md_files(src_dir: Path, dst_dir: Path, label: str):
    if not src_dir.exists():
        print(f"[跳过] {src_dir} 不存在")
        return
    if not dst_dir.exists():
        dst_dir.mkdir(parents=True, exist_ok=True)
    # 只复制 .md(避免把零散二进制文件带过来,二进制后期单独建索引)
    md_files = list(src_dir.rglob("*.md"))
    copied = 0
    skipped_existing = 0
    for m in md_files:
        # 相对路径, 保留目录结构
        rel = m.relative_to(src_dir)
        target = dst_dir / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            # 二次检查 md5
            import hashlib
            def md5f(p):
                h = hashlib.md5()
                try:
                    with p.open('rb') as f:
                        for c in iter(lambda: f.read(8192), b''): h.update(c)
                    return h.hexdigest()
                except: return None
            if md5f(m) == md5f(target):
                skipped_existing += 1
                continue
            # 不同 md5 -> 标记 source-desktop
            target = target.with_name(target.stem + " (source-desktop)" + target.suffix)
        shutil.copy2(str(m), str(target))
        copied += 1
    print(f"[{label}] src .md={len(md_files)}  copied={copied}  skipped_existing={skipped_existing}")
    print(f"        dst .md={count_md(dst_dir)}")

# 1. 张实项目总控
print("=== 复制: 张实项目总控 ===")
copy_md_files(DESK / "张实项目总控",
              VAULT / "50-外部接入" / "张实项目总控",
              "张实项目总控")

# 2. 新媒体产品线
print("\n=== 复制: 新媒体产品线 ===")
copy_md_files(DESK / "新媒体产品线",
              VAULT / "50-外部接入" / "新媒体产品线",
              "新媒体产品线")

# 3. 小红书产品线 (1 .md)
print("\n=== 复制: 小红书产品线 ===")
copy_md_files(DESK / "小红书产品线",
              VAULT / "50-外部接入" / "小红书产品线",
              "小红书产品线")

# 4. 自我革命 (1 .md)
print("\n=== 复制: 自我革命 ===")
copy_md_files(DESK / "自我革命",
              VAULT / "50-外部接入" / "自我革命",
              "自我革命")

print("\n=== 当前 vault 统计 ===")
total_md = sum(1 for _ in VAULT.rglob("*.md"))
total_files = sum(1 for _ in VAULT.rglob("*") if _.is_file())
print(f"Vault total .md: {total_md}")
print(f"Vault total files: {total_files}")
