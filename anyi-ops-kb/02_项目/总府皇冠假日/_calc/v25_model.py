
# -*- coding: utf-8 -*-
"""v25 模型定稿（修正增量口径时间轴对齐 + 25 品牌统一财务表）
★ 关键修正：增量口径必须同窗口对齐——项目臂 W＝停业月数＋240 个月，
  反事实基线（不改造持续失血）须在同一 W 个月内逐月计入，否则停业期损失的
  经营现金流被漏计（这正是旧版"投资基数不对"的根源）。
"""
import io, sys, os, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
_KEEP=sys.stdout
CALC=r'D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc'
for p in (CALC, r'D:\B166ER-openclaw\workspace\toolbox'):
    if p not in sys.path: sys.path.insert(0,p)
import hotel_irr_calc_zongfu_v2 as Z
E=sys.modules['hotel_irr_calc']
RA=0.08; RM=(1+RA)**(1/12.0)-1; OP_Y=20; OP_M=240
REV_LOSS_M=564.5; RIGID_ALL=250.5; INT_M=143.67; RIGID_PROJ=162.5
BRAND_KEEP_M=round(292.8/18.0,2); SEG1_ALL=REV_LOSS_M+RIGID_ALL
S2_NO_CUT,S2_CUT=8790.0,9330.0; BRAND_SPECIAL=1990.0; FURN=540.0
A39={('皇冠','保留','不减房'):(402,25.35,10253.6),('皇冠','保留','3改2'):(268,48.0,9688.0),
 ('皇冠','重做','不减房'):(402,25.35,18111.3),('洲至奢选','保留','不减房'):(402,25.35,17130.7),
 ('洲至奢选','重做','3改2'):(268,48.0,32781.3),('外部奢牌','重做','3改2'):(268,48.0,45250.9),
 ('外部奢牌','重做','不减房'):(402,25.35,39216.7)}
UNIT={('皇冠','保留'):5800,('皇冠','重做'):9600,('洲至奢选','保留'):9400,
 ('洲至奢选','重做'):15000,('外部奢牌','重做'):20900}
PUB={('皇冠','保留'):3554.7,('皇冠','重做'):6783.1,('洲至奢选','保留'):5585.9,
 ('洲至奢选','重做'):10200.7,('外部奢牌','重做'):12923.2}
CONT={'皇冠':0.055,'洲至奢选':0.0675,'外部奢牌':0.08}
CFG={'不减房':dict(rm=402,suite=25.35,ab=25.35,sale=30.57),
     '3改2':dict(rm=268,suite=38.03,ab=48.0,sale=45.85),
     '2改1':dict(rm=201,suite=50.71,ab=60.9,sale=61.15),
     '全套房':dict(rm=162,suite=63.0,ab=78.75,sale=75.95)}
FL,CREW,WK_M,CH_LEAD,CH_INS=20,3,4.345,9.0,3.0
SCHED={('皇冠','保留','不减房'):dict(prep=1.0,demo=2.0,mep=4.0,wk=4,comm=5.0,bp=0.0),
 ('皇冠','重做','不减房'):dict(prep=1.0,demo=2.5,mep=4.5,wk=6,comm=6.0,bp=0.0),
 ('皇冠','保留','3改2'):dict(prep=1.0,demo=3.0,mep=4.0,wk=8,comm=6.5,bp=0.0),
 ('洲至奢选','保留','不减房'):dict(prep=1.0,demo=2.0,mep=4.0,wk=4,comm=5.0,bp=1.0),
 ('洲至奢选','重做','2改1'):dict(prep=1.0,demo=3.5,mep=4.5,wk=9,comm=7.0,bp=1.0),
 ('外部奢牌','重做','2改1'):dict(prep=1.0,demo=3.5,mep=4.5,wk=9,comm=7.0,bp=1.0),
 ('外部奢牌','重做','全套房'):dict(prep=1.0,demo=4.0,mep=5.0,wk=11,comm=8.0,bp=1.0)}
