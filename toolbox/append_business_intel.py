# -*- coding: utf-8 -*-
"""Append 商业情报 section to memory/2026-07-27.md"""
import sys
from pathlib import Path

memory_file = Path(r"D:/B166ER-OpenClaw/workspace/memory/2026-07-27.md")
section_content = Path(r"C:/tmp/business-intel-2026-07-27.md").read_text(encoding="utf-8")

# Read existing content (preserve everything before)
existing = memory_file.read_text(encoding="utf-8")

# Build the section header
header = "\n\n---\n\n# § 商业情报 · 2026-07-27 (cron M/W/F 10:00)\n\n"
note = "> **来源**: B166ER cron `16c3811b-3fe5-49d0-be1a-0df19a86aef6` · 20集团版\n"
note += "> **生成时间**: 2026-07-27 10:34 GMT+8\n"
note += "> **完整报告**: `eval/2026-07-27.json` + `/tmp/business-intel-2026-07-27.md`\n"
note += "> **本session**: R258 DORMANT (非AnYi决策通道), 独立cron运行\n\n---\n\n"

# Append
new_content = existing + header + note + section_content

# Write back (utf-8, no BOM, atomic)
memory_file.write_text(new_content, encoding="utf-8")
print(f"✅ Appended 商业情报 section to {memory_file}")
print(f"   Original: {len(existing)} chars -> New: {len(new_content)} chars")
print(f"   Delta: +{len(new_content) - len(existing)} chars")