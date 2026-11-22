# -*- coding: utf-8 -*-
import sys, io, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
root = r'D:\B166ER-openclaw\workspace\anyi-ops-kb'
hits=[]
for dp,dn,fs in os.walk(root):
    for f in fs:
        if not f.endswith(('.md','.txt')): continue
        p=os.path.join(dp,f)
        try: t=open(p,encoding='utf-8',errors='ignore').read()
        except: continue
        c=t.count('二销')
        if c: hits.append((c,p,t))
for c,p,t in sorted(hits,reverse=True)[:8]:
    print('='*15, c, p.split(chr(92))[-1])
    n=0
    for line in t.split('\n'):
        if '二销' in line:
            print('  ', line.strip()[:220]); n+=1
            if n>=6: break