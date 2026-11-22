# -*- coding: utf-8 -*-
import json
import sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path

# Validate eval JSON
eval_path = Path(r'D:/B166ER-OpenClaw/workspace/eval/2026-07-27.json')
data = json.loads(eval_path.read_text(encoding='utf-8'))
print('=== eval/2026-07-27.json ===')
print('  date:', data['date'])
print('  report:', data['report'])
print('  confidence:', data['confidence'])
print('  key_signals:', len(data['key_signals']), 'items')
print('  20_groups categories:', len(data['twenty_groups']))
print('  anomalies:', len(data['anomalies']), 'items')
print('  predictions:', len(data['predictions_2_4w']), 'items')
print('  recommendations:', len(data['recommendations']), 'targets')
print()

# Check obsidian push
obs_file = Path(r'D:/B166ER-OpenClaw/workspace/obsidian-vault/50-外部接入/cron-outputs/2026-07/10-43-每日商业情报-20集团版-.md')
print('=== Obsidian Push ===')
print('  File:', obs_file.name)
print('  Size:', obs_file.stat().st_size, 'bytes')
text = obs_file.read_text(encoding='utf-8')
print('  Contains 携程:', '携程' in text)
print('  Contains 51.79:', '51.79' in text)
print('  Contains 华安锦江:', '华安锦江' in text)
print('  Contains 20集团:', '20集团' in text)
print()

# Memory file
mem_file = Path(r'D:/B166ER-OpenClaw/workspace/memory/2026-07-27.md')
mem_text = mem_file.read_text(encoding='utf-8')
print('=== memory/2026-07-27.md ===')
print('  Total:', len(mem_text), 'chars')
print('  Has 商业情报:', '商业情报' in mem_text)
print('  Has § 商业情报 section:', '§ 商业情报 · 2026-07-27' in mem_text)