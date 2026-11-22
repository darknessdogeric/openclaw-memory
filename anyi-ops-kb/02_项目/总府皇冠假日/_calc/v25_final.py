
# -*- coding: utf-8 -*-
"""v25 终检与归档：修目录表首行 → 重出 Word → 归档 → 清桌面"""
import io, os, sys, re, glob, shutil, subprocess, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
CALC=r'D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc'
KB=r'D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日'
TGT=r'C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店'
REP=os.path.join(TGT,'改造报告交付'); CO=os.path.join(TGT,'测算与中间产物')
PY=r'C:\Users\ericz\AppData\Local\Programs\Python\Python314\python.exe'
ENV=dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONUTF8='1')
F=os.path.join(KB,'总府皇冠改造_可行性研究报告_v25.0_2026-11-16.md')
T=io.open(F,encoding='utf-8').read()
L=T.split('\n')
# 定位目录表：含「章 | 标题 | 本章回答的问题」的表
for i,l in enumerate(L):
    if l.startswith('| 章 |'):
        hdr=l; sep=L[i+1]; first=L[i+2]
        print('目录表 L%d  首行: %s' % (i+2, first[:120]))
        cells=first.split('|')
        if len(cells)>2 and cells[1].strip()=='':
            cells[1]=' 0 '
            L[i+2]='|'.join(cells); print('  → 已补 0')
        break
T='\n'.join(L)
io.open(F,'w',encoding='utf-8').write(T)
# 重出 Word
r=subprocess.run([PY,os.path.join(CALC,'v25_docx.py')],capture_output=True,text=True,encoding='utf-8',errors='replace',env=ENV,timeout=1800)
print('docx rc=',r.returncode)
if r.returncode: print((r.stderr or '')[-500:])
LOG=io.open(os.path.join(r'D:\B166ER-openclaw\workspace\.tmp','v17.log'),encoding='utf-8').read()
print('--- docx 终检 ---')
for l in LOG.split('\n'):
    if l.startswith('BLANK') or 'paragraph' in l or 'emoji' in l or 'DONE' in l or l.startswith('\u6bb5') or l.startswith('绔'):
        pass
import re as _re
for l in LOG.split('\n')[-8:]: print('   ',l)
