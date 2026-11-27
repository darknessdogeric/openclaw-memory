# -*- coding: utf-8 -*-
import io, sys, os, re, json, glob, tempfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
AUD = os.path.join(ROOT,"output","audit_skills")
def jwrite(p,o):
    d=os.path.dirname(p); os.makedirs(d,exist_ok=True)
    fd,t=tempfile.mkstemp(dir=d,suffix=".tmp")
    with os.fdopen(fd,"w",encoding="utf-8") as f: json.dump(o,f,ensure_ascii=False,indent=1)
    os.replace(t,p)

# ---- 1. 注册表诚实化：状态与实际磁盘状态对齐 ----
REG = os.path.join(AUD,"SKILL_REGISTRY.json")
R = json.load(open(REG, encoding="utf-8"))
IMAN = json.load(open(os.path.join(AUD,"idle_archive_manifest_2026-11-18.json"), encoding="utf-8"))
archived = {a["name"] for a in IMAN["archived"]}
skipped = {s[0]: s[1] for s in IMAN.get("skipped",[])}
ARC = os.path.join(ROOT,"skills","_archive","idle_2026-11-18")
in_arc = set()
if os.path.isdir(ARC):
    for d in os.listdir(ARC):
        nm = d.split("__",1)[-1]
        p = os.path.join(ARC,d,"SKILL.md")
        if os.path.exists(p):
            t=open(p,encoding="utf-8",errors="replace").read()
            m=re.search(r"^name:\s*(.+)$", t, re.M)
            in_arc.add((m.group(1).strip() if m else nm).strip('"\''))
fixed=0
for r in R:
    nm=r["name"]
    if nm in in_arc:
        r["status"]="archived"; r["idle_verdict"]="已归档至 skills/_archive/idle_2026-11-18/（可回滚）"
        fixed+=1
    elif r["status"]=="archive" and nm not in archived:
        # 实际没搬 —— 状态必须诚实
        r["status"]="hold"
        r["idle_verdict"]= skipped.get(nm, "归档候选但未搬迁（保留原位）")
        fixed+=1
jwrite(REG,R)
st={}
for r in R: st[r["status"]]=st.get(r["status"],0)+1
print("注册表诚实化：修正 %d 条 ｜ 状态 %s" % (fixed, st))
# 复核：磁盘上仍在的技能，状态不得是 archived
present = {r["name"] for r in R if r["status"]!="archived"}
bad=[r["name"] for r in R if r["status"]=="archived" and r["name"] in present]
print("  自洽检查（声称已归档却仍在库）: %d 处 %s" % (len(bad), bad[:5]))

# ---- 2. 新技能入固定工作流 ----
WFP=os.path.join(AUD,"WORKFLOWS.json")
W=json.load(open(WFP,encoding="utf-8"))
ADD={
 "skill-registry-builder": ("技能注册表重建", "★ 新建/删除技能后必须重跑，否则 C14 漂移失败"),
 "tool-index-builder":     ("工具索引与归属", "★ 工具层审计：分类 capability/oneoff/orphan 并标 owner_skill"),
}
added=0
for k,(task,note) in ADD.items():
    if any(w["task"]==task for w in W): continue
    W.append({"task":task,"skills":k,"note":note,"paradigms":["SI_domains/代码与工具链.md"],"source":"2026-11-18 工具层治理"}); added+=1
jwrite(WFP,W)
print("工作流 %d 条（新增 %d）" % (len(W),added))

# ---- 3. 范式引用补齐（新增工作流的范式已指；确保无 ★待补）----
P=json.load(open(os.path.join(AUD,"PARADIGM_REGISTRY.json"),encoding="utf-8"))
files={x["file"] for x in P}
todo=[]
for w in W:
    ps=[]
    for p in w.get("paradigms",[]):
        if str(p).startswith("★"): todo.append(w["task"]); continue
        if p.startswith("SI_domains/"):
            base=p.split("/",1)[1]
            if any(x["file"].endswith(base) for x in P): ps.append(p)
        elif any(p.split("/")[0] in x["file"] for x in P): ps.append(p)
        else: todo.append(w["task"])
    w["paradigms"]=ps or ["★待补"]
jwrite(WFP,W)
print("范式引用：★待补 %d 条 %s" % (len(todo), todo[:5]))

# ---- 4. TOOL_INDEX 数字核对 ----
T=json.load(open(os.path.join(AUD,"TOOL_INDEX.json"),encoding="utf-8"))
print("工具索引: %d 个" % len(T))
print("  非临时 .py 现存: %d" % len([p for p in glob.glob(os.path.join(ROOT,"toolbox","*.py")) if not os.path.basename(p).startswith("_")]))
