# -*- coding: utf-8 -*-
import io
p = r"D:\B166ER-openclaw\workspace\toolbox\patch_chair_v21.py"
c = io.open(p, encoding='utf-8').read()
r1 = "    made.append(par._p); return par"
n1 = "    el = par._p if hasattr(par, '_p') else par._tbl\n    made.append(el); return par"
r2 = "    doc.add_paragraph().paragraph_format.space_after = Pt(3)\n    return t"
n2 = "    tail = doc.add_paragraph()\n    tail.paragraph_format.space_after = Pt(3)\n    made.append(t._tbl); made.append(tail._p)\n    return t"
r3 = "keep(tbl(['时间', '指示形态', '产发部应答', '本件关系'],"
n3 = "tbl(['时间', '指示形态', '产发部应答', '本件关系'],"
r4 = "widths=[1.4, 5.0, 5.6, 4.8]))"
n4 = "widths=[1.4, 5.0, 5.6, 4.8])"
for r, n in [(r1, n1), (r2, n2), (r3, n3), (r4, n4)]:
    assert r in c, r[:40]
    c = c.replace(r, n)
io.open(p, 'w', encoding='utf-8').write(c)
print('PATCH SCRIPT FIXED')
