# -*- coding: utf-8 -*-
from docx import Document
from collections import Counter
import sys
f = sys.argv[1]
d = Document(f)
s = d.sections[0]
print('margins cm  top=%.1f bot=%.1f left=%.1f right=%.1f' % (s.top_margin.cm, s.bottom_margin.cm, s.left_margin.cm, s.right_margin.cm))
c = Counter(); ls = Counter()
for p in d.paragraphs:
    if not p.text.strip():
        continue
    r = p.runs[0] if p.runs else None
    if r is not None:
        c[(r.font.name, r.font.size.pt if r.font.size else None)] += 1
    ls[str(p.paragraph_format.line_spacing)] += 1
for k, v in c.most_common(8):
    print('font/size', k, '->', v)
print('line_spacing:', ls.most_common(4))
print('tables:', len(d.tables))
tc = Counter()
for t in d.tables:
    for row in t.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                if p.runs:
                    r = p.runs[0]
                    tc[(r.font.name, r.font.size.pt if r.font.size else None)] += 1
                    break
print('table font/size:', tc.most_common(4))

