import os
p = r'D:\B166ER-OpenClaw\workspace\HEARTBEAT.md'
print(f'Size now: {os.path.getsize(p)} bytes')
print(f'Size /(1024*1024): {os.path.getsize(p)/1024/1024:.3f} MB')

with open(p, 'r', encoding='utf-8') as f:
    text = f.read()
print(f'Text length (chars): {len(text)}')
print(f'Text encoded UTF-8 bytes: {len(text.encode("utf-8"))}')
print(f'HB #2444 occurrences: {text.count("HB #2444")}')
print(f'HB #2443 occurrences: {text.count("HB #2443")}')
print(f'HB #2442 occurrences: {text.count("HB #2442")}')

# Check for duplicate
import re
matches = re.findall(r'## HB #2444\b', text)
print(f'## HB #2444 header markers: {len(matches)}')
matches43 = re.findall(r'## HB #2443\b', text)
print(f'## HB #2443 header markers: {len(matches43)}')
