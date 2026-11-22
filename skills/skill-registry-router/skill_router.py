# -*- coding: utf-8 -*-

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
