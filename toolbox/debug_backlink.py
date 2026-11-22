#!/usr/bin/env python3
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from collections import Counter

VAULT = Path(r'D:\B166ER-OpenClaw\workspace\obsidian-vault')
all_stems = Counter(p.stem for p in VAULT.rglob('*.md'))

# 看 AHL 平台 MOC 里的 wikilink
moc = VAULT / "emergence/hubs/AHL 平台 MOC.md"
text = moc.read_text(encoding='utf-8')
links = re.findall(r'\[\[([^\]|#]+)', text)
print(f'AHL 平台 MOC wikilinks: {len(links)}')
unique_stems = Counter()
for l in links:
    stem = l.strip().split('/')[-1].strip()
    if stem:
        unique_stems[stem] += 1

matched = 0
unmatched_samples = []
for stem, cnt in unique_stems.items():
    if all_stems.get(stem, 0) > 0:
        matched += 1
    else:
        if len(unmatched_samples) < 10:
            unmatched_samples.append((stem, cnt))

print(f'Unique stems: {len(unique_stems)}')
print(f'Matched (stem 存在于 vault): {matched}')
print(f'Not matched: {len(unique_stems)-matched}')
print(f'\n=== 未匹配样本 ===')
for s, c in unmatched_samples:
    print(f'  [{c}] stem={s!r}')

# 反向链接统计脚本: 看看是不是从 AHL 平台 MOC 算出来的 backlink 真的加了
# 跑一次诊断
print(f'\n=== 重新统计 backlink ===')
backlink_count = Counter()
all_md = list(VAULT.rglob('*.md'))
for p in all_md:
    try: t = p.read_text(encoding='utf-8')
    except: continue
    links = re.findall(r'\[\[([^\]|#]+)', t)
    for l in links:
        stem = l.strip().split('/')[-1].strip()
        if stem:
            backlink_count[stem] += 1

# 算 AHL 平台 MOC (它的 basename stem 是 "AHL 平台 MOC")
ahl_moc = backlink_count.get("AHL 平台 MOC", 0)
print(f'AHL 平台 MOC 反向: {ahl_moc}')
# 看看 stem 是 "00-项目总览" 的有没加进去
print(f'00-项目总览 反向: {backlink_count.get("00-项目总览", 0)}')
# 看看 stem 是 "自媒体计划" 的
print(f'01-自媒体计划 (有"自媒体计划"的): {backlink_count.get("01-自媒体计划", 0)}')