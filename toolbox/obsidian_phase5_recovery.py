#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""RECOVERY-LOG C 类丢失项核对"""
import sys
from pathlib import Path
sys.stdout.reconfigure(encoding='utf-8')

VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")

# C 类清单(从 RECOVERY-LOG.md 提取)
C_LOST = [
    ("20-我们共同维护的/知识库索引/00-知识库总览.md", "知识库总览"),
    ("20-我们共同维护的/知识库索引/01-核心知识库完整目录.md", "核心知识库完整目录"),
    ("10-我为你生成的/README.md", "我为你生成的 README"),
    ("10-我为你生成的/关于B166ER.md", "关于B166ER"),
    ("10-我为你生成的/我的能力图谱.md", "我的能力图谱"),
    ("10-我为你生成的/系统与工具/00-电脑与系统.md", "电脑与系统"),
    ("10-我为你生成的/系统与工具/01-工具与技能清单.md", "工具与技能清单"),
    ("10-我为你生成的/产品矩阵/00-产品总览.md", "产品总览"),
    ("10-我为你生成的/产品矩阵/供应链工程-¥99.md", "供应链工程-¥99"),
    ("10-我为你生成的/产品矩阵/酒店数据资产-¥99.md", "酒店数据资产-¥99"),
    ("10-我为你生成的/产品矩阵/收益管理-¥59.9.md", "收益管理-¥59.9"),
    ("10-我为你生成的/产品矩阵/境外客源-¥49.9.md", "境外客源-¥49.9"),
]

print("=== C 类丢失项核对 (2026-07-28) ===\n")
for rel, desc in C_LOST:
    p = VAULT / rel
    if p.exists():
        sz = p.stat().st_size
        print(f"  ✅ 已存在  [{sz:6d}B]  {desc}")
    else:
        # 检查相似名称
        parent = p.parent
        similar = []
        if parent.exists():
            for f in parent.iterdir():
                if f.is_file() and f.suffix == '.md':
                    if desc[:5] in f.name or f.name.startswith(rel.split('/')[-1][:5]):
                        similar.append(f.name)
        print(f"  ❌ 缺失    {desc}")
        if similar:
            print(f"        相似: {similar}")

# 看 30-你写给我的 目录现在有什么
print(f"\n=== 30-你写给我的 当前内容 ===")
d = VAULT / "30-你写给我的"
for p in sorted(d.rglob("*")):
    if p.is_file():
        print(f"  {p.relative_to(VAULT)}")
