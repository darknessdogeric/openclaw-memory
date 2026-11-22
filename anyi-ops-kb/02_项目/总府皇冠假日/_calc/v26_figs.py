# -*- coding: utf-8 -*-
"""v26 图件：市场分析价格 → 投资承受力（方法论反转版）"""
import io, os, sys, json, tempfile, importlib.util
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
CALC=r'D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc'
for p in (CALC,):
    if p not in sys.path: sys.path.insert(0,p)
spec=importlib.util.spec_from_file_location('M26', os.path.join(CALC,'v26_model.py'))
M=importlib.util.module_from_spec(spec)
_tf=tempfile.NamedTemporaryFile(mode='w',encoding='utf-8',suffix='.log',delete=False)
old=sys.stdout; sys.stdout=_tf
spec.loader.exec_module(M)
sys.stdout=old; _tf.close()
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
import numpy as np
for cand in ['Microsoft YaHei','SimHei','Microsoft JhengHei','SimSun']:
    if any(cand.lower() in f.name.lower() for f in font_manager.fontManager.ttflist):
        plt.rcParams['font.sans-serif']=[cand]; break
plt.rcParams['axes.unicode_minus']=False
FIG=os.path.join(CALC,'fig26')
os.makedirs(FIG,exist_ok=True)
P=M.PATHS
VA=json.load(open(r'D:\B166ER-openclaw\workspace\.tmp\v26a.json',encoding='utf-8'))
VB=json.load(open(r'D:\B166ER-openclaw\workspace\.tmp\v26b.json',encoding='utf-8'))
GRID=VA['GRID']; BE=VA['BE']; THR=VA['THR']
COL={'A1':'#2E75B6','A2':'#70AD47','A3':'#8FAADC','A4R':'#A5A5A5','A4':'#C55A11','B1':'#BF9000','B2':'#7030A0','C1':'#C00000'}
def inc_npv(p,adr,occ=0.75):
    return M.npv(M.inc_arm(p,adr,occ))
def full_npv(p,adr,occ=0.75):
    return M.npv(M.arm_cash(p,adr,occ))
NM={p['k']:p['nm'] for p in P}

# ── 图1：增量 NPV 对 ADR 曲线 ──
fig,ax=plt.subplots(figsize=(12,6.6))
for p in P:
    xs=np.linspace(300,1600,40)
    ys=[inc_npv(p,x) for x in xs]
    ax.plot(xs,ys,'-',lw=2.0,color=COL[p['k']],label='%s %s'%(p['k'],p['nm']))
    lo,mid,hi=p['mkt']
    ax.plot([lo,hi],[inc_npv(p,mid)]*2,color=COL[p['k']],lw=7,alpha=.16)
ax.axhline(0,color='#C00000',ls='--',lw=1.6,label='NPV = 0')
ax.set_xlim(300,1600); ax.set_xlabel('ADR（元/间夜）'); ax.set_ylabel('增量口径 NPV（万元）')
ax.set_title('图1　增量口径 NPV 对 ADR 的敏感性（OCC 75%）与市场分析价格带（粗带＝低～高档）',fontsize=12)
ax.legend(fontsize=8,ncol=2); ax.grid(alpha=.3)
fig.tight_layout(); fig.savefig(os.path.join(FIG,'fig01_增量NPV对ADR.png'),dpi=170); plt.close(fig)

# ── 图2：三路径分类对比 ──
fig,ax=plt.subplots(1,2,figsize=(14,5.6))
nm=[('%s %s'%(p['k'],p['nm'])) for p in P]
x=range(len(P)); w=0.38
incv=[]; fullv=[]; irrv=[]
for p in P:
    r=[r for r in VA['RES'] if r['k']==p['k'] and r['lbl']=='中'][0]
    incv.append(r['inc']); fullv.append(r['full']); irrv.append((r['irr_inc'] or 0)*100)
