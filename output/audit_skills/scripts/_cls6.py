# -*- coding: utf-8 -*-
import io, sys, os, re, glob, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")

print("="*100); print("### A. selfcheck.py 结构（要往里加断言）"); print("="*100)
sc = os.path.join(ROOT,"toolbox","selfcheck.py")
t = open(sc, encoding="utf-8", errors="replace").read()
print("  %d B ｜ %d 行" % (len(t), t.count("\n")+1))
for i,l in enumerate(t.split("\n")):
    if re.match(r"^\s*(def |class |CHECKS|CHECK |assert_|# ---|RESULT|\{)", l) or re.search(r"\"C\d\d\"|'C\d\d'|C\d\d", l):
        print("  L%-4d %s" % (i+1, l[:150]))

print()
print("="*100); print("### B. 重建技能注册表（含 5 个新技能）"); print("="*100)
WS = os.path.join(ROOT,"skills")
def skill_roots(base):
    out = {}
    if not os.path.isdir(base): return out
    for f in sorted(glob.glob(os.path.join(base,"*","SKILL.md"))):
        d = os.path.basename(os.path.dirname(f))
        if d in ("examples","variants","references","scripts","templates","assets","docs","plugins","_archive"): continue
        tx = open(f, encoding="utf-8", errors="replace").read()
        fm = {}
        if tx.startswith("---"):
            e = tx.find("\n---", 3)
            if e > 0:
                for line in tx[3:e].split("\n"):
                    if ":" in line:
                        k,v = line.split(":",1); fm[k.strip().lower()] = v.strip().strip("\"'")
        nm = fm.get("name") or d
        out[nm] = {"dir":d,"path":f,"desc":fm.get("description",""),
                   "scripts":len(glob.glob(os.path.join(os.path.dirname(f),"scripts","*.py"))),
                   "refs":len(glob.glob(os.path.join(os.path.dirname(f),"references","*.md"))),
                   "bytes":len(tx),
                   "files":len([x for x in glob.glob(os.path.join(os.path.dirname(f),"**","*"),recursive=True) if os.path.isfile(x)])}
    return out
LOCS = [("WS",WS),("HOME",os.path.join(HOME,"skills")),("CLAUDE",os.path.join(HOME,".claude","skills"))]
reg = {}
for lab, base in LOCS:
    for nm, info in skill_roots(base).items():
        reg.setdefault(nm, {"name":nm,"locs":{}})["locs"][lab] = info
def canon(e):
    for lab in ("WS","CLAUDE","HOME"):
        if lab in e["locs"]: return lab, e["locs"][lab]
    return "WS", list(e["locs"].values())[0]
rows = []
for nm, e in reg.items():
    lab, i = canon(e)
    rows.append({"name":nm,"canonical":i["path"],"canonical_loc":lab,"desc":i["desc"],
                 "scripts":i["scripts"],"refs":i["refs"],"bytes":i["bytes"],"files":i["files"],
                 "all_locs":sorted(e["locs"].keys()),"has_desc":bool(i["desc"])})
rows.sort(key=lambda r:(r["name"].lower()))
REG = os.path.join(ROOT,"output","audit_skills","SKILL_REGISTRY.json")
json.dump(rows, open(REG,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
by = {}
for r in rows:
    for l in r["all_locs"]: by[l] = by.get(l,0)+1
print("  技能总数: %d ｜ 各位置 %s ｜ 无描述 %d" % (len(rows), by, sum(1 for r in rows if not r["has_desc"])))
new5 = ["self-check-assertions","skill-registry-router","evolution-scan","doc-encoding-repair","topology-infographic",
        "writing-evals","autoreview","technical-documentation"]
for n in new5:
    hit = [r for r in rows if r["name"]==n]
    print("   %-26s %s" % (n, ("✔ 已入表 desc=%d字" % len(hit[0]["desc"])) if hit else "★ 未入表"))
