# -*- coding: utf-8 -*-
import os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from PIL import Image
P = r"C:\Users\ericz\Desktop\小红书_生物层面的危险_9x16_2026-11-01\生物层面的危险_9x16.png"
im = Image.open(P).convert("RGB")
W, H = im.size
print("size:", W, H, "ratio 1:%.3f" % (H/W))
px = im.load()
B = 16
worst = 1.0
wb = -1
for b in range(B):
    y0 = int(H*b/B)
    y1 = int(H*(b+1)/B)
    ink = 0
    tot = 0
    for y in range(y0, y1, 4):
        for x in range(0, W, 4):
            r, g, bl = px[x, y]
            tot += 1
            if r < 235 or g < 228 or bl < 214:
                ink += 1
    cov = ink / max(tot, 1)
    flag = ""
    if cov < 0.02 and 0 < b < B-1:
        flag = "<== 空带"
        if cov < worst:
            worst = cov
            wb = b
    print("%2d %5d-%5d  %6.2f%%  %s" % (b, y0, y1, cov*100, flag))
print("最大空带:", ("band %d  %.2f%%" % (wb, worst*100)) if wb >= 0 else "无")
print("file:", os.path.basename(P), os.path.getsize(P), "bytes")
