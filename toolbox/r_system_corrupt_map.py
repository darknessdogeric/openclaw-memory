#!/usr/bin/env python3
"""定位 U+FFFD 损坏字符的精确位置"""
import os, re

path = os.path.expanduser("~/self-improving/rules.md")
text = open(path, encoding="utf-8").read()
lines = text.splitlines()

print("=== 含 U+FFFD 的行分布 ===")
corrupted_lines = []
for i, line in enumerate(lines, 1):
    if '\ufffd' in line:
        corrupted_lines.append(i)

print(f"含损坏字符的行数: {len(corrupted_lines)} / 总 {len(lines)}")
print(f"损坏行号范围: {corrupted_lines[0] if corrupted_lines else '-'} ~ {corrupted_lines[-1] if corrupted_lines else '-'}")

# 按连续块分组
blocks = []
start = corrupted_lines[0]
prev = corrupted_lines[0]
for ln in corrupted_lines[1:]:
    if ln == prev + 1:
        prev = ln
    else:
        blocks.append((start, prev))
        start = ln
        prev = ln
blocks.append((start, prev))

print(f"\n损坏块（连续行）: {len(blocks)} 个")
for s, e in blocks:
    # 找到该块附近最近的规则标题
    header = ""
    for j in range(s-1, max(0, s-30), -1):
        if re.match(r'^#{1,4}\s*R', lines[j]):
            header = lines[j].strip()[:60]
            break
    print(f"  行 {s}-{e} ({e-s+1} 行) 附近规则: {header}")

# 统计每个损坏块的替换字符数
print("\n=== 各规则损坏严重度（按 U+FFFD 计数）===")
# 简单：按标题分段统计
segments = []
current_header = "(文件头)"
current_count = 0
for line in lines:
    if re.match(r'^#{1,4}\s*R', line):
        if current_count > 0:
            segments.append((current_header, current_count))
        current_header = line.strip()[:70]
        current_count = 0
    current_count += line.count('\ufffd')
if current_count > 0:
    segments.append((current_header, current_count))

segments.sort(key=lambda x: -x[1])
for h, c in segments[:15]:
    print(f"  {c:4d} 个损坏字符 | {h}")
