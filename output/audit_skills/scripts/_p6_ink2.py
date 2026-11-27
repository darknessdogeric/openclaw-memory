# -*- coding: utf-8 -*-
"""深色主题 亮度带核查 + 联络表"""
import os, sys, glob
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from PIL import Image

D = r"C:\Users\ericz\Desktop\小红书_先驱者系列6图_2026-11-01"
files = sorted(glob.glob(os.path.join(D, "*.png")))

def bands(P, B=16):
    im = Image.open(P).convert("RGB")
    W, H = im.size
    px = im.load()
    out = []
    for b in range(B):
        y0, y1 = int(H*b/B), int(H*(b+1)/B)
        mx = 0
        bright = tot = 0
        for y in range(y0, y1, 4):
            for x in range(0, W, 4):
                r, g, bl = px[x, y]
                tot += 1
                lum = 0.299*r + 0.587*g + 0.114*bl
                if lum > mx:
                    mx = lum
                if lum > 110:
                    bright += 1
        out.append((mx, bright/max(tot,1)))
    return out

for f in files:
    bs = bands(f)
    mx = max(b[0] for b in bs)
    lo = min(bs[1:-1], key=lambda t: t[1])
    print("  %-18s 全图最亮 %.0f  最空带(亮像素 %.2f%%, 峰值亮度 %.0f) @band %d"
          % (os.path.basename(f), mx, lo[1]*100, lo[0], bs.index(lo)))

tw, th = 320, 569
sheet = Image.new("RGB", (tw*3 + 4*10, th*2 + 3*10), (18, 20, 27))
for i, f in enumerate(files[:6]):
    im = Image.open(f).convert("RGB").resize((tw, th), Image.LANCZOS)
    x = 10 + (i % 3) * (tw + 10)
    y = 10 + (i // 3) * (th + 10)
    sheet.paste(im, (x, y))
out = r"D:\B166ER-openclaw\workspace\memory\小红书海报\头像预览\_p6_sheet.png"
sheet.save(out)
print("sheet:", sheet.size, os.path.getsize(out), "bytes")
