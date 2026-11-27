# -*- coding: utf-8 -*-
import io, sys, os, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = r'D:\B166ER-openclaw\workspace'
SRC = r'D:\B166ER-openclaw\workspace\media\inbound\openclaw-staged-ebdea283-4b35-4097-8dec-2a642a2a9045\input-image---1b1867e8-83f2-444a-9521-5d7babc81278.png'
OUT = os.path.join(ROOT, 'output', 'award_form')
os.makedirs(OUT, exist_ok=True)
from PIL import Image
from rapidocr_onnxruntime import RapidOCR
engine = RapidOCR()
im = Image.open(SRC).convert('RGB')
W, H = im.size
print('size', W, H)
allrows = []
nband = 6
bh = H // nband
for i in range(nband):
    y0 = i * bh
    y1 = H if i == nband-1 else (i+1)*bh + 40
    c = im.crop((0, y0, W, y1))
    c = c.resize((W*2, (y1-y0)*2), Image.LANCZOS)
    p = os.path.join(OUT, 'rband%d.png' % i)
    c.save(p)
    res, elapse = engine(p)
    print('--- band %d (y=%d..%d) lines=%s ---' % (i, y0, y1, (len(res) if res else 0)))
    if not res: continue
    rows = sorted(res, key=lambda r: (r[0][0][1], r[0][0][0]))
    for box, txt, conf in rows:
        cy = int(box[0][1]/2) + y0
        cx = int(box[0][0]/2)
        allrows.append((cy, cx, txt, round(float(conf),3)))
allrows.sort(key=lambda r: (r[0], r[1]))
outp = os.path.join(OUT, 'ocr_full.txt')
with open(outp, 'w', encoding='utf-8', newline='\n') as f:
    for cy, cx, txt, conf in allrows:
        f.write('[y=%4d x=%4d c=%.2f] %s\n' % (cy, cx, conf, txt))
print()
print('rows total:', len(allrows), '->', outp, os.path.getsize(outp), 'B')
print('=' * 90)
for cy, cx, txt, conf in allrows:
    print('%4d | %s' % (cy, txt))