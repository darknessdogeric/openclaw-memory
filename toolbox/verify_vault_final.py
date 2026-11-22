#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""最终验证 vault 结构"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from collections import defaultdict

VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")
md = list(VAULT.rglob("*.md"))
g = defaultdict(lambda: {"files": 0, "size": 0})
for f in md:
    rel = f.relative_to(VAULT)
    d = "/".join(rel.parts[:-1]) if len(rel.parts) > 1 else "(root)"
    g[d]["files"] += 1
    g[d]["size"] += f.stat().st_size

print(f"VAULT 总 .md: {len(md)}")
total_size = sum(v["size"] for v in g.values())
print(f"总大小: {total_size/1024/1024:.1f}MB")
print()
for d in sorted(g.keys()):
    v = g[d]
    size_kb = v["size"]/1024
    print(f"[{v['files']:3d} files, {size_kb:7.1f}KB] {d}/")
