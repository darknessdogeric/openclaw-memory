#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""全面对账: vault 现有内容 vs workspace 全部源文件"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path

VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")
WORKSPACE = Path(r"D:\B166ER-OpenClaw\workspace")

# 1. 列出 vault 全部 .md
vault_md = {f.relative_to(VAULT).as_posix() for f in VAULT.rglob("*.md")}
print(f"=" * 60)
print(f"VAULT 当前 .md 数量: {len(vault_md)}")
print(f"=" * 60)

# 2. 列出 workspace 全部 .md (排除 vault 自身 + node_modules + .git + .backups + .openclaw)
EXCLUDE_DIRS = ['.git', 'node_modules', '.backups', '.openclaw', 'obsidian-vault',
                '.agents', '.clawhub', '.iflow', '.last30days-skill', '.openclaw',
                '.playwright-cli', '.self-improving', '.tmp']

def should_skip(path: Path) -> bool:
    rel = path.relative_to(WORKSPACE)
    for ex in EXCLUDE_DIRS:
        if ex in rel.parts:
            return True
    return False

ws_md = []
for f in WORKSPACE.rglob("*.md"):
    if not should_skip(f):
        rel = f.relative_to(WORKSPACE).as_posix()
        ws_md.append((rel, f.stat().st_size))

print(f"\nWORKSPACE 全部 .md (排除隐藏目录): {len(ws_md)}")
print()

# 3. workspace 根目录核心文件
print("=" * 60)
print("WORKSPACE 根目录核心文件")
print("=" * 60)
for f in sorted(WORKSPACE.glob("*.md")):
    if f.is_file():
        print(f"  {f.name} ({f.stat().st_size}b)")

# 4. memory/ 全部
print("\n" + "=" * 60)
print("memory/ 全部 .md")
print("=" * 60)
mem_files = sorted((WORKSPACE / "memory").glob("*.md"))
for f in mem_files:
    print(f"  memory/{f.name} ({f.stat().st_size}b)")
print(f"  Total memory: {len(mem_files)}")

# 5. reports/ 全部
print("\n" + "=" * 60)
print("reports/ 全部 .md")
print("=" * 60)
rep_files = sorted((WORKSPACE / "reports").glob("*.md"))
for f in rep_files:
    print(f"  reports/{f.name} ({f.stat().st_size}b)")
print(f"  Total reports: {len(rep_files)}")

# 6. docs/ 全部
print("\n" + "=" * 60)
print("docs/ 全部 .md (如有)")
print("=" * 60)
docs = sorted((WORKSPACE / "docs").glob("*.md")) if (WORKSPACE / "docs").exists() else []
for f in docs:
    print(f"  docs/{f.name} ({f.stat().st_size}b)")
print(f"  Total docs: {len(docs)}")

# 7. 找哪些 workspace 文件没在 vault 里
print("\n" + "=" * 60)
print("GAP 分析: workspace 中但 vault 缺的")
print("=" * 60)

# vault 里所有 .md 名字（去前缀）
vault_names = {f.name for f in VAULT.rglob("*.md")}

missing = []
for rel, size in ws_md:
    fname = Path(rel).name
    if fname not in vault_names:
        missing.append((rel, size))

print(f"  Missing 数量: {len(missing)}")
for rel, size in missing[:30]:
    print(f"  ❌ {rel} ({size}b)")
if len(missing) > 30:
    print(f"  ... 还有 {len(missing) - 30} 个")
