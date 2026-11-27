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

P = json.load(open(os.path.join(AUD,"PARADIGM_REGISTRY.json"), encoding="utf-8"))
files = [(x["file"], x["title"], x["keywords"]) for x in P]
def pick(kws, must=None):
    best=None; bs=-1
    for f,t,k in files:
        blob = (f+" "+t+" "+" ".join(k)).lower()
        sc = sum(1 for kw in kws if kw.lower() in blob)
        if must and must not in f and must not in t: continue
        if sc>bs: bs=sc; best=f
    return best if bs>0 else None

MAP = {
 "全网检索":            (["搜索","检索","研究","调研"], None),
 "网页抓取":            (["爬","抓取","网页","浏览器"], None),
 "知识库语义检索":       (["知识库","语义","检索","笔记"], None),
 "酒店自媒体":           (["新媒体","抖音","小红书","自媒体"], None),
 "成本与用量治理":        (["成本","预算","成本治理","费用"], None),
 "OCR/文档解析":        (["文档","PDF","解析","OCR"], None),
 "代码审阅":            (["代码","审阅","review","技术文档"], None),
 "Office 文档免安装":    (["文档","Office","版式","报告范式"], None),
 "技能评估（装前必过）":  (["自检","断言","评估","代码与工具链"], None),
 "CAD 图纸编辑与出图":    (["设计","版式","设计DNA"], None),
 "图示与架构图设计":      (["设计","设计方法手册","思维导图"], None),
 "字体选型":            (["字体","版式","排版","设计"], None),
 "品牌识别与视觉系统":    (["设计","品牌","配色","配色设计"], None),
 "自进化周期扫描":        (["自检","断言","代码与工具链"], None),
 "浏览器自动化（CLI）":    (["浏览器","网页","自动化"], None),
}
WFP = os.path.join(AUD,"WORKFLOWS.json")
W = json.load(open(WFP, encoding="utf-8"))
filled=0; todo=[]
for w in W:
    if not any(str(p).startswith("★") for p in w.get("paradigms",[])): continue
    kws, must = MAP.get(w["task"], ([], None))
    if not kws: todo.append(w["task"]); continue
    p = pick(kws, must)
    if p:
        w["paradigms"]=[p]; filled+=1
    else:
        w["paradigms"]=["★待补"]; todo.append(w["task"])
jwrite(WFP, W)
print("="*100); print("### A. 范式引用填实"); print("="*100)
print("  已填 %d 条 ｜ 仍待补 %d 条 %s" % (filled, len(todo), todo))
for w in W:
    print("   %-22s → %s" % (w["task"][:22], " ｜ ".join(str(p) for p in w["paradigms"])[:76]))

# ---------- 同步 AGENTS.md 数字 ----------
AG = os.path.join(ROOT,"AGENTS.md")
t = open(AG, encoding="utf-8", errors="replace").read()
rep = [
 ("| `output/audit_skills/SKILL_REGISTRY.json` | 技能注册表 134 个（含 description／脚本数／参考文档数／三处位置） |",
  "| `output/audit_skills/SKILL_REGISTRY.json` | 技能注册表 150 个（含 description／脚本数／可执行件／三处位置／活跃状态） |"),
 ("| `output/audit_skills/WORKFLOWS.json` | 固定工作流 19 条（任务 → 技能 → 依据） |",
  "| `output/audit_skills/WORKFLOWS.json` | 固定工作流 25 条（任务 → 技能 → 范式 → 依据） |"),
 ("物理 `SKILL.md` 271 份、去重 185 命名、**79 组同名**散在 `workspace/skills`／`~/skills`／`~/.claude\\/skills` 三处",
  "物理 `SKILL.md` 271 份、去重 185 命名、**79 组同名**散在 `workspace/skills`／`~/skills`／`~/.claude\\/skills` 三处；**按真实技能边界（祖先判据）实为 150 个**"),
]
n=0
for a,b in rep:
    if a in t: t=t.replace(a,b); n+=1
open(AG,"w",encoding="utf-8",newline="\n").write(t)
print()
print("  AGENTS.md 已同步 %d 处数字" % n)

# ---------- 同步日记 ----------
MD = os.path.join(ROOT,"memory","2026-11-18.md")
d = open(MD, encoding="utf-8", errors="replace").read()
d = d.replace("**按真实技能边界（排除技能内部嵌套的 `examples/`、`variants/`）重算后为 134 个**",
              "**按真实技能边界（祖先判据：祖先目录不含 SKILL.md 才算独立技能）重算后为 150 个**")
d = d.replace("**固定工作流**：建 `SKILL_REGISTRY.json`（134 条）＋ `WORKFLOWS.json`（19 条）＋ `TOOL_INDEX.json`（698 个工具）",
              "**固定工作流**：建 `SKILL_REGISTRY.json`（150 条）＋ `WORKFLOWS.json`（25 条）＋ `PARADIGM_REGISTRY.json`（150 条范式）＋ `TOOL_INDEX.json`（698 个工具）")
d = d.replace("**断言**：selfcheck 从 12 条增至 **18 条**（C13–C18 新增），**18/18 全绿，退出码 0**。",
              "**断言**：selfcheck 从 12 条增至 **19 条**（C13–C19 新增），**19/19 全绿，退出码 0**。")
d = d.replace("→ 传感器：新增 **C13–C18 六条断言**", "→ 传感器：新增 **C13–C19 七条断言**")
d = d.replace("传感器：新增 **C13–C18 六条断言**", "传感器：新增 **C13–C19 七条断言**")
d = d.replace("注册表存在且每个技能有 description、注册表与磁盘不漂移、GitHub 安装有台账、md→docx 正本唯一、归档不回潮、工作流表非空。",
              "注册表存在且每个技能有 description、注册表与磁盘不漂移、GitHub 安装有台账、md→docx 正本唯一、归档不回潮、工作流表非空、范式可路由且工作流绑定范式。")
open(MD,"w",encoding="utf-8",newline="\n").write(d)
print("  日记已同步数字")
