# -*- coding: utf-8 -*-
import io, os, sys, re
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
LOG = open(r"D:\B166ER-openclaw\workspace\.tmp\struct.log", "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
for fn in ("总府皇冠改造_整体方案报告_v1.0_2026-11-13.md",
           "总府皇冠改造_可行性研究报告_公文版_v1.0_2026-11-09.md"):
    p = os.path.join(KB, fn)
    L("=" * 90)
    L("FILE:", fn, os.path.getsize(p) if os.path.exists(p) else "MISSING")
    if not os.path.exists(p):
        continue
    t = open(p, encoding="utf-8").read()
    for i, l in enumerate(t.split("\n"), 1):
        if re.match(r"^#{1,4} ", l):
            L("  L%-5d %s" % (i, l[:96]))
