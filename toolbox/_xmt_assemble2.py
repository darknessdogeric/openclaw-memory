# -*- coding: utf-8 -*-
import io, sys, os, json, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

J = r'D:\B166ER-openclaw\workspace\tmp\_xmt_data.json'
BODY = r'D:\B166ER-openclaw\workspace\tmp\_xmt_report_body.md'
OUT = r'C:\Users\ericz\Desktop\2026-10-27_安逸集团新媒体业务整体诊断报告_v1.0.md'
recs = json.load(open(J, encoding='utf-8'))
CHK = '√☑✅✓'
PDFNAME = {'总府皇冠':'总府皇冠假日','深圳四川':'深圳四川宾馆','锦著天府':'安逸·锦著天府','新良':'安逸新良大酒店'}

def pick_opt(raw, opts):
    if not raw: return '未填'
    for o in opts:
        i = raw.find(o)
        while i != -1:
            if any(c in raw[max(0,i-3):i] for c in CHK): return o
            i = raw.find(o, i+1)
    return '未填'

def num(raw):
    if not raw: return ''
    s = raw.strip()
    if '未开通' in s: return '未开通'
    m = re.search(r'粉丝[数]*[：:]?\s*\[?([0-9][0-9,\.]*)', s)
    if m: return m.group(1).rstrip(',.')
    m = re.search(r'\[([0-9][0-9,\.]*)\]', s)
    if m: return m.group(1).rstrip(',.')
    if '停更' in s: return '停更'
    if s in ('无','未开通') or s.startswith('无'): return '无'
    return ''

def hc(r):
    f = r.get('fulltime') or ''
    n = r.get('hc') or ''
    m = re.search(r'(\d+)', n)
    if m: return m.group(1) + '人'
    def pre(k):
        i = f.find(k)
        return any(c in f[max(0,i-3):i] for c in CHK) if i >= 0 else False
    if pre('是'): return '有(未填数)'
    if pre('否'): return '0人'
    return '未填'

def agency(r):
    yn = (r.get('agency_yn') or '').strip()
    name = (r.get('agency') or '').strip().replace('有限公司','').replace('科技','').replace('文化','').replace('传媒','').strip()
    fee = (r.get('fee') or '').replace('¥','').replace('_','').replace(' ','').strip()
    if not yn: return '—'
    if not name and not fee: return '无'
    s = name or '有'
    if fee: s += '／' + fee[:14]
    return s

def selfpct(r):
    m = r.get('ota_mix') or ''
    mm = re.search(r'自营[^0-9]*([0-9]+(?:\.[0-9]+)?)', m)
    return (mm.group(1) + '%') if mm else '未填'

rows = ['| 酒店 | 类型 | 管理 | 公众号 | 视频号 | 抖音 | 小红书 | 专职 | 代运营（费率） | 年预算 | 自营直销 |',
        '|---|---|---|---|---|---|---|---|---|---|---|']
for r in recs:
    if not r.get('ok'):
        nm = '未识别'
        for k, v in PDFNAME.items():
            if k in r['file']: nm = v; break
        rows.append('| ' + nm + ' 🔴 扫描件 | — | — | 无文本层 | 无文本层 | 无文本层 | 无文本层 | — | — | — | — |')
        continue
    name = (r.get('name') or r['file'])
    for pat in ['有限责任公司','有限公司','股份有限公司']:
        name = name.replace(pat,'')
    name = name.replace('管理','').replace('酒店','').strip()
    if len(name) > 14: name = name[:14]
    typ = pick_opt(r.get('type'), ['商务','度假','文化主题','公寓','其他'])
    mg = pick_opt(r.get('mgmt'), ['受托管理','自营'])
    bud = (r.get('budget') or '').replace('¥','').replace('_','').replace(' ','').strip()
    if bud in ('0',): bud = '0'
    if not bud: bud = '未填'
    rows.append('| ' + ' | '.join([name, typ, mg,
        num(r.get('wx_mp')) or '未填',
        num(r.get('wx_ch')) or '未填',
        num(r.get('dy')) or '未填',
        num(r.get('xhs')) or '未填',
        hc(r), agency(r)[:24], bud[:10], selfpct(r)]) + ' |')

ledger = chr(10).join(rows)
body = open(BODY, encoding='utf-8').read()
final = body.replace('<!--LEDGER-->', ledger)
open(OUT, 'w', encoding='utf-8').write(final)
print('台账 %d 行；最终 %d 字符' % (len(rows), len(final)))
for ln in rows:
    print(ln)