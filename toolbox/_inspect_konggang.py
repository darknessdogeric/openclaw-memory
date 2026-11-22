# -*- coding: utf-8 -*-
import io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn

P = r'D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\空港投资\安逸-空港投资合作框架协议_v1.1_2026-10-26.docx'
d = Document(P)
s = d.sections[0]
print('页边距 上%.2f 下%.2f 左%.2f 右%.2f cm' % (s.top_margin.cm, s.bottom_margin.cm, s.left_margin.cm, s.right_margin.cm))
print('段落 %d  表格 %d' % (len(d.paragraphs), len(d.tables)))
print('=' * 92)
for i, p in enumerate(d.paragraphs):
    t = p.text.strip()
    if not t:
        continue
    r = p.runs[0] if p.runs else None
    ea = sz = None
    if r is not None:
        rpr = r._element.find(qn('w:rPr'))
        if rpr is not None:
            f = rpr.find(qn('w:rFonts'))
            if f is not None:
                ea = f.get(qn('w:eastAsia'))
            szn = rpr.find(qn('w:sz'))
            if szn is not None:
                sz = int(szn.get(qn('w:val')))/2.0
    pf = p.paragraph_format
    print('P%-3d ea=%-11s sz=%-5s bold=%-5s align=%-9s ind=%-8s ls=%-9s sb=%-7s | %s' % (
        i, str(ea), str(sz), str(r.bold if r is not None else None), str(p.alignment),
        str(pf.first_line_indent), str(pf.line_spacing), str(pf.space_before), t[:60]))