ax[0].bar([i-w/2 for i in x],fullv,w,color='#8FAADC',label='全口径 NPV')
ax[0].bar([i+w/2 for i in x],incv,w,color='#ED7D31',label='增量口径 NPV')
ax[0].axhline(0,color='#333',lw=1); ax[0].set_xticks(list(x)); ax[0].set_xticklabels(nm,rotation=30,ha='right',fontsize=8)
ax[0].set_ylabel('NPV（万元）'); ax[0].set_title('八路径 NPV 对比（市场分析 ADR 中档 × OCC 75%）',fontsize=11.5)
ax[0].legend(); ax[0].grid(alpha=.3,axis='y')
cols=[COL[p['k']] for p in P]
ax[1].bar(list(x),irrv,color=cols)
ax[1].axhline(8,color='#C00000',ls='--',lw=1.5,label='集团 IRR 参照 8%')
ax[1].axhline(0,color='#333',lw=1)
ax[1].set_xticks(list(x)); ax[1].set_xticklabels(nm,rotation=30,ha='right',fontsize=8)
ax[1].set_ylabel('增量口径 IRR（%）'); ax[1].set_title('增量口径 IRR（负值＝不成立）',fontsize=11.5)
ax[1].legend(); ax[1].grid(alpha=.3,axis='y')
fig.suptitle('图2　三路径分类下的财务结果（保留体量轻改／保留体量重改／体量变化重改）',fontsize=13,fontweight='bold')
fig.tight_layout(); fig.savefig(os.path.join(FIG,'fig02_三路径财务对比.png'),dpi=170); plt.close(fig)

# ── 图3：敏感性龙卷风（A1）──
th={t['k']:t for t in THR}[ 'A1']
base=th['be']; rows=sorted(th['rows'],key=lambda r:abs(r[1]))
fig,ax=plt.subplots(figsize=(11,6.4))
cols2=['#70AD47' if r[1]>0 else '#C00000' for r in rows]
ax.barh([r[0] for r in rows],[r[1] for r in rows],color=cols2)
ax.axvline(0,color='#333',lw=1.2)
ax.set_xlabel('全口径 NPV（万元）'); ax.set_title('图3　A1 皇冠假日·保留体量·轻改 平衡点左右的阈值区间（平衡 ADR %d 元，基准 NPV 0）'%round(base),fontsize=12)
ax.grid(alpha=.3,axis='x')
for i,r in enumerate(rows): ax.text(r[1],i,' %+d'%r[1],va='center',fontsize=9)
fig.tight_layout(); fig.savefig(os.path.join(FIG,'fig03_敏感性龙卷风.png'),dpi=170); plt.close(fig)

# ── 图4：15 格动态区间热力（A1 与 A2）──
fig,axs=plt.subplots(1,2,figsize=(14,5.2))
for axx,k in zip(axs,['A1','A2']):
    g=GRID[k]; mat=np.array([r[2] for r in g],dtype=float)
    im=axx.imshow(mat,cmap='RdYlGn',aspect='auto',vmin=-45,vmax=45)
    axx.set_xticks(range(5)); axx.set_xticklabels(['65%','70%','75%','80%','85%'])
    axx.set_yticks(range(3)); axx.set_yticklabels(['%s档 %d 元'%(g[i][0],g[i][1]) for i in range(3)])
    for i in range(3):
        for j in range(5):
            axx.text(j,i,'%.1f'%mat[i,j],ha='center',va='center',fontsize=10,
                    color='black' if abs(mat[i,j])<20 else 'white')
    axx.set_title('%s %s 全口径 NPV（百万元）'%(k,NM[k]),fontsize=11)
    axx.set_xlabel('开房率'); axx.set_ylabel('定价档')
fig.colorbar(im,ax=axs,shrink=.85,label='百万元')
fig.suptitle('图4　推荐路径的 15 格动态区间（3 档价格 × 5 档开房率）',fontsize=13,fontweight='bold')
fig.tight_layout(); fig.savefig(os.path.join(FIG,'fig04_动态区间热力.png'),dpi=170); plt.close(fig)

# ── 图5：停业期工程流水甘特 ──
fig,ax=plt.subplots(figsize=(12.5,6.4))
rowsP=list(P)
y=0
for p in rowsP:
    d=p['dt']
    segs=[(0,d['t_mep'],'#8FAADC','准备＋拆除＋机电主干'),(d['t_mep'],d['t_floor'],'#2E75B6','楼层流水'),
          (d['t_floor'],d['t_eq'],'#FFD966','设备就绪'),(d['t_eq'],d['t_fire'],'#A9D18E','联调与消防验收'),
          (d['t_fire'],d['t_fix'],'#F4B183','整改复评'),(d['t_fix'],d['t_brand'],'#ED7D31','品牌方验收'),
          (d['t_brand'],d['t_trial'],'#C00000','试营业')]
    for s,e,c,lb in segs:
        if e>s: ax.barh(y,e-s,left=s,color=c,height=.55,edgecolor='w')
    ax.text(d['total']+.8,y,'%d 个月'%round(d['total']),va='center',fontweight='bold',fontsize=9)
    y-=1
