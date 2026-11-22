# -*- coding: utf-8 -*-
"""skill_router.py - 技能/工具/工作流统一路由（注册表驱动）

★ 用法:
    python toolbox/skill_router.py --task "md 转 docx"        # 查技能 + 工具 + 工作流
    python toolbox/skill_router.py --check "selfcheck.py"     # 自建前必查：是否已有现成件
    python toolbox/skill_router.py --workflows                # 打印固定工作流表
    python toolbox/skill_router.py --tools                    # 打印工具索引概览

依据（程序生成，勿手改）:
    output/audit_skills/SKILL_REGISTRY.json    技能注册表
    output/audit_skills/WORKFLOWS.json         固定工作流
    output/audit_skills/TOOL_INDEX.json        工具索引
    output/audit_skills/PARADIGM_REGISTRY.json 范式注册表

★ 纪律：命中即用，不得自建同类工具。
"""
import io
import sys
import os
import re
import json
import argparse

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUD = os.path.join(ROOT, "output", "audit_skills")
REG = os.path.join(AUD, "SKILL_REGISTRY.json")
WF = os.path.join(AUD, "WORKFLOWS.json")
TI = os.path.join(AUD, "TOOL_INDEX.json")


def load(path):
    if not os.path.exists(path):
        return None
    try:
        return json.load(open(path, encoding="utf-8"))
    except Exception:
        return None


def toks(s):
    """中英双分词。中文用**双字组**而非单字 —— 单字会把「转成」「表格」这类通用字
    混进每个词条，造成检索噪声（曾把 regen_templates 误命中到「md 转 docx」）。"""
    s = (s or "").lower()
    cn = set()
    for seg in re.findall(r"[\u4e00-\u9fff]+", s):
        if len(seg) == 1:
            cn.add(seg)
            continue
        for i in range(len(seg) - 1):
            cn.add(seg[i:i + 2])
    return cn, set(re.findall(r"[a-z0-9]{2,}", s))


def skill_score(task, row):
    tc, te = toks(task)
    dc, de = toks(row.get("name", "") + " " + row.get("desc", ""))
    s = 3.0 * len(tc & dc) + 2.0 * len(te & de)
    if row.get("scripts"):
        s += 0.4
    if row.get("status") == "active":
        s += 0.6
    elif row.get("status") == "idle_pending_activation":
        s -= 0.3
    return s


