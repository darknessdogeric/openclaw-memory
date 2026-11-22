# -*- coding: utf-8 -*-
"""最终版：丽苑预算模板 -> 空白模板（一次成型，严格限定改写范围）"""
import io, sys, os, glob, re, zipfile, shutil
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import xml.etree.ElementTree as ET

D = r'C:\Users\ericz\Desktop\产业发展部\外部相关资料'
SRC = [f for f in glob.glob(os.path.join(D, '*.xlsx')) if '预算模板' in os.path.basename(f)][0]
OUT = r'C:\Users\ericz\Desktop\附件5. 酒店经营预算模板-汇总版（空白模板）v1.0.xlsx'
KB = r'D:\B166ER-openclaw\workspace\anyi-ops-kb\04_方法论\酒店经营预算模板'
NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
ET.register_namespace('', NS)

YEAR = re.compile(r'(?<!\d)(19|20)\d{2}(?!\d)')
DATE = re.compile(r'(?<!\d)(19|20)\d{2}[.\-]\d{1,2}[.\-]\d{1,2}(?!\d)')
AMT = re.compile(r'[0-9][0-9,\.]*\s*(?:万元|万|元|台|个|人|条|间|次|件|只|套|份|%|％|人天)')
MDATE = re.compile(r'\d{1,2}\s*月\s*\d{1,2}\s*日')
BRANDS = [('丽苑维景', '酒店'), ('重庆丽苑', '酒店'), ('丽苑', '酒店'), ('维景', '')]
NUMLIKE = re.compile(r'^[\d\s\.\+\-\*/\(\)]+$')
CELL_RE = re.compile(r'<c r="([A-Z]+)(\d+)"([^>]*?)(?:/>|>(.*?)</c>)', re.S)
F_RE = re.compile(r'<f[^>]*>(.*?)</f>', re.S)
V_RE = re.compile(r'<v>.*?</v>', re.S)

z = zipfile.ZipFile(SRC)
items = [(i, z.read(i.filename)) for i in z.infolist()]
z.close()

# ---------- 0. 外部链接是否被公式引用 ----------
ext_used = set()
for info, data in items:
    if info.filename.startswith('xl/worksheets/sheet'):
        t = data.decode('utf-8', 'replace')
        for m in re.finditer(r'<f[^>]*>(.*?)</f>', t, re.S):
            for mm in re.finditer(r'\[(\d+)\]', m.group(1)):
                ext_used.add(int(mm.group(1)))
print('公式引用的外部链接序号: %s' % (sorted(ext_used) if ext_used else '无'))

# ---------- 通用清洗函数 ----------
def scrub_year(text):
    text = DATE.sub('XXXX.XX.XX', text)

    def rep(m):
        y = int(m.group(0))
        off = 2023 - y
        out = 'XXXX' if off == 0 else 'XXXX-%d' % off
        if not text[m.end():].startswith('年'):
            out += '年'
        return out
    return YEAR.sub(rep, text)


def scrub_brand(text):
    for a, b in BRANDS:
        text = text.replace(a, b)
    return text


def scrub_comment(text):
    t = scrub_brand(scrub_year(text))
    t = MDATE.sub('', t)
    t = AMT.sub('', t)
    t = re.sub(r'(?<!\d)\d+(?!\d)', '', t)
    t = re.sub(r'[ \t]{2,}', ' ', t)
    t = re.sub(r'\(\s*\)', '', t)
    t = re.sub(r'（\s*）', '', t)
    return t.strip()


stats = Counter()
brand_hits = Counter()
stage = []

# ---------- 1. sharedStrings ----------
for info, data in items:
    fn = info.filename
    if fn == 'xl/sharedStrings.xml':
        root = ET.fromstring(data)
        for si in root.findall('{%s}si' % NS):
            for t in si.iter('{%s}t' % NS):
                if not t.text:
                    continue
                new = t.text
                for a, _ in BRANDS:
                    if a in new:
                        brand_hits[(fn, a)] += 1
                new = scrub_year(scrub_brand(new))
                if new != t.text:
                    t.text = new
                    stats['共享串改写'] += 1
        data = ET.tostring(root, encoding='UTF-8', xml_declaration=True)
    stage.append((info, data))

# ---------- 2. 批注 ----------
for idx, (info, data) in enumerate(stage):
    fn = info.filename
    if fn.startswith('xl/comments') and fn.endswith('.xml'):
        root = ET.fromstring(data)
        for c in root.iter('{%s}comment' % NS):
            for t in c.iter('{%s}t' % NS):
                if not t.text:
                    continue
                new = scrub_comment(t.text)
                if new != t.text:
                    t.text = new
                    stats['批注改写'] += 1
        stage[idx] = (info, ET.tostring(root, encoding='UTF-8', xml_declaration=True))

