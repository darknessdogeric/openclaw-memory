# -*- coding: utf-8 -*-
import io, sys, os, glob, zipfile, re
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import openpyxl

D = r'C:\Users\ericz\Desktop\产业发展部\外部相关资料'
cands = [f for f in glob.glob(os.path.join(D, '*.xlsx')) if '预算模板' in os.path.basename(f)]
SRC = cands[0]
print('文件:', os.path.basename(SRC))

z = zipfile.ZipFile(SRC)
names = z.namelist()
print()
print('=== 包内关键部件（决定 openpyxl 往返是否会丢东西）===')
risky = [n for n in names if any(k in n for k in ('chart', 'media', 'drawing', 'pivot', 'table', 'comments', 'vmlDrawing'))]
print('  图表/图片/透视/批注类部件:', risky if risky else '无')
print('  部件总数:', len(names))
print('  sheets:', len([n for n in names if n.startswith('xl/worksheets/')]))

wb = openpyxl.load_workbook(SRC, data_only=False)
print()
print('=== 工作表清单 ===')
for i, ws in enumerate(wb.worksheets, 1):
    print('  %2d. %-34s dims=%-12s rows=%d cols=%d' % (i, ws.title[:34], ws.dimensions, ws.max_row, ws.max_column))

print()
print('=== 含 4 位年份的字符串（去重计数）===')
yr = Counter()
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            v = c.value
            if isinstance(v, str) and re.search(r'(19|20)\d{2}', v):
                yr[(ws.title, v.replace('\n', ' ')[:70])] += 1
for (sh, s), n in sorted(yr.items(), key=lambda x: (x[0][0], x[0][1])):
    print('  [%-22s] x%-4d %s' % (sh[:22], n, s))

print()
print('=== 硬编码数值（=数据）统计：按表、按列区 ===')
for ws in wb.worksheets:
    numcnt = 0
    fmcnt = 0
    strcnt = 0
    for row in ws.iter_rows():
        for c in row:
            v = c.value
            if v is None:
                continue
            if isinstance(v, str) and v.startswith('='):
                fmcnt += 1
            elif isinstance(v, str):
                strcnt += 1
            elif isinstance(v, (int, float)):
                numcnt += 1
    print('  %-34s 数值=%-6d 公式=%-6d 文本=%d' % (ws.title[:34], numcnt, fmcnt, strcnt))
