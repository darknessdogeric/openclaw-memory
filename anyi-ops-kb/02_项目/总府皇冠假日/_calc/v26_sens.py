# -*- coding: utf-8 -*-
"""v26 增量口径敏感性（A1/A2，中档 ADR × OCC 75%）"""
import io, os, sys, json, tempfile, importlib.util
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
CALC = r'D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc'
spec = importlib.util.spec_from_file_location('M26', os.path.join(CALC,'v26_model.py'))
M = importlib.util.module_from_spec(spec)
_tf = tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',suffix='.log',delete=False)
_old = sys.stdout; sys.stdout=_tf
spec.loader.exec_module(M)
sys.stdout=_old; _tf.close()
import copy
OUT = {}
for pk in ['A1','A2','A4R']:
    p = [x for x in M.PATHS if x['k']==pk][0]
    adr0 = p['mkt'][1]; occ0 = 0.75
    def inc(adr=adr0, occ=occ0, capf=1.0, du=0):
        cfs = M.inc_arm(p, adr, occ, capex=p['capex']*capf, du=p['du']+du)
        return M.npv(cfs)
    base = inc()
    rows = [
      ('ADR 上浮 10%', inc(adr=adr0*1.10)),
      ('ADR 下浮 10%', inc(adr=adr0*0.90)),
      ('开房率 +5pp', inc(occ=min(0.90,occ0+0.05))),
      ('开房率 −5pp', inc(occ=occ0-0.05)),
      ('改造投资 −20%', inc(capf=0.80)),
      ('改造投资 −10%', inc(capf=0.90)),
      ('改造投资 ＋10%', inc(capf=1.10)),
      ('改造投资 ＋20%', inc(capf=1.20)),
      ('停业期 −3 月', inc(du=-3)),
      ('停业期 ＋3 月', inc(du=3)),
    ]
    OUT[pk] = dict(base=base, rows=rows, adr=adr0, occ=occ0, cap=p['capex'], du=p['du'])
    print('=== %s %s  基准增量 NPV %+.0f 万元（中档 ADR %d × OCC %.0f%%）' % (pk, p['nm'], base, adr0, occ0*100))
    for n,v in rows: print('   %-16s %+9.0f （Δ %+9.0f）' % (n, v, v-base))
    # 组合情景：投资 −10% + 停业 −3 月
    combo = inc(capf=0.90, du=-3)
    OUT[pk]['combo'] = combo
    print('   [组合] 投资减10pct且停业减3月：%+9.0f（delta %+.0f）' % (combo, combo-base))
    print()
json.dump(OUT, open(r'D:\B166ER-openclaw\workspace\.tmp\v26c.json','w',encoding='utf-8'), ensure_ascii=False)
print('saved v26c.json')