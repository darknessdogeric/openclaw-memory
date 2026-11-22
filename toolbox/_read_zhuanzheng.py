# -*- coding: utf-8 -*-
import io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn
P = r'C:\Users\ericz\Desktop\试用期员工转正审批表（模板）中层.docx'
print('SIZE %.1f KB' % (os.path.getsize(P)/1024))
d = Document(P)
print('段落 %d  表格 %d' % (len(d.paragraphs), len(d.tables)))
body = d.element.body
pm = {p._p: p for p in d.paragraphs}
tm = {t._tbl: t for t in d.tables}
print('=' * 92)
ti = 0
for ch in body.iterchildren():
    if ch.tag == qn('w:p'):
        p = pm.get(ch)
        if p is not None and p.text.strip():
            print('[P] ' + p.text.strip()[:200])
    elif ch.tag == qn('w:tbl'):
        t = tm.get(ch)
        ti += 1
        if t is not None:
            print('=== 表格 %d (%d 行 x %d 列) ===' % (ti, len(t.rows), len(t.columns)))
            for ri, r in enumerate(t.rows):
                print('  R%-2d | %s' % (ri, ' | '.join(c.text.strip().replace(chr(10),' / ')[:100] for c in r.cells)))
            print('=== /表格 %d ===' % ti)