# -*- coding: utf-8 -*-
import os, sys, re, glob
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

D = r"C:\Users\ericz\Desktop\小红书_先驱者系列_2026-10-24"
h = open(os.path.join(D, "先驱者_space.html"), encoding="utf-8").read()

print("=== SVG 内文本（板块 03 门 / 对比表）===")
for i, m in enumerate(re.finditer(r"<svg[^>]*>(.*?)</svg>", h, re.S)):
    inner = m.group(1)
    ts = re.findall(r"<text[^>]*>(.*?)</text>", inner, re.S)
    vals = []
    for x in ts:
        v = re.sub(r"<[^>]+>", "", x)
        v = re.sub(r"\s+", " ", v).strip()
        if v and v not in vals:
            vals.append(v)
    if vals:
        print("  [svg%d] %d 段文本:" % (i, len(vals)))
        print("     " + " | ".join(v[:30] for v in vals[:26]))
        print()

print("=== 对比表类容器（04）===")
for cls in ("row", "cell", "cmp", "tbl", "tl-item", "step"):
    ms = re.findall(r"class=[\"\x27]" + cls + r"[\"\x27][^>]*>(.*?)</div>", h, re.S)
    if len(ms) > 2:
        vals = []
        for x in ms[:26]:
            v = re.sub(r"<[^>]+>", " ", x)
            v = re.sub(r"\s+", " ", v).strip()
            if v and v not in vals:
                vals.append(v)
        print("  ." + cls + " (" + str(len(ms)) + "):")
        for v in vals[:18]:
            print("      " + v[:70])
        print()

print("=== HERO 图片是否存在 ===")
for p in glob.glob(r"D:\B166ER-openclaw\media\tool-image-generation\pioneer_hero*") + glob.glob(r"D:\B166ER-openclaw\media\**\*pioneer*", recursive=True):
    try:
        from PIL import Image
        im = Image.open(p)
        print("  %s  %d x %d  %d B" % (os.path.basename(p), im.width, im.height, os.path.getsize(p)))
    except Exception as e:
        print("  %s  ERR %s" % (os.path.basename(p), str(e)[:40]))
