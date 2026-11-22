# -*- coding: utf-8 -*-
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn

DX = r'C:\Users\ericz\Desktop\产业发展部\给董事长的单独汇报\2026-11-21_发展赛道与存量改造路径_汇报要点.docx'
d = Document(DX)
print('段落 %d  表格 %d' % (len(d.paragraphs), len(d.tables)))
print('')
print('=== 段落与 run 明细（前 30 段）===')
bar = 0
for i, p in enumerate(d.paragraphs[:30]):
    tx = p.text.strip()
    if not tx:
        continue
    runs = []
    for r in p.runs:
        if not r.text.strip():
            continue
        rpr = r._element.find(qn('w:rPr'))
        ea = None
        if rpr is not None:
            f = rpr.find(qn('w:rFonts'))
            if f is not None:
                ea = f.get(qn('w:eastAsia'))
        runs.append('%s:%s' % (ea, r.text[:22]))
    if '‖' in tx:
        bar += 1
    print('P%-2d %s' % (i, ' ‖ '.join(runs)[:170]))
print('')
print('含 ‖ 分隔符的段落数: %d' % bar)
full = '\n'.join(p.text for p in d.paragraphs)
print('全文含 ‖ 次数: %d' % full.count('‖'))
print('全文含 ‖ 字符: %s' % ('是' if '‖' in full else '否'))
