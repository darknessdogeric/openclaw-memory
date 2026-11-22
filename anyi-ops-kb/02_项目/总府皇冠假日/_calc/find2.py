# -*- coding: utf-8 -*-
import io, os, sys, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
def esc(s): return s.encode("unicode_escape").decode("ascii")

P2 = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目"
print("=== 02_项目 下所有条目（ASCII 安全）===")
for e in sorted(os.listdir(P2)):
    print("  %-8s %s" % ("DIR" if os.path.isdir(os.path.join(P2, e)) else "FILE", esc(e)))

print("\n=== 各子目录内 .md 按大小找 23-24KB / 59-62KB ===")
for e in sorted(os.listdir(P2)):
    d = os.path.join(P2, e)
    if not os.path.isdir(d):
        continue
    for dirpath, dirs, files in os.walk(d):
        for f in files:
            if not f.lower().endswith(".md"):
                continue
            p = os.path.join(dirpath, f)
            try:
                sz = os.path.getsize(p)
            except Exception:
                continue
            if (22000 < sz < 25000) or (59000 < sz < 62000):
                print("  %8d %s" % (sz, esc(p)))
