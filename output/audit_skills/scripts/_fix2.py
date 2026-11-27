# -*- coding: utf-8 -*-
import io, sys, os, re, glob, json, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
WS = os.path.join(ROOT,"skills")
AUD = os.path.join(ROOT,"output","audit_skills")

def real_skills(base):
    """真技能 = 其所有祖先目录都不含 SKILL.md（排除技能内部嵌套副本）"""
    out = {}
    if not os.path.isdir(base): return out
    for f in sorted(glob.glob(os.path.join(base,"**","SKILL.md"), recursive=True)):
        d = os.path.dirname(f)
        anc = os.path.relpath(d, base).split(os.sep)[:-1]
        nested = False
        for i in range(len(anc)):
            p = os.path.join(base, *anc[:i+1])
            if os.path.exists(os.path.join(p,"SKILL.md")):
                nested = True; break
        if nested: continue
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

print("="*100); print("### A. 修注册表口径（祖先判据）"); print("="*100)
LOCS = [("WS",WS),("HOME",os.path.join(HOME,"skills")),("CLAUDE",os.path.join(HOME,".claude","skills"))]
reg = {}
for lab, base in LOCS:
    for nm, i in real_skills(base).items():
        reg.setdefault(nm, {"name":nm,"locs":{}})["locs"][lab] = i
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
rows.sort(key=lambda r:r["name"].lower())
nod = [r["name"] for r in rows if not r["has_desc"]]
by = {}
for r in rows:
    for l in r["all_locs"]: by[l] = by.get(l,0)+1
print("  技能总数 %d（修前 134）｜ 各位置 %s" % (len(rows), by))
print("  ★ 新补入的（修前漏掉的家族式嵌套技能）: %d 个" % (len(rows)-134))
newly = [r["name"] for r in rows if r["canonical_loc"]=="CLAUDE" and r["name"] not in [x["name"] for x in []]]
print("  ★ 无 description: %d 个 → 必须补，否则 C13 会 FAIL" % len(nod))
print("    ", ", ".join(nod[:20]))

