# -*- coding: utf-8 -*-
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import openpyxl
from docx import Document
from docx.oxml.ns import qn

XLSX = r'C:\Users\ericz\Desktop\产业发展部\人事组织职能绩效\安逸酒店集团&省旅投集团组织构架及通讯表.xlsx'
print('===== 1. 组织构架通讯表：含 产业发展部 / 三人姓名的行 =====')
wb = openpyxl.load_workbook(XLSX, data_only=True)
print('工作表: ' + ', '.join(wb.sheetnames))
NAMES = ['产业发展部', '肖润宇', '蒋抒伶', '阿都榈玺', '侯红']
for ws in wb.worksheets:
    for ri, row in enumerate(ws.iter_rows(values_only=True), 1):
        vals = [('' if v is None else str(v).strip()) for v in row]
        line = ' | '.join(vals)
        if any(n in line for n in NAMES):
            print('  [%s R%d] %s' % (ws.title, ri, line[:230]))

print()
print('===== 2. 产业发展部2027年预算及架构方案 v5.0 =====')
d = Document(r'C:\Users\ericz\Desktop\产业发展部\人事组织职能绩效\产业发展部2027年预算及架构方案_v5.0修订稿_2026-10-23.docx')
allt = []
body = d.element.body
pm = {p._p: p for p in d.paragraphs}
tm = {t._tbl: t for t in d.tables}
for ch in body.iterchildren():
    if ch.tag == qn('w:p'):
        p = pm.get(ch)
        if p is not None and p.text.strip():
            allt.append(p.text.strip())
    elif ch.tag == qn('w:tbl'):
        t = tm.get(ch)
        if t is not None:
            for r in t.rows:
                allt.append(' | '.join(c.text.strip().replace(chr(10),' / ')[:60] for c in r.cells))
txt = chr(10).join(allt)
print('总字数 %d' % len(txt))
for kw in ['蒋抒伶', '阿都榈玺', '肖润宇', '试用期', '转正', '编制', '岗位设置', '市场拓展', '数智化']:
    hits = [m.start() for m in re.finditer(kw, txt)][:2]
    if hits:
        for h in hits:
            print('  [' + kw + '] ' + txt[max(0,h-150):h+200].replace(chr(10),' / '))
    else:
        print('  [' + kw + '] 无')
