# -*- coding: utf-8 -*-
import io, sys, os, re, glob, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
WS = r'D:\B166ER-openclaw\workspace'
KB = os.path.join(WS, 'anyi-ops-kb')
DESK = r'C:\Users\ericz\Desktop'

print('=== 1. 全盘含 STR 的文件名 + 修改时间 ===')
res = []
for root in (KB, DESK):
    for p in glob.glob(os.path.join(root, '**', '*'), recursive=True):
        if os.path.isfile(p) and 'STR' in os.path.basename(p):
            res.append((os.path.getmtime(p), p, os.path.getsize(p)))
res.sort(reverse=True)
for m, p, sz in res[:25]:
    print('  %s  %7d KB  %s' % (time.strftime('%m-%d %H:%M', time.localtime(m)), sz // 1024, p.replace(WS, 'WS').replace(DESK, 'DESK')[:105]))

print('')
print('=== 2. 11-18 以后修改过、且正文含 STR 的文件 ===')
cut = time.mktime(time.strptime('2026-11-18', '%Y-%m-%d'))
hits = []
for root in (KB, DESK):
    for p in glob.glob(os.path.join(root, '**', '*.md'), recursive=True):
        try:
            m = os.path.getmtime(p)
        except Exception:
            continue
        if m < cut:
            continue
        try:
            t = open(p, encoding='utf-8', errors='replace').read()
        except Exception:
            continue
        if 'STR' in t:
            hits.append((m, p, t.count('STR')))
hits.sort(reverse=True)
for m, p, c in hits[:15]:
    print('  %s  STR×%-4d %s' % (time.strftime('%m-%d %H:%M', time.localtime(m)), c, p.replace(WS, 'WS').replace(DESK, 'DESK')[:100]))
if not hits:
    print('  （无）')

print('')
print('=== 3. STR 跟踪表 v1.2 结构与维度 ===')
p = os.path.join(KB, '00_全域商业市场认知', '01_酒店行业', 'STR中国酒店月度RevPAR跟踪表_v1.2_2026-11-10.md')
if os.path.exists(p):
    t = open(p, encoding='utf-8', errors='replace').read()
    print('  长度 %d 字符' % len(t))
    for l in t.split('\n'):
        s = l.strip()
        if s.startswith('#'):
            print('   ' + s[:104])
    print('  --- 表格头与首行 ---')
    n = 0
    for l in t.split('\n'):
        s = l.strip()
        if s.startswith('|'):
            print('   ' + s[:190]); n += 1
            if n >= 12:
                break
else:
    print('  !! 缺失')
