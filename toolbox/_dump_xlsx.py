# -*- coding: utf-8 -*-
import io, sys, os, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import openpyxl

cands = glob.glob(r'C:\Users\ericz\Desktop\2026.10.25*.xlsx')
print('候选台账:')
for c in cands:
    print('  ' + os.path.basename(c) + '  %.1f KB' % (os.path.getsize(c) / 1024))
if not cands:
    print('FATAL 未找到 xlsx'); sys.exit(2)

wb = openpyxl.load_workbook(cands[0], data_only=True)
print('工作表: ' + ', '.join(wb.sheetnames))
print()
for ws in wb.worksheets:
    print('===== 表: ' + ws.title + '  (%d 行 x %d 列) =====' % (ws.max_row, ws.max_column))
    for ri, row in enumerate(ws.iter_rows(values_only=True), 1):
        vals = [('' if v is None else str(v).strip().replace('\n', ' ')) for v in row]
        line = ' | '.join(vals).rstrip(' |')
        if line.strip():
            print('  R%-3d %s' % (ri, line[:250]))
    print()
