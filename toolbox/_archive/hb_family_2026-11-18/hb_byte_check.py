#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check raw bytes around mojibake in HB #2192 entry."""
import sys

f = 'D:\\B166ER-OpenClaw\\workspace\\HEARTBEAT.md'
with open(f, 'rb') as fp:
    raw = fp.read()

# Find "AnYi" followed by UTF-8 mojibake for 报到
# 报到 UTF-8 = E5 88 B0 E5 88 9A (correct)
# 鎶ュ埌 UTF-8 = E9 8E B6 E5 84 80 E5 88 B0 ... wait let me compute
exp_baodao = 'AnYi 报到'
exp_bytes = exp_baodao.encode('utf-8')
print(f'Expected "AnYi 报到" UTF-8 bytes: {exp_bytes.hex(" ")}')

# Find the mojibake
mojibake_marker = 'AnYi 鎶ュ埌'.encode('utf-8')
print(f'Mojibake marker UTF-8 bytes: {mojibake_marker.hex(" ")}')

idx = raw.find(mojibake_marker)
print(f'Mojibake marker found at byte position: {idx}')
if idx > 0:
    print(f'Bytes around mojibake marker:')
    print(raw[idx:idx+60].hex(' '))
    # Try decoding as GB2312/CP936
    try:
        snippet = raw[idx:idx+20]
        decoded_gb = snippet.decode('cp936', errors='replace')
        print(f'Decoded as CP936: {decoded_gb}')
    except Exception as e:
        print(f'CP936 decode error: {e}')

# Also check HB #2191 entry for comparison (should be clean)
hb2191_marker = 'AnYi 工作分舵'.encode('utf-8')
print('---')
print(f'Clean "AnYi 工作分舵" UTF-8 bytes: {hb2191_marker.hex(" ")}')
idx2 = raw.find(hb2191_marker)
if idx2 > 0:
    print(f'Found HB #2191 clean marker at byte position: {idx2}')
    print(f'Surrounding bytes: {raw[idx2:idx2+30].hex(" ")}')