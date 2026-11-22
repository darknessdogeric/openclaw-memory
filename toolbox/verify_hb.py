"""Verify final HEARTBEAT.md state"""
from pathlib import Path
import re

WORKSPACE = Path('D:/B166ER-OpenClaw/workspace')
HB_FILE = WORKSPACE / 'HEARTBEAT.md'

content = HB_FILE.read_text(encoding='utf-8')
print(f'HEARTBEAT.md: {len(content)/1024:.1f}KB')
print(f'  Threshold check: 1.2MB = {1.2*1024:.1f}KB, current = {len(content)/1024:.1f}KB')
status = 'UNDER threshold OK' if len(content) < 1.2*1024*1024 else 'OVER threshold FAIL'
print(f'  Status: {status}')
print()

matches = re.findall(r'## HB #(\d+)\s+\((\d{4}-\d{2}-\d{2})T(\d{2}:\d{2})', content)
print('Latest HBs:')
for num, date, time in matches[-3:]:
    print(f'  HB #{num} - {date} {time}')
print()

print('Last 5 lines:')
for line in content.splitlines()[-5:]:
    print(f'  {line[:120]}')
print()

print('=== All HEARTBEAT*.md files ===')
for f in WORKSPACE.glob('HEARTBEAT*.md'):
    print(f'  {f.name}: {f.stat().st_size/1024:.1f}KB')
