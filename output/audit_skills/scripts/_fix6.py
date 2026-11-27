# -*- coding: utf-8 -*-
import io, sys, os, re, json, glob, shutil as sh, ast, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
AUD = os.path.join(ROOT,"output","audit_skills")
SC = os.path.join(ROOT,"toolbox","selfcheck.py")

# ---------- 1. 注册表（祖先判据 + 排除 _ 开头） ----------
def real_skills(base):
    out = {}
    if not os.path.isdir(base): return out
    for f in sorted(glob.glob(os.path.join(base,"**","SKILL.md"), recursive=True)):
        d = os.path.dirname(f); rel = os.path.relpath(d, base).split(os.sep)
        if any(x.startswith("_") for x in rel): continue
        anc = rel[:-1]
        if any(os.path.exists(os.path.join(base, *anc[:i+1], "SKILL.md")) for i in range(len(anc))): continue
        tx = open(f, encoding="utf-8", errors="replace").read()
        fm = {}
        if tx.startswith("---"):
            e = tx.find("\n---", 3)
            if e > 0:
                for line in tx[3:e].split("\n"):
                    if ":" in line:
                        k,v = line.split(":",1); fm[k.strip().lower()] = v.strip().strip("\"'")
        nm = fm.get("name") or os.path.basename(d)
        out[nm] = {"dir":os.path.basename(d),"path":f,"desc":fm.get("description",""),
                   "scripts":len(glob.glob(os.path.join(d,"scripts","*.py"))),
                   "refs":len(glob.glob(os.path.join(d,"references","*.md"))),
                   "bytes":len(tx),
                   "files":len([x for x in glob.glob(os.path.join(d,"**","*"),recursive=True) if os.path.isfile(x)])}
    return out
LOCS = [("WS",os.path.join(ROOT,"skills")),("HOME",os.path.join(HOME,"skills")),("CLAUDE",os.path.join(HOME,".claude","skills"))]
reg = {}
for lab, base in LOCS:
    for nm, i in real_skills(base).items():
        reg.setdefault(nm, {"name":nm,"locs":{}})["locs"][lab] = i
def canon(e):
    for lab in ("WS","CLAUDE","HOME"):
        if lab in e["locs"]: return lab, e["locs"][lab]
    return "WS", list(e["locs"].values())[0]

# ---------- 2. 依赖就绪（真判据） ----------
EXT = re.compile(r"\b(arkcli|gstack|npx|npm|uv|docker|pip|brew)\b", re.I)
READY = {"node","npm","npx","uv","docker","git"}     # 已就绪
PLATFORM_NA = {"brew","pip"}                          # pip 用 python -m；brew 是 macOS 专属
def deps_of(d):
    deps = set()
    for f in glob.glob(os.path.join(d,"**","*"), recursive=True):
        if not os.path.isfile(f): continue
        try:
            if os.path.getsize(f) > 400000: continue
            t = open(f, encoding="utf-8", errors="replace").read()
        except Exception: continue
        for m in EXT.finditer(t): deps.add(m.group(1).lower())
    return deps
print("="*100); print("### A. 依赖就绪（真判据）"); print("="*100)
missing_bin = sorted({x for r in reg.values() for l,i in r["locs"].items()
                       for x in deps_of(os.path.dirname(i["path"])) if x not in READY and x not in PLATFORM_NA})
print("  真缺外部二进制: %s" % (", ".join(missing_bin) if missing_bin else "无"))
print("  ★ pip（用 python -m pip，rc=0）｜ brew（macOS 专属，Windows 不适用）→ 均不算缺依赖")

# ---------- 3. 语料（是否被真实调用） ----------
CORPUS = []
for pat in [os.path.join(ROOT,"memory","*.md"), os.path.join(HOME,"self-improving","**","*.md"),
            os.path.join(ROOT,"anyi-ops-kb","**","*.md")]:
    for f in glob.glob(pat, recursive=True):
        try: CORPUS.append(open(f, encoding="utf-8", errors="replace").read()[:200000])
        except Exception: pass
blob = "\n".join(CORPUS)

rows = []; verdict = []
for nm, e in reg.items():
    lab, i = canon(e)
    deps = deps_of(os.path.dirname(i["path"]))
    blocking = sorted(x for x in deps if x not in READY and x not in PLATFORM_NA)
    called = blob.count(nm) > 0
    has_exec = i["scripts"] > 0 or i["files"] > 3
    if called:
        act, vs = "active", "已被语料调用"
    elif blocking:
        act, vs = "hold", "缺 %s —— 保留待装，装上即激活" % ", ".join(blocking)
    elif not has_exec:
        act, vs = "archive", "从未被调用且无脚本无依赖（纯说明文档）—— 归档"
    else:
        act, vs = "activate", "依赖就绪、有可执行件，但未被调用 —— 纳入固定工作流以激活"
    rows.append({"name":nm,"canonical":i["path"],"canonical_loc":lab,"desc":i["desc"],
                 "scripts":i["scripts"],"refs":i["refs"],"bytes":i["bytes"],"files":i["files"],
                 "all_locs":sorted(e["locs"].keys()),"has_desc":bool(i["desc"]),
                 "status":act,"idle_verdict":vs if act!="active" else ""})
    if act != "active":
        verdict.append({"name":nm,"deps":sorted(deps),"blocking":blocking,"action":act,"verdict":vs,
                        "locs":sorted(e["locs"].keys()),"bytes":i["bytes"]})
