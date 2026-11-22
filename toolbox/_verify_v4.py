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

MUST = ['资源为先', '方式是载体', '资源比位置更靠前',
        '一个体系、三个方向、四大能力',
        '城市生活方式', '各城市核心区位物业', '城市更新',
        '全服务政商培训', '各地市州培训会议型存量改造项目', '部分占据城市核心区位',
        '度假', '山川湖泊', '森林',
        '在地文化能力', '资源能力', '产品能力', '数字化能力',
        '类似华住', '底座层全域统一', '输出层对外可售',
        '收益管理', '会议与客源', '经营诊断与预警',
        'Mandai Rainforest Resort', 'Mandai 野生动物保护区', '338 间客房',
        '独栋树屋', '房费含园区门票', '早餐在动物园',
        '可独立先行的隐蔽工程', '首批客房与公共功能区域一次做透', '隐蔽工程与饰面必须同批完成']
GONE = ['一塔一轴', '悦榕庄', '峨眉山悦榕庄', '九龙湖', '请集团决策六项', '待核实五项',
        '九寨沟悦榕庄', '资源型不是第四个业态', '174 万', '3000 万', '第二轴']
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
        cells = [x.text.strip().replace('\n', ' / ')[:46] for x in row.cells]
        line = ' | '.join([x for x in cells if x])
        if line:
            print('   ' + line[:180])

IDX = os.path.join(DIR, '00_给董事长的单独汇报_文件索引.md')
t = open(IDX, encoding='utf-8', errors='replace').read()
if 'v3 资源为先' not in t:
    blk = ['',
           '> **v3 资源为先（2026-11-21 13:20）**：按 Eric 指示重构主线——核心思想"资源为先，方式是载体"；'
           '不设一塔一轴，改为"一个体系（数智化）＋三个方向＋四大能力"；三方向分别瞄准城市核心区位物业、'
           '地市州培训会议型存量改造项目、省内山川湖泊森林等核心景点资源；案例由悦榕庄项目改为 Mandai Rainforest Resort 模式；'
           '删除决策六项与待核实五项。',
           '']
    open(IDX, 'a', encoding='utf-8').write('\n'.join(blk))
    print('')
    print('索引已更新 v3 说明')
