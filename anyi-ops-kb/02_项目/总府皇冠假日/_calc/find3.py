# -*- coding: utf-8 -*-
import io, os, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
def esc(s): return s.encode("unicode_escape").decode("ascii")
TARGET = 60568
ROOTS = [r"C:\Users\ericz\Desktop\产业发展部", r"C:\Users\ericz\Documents",
         r"C:\Users\ericz\Downloads", r"C:\Users\ericz\AppData\Local\Temp",
         r"D:\B166ER-openclaw"]
print("=== 找 %d 字节 / 或 23,803 字节 的 md ===" % TARGET)
hit = []
for root in ROOTS:
    if not os.path.isdir(root):
        continue
    for dirpath, dirs, files in os.walk(root):
        for f in files:
            if not f.lower().endswith(".md"):
                continue
            p = os.path.join(dirpath, f)
            try:
                sz = os.path.getsize(p)
            except Exception:
                continue
            if sz in (TARGET, 23803) or 60000 < sz < 61200:
                hit.append((sz, p))
for sz, p in hit:
    print("  %8d %s" % (sz, esc(p)))
print("命中:", len(hit))
