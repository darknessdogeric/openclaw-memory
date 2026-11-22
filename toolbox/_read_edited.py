# -*- coding: utf-8 -*-
import io, sys, os, re, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn

P = r'C:\Users\ericz\Desktop\2026-11-21_对大运营体系建设实施方案草案的意见建议_一页纸.docx'
print('存在:', os.path.exists(P), ' 大小:', os.path.getsize(P) // 1024 if os.path.exists(P) else 0, 'KB')
print('修改时间:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(P))))
d = Document(P)
print('段落 %d  表格 %d' % (len(d.paragraphs), len(d.tables)))
print('')
print('===== 正文（带字体）=====')
for i, p in enumerate(d.paragraphs):
    t = p.text.strip()
    if not t:
        continue
    ea = sz = None
    b = False
    for r in p.runs:
        if not r.text.strip():
            continue
        rpr = r._element.find(qn('w:rPr'))
        if rpr is not None:
            f = rpr.find(qn('w:rFonts'))
            if f is not None:
                ea = f.get(qn('w:eastAsia'))
            s2 = rpr.find(qn('w:sz'))
            if s2 is not None:
                sz = int(s2.get(qn('w:val'))) / 2.0
            if rpr.find(qn('w:b')) is not None:
                b = True
        break
    print('P%-2d [%s/%s%s] %s' % (i, ea, sz, ' B' if b else '', t))
if d.tables:
    print('')
    print('===== 表格 =====')
    for tb in d.tables:
        for row in tb.rows:
            print('  ' + ' | '.join([c.text.strip().replace('\n', ' ')[:50] for c in row.cells]))
