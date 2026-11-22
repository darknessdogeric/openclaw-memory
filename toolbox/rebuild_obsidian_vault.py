#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
保守恢复 obsidian-vault (方案 1)
- 严格 R13: 先打印动作清单，再执行删除
- 严格 R14: vault 操作前先 Test-Path 验证
"""
import os
import shutil
from pathlib import Path

VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")
WORKSPACE = Path(r"D:\B166ER-OpenClaw\workspace")

print("=" * 60)
print("Phase 0: 验证目标路径")
print("=" * 60)
print(f"  vault: {VAULT}")
print(f"  exists: {VAULT.exists()} (期望: False)")
if VAULT.exists():
    print("  ABORT: vault 已存在！")
    exit(1)

# ====== 骨架结构 ======
FOLDERS = [
    "00-Inbox-待整理",
    "00-Inbox-待整理/cron-push",
    "01-日记",
    "10-我为你生成的",
    "10-我为你生成的/产品矩阵",
    "10-我为你生成的/知识库",
    "10-我为你生成的/系统与工具",
    "10-我为你生成的/人格与认知",
    "20-我们共同维护的",
    "20-我们共同维护的/战略与节奏",
    "20-我们共同维护的/项目矩阵",
    "20-我们共同维护的/报告",
    "20-我们共同维护的/知识库索引",
    "30-你写给我的",
    "40-工具与模板",
]

print("\n" + "=" * 60)
print("Phase 1: 创建骨架")
print("=" * 60)
for f in FOLDERS:
    p = VAULT / f
    p.mkdir(parents=True, exist_ok=True)
    print(f"  + {f}")

# .obsidian 配置
(VAULT / ".obsidian").mkdir(parents=True, exist_ok=True)
app_json = """{
  "vaultName": "B166ER & ERIC 双向思考库",
  "promptDelete": true,
  "alwaysUpdateLinks": true,
  "newLinkFormat": "shortest",
  "useMarkdownLinks": false,
  "newFileLocation": "current",
  "attachmentFolderPath": ".",
  "showLineNumber": true,
  "spellcheck": false,
  "showInlineTitle": true
}
"""
(VAULT / ".obsidian" / "app.json").write_text(app_json, encoding="utf-8")
print(f"  + .obsidian/app.json")

# ====== 同步 workspace 源文件 ======
def sync(src_rel, dst_rel, label=""):
    src = WORKSPACE / src_rel
    dst = VAULT / dst_rel
    if not src.exists():
        print(f"  MISS: {src_rel}")
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    print(f"  OK  {src.name} -> {dst_rel} ({dst.stat().st_size}b)  {label}")
    return True

print("\n" + "=" * 60)
print("Phase 2: 同步 workspace 源文件")
print("=" * 60)

# MEMORY + PROJECT-TRACKING
sync("MEMORY.md", "20-我们共同维护的/00-MEMORY.md", "核心")
sync("PROJECT-TRACKING.md", "20-我们共同维护的/项目矩阵/00-PROJECT-TRACKING.md", "项目矩阵")

# 7 月日记
print("\n  -- 7月日记 --")
for f in sorted((WORKSPACE / "memory").glob("2026-07-*.md")):
    sync(f"memory/{f.name}", f"01-日记/{f.name}")

# 4 个核心报告
print("\n  -- 报告 --")
for r in [
    "2026五一全国酒店市场复盘报告.md",
    "2026-05-12-五一复盘报告-T7.md",
    "2026-05-12-沙坪坝区五一酒店分析.md",
    "2026-Q1-中国酒店行业研究报告.md",
]:
    sync(f"reports/{r}", f"20-我们共同维护的/报告/{r}")

# 5 个核心 KB
print("\n  -- KB 索引 --")
for k in [
    "酒店政策法规知识库-V1.0.md",
    "酒店运营SOP知识库-V1.0.md",
    "酒店市场销售知识库-V1.0.md",
    "酒店项目定位-V1.0.md",
    "酒店项目案例知识库-V1.0.md",
]:
    sync(f"memory/{k}", f"20-我们共同维护的/知识库索引/{k}")

# 自我革命/人格侧写
print("\n  -- 人格/认知 --")
for f in (WORKSPACE / "memory").glob("*人格*.md"):
    sync(f"memory/{f.name}", f"10-我为你生成的/人格与认知/{f.name}")
for f in (WORKSPACE / "memory").glob("*自我革命*.md"):
    sync(f"memory/{f.name}", f"10-我为你生成的/人格与认知/{f.name}")

# ====== 验证 ======
print("\n" + "=" * 60)
print("Phase 3: 验证")
print("=" * 60)
md_files = list(VAULT.rglob("*.md"))
print(f"  总 .md 文件数: {len(md_files)}")

print("\n  目录结构:")
for d in sorted(VAULT.rglob("*")):
    if d.is_dir():
        rel = d.relative_to(VAULT)
        cnt = len(list(d.glob("*.md")))
        if cnt > 0 or rel == Path("."):
            print(f"    {rel}/  [{cnt} files]")

print("\n  详细文件:")
for f in sorted(md_files):
    rel = f.relative_to(VAULT)
    print(f"    {rel}  ({f.stat().st_size}b)")
