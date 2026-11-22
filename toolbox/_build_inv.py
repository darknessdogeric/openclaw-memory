# -*- coding: utf-8 -*-
import io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import openpyxl
from collections import Counter
DESK = 'C:\\Users\\ericz\\Desktop\\产业发展部'
WS = 'D:\\B166ER-openclaw\\workspace'
OUT = os.path.join(WS, 'tmp', '_att1.md')

DROP = set([32, 12288, 183, 12295, 46, 12290, 44, 65292, 12289, 65288, 65289, 40, 41, 12304, 12305, 91, 93, 8220, 8221, 34, 39, 45, 65296])
def norm(n):
    s = str(n or '')
    return ''.join(ch for ch in s if ord(ch) not in DROP).replace('安逸', '')

rec = {}
def put(name, cat, rooms, city, src, note=''):
    name = str(name or '').strip()
    if not name or name in ('-', '合计', '小计'):
        return
    k = norm(name)
    if not k:
        return
    r = rec.setdefault(k, {'name': name, 'cat': set(), 'rooms': [], 'city': set(), 'src': set(), 'note': []})
    r['cat'].add(cat)
    r['city'].add(city)
    r['src'].add(src)
    if rooms not in (None, '', '/'):
        rs = str(rooms).strip()
        if rs not in r['rooms']:
            r['rooms'].append(rs)
    if note and note not in r['note']:
        r['note'].append(note)

def dump(path, sheet, cat, src, skip=0):
    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    ws = wb[sheet]
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        if i < skip:
            continue
        c = [('' if x is None else str(x).strip()) for x in row]
        if not any(c):
            continue
        if c[0].strip().isdigit() and len(c) > 4:
            nm = c[1] if len(c) > 1 else ''
            rooms = c[3] if len(c) > 3 else ''
            put(nm, cat, rooms, '', src)
    wb.close()

F1 = os.path.join(DESK, '旗下酒店', '安逸直营酒店名录（17及32名录）_脱敏版_2026-11-04.xlsx')
F2 = os.path.join(DESK, '旗下酒店', '轻资产在管酒店0915（43家）_脱敏版_2026-11-04.xlsx')
F3 = os.path.join(DESK, '重要文件', '202609在营酒店（自有资产+轻资产委托管理项目）-(地址+负责人+电话)(1).xlsx')

dump(F1, '直营酒店17家', '直营', '直营17家表', skip=1)
dump(F2, '管理名录', '委管', '轻资产43家表', skip=1)
dump(F3, '自有资产', '直营', '在营202609表', skip=1)
dump(F3, '已开业委托管理项目', '委管', '在营202609表', skip=1)

wb = openpyxl.load_workbook(F1, data_only=True, read_only=True)
ws = wb['直营酒店32家（含26年闭店停业）']
sec = ''
for i, row in enumerate(ws.iter_rows(values_only=True)):
    c = [('' if x is None else str(x).strip()) for x in row]
    if not any(c):
        continue
    joined = ' '.join(c)
    if '一、自主经营' in joined:
        sec = '自主经营'; continue
    if '二、资产出租' in joined:
        sec = '资产出租'; continue
    if '三、资产闲置' in joined:
        sec = '资产闲置'; continue
    if not c[0].strip().isdigit():
        continue
    if i == 2 and sec == '自主经营':
        nm = c[3]; rooms = c[5]
    else:
        nm = c[1]; rooms = c[3] if len(c) > 3 else ''
    if sec == '自主经营':
        note = '备注已停业' if '已停业' in joined else ''
        put(nm, '直营', rooms, '', '直营32家表', note)
    elif sec == '资产出租':
        put(nm, '资产出租', '', '', '直营32家表')
    elif sec == '资产闲置':
        put(nm, '资产闲置', '', '', '直营32家表')
wb.close()

