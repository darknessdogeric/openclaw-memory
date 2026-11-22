# -*- coding: utf-8 -*-
import io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
D = r'C:\Users\ericz\Desktop\产业发展部\新媒体业务\下属酒店新媒体现状采集'
OUT = r'D:\B166ER-openclaw\workspace\tmp\_xmt_collect.md'
os.makedirs(os.path.dirname(OUT), exist_ok=True)

def docx_text(p):
    from docx import Document
    from docx.oxml.ns import qn
    d = Document(p)
    pm = {x._p: x for x in d.paragraphs}
    tm = {x._tbl: x for x in d.tables}
    lines = []
    for ch in d.element.body.iterchildren():
        if ch.tag == qn('w:p'):
            x = pm.get(ch)
            if x is not None and x.text.strip():
                lines.append(x.text.strip())
        elif ch.tag == qn('w:tbl'):
            t = tm.get(ch)
            if t is not None:
                for r in t.rows:
                    lines.append('| ' + ' | '.join(c.text.strip().replace(chr(10),' ') for c in r.cells) + ' |')
    return chr(10).join(lines)

def pdf_text(p):
    import fitz
    d = fitz.open(p)
    return chr(10).join(pg.get_text() for pg in d)

files = sorted(os.listdir(D))
docs = []
for f in files:
    p = os.path.join(D, f)
    if not os.path.isfile(p):
        continue
    ext = os.path.splitext(f)[1].lower()
    t = ''
    try:
        if ext == '.docx':
            t = docx_text(p)
        elif ext == '.pdf':
            t = pdf_text(p)
    except Exception as e:
        print('ERR %s :: %s' % (f[:50], e))
    t = (t or '').strip()
    docs.append((f, t))
    print('%-64s %6d chars' % (f[:64], len(t)))

parts = []
for f, t in docs:
    parts.append(chr(10) + chr(10) + '===== FILE: ' + f + ' =====' + chr(10))
    parts.append(t if t else '(无文本层/空)')
out = ''.join(parts)
open(OUT, 'w', encoding='utf-8').write(out)
print()
print('FILES %d   TOTAL chars %d' % (len(docs), len(out)))
print('OUT ' + OUT)