# ---------- 3. 工作表：清硬编码数据 + 清伪公式 + 剥缓存值 ----------
def handle_sheet(txt):
    def repl(m):
        col, row, attrs, inner = m.group(1), m.group(2), m.group(3), m.group(4)
        if inner is None:
            return m.group(0)
        fm = F_RE.search(inner)
        if '<f' in inner and fm:
            ftext = fm.group(1).strip()
            if NUMLIKE.match(ftext.replace('=', '')):
                stats['伪公式清空'] += 1
                return '<c r="%s%s"%s/>' % (col, row, attrs)
            stats['公式保留'] += 1
            ni = V_RE.sub('', inner)
            if ni != inner:
                stats['剥缓存值'] += 1
            return '<c r="%s%s"%s>%s</c>' % (col, row, attrs, ni)
        tm = re.search(r'\st="([^"]+)"', attrs)
        ctype = tm.group(1) if tm else None
        if ctype in ('s', 'inlineStr', 'str', 'b'):
            stats['文本保留'] += 1
            return m.group(0)
        if '<v>' in inner:
            if col == 'A':
                stats['列A数字保留'] += 1
            else:
                stats['硬编码清空'] += 1
                return '<c r="%s%s"%s/>' % (col, row, re.sub(r'\st="[^"]+"', '', attrs))
        return m.group(0)
    return CELL_RE.sub(repl, txt)


stage2 = []
for info, data in stage:
    fn = info.filename
    if fn.startswith('xl/worksheets/sheet') and fn.endswith('.xml'):
        txt = data.decode('utf-8')
        nt = handle_sheet(txt)
        if nt != txt:
            data = nt.encode('utf-8')
    stage2.append((info, data))

# ---------- 4. workbook.xml: fullCalcOnLoad ----------
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
    stage3.append((info, data))

# ---------- 5. 移除 calcChain；按需移除 externalLinks ----------
final = []
drop_ext = (not ext_used)
for info, data in stage3:
    fn = info.filename
    if fn == 'xl/calcChain.xml':
        continue
    if drop_ext and (fn.startswith('xl/externalLinks/')):
        continue
    if fn == '[Content_Types].xml':
        t = data.decode('utf-8')
        t = re.sub(r'<Override PartName="/xl/calcChain\.xml"[^>]*/>', '', t)
        if drop_ext:
            t = re.sub(r'<Override PartName="/xl/externalLinks/[^"]*"[^>]*/>', '', t)
        data = t.encode('utf-8')
    if fn == 'xl/_rels/workbook.xml.rels':
        t = data.decode('utf-8')
        t = re.sub(r'<Relationship[^>]*Target="calcChain\.xml"[^>]*/>', '', t)
        if drop_ext:
            t = re.sub(r'<Relationship[^>]*Target="externalLinks/[^"]*"[^>]*/>', '', t)
        data = t.encode('utf-8')
    if not drop_ext and fn.startswith('xl/externalLinks/'):
        t = data.decode('utf-8')
        for a, b in BRANDS:
            if a in t:
                brand_hits[(fn, a)] += 1
                t = t.replace(a, b)
        data = t.encode('utf-8')
    final.append((info, data))
print('calcChain 已移除；externalLinks %s' % ('已移除（公式未引用）' if drop_ext else '保留（公式引用中）'))

# ---------- 6. 写出 ----------
if os.path.exists(OUT):
    os.remove(OUT)
zo = zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED)
for info, data in final:
    zi = zipfile.ZipInfo(info.filename, date_time=info.date_time)
    zi.compress_type = zipfile.ZIP_DEFLATED
    zi.external_attr = info.external_attr
    zo.writestr(zi, data)
zo.close()
os.makedirs(KB, exist_ok=True)
shutil.copy2(OUT, os.path.join(KB, os.path.basename(OUT)))
print('已生成: %s  %.1f KB' % (os.path.basename(OUT), os.path.getsize(OUT) / 1024))
print('处理统计: ' + ' | '.join('%s=%d' % (k, v) for k, v in stats.most_common()))
print('品牌名泛化: %s' % (dict(brand_hits) if brand_hits else '无'))

# ---------- 7. 验证 ----------
zz = zipfile.ZipFile(OUT)
bad = []
for n in zz.namelist():
    if n.endswith(('.xml', '.rels')):
        try:
            ET.fromstring(zz.read(n))
        except Exception as e:
            bad.append((n, str(e)[:70]))
print('XML 完整性: %d 部件，异常 %d' % (len([n for n in zz.namelist() if n.endswith(('.xml', '.rels'))]), len(bad)))
for n, e in bad[:8]:
    print('   !! ' + n + ' :: ' + e)

import openpyxl
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
                    yrs.append((ws.title, c.coordinate, v[:46]))
            else:
                num += 1
                if not c.coordinate.startswith('A'):
                    nonA += 1
print('验证: 表 %d  公式 %d  剩余数值 %d（非A列 %d）' % (len(wb.worksheets), fml, num, nonA))
print('残留 4 位年份: %s' % (yrs[:6] if yrs else '无'))
core = zz.read('docProps/core.xml').decode('utf-8', 'replace')
print('core.xml 时间戳完好: %s' % ('是' if re.search(r'(19|20)\d{2}-\d{2}-\d{2}T', core) else '否'))
print('批注部件 %d｜总部件 %d' % (len([n for n in zz.namelist() if 'comments' in n]), len(zz.namelist())))
print()
print('=== 批注清洗后抽样 ===')
cn = 0
for n in sorted(zz.namelist()):
    if 'comments' in n and n.endswith('.xml'):
        root = ET.fromstring(zz.read(n))
        for c in root.iter('{%s}comment' % NS):
            t = ''.join(x.text or '' for x in c.iter('{%s}t' % NS)).strip()
            if t and cn < 12:
                print('   ' + t[:80])
                cn += 1
