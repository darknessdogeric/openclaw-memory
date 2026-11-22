# -*- coding: utf-8 -*-
"""丽苑预算模板 -> 空白模板 v2（修正：不再边遍历边 append）"""
import io, sys, os, glob, re, zipfile
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
CELL_RE = re.compile(r'<c r="([A-Z]+)(\d+)"([^>]*?)(?:/>|>(.*?)</c>)', re.S)
F_RE = re.compile(r'<f[^>]*>(.*?)</f>', re.S)
V_RE = re.compile(r'<v>.*?</v>', re.S)


def scrub_year(text):
    text = DATE.sub('XXXX.XX.XX', text)

    def rep(m):
        y = int(m.group(0))
        off = BASE_YEAR - y
        out = 'XXXX' if off == 0 else 'XXXX-%d' % off
        if not text[m.end():].startswith('年'):
            out += '年'
        return out
    return YEAR.sub(rep, text)


z = zipfile.ZipFile(SRC)
items = [(i, z.read(i.filename)) for i in z.infolist()]

# ---------- 1. sharedStrings 年份替换 ----------
ss_total = ss_chg = 0
stage1 = []
for info, data in items:
    if info.filename == 'xl/sharedStrings.xml':
        root = ET.fromstring(data)
        for si in root.findall('{%s}si' % NS):
            ss_total += 1
            for t in si.iter('{%s}t' % NS):
                if t.text and re.search(r'(19|20)\d{2}', t.text):
                    new = scrub_year(t.text)
                    if new != t.text:
                        t.text = new
                        ss_chg += 1
        data = ET.tostring(root, encoding='UTF-8', xml_declaration=True)
    stage1.append((info, data))
print('sharedStrings: 共享串 %d 条，改写含年份 %d 条' % (ss_total, ss_chg), flush=True)

# ---------- 2. 工作表清数（独立新列表，避免边遍历边 append）----------
stats = Counter()
stage2 = []
ws_list = [i for i, _ in stage1 if i.filename.startswith('xl/worksheets/sheet') and i.filename.endswith('.xml')]
print('待处理工作表 %d 张' % len(ws_list), flush=True)


def handle_sheet(txt):
    def repl(m):
        col, row, attrs, inner = m.group(1), m.group(2), m.group(3), m.group(4)
        if inner is None:
            return m.group(0)
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
                na = re.sub(r'\st="[^"]+"', '', attrs)
                return '<c r="%s%s"%s/>' % (col, row, na)
        return m.group(0)
    return CELL_RE.sub(repl, txt)


for idx, (info, data) in enumerate(stage1):
    fn = info.filename
    if fn.startswith('xl/worksheets/sheet') and fn.endswith('.xml'):
        txt = data.decode('utf-8')
        nt = handle_sheet(txt)
        if nt != txt:
            data = nt.encode('utf-8')
        if (idx + 1) % 15 == 0:
            print('  ...%d/%d  %s' % (idx + 1, len(stage1), fn), flush=True)
    stage2.append((info, data))

print('单元格处理: ' + ' | '.join('%s=%d' % (k, v) for k, v in stats.most_common()), flush=True)

# ---------- 3. workbook fullCalcOnLoad ----------
stage3 = []
for info, data in stage2:
    if info.filename == 'xl/workbook.xml':
        t = data.decode('utf-8')
        if '<calcPr' in t:
            t = re.sub(r'<calcPr([^>]*?)/>',
                       lambda m: '<calcPr%s fullCalcOnLoad="1"/>' % re.sub(r'\sfullCalcOnLoad="[^"]*"', '', m.group(1)), t, count=1)
        else:
            t = t.replace('</workbook>', '<calcPr calcId="171027" fullCalcOnLoad="1"/></workbook>')
        data = t.encode('utf-8')
        print('workbook.xml: fullCalcOnLoad=1 已设置', flush=True)
    stage3.append((info, data))

# ---------- 4. 移除 calcChain ----------
final = []
for info, data in stage3:
    if info.filename == 'xl/calcChain.xml':
        print('已移除 calcChain.xml', flush=True)
        continue
    if info.filename == '[Content_Types].xml':
        data = re.sub(r'<Override PartName="/xl/calcChain\.xml"[^>]*/>', '', data.decode('utf-8')).encode('utf-8')
    if info.filename == 'xl/_rels/workbook.xml.rels':
        data = re.sub(r'<Relationship[^>]*Target="calcChain\.xml"[^>]*/>', '', data.decode('utf-8')).encode('utf-8')
    final.append((info, data))

# ---------- 5. 写出 ----------
if os.path.exists(OUT):
    os.remove(OUT)
zo = zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED)
for info, data in final:
    zi = zipfile.ZipInfo(info.filename, date_time=info.date_time)
    zi.compress_type = zipfile.ZIP_DEFLATED
    zi.external_attr = info.external_attr
    zo.writestr(zi, data)
zo.close()
print('已生成: %s  %.1f KB' % (os.path.basename(OUT), os.path.getsize(OUT) / 1024), flush=True)

# ---------- 6. 验证 ----------
import openpyxl
wb = openpyxl.load_workbook(OUT, data_only=False)
num = fml = txt = 0
leftover = []
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
                leftover.append((ws.title, c.coordinate, v))
print('验证: 表 %d  公式 %d  文本 %d  剩余数值 %d' % (len(wb.worksheets), fml, txt, num))
nonA = [x for x in leftover if not x[1].startswith('A')]
print('   其中非A列残留: %d' % len(nonA))
for sh, co, v in nonA[:20]:
    print('     [%s] %s = %s' % (sh[:22], co, v))
if years:
    print('残留年份:')
    for (sh, s), n in list(years.items())[:15]:
        print('   [%s] x%d %s' % (sh[:20], n, s))
else:
    print('残留年份: 无')
zz = zipfile.ZipFile(OUT)
names = zz.namelist()
print('批注部件 %d（源 29）｜vmlDrawing %d（源 29）｜总部件 %d' % (
    len([n for n in names if 'comments' in n]), len([n for n in names if 'vmlDrawing' in n]), len(names)))
