
# -*- coding: utf-8 -*-
"""25 品牌统一财务表：房量按 PIP 面积门槛反推，投资与收益按档次单价测算"""
import io, os, sys, json, re
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
_KEEP=sys.stdout
KB=r'D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日'
CALC=os.path.join(KB,'_calc')
for p in (CALC, r'D:\B166ER-openclaw\workspace\toolbox'):
    if p not in sys.path: sys.path.insert(0,p)
import hotel_irr_calc_zongfu_v2 as Z
E=sys.modules['hotel_irr_calc']
# ── 解析 v23 品牌表取「落位与可得性」──
T=io.open(os.path.join(KB,'总府皇冠改造_可行性研究报告_v23.0_2026-11-16.md'),encoding='utf-8').read()
L=T.split(chr(10)); LOC={}
i=0
while i<len(L):
    if L[i].lstrip().startswith('| 级别 |') and '品牌' in L[i]:
        j=i
        while j<len(L) and L[j].lstrip().startswith('|'): j+=1
        for k in range(i+2,j):
            c=[x.strip() for x in L[k].strip().strip('|').split('|')]
            if len(c)>=11: LOC[c[1].replace('**','')]=(c[0].replace('**',''),c[2].replace('**',''),c[-1].replace('**',''))
        break
    i+=1
print('v23 品牌表解析行数：', len(LOC))
# ── 品牌清单：门槛（PIP 套内面积）、做法、档次 ──
BR=[
 ('皇冠假日','IHG','五星全服',35.0,'保留','皇冠','春熙路核心商圈·现有合同主体'),
 ('集团自有品牌','安逸/自投','五星全服',30.0,'保留','皇冠','总府路自主品牌·不需品牌方'),
 ('洲至奢选','IHG','上奢',40.0,'保留','洲至奢选','棕榈泉 8km·体系内可换牌路径'),
 ('艾美','雅高','上奢',40.0,'重做','洲至奢选','群光路 2.5km·无'),
 ('威斯汀','雅高','上奢',40.0,'重做','洲至奢选','天府大道 8km·无'),
 ('喜来登','雅高','上奢',40.0,'重做','洲至奢选','无布点·中'),
 ('君悦','凯悦','上奢',40.0,'重做','洲至奢选','春熙路 1km·近'),
 ('凯宾斯基','凯悦','上奢',40.0,'重做','洲至奢选','盐市口 2.5km·中'),
 ('万豪','万豪','上奢',40.0,'重做','洲至奢选','新会展 15km·远'),
 ('雅乐轩','雅高','上奢',35.0,'重做','洲至奢选','少府街 5km·中'),
 ('雅高系其他','雅高','上奢',40.0,'重做','洲至奢选','多品牌可选·远'),
 ('洲际','IHG','上奢',40.0,'重做','洲至奢选','现有合作品牌·可争取'),
 ('瑞吉','万豪','顶奢',40.0,'重做','外部奢牌','春熙路 0.5km·近'),
 ('麒麟','凯宾斯基','顶奢',45.0,'重做','外部奢牌','骡马市 2km·近'),
 ('丽思卡尔顿','万豪','顶奢',45.0,'重做','外部奢牌','天府大道 8km·远'),
 ('宝格丽','万豪','顶奢',60.0,'重做','外部奢牌','无布点·低'),
 ('半岛','半岛','顶奢',55.0,'重做','外部奢牌','无布点·低'),
 ('瑰丽','太古','顶奢',45.0,'重做','外部奢牌','无布点·低'),
 ('文华东方','文华东方','顶奢',45.0,'重做','外部奢牌','已签约 2022-10·低'),
 ('尼依格罗','IHG','顶奢',40.0,'重做','外部奢牌','东大街 2.5km·近'),
 ('四季','四季','顶奢',45.0,'重做','外部奢牌','无布点·低'),
 ('居舍（原博舍）','太古集团','顶奢',45.0,'重做','外部奢牌','太古里·直营自营·不可比选'),
]
# ── 配置与造价参数（与 v25 模型一致）──
UNIT={('皇冠','保留'):5800,('皇冠','重做'):9600,('洲至奢选','保留'):9400,
 ('洲至奢选','重做'):15000,('外部奢牌','重做'):20900}
PUB={('皇冠','保留'):3554.7,('皇冠','重做'):6783.1,('洲至奢选','保留'):5585.9,
 ('洲至奢选','重做'):10200.7,('外部奢牌','重做'):12923.2}
CONT={'皇冠':0.055,'洲至奢选':0.0675,'外部奢牌':0.08}
A39={('皇冠','保留','不减房'):(402,25.35,10253.6),('皇冠','保留','3改2'):(268,48.0,9688.0),
 ('皇冠','重做','不减房'):(402,25.35,18111.3),('洲至奢选','保留','不减房'):(402,25.35,17130.7),
 ('洲至奢选','重做','3改2'):(268,48.0,32781.3),('外部奢牌','重做','3改2'):(268,48.0,45250.9),
 ('外部奢牌','重做','不减房'):(402,25.35,39216.7)}
