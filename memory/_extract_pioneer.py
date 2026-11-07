# -*- coding: utf-8 -*-
import os, sys, re, glob
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from PIL import Image

D = r"C:\Users\ericz\Desktop\小红书_先驱者系列_2026-10-24"
print("=== PNG 尺寸 ===")
for f in sorted(glob.glob(os.path.join(D, "*.png"))):
    im = Image.open(f)
    print("  %-22s %d x %d  ratio 1:%.3f" % (os.path.basename(f), im.width, im.height, im.height/im.width))

h = open(os.path.join(D, "先驱者_space.html"), encoding="utf-8").read()
print("=== html len:", len(h), "===")

print("=== 标题层级 ===")
for m in re.finditer(r"<(h1|h2|h3)[^>]*>(.*?)</\1>", h, re.S):
    t = re.sub(r"<[^>]+>", " ", m.group(2))
    t = re.sub(r"\s+", " ", t).strip()
    if t:
        print("  [%s] %s" % (m.group(1), t[:100]))

print("=== 图注 / 标签类 ===")
for cls in ("figt", "cap", "lbl", "tag", "kicker", "sub"):
    ms = re.findall(r"class=[\"\x27]" + cls + r"[\"\x27][^>]*>(.*?)<", h, re.S)
    vals = []
    for x in ms[:8]:
        v = re.sub(r"<[^>]+>", " ", x)
        v = re.sub(r"\s+", " ", v).strip()
        if v and v not in vals:
            vals.append(v)
    if vals:
        print("  ." + cls + ": " + " | ".join(v[:44] for v in vals[:8]))

print("=== 正文纯文本（前 5200 字，剥标签）===")
t = re.sub(r"<script.*?</script>", " ", h, flags=re.S)
t = re.sub(r"<style.*?</style>", " ", t, flags=re.S)
t = re.sub(r"<svg.*?</svg>", " ", t, flags=re.S)
t = re.sub(r"<[^>]+>", "\n", t)
t = re.sub(r"\n\s*\n+", "\n", t)
lines = [l.strip() for l in t.split("\n") if l.strip()]
print("\n".join(lines[:150]))
