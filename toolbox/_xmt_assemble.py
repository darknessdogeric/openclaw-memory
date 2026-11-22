# -*- coding: utf-8 -*-
import io, sys, os, json, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

J = r'D:\B166ER-openclaw\workspace\tmp\_xmt_data.json'
BODY = r'D:\B166ER-openclaw\workspace\tmp\_xmt_report_body.md'
OUT = r'C:\Users\ericz\Desktop\2026-10-27_安逸集团新媒体业务整体诊断报告_v1.0.md'

recs = json.load(open(J, encoding='utf-8'))
CHK = '√☑✅✓'

def pick_opt(raw, opts):
    if not raw:
        return '未填'
    for o in opts:
        i = raw.find(o)
        while i != -1:
            pre = raw[max(0, i-3):i]
            if any(c in pre for c in CHK):
                return o
            i = raw.find(o, i+1)
    return '未填'

def num(raw):
    if not raw:
        return ''
    m = re.search(r'粉丝[数]*[：:]?\s*\[?([0-9][0-9,\.]*)', raw)
    if m:
        return m.group(1)
    m = re.search(r'\[([0-9][0-9,\.]*)\]', raw)
    if m:
        return m.group(1)
    if re.search(r'停更', raw):
        return '停更'
    if re.search(r'未开通|无$|^无', raw.strip()):
        return '无'
    return ''

def hc(r):
    f = (r.get('fulltime') or '')
    n = (r.get('hc') or '')
    m = re.search(r'(\d+)', n)
    if m:
        v = int(m.group(1))
        return str(v) + ('人' if v else '0人')
    if ('否' in f) and not any(c in f.split('否')[0] for c in CHK):
        return '0人'
    if any(c in f for c in CHK):
        return '未填'
    return '未填'

def agency(r):
    if not (r.get('agency_yn') or '').strip():
        return '—'
    yn = r.get('agency_yn') or ''
    has = any(c in yn.split('是')[0] for c in CHK) if '是' in yn else False
    name = (r.get('agency') or '').strip()
    fee = (r.get('fee') or '').replace('¥','').replace('_','').strip()
    if not name and not fee:
        return '无'
    s = name.replace('有限公司','').replace('科技','').strip() or '有'
    if fee:
        s += '／' + fee[:16]
    return s or '有'

def selfpct(r):
    m = (r.get('ota_mix') or '')
    mm = re.search(r'自营[^0-9]*([0-9]+)', m)
    if mm:
        return mm.group(1) + '%'
    return '未填'

rows = []
rows.append('| 酒店 | 类型 | 管理 | 公众号 | 视频号 | 抖音 | 小红书 | 专职 | 代运营（费率） | 年预算 | 自营直销 |')
rows.append('|---|---|---|---|---|---|---|---|---|---|---|')
for r in recs:
    if not r.get('ok'):
        nm = r['file'].replace('.pdf','').replace('.PDF','')
        nm = re.sub(r'^集团与56家酒店账号现状[（(]|[）)]$', '', nm)
        nm = re.sub(r'^集团旗下酒店新媒体账号采集表-', '', nm)
        rows.append('| ' + nm[:16] + ' | 未读 | 未读 | 无文本层 | 无文本层 | 无文本层 | 无文本层 | 未读 | 未读 | 未读 | 未读 |')
        continue
    name = (r.get('name') or r['file']).replace('有限责任公司','').replace('有限公司','').replace('管理','').strip()
    name = name[:16]
    typ = pick_opt(r.get('type'), ['商务','度假','文化主题','公寓','其他'])
    mg = pick_opt(r.get('mgmt'), ['自营','受托管理'])
    gz = num(r.get('wx_mp')) or '未填'
    sp = num(r.get('wx_ch')) or '未填'
    dy = num(r.get('dy')) or '未填'
    xhs = num(r.get('xhs')) or '未填'
    bud = (r.get('budget') or '').replace('¥','').replace('_','').replace(' ','').strip() or '未填'
    rows.append('| ' + ' | '.join([name, typ, mg, gz, sp, dy, xhs, hc(r), agency(r)[:26], bud[:12], selfpct(r)]) + ' |')

ledger = chr(10).join(rows)
body = open(BODY, encoding='utf-8').read()
final = body.replace('<!--LEDGER-->', ledger)
open(OUT, 'w', encoding='utf-8').write(final)
print('台账行数 %d (含表头2行)' % len(rows))
print('最终 %d 字符 -> %s' % (len(final), OUT))
print()
print(ledger[:2400])