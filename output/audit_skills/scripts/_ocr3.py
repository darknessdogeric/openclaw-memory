# -*- coding: utf-8 -*-
import io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = r'D:\B166ER-openclaw\workspace'
SRC = r'D:\B166ER-openclaw\workspace\media\inbound\openclaw-staged-ebdea283-4b35-4097-8dec-2a642a2a9045\input-image---1b1867e8-83f2-444a-9521-5d7babc81278.png'
OUT = os.path.join(ROOT, 'output', 'award_form')
from PIL import Image
from rapidocr_onnxruntime import RapidOCR
engine = RapidOCR()
im = Image.open(SRC).convert('RGB')
W, H = im.size
REGIONS = [('design', 2020, 2580), ('art', 4220, 5000), ('boutique', 5400, 5990), ('lux', 3020, 3760), ('head', 780, 1100)]
for tag, y0, y1 in REGIONS:
    c = im.crop((0, y0, W, y1))
    k = 3
    c = c.resize((W*k, (y1-y0)*k), Image.LANCZOS)
    p = os.path.join(OUT, 'zoom_%s.png' % tag)
    c.save(p)
    res, el = engine(p)
    print('=== %s (y=%d..%d) %d lines ===' % (tag, y0, y1, len(res) if res else 0))
    if not res: continue
    rows = sorted(res, key=lambda r: (r[0][0][1], r[0][0][0]))
    for box, txt, conf in rows:
        cy = int(box[0][1]/k) + y0
        print('   %4d  c=%.2f  %s' % (cy, float(conf), txt))
    print()