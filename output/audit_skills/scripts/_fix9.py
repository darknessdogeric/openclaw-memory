# -*- coding: utf-8 -*-
import io, sys, os, re, json, glob, shutil as sh, ast, subprocess, tempfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
AUD = os.path.join(ROOT,"output","audit_skills")
SC  = os.path.join(ROOT,"toolbox","selfcheck.py")
WFP = os.path.join(AUD,"WORKFLOWS.json")
LOCS = [("WS",os.path.join(ROOT,"skills")),("HOME",os.path.join(HOME,"skills")),("CLAUDE",os.path.join(HOME,".claude","skills"))]

def jwrite(path, obj):
    """原子写：先写临时文件再替换，杜绝半截 JSON"""
    d = os.path.dirname(path); os.makedirs(d, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=d, suffix=".tmp")
    with os.fdopen(fd,"w",encoding="utf-8") as f:
        json.dump(obj,f,ensure_ascii=False,indent=1)
    os.replace(tmp,path)

def real_skills(base):
    out={}
    if not os.path.isdir(base): return out
    for f in sorted(glob.glob(os.path.join(base,"**","SKILL.md"), recursive=True)):
        d=os.path.dirname(f); rel=os.path.relpath(d,base).split(os.sep)
        if any(x.startswith("_") for x in rel): continue
        anc=rel[:-1]
        if any(os.path.exists(os.path.join(base,*anc[:i+1],"SKILL.md")) for i in range(len(anc))): continue
        tx=open(f,encoding="utf-8",errors="replace").read(); fm={}
        if tx.startswith("---"):
            e=tx.find("\n---",3)
            if e>0:
                for line in tx[3:e].split("\n"):
                    if ":" in line:
                        k,v=line.split(":",1); fm[k.strip().lower()]=v.strip().strip("\"'")
        nm=fm.get("name") or os.path.basename(d)
        out[nm]={"dir":os.path.basename(d),"path":f,"desc":fm.get("description",""),
                 "scripts":len(glob.glob(os.path.join(d,"scripts","*.py"))),
                 "refs":len(glob.glob(os.path.join(d,"references","*.md"))),
                 "bytes":len(tx),
                 "files":len([x for x in glob.glob(os.path.join(d,"**","*"),recursive=True) if os.path.isfile(x)])}
    return out
def canon(e):
    for lab in ("WS","CLAUDE","HOME"):
        if lab in e["locs"]: return lab, e["locs"][lab]
    return "WS", list(e["locs"].values())[0]

EXEC_EXT=(".py",".sh",".js",".ts",".ps1",".bat",".cmd",".exe",".mjs")
EXT = re.compile(r"\b(arkcli|gstack|npx|npm|uv|docker|pip|brew)\b", re.I)
READY={"node","npm","npx","uv","docker","git"}; PLAT_NA={"brew","pip"}
def scan(d):
    ex=[]; docs=0; deps=set()
    for f in glob.glob(os.path.join(d,"**","*"), recursive=True):
        if not os.path.isfile(f): continue
        lo=f.lower()
        if lo.endswith(EXEC_EXT): ex.append(os.path.relpath(f,d).replace(os.sep,"/"))
        if lo.endswith(".md") and os.path.basename(f)!="SKILL.md": docs+=1
        if lo.endswith((".md",".py",".sh",".json",".js",".ts",".txt")):
            try:
                if os.path.getsize(f)>400000: continue
                t=open(f,encoding="utf-8",errors="replace").read()
                for m in EXT.finditer(t): deps.add(m.group(1).lower())
            except Exception: pass
    return ex, docs, sorted(deps)

CORPUS=[]
for pat in [os.path.join(ROOT,"memory","*.md"), os.path.join(HOME,"self-improving","**","*.md"),
            os.path.join(ROOT,"anyi-ops-kb","**","*.md")]:
    for f in glob.glob(pat, recursive=True):
        try: CORPUS.append(open(f,encoding="utf-8",errors="replace").read()[:200000])
        except Exception: pass
