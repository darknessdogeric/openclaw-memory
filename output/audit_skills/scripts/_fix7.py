# -*- coding: utf-8 -*-
import io, sys, os, re, json, glob, shutil as sh, ast, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
AUD = os.path.join(ROOT,"output","audit_skills")
SC  = os.path.join(ROOT,"toolbox","selfcheck.py")
WFP = os.path.join(AUD,"WORKFLOWS.json")

# ---------- 0. 完整性核验：确认无损失 ----------
print("="*100); print("### 0. 完整性核验（先确认没丢东西）"); print("="*100)
def real_skills(base):
    out = {}
    if not os.path.isdir(base): return out
    for f in sorted(glob.glob(os.path.join(base,"**","SKILL.md"), recursive=True)):
        d = os.path.dirname(f); rel = os.path.relpath(d, base).split(os.sep)
        if any(x.startswith("_") for x in rel): continue
        anc = rel[:-1]
        if any(os.path.exists(os.path.join(base,*anc[:i+1],"SKILL.md")) for i in range(len(anc))): continue
        tx = open(f, encoding="utf-8", errors="replace").read()
        fm = {}
        if tx.startswith("---"):
            e = tx.find("\n---",3)
            if e>0:
                for line in tx[3:e].split("\n"):
                    if ":" in line:
                        k,v = line.split(":",1); fm[k.strip().lower()]=v.strip().strip("\"'")
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
        reg.setdefault(nm,{"name":nm,"locs":{}})["locs"][lab]=i
def canon(e):
    for lab in ("WS","CLAUDE","HOME"):
        if lab in e["locs"]: return lab, e["locs"][lab]
    return "WS", list(e["locs"].values())[0]
print("  在库真技能: %d 个（归档目录空，未发生任何搬迁）" % len(reg))
for n in ["self-check-assertions","skill-registry-router","evolution-scan","doc-encoding-repair","topology-infographic","writing-evals","autoreview","technical-documentation"]:
    print("     %-26s %s" % (n, "✔ 在库" if n in reg else "★ 丢失"))

# ---------- 1. 硬护栏：受保护集合 ----------
PROTECT = {"self-check-assertions","skill-registry-router","evolution-scan","doc-encoding-repair",
           "topology-infographic","writing-evals","autoreview","technical-documentation"}
WF = json.load(open(WFP, encoding="utf-8"))
wfblob = json.dumps(WF, ensure_ascii=False)
for w in WF:
    for tok in re.findall(r"[A-Za-z0-9][A-Za-z0-9\-\.]{2,}", w.get("skills","")):
        if tok in reg: PROTECT.add(tok)
sct = open(SC, encoding="utf-8", errors="replace").read()
for tok in re.findall(r'"([a-z0-9][a-z0-9\-]{2,})"', sct):
    if tok in reg: PROTECT.add(tok)
print()
print("  硬护栏（绝不动）: %d 个 —— %s" % (len(PROTECT), ", ".join(sorted(PROTECT)[:18])))

# ---------- 2. 正确的"有无可执行件"判据（全目录扫，不只 scripts/） ----------
EXEC_EXT = (".py",".sh",".js",".ts",".ps1",".bat",".cmd",".exe",".mjs")
def exec_files(d):
    out = []
    for f in glob.glob(os.path.join(d,"**","*"), recursive=True):
        if os.path.isfile(f) and f.lower().endswith(EXEC_EXT):
            out.append(os.path.relpath(f,d).replace(os.sep,"/"))
    return out
def doc_files(d):
    return [os.path.relpath(f,d).replace(os.sep,"/") for f in glob.glob(os.path.join(d,"**","*.md"), recursive=True)
            if os.path.basename(f) != "SKILL.md"]

# ---------- 3. 语料 ----------
CORPUS=[]
for pat in [os.path.join(ROOT,"memory","*.md"), os.path.join(HOME,"self-improving","**","*.md"),
            os.path.join(ROOT,"anyi-ops-kb","**","*.md")]:
    for f in glob.glob(pat, recursive=True):
        try: CORPUS.append(open(f, encoding="utf-8", errors="replace").read()[:200000])
        except Exception: pass
blob = "\n".join(CORPUS)