def tool_score(task, key, row):
    """工具按 purpose / keywords / owner_skill / 文件名 检索"""
    tc, te = toks(task)
    blob = " ".join([key, row.get("purpose", "") or "", " ".join(row.get("keywords", []) or []),
                     row.get("owner_skill", "") or ""])
    dc, de = toks(blob)
    s = 2.5 * len(tc & dc) + 2.0 * len(te & de)
    if row.get("category") == "capability":
        s += 1.0
    elif row.get("category") == "oneoff_family":
        s -= 1.5
    if row.get("owner_skill"):
        s += 0.3
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", default="")
    ap.add_argument("--check", default="")
    ap.add_argument("--workflows", action="store_true")
    ap.add_argument("--tools", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    reg = load(REG) or []
    wf = load(WF) or []
    tools = load(TI) or {}

    if a.workflows or (not a.task and not a.check and not a.tools):
        print("=== 固定工作流（%d 条）===" % len(wf))
        for w in wf:
            print("  %-18s → %-44s %s" % (w.get("task", "")[:18], w.get("skills", "")[:44],
                                          (w.get("note", "") or "")[:50]))
        print()
        print("★ 动手前先在此表查；命中即用，不得自建同类工具。")
        return

    if a.tools:
        cats = {}
        for v in tools.values():
            cats[v.get("category", "?")] = cats.get(v.get("category", "?"), 0) + 1
        owned = sum(1 for v in tools.values() if v.get("owner_skill"))
        print("=== 工具索引：%d 个 ===" % len(tools))
        print("  分类: %s" % cats)
        print("  已归属技能: %d ｜ 未归属: %d" % (owned, len(tools) - owned))
        print()
        print("  ★ 能力型工具（capability）清单:")
        for k, v in sorted(tools.items()):
            if v.get("category") == "capability":
                print("     %-40s owner=%-24s %s" % (k.replace("toolbox/", "")[:40],
                                                      (v.get("owner_skill") or "-")[:24],
                                                      (v.get("purpose") or "")[:44]))
        return

    if a.check:
        print("=== 自建前查重：%s ===" % a.check)
        base = os.path.splitext(os.path.basename(a.check))[0].lower()
        kw = set(re.findall(r"[a-z0-9]{3,}", base.replace("_", " ")))
        hits = []
        for r in reg:
            blob = (r.get("name", "") + " " + r.get("desc", "")).lower()
            sc = len(kw & set(re.findall(r"[a-z0-9]{3,}", blob)))
            if sc or base in r.get("name", "").lower():
                hits.append(("skill", sc, r.get("name"), r.get("canonical", "")))
        for k, v in tools.items():
            blob = (k + " " + (v.get("purpose") or "") + " " + (v.get("owner_skill") or "")).lower()
            sc = len(kw & set(re.findall(r"[a-z0-9]{3,}", blob)))
            if sc or base in k.lower():
                hits.append(("tool", sc, k, v.get("path", "")))
        hits.sort(key=lambda x: -x[1])
        if hits:
            print("  ★★ 已存在同类件，**不要自建**：")
            for kind, sc, name, path in hits[:8]:
                print("     [%-5s] %-40s %s" % (kind, name.replace("toolbox/", "")[:40],
                                               path.replace(ROOT + "\\", "")))
        else:
            print("  未命中既有技能/工具 → 可自建，但请先在 WORKFLOWS 与注册表确认")
            print("  ★ 自建后必须：① 落到 skills/<name>/SKILL.md ② 登记进 SKILL_REGISTRY ③ 在 selfcheck.py 加断言")
        return

    # --task
    rows = sorted(((skill_score(a.task, r), r) for r in reg), key=lambda x: -x[0])
    tops = [x for x in rows if x[0] >= 2.0][:8]
    trows = sorted(((tool_score(a.task, k, v), k, v) for k, v in tools.items()), key=lambda x: -x[0])
    ttops = [x for x in trows if x[0] >= 2.0][:8]

    if a.json:
        print(json.dumps({
            "workflows": [w for w in wf if len(set(toks(a.task)[0]) & set(toks(w.get("task", "") + " " + w.get("skills", ""))[0])) >= 2],
            "skills": [{"score": s, "name": r["name"], "path": r["canonical"], "desc": r["desc"],
                        "status": r.get("status", "active")} for s, r in tops],
            "tools": [{"score": s, "name": k, "path": v.get("path"), "purpose": v.get("purpose"),
                       "category": v.get("category"), "owner": v.get("owner_skill")} for s, k, v in ttops],
        }, ensure_ascii=False, indent=1))
        return

    print("=== 任务: %s ===" % a.task)
    tc, te = toks(a.task)
    hitwf = []
    for w in wf:
        wc, we = toks(w.get("task", "") + " " + w.get("skills", ""))
        if len(tc & wc) + len(te & we) >= 2:
            hitwf.append(w)
    if hitwf:
        print()
        print("  ★ 工作流命中:")
        for w in hitwf:
            print("     %s → %s  (%s)" % (w.get("task"), w.get("skills"), w.get("note", "")[:48]))
    print()
    print("  技能命中:")
    if not tops:
        print("    无 → 先确认确实无现成件（--check），再自建")
    for s, r in tops:
        flag = "" if r.get("status", "active") == "active" else " [%s]" % r.get("status")
        print("    %5.1f  %-32s%s" % (s, r["name"][:32], flag))
        if r.get("desc"):
            print("           %s" % r["desc"][:100])
    print()
    print("  工具命中:")
    if not ttops:
        print("    无")
    for s, k, v in ttops:
        print("    %5.1f  %-38s [%s] owner=%s" % (s, k.replace("toolbox/", "")[:38],
                                                  v.get("category", "?"), v.get("owner_skill") or "-"))
        if v.get("purpose"):
            print("           %s" % v["purpose"][:96])


if __name__ == "__main__":
    main()
