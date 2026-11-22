# -*- coding: utf-8 -*-
import io, sys, os, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.shared import Pt

A = glob.glob(r'C:\Users\ericz\Desktop\*美团充电宝战略合作框架协议*.docx')[0]
d = Document(A)

s = d.sections[0]
print('页边距 cm: top=%.2f bottom=%.2f left=%.2f right=%.2f' % (
    s.top_margin.cm, s.bottom_margin.cm, s.left_margin.cm, s.right_margin.cm))
print()

def probe(idx):
    p = d.paragraphs[idx]
    pf = p.paragraph_format
    r = p.runs[0] if p.runs else None
    ea = None
    if r is not None:
        rpr = r._element.find(
            '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rPr')
        if rpr is not None:
            rf = rpr.find(
                '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rFonts')
            if rf is not None:
                ea = rf.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}eastAsia')
    print('p%-3d align=%-14s ind=%-8s ls=%-6s font=%-10s size=%-6s bold=%-5s | %s' % (
        idx, str(p.alignment), str(pf.first_line_indent), str(pf.line_spacing),
        ea, (r.font.size.pt if r is not None and r.font.size else None),
        (r.bold if r is not None else None),
        p.text.strip()[:30]))

for i in [0, 1, 2, 3, 10, 15, 16, 18, 19, 21, 22, 27, 28, 33, 38, 39, 44, 47, 52, 53]:
    probe(i)

print()
print('--- 全文再次确认是否含排他类表述 ---')
f = ''.join(x.text for x in d.paragraphs)
for kw in ['不再与', '排他', '独家', '唯一', '不得与', '仅限', '排它']:
    idxs = [i for i, p in enumerate(d.paragraphs) if kw in p.text]
    for i in idxs:
        print('  [%s] p%d: %s' % (kw, i, d.paragraphs[i].text.strip()[:150]))