rows.sort(key=lambda r:r["name"].lower())
ac = {}
for v in verdict: ac[v["action"]] = ac.get(v["action"],0)+1
print()
print("  技能 %d ｜ 活跃 %d ｜ 闲置裁决 %d: %s" % (len(rows), len(rows)-len(verdict), len(verdict), ac))
for a in ("archive","activate","hold"):
    g = [v for v in verdict if v["action"]==a]
    if not g: continue
    print("   【%s】%d 个" % (a, len(g)))
    for v in g[:14]: print("      %-28s %s" % (v["name"][:28], v["verdict"][:58]))

# ---------- 4. 执行归档（全部位置一起搬，避免同技能换处冒出来） ----------
print()
print("="*100); print("### B. 执行归档"); print("="*100)
ARC = os.path.join(ROOT,"skills","_archive","idle_2026-11-18")
os.makedirs(ARC, exist_ok=True)
moved = []
for v in verdict:
    if v["action"] != "archive": continue
    for lab in v["locs"]:
        base = dict(LOCS)[lab]
        d = os.path.dirname([r for r in rows if r["name"]==v["name"]][0]["canonical"]) if lab=="WS" else None
        # 逐位置定位该技能目录
        for f in glob.glob(os.path.join(base,"**","SKILL.md"), recursive=True):
            rel = os.path.relpath(os.path.dirname(f), base).split(os.sep)
            if any(x.startswith("_") for x in rel): continue
            anc = rel[:-1]
            if any(os.path.exists(os.path.join(base,*anc[:i+1],"SKILL.md")) for i in range(len(anc))): continue
            tx = open(f, encoding="utf-8", errors="replace").read()
            m = re.search(r"^name:\s*%s\s*$" % re.escape(v["name"]), tx, re.M)
            nm2 = m.group(1) if m else rel[-1]
            if nm2 != v["name"]: continue
            src = os.path.dirname(f)
            dst = os.path.join(ARC, lab+"__"+os.path.basename(src))
            if os.path.exists(dst): continue
            shutil.move(src, dst)
            moved.append({"name":v["name"],"loc":lab,"from":os.path.relpath(src,ROOT).replace(os.sep,"/"),
                          "to":os.path.relpath(dst,ROOT).replace(os.sep,"/"),"bytes":v["bytes"]})
print("  已归档 %d 份（跨 %d 个位置）→ skills/_archive/idle_2026-11-18/" % (len(moved), len({m['name'] for m in moved})))
for m in moved[:20]: print("     %-26s %-7s %s" % (m["name"][:26], m["loc"], m["to"]))
json.dump({"date":"2026-11-18","rule":"闲置且无脚本无依赖 → 归档（可回滚：移回原位）","archived":moved},
          open(os.path.join(AUD,"idle_archive_manifest_2026-11-18.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------- 5. 重建注册表（归档后） ----------
reg2 = {}
for lab, base in LOCS:
    for nm, i in real_skills(base).items():
        reg2.setdefault(nm, {"name":nm,"locs":{}})["locs"][lab] = i
st = {r["name"]: (r["status"], r["idle_verdict"]) for r in rows}
rows2 = []
for nm, e in reg2.items():
    lab, i = canon(e)
    s, v = st.get(nm, ("active",""))
    rows2.append({"name":nm,"canonical":i["path"],"canonical_loc":lab,"desc":i["desc"],
                  "scripts":i["scripts"],"refs":i["refs"],"bytes":i["bytes"],"files":i["files"],
                  "all_locs":sorted(e["locs"].keys()),"has_desc":bool(i["desc"]),
                  "status":s,"idle_verdict":v})
rows2.sort(key=lambda r:r["name"].lower())
json.dump(rows2, open(os.path.join(AUD,"SKILL_REGISTRY.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(verdict, open(os.path.join(AUD,"IDLE_VERDICT.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("  注册表重建: %d 条 ｜ active %d" % (len(rows2), sum(1 for r in rows2 if r["status"]=="active")))

# ---------- 6. 修 C14 的 _archive 排除 ----------
t = open(SC, encoding="utf-8", errors="replace").read()
if 'if any(x.startswith("_") for x in rel):' not in t:
    old = '''            d = os.path.dirname(f)
            anc = os.path.relpath(d, base).split(os.sep)[:-1]
            if any(os.path.exists(os.path.join(base, *anc[:i+1], "SKILL.md")) for i in range(len(anc))):
                continue'''
    new = '''            d = os.path.dirname(f)
            rel = os.path.relpath(d, base).split(os.sep)
            if any(x.startswith("_") for x in rel):
                continue
            anc = rel[:-1]
            if any(os.path.exists(os.path.join(base, *anc[:i+1], "SKILL.md")) for i in range(len(anc))):
                continue'''
    assert old in t, "C14 原文未命中"
    t = t.replace(old, new, 1)
    ast.parse(t)
    open(SC,"w",encoding="utf-8",newline="\n").write(t)
    print("  ✔ C14 已排除 _ 开头目录")

print()
r = subprocess.run([sys.executable, SC], capture_output=True, timeout=400)
print(r.stdout.decode("utf-8","replace"))
print("退出码:", r.returncode)
