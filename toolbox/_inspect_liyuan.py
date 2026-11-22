# -*- coding: utf-8 -*-
import io, sys, os, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import openpyxl

SRC = r'C:\Users\ericz\Desktop\产业发展部\外部相关资料\附件5. 重庆丽苑酒店2023年酒店经营预算模板-汇总版V4-0306（总收入5114万，利润总额和净利润-640万）(1).xlsx'
c = glob.glob(os.path.join(os.path.dirname(SRC), '*丽苑*'))
if c:
    SRC = c[0]
print('文件:', os.path.basename(SRC))
print('大小: %.1f KB' % (os.path.getsize(SRC) / 1024))

wb = openpyxl.load_workbook(SRC, data_only=False)
print('工作表数:', len(wb.sheetnames))
for ws in wb.worksheets:
    nonempty = 0
    formulas = 0
    for row in ws.iter_rows():
        for c2 in row:
            if c2.value is not None and str(c2.value).strip() != '':
                nonempty += 1
                if isinstance(c2.value, str) and c2.value.startswith('='):
                    formulas += 1
    print('  [%-22s] dims=%s  max_row=%d max_col=%d  非空=%d  公式=%d  合并=%d'
          % (ws.title, ws.dimensions, ws.max_row, ws.max_column, nonempty, formulas, len(ws.merged_cells.ranges)))
print()
print('=== 定义名称 ===')
try:
    for n in wb.defined_names:
        print('  ', n)
except Exception:
    pass
print()
print('=== 各表非空前 12 行速览 ===')
for ws in wb.worksheets:
    print('--- ' + ws.title + ' ---')
    for ri, row in enumerate(ws.iter_rows(max_row=min(12, ws.max_row)), 1):
        vals = []
        for c2 in row:
            v = c2.value
            if v is not None and str(v).strip() != '':
                vals.append('%s=%s' % (c2.coordinate, str(v)[:26]))
        if vals:
            print('  R%-3d %s' % (ri, '  '.join(vals[:12])))
    print()
