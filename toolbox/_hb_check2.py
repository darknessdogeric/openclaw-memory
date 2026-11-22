import re
from pathlib import Path
hb = Path(r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md').read_text(encoding='utf-8-sig')
# Find all HB ## header positions
positions = [(m.group(1), m.start()) for m in re.finditer(r'^## HB #(\d+).*GMT\+8\)', hb, re.MULTILINE)]
print(f'All HB ## header entries: {len(positions)}')
print(f'Last 10:')
for num, pos in positions[-10:]:
    snippet = hb[pos:pos+100].replace('\n', ' ')
    print(f'  HB #{num} @ {pos}: {snippet}')

# Count HB #928 main headers specifically
main_928 = re.findall(r'^## HB #928 ', hb, re.MULTILINE)
print(f'\nMain HB #928 headers: {len(main_928)}')