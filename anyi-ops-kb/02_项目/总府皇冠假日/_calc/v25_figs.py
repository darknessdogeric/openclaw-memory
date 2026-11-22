
# -*- coding: utf-8 -*-
"""v25 敏感性 + 图件"""
import io, os, sys, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
CALC=r'D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc'
for p in (CALC, r'D:\B166ER-openclaw\workspace\toolbox'):
    if p not in sys.path: sys.path.insert(0,p)
import importlib.util
spec=importlib.util.spec_from_file_location('M25', os.path.join(CALC,'v25_model.py'))
M=importlib.util.module_from_spec(spec)
import tempfile
_tf=tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',suffix='.log',delete=False)
old=sys.stdout; sys.stdout=_tf
spec.loader.exec_module(M)
sys.stdout=old; _tf.close()
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
for cand in ['Microsoft YaHei','SimHei','Microsoft JhengHei','SimSun']:
    if any(cand.lower() in f.name.lower() for f in font_manager.fontManager.ttflist):
        plt.rcParams['font.sans-serif']=[cand]; break
plt.rcParams['axes.unicode_minus']=False
FIG=r'D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc\fig'
os.makedirs(FIG,exist_ok=True)
P=M.PATHS
PA=json.load(open(r'D:\B166ER-openclaw\workspace\.tmp\v25.json',encoding='utf-8'))['PARAMS']
# ── 敏感性 ──
def sens(p):
    def s(adr_f=1.0,occ_d=0.0,cap_f=1.0,du_d=0,rate=None,deg=0.0):
        a=int(round(p['adr'][1]*adr_f)); o=min(0.90,0.75+occ_d)
        cx=round(p['cap']*cap_f); du=p['du']+du_d
        c=M.inc_monthly(p,a,o,capex=cx,du=du,degrade=deg)
        r=PA['RA'] if rate is None else rate
        rm=(1+r)**(1/12.0)-1
        return int(round(sum(x/((1+rm)**m) for m,x in c)))
    base=s()
    rows=[('ADR 上浮 10%',s(adr_f=1.10)),('ADR 下浮 10%',s(adr_f=0.90)),
      ('开房率 +5pp',s(occ_d=0.05)),('开房率 −5pp',s(occ_d=-0.05)),
      ('段三 −10%（投资优化）',s(cap_f=0.90)),('段三 +10%（超支）',s(cap_f=1.10)),
      ('停业期 −3 月',s(du_d=-3)),('停业期 +3 月',s(du_d=3)),
      ('折现率 7%',s(rate=0.07)),('折现率 9%',s(rate=0.09)),
      ('反事实劣化 5%/年',s(deg=0.05))]
    return base, rows
SENS={}
for pk in ('P1','P4','P6'):
    p=[x for x in P if x['k']==pk][0]
    b,rows=sens(p); SENS[pk]=dict(base=b,rows=rows)
    print('%s %s 基准 %+d' % (pk,p['nm'],b))
    for n,v in rows: print('   %-22s %+9d（Δ %+d）' % (n,v,v-b))
json.dump(SENS,open(r'D:\B166ER-openclaw\workspace\.tmp\v25c.json','w',encoding='utf-8'),ensure_ascii=False)
# ── 图1：20 年营业现金流与 TRevPAR ──
fig,ax=plt.subplots(1,2,figsize=(13,5))
for pk,col in (('P1','#2E75B6'),('P4','#C55A11')):
    p=[x for x in P if x['k']==pk][0]
    ax[0].plot(range(1,21),p['cf20'],'-o',ms=4,color=col,label='%s 营业现金流'%p['nm'])
    ax[1].plot(range(1,21),p['tr20'],'-o',ms=4,color=col,label='%s TRevPAR'%p['nm'])
