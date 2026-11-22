# -*- coding: utf-8 -*-
import io, sys, os, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
KB = 'D:\\B166ER-openclaw\\workspace\\anyi-ops-kb'
P = r'C:\Users\ericz\Desktop\2026.11.19_四川省旅游投资集团有限责任公司增资实施细则（试行）.docx'

print('=== 主文档 ===')
print('存在:', os.path.exists(P), ' 大小:', os.path.getsize(P) // 1024 if os.path.exists(P) else 0, 'KB')
d = Document(P)
print('段落 %d  表格 %d' % (len(d.paragraphs), len(d.tables)))
print('')
print('--- 正文全文 ---')
for p in d.paragraphs:
    t = p.text.strip()
    if t:
        st = p.style.name if p.style is not None else ''
        mark = '##' if ('Head' in st or '标题' in st) else '  '
        print(mark + ' ' + t)
print('')
print('--- 表格 ---')
for i, tb in enumerate(d.tables):
    print('  [表 %d] %d 行 x %d 列' % (i + 1, len(tb.rows), len(tb.columns)))
    for row in tb.rows:
        cells = [c.text.strip().replace('\n', ' ')[:40] for c in row.cells]
        line = ' | '.join([c for c in cells if c])
        if line:
            print('      ' + line[:200])
