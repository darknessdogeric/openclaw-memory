# -*- coding: utf-8 -*-
"""v26 报告装配：数据表生成层（供 v26_asm.py 调用）"""
import io, os, sys, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
T = r'D:\B166ER-openclaw\workspace\.tmp'
VA = json.load(open(os.path.join(T,'v26a.json'), encoding='utf-8'))
VB = json.load(open(os.path.join(T,'v26b.json'), encoding='utf-8'))
P = VA['P']; RES = VA['RES']; BE = VA['BE']; CAP = VA['CAP']; THR = VA['THR']; GRID = VA['GRID']; GRID_INC = VA.get('GRID_INC', {})
M = VA['M']; PARAMS = VA['PARAMS']; MINC = VA['MIN_COMPLY']
BRS = VB['ROWS']; NL = chr(10)
def f0(v): return '{:,}'.format(int(round(v)))
def sg(v): return ('\u2212'+f0(abs(v))) if v<0 else ('\uff0b'+f0(v))
def pc(v): return ('%.2f%%'%(100*v)) if v is not None else '为负'
def yr(v): return ('%.1f 年'%v) if v else '未回本'
def res(k,lbl):
    for r in RES:
        if r['k']==k and r['lbl']==lbl: return r
    return {}
PK = [p['k'] for p in P]
PN = {p['k']:p['nm'] for p in P}
PG = {p['k']:p['grp'] for p in P}

