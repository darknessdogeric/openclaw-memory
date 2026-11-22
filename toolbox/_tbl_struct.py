# -*- coding: utf-8 -*-
import io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn
P = r'C:\Users\ericz\Desktop\试用期员工转正审批表（模板）中层.docx'
d = Document(P)
t = d.tables[0]
print('表格1 列数', len(t.columns))
for ri, row in enumerate(t.rows):
    print('--- R%d ---' % ri)
    for ci, tc in enumerate(row._tr.tc_lst):
        pr = tc.find(qn('w:tcPr'))
        gs = vm = None
        w = None
        if pr is not None:
            g = pr.find(qn('w:gridSpan'))
            if g is not None: gs = g.get(qn('w:val'))
            v = pr.find(qn('w:vMerge'))
            if v is not None: vm = v.get(qn('w:val')) or 'continue'
            tw = pr.find(qn('w:tcW'))
            if tw is not None: w = tw.get(qn('w:w'))
        txt = ''.join(x.text or '' for x in tc.iter(qn('w:t')))
        print('   tc%-2d gridSpan=%-4s vMerge=%-10s w=%-6s | %s' % (ci, str(gs), str(vm), str(w), txt[:60]))
print()
print('=== 表格2 结构 ===')
t2 = d.tables[1]
for ri, row in enumerate(t2.rows):
    cells = [c.text.strip().replace(chr(10),' / ')[:60] for c in row.cells]
    print('  R%d | %s' % (ri, ' || '.join(cells)))