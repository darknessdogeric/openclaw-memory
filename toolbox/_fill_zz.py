# -*- coding: utf-8 -*-
import io, sys, os, copy
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn
from docx.table import _Cell

SRC = r'C:\Users\ericz\Desktop\试用期员工转正审批表（模板）中层.docx'
OUT = r'C:\Users\ericz\Desktop\试用期员工转正审批表（产业发展部）20261102.docx'

POINTS = [
 '1、试用期内主要负责产业发展部市场拓展与对外合作，牵头完成商投集团、新启航、中旅集团、空港投资、美团等五项合作框架协议的起草与洽谈。',
 '2、完成古尔沟、总府皇冠假日、三岔湖天府山庄等存量项目的方案比选、改造测算与品牌合作比选，为资产盘活与改造决策提供依据。',
 '3、牵头国堰宾馆文化主题改造营销策划与集团新媒体业务诊断，推动小红书本地生活、抖音矩阵等项目落地。',
 '4、不足在于数据分析深度与项目全周期管理仍需加强，后续以量化跟踪、提前谋划为重点改进。',
]

def set_para(p_el, text):
    runs = p_el.findall(qn('w:r'))
    if runs:
        r = runs[0]
        for extra in runs[1:]:
            p_el.remove(extra)
        ts = r.findall(qn('w:t'))
        if ts:
            ts[0].text = text
            ts[0].set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
            for extra in ts[1:]:
                r.remove(extra)
        else:
            t = r.makeelement(qn('w:t'), {'{http://www.w3.org/XML/1998/namespace}space': 'preserve'})
            t.text = text
            r.append(t)
    else:
        r = p_el.makeelement(qn('w:r'), {})
        t = r.makeelement(qn('w:t'), {'{http://www.w3.org/XML/1998/namespace}space': 'preserve'})
        t.text = text
        r.append(t)
        p_el.append(r)

def set_cell(cell, text):
    ps = cell.paragraphs
    if not ps:
        cell.add_paragraph()
        ps = cell.paragraphs
    set_para(ps[0]._element, text)
    for p in list(ps[1:]):
        p._element.getparent().remove(p._element)

d = Document(SRC)
t = d.tables[0]

def cs(row):
    return [_Cell(tc, t) for tc in row._tr.tc_lst]

r0 = cs(t.rows[0])
set_cell(r0[1], '【待填】')
set_cell(r0[3], '产业发展部')
r1 = cs(t.rows[1])
set_cell(r1[1], '【待填】')
set_cell(r1[3], '____年__月__日 至 ____年__月__日')
r2 = cs(t.rows[2])
set_cell(r2[1], '【待填】')
set_cell(r2[3], '____年__月__日')

r3 = cs(t.rows[3])
cell = r3[1]
ps = cell.paragraphs
tpl = None
for p in ps:
    if '所任岗位试用期间' in p.text:
        tpl = p
        break
if tpl is None:
    tpl = ps[0]
set_para(tpl._element, POINTS[0])
last = tpl._element
for txt in POINTS[1:]:
    newp = copy.deepcopy(tpl._element)
    last.addnext(newp)
    last = newp
    set_para(newp, txt)

d.save(OUT)
print('已保存: %s  (%.1f KB)' % (os.path.basename(OUT), os.path.getsize(OUT)/1024))

d2 = Document(OUT)
t2 = d2.tables[0]
for ri, row in enumerate(t2.rows):
    cells = [_Cell(tc, t2) for tc in row._tr.tc_lst]
    print('R%d | %s' % (ri, ' || '.join((c.text.strip().replace(chr(10),' / ')[:150]) for c in cells)))
print()
print('=== 表格2 是否保持空白 ===')
for ri, row in enumerate(d2.tables[1].rows):
    print('  R%d | %s' % (ri, ' || '.join(c.text.strip().replace(chr(10),' / ')[:40] for c in row.cells)))