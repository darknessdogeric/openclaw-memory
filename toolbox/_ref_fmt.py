# -*- coding: utf-8 -*-
import io, sys, os, copy
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.shared import Pt, Cm, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

REF = r'C:\Users\ericz\Desktop\中演西南（四川）文旅有限公司与四川省旅游投资有限公司战略合作协议（修改稿10.29（1））(1)(1).docx'
OUT = r'C:\Users\ericz\Desktop\美团与安逸酒店集团有限责任公司战略合作框架协议（起草稿）20261029.docx'

# ---------- 1. 读取参考件版式 ----------
ref = Document(REF)
rs = ref.sections[0]
print('参考件页边距 上%.2f 下%.2f 左%.2f 右%.2f cm' % (rs.top_margin.cm, rs.bottom_margin.cm, rs.left_margin.cm, rs.right_margin.cm))
print('参考件 段落 %d 表格 %d' % (len(ref.paragraphs), len(ref.tables)))
for i, p in enumerate(ref.paragraphs[:14]):
    if not p.text.strip():
        continue
    r = p.runs[0] if p.runs else None
    ea = sz = None
    if r is not None:
        rpr = r._element.find(qn('w:rPr'))
        if rpr is not None:
            f = rpr.find(qn('w:rFonts'))
            if f is not None:
                ea = f.get(qn('w:eastAsia'))
            s = rpr.find(qn('w:sz'))
            if s is not None:
                sz = int(s.get(qn('w:val')))/2.0
    pf = p.paragraph_format
    print('  P%-2d ea=%-12s sz=%-5s bold=%-5s align=%-10s ind=%-8s ls=%-8s | %s' % (
        i, str(ea), str(sz), str(r.bold if r is not None else None), str(p.alignment),
        str(pf.first_line_indent), str(pf.line_spacing), p.text.strip()[:34]))
