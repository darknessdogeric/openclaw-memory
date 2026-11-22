# -*- coding: utf-8 -*-
"""交付物完整性复核（被终止进程后的安全确认）"""
import io, sys, os, re, glob, zipfile
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import xml.etree.ElementTree as ET
import openpyxl

OUT = r'C:\Users\ericz\Desktop\附件5. 酒店经营预算模板-汇总版（空白模板）v1.0.xlsx'
KB = r'D:\B166ER-openclaw\workspace\anyi-ops-kb\04_方法论\酒店经营预算模板'
NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
BRANDS = ['丽苑', '维景']

print('=== 1. 文件存在性 ===')
print('  桌面成品: %s' % ('存在 %.1f KB' % (os.path.getsize(OUT) / 1024) if os.path.exists(OUT) else '缺失！'))
for f in glob.glob(os.path.join(KB, '*.xlsx')):
    print('  KB 副本  : %s  %.1f KB' % (os.path.basename(f), os.path.getsize(f) / 1024))

print()
print('=== 2. 桌面残留检查（近期 xlsx/docx，排除成品）===')
import time
cut = time.time() - 86400
res = []
for f in glob.glob(r'C:\Users\ericz\Desktop\*') + glob.glob(r'C:\Users\ericz\Desktop\*.*'):
    if os.path.isfile(f) and os.path.getmtime(f) > cut and f.lower().endswith(('.xlsx', '.xls', '.docx')):
        if os.path.abspath(f) != os.path.abspath(OUT):
            res.append(f)
for f in res:
    print('  残留: %s  %.1f KB' % (os.path.basename(f), os.path.getsize(f) / 1024))
if not res:
    print('  无残留')

print()
print('=== 3. 包完整性 ===')
z = zipfile.ZipFile(OUT)
names = z.namelist()
bad = []
for n in names:
    if n.endswith(('.xml', '.rels')):
        try:
            ET.fromstring(z.read(n))
        except Exception as e:
            bad.append((n, str(e)[:60]))
print('  部件 %d｜XML 异常 %d｜批注 %d｜calcChain %s'
      % (len(names), len(bad), len([n for n in names if 'comments' in n]),
         '存在(异常)' if any('calcChain' in n for n in names) else '已移除'))
for n, e in bad[:6]:
    print('    !! ' + n + ' :: ' + e)

print()
print('=== 4. 内容核验 ===')
wb = openpyxl.load_workbook(OUT, data_only=False)
num = nonA = fml = 0
yrs = []
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            v = c.value
            if v is None:
                continue
            if isinstance(v, str) and v.startswith('='):
                fml += 1
            elif isinstance(v, str):
                if re.search(r'(19|20)\d{2}', v):
                    yrs.append((ws.title, c.coordinate, v[:40]))
            else:
                num += 1
                if not c.coordinate.startswith('A'):
                    nonA += 1
print('  表 %d｜公式 %d｜剩余数值 %d（非A列 %d）｜单元格内4位年份 %s'
      % (len(wb.worksheets), fml, num, nonA, yrs[:3] if yrs else '无'))

ext = 0
for n in names:
    if n.startswith('xl/externalLinks/externalLink') and n.endswith('.xml'):
        ext += len(re.findall(r'<v>[^<]+</v>', z.read(n).decode('utf-8', 'replace')))
print('  外部链接缓存非空值: %d' % ext)

bl = []
for n in names:
    if n.endswith(('.xml', '.rels')):
        t = z.read(n).decode('utf-8', 'replace')
        for b in BRANDS:
            if b in t:
                bl.append((n, b))
print('  品牌名残留: %s' % (bl if bl else '无'))

print()
print('=== 5. 关键表头抽样 ===')
for name in ['Total酒店汇总表', 'P&L Summary  损益表', '财务关键指标', '利润表', 'Total 酒店汇总表']:
    if name in wb.sheetnames:
        ws = wb[name]
        vals = [(c.coordinate, str(c.value)[:32].replace('\n', ' ')) for row in ws.iter_rows(min_row=1, max_row=3) for c in row
                if c.value is not None and str(c.value).strip()]
        print('  [' + name + '] ' + ' | '.join('%s=%s' % (a, b) for a, b in vals[:5]))
