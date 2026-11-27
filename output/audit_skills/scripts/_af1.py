# -*- coding: utf-8 -*-
import io, sys, os, re, glob
from PIL import Image
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = r'D:\B166ER-openclaw\workspace'
SRC = r'D:\B166ER-openclaw\workspace\media\inbound\openclaw-staged-ebdea283-4b35-4097-8dec-2a642a2a9045\input-image---1b1867e8-83f2-444a-9521-5d7babc81278.png'
OUT = os.path.join(ROOT, 'output', 'award_form')
os.makedirs(OUT, exist_ok=True)
im = Image.open(SRC).convert('RGB')
W, H = im.size
print('origin size:', W, 'x', H)
print('--- KB scan: 设计酒店奖 / 安逸设计资产 ---')
KW = ['设计酒店', 'THE BUD', 'BUD DESIGN', '年度设计', '酒店设计奖', 'AHEAD', 'WAF', 'ADN', 'CHINESE HOTEL DESIGN', '侘寂', '留白', '美学', '设计感', '年度设计酒店']
files = glob.glob(os.path.join(ROOT, 'anyi-ops-kb', '**', '*.md'), recursive=True)
files += glob.glob(os.path.join(ROOT, 'memory', '*.md'))
cnt = 0
for p in files:
    try: t = open(p, encoding='utf-8', errors='replace').read()
    except Exception: continue
    hs = [k for k in KW if k in t]
    if len(hs) >= 3:
        print('   %-72s %s' % (os.path.relpath(p, ROOT).replace(os.sep,'/')[-72:], ','.join(hs[:6])))
        cnt += 1
        if cnt >= 14: break
print('   命中文件:', cnt)
print('--- crop into bands ---')
target_w = 1500
scale = target_w / float(W) if W < target_w else 1.0
nband = 5
bh = H // nband
for i in range(nband):
    y0 = i * bh
    y1 = H if i == nband-1 else (i+1)*bh + 24
    c = im.crop((0, y0, W, y1))
    if scale != 1.0:
        c = c.resize((int(c.width*scale), int(c.height*scale)), Image.LANCZOS)
    p = os.path.join(OUT, 'band%d.png' % i)
    c.save(p)
    print('   band%d  y=%d..%d  %s  %d B' % (i, y0, y1, c.size, os.path.getsize(p)))
print('OUT:', OUT)