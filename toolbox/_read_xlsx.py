# -*- coding: utf-8 -*-
import io, sys, os, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
try:
    import openpyxl
except Exception:
    print('NO_OPENPYXL'); sys.exit(0)
DESK = r'C:\Users\ericz\Desktop\产业发展部'

FILES = [
 ('直营17及32', os.path.join(DESK, '旗下酒店', '安逸直营酒店名录（17及32名录）_脱敏版_2026-11-04.xlsx')),
 ('轻资产43', os.path.join(DESK, '旗下酒店', '轻资产在管酒店0915（43家）_脱敏版_2026-11-04.xlsx')),
 ('在营202609', os.path.join(DESK, '重要文件', '202609在营酒店（自有资产+轻资产委托管理项目）-(地址+负责人+电话)(1).xlsx')),
]

for tag, f in FILES:
    print('=' * 90)
    print('【' + tag + '】 ' + os.path.basename(f))
    if not os.path.exists(f):
        print('  !! 不存在'); continue
    wb = openpyxl.load_workbook(f, data_only=True, read_only=True)
    for sn in wb.sheetnames:
        ws = wb[sn]
        print('  --- sheet: %s  dims=%sx%s ---' % (sn, ws.max_row, ws.max_column))
        rows = []
        for i, row in enumerate(ws.iter_rows(values_only=True)):
            if i > 90:
                break
            cells = [('' if c is None else str(c).replace(chr(10), ' ').strip()) for c in row]
            if not any(cells):
                continue
            rows.append((i, cells))
        for i, cells in rows[:60]:
            line = ' | '.join([c[:26] for c in cells if c][:7])
            print('   R%-3d %s' % (i, line[:200]))
    wb.close()
    print()