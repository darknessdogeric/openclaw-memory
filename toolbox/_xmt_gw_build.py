# -*- coding: utf-8 -*-
import io, sys, os, json, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
J = r'D:\B166ER-openclaw\workspace\tmp\_xmt_data.json'
BODY = r'D:\B166ER-openclaw\workspace\tmp\_xmt_gw_body.md'
OUT = r'C:\Users\ericz\Desktop\2026-10-27_安逸集团新媒体业务诊断报告_公文版.md'
recs = json.load(open(J, encoding='utf-8'))
CHK = '√☑✅✓'
PDFNAME = {'总府皇冠':'总府皇冠假日','深圳四川':'深圳四川宾馆','锦著天府':'安逸锦著天府','新良':'安逸新良大酒店'}

def clean(s):
    for ch in ['✅','☑','√','✓','☐','□']:
        s = s.replace(ch, '')
    return s.strip()

def pick_opt(raw, opts):
    if not raw: return '未填'
    for o in opts:
        i = raw.find(o)
        while i != -1:
            if any(c in raw[max(0,i-3):i] for c in CHK): return o
            i = raw.find(o, i+1)
    return '未填'

def num(raw):
    if not raw: return '未填'
    s = raw.strip()
    if '未开通' in s: return '未开通'
    m = re.search(r'粉丝[数]*[：:]?\s*\[?([0-9][0-9,\.]*)', s)
    if m: return m.group(1).rstrip(',.')
    m = re.search(r'\[([0-9][0-9,\.]*)\]', s)
    if m: return m.group(1).rstrip(',.')
    if '停更' in s: return '停更'
    if s.startswith('无'): return '无'
    return '未填'

def hc(r):
    f = r.get('fulltime') or ''
    n = r.get('hc') or ''
    m = re.search(r'(\d+)', n)
    if m: return m.group(1) + ' 人'
    def pre(k):
        i = f.find(k)
        return any(c in f[max(0,i-3):i] for c in CHK) if i >= 0 else False
    if pre('是'): return '有，未填数'
    if pre('否'): return '0 人'
    return '未填'

def agency(r):
    yn = (r.get('agency_yn') or '').strip()
    name = (r.get('agency') or '').strip()
    for w in ['有限公司','有限责任公司','科技','文化','传媒']:
        name = name.replace(w,'')
    fee = (r.get('fee') or '').replace('¥','').replace('_','').replace(' ','').strip()
    if not yn: return '—'
    if not name and not fee: return '无'
    s = name or '有'
    if fee: s += '／' + fee[:12]
    return clean(s)[:20]

def sp(r):
    m = r.get('ota_mix') or ''
    mm = re.search(r'自营[^0-9]*([0-9]+(?:\.[0-9]+)?)', m)
    return (mm.group(1) + '%') if mm else '未填'

def short(r):
    nm = r.get('name') or r['file']
    for w in ['有限责任公司','有限公司','股份有限公司','管理']:
        nm = nm.replace(w,'')
    return clean(nm)[:12]

t1 = ['|酒店|公众号|视频号|抖音|小红书|', '|---|---|---|---|---|']
t2 = ['|酒店|类型|专职|代运营及费率|年预算|自营直销|', '|---|---|---|---|---|---|']
for r in recs:
    if not r.get('ok'):
        nm = '未识别'
        for k, v in PDFNAME.items():
            if k in r['file']: nm = v; break
        t1.append('|' + nm + '（扫描件）|无文本层|—|—|—|')
        t2.append('|' + nm + '（扫描件）|—|—|—|—|—|')
        continue
    nm = short(r)
    t1.append('|' + '|'.join([nm, num(r.get('wx_mp')), num(r.get('wx_ch')), num(r.get('dy')), num(r.get('xhs'))]) + '|')
    bud = (r.get('budget') or '').replace('¥','').replace('_','').replace(' ','').strip() or '未填'
    typ = pick_opt(r.get('type'), ['商务','度假','文化主题','公寓','其他'])
    t2.append('|' + '|'.join([nm, typ, hc(r), agency(r), clean(bud)[:10], sp(r)]) + '|')

body = open(BODY, encoding='utf-8').read()
final = body.replace('<!--T1-->', chr(10).join(t1)).replace('<!--T2-->', chr(10).join(t2))
SYM = ['🟢','🟡','🟠','🔴','✅','☑','√','✓','☐','□','★','☆']
hit = [x for x in SYM if x in final]
print('符号残留（正文）: ' + (','.join(hit) if hit else '无'))
open(OUT, 'w', encoding='utf-8').write(final)
print('合计 %d 字符  T1 %d 行  T2 %d 行' % (len(final), len(t1), len(t2)))
print('抽查附件二前 4 行:')
for ln in t2[:4]:
    print('  ' + ln)