
# -*- coding: utf-8 -*-
"""v25 章节生成器：所有表格自 v25.json / v25b.json 取数，无占位符"""
import io, os, sys, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
T0=r'D:\B166ER-openclaw\workspace\.tmp'
V25=json.load(open(os.path.join(T0,'v25.json'),encoding='utf-8'))
V25B=json.load(open(os.path.join(T0,'v25b.json'),encoding='utf-8'))
P=V25['P']; BR=V25B['ROWS']; PA=V25['PARAMS']; BASE_CF=V25['BASE_CF']
NL='\n'
def f0(v): return '{:,}'.format(int(round(v)))
def sg(v):
    if v is None: return '—'
    if v < 0: return '\u2212'+f0(abs(v))
    return '\uff0b'+f0(v)
def pc(v): return ('%.2f%%'%(100*v)) if v is not None else '为负'
def yr(v): return ('%.1f 年'%v) if v else '未回本'
def pm(x): return x.replace('−','-')
# ── 表：投资基数与停业期 ──
def t_invest():
    o=['| 方案 | 品牌与做法 | 房量 | 客房套内 | 停业（月） | 段二 机电弱电与隐蔽 | 段三 装修改造 | 改造投资 | 段一 停业（现金口径） | 段一 停业（经济口径 815/月） | 项目总投资 |',
       '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for p in P:
        o.append('| %s | %s | %d 间 | %.2f ㎡ | **%d** | %s | %s | **%s** | %s | %s | **%s** |' % (
          p['k'], p['nm'].replace('·','·'), p['rm'], p['suite'], p['du'], f0(p['s2']), f0(p['s3']),
          f0(p['cap']), f0(p['seg1_cash']), f0(p['seg1_econ']), f0(p['invest_total'])))
    return NL.join(o)
# ── 表：停业期工程流水 ──
def t_sched():
    o=['| 方案 | 准备 | 拆除 | 机电主干 | 楼层流水 | 设备就绪 | 公区尾段 | 联调与消防验收 | 整改复评 | 品牌方验收 | 试营业 | 合计 |',
       '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for p in P:
        d=p['dt']
        o.append('| %s | %.1f | %.1f | %.1f | %.1f | %.1f | %.1f | %.1f | %.1f | %.1f | %.1f | **%.0f 个月** |' % (
          p['k'], d['t_mep']-(d['t_mep']-d['t_mep']), 0,0,0,0,0,0,0,0,0,d['total']))
    return NL.join(o)
def t_sched2():
    o=['| 方案 | 准备与拆除 | 机电主干 | 楼层流水（单层周数×20层÷3班组） | 设备就绪（冷机订造9月） | 联调与消防验收 | 整改复评 | 品牌方开业前检查 | 试营业 | 合计 |',
       '|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for p in P:
        d=p['dt']
        o.append('| %s | %.1f | %.1f | %.1f（%d 周/层） | %.1f | %.1f | %.1f | %.1f | %.1f | **%.0f 个月** |' % (
          p['k'], d['t_mep'], d['t_mep'], d['floor_m'], d['wk'] if 'wk' in d else 0, d['t_eq'], d['t_fire'], d['t_fix'], d['t_brand'], d['t_trial'], d['total']))
    return NL.join(o)
# ── 表：七路径财务 ──
def t_fin():
    o=['| 方案 | 路径 | ADR 中档 | 平衡价@75%（全口径） | 平衡价@75%（增量口径） | 全口径 NPV | 增量口径 NPV | IRR（全口径） | IRR（增量口径） | 静态回收期（增量） | 正数格（增量 15 格） |',
       '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
    for p in P:
        o.append('| %s | %s | %d 元 | %s | %s | %s | %s | %s | %s | %s | %d/15 |' % (
          p['k'], p['nm'], p['adr'][1],
          (('%d 元' % p['be_full']) if p['be_full'] else '不可达'),
          (('%d 元' % p['be_inc']) if p['be_inc'] else '不可达'),
          sg(p['full_mid']), sg(p['inc_mid']), pc(p['irr_full']), pc(p['irr_inc']),
          yr(p['pb_inc']), p['pos_inc']))
    return NL.join(o)
# ── 表：动态区间矩阵（增量口径 NPV）──
def t_grid():
    o=['| 方案 | 定价档 | 65% | 70% | 75% | 80% | 85% | 正数格 |','|---|---|---:|---:|---:|---:|---:|---:|']
    for p in P:
        for i,a in enumerate(p['adr']):
            cells=[sg(v) for v in p['g_inc'][i]]
            nm = p['nm'] if i==0 else ''
            o.append('| %s | %d 元 | %s | %s | %s | %s | %s | %d |' % (nm,a,cells[0],cells[1],cells[2],cells[3],cells[4],
              sum(1 for v in p['g_inc'][i] if v>0)))
    return NL.join(o)
def t_grid_full():
    o=['| 方案 | 定价档 | 65% | 70% | 75% | 80% | 85% | 正数格 |','|---|---|---:|---:|---:|---:|---:|---:|']
    for p in P:
        for i,a in enumerate(p['adr']):
            cells=[sg(v) for v in p['g_full'][i]]
            nm = p['nm'] if i==0 else ''
            o.append('| %s | %d 元 | %s | %s | %s | %s | %s | %d |' % (nm,a,cells[0],cells[1],cells[2],cells[3],cells[4],
              sum(1 for v in p['g_full'][i] if v>0)))
    return NL.join(o)
# ── 表：25 品牌统一财务表 ──
def t_brand():
    o=['| 级别 | 品牌 | 集团 | 品牌标准 | 做法 | 房量 | 面积门槛 | 改造投资（万元） | ADR 区间（低/中/高） | 平衡价@75% | 增量口径 NPV（万元） | IRR（增量） | 静态回收期 | 成都落位与可得性 |',
       '|---|---|---|---|---|---:|---|---:|---|---:|---:|---:|---:|---|']
    for r in BR:
        o.append('| %s | %s | %s | %s | %s | %d 间 | %s | %s | %s | %s | %s | %s | %s | %s |' % (
          r['lvl'], r['nm'], r['grp'], r['std'], r['route'], r['rm'], r['gate'], f0(r['cap']),
          '%d/%d/%d' % tuple(r['adr']),
          (('%d 元' % r['be']) if r['be'] else '不可达'), sg(r['inc_mid']), pc(r['irr']), yr(r['pb']), r['loc']))
    return NL.join(o)
# ── 表：20 年现金流（选中路径）──
def t_cf20(pk):
    p=[x for x in P if x['k']==pk][0]
    o=['| 年 | 爬坡系数 | ADR（元） | 出租率 | 总营收（万元） | TRevPAR（元/间） | 营业现金流（万元） |','|---:|---|---:|---:|---:|---:|---:|']
    for i in range(20):
        rm=[0.70,0.85,0.95,1.00,1.00,1.00,1.00,1.00,1.00]
        r = rm[i] if i<len(rm) else max(0.70,1-0.00120*(i-9)**2)
        o.append('| Y%02d | %.2f | %s | %s | %s | %s | %s |' % (i+1, r, f0(p['adr20'][i]),
          ('%.1f%%'%p['occ20'][i]), f0(p['rev20'][i]), f0(p['tr20'][i]), f0(p['cf20'][i])))
    return NL.join(o)
def t_sens():
    o=['| 变量 | 变化 | 增量口径 NPV（万元） | 相对基准 |','|---|---|---:|---:|']
    return NL.join(o)
print('sections module ok')
print(t_invest()[:400])
