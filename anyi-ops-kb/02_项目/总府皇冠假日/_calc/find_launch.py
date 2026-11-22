# -*- coding: utf-8 -*-
import io, os, sys, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
def esc(s): return s.encode("unicode_escape").decode("ascii")

ROOTS = [r"D:\B166ER-openclaw\workspace", r"C:\Users\ericz\Desktop"]
hits = []
for root in ROOTS:
    for dirpath, dirs, files in os.walk(root):
        for f in files:
            p = os.path.join(dirpath, f)
            try:
                sz = os.path.getsize(p)
            except Exception:
                continue
            if f.lower().endswith(".md") and 22000 < sz < 25000:
                hits.append((sz, p))
            if f.lower().endswith(".md") and 59000 < sz < 62000:
                hits.append((sz, p))
print("=== 按大小命中（22-25KB / 59-62KB 的 .md）===")
for sz, p in sorted(hits):
    print("  %8d  %s" % (sz, esc(p)))

print("\n=== 含'立项报告'字样的 .md（全盘，扫前 200KB）===")
found = 0
for root in ROOTS:
    for dirpath, dirs, files in os.walk(root):
        for f in files:
            if not f.lower().endswith(".md"): continue
            p = os.path.join(dirpath, f)
            try:
                if os.path.getsize(p) > 400000: continue
                t = open(p, encoding="utf-8", errors="ignore").read(60000)
            except Exception:
                continue
            if "立项报告" in t:
                print("  HIT %8d %s" % (os.path.getsize(p), esc(p)))
                found += 1
print("  命中数:", found)