def downtime(k):
    if isinstance(k,str): k=tuple(k.split('·'))
    s=SCHED[k]; fm=s['wk']*FL/CREW/WK_M
    t_mep=s['prep']+s['demo']+s['mep']; t_fl=t_mep+fm
    t_eq=max(t_fl,CH_LEAD+CH_INS); t_pub=t_mep+s['comm']
    t_cm=max(t_eq,t_pub); t_fire=t_cm+2.0; t_fix=t_fire+1.5
    t_br=t_fix+s['bp']+1.0; t_tr=t_br+1.0
    return dict(total=t_tr,floor_m=round(fm,1),t_mep=round(t_mep,1),t_floor=round(t_fl,1),
      t_eq=round(t_eq,1),t_pub=round(t_pub,1),t_comm=round(t_cm,1),t_fire=round(t_fire,1),
      t_fix=round(t_fix,1),t_brand=round(t_br,1),t_trial=round(t_tr,1))
TRANS={('皇冠','保留'):dict(drag=0.12,dy=2,extra=400.0,oneoff=1200.0),
 ('皇冠','重做'):dict(drag=0.14,dy=2,extra=450.0,oneoff=1400.0),
 ('洲至奢选','保留'):dict(drag=0.18,dy=2,extra=520.0,oneoff=1700.0),
 ('洲至奢选','重做'):dict(drag=0.20,dy=2,extra=550.0,oneoff=1800.0),
 ('外部奢牌','重做'):dict(drag=0.25,dy=2,extra=700.0,oneoff=2200.0)}
PSQM={('皇冠','保留','不减房'):(14.5,16.0,17.5),
      ('皇冠','重做','不减房'):(15.5,17.0,18.5),
      ('皇冠','保留','3改2'):(14.5,16.0,17.5),
      ('洲至奢选','保留','不减房'):(16.0,17.8,19.5),
      ('洲至奢选','重做','2改1'):(17.0,19.0,21.0),
      ('外部奢牌','重做','2改1'):(23.0,27.0,31.0),
      ('外部奢牌','重做','全套房'):(23.0,27.0,31.0)}
TIER={('皇冠','保留'):'intl_current_crowne',('皇冠','重做'):'intl_current_crowne',
 ('洲至奢选','保留'):'intl_upper_upscale',('洲至奢选','重做'):'intl_upper_upscale',
 ('外部奢牌','重做'):'intl_luxury'}
THR={'皇冠':35.0,'洲至奢选':40.0,'外部奢牌':45.0}
OCC=[0.65,0.70,0.75,0.80,0.85]
def seg3(b,m,cfg):
    c=CFG[cfg]; room=c['rm']*c['ab']*UNIT[(b,m)]/1e4; pub=PUB[(b,m)]
    cont=(room+pub)*CONT[b]; key=(b,m,cfg)
    if key in A39:
        ar,aa,av=A39[key]; s3=av+(c['rm']*c['ab']-ar*aa)*UNIT[(b,m)]/1e4; src='039 锚点＋面积差额'
    else:
        # 以同品牌最近锚点反推「公区＋不可预见费＋家具」固定部分，再按面积差调整
        cand=[(k,v) for k,v in A39.items() if k[0]==b and k[1]==m] or [(k,v) for k,v in A39.items() if k[0]==b]
        kk,vv=max(cand,key=lambda kv:kv[1][0]); ar,aa,av=vv
        room_a=ar*aa*UNIT[(b,m)]/1e4
        fixed=av-room_a
        s3=room+fixed; src='039 锚点反推公区＋面积差额'
    return dict(room=round(room,1),pub=round(pub,1),cont=round(cont,1),
                s3=round(s3+BRAND_SPECIAL,1),s3_base=round(s3,1),src=src)
