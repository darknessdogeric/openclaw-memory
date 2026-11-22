
# -*- coding: utf-8 -*-
"""v25 终检与归档"""
import io, os, sys, re, glob, shutil, subprocess, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
CALC=r'D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc'
KB=r'D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日'
TGT=r'C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店'
REP=os.path.join(TGT,'改造报告交付'); CO=os.path.join(TGT,'测算与中间产物')
FIGD=os.path.join(CALC,'fig')
PY=r'C:\Users\ericz\AppData\Local\Programs\Python\Python314\python.exe'
ENV=dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONUTF8='1')
F=os.path.join(KB,'总府皇冠改造_可行性研究报告_v25.0_2026-11-16.md')
T=io.open(F,encoding='utf-8').read()
L=T.split('\n')
for i,l in enumerate(L):
    if l.startswith('| 摘要 |'):
        L[i]='| 摘要 | **结论摘要（结论先行）** | 怎么做、要多少钱、能不能赚钱 |'
        print('TOC row fixed at L%d' % (i+1)); break
for i,l in enumerate(L):
    if l.startswith('| 6 | 六路径界定与投资估算 |'):
        L[i]='| 6 | 路径界定与投资估算 | 每条路多少钱、顶奢减房为何无解 |'
        print('TOC ch6 title fixed at L%d' % (i+1)); break
T='\n'.join(L)
io.open(F,'w',encoding='utf-8').write(T)
# ── Word 重建 ──
r=subprocess.run([PY,os.path.join(CALC,'v25_docx.py')],capture_output=True,text=True,encoding='utf-8',errors='replace',env=ENV,timeout=1800)
print('docx rc=',r.returncode)
if r.returncode: print((r.stderr or '')[-400:])
LOG=io.open(os.path.join(r'D:\B166ER-openclaw\workspace\.tmp','v17.log'),encoding='utf-8').read()
bl=[l for l in LOG.split('\n') if l.startswith('BLANK')]
tail=[l for l in LOG.split('\n') if l.strip()][-5:]
print('docx 空白格:',len(bl))
for l in tail: print('   ',l)
# ── 归档 ──
DOCX=os.path.join(REP,'总府皇冠改造_可行性研究报告_v25.0_2026-11-16.docx')
XLSX=os.path.join(CO,'总府皇冠改造_测算附表_v25.0_2026-11-16.xlsx')
FIGOUT=os.path.join(CO,'图件')
os.makedirs(FIGOUT,exist_ok=True)
for f in glob.glob(os.path.join(FIGD,'fig*.png')):
    shutil.copy2(f, FIGOUT)
# 中间产物：模型 json 与脚本
MODOUT=os.path.join(CO,'测算中间产物')
os.makedirs(MODOUT,exist_ok=True)
for f in ['v25.json','v25b.json','v25c.json','v25p.json']:
    s=os.path.join(r'D:\B166ER-openclaw\workspace\.tmp',f)
    if os.path.exists(s): shutil.copy2(s, MODOUT)
for f in ['v25_model.py','v25_brands.py','v25_figs.py','v25_asm.py','v25_excel.py','v25_docx.py']:
    s=os.path.join(CALC,f)
    if os.path.exists(s): shutil.copy2(s, MODOUT)
shutil.copy2(F, os.path.join(REP,'总府皇冠改造_可行性研究报告_v25.0_2026-11-16.md'))
# ── 清旧版 ──
for d in (REP,CO):
    for f in os.listdir(d):
        if re.search(r'_v(2[0-4])\.0_2026-11-16\.(docx|xlsx|md)$', f) or ('_v2' in f and f.endswith('.docx')):
            p=os.path.join(d,f)
            if 'v25.0' not in f:
                os.remove(p); print('removed', os.path.basename(p))
print()
print('=== 交付目录 ===')
for d in (REP,CO):
    print('--',d)
    for f in sorted(os.listdir(d)):
        p=os.path.join(d,f)
        if os.path.isfile(p): print('   %9.1f KB  %s' % (os.path.getsize(p)/1024,f))
    for sub in os.listdir(d):
        sp=os.path.join(d,sub)
        if os.path.isdir(sp):
            print('   [dir]',sub, len(os.listdir(sp)),'项')
