#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Check file encoding and find non-UTF-8 bytes."""
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

f = 'D:\\B166ER-OpenClaw\\workspace\\HEARTBEAT.md'

# Read as bytes
with open(f, 'rb') as fp:
    raw = fp.read()

print(f'File size: {len(raw)} bytes')

# Try strict UTF-8 decode
try:
    raw.decode('utf-8', errors='strict')
    print('Pure UTF-8 (strict): OK')
except UnicodeDecodeError as e:
    print(f'UTF-8 (strict) FAILED at byte position {e.start}: {e.reason}')
    # Show bytes around the failure
    print(f'Bytes around failure: {raw[max(0,e.start-10):e.start+20].hex(" ")}')
    # Try to identify what character
    print(f'Failed byte: 0x{raw[e.start]:02x}')

# Find all non-UTF-8 byte positions
non_utf8 = []
for i, b in enumerate(raw):
    if b > 0x7F:
        # High byte — check if part of valid UTF-8 sequence
        pass

# Count non-ASCII bytes
non_ascii = sum(1 for b in raw if b > 0x7F)
print(f'Non-ASCII bytes: {non_ascii} / {len(raw)} ({100*non_ascii/len(raw):.1f}%)')

# Try GB2312/CP936 decode
try:
    decoded_gb = raw.decode('gb2312', errors='strict')
    print(f'GB2312 (strict): OK, {len(decoded_gb)} chars')
except UnicodeDecodeError as e:
    print(f'GB2312 (strict) FAILED at byte {e.start}: {e.reason}')

# Find the most likely bad sections (positions where UTF-8 fails)
errors = []
i = 0
while i < len(raw):
    try:
        # Try to decode one char
        char_bytes = raw[i:i+4]  # max UTF-8 char is 4 bytes
        for n in (1, 2, 3, 4):
            try:
                char_bytes[:n].decode('utf-8', errors='strict')
                if char_bytes[n-1:n] == b'' or (char_bytes[n-1] < 0x80 or (0xc0 <= char_bytes[n-1] <= 0xdf and 0x80 <= char_bytes[n] <= 0xbf)):
                    # Boundary
                    char_bytes[:n].decode('utf-8', errors='strict')
                    break
            except:
                continue
        i += 1
    except:
        errors.append(i)
        i += 1

print(f'Approx non-UTF-8 byte positions (first 20): {errors[:20]}')

# Use chardet if available
try:
    import chardet
    result = chardet.detect(raw)
    print(f'chardet result: {result}')
except ImportError:
    print('chardet not available')

# Scan for byte 0xb1 specifically
positions_0xb1 = [i for i, b in enumerate(raw) if b == 0xb1]
print(f'Bytes 0xb1 at positions: {positions_0xb1[:20]}')