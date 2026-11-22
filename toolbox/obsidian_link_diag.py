#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""精确诊断 vault 链接密度"""
import sys, re
from pathlib import Path
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')

VAULT = Path(r'D:\B166ER-OpenClaw\workspace\obsidian-vault')
all_md = list(VAULT.rglob('*.md'))
total = len(all_md)

# 反向链接: wikilink 最后一段 (用 .strip().rstrip('.md') 兼容两种写法)
backlink_count = {}
total_links = 0
has_link_count = 0
for p in all_md:
    try:
        text = p.read_text(encoding='utf-8', errors='ignore')
    except:
        continue
    links = re.findall(r'\[\[([^\]|#]+)', text)
    if links:
        has_link_count += 1
        total_links += len(links)
    for l in links:
        # 用 loose 比较 (去掉 .md 后缀)
        target = l.strip().split('/')[-1].strip().rstrip('.md').lower()
        if target:
            backlink_count[target] = backlink_count.get(target, 0) + 1

# 孤岛 (精确): 用 stem.lower() 比较
islands = [p for p in all_md if p.stem.lower() not in backlink_count] 

print(f'=== 精确诊断 ===')
print(f'总笔记: {total}')
print(f'有 wikilink 的笔记: {has_link_count} ({has_link_count/total*100:.1f}%)')
print(f'总 wikilink 数: {total_links}')
print(f'平均每个有 link 笔记的连接数: {total_links/has_link_count:.1f}')
print(f'**孤岛笔记: {len(islands)} ({len(islands)/total*100:.1f}%)**')

dir_counter = Counter(p.relative_to(VAULT).parts[0] for p in islands)
print(f'\n=== 孤岛按目录分布 ===')
for d, c in dir_counter.most_common():
    print(f'  {d:<30} {c:4d} ({c/len(islands)*100:.1f}%)')

# hub MOC 反向链接
print(f'\n=== hub MOC 反向链接 (网络中心强度) ===')
mocs = ['酒店行业 MOC', 'AI-Agent MOC', 'AHL 平台 MOC', '战略-方法论 MOC',
        'B166ER 知识库 MOC', '工具-系统 MOC', 'Eric 人格-审美 MOC',
        '安逸集团-D-day MOC', '跨境-出海 MOC', '新媒体 MOC',
        'B166ER 全景信息图 MOC']
for m in mocs:
    print(f'  [{backlink_count.get(m.lower(), 0):4d}] {m}')

print(f'\n=== 真正的网络中心 (top 20) ===')
for name, cnt in sorted(backlink_count.items(), key=lambda x: -x[1])[:20]:
    print(f'  [{cnt:4d}] {name}')