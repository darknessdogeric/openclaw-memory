#!/usr/bin/env python3
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
moc = Path(r'D:\B166ER-OpenClaw\workspace\obsidian-vault\emergence\hubs\AHL 平台 MOC.md')
text = moc.read_text(encoding='utf-8')
print(f'文件大小: {len(text)} chars')
print(f'包含 桌面项目素材: {"桌面项目素材" in text}')
print(f'包含 自媒体计划 wikilink: {"自媒体计划" in text}')
print('---')
print(text[-1500:])