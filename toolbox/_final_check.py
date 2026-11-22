# -*- coding: utf-8 -*-
"""修正 '20221' 错字 + 最终体检"""
import io, sys, os, re, zipfile, shutil
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import xml.etree.ElementTree as ET

OUT = r'C:\Users\ericz\Desktop\附件5. 酒店经营预算模板-汇总版（空白模板）v1.0.xlsx'
KB = r'D:\B166ER-openclaw\workspace\anyi-ops-kb\04_方法论\酒店经营预算模板'
NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
ET.register_namespace('', NS)

z = zipfile.ZipFile(OUT)
items = [(i, z.read(i.filename)) for i in z.infolist()]

# ---------- 1. 修正错字：20221 -> 2022 并统一年份替换 ----------
YEAR = re.compile(r'(?<!\d)(19|20)\d{2}(?!\d)')


def scrub(text):
    def rep(m):
        y = int(m.group(0))
        off = 2023 - y
        out = 'XXXX' if off == 0 else 'XXXX-%d' % off
        if not text[m.end():].startswith('年'):
            out += '年'
        return out
    return YEAR.sub(rep, text)


fixed = 0
residual = Counter()
stage = []
for info, data in items:
    if info.filename == 'xl/sharedStrings.xml':
        root = ET.fromstring(data)
        for si in root.findall('{%s}si' % NS):
            for t in si.iter('{%s}t' % NS):
                if not t.text:
                    continue
                s = t.text
                s2 = re.sub(r'\b20221\b', '2022', s)
                if s2 != s:
                    fixed += 1
                    s = s2
                s2 = scrub(s)
                if s2 != s:
                    t.text = s2
                    fixed += 1
                if re.search(r'(19|20)\d{2}', t.text or ''):
                    residual[(info.filename, (t.text or '')[:50])] += 1
        data = ET.tostring(root, encoding='UTF-8', xml_declaration=True)
    stage.append((info, data))
print('sharedStrings 修正 %d 处' % fixed)
z.close()  # 释放文件锁
if residual:
    print('仍含 4 位年份的文本:')
    for (fn, s), n in list(residual.items())[:15]:
        print('   x%d %s' % (n, s))
else:
    print('仍含 4 位年份的文本: 无')

# ---------- 2. 写出 ----------
if os.path.exists(OUT):
    os.remove(OUT)
zo = zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED)
for info, data in stage:
    zi = zipfile.ZipInfo(info.filename, date_time=info.date_time)
    zi.compress_type = zipfile.ZIP_DEFLATED
    zi.external_attr = info.external_attr
    zo.writestr(zi, data)
zo.close()
os.makedirs(KB, exist_ok=True)
shutil.copy2(OUT, os.path.join(KB, os.path.basename(OUT)))
print('已重写: %s  %.1f KB' % (os.path.basename(OUT), os.path.getsize(OUT) / 1024))

# ---------- 3. XML 完整性体检 ----------
zz = zipfile.ZipFile(OUT)
bad = []
for n in zz.namelist():
    if n.endswith('.xml') or n.endswith('.rels'):
        try:
            ET.fromstring(zz.read(n))
        except Exception as e:
            bad.append((n, str(e)[:80]))
print('XML 解析: %d 个部件，异常 %d 个' % (len([n for n in zz.namelist() if n.endswith(('.xml', '.rels'))]), len(bad)))
for n, e in bad[:10]:
    print('   !! ' + n + ' :: ' + e)

# ---------- 4. 表头抽样 ----------
import openpyxl
wb = openpyxl.load_workbook(OUT, data_only=False)
print()
print('=== 表头年份替换抽样 ===')
shown = 0
for ws in wb.worksheets:
    for row in ws.iter_rows(min_row=1, max_row=4):
        for c in row:
            if isinstance(c.value, str) and ('XXXX' in c.value or 'Budget' in c.value or 'Act' in c.value):
                if shown < 18:
                    print('   [%-22s] %-6s %s' % (ws.title[:22], c.coordinate, c.value.replace('\n', ' ')[:56]))
                    shown += 1
print()
print('=== 关键表首行 ===')
for name in ['Total酒店汇总表', 'P&L Summary  损益表', 'Rooms 房务部', 'F&B Department 餐饮部', '利润表', '资产负债表', '现流表', '财务关键指标']:
    if name in wb.sheetnames:
        ws = wb[name]
        vals = [(c.coordinate, str(c.value)[:40]) for row in ws.iter_rows(min_row=1, max_row=3) for c in row if c.value is not None and str(c.value).strip()]
        print('  [' + name + '] ' + ' | '.join('%s=%s' % (a, b.replace('\n', ' ')) for a, b in vals[:6]))

# ---------- 5. 残留数据体检 ----------
num = 0
nonA = []
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, (int, float)):
                num += 1
                if not c.coordinate.startswith('A'):
                    nonA.append((ws.title, c.coordinate, c.value))
print()
print('剩余数值单元格 %d 个（其中非A列 %d 个）' % (num, len(nonA)))
for sh, co, v in nonA[:12]:
    print('   [%s] %s = %s' % (sh[:22], co, v))

# ---------- 6. 批注抽样 ----------
print()
print('=== 批注抽样（确认是否含酒店专有数据）===')
cn = 0
for n in sorted(zz.namelist()):
    if 'comments' in n and n.endswith('.xml'):
        root = ET.fromstring(zz.read(n))
        for c in root.iter('{%s}comment' % NS):
            txt = ''.join(t.text or '' for t in c.iter('{%s}t' % NS)).strip()
            if txt and cn < 14:
                print('   [%s] %s' % (n.split('/')[-1], txt.replace('\n', ' ')[:90]))
                cn += 1
print('   批注总数抽样显示: %d 条' % cn)
