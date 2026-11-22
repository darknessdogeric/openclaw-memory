# -*- coding: utf-8 -*-
import io, sys, os, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import openpyxl

D = r'C:\Users\ericz\Desktop\产业发展部\外部相关资料'
print('=== 目录内 xlsx ===')
for f in sorted(glob.glob(os.path.join(D, '*.xlsx'))):
    print('  %s  %.1f KB' % (os.path.basename(f), os.path.getsize(f) / 1024))

cands = [f for f in glob.glob(os.path.join(D, '*.xlsx')) if '预算模板' in os.path.basename(f)]
if not cands:
    print('FATAL 未找到预算模板'); sys.exit(2)
SRC = cands[0]
print()
print('目标:', os.path.basename(SRC), ' %.1f KB' % (os.path.getsize(SRC) / 1024))

wb = openpyxl.load_workbook(SRC, data_only=False)
print('工作表:', wb.sheetnames)
for ws in wb.worksheets:
    ne = fm = 0
    for row in ws.iter_rows():
        for c in row:
            if c.value is not None and str(c.value).strip() != '':
                ne += 1
                if isinstance(c.value, str) and c.value.startswith('='):
                    fm += 1
    print('  [%-24s] dims=%s rows=%d cols=%d 非空=%d 公式=%d 合并=%d'
          % (ws.title, ws.dimensions, ws.max_row, ws.max_column, ne, fm, len(ws.merged_cells.ranges)))
print()
print('=== 各表前 30 行非空内容 ===')
for ws in wb.worksheets:
    print('---------- ' + ws.title + ' ----------')
    for ri, row in enumerate(ws.iter_rows(max_row=min(30, ws.max_row)), 1):
        vals = []
        for c in row:
            v = c.value
            if v is not None and str(v).strip() != '':
                vals.append('%s=%s' % (c.coordinate, str(v)[:30]))
        if vals:
            print('  R%-3d %s' % (ri, '  '.join(vals[:14])))
    print()
