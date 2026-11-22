#!/usr/bin/env python3
import re

with open(r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md', 'r', encoding='utf-8') as f:
    content = f.read()

last_blocks = re.findall(r'^## HB #\d+.*?(?=^## HB #|\Z)', content, re.MULTILINE | re.DOTALL)
last = last_blocks[-1]
# Print the first 200 chars (header zone)
print('=== HEADER ZONE ===')
print(last[:400])
print('=== END ===')
