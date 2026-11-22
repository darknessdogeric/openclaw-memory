# -*- coding: utf-8 -*-
import io, sys, os, re, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn
from collections import Counter

DESK = r'C:\Users\ericz\Desktop'
DIR = os.path.join(DESK, '产业发展部', '给董事长的单独汇报')
NAME = '2026-11-21_发展赛道与存量改造路径_汇报要点一页纸'
DX = os.path.join(DIR, NAME + '.docx')

print('=== 交付物核验 ===')
print('存在:', os.path.exists(DX), ' 大小:', os.path.getsize(DX) // 1024, 'KB')
print('修改时间:', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(DX))))
d = Document(DX)
c = Counter()
for p in d.paragraphs:
    for r in p.runs:
        if not r.text.strip():
            continue
        rpr = r._element.find(qn('w:rPr'))
        ea = sz = None
        if rpr is not None:
            f = rpr.find(qn('w:rFonts'))
            if f is not None:
                ea = f.get(qn('w:eastAsia'))
            s2 = rpr.find(qn('w:sz'))
            if s2 is not None:
                sz = int(s2.get(qn('w:val'))) / 2.0
        c[(ea, sz)] += 1
s = d.sections[0]
print('字体: ' + ' | '.join('%s/%s x%d' % (k[0], k[1], v) for k, v in c.most_common(6)))
print('页边距 上%.1f 下%.1f 左%.1f 右%.1f cm' % (s.top_margin.cm, s.bottom_margin.cm, s.left_margin.cm, s.right_margin.cm))
print('段落 %d  表格 %d' % (len(d.paragraphs), len(d.tables)))
txt = '\n'.join(p.text for p in d.paragraphs) + '\n' + '\n'.join(
    c2.text for t in d.tables for r in t.rows for c2 in r.cells)
CK = ['三业态', '资源轴', '174 万', '3000 万', '45%', '零改造先托管', '不挂牌外部品牌',
      '品牌归属', '会员与数据归属', '排他与优先权', '底座层', '收益管理', '四步',
      '请集团决策六项', '待核实五项', '锦秀商标', '297 天']
print('')
print('关键内容: ' + ('全部在' if all(k in txt for k in CK) else '缺: ' + ', '.join(k for k in CK if k not in txt)))

# 更新索引
IDX = os.path.join(DIR, '00_给董事长的单独汇报_文件索引.md')
MARK = '2026-11-21 汇报要点一页纸'
if os.path.exists(IDX):
    t = open(IDX, encoding='utf-8', errors='replace').read()
    if MARK in t:
        print('')
        print('索引已含该条目，跳过')
    else:
        blk = []
        blk.append('')
        blk.append('## 2026-11-21 汇报要点一页纸（' + MARK + '）')
        blk.append('')
        blk.append('| 文件 | 用途 |')
        blk.append('|---|---|')
        blk.append('| `2026-11-21_发展赛道与存量改造路径_汇报要点一页纸.docx` | 《安逸酒店集团发展赛道与存量改造路径的报告_2026-11-20.docx》的董事长汇报要点，一页纸。含一句话结论、赛道三业态表、改造三级下探表（含止损线）、资源型项目零改造先托管、数字化三层四场景四步、请集团决策六项、待核实五项。LibreOffice 实测 1 页 |')
        blk.append('')
        open(IDX, 'a', encoding='utf-8').write('\n'.join(blk))
        print('')
        print('索引已追加 -> %d B' % os.path.getsize(IDX))
else:
    print('')
    print('索引文件不存在')

print('')
print('=== 目录最终状态 ===')
for f in sorted(os.listdir(DIR)):
    p = os.path.join(DIR, f)
    if os.path.isfile(p):
        print('  %-68s %5d KB  %s' % (f[:68], os.path.getsize(p) // 1024, time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(p)))))
