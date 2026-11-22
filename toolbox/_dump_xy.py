# -*- coding: utf-8 -*-
import io, sys, os, zipfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn

SRC = r'C:\Users\ericz\Desktop\中演西南（四川）文旅有限公司与四川省旅游投资有限公司战略合作协议（修改稿10.29（1））(1)(1).docx'
z = zipfile.ZipFile(SRC)
names = z.namelist()
print('文件 %s  %.1f KB' % (os.path.basename(SRC), os.path.getsize(SRC) / 1024))
print('部件: ' + ', '.join(sorted(n for n in names if not n.endswith('/'))))
print('含批注/修订: %s' % ([n for n in names if 'comment' in n.lower() or 'people' in n.lower()] or '无'))
print()

d = Document(SRC)
print('段落 %d  表格 %d' % (len(d.paragraphs), len(d.tables)))
print('=' * 90)
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
                print('  | ' + ' | '.join(c.text.strip().replace('\n', ' ') for c in r.cells) + ' |')
            print('--- /表格 ---')
