# -*- coding: utf-8 -*-
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import openpyxl
DESK = r'C:\Users\ericz\Desktop\产业发展部'

f = os.path.join(DESK, '重要文件', '202609在营酒店（自有资产+轻资产委托管理项目）-(地址+负责人+电话)(1).xlsx')
wb = openpyxl.load_workbook(f, data_only=True, read_only=True)
ws = wb['已开业委托管理项目']
print('=== 已开业委托管理项目 R32+ ===')
for i, row in enumerate(ws.iter_rows(values_only=True)):
    if i < 32 or i > 70:
        continue
    cells = [('' if c is None else str(c).replace(chr(10), ' ').strip()) for c in row]
    if not any(cells):
        continue
    print('   R%-3d %s' % (i, ' | '.join([c[:26] for c in cells if c][:8])[:200]))
print()
for sn in wb.sheetnames:
    if sn not in ('已开业委托管理项目',):
        print('  other sheet:', sn)
wb.close()
print()
print('=== 到期单位 全表 ===')
f2 = os.path.join(DESK, '旗下酒店', '轻资产在管酒店0915（43家）_脱敏版_2026-11-04.xlsx')
wb2 = openpyxl.load_workbook(f2, data_only=True, read_only=True)
ws2 = wb2['到期单位']
for i, row in enumerate(ws2.iter_rows(values_only=True)):
    if i > 30:
        break
    cells = [('' if c is None else str(c).replace(chr(10), ' ').strip()) for c in row]
    if not any(cells):
        continue
    print('   R%-3d %s' % (i, ' | '.join([c[:22] for c in cells if c][:9])[:200]))
wb2.close()
