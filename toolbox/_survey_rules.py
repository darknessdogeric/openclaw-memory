# -*- coding: utf-8 -*-
import io, sys, os, glob, re
from collections import Counter, defaultdict
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import openpyxl

D = r'C:\Users\ericz\Desktop\产业发展部\外部相关资料'
SRC = [f for f in glob.glob(os.path.join(D, '*.xlsx')) if '预算模板' in os.path.basename(f)][0]
wb = openpyxl.load_workbook(SRC, data_only=False)

YEAR = re.compile(r'(19|20)\d{2}')
DATE = re.compile(r'(19|20)\d{2}[.\-/年]\d{1,2}')

# ---- 1. 列 A 的数字：是不是行号 ----
print('=== 列A数字统计（判断是否为行号索引）===')
a_num = defaultdict(list)
for ws in wb.worksheets:
    for row in ws.iter_rows(max_col=1):
        c = row[0]
        if isinstance(c.value, (int, float)):
            a_num[ws.title].append((c.coordinate, c.value))
for sh, lst in sorted(a_num.items()):
    vals = [v for _, v in lst]
    contig = all(vals[i] == vals[0] + i for i in range(len(vals))) if vals else False
    print('  %-34s n=%-4d 值域=%s 连续递增=%s  样例=%s' % (sh[:34], len(lst), (min(vals), max(vals)) if vals else '-', contig, lst[:4]))
print('  列A数字表数: %d / %d' % (len(a_num), len(wb.worksheets)))

# ---- 2. 文字里的非年份数字：是数据吗 ----
print()
print('=== 文本中含数字（剔除年份/日期/纯标签）的样本 ===')
c = Counter()
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for cell in row:
            v = cell.value
            if isinstance(v, str) and not v.startswith('='):
                s = v.replace('\n', ' ')
                t = DATE.sub('', s)
                t = YEAR.sub('', t)
                t = re.sub(r'\d+([.,]\d+)?', '', t)
                if re.search(r'\d', t):
                    c[(ws.title, s.strip()[:64])] += 1
print('  独立样本数: %d' % len(c))
for (sh, s), n in list(sorted(c.items(), key=lambda x: -x[1]))[:40]:
    print('   [%s] x%d %s' % (sh[:20], n, s))

# ---- 3. 公式中嵌死的数字（=数据伪装成公式）----
print()
print('=== 仅含数字与运算符的公式（应视为数据清空）===')
op = re.compile(r'^[\d\s\.\+\-\*/\(\)]+$')
cnt = 0
samples = []
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for cell in row:
            v = cell.value
            if isinstance(v, str) and v.startswith('=') and op.match(v[1:]):
                cnt += 1
                if len(samples) < 12:
                    samples.append((ws.title, cell.coordinate, v))
print('  数量: %d' % cnt)
for sh, co, v in samples:
    print('   [%s] %s %s' % (sh[:24], co, v[:40]))
