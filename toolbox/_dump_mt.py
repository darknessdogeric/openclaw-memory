# -*- coding: utf-8 -*-
import io, sys, os, zipfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn
SRC = r'C:\Users\ericz\Desktop\与美团充电宝合作业务洽谈会议纪要.docx'
z = zipfile.ZipFile(SRC)
print('文件 %s  %.1f KB' % (os.path.basename(SRC), os.path.getsize(SRC)/1024))
print('批注/修订部件: %s' % ([n for n in z.namelist() if 'comment' in n.lower() or 'people' in n.lower()] or '无'))
d = Document(SRC)
print('段落 %d  表格 %d' % (len(d.paragraphs), len(d.tables)))
print('='*92)
body = d.element.body
pm = {p._p: p for p in d.paragraphs}
tm = {t._tbl: t for t in d.tables}
for ch in body.iterchildren():
    if ch.tag == qn('w:p'):
        p = pm.get(ch)
        if p is not None and p.text.strip():
            print(p.text.strip())
    elif ch.tag == qn('w:tbl'):
        t = tm.get(ch)
        if t is not None:
            print('--- 表格 ---')
            for r in t.rows:
                print('  | ' + ' | '.join(c.text.strip().replace(chr(10),' ') for c in r.cells) + ' |')
            print('--- /表格 ---')