blob="\n".join(CORPUS)

reg={}
for lab,base in LOCS:
    for nm,i in real_skills(base).items():
        reg.setdefault(nm,{"name":nm,"locs":{}})["locs"][lab]=i

PROTECT={"self-check-assertions","skill-registry-router","evolution-scan","doc-encoding-repair",
         "topology-infographic","writing-evals","autoreview","technical-documentation"}
print("="*100); print("### A. 重生成闲置裁决（原子写）"); print("="*100)
rows=[]; verdict=[]
for nm,e in reg.items():
    lab,i=canon(e); d=os.path.dirname(i["path"])
    ex,docs,deps = scan(d)
    blocking=[x for x in deps if x not in READY and x not in PLAT_NA]
    called = blob.count(nm)>0
    if called: act,vs="active","已被语料调用"
    elif nm in PROTECT: act,vs="protected","受保护（今日新建/被工作流或自检引用）"
    elif blocking: act,vs="hold","缺 %s —— 保留待装" % ", ".join(blocking)
    elif ex: act,vs="activate","有可执行件但未被调用 —— 纳入固定工作流"
    elif docs: act,vs="hold","知识包（%d 份文档）未被调用 —— 保留待用" % docs
    else: act,vs="archive","纯单文件说明、无可执行件、从未被调用"
    rows.append({"name":nm,"canonical":i["path"],"canonical_loc":lab,"desc":i["desc"],
        "scripts":i["scripts"],"refs":i["refs"],"bytes":i["bytes"],"files":i["files"],
        "exec":ex,"docs":docs,"deps":deps,"all_locs":sorted(e["locs"].keys()),
        "has_desc":bool(i["desc"]),"status":act,"idle_verdict":vs if act!="active" else ""})
    if act!="active":
        verdict.append({"name":nm,"deps":deps,"blocking":blocking,"action":act,"verdict":vs,
                        "locs":sorted(e["locs"].keys()),"bytes":i["bytes"],"exec":ex,"docs":docs})
rows.sort(key=lambda r:r["name"].lower())
jwrite(os.path.join(AUD,"IDLE_VERDICT.json"), verdict)
ac={}
for v in verdict: ac[v["action"]]=ac.get(v["action"],0)+1
print("  技能 %d ｜ 活跃 %d ｜ 闲置 %d: %s" % (len(rows), sum(1 for r in rows if r["status"]=="active"), len(verdict), ac))
for a in ("archive","activate","hold","protected"):
    g=[v for v in verdict if v["action"]==a]
    if g: print("   【%s】%d: %s" % (a,len(g), ", ".join(v["name"] for v in g[:8])))

print()
print("="*100); print("### B. 归档（原子清单 + 可回滚）"); print("="*100)
ACTIVE={r["name"] for r in rows if r["status"]=="active"}
ARC=os.path.join(ROOT,"skills","_archive","idle_2026-11-18"); os.makedirs(ARC,exist_ok=True)
moved=[]; skipped=[]
for v in verdict:
    if v["action"]!="archive": continue
    nm=v["name"]
    if nm in PROTECT: skipped.append([nm,"受保护"]); continue
    fam=[a for a in ACTIVE if a!=nm and (nm.startswith(a+"-") or a.startswith(nm+"-"))]
    if fam: skipped.append([nm,"同族活跃技能 %s 存在，不拆散" % fam[0]]); continue
    for lab in v["locs"]:
        base=dict(LOCS)[lab]
        for f in glob.glob(os.path.join(base,"**","SKILL.md"), recursive=True):
            rel=os.path.relpath(os.path.dirname(f),base).split(os.sep)
            if any(x.startswith("_") for x in rel): continue
            anc=rel[:-1]
            if any(os.path.exists(os.path.join(base,*anc[:i+1],"SKILL.md")) for i in range(len(anc))): continue
            tx=open(f,encoding="utf-8",errors="replace").read()
            m=re.search(r"^name:\s*(%s)\s*$" % re.escape(nm), tx, re.M)
            if (m.group(1).strip() if m else rel[-1]) != nm: continue
            src=os.path.dirname(f); dst=os.path.join(ARC, lab+"__"+os.path.basename(src))
            if os.path.exists(dst): continue
            try:
                sh.move(src,dst)
                moved.append({"name":nm,"loc":lab,"from":os.path.relpath(src,ROOT).replace(os.sep,"/"),
                              "to":os.path.relpath(dst,ROOT).replace(os.sep,"/"),"bytes":v["bytes"],
                              "rollback":"移回 from 路径即恢复"})
            except Exception as ex:
                skipped.append([nm,"移动失败 %s" % str(ex)[:50]])
