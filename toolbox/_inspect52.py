# -*- coding: utf-8 -*-
import io, sys, os, re, copy
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn

SRC = r'C:\Users\ericz\Desktop\安逸酒店集团有限责任公司2025年度经理层向董事会述职报告（待补充批注版）20261028.docx'
d = Document(SRC)
P = d.paragraphs

for idx in (52, 54):
    p = P[idx]
    print('===== P%d  style=%s =====' % (idx, p.style.name if p.style else ''))
    for i, r in enumerate(p.runs):
        rpr = r._element.find(qn('w:rPr'))
        hl = col = ea = None
        sz = r.font.size.pt if r.font.size else None
        if rpr is not None:
            h = rpr.find(qn('w:highlight'))
            if h is not None:
                hl = h.get(qn('w:val'))
            c = rpr.find(qn('w:color'))
            if c is not None:
                col = c.get(qn('w:val'))
            f = rpr.find(qn('w:rFonts'))
            if f is not None:
                ea = f.get(qn('w:eastAsia'))
        print('  run%-2d font=%-14s ea=%-12s sz=%-6s bold=%-5s hl=%-8s color=%-8s | %s' % (
            i, str(r.font.name), str(ea), str(sz), str(r.bold), str(hl), str(col), r.text[:46]))
    pf = p.paragraph_format
    print('  段: 首行缩进=%s 行距=%s 段前=%s' % (pf.first_line_indent, pf.line_spacing, pf.space_before))
    print()

# 参考：一个无标记正文段落的字体
p = P[53]
print('===== 参考 P53 首个正文 run =====')
for r in p.runs[:1]:
    rpr = r._element.find(qn('w:rPr'))
    ea = None
    if rpr is not None:
        f = rpr.find(qn('w:rFonts'))
        if f is not None:
            ea = f.get(qn('w:eastAsia'))
    print('  font=%s ea=%s size=%s' % (r.font.name, ea, r.font.size.pt if r.font.size else None))
