# -*- coding: utf-8 -*-
import io, sys, os, re, json, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
ARC = os.path.join(ROOT,"skills","_archive","idle_2026-11-18")
print("=== 归档目录是否存在:", os.path.isdir(ARC))
if os.path.isdir(ARC):
    items = sorted(os.listdir(ARC))
    print("  条目 %d:" % len(items))
    for i in items: print("    ", i)
MAN = os.path.join(ROOT,"output","audit_skills","idle_archive_manifest_2026-11-18.json")
print()
print("=== 清单落盘:", os.path.exists(MAN))
if os.path.exists(MAN):
    m = json.load(open(MAN, encoding="utf-8"))
    print("  已归档 %d 份" % len(m.get("archived",[])))
    for a in m.get("archived",[]): print("    %-26s %-7s %s" % (a["name"][:26], a["loc"], a["to"][:60]))
print()
print("=== 我今天新建的 5 个技能现在在哪 ===")
for n in ["self-check-assertions","skill-registry-router","evolution-scan","doc-encoding-repair","topology-infographic"]:
    hits = []
    for base in [os.path.join(ROOT,"skills"), os.path.join(HOME,"skills"), os.path.join(HOME,".claude","skills")]:
        p = os.path.join(base,n,"SKILL.md")
        if os.path.exists(p): hits.append(p)
        if os.path.isdir(ARC):
            for q in glob.glob(os.path.join(ARC,"*"+n,"SKILL.md")): hits.append(q)
    print("  %-26s %s" % (n, hits if hits else "★ 找不到"))
