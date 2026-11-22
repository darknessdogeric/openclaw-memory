#!/usr/bin/env python3
"""去重周报数据"""
import re

with open(r"D:\B166ER-OpenClaw\workspace\toolbox\weekly_reports_raw.txt", encoding="utf-8") as f:
    text = f.read()

# Split by file marker
sections = re.split(r"={40,}\n### FILE: ", text)
out = ""
for sec in sections[1:]:
    fname, _, body = sec.partition("\n")
    out += f"\n{'='*70}\n### FILE: {fname}\n{'='*70}\n"
    # Split by lines, dedupe consecutive identical lines
    seen = set()
    for line in body.split("\n"):
        line = line.strip()
        if not line or line.startswith("--- TABLE"):
            out += line + "\n"
            continue
        if line in seen:
            continue
        seen.add(line)
        out += line + "\n"
        seen = set()  # Reset for non-consecutive dupes

with open(r"D:\B166ER-OpenClaw\workspace\toolbox\weekly_reports_clean.txt", "w", encoding="utf-8") as f:
    f.write(out)
print(f"Cleaned: {len(out)} chars")