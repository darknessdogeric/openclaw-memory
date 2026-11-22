# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import openpyxl
p = r'C:\Users\ericz\Desktop\十五五规划指标测算分解表.xlsx'
wb = openpyxl.load_workbook(p, data_only=True)
print('SHEETS', wb.sheetnames)
for ws in wb.worksheets:
    print('\n' + '='*20, ws.title, ws.max_row, 'x', ws.max_column)
    for r in ws.iter_rows(min_row=1, max_row=min(ws.max_row,80), values_only=True):
        cells = ['' if v is None else (str(round(v,4)) if isinstance(v,float) else str(v)) for v in r]
        line = ' | '.join(cells).strip()
        if line.replace('|','').strip():
            print(line[:400])