wb = openpyxl.load_workbook(F2, data_only=True, read_only=True)
ws = wb['到期单位']
for i, row in enumerate(ws.iter_rows(values_only=True)):
    if i < 1:
        continue
    c = [('' if x is None else str(x).strip()) for x in row]
    if not any(c) or not c[0].strip().isdigit():
        continue
    exp = c[7] if len(c) > 7 else ''
    put(c[2], '委管', c[5] if len(c) > 5 else '', c[1] if len(c) > 1 else '', '到期单位表', '合同' + c[3] + '至' + exp)
wb.close()

CAT_ORDER = ['直营', '委管', '资产出租', '资产闲置']
rows = []
for k, v in rec.items():
    if v['rooms']:
        rm = v['rooms'][0]
        conf = '高' if len(set(v['rooms'])) == 1 else '中'
    else:
        rm = ''; conf = '高'
    rows.append({'name': v['name'], 'cat': '/'.join(sorted(v['cat'])), 'rooms': rm, 'conf': conf, 'src': '/'.join(sorted(v['src'])), 'note': '; '.join(v['note'][:2])})
def sk(r):
    c0 = r['cat'].split('/')[0]
    return (CAT_ORDER.index(c0) if c0 in CAT_ORDER else 9, r['name'])
rows.sort(key=sk)

cnt = Counter()
for r in rows:
    for cc in r['cat'].split('/'):
        cnt[cc] += 1
cf = Counter(r['conf'] for r in rows)
print('合并去重条目: %d' % len(rows))
for k, v in cnt.items():
    print('   ' + k + ': ' + str(v))
print('   房数一致(高): ' + str(cf['高']) + '  房数冲突(中): ' + str(cf['中']))
print('')
print('=== 房数冲突条目 ===')
for r in rows:
    if r['conf'] == '中':
        print('   ' + r['name'][:26].ljust(26) + ' ' + r['rooms'][:26].ljust(26) + ' ' + r['src'][:34])
print('')
print('=== 多口径同名条目 ===')
for r in rows:
    if '/' in r['cat']:
        print('   ' + r['name'][:30].ljust(30) + ' ' + r['cat'] + '  ' + r['src'])

L = []
L.append('附件一　安逸集团旗下酒店摸排底册（产业发展部自摸底　2026 年 11 月 13 日）')
L.append('')
L.append('> **用途**：本表是产业发展部依据集团内部五份原始名录（直营 17 家表、直营 32 家资产表、轻资产在管 43 家表、202609 在营酒店表、轻资产到期单位表）自行整理的摸排底册，**尚未经各店确认**。请贵店逐条核对：是否在册、是否遗漏、房数是否准确、经营状态是否属实、归属口径是否正确。核对无误的勾选，不一致的在差异说明栏写明正确情况。')
L.append('')
L.append('| 序号 | 酒店名称 | 归属口径 | 名录房数 | 房数置信度 | 数据来源 | 需核对事项 |')
L.append('|---|---|---|---|---|---|---|')
i = 0
for r in rows:
    i += 1
    note = r['note']
    if not note and '/' in r['cat']:
        note = '同名不同体，请确认是否同一项目'
    if not note and r['conf'] == '中':
        note = '房数口径不一致，请核定'
    L.append('| ' + str(i) + ' | ' + r['name'] + ' | ' + r['cat'] + ' | ' + r['rooms'] + ' | ' + r['conf'] + ' | ' + r['src'] + ' | ' + note + ' |')
L.append('')
L.append('**统计**：合并去重后共 **' + str(len(rows)) + '** 个条目；其中直营 ' + str(cnt['直营']) + '、委管 ' + str(cnt['委管']) + '、资产出租 ' + str(cnt['资产出租']) + '、资产闲置 ' + str(cnt['资产闲置']) + '。房数口径一致 ' + str(cf['高']) + ' 个，存在冲突 ' + str(cf['中']) + ' 个。**本表仅供核对，不作为经营与考核依据。**')
open(OUT, 'w', encoding='utf-8').write(chr(10).join(L))
print('附件一已生成 -> ' + OUT + '  (' + str(len(L)) + ' 行)')