BRAND_SPECIAL=1990.0; FURN=540.0; S2_NO_CUT,S2_CUT=8790.0,9330.0
CFG={'不减房':dict(rm=402,suite=25.35,ab=25.35,sale=30.57),
     '3改2':dict(rm=268,suite=38.03,ab=48.0,sale=45.85),
     '2改1':dict(rm=201,suite=50.71,ab=60.9,sale=61.15),
     '全套房':dict(rm=162,suite=63.0,ab=78.75,sale=75.95)}
TIER={'皇冠':('intl_current_crowne',0.020,0.06),'洲至奢选':('intl_upper_upscale',0.020,0.08),
      '外部奢牌':('intl_luxury',0.020,0.10)}
BASE_FEE={'intl_current_crowne':0.020,'intl_upper_upscale':0.020,'intl_luxury':0.020}
INC_FEE={'intl_current_crowne':0.06,'intl_upper_upscale':0.08,'intl_luxury':0.10}
GOPM={'intl_current_crowne':0.6725,'intl_upper_upscale':0.6725,'intl_luxury':0.6725}
RA=0.08; RM=(1+RA)**(1/12.0)-1; OP_Y=20; OP_M=240
SEG1_ALL=815.0; RIGID_PROJ=162.5; BRAND_KEEP_M=round(292.8/18.0,2)
REV_LOSS_M=564.5; RIGID_ALL=250.5
# 单位面积价带（毛房价，元/㎡·夜）
PSQM={('皇冠','保留','不减房'):(14.5,16.0,17.5),
      ('皇冠','保留','3改2'):(14.5,16.0,17.5),
      ('皇冠','重做','不减房'):(15.5,17.0,18.5),
      ('洲至奢选','保留','不减房'):(16.0,17.8,19.5),
      ('洲至奢选','重做','2改1'):(17.0,19.0,21.0),
      ('洲至奢选','重做','全套房'):(17.0,19.0,21.0),
      ('外部奢牌','重做','2改1'):(23.0,27.0,31.0),
      ('外部奢牌','重做','全套房'):(23.0,27.0,31.0)}
# 停业期（按做法＋房量配置工程流水）
DTMAP={'保留·不减房':19,'保留·3改2':26,'重做·不减房':23,'重做·2改1':29,'重做·3改2':27,'重做·全套房':33}
def pick_cfg(thr, keep_402_exc):
    if keep_402_exc: return '不减房'
    for cn,su in (('3改2',38.03),('2改1',50.71),('全套房',63.0)):
        if su>=thr: return cn
    return '全套房'
def seg3(b,m,cfg):
    c=CFG[cfg]; room=c['rm']*c['ab']*UNIT[(b,m)]/1e4; pub=PUB[(b,m)]
    key=(b,m,cfg)
    if key in A39:
        ar,aa,av=A39[key]; s3=av+(c['rm']*c['ab']-ar*aa)*UNIT[(b,m)]/1e4
    else:
        cand=[(k,v) for k,v in A39.items() if k[0]==b and k[1]==m] or [(k,v) for k,v in A39.items() if k[0]==b]
        kk,vv=max(cand,key=lambda kv:kv[1][0]); ar,aa,av=vv
        s3=room+(av-ar*aa*UNIT[(b,m)]/1e4)
    return round(s3+BRAND_SPECIAL,1)
def engine(p,adr,occ):
    q=dict(Z.BASELINE)
    q.update(project_name=p['nm'],scenario='测算',tier_params=p['tier'],rooms=p['rm'],
      peak_adr=float(adr),peak_occ=float(occ),total_invest=p['cap'],include_new_dep=True,
      building_value_existing=21949.0,electromechanical_value=p['s2'],labor_in_gop=True,
      labor_cost_annual=2023.0,debt_service_annual=0.0,rent_annual=0,discount_rate=RA,
      tax_rate=0.25,horizon=OP_Y,ramp_type='renovation',closure_months=0,closure_loss_monthly=0,
      transition_drag_pct=p['trans']['drag'],transition_years=p['trans']['dy'],
      transition_extra_cost_annual=p['trans']['extra'],transition_oneoff=0.0,gop_measured_rate=None)
    return Z.calc_zongfu2(q)
BASE=dict(Z.BASELINE)
BASE.update(debt_service_annual=0.0,horizon=OP_Y,include_new_dep=False,gop_measured_rate=0.0974,
  total_invest=0,closure_months=0,closure_loss_monthly=0)
