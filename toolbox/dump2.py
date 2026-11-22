# -*- coding: utf-8 -*-
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
fp = r'D:\B166ER-openclaw\workspace\anyi-ops-kb\07_战略与改革\集团战略文件\省旅投十五五规划_送审稿_全文_v1.0_2026-10-21.txt'
t = open(fp, encoding='utf-8').read()
pages = t.split('===== P')
def dump(a,b,label,lim=2200):
    print('\n########', label)
    for pg in pages:
        if not pg.strip(): continue
        try: num=int(pg.split('=====')[0])
        except: continue
        if a<=num<=b:
            print('---P%d---' % num)
            print(pg.split('=====',1)[-1].strip()[:lim])
dump(24,30,'酒店运营管理')
dump(40,46,'重点任务',1800)