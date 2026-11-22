#!/usr/bin/env python3
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from collections import Counter

VAULT = Path(r'D:\B166ER-OpenClaw\workspace\obsidian-vault')
all_md = list(VAULT.rglob('*.md'))

# 统计 vault 里所有文件 (两种粒度)
all_stems_strict = Counter(p.name.lower() for p in all_md)  # 00-项目总览.md
all_stems_loose = Counter(p.stem.lower() for p in all_md)   # 00-项目总览

# 测试 wikilink 提取方式: 取最后一段 (可能带 .md)
backlink_count_strict = Counter()
backlink_count_loose = Counter()

for p in all_md:
    try:
        t = p.read_text(encoding='utf-8')
    except:
        continue
    links = re.findall(r'\[\[([^\]|#]+)', t)
    for l in links:
        s = l.strip().split('/')[-1].strip().lower()
        backlink_count_strict[s] += 1
        backlink_count_loose[s.rstrip('.md')] += 1

# 看 AHL 平台 MOC 的实际效果
moc = VAULT / 'emergence/hubs/AHL 平台 MOC.md'
text = moc.read_text(encoding='utf-8')
links = re.findall(r'\[\[([^\]|#]+)', text)
matched_strict = matched_loose = 0
for l in links:
    s = l.strip().split('/')[-1].strip().lower()
    if s in all_stems_strict: matched_strict += 1
    if s.rstrip('.md') in all_stems_loose: matched_loose += 1

print(f'AHL 平台 MOC: {len(links)} wikilinks')
print(f'  strict (.md included) match: {matched_strict}')
print(f'  loose (.md stripped) match: {matched_loose}')

# 现在算 backlink (用 loose)
ahl_moc_loose = backlink_count_loose.get('ahl 平台 moc', 0)
print(f'AHL 平台 MOC 反向 (loose): {ahl_moc_loose}')

# 看 00-项目总览 是否被 link
print(f'00-项目总览 的反向 (strict): {backlink_count_strict.get("00-项目总览", 0)}')  # 没 .md
print(f'00-项目总览.md 的反向 (strict): {backlink_count_strict.get("00-项目总览.md", 0)}')
print(f'00-项目总览 的反向 (loose): {backlink_count_loose.get("00-项目总览", 0)}')