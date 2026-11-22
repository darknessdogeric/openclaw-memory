# -*- coding: utf-8 -*-
import io, sys, os, re, zipfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn

SRC = r'C:\Users\ericz\Desktop\安逸酒店集团有限责任公司2025年度经理层向董事会述职报告（待补充批注版）20261028.docx'
DST = r'C:\Users\ericz\Desktop\安逸酒店集团有限责任公司2025年度经理层向董事会述职报告（产发部已补充版）20261028.docx'

# 1) 部件完整性（只比文件，不比目录条目）
a = {n for n in zipfile.ZipFile(SRC).namelist() if not n.endswith('/')}
b = {n for n in zipfile.ZipFile(DST).namelist() if not n.endswith('/')}
print('原始文件部件 %d  新文件部件 %d' % (len(a), len(b)))
print('  丢失文件: %s' % (', '.join(sorted(a - b)) or '无'))
print('  新增文件: %s' % (', '.join(sorted(b - a)) or '无'))

d = Document(DST)
P = d.paragraphs

# 2) 全部待补充标记归属
print()
print('=== 全文待补充标记（%d 处）===' % sum(1 for p in P if re.search(r'（待[^）]*）', p.text)))
for i, p in enumerate(P):
    m = re.findall(r'（待[^）]*）', p.text)
    if m:
        print('  P%-3d %s' % (i, ' | '.join(m)))

# 3) 产发两段的字体核验
print()
print('=== 产发补充段字体核验 ===')
for idx in (52, 54):
    p = P[idx]
    print('P%d:' % idx)
    bad = 0
    for r in p.runs:
        rpr = r._element.find(qn('w:rPr'))
        ea = sz = hl = col = None
        if rpr is not None:
            f = rpr.find(qn('w:rFonts'))
            if f is not None:
                ea = f.get(qn('w:eastAsia'))
            h = rpr.find(qn('w:highlight'))
            if h is not None:
                hl = h.get(qn('w:val'))
            c = rpr.find(qn('w:color'))
            if c is not None:
                col = c.get(qn('w:val'))
            s = rpr.find(qn('w:sz'))
            if s is not None:
                sz = int(s.get(qn('w:val'))) / 2.0
        is_marker = (hl == 'yellow')
        flag = ''
        if not is_marker:
            if ea != '仿宋_GB2312' or sz != 16.0:
                flag = '  <== 异常'
                bad += 1
        print('   ea=%-12s sz=%-5s hl=%-8s color=%-8s%s | %s' % (str(ea), str(sz), str(hl), str(col), flag, r.text[:34]))
    pf = p.paragraph_format
    print('   缩进=%s 行距=%s 段前=%s  异常run=%d' % (pf.first_line_indent, pf.line_spacing, pf.space_before, bad))

# 4) 关键数据完整性
print()
print('=== 产发补充段关键数据抽查 ===')
for k in ['1296.09', '44.66%', '235间', '11个温泉汤池', '19个会议室', '266.80', '488', '15%的OTA', '7.5%', '2700至8000', '3万间客房', '5家专业机构', '50%至55%', '280至320', '140至176', '11月15日', '11月2日', '11月7日', '18节车厢', '92名乘客', '5月19日', '爱达邮轮', '中免含税', '境外签证中心', '悦榕集团', '国网商旅', '中青旅商旅', '华为汇通', '道旅']:
    print('  %-14s %s' % (k, 'OK' if k in P[52].text or k in P[54].text else 'MISSING'))
print()
print('  P52 长度 %d 字   P54 长度 %d 字' % (len(P[52].text), len(P[54].text)))
print('  文件大小 %.1f KB' % (os.path.getsize(DST) / 1024))
