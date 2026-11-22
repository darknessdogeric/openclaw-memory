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
    cc.text for t in d.tables for r in t.rows for cc in r.cells)

MUST = ['三类业态', '城市更新片区', '各地市州存量物业', '大四川承接的旅游度假型项目',
        '资源不是第四个业态', '五项不做',
        '峨眉山悦榕庄', '130 间客房全部配私享温泉泡池', '九龙湖悦榕庄', '147 间客房及套房',
        '38 家', '14 个品牌', '零改造先托管', '不挂牌外部品牌', '品牌归属', '排他与优先权',
        '九寨沟悦榕庄经营不佳',
        '可独立先行的隐蔽工程', '首批客房与公共功能区域一次做透', '拓展客房与园林', '剩余区域与运营深化',
        '隐蔽工程与饰面必须同批完成', '样板先行', '45%',
        '底座层全域统一', '收益管理', '四步', '统一口径']
GONE = ['请集团决策六项', '待核实五项', '174 万', '3000 万']
print('')
miss = [k for k in MUST if k not in txt]
print('必须包含: ' + ('全部在' if not miss else '缺: ' + ', '.join(miss)))
still = [k for k in GONE if k in txt]
print('应已删除: ' + ('已删除' if not still else '仍存在: ' + ', '.join(still)))
print('')
print('=== 全文 ===')
for p in d.paragraphs:
    t = p.text.strip()
    if t:
        print(t)
for ti, tb in enumerate(d.tables):
    print('--- 表 %d ---' % (ti + 1))
    for row in tb.rows:
        cells = [x.text.strip().replace('\n', ' / ')[:40] for x in row.cells]
        line = ' | '.join([x for x in cells if x])
        if line:
            print('   ' + line[:180])

IDX = os.path.join(DIR, '00_给董事长的单独汇报_文件索引.md')
t = open(IDX, encoding='utf-8', errors='replace').read()
if 'v2 四板块' not in t:
    blk = ['',
           '> **v2 更新（2026-11-21 12:35）**：按 Eric 指示改为四板块——三业态绑定瞄准资源、'
           '资源型折进旅游度假型（不单列一条线）、存量改造改为按步骤推进、新增悦榕庄案例与数字化；'
           '已删除"请集团决策六项"与"待核实五项"两块。',
           '']
    open(IDX, 'a', encoding='utf-8').write('\n'.join(blk))
    print('')
    print('索引已更新 v2 说明')
