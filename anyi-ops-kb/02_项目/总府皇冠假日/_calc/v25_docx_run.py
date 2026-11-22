
# -*- coding: utf-8 -*-
"""v25：插图引用 + 生成 Word"""
import io, os, sys, re, shutil, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
CALC=r'D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc'
KB=r'D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日'
TGT=r'C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店'
REP=os.path.join(TGT,'改造报告交付')
FIGDIR=os.path.join(CALC,'fig')
F=os.path.join(KB,'总府皇冠改造_可行性研究报告_v25.0_2026-11-16.md')
T=io.open(F,encoding='utf-8').read()
# 图件插入点：锚点标题之后
FIGS=[
 ('## 6.4 停业期重新核定（工程流水法）','fig5_停业期流水.png','图5　各路径停业期工程流水核定'),
 ('## 7.1 七路径结果总表','fig2_NPV路径.png','图2　NPV 路径与 IRR 对比'),
 ('## 7.3 动态区间矩阵与回正空间','fig4_NPV对ADR.png','图4　增量口径 NPV 对 ADR 的敏感性'),
 ('## 8.2 敏感性（P4 洲至奢选·保留·不减房，增量口径 NPV，基准 −6,653 万元）','fig3_敏感性.png','图3　P4 敏感性（增量口径 NPV）'),
 ('## 9.2 生命周期四段优化','fig1_现金流曲线.png','图1　20 年现金流曲线与 TRevPAR 趋势'),
]
n=0
for anchor,fn,cap in FIGS:
    if anchor not in T: print('  [MISS anchor]',anchor[:30]); continue
    rel='_calc/fig/'+fn
    if not os.path.exists(os.path.join(KB,rel)): print('  [MISS fig]',fn); continue
    blk='\n![%s](%s)\n' % (cap,rel)
    T=T.replace(anchor, anchor+blk, 1)
    n+=1
io.open(F,'w',encoding='utf-8').write(T)
print('figures inserted:',n)
# 生成 docx
src=io.open(os.path.join(CALC,'v996_docx.py'),encoding='utf-8').read()
s2=src.replace('v24.0_2026-11-16','v25.0_2026-11-16')
dst=os.path.join(CALC,'v25_docx.py')
io.open(dst,'w',encoding='utf-8').write(s2)
print('docx script written')
PY=r'C:\Users\ericz\AppData\Local\Programs\Python\Python314\python.exe'
ENV=dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONUTF8='1')
r=subprocess.run([PY,dst],capture_output=True,text=True,encoding='utf-8',errors='replace',env=ENV,timeout=1200)
print('rc=',r.returncode)
if r.returncode: print((r.stderr or '')[-800:])
lg=os.path.join(r'D:\B166ER-openclaw\workspace\.tmp','v17.log')
if os.path.exists(lg):
    print('--- log tail ---')
    print('\n'.join(io.open(lg,encoding='utf-8').read().split('\n')[-22:]))