ax.set_yticks(range(len(rowsP))); ax.set_yticklabels(['%s %s'%(p['k'],p['nm']) for p in rowsP],fontsize=9)
ax.set_xlabel('停业期（月）'); ax.set_title('图5　各路径停业期工程流水核定（工程流水法推得，非手填）',fontsize=13,fontweight='bold')
ax.grid(alpha=.3,axis='x'); ax.invert_yaxis()
fig.tight_layout(); fig.savefig(os.path.join(FIG,'fig05_停业期流水.png'),dpi=170); plt.close(fig)

# ── 图6：25 品牌增量 NPV 排序 ──
B=VB['ROWS']; Bs=sorted(B,key=lambda r:-r['inc'])
fig,ax=plt.subplots(figsize=(12.5,8.2))
ys=range(len(Bs))
cols3=['#70AD47' if r['inc']>0 else '#C00000' for r in Bs]
ax.barh(list(ys),[r['inc'] for r in Bs],color=cols3)
ax.set_yticks(list(ys)); ax.set_yticklabels(['%s（%s，%d间）'%(r['nm'],r['lvl'],r['rm']) for r in Bs],fontsize=8.5)
ax.axvline(0,color='#333',lw=1.2)
ax.set_xlabel('增量口径 NPV（万元，ADR 中档 × OCC 75%）')
ax.set_title('图6　25 个品牌候选统一比较：增量口径 NPV（绿色＝成立）',fontsize=13,fontweight='bold')
ax.grid(alpha=.3,axis='x'); ax.invert_yaxis()
for i,r in enumerate(Bs):
    v=r['inc']; ax.text(v+(700 if v>=0 else -700),i,'%+d'%v,va='center',ha='left' if v>=0 else 'right',fontsize=8)
fig.tight_layout(); fig.savefig(os.path.join(FIG,'fig06_25品牌增量NPV.png'),dpi=170); plt.close(fig)

# ── 图7：现金流与累计折现 ──
fig,ax=plt.subplots(1,2,figsize=(14,5.6))
for k in ['A1','A2']:
    p=[x for x in P if x['k']==k][0]
    cfs=M.arm_cash(p,p['mkt'][1],0.75)
    ys=[v for m,v in cfs if m>p['du']]
    ann=[]; tot=0
    for i in range(0,len(ys),12):
        tot+=sum(ys[i:i+12]); ann.append(tot)
    ax[0].plot(range(1,len(ann)+1),ann,'-o',ms=4,color=COL[k],label='%s 累计经营现金流'%k)
    icf=M.inc_arm(p,p['mkt'][1],0.75)
    iys=[v for m,v in icf]; itot=0; iann=[]
    for i in range(0,len(iys),12):
        itot+=sum(iys[i:i+12]); iann.append(itot)
    ax[1].plot(range(1,len(iann)+1),iann,'-o',ms=4,color=COL[k],label='%s 累计增量现金流'%k)
ax[0].axhline(0,color='#333',lw=1); ax[0].set_xlabel('运营年度'); ax[0].set_ylabel('累计（万元）')
ax[0].set_title('改造后 20 年累计经营现金流',fontsize=11.5); ax[0].legend(); ax[0].grid(alpha=.3)
ax[1].axhline(0,color='#333',lw=1); ax[1].set_xlabel('运营年度'); ax[1].set_ylabel('累计（万元）')
ax[1].set_title('相对最小合规臂的累计增量现金流',fontsize=11.5); ax[1].legend(); ax[1].grid(alpha=.3)
fig.suptitle('图7　推荐路径的现金流形态（未折现，市场分析 ADR 中档）',fontsize=13,fontweight='bold')
fig.tight_layout(); fig.savefig(os.path.join(FIG,'fig07_现金流与累计.png'),dpi=170); plt.close(fig)
print('figs:', sorted(os.listdir(FIG)))