# -*- coding: utf-8 -*-
import io, sys, os, re, glob, json, hashlib, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
WS = os.path.join(ROOT,"skills")
REG = os.path.join(ROOT, "output", "audit_skills", "SKILL_REGISTRY.json")
os.makedirs(os.path.dirname(REG), exist_ok=True)

# ---- 技能真实边界：只认 <skill>/SKILL.md，排除内部嵌套 examples/variants/references ----
def skill_roots(base):
    out = {}
    if not os.path.isdir(base): return out
    for f in sorted(glob.glob(os.path.join(base, "*", "SKILL.md"))):
        d = os.path.basename(os.path.dirname(f))
        if d in ("examples","variants","references","scripts","templates","assets","docs","plugins"): continue
        t = open(f, encoding="utf-8", errors="replace").read()
        fm = {}
        if t.startswith("---"):
            e = t.find("\n---", 3)
            if e > 0:
                for line in t[3:e].split("\n"):
                    if ":" in line:
                        k,v = line.split(":",1); fm[k.strip().lower()] = v.strip().strip("\"'")
        nm = fm.get("name") or d
        out[nm] = {"dir": d, "path": f, "fm": fm,
                    "desc": fm.get("description",""),
                    "scripts": len(glob.glob(os.path.join(os.path.dirname(f),"scripts","*.py"))),
                    "refs": len(glob.glob(os.path.join(os.path.dirname(f),"references","*.md"))),
                    "bytes": len(t),
                    "files": len([x for x in glob.glob(os.path.join(os.path.dirname(f),"**","*"), recursive=True) if os.path.isfile(x)])}
    return out

print("="*94); print("### 建技能注册表（按真实技能边界）"); print("="*94)
LOCS = [("WS", WS), ("HOME", os.path.join(HOME,"skills")), ("CLAUDE", os.path.join(HOME,".claude","skills"))]
reg = {}
for lab, base in LOCS:
    for nm, info in skill_roots(base).items():
        e = reg.setdefault(nm, {"name": nm, "locs": {}})
        e["locs"][lab] = info
uniq = len(reg)
print("  真实技能数（排除嵌套 examples/variants）: %d" % uniq)
by = {}
for nm, e in reg.items():
    for lab, i in e["locs"].items(): by[lab] = by.get(lab,0)+1
print("  各位置:", by)

# ---- 规范路径：WS 优先，其次 CLAUDE，再次 HOME ----
def canon(e):
    for lab in ("WS","CLAUDE","HOME"):
        if lab in e["locs"]: return lab, e["locs"][lab]
    return "WS", list(e["locs"].values())[0]
rows = []
for nm, e in reg.items():
    lab, i = canon(e)
    rows.append({"name": nm, "canonical": i["path"], "canonical_loc": lab,
        "desc": i["desc"], "scripts": i["scripts"], "refs": i["refs"],
        "bytes": i["bytes"], "files": i["files"],
        "all_locs": sorted(e["locs"].keys()),
        "has_desc": bool(i["desc"])})
