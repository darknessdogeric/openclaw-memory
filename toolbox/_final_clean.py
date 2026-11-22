# -*- coding: utf-8 -*-
"""最终清洗：批注去数据化 + 品牌名泛化 + 全包残留扫描"""
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
AMT = re.compile(r'[0-9][0-9,\.]*\s*(?:万元|万|元|台|个|人|条|间|次|件|只|套|份|%|％|人天)')
MDATE = re.compile(r'\d{1,2}\s*月\s*\d{1,2}\s*日')
BRANDS = [('丽苑维景', '酒店'), ('丽苑', '酒店'), ('维景', ''), ('重庆丽苑', '酒店')]


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


def scrub_comment(text):
    t = scrub_year(text)
    t = MDATE.sub('', t)
    t = AMT.sub('', t)
    t = re.sub(r'(?<!\d)\d+(?!\d)', '', t)
    t = re.sub(r'[ \t]{2,}', ' ', t)
    t = re.sub(r'\(\s*\)', '', t)
    t = re.sub(r'（\s*）', '', t)
    return t.strip()


z = zipfile.ZipFile(OUT)
items = [(i, z.read(i.filename)) for i in z.infolist()]
z.close()

brand_hits = Counter()
c_fixed = 0
s_fixed = 0
stage = []
for info, data in items:
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
                    c_fixed += 1
        data = ET.tostring(root, encoding='UTF-8', xml_declaration=True)
    elif fn == 'xl/sharedStrings.xml':
        root = ET.fromstring(data)
        for si in root.findall('{%s}si' % NS):
            for t in si.iter('{%s}t' % NS):
                if not t.text:
                    continue
                new = t.text
                for a, b in BRANDS:
                    if a in new:
                        brand_hits[(fn, a)] += 1
                        new = new.replace(a, b)
                new = scrub_year(new)
                if new != t.text:
                    t.text = new
                    s_fixed += 1
        data = ET.tostring(root, encoding='UTF-8', xml_declaration=True)
    else:
        try:
            txt = data.decode('utf-8')
        except UnicodeDecodeError:
            txt = None
        if txt is not None:
            for a, b in BRANDS:
                if a in txt:
                    brand_hits[(fn, a)] += 1
            for pat, rep in [(DATE.pattern, 'XXXX.XX.XX')]:
                txt = re.sub(pat, rep, txt)
            if fn.startswith('xl/worksheets/'):
                txt = re.sub(r'(?<!\d)(19|20)\d{2}(?!\d)', 'XXXX年', txt)
            data = txt.encode('utf-8')
    stage.append((info, data))

print('批注清洗: 修改 %d 处文本' % c_fixed)
print('共享串清洗: 修改 %d 处文本' % s_fixed)
print('品牌名残留（已泛化）: %s' % (dict(brand_hits) if brand_hits else '无'))

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

left = Counter()
for n in zz.namelist():
    if n.endswith(('.xml', '.rels')):
        t = zz.read(n).decode('utf-8', 'replace')
        for a, _ in BRANDS:
            if a in t:
                left[(n, a)] += 1
        if re.search(r'(19|20)\d{2}', t) and 'sharedStrings' not in n:
            pass
print('品牌名残留: %s' % (dict(left) if left else '无'))

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
                    yrs.append((ws.title, c.coordinate, v[:50]))
            else:
                num += 1
                if not c.coordinate.startswith('A'):
                    nonA += 1
print('验证: 表 %d  公式 %d  剩余数值 %d（非A列 %d）' % (len(wb.worksheets), fml, num, nonA))
print('残留 4 位年份文本: %s' % (yrs[:8] if yrs else '无'))
print('批注部件 %d｜vmlDrawing %d｜总部件 %d' % (
    len([n for n in zz.namelist() if 'comments' in n]),
    len([n for n in zz.namelist() if 'vmlDrawing' in n]), len(zz.namelist())))
print()
print('=== 批注清洗后抽样 ===')
cn = 0
for n in sorted(zz.namelist()):
    if 'comments' in n and n.endswith('.xml'):
        root = ET.fromstring(zz.read(n))
        for c in root.iter('{%s}comment' % NS):
            t = ''.join(x.text or '' for x in c.iter('{%s}t' % NS)).strip()
            if t and cn < 14:
                print('   ' + t[:84])
                cn += 1
