# -*- coding: utf-8 -*-
"""v25 装配脚本（结构化编号定位，不依赖中文字面）"""
import io, os, sys, json, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
CALC=r'D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc'
KB=r'D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日'
sys.path.insert(0,CALC)
import importlib.util
def _load(n,p):
    sp=importlib.util.spec_from_file_location(n,p); m=importlib.util.module_from_spec(sp); sp.loader.exec_module(m); return m
T1=_load('t1',os.path.join(CALC,'_t1.py')); T2=_load('t2',os.path.join(CALC,'_t2.py'))
T3=_load('t3',os.path.join(CALC,'_t3.py')); T4=_load('t4',os.path.join(CALC,'_t4.py'))
T5=_load('t5',os.path.join(CALC,'_t5.py')); T6=_load('t6',os.path.join(CALC,'_t6.py'))
V25=json.load(open(r'D:\B166ER-openclaw\workspace\.tmp\v25.json',encoding='utf-8'))
V25B=json.load(open(r'D:\B166ER-openclaw\workspace\.tmp\v25b.json',encoding='utf-8'))
P=V25['P']; BRS=V25B['ROWS']; NL='\n'
def f0(v): return '{:,}'.format(int(round(v)))
def sg(v): return ('\u2212'+f0(abs(v))) if v<0 else ('\uff0b'+f0(v))
def pc(v): return ('%.2f%%'%(100*v)) if v is not None else '为负'
def yr(v): return ('%.1f 年'%v) if v else '未回本'
WK={'P1':4,'P2':6,'P3':8,'P4':4,'P5':9,'P6':9,'P7':11}
def t_invest():
    o=['| 方案 | 品牌与做法 | 房量 | 客房套内 | 停业（月） | 段二 机电弱电与隐蔽 | 段三 装修改造 | 改造投资 | 段一 停业（现金口径） | 段一 停业（经济口径 815/月） | 项目总投资 |',
       '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for p in P:
        o.append('| %s | %s | %d 间 | %.2f ㎡ | **%d** | %s | %s | **%s** | %s | %s | **%s** |' % (
          p['k'],p['nm'],p['rm'],p['suite'],p['du'],f0(p['s2']),f0(p['s3']),f0(p['cap']),
          f0(p['seg1_cash']),f0(p['seg1_econ']),f0(p['invest_total'])))
    return NL.join(o)
def t_sched():
    o=['| 方案 | 路径 | 准备与拆除 | 机电主干 | 楼层流水（单层周数×20层÷3班组） | 设备就绪（冷机订造9月） | 联调与消防验收 | 整改复评 | 品牌方开业前检查 | 试营业 | 合计 |',
       '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for p in P:
        d=p['dt']
        o.append('| %s | %s | %.1f | %.1f | %.1f（%d 周/层） | %.1f | %.1f | %.1f | %.1f | %.1f | **%.0f 个月** |' % (
          p['k'],p['nm'],d['t_mep'],d['t_mep'],d['floor_m'],WK[p['k']],d['t_eq'],d['t_fire'],d['t_fix'],d['t_brand'],d['t_trial'],d['total']))
    return NL.join(o)
def t_fin():
    o=['| 方案 | 路径 | ADR 中档 | 平衡价@75%（全口径） | 平衡价@75%（增量口径） | 全口径 NPV | 增量口径 NPV | IRR（全口径） | IRR（增量口径） | 静态回收期（增量） | 正数格（增量 15 格） |',
       '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for p in P:
        o.append('| %s | %s | %d 元 | %s | %s | %s | %s | %s | %s | %s | %d/15 |' % (
          p['k'],p['nm'],p['adr'][1],
          (('%d 元'%p['be_full']) if p['be_full'] else '不可达'),
          (('%d 元'%p['be_inc']) if p['be_inc'] else '不可达'),
          sg(p['full_mid']),sg(p['inc_mid']),pc(p['irr_full']),pc(p['irr_inc']),yr(p['pb_inc']),p['pos_inc']))
    return NL.join(o)
def t_grid(key):
    o=['| 方案 | 定价档 | 65% | 70% | 75% | 80% | 85% | 正数格 |','|---|---|---:|---:|---:|---:|---:|---:|']
    for p in P:
        for i,a in enumerate(p['adr']):
            row=p[key][i]; nm=p['nm'] if i==0 else ''
            o.append('| %s | %d 元 | %s | %s | %s | %s | %s | %d |' % (nm,a,sg(row[0]),sg(row[1]),sg(row[2]),sg(row[3]),sg(row[4]),
              sum(1 for v in row if v>0)))
    return NL.join(o)
def t_brand():
    o=['| 级别 | 品牌 | 集团 | 品牌标准 | 做法 | 房量 | 面积门槛 | 改造投资（万元） | ADR 区间（低/中/高） | 平衡价@75% | 增量口径 NPV（万元） | IRR（增量） | 静态回收期 | 成都落位与可得性 |',
       '|---|---|---|---|---|---:|---|---:|---|---:|---:|---:|---:|---|']
    for r in BRS:
        o.append('| %s | %s | %s | %s | %s | %d 间 | %s | %s | %s | %s | %s | %s | %s | %s |' % (
          r['lvl'],r['nm'],r['grp'],r['std'],r['route'],r['rm'],r['gate'],f0(r['cap']),
          '%d/%d/%d'%tuple(r['adr']),('%d 元'%r['be']) if r['be'] else '不可达',
          sg(r['inc_mid']),pc(r['irr']),yr(r['pb']),r['loc']))
    return NL.join(o)
SRC=os.path.join(KB,'总府皇冠改造_可行性研究报告_v23.0_2026-11-16.md')
T=io.open(SRC,encoding='utf-8').read()
def hkey(line):
    m=re.match(r'^(#{1,6})\s*([0-9]+(?:\.[0-9]+)*)\.?\s', line+' ')
    return (len(m.group(1)), m.group(2)) if m else None
def find_title(lines, word, after=0):
    for i in range(after,len(lines)):
        if lines[i].startswith('#') and word in lines[i]: return i
    return -1
def block_bounds(lines, start_key, end_key=None, title=None, title_end=None):
    si=-1
    if title is not None:
        si=find_title(lines,title)
    else:
        for i,l in enumerate(lines):
            if hkey(l)==start_key: si=i; break
    if si<0: return None
    if end_key is not None:
        for j in range(si+1,len(lines)):
            if hkey(lines[j])==end_key: return si,j
        return None
    if title_end is not None:
        for j in range(si+1,len(lines)):
            if lines[j].startswith('#') and title_end in lines[j]: return si,j
        return None
    lvl=len(lines[si].split(' ')[0])
    for j in range(si+1,len(lines)):
        if lines[j].startswith('#'):
            l2=len(lines[j].split(' ')[0])
            if l2<=lvl: return si,j
    return si,len(lines)
JOBS=[
 (dict(title='结论摘要'), T1.CONC),
 (dict(start_key=(1,'1')), T2.CHAPTER1),
 (dict(start_key=(1,'2')), T3.CH2),
 (dict(start_key=(2,'4.2'), end_key=(3,'4.2.2')), T5.OTA_PATCH),
 (dict(start_key=(2,'5.1'), end_key=(1,'6')), T5.CH5INTRO+t_brand()+NL+NL+T6.CH52),
 (dict(start_key=(1,'6'), end_key=(1,'7')), T3.CH6),
 (dict(start_key=(1,'7'), end_key=(1,'8')), T4.CH7),
 (dict(start_key=(1,'8'), end_key=(1,'9')), T4.CH8),
 (dict(start_key=(1,'16')), T5.CH16),
]
lines=T.split(NL)
ok=0; fail=[]
for spec,new in JOBS:
    kw={k:v for k,v in spec.items() if k!='start_key' and k!='end_key' and k!='title'}
    b=block_bounds(lines, spec.get('start_key'), spec.get('end_key'), spec.get('title'), kw.get('title_end'))
    if b is None:
        fail.append(str(spec)); continue
    si,ei=b
    lines=lines[:si]+new.split(NL)+lines[ei:]
    ok+=1
T=NL.join(lines)
T=T.replace('{{T_INVEST}}',t_invest()).replace('{{T_SCHED}}',t_sched()).replace('{{T_FIN}}',t_fin())
T=T.replace('{{T_GRID_INC}}',t_grid('g_inc')).replace('{{T_GRID_FULL}}',t_grid('g_full'))
T=re.sub(r'v23\.0','v25.0',T)
OUT=os.path.join(KB,'总府皇冠改造_可行性研究报告_v25.0_2026-11-16.md')
io.open(OUT,'w',encoding='utf-8').write(T)
print('replaced', ok, 'failed', fail)
print('written', OUT, len(T))
print('placeholders left:', sorted(set(re.findall(r'\{\{[^}]+\}\}',T))))