# 补 description（就地写入 frontmatter）
FIX = {
 "plan-ceo-review":"从 CEO 视角做计划审查（商业价值/风险/资源）。触发：计划评审、CEO 视角审查、项目立项前把关。",
 "plan-devex-review":"从开发者体验（DX）角度审查计划。触发：DX 评审、开发者体验评估、工程计划把关。",
 "plan-design-review":"从设计角度审查计划（可用性/一致性/视觉）。触发：设计评审、UI/UX 计划审查。",
 "plan-eng-review":"从工程角度审查计划（可实现性/技术债/容量）。触发：工程评审、技术方案把关。",
 "land-and-deploy":"把评审通过的方案落地并部署（合并→发布→验证）。触发：上线、部署、发布到生产。",
 "design-review":"对设计稿/界面做系统化审查。触发：设计审查、UI 检查、视觉走查。",
 "autoplan":"自动生成实施计划（从需求到可执行步骤）。触发：自动出方案、生成计划、拆解需求。",
 "design-consultation":"设计咨询：给设计决策做方案对比与建议。触发：设计咨询、方案取舍建议。",
 "devex-review":"开发者体验专项审查。触发：DX 体检、开发者满意度检查。",
 "design-html":"生成单文件 HTML 设计稿/页面。触发：快速出页面、HTML 原型、单页设计。",
 "qa-only":"只跑测试的 QA 流程（不实施修复）。触发：只测试、回归验证、QA 报告。",
 "design-shotgun":"多方案并行生成再择优的设计打法。触发：多方案对比、并行设计、爆款设计试探。",
 "document-release":"为发布撰写文档（release notes/变更说明）。触发：发版说明、变更日志。",
 "canary":"金丝雀发布/灰度验证流程。触发：灰度发布、canary、小流量验证。",
 "open-gstack-browser":"打开 gstack 配套浏览器环境。触发：gstack 浏览器、自动化浏览。",
 "setup-deploy":"初始化部署环境与配置。触发：部署初始化、环境准备。",
 "setup-browser-cookies":"配置浏览器 cookies 以通过登录态抓取。触发：登录态、cookies 配置、免登录抓取。",
 "benchmark":"跑基准测试并对比结果。触发：性能基准、benchmark、性能对比。",
 "browse":"快速浏览网页并提取正文。触发：网页速读、批量浏览、页面抓取。",
 "careful":"高风险操作前的谨慎复核流程（改动前必查）。触发：危险操作、不可逆操作前复核。",
 "checkpoint":"在关键节点建立检查点（可回滚）。触发：检查点、快照、可回滚标记。",
 "codex":"以 Codex 风格生成/审阅代码。触发：代码生成、codex 风格改写。",
 "cso":"以 CSO 视角给出安全与合规建议。触发：安全评审、合规检查、CSO 视角。",
 "follow-builders":"追踪关注对象（人物/公司）的动态。触发：跟踪、关注动态、订阅追踪。",
 "freeze":"冻结当前状态（禁止变更）作为基线。触发：冻结、锁定基线、变更管控。",
 "guard":"加装防护/前置校验，阻止危险操作。触发：加护栏、危险操作拦截。",
 "health":"检查项目/系统健康度并给结论。触发：健康检查、状态体检、诊断。",
 "investigate":"系统性排查问题并给出根因。触发：排查、定位问题、根因分析。",
 "learn":"从本次任务中提炼可复用经验。触发：复盘学习、经验沉淀。",
 "office-hours":"以顾问式答疑时间的方式讨论问题并给建议。触发：咨询、答疑、office hours。",
 "playwright-cli":"用 Playwright CLI 驱动浏览器自动化。触发：浏览器自动化、Playwright 操作。",
 "qa":"完整 QA 流程（测试→发现问题→修复→回归）。触发：QA 流程、测试验证、回归。",
 "retro":"团队/项目复盘（做得好/待改进/下一步）。触发：复盘、事后回顾、retro。",
 "review":"通用代码/方案审查流程。触发：review、审查、把关。",
 "ship":"把改动推上线（检查→构建→发布）。触发：发布、ship、推上线。",
 "unfreeze":"解除冻结状态，恢复可变更。触发：解冻、恢复变更。",
 "tavily-research":"用 Tavily 做深度调研并给带来源的结论。触发：深度调研、联网研究、带信源调研。",
}
fixed = 0
for nm in nod:
    d = FIX.get(nm)
    if not d: continue
    for lab, base in LOCS:
        for f in glob.glob(os.path.join(base,"**","SKILL.md"), recursive=True):
            tx = open(f, encoding="utf-8", errors="replace").read()
            m = re.search(r"^name:\s*%s\s*$" % re.escape(nm), tx, re.M)
            if not m: continue
            if not tx.lstrip().startswith("---"):
                open(f,"w",encoding="utf-8",newline="\n").write("---\nname: %s\ndescription: %s\n---\n\n" % (nm,d) + tx); fixed+=1
            else:
                e = tx.find("\n---",3)
                fm, body = tx[:e], tx[e:]
                if re.search(r"^description:", fm, re.M):
                    fm2 = re.sub(r"^description:.*$", "description: "+d, fm, count=1, flags=re.M)
                else:
                    fm2 = fm + "\ndescription: "+d
                open(f,"w",encoding="utf-8",newline="\n").write(fm2+body); fixed+=1
print("  已补 description: %d 处" % fixed)
# 重建（补完后）
reg = {}
for lab, base in LOCS:
    for nm, i in real_skills(base).items():
        reg.setdefault(nm, {"name":nm,"locs":{}})["locs"][lab] = i
rows = []
for nm, e in reg.items():
    lab, i = canon(e)
    rows.append({"name":nm,"canonical":i["path"],"canonical_loc":lab,"desc":i["desc"],
                 "scripts":i["scripts"],"refs":i["refs"],"bytes":i["bytes"],"files":i["files"],
                 "all_locs":sorted(e["locs"].keys()),"has_desc":bool(i["desc"])})
