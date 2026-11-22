# -*- coding: utf-8 -*-
"""丽苑预算模板 -> 空白模板（zip 内 XML 手术，保留批注/样式/合并/公式）"""
import io, sys, os, glob, re, shutil, zipfile
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import xml.etree.ElementTree as ET

D = r'C:\Users\ericz\Desktop\产业发展部\外部相关资料'
SRC = [f for f in glob.glob(os.path.join(D, '*.xlsx')) if '预算模板' in os.path.basename(f)][0]
OUT = r'C:\Users\ericz\Desktop\附件5. 酒店经营预算模板-汇总版（空白模板）v1.0.xlsx'
BASE_YEAR = 2023

NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
ET.register_namespace('', NS)

YEAR = re.compile(r'(?<!\d)(19|20)\d{2}(?!\d)')
DATE = re.compile(r'(?<!\d)(19|20)\d{2}[.\-]\d{1,2}[.\-]\d{1,2}(?!\d)')
NUMLIKE = re.compile(r'^[\d\s\.\+\-\*/\(\)]+$')


def scrub_year(text):
    text = DATE.sub('XXXX.XX.XX', text)
    def rep(m):
        y = int(m.group(0))
        off = BASE_YEAR - y
        rep_ = 'XXXX' if off == 0 else 'XXXX-%d' % off
        tail = text[m.end():]
        if not tail.startswith('年'):
            rep_ += '年'
        return rep_
    return YEAR.sub(rep, text)


z = zipfile.ZipFile(SRC)
items = [(i, z.read(i.filename)) for i in z.infolist()]

# ============ 1. sharedStrings：年份/日期替换 ============
ss_count = 0
ss_changed = 0
out_items = []
for info, data in items:
    if info.filename == 'xl/sharedStrings.xml':
        root = ET.fromstring(data)
        for si in root.findall('{%s}si' % NS):
            ss_count += 1
            for t in si.iter('{%s}t' % NS):
                if t.text and re.search(r'(19|20)\d{2}', t.text):
                    new = scrub_year(t.text)
                    if new != t.text:
                        t.text = new
                        ss_changed += 1
        data = ET.tostring(root, encoding='UTF-8', xml_declaration=True)
    out_items.append((info, data))
print('sharedStrings: 共享串 %d 条，改写含年份的 %d 条' % (ss_count, ss_changed))

# ============ 2. 工作表：清数据 + 清伪公式 + 剥缓存值 ============
CELL_RE = re.compile(r'<c r="([A-Z]+)(\d+)"([^>]*?)(/>|>(.*?)</c>)', re.S)
F_RE = re.compile(r'<f[^>]*>(.*?)</f>', re.S)
V_RE = re.compile(r'<v>.*?</v>', re.S)

stats = Counter()
sheet_reports = []
for info, data in out_items:
    fn = info.filename
    if not (fn.startswith('xl/worksheets/sheet') and fn.endswith('.xml')):
        continue
    txt = data.decode('utf-8')

    def repl(m):
        col, row, attrs, tail, inner = m.group(1), m.group(2), m.group(3), m.group(4), m.group(5)
        if tail == '/>':
            return m.group(0)
        if inner is None:
            inner = ''
        has_f = '<f' in inner
        fm = F_RE.search(inner)
        if has_f and fm:
            ftext = fm.group(1).strip()
            if NUMLIKE.match(ftext.replace('=', '')):
                stats['伪公式清空'] += 1
                return '<c r="%s%s"%s/>' % (col, row, attrs)
            stats['公式保留'] += 1
            new_inner = V_RE.sub('', inner)
            if new_inner != inner:
                stats['剥缓存值'] += 1
            return '<c r="%s%s"%s>%s</c>' % (col, row, attrs, new_inner)
        # 无公式
        t_m = re.search(r'\st="([^"]+)"', attrs)
        ctype = t_m.group(1) if t_m else None
        if ctype in ('s', 'inlineStr', 'str', 'b'):
            stats['文本保留'] += 1
            return m.group(0)
        if '<v>' in inner:
            if col == 'A':
                stats['列A数字保留'] += 1
            else:
                stats['硬编码清空'] += 1
                new_attrs = re.sub(r'\st="[^"]+"', '', attrs)
                return '<c r="%s%s"%s/>' % (col, row, new_attrs)
        return m.group(0)

    new_txt = CELL_RE.sub(repl, txt)
    if new_txt != txt:
        data = new_txt.encode('utf-8')
    out_items.append((info, data))

