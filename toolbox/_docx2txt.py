# -*- coding: utf-8 -*-
import io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn
SRC = r'C:\Users\ericz\Desktop\近期重点工作汇报.docx'
OUT = r'D:\B166ER-openclaw\workspace\tmp\_jqzdgz.txt'
os.makedirs(os.path.dirname(OUT), exist_ok=True)
d = Document(SRC)
pm = {p._p: p for p in d.paragraphs}
tm = {t._tbl: t for t in d.tables}
lines = []
for ch in d.element.body.iterchildren():
    if ch.tag == qn('w:p'):
        p = pm.get(ch)
        if p is not None and p.text.strip():
            lines.append(p.text.strip())
    elif ch.tag == qn('w:tbl'):
        t = tm.get(ch)
        if t is not None:
            lines.append('--- TABLE ---')
            for r in t.rows:
                lines.append(' | '.join(c.text.strip().replace(chr(10),' ') for c in r.cells))
            lines.append('--- /TABLE ---')
txt = chr(10).join(lines)
open(OUT,'w',encoding='utf-8').write(txt)
print('OK', len(txt), 'chars;', len(d.paragraphs), 'paras;', len(d.tables), 'tables')