rows.sort(key=lambda r:r["name"].lower())
json.dump(rows, open(os.path.join(AUD,"SKILL_REGISTRY.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("  注册表重建: %d 条 ｜ 无描述 %d" % (len(rows), sum(1 for r in rows if not r["has_desc"])))

print()
print("="*100); print("### B. 范式注册表：补 SI_domains + 自动派生可路由关键词"); print("="*100)
SI = os.path.join(HOME,"self-improving")
KB4 = os.path.join(ROOT,"anyi-ops-kb","04_方法论")
STOP = set("的了是在和与及对于关于一个这个那个我们你们他们如果因为所以但是可以进行通过已经以及需要必须这个以及一种一些以及比如然后由于并且因此其中同时包括等等而且或者并且".split())
def keywords(title, body):
    ks = set()
    for seg in re.split(r"[\s/／、,，。：:（）()《》\"'`]+", title):
        seg = seg.strip()
        if len(seg) >= 2 and seg not in STOP: ks.add(seg)
    head = "\n".join(body.split("\n")[:26])
    for w in re.findall(r"[一-龥]{2,6}", head):
        if w not in STOP and not any(w in s and s != w for s in ks): ks.add(w)
    return sorted(ks)[:12]
PARA = []
def add_paradigm(src, path, rel):
    t = open(path, encoding="utf-8", errors="replace").read()
    ttl = next((l.lstrip("# ").strip() for l in t.split("\n") if l.startswith("#")), os.path.basename(path))
    m = re.search(r"^\*\*(?:何时用|适用|触发|用途|使用场景|应用场景)\*\*[:：]\s*(.+)$", t, re.M)
    explicit = m.group(1)[:100] if m else ""
    PARA.append({"src":src,"file":rel,"title":ttl[:80],
                 "when":explicit or "触发词："+" / ".join(keywords(ttl,t)),
                 "trigger_source":"explicit" if explicit else "derived",
                 "keywords":keywords(ttl,t),"bytes":len(t)})
for base, dirs, fs in os.walk(KB4):
    dirs[:] = [d for d in dirs if d != "_归档_被取代版本"]
    for f in fs:
        if f.endswith(".md"): add_paradigm("KB_04_方法论", os.path.join(base,f), os.path.relpath(os.path.join(base,f),ROOT).replace(os.sep,"/"))
for p in sorted(glob.glob(os.path.join(SI,"rules","*.md"))): add_paradigm("SI_rules", p, os.path.relpath(p,SI).replace(os.sep,"/"))
for p in sorted(glob.glob(os.path.join(SI,"rules_*.md"))): add_paradigm("SI_专题", p, os.path.basename(p))
for p in sorted(glob.glob(os.path.join(SI,"domains","*.md"))): add_paradigm("SI_domains", p, os.path.relpath(p,SI).replace(os.sep,"/"))
json.dump(PARA, open(os.path.join(AUD,"PARADIGM_REGISTRY.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
bs = {}
for x in PARA: bs[x["src"]] = bs.get(x["src"],0)+1
print("  范式 %d 条: %s" % (len(PARA), bs))
print("  ★ 无关键词（不可路由）: %d" % sum(1 for x in PARA if not x["keywords"]))

# 修工作流的 paradigm 引用
WFP = os.path.join(AUD,"WORKFLOWS.json")
WF = json.load(open(WFP, encoding="utf-8"))
FIXP = {"自检/断言/回归":["SI_domains/自检与断言.md"], "编码/文件完整性":["SI_domains/代码与工具链.md"]}
for w in WF:
    if w["task"] in FIXP: w["paradigms"] = FIXP[w["task"]]
    w.setdefault("paradigms", ["★待补"])
json.dump(WF, open(WFP,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
fileset = {x["file"] for x in PARA}
bad = []
for w in WF:
    for p in w["paradigms"]:
        if "（" in p or p.startswith("★"): continue
        if p.startswith("SI_domains/"):
            key = "domains/"+p.split("/",1)[1]
            if not any(x["file"].endswith(p.split("/",1)[1]) for x in PARA): bad.append((w["task"],p))
        elif not any(p.split("/")[0] in x["file"] for x in PARA): bad.append((w["task"],p))
print("  工作流 %d 条已绑定范式 ｜ 引用不存在: %d 处 %s" % (len(WF), len(bad), bad[:4]))
