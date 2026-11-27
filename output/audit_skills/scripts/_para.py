# -*- coding: utf-8 -*-
import io, sys, os, re, glob, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
SI = os.path.join(HOME,"self-improving")
KB4 = os.path.join(ROOT,"anyi-ops-kb","04_方法论")

print("="*100); print("### A. 范式库注册表：逐文件抽标题与触发词"); print("="*100)
PARA = []
# 1) KB_04_方法论
for base, dirs, fs in os.walk(KB4):
    dirs[:] = [d for d in dirs if d != "_归档_被取代版本"]
    for f in fs:
        if not f.endswith(".md"): continue
        p = os.path.join(base,f)
        t = open(p, encoding="utf-8", errors="replace").read()
        ttl = next((l.lstrip("# ").strip() for l in t.split("\n") if l.startswith("#")), f[:-3])
        m = re.search(r"^\*\*(?:何时用|适用|触发|用途|使用场景)\*\*[:：]\s*(.+)$", t, re.M)
        when = m.group(1)[:90] if m else ""
        # 自动抽关键词：前 40 行里的中文名词 + 标题
        head = "\n".join(t.split("\n")[:40])
        kw = sorted(set(re.findall(r"[一-龥]{2,6}", head)))[:0]
        PARA.append({"src":"KB_04_方法论","file":os.path.relpath(p,ROOT).replace(os.sep,"/"),
                     "title":ttl[:70],"when":when,"bytes":len(t)})
# 2) SI rules
for p in sorted(glob.glob(os.path.join(SI,"rules","*.md"))):
    t = open(p, encoding="utf-8", errors="replace").read()
    ttl = next((l.lstrip("# ").strip() for l in t.split("\n") if l.startswith("#")), os.path.basename(p))
    m = re.search(r"^\*\*何时用\*\*[:：]\s*(.+)$", t, re.M)
    PARA.append({"src":"SI_rules","file":os.path.relpath(p,SI).replace(os.sep,"/"),
                 "title":ttl[:70],"when":m.group(1)[:90] if m else "","bytes":len(t)})
# 3) SI 专题 rules_*.md
for p in sorted(glob.glob(os.path.join(SI,"rules_*.md"))):
    t = open(p, encoding="utf-8", errors="replace").read()
    ttl = next((l.lstrip("# ").strip() for l in t.split("\n") if l.startswith("#")), os.path.basename(p))
    m = re.search(r"^\*\*何时用\*\*[:：]\s*(.+)$", t, re.M)
    PARA.append({"src":"SI_专题","file":os.path.basename(p),
                 "title":ttl[:70],"when":m.group(1)[:90] if m else "","bytes":len(t)})

by_src = {}
for x in PARA: by_src[x["src"]] = by_src.get(x["src"],0)+1
print("  范式条目 %d 条: %s" % (len(PARA), by_src))
no_when = [x for x in PARA if not x["when"]]
print("  ★ 无『何时用』触发说明（不可路由）: %d 条" % len(no_when))
for x in no_when[:8]: print("     %-52s %s" % (x["file"][:52], x["title"][:40]))

# ---- 技能—范式—工作流 对齐表 ----
WFP = os.path.join(ROOT,"output","audit_skills","WORKFLOWS.json")
WF = json.load(open(WFP, encoding="utf-8"))
print()
print("="*100); print("### B. 技能—范式—工作流 对齐（每条工作流绑定范式）"); print("="*100)
ALIGN = {
 "md→docx 转换": ["报告范式/00_报告范式_总入口", "版式设计/《版式之道》核心内化笔记"],
 "公文/请示/报告 排版": ["报告范式/00_报告范式_总入口", "设计内化/B166ER设计方法手册"],
 "PPT 生成": ["报告范式/04_报告体系总图"],
 "信息图/海报": ["配色设计/《中国传统色主题配色手册》", "设计内化/《版式之道》核心内化笔记"],
 "酒店收益管理": ["经营分析范式/02_P&L月报模板", "经营分析范式/01_经营分析框架"],
 "自检/断言/回归": ["domains/自检与断言"],
 "编码/文件完整性": ["domains/代码与工具链"],
 "技术文档写作": ["technical-documentation（技能自带规范）"],
 "知识库结构化": ["方法论书籍内化/Kano模型", "服务设计/《服务不设限》"],
 "CAD/室内设计": ["设计DNA/设计DNA"],
}
miss = []
for w in WF:
    ps = ALIGN.get(w["task"])
    if ps is None: ps = ["★待补"]
    else:
        for p in ps:
            if "（" in p: continue
            if not any(p.split("/")[0] in x["file"] for x in PARA): miss.append((w["task"], p))
    w["paradigms"] = ps
json.dump(WF, open(WFP,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("  工作流 %d 条已回写 paradigm 字段" % len(WF))
print("  ★ 引用了不存在的范式: %d 处" % len(miss))
for t,p in miss[:8]: print("     %-18s → %s" % (t, p))
json.dump(PARA, open(os.path.join(ROOT,"output","audit_skills","PARADIGM_REGISTRY.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("  范式注册表落盘: PARADIGM_REGISTRY.json (%d 条)" % len(PARA))

print()
print("="*100); print("### C. 66 个闲置技能 —— 处置裁决（能用/需装/该退）"); print("="*100)
REG = json.load(open(os.path.join(ROOT,"output","audit_skills","SKILL_REGISTRY.json"), encoding="utf-8"))
by = {r["name"]: r for r in REG}
FAM = {
 "arkcli-*": ("需外部 API/二进制", "arkcli 全家桶指向 ArkCLI 服务，需账号与 API Key；未配置即不可用"),
 "gstack*": ("需外部 CLI", "gstack 系列依赖其自带 CLI 工具链"),
 "plan-*": ("需外部 CLI", "plan-* 属 gstack 的计划审查家族"),
}
idle = ["plan-ceo-review","plan-devex-review","plan-design-review","plan-eng-review","land-and-deploy","design-review","autoplan","design-consultation","devex-review","design-html","qa-only","design-shotgun","document-release","canary","open-gstack-browser","setup-deploy","diagram-design","setup-browser-cookies"]
for n in idle:
    r = by.get(n)
    if not r: print("     %-26s ★不在注册表" % n); continue
    print("     %-26s %-22s scripts=%d refs=%d  %s" % (n[:26], r["canonical_loc"], r["scripts"], r["refs"], r["canonical"].replace(ROOT+"\\","")[:56]))
print()
print("  ★ 关键问题：arkcli(26)+gstack(38) 是否可运行？逐个查依赖")
import subprocess
for fam, key in [("arkcli","arkcli"), ("gstack","gstack")]:
    names = [r["name"] for r in REG if r["name"].startswith(fam)]
    dep = set()
    for n in names:
        for f in glob.glob(os.path.join(ROOT,"skills",n,"**","*"), recursive=True):
            if os.path.isfile(f) and f.endswith((".md",".py",".sh",".json")):
                tx = open(f, encoding="utf-8", errors="replace").read()
                for m in re.findall(r"\b(arkcli|gstack|brew|npm|npx|node|python3?)\b", tx): dep.add(m)
    print("     %-8s %d 个技能 ｜ 提及依赖: %s" % (fam, len(names), ", ".join(sorted(dep))))
