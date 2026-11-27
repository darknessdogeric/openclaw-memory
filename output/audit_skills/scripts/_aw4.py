# -*- coding: utf-8 -*-
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = r'D:\B166ER-openclaw\workspace'
SRC = r'D:\B166ER-openclaw\workspace\media\inbound\openclaw-staged-ebdea283-4b35-4097-8dec-2a642a2a9045\input-image---1b1867e8-83f2-444a-9521-5d7babc81278.png'
OUT = os.path.join(ROOT, 'output', 'award_form')
from PIL import Image
from rapidocr_onnxruntime import RapidOCR
engine = RapidOCR()
im = Image.open(SRC).convert('RGB')
W = im.size[0]
print('=== A. 艺术人文类前两项 8x 精读 ===')
c = im.crop((0, 4290, W, 4470)).resize((W*8, 180*8), Image.LANCZOS)
p = os.path.join(OUT, 'z8_art1.png')
c.save(p)
res, el = engine(p)
for box, txt, conf in sorted(res, key=lambda r: (r[0][0][1], r[0][0][0])):
    print('   c=%.2f  %s' % (float(conf), txt))
print()
print('=== B. 顶部声明区 8x 精读 ===')
c = im.crop((0, 940, W, 1060)).resize((W*8, 120*8), Image.LANCZOS)
p2 = os.path.join(OUT, 'z8_head.png')
c.save(p2)
res2, el2 = engine(p2)
for box, txt, conf in sorted(res2, key=lambda r: (r[0][0][1], r[0][0][0])):
    print('   c=%.2f  %s' % (float(conf), txt))