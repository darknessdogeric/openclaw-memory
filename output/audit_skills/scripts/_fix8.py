# -*- coding: utf-8 -*-
import io, sys, os, re, json, glob, shutil as sh, ast, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
AUD = os.path.join(ROOT,"output","audit_skills")
SC  = os.path.join(ROOT,"toolbox","selfcheck.py")
WFP = os.path.join(AUD,"WORKFLOWS.json")
LOCS = [("WS",os.path.join(ROOT,"skills")),("HOME",os.path.join(HOME,"skills")),("CLAUDE",os.path.join(HOME,".claude","skills"))]

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

reg={}
for lab,base in LOCS:
    for nm,i in real_skills(base).items():
        reg.setdefault(nm,{"name":nm,"locs":{}})["locs"][lab]=i
print("="*100); print("### A. 归档（修正正则：加捕获组；家族不拆散）"); print("="*100)
V = json.load(open(os.path.join(AUD,"IDLE_VERDICT.json"), encoding="utf-8"))
ARC = os.path.join(ROOT,"skills","_archive","idle_2026-11-18")
os.makedirs(ARC, exist_ok=True)
ACTIVE = set()
# 重算 active（语料）
CORPUS=[]
for pat in [os.path.join(ROOT,"memory","*.md"), os.path.join(HOME,"self-improving","**","*.md"),
            os.path.join(ROOT,"anyi-ops-kb","**","*.md")]:
    for f in glob.glob(pat, recursive=True):
        try: CORPUS.append(open(f,encoding="utf-8",errors="replace").read()[:200000])
        except Exception: pass
blob="\n".join(CORPUS)
for nm in reg:
    if blob.count(nm)>0: ACTIVE.add(nm)
PROTECT = {"self-check-assertions","skill-registry-router","evolution-scan","doc-encoding-repair",
           "topology-infographic","writing-evals","autoreview","technical-documentation"}
moved=[]; skipped=[]
for v in V:
    if v["action"]!="archive": continue
    nm=v["name"]
    if nm in PROTECT: skipped.append([nm,"受保护（今日新建）"]); continue
    fam=[a for a in ACTIVE if a!=nm and (nm.startswith(a+"-") or a.startswith(nm+"-"))]
    if fam: skipped.append([nm,"同族活跃技能 %s 存在，保留成族不拆散" % fam[0]]); continue
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
print("  已归档 %d 份:" % len(moved))
for m in moved: print("     %-24s %-7s %s" % (m["name"][:24], m["loc"], m["to"]))
print("  ★ 跳过 %d 个:" % len(skipped))
for s in skipped: print("     %-24s %s" % (s[0][:24], s[1]))
json.dump({"date":"2026-11-18","rule":"纯单文件说明 + 零调用 + 零可执行件 → 归档（可回滚）；受保护与同族活跃技能一律不动",
           "archived":moved,"skipped":skipped},
          open(os.path.join(AUD,"idle_archive_manifest_2026-11-18.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)

print()
print("="*100); print("### B. 激活候选纳入固定工作流"); print("="*100)
WF = json.load(open(WFP, encoding="utf-8"))
ADD = {
 "cad-editor":           ("CAD 图纸编辑与出图", "CAD 编辑/出图，配合 cad-batch-processing 批量处理"),
 "diagram-design":       ("图示与架构图设计", "把结构讲成图，配合 diagram-maker 与拓扑图生成器"),
 "FontPick":             ("字体选型", "排版前定字体，避免字体缺失返工"),
 "brand-identity-design":("品牌识别与视觉系统", "品牌重塑/VI 落地，配合 design-md 与配色范式"),
 "evolution-scan":       ("自进化周期扫描", "★ 周期自动跑断言，防止进化退化"),
 "playwright-cli":       ("浏览器自动化（CLI）", "抓取/截图/表单，配合 agent-reach 与 scrape_matrix"),
}
added=0
for k,(task,note) in ADD.items():
    if any(w["task"]==task for w in WF): continue
    if k not in reg: print("  ★ %s 不在库" % k); continue
    WF.append({"task":task,"skills":k,"note":note,"paradigms":["★待补"],"source":"2026-11-18 闲置激活"})
    added+=1; print("  ✔ %-24s → %s" % (k, task))
json.dump(WF, open(WFP,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("  工作流 %d 条（新增 %d）" % (len(WF), added))

print()
print("="*100); print("### C. 重建注册表 + 自检"); print("="*100)
EXEC_EXT=(".py",".sh",".js",".ts",".ps1",".bat",".cmd",".exe",".mjs")
reg2={}
for lab,base in LOCS:
    for nm,i in real_skills(base).items():
        reg2.setdefault(nm,{"name":nm,"locs":{}})["locs"][lab]=i
old = {r["name"]:r for r in json.load(open(os.path.join(AUD,"SKILL_REGISTRY.json"),encoding="utf-8"))}
rows=[]
for nm,e in reg2.items():
    lab,i=canon(e); d=os.path.dirname(i["path"])
    ex=[os.path.relpath(f,d).replace(os.sep,"/") for f in glob.glob(os.path.join(d,"**","*"),recursive=True)
        if os.path.isfile(f) and f.lower().endswith(EXEC_EXT)]
    docs=len([f for f in glob.glob(os.path.join(d,"**","*.md"),recursive=True) if os.path.basename(f)!="SKILL.md"])
    o=old.get(nm,{})
    rows.append({"name":nm,"canonical":i["path"],"canonical_loc":lab,"desc":i["desc"],
        "scripts":i["scripts"],"refs":i["refs"],"bytes":i["bytes"],"files":i["files"],
        "exec":ex,"docs":docs,"all_locs":sorted(e["locs"].keys()),"has_desc":bool(i["desc"]),
        "status":o.get("status","active"),"idle_verdict":o.get("idle_verdict","")})
rows.sort(key=lambda r:r["name"].lower())
json.dump(rows, open(os.path.join(AUD,"SKILL_REGISTRY.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("  注册表: %d 条 ｜ active %d" % (len(rows), sum(1 for r in rows if r["status"]=="active")))
r = subprocess.run([sys.executable, SC], capture_output=True, timeout=400)
print(r.stdout.decode("utf-8","replace"))
print("退出码:", r.returncode)
