# -*- coding: utf-8 -*-
import io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import openpyxl
from collections import Counter
DESK = 'C:\\Users\\ericz\\Desktop\\产业发展部'
WS = 'D:\\B166ER-openclaw\\workspace'
OUT = os.path.join(WS, 'tmp', '_att1.md')
F1 = os.path.join(DESK, '旗下酒店', '安逸直营酒店名录（17及32名录）_脱敏版_2026-11-04.xlsx')
F2 = os.path.join(DESK, '旗下酒店', '轻资产在管酒店0915（43家）_脱敏版_2026-11-04.xlsx')
F3 = os.path.join(DESK, '重要文件', '202609在营酒店（自有资产+轻资产委托管理项目）-(地址+负责人+电话)(1).xlsx')

DROP = set([32, 12288, 183, 12295, 46, 12290, 44, 65292, 12289, 65288, 65289, 40, 41, 12304, 12305, 91, 93, 8220, 8221, 34, 39, 45, 65296, 12288])
def norm(n):
    s = str(n or '')
    return ''.join(ch for ch in s if ord(ch) not in DROP).replace('安逸', '').replace('酒店', '').replace('宾馆', '')

rec = {}
def put(nm, cat, rooms, mode, city, status, term, src, star=''):
    nm = str(nm or '').strip()
    if not nm or nm in ('-', '合计', '小计', '序号', '酒店'):
        return
    k = norm(nm)
    if not k:
        return
    r = rec.setdefault(k, {'name': nm, 'cat': set(), 'rooms': [], 'mode': set(), 'city': set(), 'status': set(), 'term': set(), 'src': set(), 'star': set()})
    r['cat'].add(cat)
    r['src'].add(src)
    if str(rooms).strip() not in ('', '/'):
        if str(rooms).strip() not in r['rooms']:
            r['rooms'].append(str(rooms).strip())
    if mode: r['mode'].add(str(mode).strip())
    if city: r['city'].add(str(city).strip())
    if status: r['status'].add(str(status).strip())
    if term: r['term'].add(str(term).strip())
    if star: r['star'].add(str(star).strip())

def rows_of(path, sheet, hdr):
    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    ws = wb[sheet]
    out = []
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        if i < hdr: continue
        c = [('' if x is None else str(x).strip().replace(chr(10), ' ')) for x in row]
        if any(c): out.append((i, c))
    wb.close()
    return out

# --- F1 直营17家 ---
for i, c in rows_of(F1, '直营酒店17家', 2):
    if not c[0].isdigit(): continue
    put(c[1], '直营', c[3], '直营经营', '', '', '', '直营17家表', c[2])
# --- F3 自有资产 ---
for i, c in rows_of(F3, '自有资产', 2):
    if not c[0].isdigit(): continue
    put(c[1], '直营', c[3], '直营经营', '', '', '', '在营202609表', c[2])
# --- F2 管理名录 ---
for i, c in rows_of(F2, '管理名录', 2):
    if not c[0].isdigit(): continue
    g = lambda k: (c[k] if len(c) > k else '')
    put(g(1), '委管', g(2), g(11), g(4) + ' ' + g(5), g(12), g(9), '轻资产43家表', g(3))
# --- F3 已开业委托管理项目 ---
for i, c in rows_of(F3, '已开业委托管理项目', 2):
    if not c[0].isdigit(): continue
    g = lambda k: (c[k] if len(c) > k else '')
    put(g(1), '委管', g(4), g(2), '', g(5), '', '在营202609表', g(3))
# --- F2 到期单位 ---
for i, c in rows_of(F2, '到期单位', 1):
    if not c[0].isdigit(): continue
    g = lambda k: (c[k] if len(c) > k else '')
    put(g(2), '委管', g(5), g(3), g(1), g(6), g(9), '到期单位表', g(4))
# --- F1 直营32家（资产口径）---
sec = ''
for i, c in rows_of(F1, '直营酒店32家（含26年闭店停业）', 2):
    j = ' '.join(c)
    if '一、自主经营' in j: sec = '自主经营'; continue
    if '二、资产出租' in j: sec = '资产出租'; continue
    if '三、资产闲置' in j: sec = '资产闲置'; continue
    if not c[2].isdigit(): continue
    if sec == '自主经营':
        put(c[3], '直营', c[5], '直营经营', '', c[9], '', '直营32家表', c[4])
    elif sec == '资产出租':
        put(c[3], '资产出租', '', '资产出租', '', c[9] if len(c) > 9 else '', '', '直营32家表')
    elif sec == '资产闲置':
        put(c[3], '资产闲置', '', '资产闲置', '', c[9] if len(c) > 9 else '', '', '直营32家表')

