# -*- coding: utf-8 -*-
import io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn
from collections import Counter
p = r'C:\Users\ericz\Desktop\安逸酒店集团与美团合作框架协议_起草稿_20261029.docx'
d = Document(p); s = d.sections[0]
print('页边距 上%.2f 下%.2f 左%.2f 右%.2f cm' % (s.top_margin.cm, s.bottom_margin.cm, s.left_margin.cm, s.right_margin.cm))
print('段落 %d  表格 %d  大小 %.1f KB' % (len(d.paragraphs), len(d.tables), os.path.getsize(p)/1024))
c = Counter(); inds = Counter(); ls = Counter()
for x in d.paragraphs:
    if not x.text.strip(): continue
    for r in x.runs:
        if not r.text.strip(): continue
        rpr = r._element.find(qn('w:rPr')); ea=None; sz=None
        if rpr is not None:
            f = rpr.find(qn('w:rFonts'))
            if f is not None: ea = f.get(qn('w:eastAsia'))
            sn = rpr.find(qn('w:sz'))
            if sn is not None: sz = int(sn.get(qn('w:val')))/2.0
        c[(ea, sz)] += 1
    inds[str(x.paragraph_format.first_line_indent)] += 1
    ls[str(x.paragraph_format.line_spacing)] += 1
print('字体: ' + ' | '.join('%s/%s x%d' % (k[0], k[1], v) for k, v in c.most_common(6)))
print('缩进: ' + ' | '.join('%s x%d' % (k, v) for k, v in inds.most_common(4)))
print('行距: ' + ' | '.join('%s x%d' % (k, v) for k, v in ls.most_common(4)))
print()
for i, x in enumerate(d.paragraphs[:14]):
    if x.text.strip(): print('P%-2d %s' % (i, x.text.strip()[:58]))