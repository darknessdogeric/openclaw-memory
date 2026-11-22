import re
from pathlib import Path
hb = Path(r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md').read_text(encoding='utf-8-sig')
# Find all HB ## header positions with regex
pattern = re.compile(r'^## HB #(\d+).*?(\d{2}:\d{2}) GMT\+8', re.MULTILINE)
matches = pattern.findall(hb)
print(f'Total HB ## header entries: {len(matches)}')
print(f'Last 8 entries:')
for num, time in matches[-8:]:
    print(f'  HB #{num} at {time}')