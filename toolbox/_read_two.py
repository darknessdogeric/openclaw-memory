# -*- coding: utf-8 -*-
import io, sys, os, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document

DESK = r'C:\Users\ericz\Desktop'
PROJ = r'C:\Users\ericz\Desktop\产业发展部\项目\美团本地生活'

cand_a = glob.glob(os.path.join(DESK, '*美团充电宝战略合作框架协议*.docx'))
cand_b = glob.glob(os.path.join(PROJ, '*起草稿_20261029.docx'))

paths = []
paths.append(('A 对方版', cand_a[0] if cand_a else None))
paths.append(('B 我方版', cand_b[0] if cand_b else None))

for tag, path in paths:
    print('#' * 70)
    print('###', tag, path)
    print('#' * 70)
    if not path or not os.path.exists(path):
        print('  !! NOT FOUND')
        continue
    d = Document(path)
    print('段落 %d  表格 %d' % (len(d.paragraphs), len(d.tables)))
    for i, p in enumerate(d.paragraphs):
        t = p.text.strip()
        print('%2d | %s' % (i, t if t else '(空)'))
    for ti, tb in enumerate(d.tables):
        print('--- 表%d (%d行 x %d列) ---' % (ti+1, len(tb.rows), len(tb.columns)))
        for rr in tb.rows:
            print('   ', ' | '.join(c.text.strip() for c in rr.cells))
    print()