EXT = re.compile(r"\b(arkcli|gstack|npx|npm|uv|docker|pip|brew)\b", re.I)
READY = {"node","npm","npx","uv","docker","git"}
PLAT_NA = {"brew","pip"}
def deps_of(d):
    deps=set()
    for f in glob.glob(os.path.join(d,"**","*"), recursive=True):
        if not os.path.isfile(f): continue
        try:
            if os.path.getsize(f)>400000: continue
            t=open(f,encoding="utf-8",errors="replace").read()
        except Exception: continue
        for m in EXT.finditer(t): deps.add(m.group(1).lower())
    return deps

rows=[]; verdict=[]
for nm,e in reg.items():
    lab,i = canon(e); d = os.path.dirname(i["path"])
    ex = exec_files(d); docs = doc_files(d)
    deps = deps_of(d)
    blocking = sorted(x for x in deps if x not in READY and x not in PLAT_NA)
    called = blob.count(nm) > 0
    if called:
        act, vs = "active", "已被语料调用"
    elif nm in PROTECT:
        act, vs = "protected", "受保护（今日新建/被工作流或自检引用）—— 不动"
    elif blocking:
        act, vs = "hold", "缺 %s —— 保留待装" % ", ".join(blocking)
    elif ex:
        act, vs = "activate", "有可执行件（%s）但未被调用 —— 纳入固定工作流" % ", ".join(ex[:2])
    elif docs:
        act, vs = "hold", "知识包（%d 份文档）但未被调用 —— 保留待用" % len(docs)
    else:
        act, vs = "archive", "纯单文件说明、无可执行件、从未被调用 —— 归档"
    rows.append({"name":nm,"canonical":i["path"],"canonical_loc":lab,"desc":i["desc"],
        "scripts":i["scripts"],"refs":i["refs"],"bytes":i["bytes"],"files":i["files"],
        "exec":ex,"docs":len(docs),"all_locs":sorted(e["locs"].keys()),"has_desc":bool(i["desc"]),
        "status":act,"idle_verdict":vs if act!="active" else ""})
    if act!="active":
        verdict.append({"name":nm,"deps":sorted(deps),"blocking":blocking,"action":act,"verdict":vs,
                        "locs":sorted(e["locs"].keys()),"bytes":i["bytes"],"exec":ex})
rows.sort(key=lambda r:r["name"].lower())
ac={}
for v in verdict: ac[v["action"]]=ac.get(v["action"],0)+1
print()
print("="*100); print("### 1. 闲置裁决（正确判据：全目录扫可执行件）"); print("="*100)
print("  技能 %d ｜ 活跃 %d ｜ 闲置 %d: %s" % (len(rows), sum(1 for r in rows if r["status"]=="active"), len(verdict), ac))
for a in ("archive","activate","hold","protected"):
    g=[v for v in verdict if v["action"]==a]
    if not g: continue
    print("   【%s】%d 个" % (a,len(g)))
    for v in g[:16]: print("      %-28s %s" % (v["name"][:28], v["verdict"][:62]))

# ---------- 4. 执行归档（严格白名单 + 可回滚） ----------
print()
print("="*100); print("### 2. 执行归档（仅 archive，且跳过受保护/家族根技能）"); print("="*100)
ARC = os.path.join(ROOT,"skills","_archive","idle_2026-11-18")
os.makedirs(ARC, exist_ok=True)
ACTIVE_NAMES = {r["name"] for r in rows if r["status"]=="active"}
moved=[]; skipped=[]
for v in verdict:
    if v["action"]!="archive": continue
    if v["name"] in PROTECT: skipped.append((v["name"],"受保护")); continue
    # 家族根技能保护：若存在同名活跃技能（ponytail / ponytail-gain 同族），不拆散
    fam = [a for a in ACTIVE_NAMES if a and (v["name"].startswith(a+"-") or a.startswith(v["name"]+"-"))]
    if fam: skipped.append((v["name"],"同族活跃技能 %s 存在，保留成族" % fam[0])); continue
    for lab in v["locs"]:
        base = dict(LOCS)[lab]
        for f in glob.glob(os.path.join(base,"**","SKILL.md"), recursive=True):
            rel = os.path.relpath(os.path.dirname(f), base).split(os.sep)
            if any(x.startswith("_") for x in rel): continue
            anc = rel[:-1]
            if any(os.path.exists(os.path.join(base,*anc[:i+1],"SKILL.md")) for i in range(len(anc))): continue
            tx = open(f, encoding="utf-8", errors="replace").read()
            m = re.search(r"^name:\s*%s\s*$" % re.escape(v["name"]), tx, re.M)
            nm2 = m.group(1) if m else rel[-1]
            if nm2 != v["name"]: continue
            src = os.path.dirname(f); dst = os.path.join(ARC, lab+"__"+os.path.basename(src))
            if os.path.exists(dst): continue
            try:
                sh.move(src, dst)
                moved.append({"name":v["name"],"loc":lab,"from":os.path.relpath(src,ROOT).replace(os.sep,"/"),
                              "to":os.path.relpath(dst,ROOT).replace(os.sep,"/"),"bytes":v["bytes"],
                              "rollback":"移回 from 路径即恢复"})
            except Exception as ex:
                skipped.append((v["name"],"移动失败 %s" % str(ex)[:40]))
