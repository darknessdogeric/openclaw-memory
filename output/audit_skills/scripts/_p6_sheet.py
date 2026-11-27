# -*- coding: utf-8 -*-
"""深色主题像素带核查 + 联络表"""
import os, sys, glob
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from PIL import Image

D = r"C:\Users\ericz\Desktop\小红书_先驱者系列6图_2026-11-01"
files = sorted(glob.glob(os.path.join(D, "*.png")))

def bands(P, B=16):
    im = Image.open(P).convert("RGB")
    W, H = im.size
    px = im.load()
    res = []
    for b in range(B):
        y0, y1 = int(H*b/B), int(H*(b+1)/B)
        ink = tot = 0
        for y in range(y0, y1, 8):
            for x in range(0, W, 8):
                r, g, bl = px[x, y]
                tot += 1
                lum = 0.299*r + 0.587*g + 0.114*bl
                if lum > 88:
                    ink += 1
        res.append(ink / max(tot, 1))
    return res

for f in files:
    bs = bands(f)
    worst = min(bs[1:-1])
    print("  %-18s 最低带 %.2f%%  %s" % (os.path.basename(f), worst*100, ("@band %d" % (bs.index(worst))) if worst < 0.02 else "无空带"))

tw, th = 300, 533
sheet = Image.new("RGB", (tw*3 + 4*10, th*2 + 3*10), (18, 20, 27))
for i, f in enumerate(files[:6]):
    im = Image.open(f).convert("RGB").resize((tw, th), Image.LANCZOS)
    x = 10 + (i % 3) * (tw + 10)
    y = 10 + (i // 3) * (th + 10)
    sheet.paste(im, (x, y))
out = r"D:\B166ER-openclaw\workspace\memory\小红书海报\头像预览\_p6_sheet.png"
sheet.save(out)
print("sheet:", sheet.size, os.path.getsize(out), "bytes")
