# -*- coding: utf-8 -*-
import io, sys, os, json, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn
D = r'C:\Users\ericz\Desktop\产业发展部\新媒体业务\下属酒店新媒体现状采集'
OUTJ = r'D:\B166ER-openclaw\workspace\tmp\_xmt_data.json'

def rows(p):
    d = Document(p)
    pm = {x._p: x for x in d.paragraphs}
    tm = {x._tbl: x for x in d.tables}
    out = []
    for ch in d.element.body.iterchildren():
        if ch.tag == qn('w:p'):
            x = pm.get(ch)
            if x is not None and x.text.strip():
                out.append(x.text.strip())
        elif ch.tag == qn('w:tbl'):
            t = tm.get(ch)
            if t is not None:
                for r in t.rows:
                    cs = [c.text.strip().replace(chr(10),' ') for c in r.cells]
                    out.append('|' + '|'.join(cs) + '|')
    return out

def cells(line):
    s = line.strip()
    if not (s.startswith('|') and s.endswith('|')):
        return None
    return [c.strip() for c in s[1:-1].split('|')]

def pick(lines, kw, col=3):
    for ln in lines:
        cs = cells(ln)
        if cs and len(cs) > col and kw in cs[1]:
            return cs[col]
    return ''

recs = []
for f in sorted(os.listdir(D)):
    p = os.path.join(D, f)
    if not os.path.isfile(p):
        continue
    ext = os.path.splitext(f)[1].lower()
    if ext != '.docx':
        recs.append({'file': f, 'ok': False, 'note': 'PDF扫描件/无文本层'})
        continue
    L = rows(p)
    r = {'file': f, 'ok': True}
    r['name'] = pick(L, '酒店全称')
    r['type'] = pick(L, '酒店类型')
    r['mgmt'] = pick(L, '管理类型')
    r['addr'] = pick(L, '详细地址')
    r['wx_mp'] = pick(L, '微信公众号')
    r['wx_ch'] = pick(L, '微信视频号')
    r['dy'] = pick(L, '抖音')
    r['xhs'] = pick(L, '小红书')
    r['wb'] = pick(L, '微博')
    r['bili'] = pick(L, 'B 站')
    r['site'] = pick(L, '官网')
    r['mini'] = pick(L, '微信小程序')
    r['ota'] = pick(L, '携程 / 美团商家版')
    r['other'] = pick(L, '其他平台')
    r['fulltime'] = pick(L, '是否有专职新媒体运营人员')
    r['hc'] = pick(L, '专职运营人数')
    r['pt'] = pick(L, '兼职')
    r['cap'] = pick(L, '运营团队设计')
    r['agency_yn'] = pick(L, '是否有第三方代运营')
    r['agency'] = pick(L, '代运营公司全称')
    r['term'] = pick(L, '合同期限')
    r['fee'] = pick(L, '年费金额')
    r['svc'] = pick(L, '服务内容')
    r['renew'] = pick(L, '续约计划')
    r['ctype'] = pick(L, '常发布内容类型')
    r['best'] = pick(L, '过去 6 个月最高传播内容')
    r['ip'] = pick(L, '酒店专属 IP')
    r['group_act'] = pick(L, '是否参与过集团统一营销活动')
    r['anyi_mem'] = pick(L, '是否使用集团会员体系')
    r['ota_mix'] = pick(L, '主要 OTA 渠道占比')
    r['budget'] = pick(L, '酒店年度新媒体预算')
    recs.append(r)

os.makedirs(os.path.dirname(OUTJ), exist_ok=True)
open(OUTJ, 'w', encoding='utf-8').write(json.dumps(recs, ensure_ascii=False, indent=1))
print('RECORDS %d  (docx %d / 无文本 %d)' % (len(recs), sum(1 for x in recs if x.get('ok')), sum(1 for x in recs if not x.get('ok'))))
print()
for r in recs:
    if not r.get('ok'):
        print('[X] ' + r['file'][:60] + '  -> ' + r['note'])
        continue
    print('[' + r['name'][:22] + ']  ' + r['file'][:26])
    print('   类型:' + r['type'][:26] + ' | 管理:' + r['mgmt'][:14])
    print('   公众号:' + r['wx_mp'][:70])
    print('   视频号:' + r['wx_ch'][:50] + ' | 抖音:' + r['dy'][:60])
    print('   小红书:' + r['xhs'][:50])
    print('   专职:' + r['fulltime'][:10] + ' 人数:' + r['hc'][:6] + ' 能力:' + r['cap'][:14])
    print('   代运营:' + r['agency_yn'][:8] + ' ' + r['agency'][:26] + ' 费:' + r['fee'][:14] + ' 续约:' + r['renew'][:10])
    print('   内容:' + r['ctype'][:40] + ' | 集团活动:' + r['group_act'][:8] + ' 安逸会:' + r['anyi_mem'][:8])
    print('   OTA:' + r['ota_mix'][:60] + ' | 预算:' + r['budget'][:16])
    print()