def t_invest():
    o=['| 方案 | 路径分类 | 档次 | 品牌与做法 | 房量 | 客房套内 | 停业（月） | 段二 机电管线与隐蔽 | 段三 装修改造 | 品牌专项 | 改造投资 | 停业损失（经济口径 815/月） | 项目总投资 |',
       '|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for p in P:
        o.append('| %s | %s | %s | %s | %d 间 | %.2f ㎡ | **%d** | %s | %s | %s | **%s** | %s | **%s** |' % (
          p['k'], p['grp'], p['tier'], p['b'], p['rooms'], p['suite'], p['du'],
          f0(p['s2']), f0(p['s3']), f0(p['special']), f0(p['capex']),
          f0(p['down_loss_econ']), f0(p['capex']+p['down_loss_econ'])))
    return NL.join(o)

def t_sched():
    o=['| 方案 | 路径 | 准备＋拆除＋机电主干 | 楼层流水（周/层×20层÷3班组） | 设备就绪（冷机订造 9 月） | 联调与消防验收 | 整改复评 | 品牌方开业前检查 | 试营业 | 合计 |',
       '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for p in P:
        d=p['dt']
        o.append('| %s | %s | %.1f | %.1f（%d 周/层） | %.1f | %.1f | %.1f | %.1f | %.1f | **%.0f 个月** |' % (
          p['k'], p['nm'], d['t_mep'], d['floor_m'], d['wk'], d['t_eq'], d['t_fire'], d['t_fix'], d['t_brand'], d['t_trial'], d['total']))
    o.append('| 反事实 | 最小合规臂（仅段二） | 5.0 | 3.1（2 周/层） | 12.0 | 14.0 | 15.5 | — | 17.5 | **18 个月** |')
    return NL.join(o)

def t_fin():
    o=['| 方案 | 路径 | 档 | ADR | 全口径 NPV | 增量口径 NPV | IRR（全口径） | IRR（增量口径） | 静态回收期（增量） | 增量平衡 ADR | 增量平衡价折单位面积 | 可承受改造投资上限（增量，中档） |',
       '|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for p in P:
        for lbl, i in (('低',0),('中',1),('高',2)):
            r = res(p['k'], lbl)
            o.append('| %s | %s | %s | %d 元 | %s | %s | %s | %s | %s | %s | %s | %s |' % (
              p['k'], p['nm'], lbl, p['mkt'][i],
              sg(r['full']), sg(r['inc']), pc(r['irr']), pc(r['irr_inc']), yr(r['pb']),
              ('%d 元'%round(BE[p['k']]['be_inc'])) if BE[p['k']]['be_inc'] else '不可达',
              ('%.1f 元/㎡·夜'%(BE[p['k']]['be_inc']/p['sale'])) if BE[p['k']]['be_inc'] else '—',
              f0(CAP[p['k']]['中']['cap_inc']) if CAP[p['k']]['中']['cap_inc'] else '不可达'))
    return NL.join(o)

def t_cap():
    o=['| 方案 | 路径 | 档 | ADR | 估算改造投资 | 全口径可承受上限 | 增量口径可承受上限 | 增量缺口 | 结论 |',
       '|---|---|---|---:|---:|---:|---:|---:|---|']
    for p in P:
        for lbl in ('低','中','高'):
            c = CAP[p['k']][lbl]; r = res(p['k'], lbl)
            ci = c['cap_inc']; gap = (p['capex']-ci) if ci else None
            ok = '成立' if (ci and ci >= p['capex']) else '不成立'
            o.append('| %s | %s | %s | %d 元 | %s | %s | %s | %s | %s |' % (
              p['k'], p['nm'], lbl, p['mkt'][['低','中','高'].index(lbl)],
              f0(p['capex']), f0(c['cap_full']) if c['cap_full'] else '不可达', f0(ci) if ci else '不可达',
              f0(gap) if gap is not None else '—', ok))
    return NL.join(o)

def t_grid(key='inc'):
    src = GRID_INC if key=='inc' else GRID
    o=['| 方案 | 路径 | 定价档 | 65% | 70% | 75% | 80% | 85% | 正数格 |',
       '|---|---|---|---:|---:|---:|---:|---:|---:|']
    for p in P:
        g = src[p['k']]
        for i,(lbl,adr,row) in enumerate(g):
            o.append('| %s | %s | %s档 %d 元 | %s | %s | %s | %s | %s | %d/5 |' % (
              p['k'], p['nm'], lbl, adr,
              sg(row[0]), sg(row[1]), sg(row[2]), sg(row[3]), sg(row[4]),
              sum(1 for v in row if v>0)))
    return NL.join(o)

def t_sens():
    S = json.load(open(os.path.join(T,'v26c.json'), encoding='utf-8'))
    o=['| 变量 | A1 皇冠假日·保留体量·轻改 | A2 安逸集团自有五星 | A4R 洲至奢选·保留体量·轻改 |',
       '|---|---:|---:|---:|']
    keys = [r[0] for r in S['A1']['rows']]
    for i,k in enumerate(keys):
        cells = []
        for pk in ('A1','A2','A4R'):
            v = S[pk]['rows'][i][1]; cells.append(sg(v))
        o.append('| %s | %s | %s | %s |' % (k, cells[0], cells[1], cells[2]))
    o.append('| **基准增量 NPV** | %s | %s | %s |' % (sg(S['A1']['base']), sg(S['A2']['base']), sg(S['A4R']['base'])))
    o.append('| **组合：投资 −10%% 且停业 −3 月** | %s | %s | %s |' % (sg(S['A1']['combo']), sg(S['A2']['combo']), sg(S['A4R']['combo'])))
    return NL.join(o)

def t_thr():
    o=['| 方案 | 路径 | 平衡 ADR | 改造投资 −20% | −10% | ＋10% | ＋20% | 开房率 −5pp | ＋5pp | 停业期 −3 月 | ＋3 月 | ADR −10% | ＋10% |',
       '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for t in THR:
        if not t.get('be'): continue
        d = {r[0]: r[1] for r in t['rows']}
        p = [x for x in P if x['k']==t['k']][0]
        o.append('| %s | %s | %d 元 | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s |' % (
          t['k'], p['nm'], round(t['be']),
          sg(d.get('改造投资 −20%',0)), sg(d.get('改造投资 −10%',0)), sg(d.get('改造投资 ＋10%',0)), sg(d.get('改造投资 ＋20%',0)),
          sg(d.get('开房率 −5pp',0)), sg(d.get('开房率 ＋5pp',0)),
          sg(d.get('停业期 −3 月',0)), sg(d.get('停业期 ＋3 月',0)),
          sg(d.get('ADR −10%',0)), sg(d.get('ADR ＋10%',0))))
    return NL.join(o)

def t_brand():
    o=['| 级别 | 品牌 | 集团 | 做法 | 房量 | 面积门槛与妥协 | 改造投资（万元） | ADR 区间（低/中/高） | 增量口径 NPV（万元） | IRR（增量） | 静态回收期 | 可承受投资上限 | 成都落位与可得性 |',
       '|---|---|---|---|---:|---|---:|---|---:|---:|---:|---:|---|']
    for r in sorted(BRS, key=lambda x:(0 if x['inc']>0 else 1, -x['inc'])):
        o.append('| %s | %s | %s | %s | %d 间 | %s | %s | %s | %s | %s | %s | %s | %s |' % (
          r['lvl'], r['nm'], r['grp'], r['cfg'], r['rm'], r['gate'], f0(r['cap']),
          '%d/%d/%d'%tuple(r['adr']), sg(r['inc']), pc(r['irr']), yr(r['pb']),
          f0(r['cmax']) if r['cmax'] else '不可达', r['loc']))
    return NL.join(o)

def t_brand_detail():
    o=['| 品牌 | 档次 | 做法 | 房量 | 客房套内 | 面积门槛 | 面积妥协条件 | 停业（月） | 改造投资 | 增量口径 NPV | 增量 IRR | 静态回收期 | 可得性与商务前提 |',
       '|---|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|---|']
    for r in sorted(BRS, key=lambda x:(0 if x['inc']>0 else 1, -x['inc'])):
        o.append('| %s | %s | %s | %d 间 | %.2f ㎡ | %.1f ㎡ | %s | %d | %s | %s | %s | %s | %s |' % (
          r['nm'], r['lvl'], r['cfg'], r['rm'], r['suite'], r['thr'], r['gate'], r['du'],
          f0(r['cap']), sg(r['inc']), pc(r['irr']), yr(r['pb']), r['avail']))
    return NL.join(o)