def mkpath(k,nm,b,m,cfg,sched_key):
    c=CFG[cfg]; dt=downtime(sched_key); s3=seg3(b,m,cfg)
    s2=S2_CUT if cfg!='不减房' else S2_NO_CUT; du=int(round(dt['total']))
    rigid=round(RIGID_PROJ+(BRAND_KEEP_M if b!='皇冠' else 0.0),2)
    return dict(k=k,nm=nm,b=b,m=m,cfg=cfg,rm=c['rm'],suite=c['suite'],sale=c['sale'],
      s2=s2,s3=s3['s3'],s3b=s3,cap=round(s2+s3['s3'],1),du=du,dt=dt,rigid=rigid,
      seg1_cash=round(rigid*du,1),
      seg1_econ=round((SEG1_ALL+(BRAND_KEEP_M if b!='皇冠' else 0.0))*du,1),
      thr=THR[b],tier=TIER[(b,m)],psqm=PSQM[(b,m,cfg)],trans=TRANS[(b,m)],
      adr=[int(round(x*c['sale'])) for x in PSQM[(b,m,cfg)]])
DEF=[('P1','皇冠假日·保留·不减房','皇冠','保留','不减房','皇冠·保留·不减房'),
 ('P2','皇冠假日·重做·不减房','皇冠','重做','不减房','皇冠·重做·不减房'),
 ('P3','皇冠假日·保留·3改2','皇冠','保留','3改2','皇冠·保留·3改2'),
 ('P4','洲至奢选·保留·不减房','洲至奢选','保留','不减房','洲至奢选·保留·不减房'),
 ('P5','洲至奢选·重做·2改1','洲至奢选','重做','2改1','洲至奢选·重做·2改1'),
 ('P6','外部奢牌·重做·2改1','外部奢牌','重做','2改1','外部奢牌·重做·2改1'),
 ('P7','外部奢牌·重做·全套房','外部奢牌','重做','全套房','外部奢牌·重做·全套房')]
PATHS=[mkpath(*d) for d in DEF]
for p in PATHS:
    p['gate']='达标' if p['suite']>=p['thr'] else '差%.1f㎡'%(p['thr']-p['suite'])
    p['invest_total']=round(p['cap']+p['seg1_econ'],1)
def engine(p,adr,occ,capex=None):
    q=dict(Z.BASELINE)
    q.update(project_name=p['nm'],scenario='测算',tier_params=p['tier'],rooms=p['rm'],
      peak_adr=float(adr),peak_occ=float(occ),total_invest=(p['cap'] if capex is None else capex),
      include_new_dep=True,building_value_existing=21949.0,electromechanical_value=p['s2'],
      labor_in_gop=True,labor_cost_annual=2023.0,debt_service_annual=0.0,rent_annual=0,
      discount_rate=RA,tax_rate=0.25,horizon=OP_Y,ramp_type='renovation',closure_months=0,
      closure_loss_monthly=0,transition_drag_pct=p['trans']['drag'],transition_years=p['trans']['dy'],
      transition_extra_cost_annual=p['trans']['extra'],transition_oneoff=0.0,gop_measured_rate=None)
    return Z.calc_zongfu2(q)
BASE=dict(Z.BASELINE)
BASE.update(debt_service_annual=0.0,horizon=OP_Y,include_new_dep=False,gop_measured_rate=0.0974,
  total_invest=0,closure_months=0,closure_loss_monthly=0)