print("  已归档 %d 份" % len(moved))
for m in moved: print("     %-26s %-7s %s" % (m["name"][:26], m["loc"], m["to"]))
print("  ★ 跳过 %d 个：" % len(skipped))
for s in skipped: print("     %-26s %s" % (s[0][:26], s[1]))
json.dump({"date":"2026-11-18","rule":"纯单文件说明 + 零调用 + 零可执行件 → 归档（可回滚）","archived":moved,"skipped":skipped},
          open(os.path.join(AUD,"idle_archive_manifest_2026-11-18.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)

# ---------- 5. activate 的纳入固定工作流 ----------
print()
print("="*100); print("### 3. 把『activate』候选纳入固定工作流"); print("="*100)
ADD = {
 "cad-editor":          ("CAD 图纸编辑与出图", "CAD 编辑/出图，配合 cad-batch-processing 做批量处理"),
 "brand-identity-design":("品牌识别与视觉系统", "品牌重塑/VI 落地，配合 design-md 与配色范式"),
 "diagram-design":      ("图示与架构图设计", "把结构讲成图，配合 diagram-maker 与拓扑图生成器"),
 "evolution-scan":      ("自进化周期扫描", "★ 每天/每周自动跑断言，防止进化退化"),
 "FontPick":            ("字体选型", "排版前定字体，避免字体缺失返工"),
 "playwright-cli":      ("浏览器自动化（CLI）", "抓取/截图/表单，配合 agent-reach 与 scrape_matrix"),
}
added = 0
for k,(task,note) in ADD.items():
    if any(w["task"]==task for w in WF): continue
    if k not in reg: print("  ★ %s 不在库" % k); continue
    WF.append({"task":task,"skills":k,"note":note,"paradigms":["★待补"],"source":"2026-11-18 闲置激活"})
    added += 1
    print("  ✔ 工作流 + %-24s %s" % (k, task))
json.dump(WF, open(WFP,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("  工作流 %d 条（新增 %d）" % (len(WF), added))

# ---------- 6. 重建注册表 ----------
reg2={}
for lab,base in LOCS:
    for nm,i in real_skills(base).items():
        reg2.setdefault(nm,{"name":nm,"locs":{}})["locs"][lab]=i
st={r["name"]:(r["status"],r["idle_verdict"]) for r in rows}
rows2=[]
for nm,e in reg2.items():
    lab,i=canon(e); s,v=st.get(nm,("active",""))
    d=os.path.dirname(i["path"])
    rows2.append({"name":nm,"canonical":i["path"],"canonical_loc":lab,"desc":i["desc"],
        "scripts":i["scripts"],"refs":i["refs"],"bytes":i["bytes"],"files":i["files"],
        "exec":exec_files(d),"docs":len(doc_files(d)),"all_locs":sorted(e["locs"].keys()),
        "has_desc":bool(i["desc"]),"status":s,"idle_verdict":v})
rows2.sort(key=lambda r:r["name"].lower())
json.dump(rows2, open(os.path.join(AUD,"SKILL_REGISTRY.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(verdict, open(os.path.join(AUD,"IDLE_VERDICT.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print()
print("  注册表重建: %d 条 ｜ active %d ｜ archive %d" % (len(rows2), sum(1 for r in rows2 if r["status"]=="active"), sum(1 for r in rows2 if r["status"]=="archive")))