print('单元格处理: ' + ' | '.join('%s=%d' % (k, v) for k, v in stats.most_common()))

# ============ 3. workbook.xml：fullCalcOnLoad ============
for idx, (info, data) in enumerate(out_items):
    if info.filename == 'xl/workbook.xml':
        t = data.decode('utf-8')
        if '<calcPr' in t:
            t = re.sub(r'<calcPr([^>]*?)/>', lambda m: '<calcPr%s fullCalcOnLoad="1"/>' % re.sub(r'\sfullCalcOnLoad="[^"]*"', '', m.group(1)), t, count=1)
        else:
            t = t.replace('</workbook>', '<calcPr calcId="171027" fullCalcOnLoad="1"/></workbook>')
        out_items[idx] = (info, t.encode('utf-8'))
        print('workbook.xml: 已设置 fullCalcOnLoad=1')

# ============ 4. 删除 calcChain（含 ContentTypes / rels 清理）============
final = []
for info, data in out_items:
    if info.filename == 'xl/calcChain.xml':
        print('已移除 calcChain.xml（Excel 打开时自动重建）')
        continue
    if info.filename == '[Content_Types].xml':
        t = data.decode('utf-8')
        t = re.sub(r'<Override PartName="/xl/calcChain\.xml"[^>]*/>', '', t)
        data = t.encode('utf-8')
    if info.filename == 'xl/_rels/workbook.xml.rels':
        t = data.decode('utf-8')
        t = re.sub(r'<Relationship[^>]*Target="calcChain\.xml"[^>]*/>', '', t)
        data = t.encode('utf-8')
    final.append((info, data))

# ============ 5. 写出 ============
if os.path.exists(OUT):
    os.remove(OUT)
zo = zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED)
for info, data in final:
    zi = zipfile.ZipInfo(info.filename, date_time=info.date_time)
    zi.compress_type = zipfile.ZIP_DEFLATED
    zi.external_attr = info.external_attr
    zo.writestr(zi, data)
zo.close()
print()
print('已生成: %s  %.1f KB' % (os.path.basename(OUT), os.path.getsize(OUT) / 1024))

# ============ 6. 验证 ============
import openpyxl
wb = openpyxl.load_workbook(OUT, data_only=False)
num = fml = txt = 0
years = Counter()
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            v = c.value
            if v is None:
                continue
            if isinstance(v, str) and v.startswith('='):
                fml += 1
            elif isinstance(v, str):
                txt += 1
                if re.search(r'(19|20)\d{2}', v):
                    years[(ws.title, v[:40])] += 1
            else:
                num += 1
print('验证: 表 %d  公式 %d  文本 %d  剩余数值 %d' % (len(wb.worksheets), fml, txt, num))
print('剩余硬编码数值所在单元格:')
cnt = 0
for ws in wb.worksheets:
    for row in ws.iter_rows():
        for c in row:
            if isinstance(c.value, (int, float)):
                if cnt < 25:
                    print('   [%s] %s = %s' % (ws.title[:22], c.coordinate, c.value))
                cnt += 1
print('   合计 %d 个（应全部位于 A 列行号）' % cnt)
if years:
    print('残留年份:')
    for (sh, s), n in list(years.items())[:20]:
        print('   [%s] x%d %s' % (sh[:20], n, s))
else:
    print('残留年份: 无')
zz = zipfile.ZipFile(OUT)
names = zz.namelist()
print('批注部件: %d 个（源文件 29 个）' % len([n for n in names if 'comments' in n]))
print('vmlDrawing: %d 个（源文件 29 个）' % len([n for n in names if 'vmlDrawing' in n]))
print('总部件: %d' % len(names))
