# -*- coding: utf-8 -*-
import io, sys, os, re, time, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn

D = r'C:\Users\ericz\Desktop\产业发展部\给董事长的单独汇报'
print('=== 目录 ===')
for f in sorted(os.listdir(D)):
    p = os.path.join(D, f)
    if os.path.isfile(p):
        print('  %-70s %5d KB  %s' % (f[:70], os.path.getsize(p) // 1024, time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(p)))))
    else:
        print('  [DIR] ' + f)

P = os.path.join(D, '安逸酒店集团发展赛道与存量改造路径的报告_2026-11-20.docx')
print('')
print('=== 主文档 ===')
print('存在:', os.path.exists(P), ' 大小:', os.path.getsize(P) // 1024 if os.path.exists(P) else 0, 'KB')
d = Document(P)
print('段落 %d  表格 %d' % (len(d.paragraphs), len(d.tables)))
print('')
print('===== 正文 =====')
for i, p in enumerate(d.paragraphs):
    t = p.text.strip()
    if not t:
        continue
    ea = sz = None
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
        break
    st = p.style.name if p.style is not None else ''
    tag = 'H' if ('Head' in st or '标题' in st) else ('C' if (p.alignment is not None and str(p.alignment).endswith('CENTER')) else ' ')
    print('%s P%-3d [%s/%s] %s' % (tag, i, ea, sz, t))
print('')
print('===== 表格 =====')
for ti, tb in enumerate(d.tables):
    print('--- 表 %d (%d 行 x %d 列) ---' % (ti + 1, len(tb.rows), len(tb.columns)))
    for row in tb.rows:
        cells = [c.text.strip().replace('\n', ' ')[:38] for c in row.cells]
        line = ' | '.join([c for c in cells if c])
        if line:
            print('   ' + line[:190])
