# -*- coding: utf-8 -*-
import io, sys, os, re, glob, json, subprocess, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
import requests
H = {"User-Agent":"openclaw-audit","Accept":"application/vnd.github+json"}

print("="*100); print("### A. 取 GitHub 许可证与 commit（台账必备）"); print("="*100)
meta = {}
for repo in ["openclaw/clawhub","VoltAgent/awesome-openclaw-skills"]:
    try:
        r = requests.get("https://api.github.com/repos/%s" % repo, headers=H, timeout=30)
        j = r.json()
        lic = (j.get("license") or {}).get("spdx_id") or "NOASSERTION"
        cm = requests.get("https://api.github.com/repos/%s/commits/main" % repo, headers=H, timeout=30).json()
        sha = cm.get("sha","")[:12]
        meta[repo] = {"stars": j["stargazers_count"], "license": lic, "commit": sha,
                      "pushed_at": j.get("pushed_at"), "archived": j.get("archived"),
                      "desc": (j.get("description") or "")[:80]}
        print("  %-40s ★%s ｜ %s ｜ commit %s ｜ archived=%s" % (repo, j["stargazers_count"], lic, sha, j.get("archived")))
    except Exception as e:
        print("  %-40s 取值失败 %s" % (repo, str(e)[:70]))

print()
print("="*100); print("### B. 建安装台账"); print("="*100)
WS = os.path.join(ROOT,"skills")
LEDGER = os.path.join(ROOT,"output","audit_skills","GITHUB_INSTALL_LEDGER.json")
INSTALLED = [
 {"name":"writing-evals","path":"skills/writing-evals","repo":"openclaw/clawhub",
  "subpath":".agents/skills/writing-evals/","files":21,
  "gap_filled":"自检/回归/评测写法 —— 我今天手搓 selfcheck.py 时缺少的方法论层",
  "why":"★ 已证实的能力缺口（本地无对应技能），非堆叠"},
 {"name":"autoreview","path":"skills/autoreview","repo":"openclaw/clawhub",
  "subpath":".agents/skills/autoreview/","files":1,
  "gap_filled":"自动代码审阅 —— 验证断言的独立视角",
  "why":"★ 已证实的能力缺口"},
 {"name":"technical-documentation","path":"skills/technical-documentation","repo":"openclaw/clawhub",
  "subpath":".agents/skills/technical-documentation/","files":13,
  "gap_filled":"技术文档写作规范 —— 范式库写作层缺口",
  "why":"★ 已证实的能力缺口"},
]
man = {"date":"2026-11-18",
 "rule":"GitHub 安装只针对已证实的能力缺口；须留来源/版本/许可证/回滚记录（AGENTS.md 硬要求）",
 "repos": meta,
 "installs": [],
 "rollback": "删除 skills/<name>/ 目录即回滚；未修改任何系统配置，无外部副作用",
 "not_installed": [
   {"repo":"VoltAgent/awesome-openclaw-skills","stars":meta.get("VoltAgent/awesome-openclaw-skills",{}).get("stars"),
    "reason":"★ 只作缺口发现目录（5,300+ 技能清单），未安装任何条目 —— 无已证实缺口对应",
    "license":meta.get("VoltAgent/awesome-openclaw-skills",{}).get("license")}]}
for it in INSTALLED:
    d = os.path.join(ROOT, it["path"].replace("/", os.sep))
    fs = [os.path.join(base,f) for base,_,files in os.walk(d) for f in files]
    it2 = dict(it); it2["actual_files"] = len(fs)
    it2["bytes"] = sum(os.path.getsize(f) for f in fs)
    it2["license"] = meta.get(it["repo"],{}).get("license","NOASSERTION")
    it2["repo_stars"] = meta.get(it["repo"],{}).get("stars")
    it2["commit"] = meta.get(it["repo"],{}).get("commit")
    it2["installed_at"] = "2026-11-18"
    man["installs"].append(it2)
    print("  ✔ %-26s %2d 文件 / %6d B ｜ %s ｜ %s ｜ commit %s" % (
        it["name"], it2["actual_files"], it2["bytes"], it["repo"], it2["license"], it2["commit"]))
json.dump(man, open(LEDGER,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("  台账落盘:", os.path.basename(LEDGER))

print()
print("="*100); print("### C. 同步更新 TOOL_INDEX（归档后重建，排除 _ 开头与 _archive）"); print("="*100)
TB = os.path.join(ROOT,"toolbox")
TOOLS = {}
for p in sorted(glob.glob(os.path.join(TB,"*.py"))):
    b = os.path.basename(p)
    if b.startswith("_"): continue
    t = open(p, encoding="utf-8", errors="replace").read()
    purpose = next((l.strip() for l in t.split("\n")[:10] if l.strip() and not l.strip().startswith("#")), "")[:160]
    TOOLS["toolbox/"+b] = {"bytes": len(t), "purpose": purpose, "skill_equivalent": "", "scope_note": ""}
MAP = {
 "toolbox/md2docx.py": ("docx-md-bridge", "研判报告排版变体（宋体/黑体/纸色主题）。★通用 md→docx 请用 skills/docx-md-bridge"),
 "toolbox/md2gongwen_docx.py": ("gongwen-docx-cn", "公文版式（旧克隆）—— 已被 skills/gongwen-docx-cn 取代"),
 "toolbox/selfcheck.py": ("self-check-assertions", "自检断言执行器（本技能正主）"),
 "toolbox/skill_router.py": ("skill-registry-router", "技能路由（本技能正主）"),
 "toolbox/evolution_scan.py": ("evolution-scan", "扫描器（本技能正主）"),
 "toolbox/evolution_watch.py": ("evolution-scan", "缺席探测器（本技能正主）"),
 "toolbox/fix_mixed_encoding.py": ("doc-encoding-repair", "编码修复器（本技能正主）"),
 "toolbox/make_topology.py": ("topology-infographic", "拓扑图生成器（本技能正主）"),
}
for k,(sk,note) in MAP.items():
    if k in TOOLS: TOOLS[k]["skill_equivalent"] = sk; TOOLS[k]["scope_note"] = note
TI = os.path.join(ROOT,"output","audit_skills","TOOL_INDEX.json")
json.dump(TOOLS, open(TI,"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("  工具索引重建: %d 个（归档 6 个旧克隆后）→ %s" % (len(TOOLS), os.path.basename(TI)))