BASE_CF=[y['cash_flow'] for y in Z.calc_zongfu2(dict(BASE))['yearly']]
def base_monthly(months, degrade=0.0):
    """反事实基线：不改造、继续经营，逐月计入同一窗口"""
    out=[]
    for m in range(1,months+1):
        y=min((m-1)//12, OP_Y-1)
        f=BASE_CF[y]*((1-degrade)**y)
        out.append((m,f/12.0))
    return out
def project_monthly(p,adr,occ,capex=None,du=None):
    du=du or p['du']; capex=p['cap'] if capex is None else capex
    op=[y['cash_flow'] for y in engine(p,adr,occ,capex)['yearly']]
    cfs=[]; capm=capex/du
    for m in range(1,du+1): cfs.append((m,-capm-p['rigid']))
    for y in range(OP_Y):
        for k in range(12):
            v=op[y]/12.0
            if y==0 and k==0: v-=p['trans']['oneoff']/12.0
            cfs.append((du+y*12+k+1,v))
    return cfs
def inc_monthly(p,adr,occ,capex=None,du=None,degrade=0.0):
    du=du or p['du']; W=du+OP_M
    c=project_monthly(p,adr,occ,capex,du); b=dict(base_monthly(W,degrade))
    return [(m, v-b.get(m,0.0)) for m,v in c]
def xnpv(cfs,r=RA):
    rm=(1+r)**(1/12.0)-1
    return sum(v/((1+rm)**m) for m,v in cfs)
def irr_a(cfs):
    def g(r):
        rm=(1+r)**(1/12.0)-1
        return sum(v/((1+rm)**m) for m,v in cfs)
    lo,hi=-0.95,5.0
    if g(lo)*g(hi)>0: return None
    for _ in range(300):
        mid=(lo+hi)/2
        if g(lo)*g(mid)<=0: hi=mid
        else: lo=mid
    return (lo+hi)/2
def pb_y(cfs):
    cum=0.0
    for m,v in cfs:
        cum+=v
        if cum>=0 and m>0: return m/12.0
    return None
def solve(fn,lo=80.0,hi=9000.0):
    if fn(hi)<0: return None
    for _ in range(64):
        mid=(lo+hi)/2
        if fn(mid)<0: lo=mid
        else: hi=mid
    return int(round((lo+hi)/2))
print('=== 反事实基线（不改造·项目口径·逐月同窗口）===')
print('  年均经营现金流 %.0f 万元（业主口径含存量利息 1,785 万元/年时为 −1,924 万元/年）' % (sum(BASE_CF)/OP_Y))
print()
print('=== 投资基数与停业期（v25）===')
print('%-3s %-22s %4s %4s %7s %8s %8s %9s %9s %8s %9s' % ('#','路径','房量','停业','段二','段三','改造投资','段一现金','段一经济','门槛','项目总投资'))
for p in PATHS:
    print('%-3s %-22s %4d %4d %7.0f %8.0f %8.0f %9.0f %9.0f %8s %9.0f' % (p['k'],p['nm'],p['rm'],p['du'],
      p['s2'],p['s3'],p['cap'],p['seg1_cash'],p['seg1_econ'],p['gate'],p['invest_total']))
print()
print('=== 七路径财务结果（ADR 中值 × OCC 75%，增量口径已同窗口对齐）===')
print('%-3s %-22s %6s %7s %7s %10s %10s %8s %8s %8s %6s' % ('#','路径','ADR中','平衡全','平衡增','全口径NPV','增量NPV','IRR全','IRR增','回收增','正格'))
for p in PATHS:
    p['g_full']=[]; p['g_inc']=[]
    for a in p['adr']:
        rf=[];ri=[]
        for o in OCC:
            rf.append(int(round(xnpv(project_monthly(p,a,o)))))
            ri.append(int(round(xnpv(inc_monthly(p,a,o)))))
        p['g_full'].append(rf); p['g_inc'].append(ri)
    p['be_full']=solve(lambda x: xnpv(project_monthly(p,x,0.75)))
    p['be_inc']=solve(lambda x: xnpv(inc_monthly(p,x,0.75)))
    p['pos_full']=sum(1 for r in p['g_full'] for v in r if v>0)
    p['pos_inc']=sum(1 for r in p['g_inc'] for v in r if v>0)
    c=project_monthly(p,p['adr'][1],0.75); ic=inc_monthly(p,p['adr'][1],0.75)
    p['full_mid']=int(round(xnpv(c))); p['inc_mid']=int(round(xnpv(ic)))
    p['irr_full']=irr_a(c); p['pb_full']=pb_y(c); p['irr_inc']=irr_a(ic); p['pb_inc']=pb_y(ic)
    cl=project_monthly(p,p['adr'][0],0.75); ch=project_monthly(p,p['adr'][2],0.75)
    p['full_lo']=int(round(xnpv(cl))); p['full_hi']=int(round(xnpv(ch)))
    p['inc_lo']=int(round(xnpv(inc_monthly(p,p['adr'][0],0.75)))); p['inc_hi']=int(round(xnpv(inc_monthly(p,p['adr'][2],0.75))))
    e=engine(p,p['adr'][1],0.75); p['cf20']=[round(y['cash_flow'],1) for y in e['yearly']]
    p['tr20']=[round(y['trevpar'],1) for y in e['yearly']]
    p['adr20']=[round(y['adr'],1) for y in e['yearly']]
    p['occ20']=[round(y['occ'],1) for y in e['yearly']]
    p['rev20']=[round(y['total_revenue'],1) for y in e['yearly']]
    p['gop20']=[round(y['gop_rate'],1) for y in e['yearly']]
    print('%-3s %-22s %6d %7s %7s %10s %10s %8s %8s %8s %6s' % (p['k'],p['nm'],p['adr'][1],
      ('%d'%p['be_full']) if p['be_full'] else '不可达',
      ('%d'%p['be_inc']) if p['be_inc'] else '不可达',
      ('%+d'%p['full_mid']),('%+d'%p['inc_mid']),
      ('%.2f%%'%(100*p['irr_full'])) if p['irr_full'] else '为负',
      ('%.2f%%'%(100*p['irr_inc'])) if p['irr_inc'] else '为负',
      ('%.1f年'%p['pb_inc']) if p['pb_inc'] else '>20','%d/15'%p['pos_inc']))
print()
print('=== 自检：增量口径时间轴对齐 ===')
p=PATHS[0]
c=project_monthly(p,p['adr'][1],0.75); ic=inc_monthly(p,p['adr'][1],0.75)
print('  项目臂 %d 个月｜反事实窗口 %d 个月｜增量臂 %d 个月' % (len(c), p['du']+OP_M, len(ic)))
print('  项目臂 NPV %+.0f｜反事实 NPV %+.0f｜增量 NPV %+.0f（差 %+.0f，检验一致）' % (
  xnpv(c), xnpv([(m,v) for m,v in base_monthly(p['du']+OP_M)]), xnpv(ic),
  xnpv(c)-xnpv([(m,v) for m,v in base_monthly(p['du']+OP_M)])-xnpv(ic)))
print('  停业期经营现金流损失（改造后 0 收入 vs 不改造继续经营）已逐月计入增量')
json.dump(dict(P=PATHS,BASE_CF=BASE_CF,PARAMS=dict(RA=RA,OP_Y=OP_Y,OP_M=OP_M,SEG1_ALL=SEG1_ALL,
 RIGID_ALL=RIGID_ALL,RIGID_PROJ=RIGID_PROJ,INT_M=INT_M,REV_LOSS_M=REV_LOSS_M,BRAND_KEEP_M=BRAND_KEEP_M,
 BRAND_SPECIAL=BRAND_SPECIAL,S2_NO_CUT=S2_NO_CUT,S2_CUT=S2_CUT,CONT=CONT,FURN=FURN,OCC=OCC,
 FL=FL,CREW=CREW,CH_LEAD=CH_LEAD,UNIT={'%s·%s'%k:v for k,v in UNIT.items()},
 PUB={'%s·%s'%k:v for k,v in PUB.items()},PSQM={'%s·%s·%s'%k:v for k,v in PSQM.items()},
 DT={'%s·%s·%s'%k:downtime(k) for k in SCHED})),
 open(r'D:\B166ER-openclaw\workspace\.tmp\v25.json','w',encoding='utf-8'),ensure_ascii=False,default=str)
print('saved v25.json')
