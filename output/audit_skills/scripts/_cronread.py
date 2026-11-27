# -*- coding: utf-8 -*-
import io, sys, os, re, glob, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
D = r"C:\Users\ericz\self-improving"
for fn in ["cron_anomaly_log.md", "history.md"]:
    p = os.path.join(D, fn)
    print("=" * 88); print("### %s" % fn); print("=" * 88)
    if not os.path.exists(p):
        print("  不存在"); continue
    print(open(p, encoding="utf-8", errors="replace").read()[:3600])
    print()
print("=" * 88); print("### eval 记录时间线（间隔是否规律）"); print("=" * 88)
fs = sorted(glob.glob(os.path.join(D, "eval", "*.json")))
for f in fs:
    b = os.path.basename(f)
    if re.match(r"^\d{4}-\d{2}-\d{2}\.json$", b):
        print("   %s" % b)
print()
print("=" * 88); print("### rules.md 里的 cron/自进化 调度规则"); print("=" * 88)
rt = open(os.path.join(D, "rules.md"), encoding="utf-8", errors="replace").read()
for i, l in enumerate(rt.split("\n")):
    if re.search(r"(cron|定时|每小时|自进化.*触发|唤醒)", l) and len(l.strip()) > 6:
        print("   L%-5d %s" % (i+1, l.strip()[:150]))