jwrite(os.path.join(AUD,"idle_archive_manifest_2026-11-18.json"),
       {"date":"2026-11-18","rule":"纯单文件说明+零调用+零可执行件 → 归档（可回滚）；受保护与同族活跃技能不动","archived":moved,"skipped":skipped})
print("  已归档 %d 份:" % len(moved))
for m in moved: print("     %-24s %-7s %s" % (m["name"][:24],m["loc"],m["to"]))
print("  跳过 %d: %s" % (len(skipped), "; ".join("%s(%s)"%(s[0],s[1][:22]) for s in skipped[:8])))

print()
print("="*100); print("### C. 激活候选纳入固定工作流"); print("="*100)
WF=json.load(open(WFP,encoding="utf-8"))
ADD={"cad-editor":("CAD 图纸编辑与出图","CAD 编辑/出图，配合 cad-batch-processing 批量处理"),
 "diagram-design":("图示与架构图设计","把结构讲成图，配合 diagram-maker 与拓扑图生成器"),
 "FontPick":("字体选型","排版前定字体，避免字体缺失返工"),
 "brand-identity-design":("品牌识别与视觉系统","品牌重塑/VI 落地，配合 design-md 与配色范式"),
 "evolution-scan":("自进化周期扫描","★ 周期自动跑断言，防止进化退化"),
 "playwright-cli":("浏览器自动化（CLI）","抓取/截图/表单，配合 agent-reach 与 scrape_matrix")}
added=0
for k,(task,note) in ADD.items():
    if any(w["task"]==task for w in WF): continue
    if k not in reg: print("  ★ %s 不在库" % k); continue
    WF.append({"task":task,"skills":k,"note":note,"paradigms":["★待补"],"source":"2026-11-18 闲置激活"}); added+=1
    print("  ✔ %-24s → %s" % (k,task))
jwrite(WFP, WF); print("  工作流 %d 条（新增 %d）" % (len(WF),added))

print()
print("="*100); print("### D. 重建注册表 + 自检"); print("="*100)
reg2={}
for lab,base in LOCS:
    for nm,i in real_skills(base).items():
        reg2.setdefault(nm,{"name":nm,"locs":{}})["locs"][lab]=i
old={r["name"]:r for r in rows}
rows2=[]
for nm,e in reg2.items():
    lab,i=canon(e); d=os.path.dirname(i["path"]); ex,docs,deps=scan(d)
    o=old.get(nm,{})
    rows2.append({"name":nm,"canonical":i["path"],"canonical_loc":lab,"desc":i["desc"],
        "scripts":i["scripts"],"refs":i["refs"],"bytes":i["bytes"],"files":i["files"],
        "exec":ex,"docs":docs,"deps":deps,"all_locs":sorted(e["locs"].keys()),
        "has_desc":bool(i["desc"]),"status":o.get("status","active"),"idle_verdict":o.get("idle_verdict","")})
rows2.sort(key=lambda r:r["name"].lower())
jwrite(os.path.join(AUD,"SKILL_REGISTRY.json"), rows2)
print("  注册表 %d 条 ｜ active %d" % (len(rows2), sum(1 for r in rows2 if r["status"]=="active")))
r=subprocess.run([sys.executable,SC],capture_output=True,timeout=400)
print(r.stdout.decode("utf-8","replace")); print("退出码:", r.returncode)
