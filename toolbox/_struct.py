# -*- coding: utf-8 -*-
"""核准表结构：合并区域 + 表头行，用于写使用说明"""
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import openpyxl

OUT = r'C:\Users\ericz\Desktop\附件5. 酒店经营预算模板-汇总版（空白模板）v1.0.xlsx'
wb = openpyxl.load_workbook(OUT, data_only=False)

TARGET = ['F&B Steward 餐饮管事部', 'Total酒店汇总表', 'P&L Summary  损益表', '利润表',
          '资产负债表', '现流表', '财务关键指标', 'Flash Report for Sasac', '人工成本',
          'Labour Cost and Headcount 人工成本', 'Energy Cost 能源成本', '主营业务成本下人工']

for name in TARGET:
    if name not in wb.sheetnames:
        continue
    ws = wb[name]
    print('=' * 92)
    print('【%s】 dims=%s  合并 %d' % (name, ws.dimensions, len(ws.merged_cells.ranges)))
    mg = [str(r) for r in ws.merged_cells.ranges]
    row1 = [m for m in mg if re.match(r'^[A-Z]+[1-4]:', m)]
    print('  前4行合并: ' + (', '.join(sorted(row1)[:14]) if row1 else '无'))
    for ri in (1, 2, 3, 4):
        vals = []
        for c in ws[ri]:
            if c.value is not None and str(c.value).strip():
                vals.append('%s=%s' % (c.coordinate, str(c.value).replace('\n', ' ')[:30]))
        if vals:
            print('  R%d %s' % (ri, ' | '.join(vals[:16])))
    # 该表是否还有残留数值（非A列）
    hard = [(c.coordinate, c.value) for row in ws.iter_rows() for c in row
            if isinstance(c.value, (int, float)) and not c.coordinate.startswith('A')]
    print('  非A列硬编码残留: %d %s' % (len(hard), hard[:5] if hard else ''))
print()
print('=' * 92)
print('全部 71 表清单（含首行标题）:')
for i, ws in enumerate(wb.worksheets, 1):
    a1 = str(ws['A1'].value or '')[:40] if ws['A1'].value else ''
    print('  %2d. %-40s %s' % (i, ws.title[:40], a1))
