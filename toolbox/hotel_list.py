# -*- coding: utf-8 -*-
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
fp = r'D:\\B166ER-openclaw\\workspace\\anyi-ops-kb\\01_集团文件\\安逸集团家底_2026-09-10_v1.3_锦宾国际确认.md'
t = open(fp, encoding='utf-8', errors='ignore').read()
started=False
for l in t.split('\n'):
    s=l.strip()
    if not s: continue
    if re.match(r'^(#|\|).*(酒店|山庄|宾馆|大厦|温泉|实业|茶业|锦江|华龙|国堰|海螺|峨眉|三岔|天府)', s) or re.match(r'^├─|^└─|^│', s):
        print(s[:180])