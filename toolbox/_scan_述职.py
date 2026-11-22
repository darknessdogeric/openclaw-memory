# -*- coding: utf-8 -*-
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn

SRC = r'C:\Users\ericz\Desktop\安逸酒店集团有限责任公司2025年度经理层向董事会述职报告（待补充批注版）20261028.docx'
d = Document(SRC)
paras = d.paragraphs

print('段落总数 %d  表格 %d' % (len(paras), len(d.tables)))
print()


def run_mark(r):
    rpr = r._element.find(qn('w:rPr'))
    if rpr is None:
        return ''
    m = []
    hl = rpr.find(qn('w:highlight'))
    if hl is not None:
        m.append('HL:' + hl.get(qn('w:val')))
    col = rpr.find(qn('w:color'))
    if col is not None:
        v = col.get(qn('w:val'))
        if v and v.lower() not in ('auto', '000000'):
            m.append('C:' + v)
    return ','.join(m)


marks = []
cur_head = ''
for i, p in enumerate(paras):
    t = p.text.strip()
    st = (p.style.name if p.style is not None else '')
    if st.startswith('Heading') or re.match(r'^（[一二三四五六七八九十]+）', t) or re.match(r'^\d+[\.、]', t):
        cur_head = t[:60]
    mk = []
    for r in p.runs:
        m = run_mark(r)
        if m:
            mk.append((m, r.text))
    if mk:
        marks.append((i, cur_head, t, mk))

print('=== 含格式标记（提亮/彩色）的段落：%d 处 ===' % len(marks))
for i, hd, t, mk in marks:
    print()
    print('[P%d] 上级标题: %s' % (i, hd or '(无)'))
    print('  全文: ' + (t[:300] if t else '(空)'))
    for m, rt in mk:
        print('  >> [%s] %s' % (m, rt[:120]))

print()
print('=== 含"待补充/待核对/待产发/待资产"字样的段落 ===')
for i, p in enumerate(paras):
    t = p.text.strip()
    if re.search(r'待.{0,4}(补充|核对|产发|资产)', t):
        print('[P%d] %s' % (i, t[:260]))
