# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
t = open(r'D:\B166ER-openclaw\workspace\anyi-ops-kb\07_战略与改革\集团战略文件\省旅投十五五规划_送审稿_全文_v1.0_2026-10-21.txt', encoding='utf-8').read()
for kw in ['国堰','都江堰','文化主题','花园宾馆','四川宾馆','新良','深圳四川大厦']:
    print(kw, '出现', t.count(kw), '次')
print('---- 文化主题 上下文 ----')
import re
for m in re.finditer('文化主题', t):
    print('...', t[max(0,m.start()-90):m.start()+90].replace(chr(10),''), '...')