# -*- coding: utf-8 -*-
import io, sys, os, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
SI = os.path.join(HOME,"self-improving")
p = os.path.join(SI,"corrections.md")
t = open(p, encoding="utf-8", errors="replace").read()
print("=== corrections.md 尾部格式 (%d B) ===" % len(t))
print("\n".join(t.split("\n")[-24:]))
print()
print("=== domains 目录 ===")
for f in sorted(glob.glob(os.path.join(SI,"domains","*.md"))):
    print("  %8d B  %s" % (os.path.getsize(f), os.path.basename(f)))
print()
print("=== 今日/昨日日记 ===")
for d in ["2026-11-17.md","2026-11-18.md"]:
    f = os.path.join(ROOT,"memory",d)
    print("  %-16s 存在=%s %s" % (d, os.path.exists(f), (str(os.path.getsize(f))+" B") if os.path.exists(f) else ""))
