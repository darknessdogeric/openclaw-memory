import re
from pathlib import Path
hb = Path(r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md').read_text(encoding='utf-8-sig')
# Find all HB ## header positions with regex
pattern = re.compile(r'^## HB #(\d+).*?(\d{2}:\d{2}) GMT\+8', re.MULTILINE)
matches = pattern.findall(hb)
# Look for any 15:55
hits_1555 = [m for m in matches if m[1] == '15:55']
hits_1550 = [m for m in matches if m[1] == '15:50']
hits_1601 = [m for m in matches if m[1] == '16:01']
print(f'15:55 entries: {len(hits_1555)} {hits_1555}')
print(f'15:50 entries: {len(hits_1550)} {hits_1550}')
print(f'16:01 entries: {len(hits_1601)} {hits_1601}')