BASE_CF=[y['cash_flow'] for y in Z.calc_zongfu2(dict(BASE))['yearly']]
def base_monthly(months):
    out=[]
    for m in range(1,months+1):
        y=min((m-1)//12,OP_Y-1); out.append((m,BASE_CF[y]/12.0))
    return out
def xnpv(c,r=RA):
    rm=(1+r)**(1/12.0)-1
    return sum(v/((1+rm)**m) for m,v in c)
def irr_a(c):
    def g(r):
        rm=(1+r)**(1/12.0)-1
        return sum(v/((1+rm)**m) for m,v in c)
    lo,hi=-0.95,5.0
    if g(lo)*g(hi)>0: return None
    for _ in range(300):
        mid=(lo+hi)/2
        if g(lo)*g(mid)<=0: hi=mid
        else: lo=mid
    return (lo+hi)/2
def pb_y(c):
    cum=0.0
    for m,v in c:
        cum+=v
        if cum>=0 and m>0: return m/12.0
    return None
def solve(fn,lo=80.0,hi=9000.0):
    if fn(hi)<0: return None
    for _ in range(60):
        mid=(lo+hi)/2
        if fn(mid)<0: lo=mid
        else: hi=mid
    return int(round((lo+hi)/2))
TRANS={('皇冠','保留'):dict(drag=0.12,dy=2,extra=400.0,oneoff=1200.0),
 ('皇冠','重做'):dict(drag=0.14,dy=2,extra=450.0,oneoff=1400.0),
 ('洲至奢选','保留'):dict(drag=0.18,dy=2,extra=520.0,oneoff=1700.0),
 ('洲至奢选','重做'):dict(drag=0.20,dy=2,extra=550.0,oneoff=1800.0),
 ('外部奢牌','重做'):dict(drag=0.25,dy=2,extra=700.0,oneoff=2200.0)}
ROWS=[]
for nm,grp,lvl,thr,route,std,loc in BR:
    keep402 = (nm in ('皇冠假日','集团自有品牌','洲至奢选'))
    cfg = pick_cfg(thr, keep402)
    c=CFG[cfg]; s2=S2_CUT if cfg!='不减房' else S2_NO_CUT
    s3=seg3(std,route,cfg); cap=round(s2+s3,1)
    du=DTMAP['%s·%s'%(route,cfg)]
    rigid=round(RIGID_PROJ+(BRAND_KEEP_M if std!='皇冠' else 0.0),2)
    band=PSQM.get((std,route,cfg)) or PSQM[(std,route,'2改1')]
    adr=[int(round(x*c['sale'])) for x in band]
    p=dict(nm=nm,nm2=nm,grp=grp,lvl=lvl,std=std,route=route,cfg=cfg,rm=c['rm'],suite=c['suite'],
      sale=c['sale'],thr=thr,cap=cap,s2=s2,s3=s3,du=du,rigid=rigid,adr=adr,band=band,
      tier=TIER[std][0],trans=TRANS[(std,route)],loc=loc,
      seg1_cash=round(rigid*du,1),seg1_econ=round(SEG1_ALL*du,1),
      invest_total=round(cap+SEG1_ALL*du,1))
    p['gate']='达标' if p['suite']>=thr else '差%.1f㎡'%(thr-p['suite'])
    if keep402 and thr>25.35: p['gate']='需书面例外'
    def pm(a,o):
        op=[y['cash_flow'] for y in engine(p,a,o)['yearly']]
        cf=[]; capm=cap/du
        for m in range(1,du+1): cf.append((m,-capm-rigid))
        for y in range(OP_Y):
            for k in range(12):
                v=op[y]/12.0
                if y==0 and k==0: v-=p['trans']['oneoff']/12.0
                cf.append((du+y*12+k+1,v))
        return cf
    def ic(a,o):
        cf=pm(a,o); W=du+OP_M; bm=dict(base_monthly(W))
        return [(m,v-bm.get(m,0.0)) for m,v in cf]
    p['g_inc']=[[int(round(xnpv(ic(a,o)))) for o in (0.65,0.70,0.75,0.80,0.85)] for a in adr]
    p['pos']=sum(1 for r in p['g_inc'] for v in r if v>0)
    cf=pm(adr[1],0.75); icf=ic(adr[1],0.75)
    p['inc_mid']=int(round(xnpv(icf))); p['full_mid']=int(round(xnpv(cf)))
    p['irr']=irr_a(icf); p['pb']=pb_y(icf)
    p['be']=solve(lambda x: xnpv(ic(x,0.75)))
    ROWS.append(p)
json.dump(dict(ROWS=ROWS,BASE_CF=BASE_CF),open(r'D:\B166ER-openclaw\workspace\.tmp\v25b.json','w',encoding='utf-8'),ensure_ascii=False,default=str)
print()
print('=== 25 品牌统一财务表（ADR 中值 × OCC 75%，增量口径）===')
print('%-14s %-8s %-8s %-10s %5s %-9s %9s %8s %8s %8s %6s' % ('品牌','集团','档次','标准/做法','房量','门槛','改造投资','ADR区间','平衡价','增量NPV','IRR'))
for r in ROWS:
    print('%-14s %-8s %-8s %-10s %5d %-9s %9.0f %8s %8s %8s %6s' % (r['nm'],r['grp'][:6],r['lvl'],r['std']+'·'+r['route'],
      r['rm'],r['gate'],r['cap'],'%d/%d/%d'%tuple(r['adr']),
      ('%d'%r['be']) if r['be'] else '不可达','%+d'%r['inc_mid'],
      ('%.2f%%'%(100*r['irr'])) if r['irr'] else '为负'))
print('saved v25b.json ｜ 品牌数', len(ROWS))
