#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查未匹配的文件"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
import re

VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")
TODAY_DIRS = ["张实项目总控", "新媒体产品线", "小红书产品线",
              "AHL源代码-docs", "AHL专利-原始申请", "AHL专利-技术材料",
              "AHL专利-补正", "AHL软著申请", "知局-v1.0", "自我革命"]

KEYWORDS = set()
for klist, _, _ in [
    (["AHL", "去中心化", "AI酒店", "AI单体"], "x", 1),
    (["酒店", "OTA", "SOP"], "x", 1),
    (["Agent", "LLM", "大模型"], "x", 1),
    (["安逸", "十五五"], "x", 1),
    (["战略", "方法论"], "x", 1),
    (["审美", "音乐"], "x", 1),
    (["工具", "Python"], "x", 1),
    (["跨境", "出海", "Booking"], "x", 1),
    (["B166ER"], "x", 1),
]:
    for k in klist:
        KEYWORDS.add(k.lower())

errors = []
nokey = []
for d in TODAY_DIRS:
    dp = VAULT / "50-外部接入" / d
    if not dp.exists(): continue
    for f in dp.rglob("*.md"):
        try:
            text = f.read_text(encoding='utf-8')
        except Exception as e:
            errors.append((f.relative_to(VAULT), str(e)[:50]))
            continue
        # 去掉 frontmatter
        body = re.sub(r'^---\n.*?\n---\n', '', text, count=1, flags=re.S)
        preview = body[:500].lower()
        matched = any(k in preview for k in KEYWORDS)
        if not matched:
            nokey.append((f.relative_to(VAULT), text[:200]))

print("=== READ_ERROR ===")
for f, e in errors:
    print(f"  {f}: {e}")

print(f"\n=== NO_KEYWORDS ({len(nokey)}) ===")
for f, preview in nokey:
    print(f"\n  {f}")
    print(f"    {preview[:150].replace(chr(10), ' ')}")