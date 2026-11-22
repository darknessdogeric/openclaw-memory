# -*- coding: utf-8 -*-
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
KB = r'D:\B166ER-openclaw\workspace\anyi-ops-kb'
f = os.path.join(KB, '01_集团文件', '2026-09-16_安逸集团酒店名录三表内化_v1.0.md')
t = open(f, encoding='utf-8', errors='replace').read()
lines = t.split(chr(10))
tbl = [l for l in lines if l.strip().startswith('|')]
print('=== 表格行 45-121 ===')
for l in tbl[44:]:
    print(l[:200])