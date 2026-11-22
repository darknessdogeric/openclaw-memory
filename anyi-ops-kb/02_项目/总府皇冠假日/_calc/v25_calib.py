
# -*- coding: utf-8 -*-
import io, sys, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
_KEEP=sys.stdout
CALC=r'D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc'
for p in (CALC, r'D:\B166ER-openclaw\workspace\toolbox'):
    if p not in sys.path: sys.path.insert(0,p)
import hotel_irr_calc_zongfu_v2 as Z
# ---------- A. 档案引擎原始预设（10 年 / 20 年）----------
TRANS={'d1a':dict(transition_drag_pct=0.12,transition_years=2,transition_extra_cost_annual=400.0,transition_oneoff=1200.0),
 'd1b':dict(transition_drag_pct=0.12,transition_years=2,transition_extra_cost_annual=400.0,transition_oneoff=1200.0),
 'd2':dict(transition_drag_pct=0.20,transition_years=2,transition_extra_cost_annual=550.0,transition_oneoff=1800.0),
 'd3':dict(transition_drag_pct=0.25,transition_years=2,transition_extra_cost_annual=700.0,transition_oneoff=2200.0)}
def run_preset(H):
    P=Z.build_presets(); out={}
    for k,p in P.items():
        key=k.rsplit('_',1)[0]; q=dict(p); q.update(TRANS.get(key,{}))
        q['horizon']=H; q['baseline']=dict(p['baseline']); q['baseline']['horizon']=H
        out[k]=Z.calc_zongfu2(q)
    return out
for H in (10,20):
    res=run_preset(H)
    print('=== 档案引擎预设 · %d 年 · 中性情景 ===' % H)
    print('%-26s %4s %6s %9s %9s %8s %8s %9s %11s %9s' % ('方案','房','ADR','总营收','GOP率','品牌费率','业主GOP','年均CF','增量NPV','增量IRR'))
    for key,name,tier,rooms,adr,occ,clm,inv,fo in Z.PATHS:
        r=res[key+'_中性']; y=r['yearly'][1]; i=r['inc']
        ii=i.get('inc_irr')
        print('%-26s %4d %6.0f %9.0f %8.1f %8.1f %9.0f %9.0f %11.0f %9s' % (name,rooms,adr,
          y['total_revenue'],y['gop_rate'],y['brand_fee_rate'],y['gop_net'],
          i['post_annual_cf'],i['inc_npv'], ('%.2f%%'%(ii*100)) if ii else '不存在'))
    b=res['d2_中性']['inc']
    print('  基线：年均CF %.0f 万｜总营收 %.0f 万｜业主GOP率 %.1f%%｜品牌费率 %.1f%%｜closure_loss %.0f 万' % (
      b['base_annual_cf'],b['base_total_rev'],b['base_gop_net_rate'],b['base_brand_fee_rate'],
      res['d2_中性']['closure_loss']))
    print()
# ---------- B. 我的 P1 vs 档案 d1b 逐年拆解 ----------
def dump(res,name):
    y=res['yearly']
    print('  %s：' % name)
    for yr in (1,2,5,10,20):
        if yr<=len(y):
            x=y[yr-1]
            print('    Y%02d ADR%6.0f OCC%5.1f 客房%8.0f 总营收%8.0f GOP率%5.1f 品牌费%7.0f 业主GOP%8.0f 折旧%7.0f 税%6.0f CF%8.0f TRevPAR%6.0f' % (
              yr,x['adr'],x['occ'],x['room_revenue'],x['total_revenue'],x['gop_rate'],x['brand_fees'],
              x['gop_net'],x['depreciation'],x['tax'],x['cash_flow'],x['trevpar']))
print('=== 逐年拆解对比（20 年）===')
P=Z.build_presets()
q=dict(P['d1b_中性']); q.update(TRANS['d1b']); q['horizon']=20
q['baseline']=dict(q['baseline']); q['baseline']['horizon']=20
dump(Z.calc_zongfu2(q),'档案 d1b（402间 ADR620 OCC73% 投资18,400 停业15月 债务1,785）')
# 我的 P1 同参对照
my=dict(Z.BASELINE)
my.update(project_name='P1',scenario='x',tier_params='intl_current_crowne',rooms=402,
  peak_adr=500.0,peak_occ=0.75,total_invest=21034.0,include_new_dep=True,
  building_value_existing=21949.0,electromechanical_value=8790.0,labor_in_gop=True,
  labor_cost_annual=2023.0,debt_service_annual=0.0,rent_annual=0,discount_rate=0.08,
  tax_rate=0.25,horizon=20,ramp_type='renovation',closure_months=0,closure_loss_monthly=0,
  transition_drag_pct=0.12,transition_years=2,transition_extra_cost_annual=400.0,
  transition_oneoff=0.0,gop_measured_rate=None)
dump(Z.calc_zongfu2(my),'我的 P1（402间 ADR500 OCC75% 投资21,034 无债务）')
# 同参数对照：只差债务与ADR
for lbl,adr,debt in (('ADR620+债务1785 (=d1b)',620.0,1785.0),('ADR620+无债务',620.0,0.0),
                     ('ADR500+债务1785',500.0,1785.0),('ADR500+无债务',500.0,0.0)):
    m=dict(my); m['peak_adr']=adr; m['debt_service_annual']=debt
    r=Z.calc_zongfu2(m); y=r['yearly']
    print('  %-22s 总营收%8.0f GOP率%5.1f 品牌费%7.0f 业主GOP%8.0f CF(Y1/Y5/Y20)=%7.0f/%7.0f/%7.0f' % (
      lbl,y[1]['total_revenue'],y[1]['gop_rate'],y[1]['brand_fees'],y[1]['gop_net'],
      y[0]['cash_flow'],y[4]['cash_flow'],y[19]['cash_flow']))
