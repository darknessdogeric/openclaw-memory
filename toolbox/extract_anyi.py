# -*- coding: utf-8 -*-
import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
fp = r'D:\\B166ER-openclaw\\workspace\\anyi-ops-kb\\01_集团文件\\安逸集团家底_2026-09-10_v1.3_锦宾国际确认.md'
t = open(fp, encoding='utf-8', errors='ignore').read()
lines = t.split('\n')
seen=0
for l in lines:
    s = l.strip()
    if re.search(r'(家酒店|酒店数|客房|房间数|会员|营业收入|资产总额|员工)', s) and 5 < len(s) < 260:
        print(s)
        seen += 1
        if seen > 45: break