#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""外部内容纳入 vault: Part 2 - 简化版 + 错误处理"""
import sys, io, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")
EXTERNAL = VAULT / "50-外部接入"
EXTERNAL.mkdir(parents=True, exist_ok=True)


def safe_copy_dir(src: Path, dst: Path, label: str, max_files: int = 10000):
    if not src.exists():
        print(f"SKIP {label}: NOT EXIST", flush=True)
        return 0
    dst.mkdir(parents=True, exist_ok=True)
    count = 0
    skipped = 0
    for f in src.rglob("*"):
        if f.is_file():
            if '.obsidian' in f.parts:
                skipped += 1
                continue
            try:
                if f.stat().st_size > 50 * 1024 * 1024:
                    skipped += 1
                    continue
            except Exception:
                pass
            rel = f.relative_to(src)
            target = dst / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            try:
                shutil.copy2(f, target)
                count += 1
            except Exception as e:
                print(f"ERR {f.name}: {e}", flush=True)
            if count >= max_files:
                break
    print(f"OK {label}: copied {count} (skipped {skipped})", flush=True)
    return count


print("START", flush=True)

# 1. 安逸集团入职物料
print("\n[1] 安逸入职物料", flush=True)
safe_copy_dir(
    Path(r"C:\Users\ericz\Desktop\安逸集团_入职物料_20260707"),
    EXTERNAL / "01-安逸入职物料-20260707",
    "anyi", max_files=50)

# 2. Eric 自己的 Obsidian
print("\n[2] Eric Obsidian", flush=True)
safe_copy_dir(
    Path(r"C:\Users\ericz\Documents\Obsidian Vault"),
    EXTERNAL / "02-Eric-Obsidian-Vault",
    "eric_obs", max_files=200)

# 3. 维景 SOP
print("\n[3] 维景 SOP&PP", flush=True)
safe_copy_dir(
    Path(r"D:\酒店相关SOP"),
    EXTERNAL / "03-维景SOP-PP-2024",
    "weijing", max_files=5000)

print("\nDONE", flush=True)
