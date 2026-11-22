# -*- coding: utf-8 -*-
"""收尾修补：inline string 年份 + 外部链接缓存清空 + 品牌名终检"""
import io, sys, os, re, zipfile, shutil
from collections import Counter
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import xml.etree.ElementTree as ET

OUT = r'C:\Users\ericz\Desktop\附件5. 酒店经营预算模板-汇总版（空白模板）v1.0.xlsx'
KB = r'D:\B166ER-openclaw\workspace\anyi-ops-kb\04_方法论\酒店经营预算模板'
NS = 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'
ET.register_namespace('', NS)

YEAR = re.compile(r'(?<!\d)(19|20)\d{2}(?!\d)')
DATE = re.compile(r'(?<!\d)(19|20)\d{2}[.\-]\d{1,2}[.\-]\d{1,2}(?!\d)')
BRANDS = [('丽苑维景', '酒店'), ('重庆丽苑', '酒店'), ('丽苑', '酒店'), ('维景', '')]


def scrub_year(text):
    text = re.sub(r'\b20221\b', '2022', text)
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


z = zipfile.ZipFile(OUT)
items = [(i, z.read(i.filename)) for i in z.infolist()]
z.close()

stats = Counter()
stage = []
for info, data in items:
    fn = info.filename
    # 1) 外部链接缓存：清空全部缓存值（保留链接结构，避免公式变 #REF!）
    if fn.startswith('xl/externalLinks/externalLink') and fn.endswith('.xml'):
        t = data.decode('utf-8')
        n = len(re.findall(r'<v>[^<]*</v>', t))
        t2 = re.sub(r'<v>[^<]*</v>', '<v></v>', t)
        if n:
            stats['外链缓存清空'] += n
        data = t2.encode('utf-8')
    # 2) 共享串
    elif fn == 'xl/sharedStrings.xml':
        root = ET.fromstring(data)
        for si in root.findall('{%s}si' % NS):
            for t in si.iter('{%s}t' % NS):
                if not t.text:
                    continue
                new = scrub_year(scrub_brand(t.text))
                if new != t.text:
                    t.text = new
                    stats['共享串改写'] += 1
        data = ET.tostring(root, encoding='UTF-8', xml_declaration=True)
    # 3) 批注
    elif fn.startswith('xl/comments') and fn.endswith('.xml'):
        root = ET.fromstring(data)
        for c in root.iter('{%s}comment' % NS):
            for t in c.iter('{%s}t' % NS):
                if not t.text:
                    continue
                new = scrub_year(scrub_brand(t.text))
                if new != t.text:
                    t.text = new
                    stats['批注改写'] += 1
        data = ET.tostring(root, encoding='UTF-8', xml_declaration=True)
    # 4) 工作表：inline string
    elif fn.startswith('xl/worksheets/sheet') and fn.endswith('.xml'):
        t = data.decode('utf-8')

        def repl_is(m):
            inner = m.group(1)
            body = m.group(2)
            new = scrub_year(scrub_brand(body))
            if new != body:
                stats['内联文本改写'] += 1
            return '<is>%s</is>' % new
        t2 = re.sub(r'<is>(.*?)</is>', repl_is, t, flags=re.S)
        data = t2.encode('utf-8')
    stage.append((info, data))

print('修补统计: ' + ' | '.join('%s=%d' % (k, v) for k, v in stats.most_common()))

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

# ---------- 验证 ----------
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

brand_left = []
year_left = []
for n in zz.namelist():
    if not n.endswith(('.xml', '.rels')):
        continue
    t = zz.read(n).decode('utf-8', 'replace')
    for a, _ in BRANDS:
        if a in t:
            brand_left.append((n, a))
    if 'docProps/core.xml' in n or 'externalLinks/_rels' in n:
        continue
    for m in re.finditer(r'(19|20)\d{2}', t):
        seg = t[max(0, m.start() - 30):m.start() + 20]
        if 'XXXX' in seg:
            continue
        year_left.append((n, seg.replace('\n', ' ')[:56]))
        break
print('品牌名残留: %s' % (brand_left if brand_left else '无'))
print('4位年份残留(排除core时间戳/外链路径): %s' % (year_left if year_left else '无'))

ext_cache = 0
for n in zz.namelist():
    if n.startswith('xl/externalLinks/externalLink') and n.endswith('.xml'):
        ext_cache += len(re.findall(r'<v>[^<]+</v>', zz.read(n).decode('utf-8', 'replace')))
print('外部链接缓存非空值: %d' % ext_cache)

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
                    yrs.append((ws.title, c.coordinate, v[:44]))
            else:
                num += 1
                if not c.coordinate.startswith('A'):
                    nonA += 1
print('验证: 表 %d  公式 %d  剩余数值 %d（非A列 %d）' % (len(wb.worksheets), fml, num, nonA))
print('单元格内 4 位年份: %s' % (yrs[:6] if yrs else '无'))
print('批注部件 %d｜总部件 %d' % (len([n for n in zz.namelist() if 'comments' in n]), len(zz.namelist())))
print()
print('=== 关键表头抽样 ===')
for name in ['Total酒店汇总表', 'P&L Summary  损益表', '财务关键指标', '利润表']:
    if name in wb.sheetnames:
        ws = wb[name]
        vals = [(c.coordinate, str(c.value)[:34].replace('\n', ' ')) for row in ws.iter_rows(min_row=1, max_row=3) for c in row
                if c.value is not None and str(c.value).strip()]
        print('  [' + name + '] ' + ' | '.join('%s=%s' % (a, b) for a, b in vals[:5]))
