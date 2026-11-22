# -*- coding: utf-8 -*-
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
pdf = r'C:\Users\ericz\Desktop\四川省旅游投资集团有限责任公司十五五发展规划（送审稿）.pdf'
print('EXISTS', os.path.exists(pdf), os.path.getsize(pdf) if os.path.exists(pdf) else 0)
import pdfplumber
with pdfplumber.open(pdf) as p:
    print('PAGES', len(p.pages))
    out=[]
    for i, pg in enumerate(p.pages):
        t = pg.extract_text() or ''
        out.append('===== P%d =====\n%s' % (i+1, t))
    txt='\n'.join(out)
open(r'D:\B166ER-openclaw\workspace\anyi-ops-kb\07_战略与改革\集团战略文件\省旅投十五五规划_送审稿_全文_v1.0_2026-10-21.txt','w',encoding='utf-8').write(txt)
print('CHARS', len(txt))
print(txt[:1500])