# -*- coding: utf-8 -*-
import io, sys, os, re, zipfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn

P = r'C:\Users\ericz\Desktop\安逸酒店集团有限责任公司2025年度经理层向董事会述职报告（产发部已补充版）20261028.docx'
z = zipfile.ZipFile(P)
print('部件: ' + ', '.join(sorted(z.namelist())))
d = Document(P)
print()
print('段落 %d 表格 %d  修改时间 %s' % (len(d.paragraphs), len(d.tables),
      __import__('datetime').datetime.fromtimestamp(os.path.getmtime(P)).strftime('%H:%M:%S')))
print()
print('=== 全文（含你的修改）===')
for i, p in enumerate(d.paragraphs):
    t = p.text.strip()
    if t:
        mark = ''
        if re.search(r'（待[^）]*）', t):
            mark = '  [标记]'
        print('P%-3d %s%s' % (i, t[:300], mark))