CAT_ORDER = ['直营', '委管', '资产出租', '资产闲置']
rows = []
for k, v in rec.items():
    rm = v['rooms'][0] if v['rooms'] else ''
    conf = '高' if (not v['rooms'] or len(set(v['rooms'])) == 1) else '中'
    rows.append({'name': v['name'], 'cat': '/'.join(sorted(v['cat'])), 'rooms': rm, 'roomall': '、'.join(v['rooms']),
                 'conf': conf, 'mode': '、'.join(sorted(v['mode'])), 'city': '、'.join(sorted(v['city'])),
                 'status': '、'.join(sorted(v['status'])), 'term': '、'.join(sorted(v['term'])), 'src': '、'.join(sorted(v['src']))})
def sk(r):
    c0 = r['cat'].split('/')[0]
    return (CAT_ORDER.index(c0) if c0 in CAT_ORDER else 9, r['name'])
rows.sort(key=sk)
cnt = Counter()
for r in rows:
    for cc in r['cat'].split('/'): cnt[cc] += 1
cf = Counter(r['conf'] for r in rows)
print('合并去重条目: %d  | ' % len(rows) + ' '.join([k + ':' + str(v) for k, v in cnt.items()]) + '  房数一致:' + str(cf['高']) + ' 冲突:' + str(cf['中']))
print('')
print('=== 房数冲突 ===')
for r in rows:
    if r['conf'] == '中': print('   ' + r['name'][:24].ljust(24) + r['roomall'][:34].ljust(34) + r['src'][:30])
print('')
print('=== 状态/模式缺失 ===')
print('   无归属口径: ' + str(len([r for r in rows if not r['cat']])))
print('   无模式: ' + str(len([r for r in rows if not r['mode']])))
print('   无城市: ' + str(len([r for r in rows if not r['city']])))
print('   无房数: ' + str(len([r for r in rows if not r['rooms']])))
print('')
L = []
L.append('附件一　安逸集团旗下酒店摸排底册（产业发展部自摸底　2026 年 11 月 13 日）')
L.append('')
L.append('> **用途与说明**：本表是产业发展部依据集团内部五份原始名录（直营 17 家表、直营 32 家资产表、轻资产在管 43 家表、202609 在营酒店表、轻资产到期单位表）自行整理的摸排底册，**尚未经各店确认，不作为经营与考核依据**。请贵店逐条核对是否在册、是否遗漏、房数是否准确、经营状态是否属实、归属与管理模式是否正确。核对无误的勾选；不一致的在差异说明栏写明正确情况。')
L.append('')
L.append('| 序号 | 酒店名称 | 归属口径 | 管理模式 | 名录房数 | 城市与区域 | 营业状态 | 合作起止 | 数据来源 | 需核对事项 |')
L.append('|---|---|---|---|---|---|---|---|---|---|')
i = 0
for r in rows:
    i += 1
    nt = ''
    if r['conf'] == '中': nt = '房数口径冲突（' + r['roomall'] + '），请核定'
    if '/' in r['cat']: nt = (nt + '；' if nt else '') + '多口径同名，请确认归属'
    if not r['city']: nt = (nt + '；' if nt else '') + '缺城市信息'
    if '结束' in r['term']: nt = (nt + '；' if nt else '') + '合作已到期或临近到期'
    L.append('| ' + str(i) + ' | ' + r['name'] + ' | ' + r['cat'] + ' | ' + r['mode'] + ' | ' + r['rooms'] + ' | ' + r['city'] + ' | ' + r['status'] + ' | ' + r['term'] + ' | ' + r['src'] + ' | ' + nt + ' |')
L.append('')
L.append('**统计**：合并去重后共 **' + str(len(rows)) + '** 个条目，其中直营 ' + str(cnt['直营']) + '、委管 ' + str(cnt['委管']) + '、资产出租 ' + str(cnt['资产出租']) + '、资产闲置 ' + str(cnt['资产闲置']) + '；房数口径一致 ' + str(cf['高']) + ' 个、存在冲突 ' + str(cf['中']) + ' 个。')
open(OUT, 'w', encoding='utf-8').write(chr(10).join(L))
print('')
print('附件一已生成 (' + str(len(L)) + ' 行) -> ' + OUT)