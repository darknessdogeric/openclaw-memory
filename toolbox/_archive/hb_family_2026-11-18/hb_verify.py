#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verify HB #2192 entry is correctly UTF-8."""
import io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

f = 'D:\\B166ER-OpenClaw\\workspace\\HEARTBEAT.md'

# Read raw bytes
with open(f, 'rb') as fp:
    raw = fp.read()

# Find my entry start (using the marker)
marker = b'## HB #2192 (2026-08-02T05:40'
pos = raw.rfind(marker)
print(f'HB #2192 entry starts at byte position: {pos}')

# Find next entry or EOF
next_marker = b'\n## HB #2'
next_pos = raw.find(next_marker, pos + 50)
if next_pos < 0:
    end_pos = len(raw)
else:
    end_pos = next_pos
print(f'HB #2192 entry ends at byte position: {end_pos}')

# Extract entry bytes
entry_bytes = raw[pos:end_pos]
print(f'Entry size: {len(entry_bytes)} bytes')

# Try strict UTF-8 decode
try:
    entry_text = entry_bytes.decode('utf-8', errors='strict')
    print('UTF-8 strict decode: OK')
except UnicodeDecodeError as e:
    print(f'UTF-8 strict decode FAILED at byte {e.start}: {e.reason}')
    print(f'Bytes around failure: {entry_bytes[max(0,e.start-10):e.start+20].hex(" ")}')

# Print first 500 chars of decoded entry
print('---DECODED ENTRY (first 600 chars)---')
print(entry_text[:600])
print('---DECODED ENTRY (chars 600-1200)---')
print(entry_text[600:1200])