rows.sort(key=lambda r: (-r["scripts"], r["name"].lower()))
json.dump(rows, open(REG,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("  注册表落盘:", REG, os.path.getsize(REG), "B ｜ %d 条" % len(rows))

nod = [r["name"] for r in rows if not r["has_desc"]]
print("  无 description: %d %s" % (len(nod), nod[:10]))
print("  有脚本的技能: %d ｜ 有参考文档的: %d" % (sum(1 for r in rows if r["scripts"]), sum(1 for r in rows if r["refs"])))

# ---- 固定工作流路由（任务类型 → 技能 → 依据）----
WF = [
 ("md→docx 转换", "docx-md-bridge", "scripts/md_to_docx.py（已实测 rc=0，产出含表 docx）"),
 ("公文/请示/报告 排版", "gongwen-docx-cn + gongwen-report-cn", "GB/T 9704-2012 ＋ Eric 排版习惯；请示四段骨架"),
 ("PPT 生成", "ppt-deck-builder-pro", "run_image_batch.sh / package_image_deck.sh"),
 ("信息图/海报", "article-to-infographic + china-poster-studio + infographic", "文字→信息图，多风格"),
 ("全网检索", "agent-reach", "~/.agents/skills/agent-reach（17 平台路由，已核实存在）"),
 ("网页抓取", "scrap_tools.py / ultimate-search / crawl4ai / playwright-mcp", "scrap_matrix 自动路由 Booking→InvisiblePlaywright、携程→Obscura"),
 ("知识库语义检索", "openviking + local_semantic_search.py", "本地免费无限制；ov status / ov find"),
 ("酒店收益管理", "hotel-revenue-management", "RevPAR/ADR/OCC/GOPPAR ＋ 竞对对标 ＋ 决策清单"),
 ("酒店自媒体", "hotel-new-media", "抖音/小红书运营"),
 ("成本与用量治理", "cost-governor + clawhub/controlling-costs", "x402 预算与熔断（cost-governor 已补 description）"),
 ("自检/断言/回归", "writing-evals + autoreview + toolbox/selfcheck.py", "★ 今日新建：12 条可失败断言"),
 ("编码/文件完整性", "toolbox/fix_mixed_encoding.py + toolbox/selfcheck.py C01", "★ 今日新建：混合编码修复 + 基线感知"),
 ("OCR/文档解析", "toolbox/ocr（rapidocr 封装）", "★ 今日新建：Windows 本地 OCR"),
 ("代码审阅", "autoreview + review + codex", "本次新装"),
 ("技术文档写作", "technical-documentation", "本次新装"),
 ("知识库结构化", "ontology + growth-mindset", "图谱化知识 + 复盘"),
 ("CAD/室内设计", "cad-batch-processing + interior-fullplan", "DWG/DXF 批量 ＋ 全案生成"),
 ("Office 文档免安装", "officecli", "单文件二进制，免装 Office"),
 ("技能评估（装前必过）", "skill-vetter", "★ 装任何 GitHub/ClawdHub 技能前先过这一关"),
]
WFJ = [{"task":a,"skills":b,"note":c} for a,b,c in WF]
json.dump(WFJ, open(os.path.join(os.path.dirname(REG),"WORKFLOWS.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("  固定工作流: %d 条 → %s" % (len(WFJ), os.path.join(os.path.dirname(REG),"WORKFLOWS.json")))

# ---- 升级 skill_router.py：读注册表 + 命中工作流 + 提示"先查表再自建" ----
SR = r"""# -*- coding: utf-8 -*-
""" + r'''
"""skill_router.py - 技能/工具路由（注册表驱动）
★ 用法:
    python toolbox/skill_router.py --task "md 转 docx"
    python toolbox/skill_router.py --workflows
    python toolbox/skill_router.py --check "selfcheck.py"     # 自建前必查：是否已有现成件
依据: output/audit_skills/SKILL_REGISTRY.json + WORKFLOWS.json（程序生成，勿手改）
"""
import io, sys, os, re, json, glob, argparse
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = os.path.join(ROOT, "output", "audit_skills", "SKILL_REGISTRY.json")
WF = os.path.join(ROOT, "output", "audit_skills", "WORKFLOWS.json")

def load():
    reg = json.load(open(REG, encoding="utf-8")) if os.path.exists(REG) else []
    wf = json.load(open(WF, encoding="utf-8")) if os.path.exists(WF) else []
    return reg, wf

def toks(s):
    s = (s or "").lower()
    return set(re.findall(r"[\u4e00-\u9fff]", s)), set(re.findall(r"[a-z0-9]{2,}", s))

def score(task, row):
    tc, te = toks(task)
    dc, de = toks(row["name"] + " " + row["desc"])
    s = 3.0 * len(tc & dc) + 2.0 * len(te & de)
    if row["scripts"]: s += 0.4
    return s

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", default="")
    ap.add_argument("--workflows", action="store_true")
    ap.add_argument("--check", default="")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    reg, wf = load()
    if a.workflows or (not a.task and not a.check):
        print("=== 固定工作流（%d 条）===" % len(wf))
        for w in wf:
            print("  %-16s → %-46s %s" % (w["task"][:16], w["skills"][:46], w["note"][:52]))
        print()
        print("★ 动手前先在此表查；命中即用，不得自建同类工具。")
        return
    if a.check:
        print("=== 自建前查重：%s ===" % a.check)
        base = os.path.splitext(os.path.basename(a.check))[0].lower()
        kw = set(re.findall(r"[a-z0-9]{3,}", base.replace("_"," ")))
        hits = []
        for r in reg:
            blob = (r["name"] + " " + r["desc"]).lower()
            sc = len(kw & set(re.findall(r"[a-z0-9]{3,}", blob)))
            if sc or base in r["name"].lower():
                hits.append((sc, r))
        hits.sort(key=lambda x: -x[0])
        if hits:
            print("  ★★ 已存在同类技能，**不要自建**：")
            for sc, r in hits[:6]:
                print("     %-34s %s" % (r["name"][:34], r["canonical"].replace(ROOT+"\\","")))
        else:
            print("  未命中既有技能 → 可自建，但请先在 WORKFLOWS 与本注册表确认")
            print("  ★ 自建后必须：① 落到 skills/<name>/SKILL.md ② 登记进 SKILL_REGISTRY ③ 在 selfcheck.py 加断言")
        return
    rows = sorted(((score(a.task, r), r) for r in reg), key=lambda x: -x[0])
    top = [x for x in rows if x[0] >= 2.0][:8]
    if a.json:
        print(json.dumps([{"score":s,"name":r["name"],"path":r["canonical"],"desc":r["desc"]} for s,r in top], ensure_ascii=False, indent=1))
        return
    print("=== 任务: %s ===" % a.task)
    # 先给工作流
    tc, te = toks(a.task)
    for w in wf:
        wc, we = toks(w["task"] + " " + w["skills"])
        if len(tc & wc) + len(te & we) >= 2:
            print("  ★ 工作流命中: %s → %s  (%s)" % (w["task"], w["skills"], w["note"]))
    print()
    print("  技能命中:")
    if not top:
        print("    无 → 先确认确实无现成件（--check），再自建")
    for s, r in top:
        print("    %5.1f  %-32s %s" % (s, r["name"][:32], r["canonical"].replace(ROOT+"\\","")))
        if r["desc"]: print("           %s" % r["desc"][:100])

if __name__ == "__main__":
    main()
'''
open(os.path.join(ROOT,"toolbox","skill_router.py"),"w",encoding="utf-8",newline="\n").write(SR)
import ast; ast.parse(SR)
print()
print("✔ skill_router.py 已升级（注册表驱动 + 工作流优先 + --check 自建前查重）:", os.path.getsize(os.path.join(ROOT,"toolbox","skill_router.py")), "B")
