"""Check HEARTBEAT.md tail for HB entries (R-NEW-V3 diagnostic)."""
import re
import sys

path = sys.argv[1] if len(sys.argv) > 1 else r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()
matches = re.findall(r'## HB #(\d+) \(([^\)]+)\)', content)
print(f'Total HB entries: {len(matches)}')
if matches:
    print(f'Last 5 entries:')
    for m in matches[-5:]:
        print(f'  HB #{m[0]} @ {m[1]}')
print(f'File size: {len(content)} chars')