ax[0].axhline(0,color='#888',lw=1); ax[0].set_title('改造后 20 年营业现金流（万元/年）',fontsize=12)
ax[0].set_xlabel('运营年度'); ax[0].set_ylabel('营业现金流（万元）'); ax[0].legend(); ax[0].grid(alpha=.3)
ax[1].set_title('改造后 20 年 TRevPAR（元/间）',fontsize=12)
ax[1].set_xlabel('运营年度'); ax[1].set_ylabel('TRevPAR（元/间）'); ax[1].legend(); ax[1].grid(alpha=.3)
fig.suptitle('图1　20 年现金流曲线与 TRevPAR 趋势',fontsize=14,fontweight='bold')
fig.tight_layout(); fig.savefig(os.path.join(FIG,'fig1_现金流曲线.png'),dpi=170); plt.close(fig)
# ── 图2：七路径 NPV/IRR ──
fig,ax=plt.subplots(1,2,figsize=(13,5.2))
nm=[p['k']+' '+p['nm'].replace('假日·','') for p in P]
x=range(len(P)); w=0.38
ax[0].bar([i-w/2 for i in x],[p['full_mid'] for p in P],w,color='#8FAADC',label='全口径 NPV')
ax[0].bar([i+w/2 for i in x],[p['inc_mid'] for p in P],w,color='#ED7D31',label='增量口径 NPV')
ax[0].axhline(0,color='#333',lw=1); ax[0].set_xticks(list(x)); ax[0].set_xticklabels(nm,rotation=32,ha='right',fontsize=8)
ax[0].set_ylabel('NPV（万元）'); ax[0].set_title('七路径 NPV 对比（ADR 中值 × OCC 75%）',fontsize=12)
ax[0].legend(); ax[0].grid(alpha=.3,axis='y')
irr=[(p['irr_inc'] or 0)*100 for p in P]
ax[1].bar(list(x),irr,color='#70AD47')
ax[1].axhline(8,color='#C00000',ls='--',lw=1.5,label='集团 IRR 参照 8%')
ax[1].set_xticks(list(x)); ax[1].set_xticklabels(nm,rotation=32,ha='right',fontsize=8)
ax[1].set_ylabel('增量口径 IRR（%）'); ax[1].set_title('增量口径 IRR 对比',fontsize=12)
ax[1].legend(); ax[1].grid(alpha=.3,axis='y')
fig.suptitle('图2　NPV 路径与 IRR 对比',fontsize=14,fontweight='bold')
fig.tight_layout(); fig.savefig(os.path.join(FIG,'fig2_NPV路径.png'),dpi=170); plt.close(fig)
# ── 图3：敏感性龙卷风（P4）──
b=SENS['P4']['base']; rows=sorted(SENS['P4']['rows'],key=lambda r:abs(r[1]-b))
fig,ax=plt.subplots(figsize=(11,6))
cols=['#70AD47' if r[1]>b else '#C00000' for r in rows]
ax.barh([r[0] for r in rows],[r[1]-b for r in rows],color=cols)
ax.axvline(0,color='#333',lw=1)
ax.set_xlabel('增量口径 NPV 变动（万元）'); ax.set_title('图3　P4 洲至奢选·保留·不减房 敏感性（增量口径 NPV 基准 %s 万元）'%'{:,}'.format(b),fontsize=12)
ax.grid(alpha=.3,axis='x')
for i,r in enumerate(rows): ax.text(r[1]-b, i, ' %+d'%(r[1]-b), va='center',fontsize=9)
fig.tight_layout(); fig.savefig(os.path.join(FIG,'fig3_敏感性.png'),dpi=170); plt.close(fig)
# ── 图4：增量 NPV 对 ADR 曲线 + 天花板 ──
fig,ax=plt.subplots(figsize=(11,6))
for p,col in zip(P,['#2E75B6','#7F7F7F','#A5A5A5','#C55A11','#BF9000','#7030A0','#375623']):
    ax.plot(p['adr'],[p['g_inc'][i][2] for i in range(len(p['adr']))],'-o',ms=5,color=col,label='%s %s'%(p['k'],p['nm']))
top=37.0
ax.set_xlim(300,2600)
ax.set_xlabel('ADR（元/间夜）'); ax.set_ylabel('增量口径 NPV（万元）')
ax.set_title('图4　增量口径 NPV 对 ADR 的敏感性（OCC 75%）与单位面积价天花板 37.0 元/㎡·夜',fontsize=12)
ax.axhline(0,color='#C00000',ls='--',lw=1.5,label='NPV = 0')
ax.legend(fontsize=8); ax.grid(alpha=.3)
fig.tight_layout(); fig.savefig(os.path.join(FIG,'fig4_NPV对ADR.png'),dpi=170); plt.close(fig)
# ── 图5：停业期工程流水甘特 ──
fig,ax=plt.subplots(figsize=(12,6))
y=0
for p in P:
    d=p['dt']
    segs=[(0,d['t_mep'],'#8FAADC','准备＋拆除＋机电主干'),(d['t_mep'],d['t_floor'],'#2E75B6','楼层流水'),
          (d['t_floor'],d['t_eq'],'#FFD966','设备就绪'),(d['t_eq'],d['t_fire'],'#A9D18E','联调与消防验收'),
          (d['t_fire'],d['t_fix'],'#F4B183','整改复评'),(d['t_fix'],d['t_brand'],'#ED7D31','品牌方验收'),
          (d['t_brand'],d['t_trial'],'#C00000','试营业')]
    for s,e,c,lb in segs:
        if e>s: ax.barh(y,e-s,left=s,color=c,height=.55,edgecolor='w')
    ax.text(d['total']+1.0,y,'%d 个月'%d['total'],va='center',fontweight='bold',fontsize=9)
    y-=1
ax.set_yticks(range(len(P))); ax.set_yticklabels(['%s %s'%(p['k'],p['nm']) for p in P],fontsize=9)
ax.set_xlabel('停业期（月）'); ax.set_title('图5　各路径停业期工程流水核定',fontsize=13,fontweight='bold')
ax.grid(alpha=.3,axis='x'); ax.invert_yaxis()
fig.tight_layout(); fig.savefig(os.path.join(FIG,'fig5_停业期流水.png'),dpi=170); plt.close(fig)
print('figs:', sorted(os.listdir(FIG)))
