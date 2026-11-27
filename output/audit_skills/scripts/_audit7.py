# -*- coding: utf-8 -*-
import io, sys, os, re, glob, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
BASES = {"WS": os.path.join(ROOT,"skills"), "HOME": os.path.join(HOME,"skills"), "CLAUDE": os.path.join(HOME,".claude","skills")}

print("="*94); print("### A. ★ 空技能（SKILL.md 0 字节或近乎空）—— 路由中枢就是空的？"); print("="*94)
empties = []
for lab, base in BASES.items():
    if not os.path.isdir(base): continue
    for f in glob.glob(os.path.join(base,"**","SKILL.md"), recursive=True):
        sz = os.path.getsize(f)
        body = open(f, encoding="utf-8", errors="replace").read()
        if sz < 120:
            empties.append((lab, os.path.relpath(f, base).replace(os.sep,"/"), sz, len(body.strip())))
print("  空/近空 SKILL.md: %d 个" % len(empties))
for lab, rel, sz, bl in empties:
    print("     %-8s %-52s %5d B (内容 %d 字)" % (lab, rel[:52], sz, bl))

print()
print("="*94); print("### B. GitHub 真实结构探测（默认分支 / 路径）"); print("="*94)
import requests
H = {"User-Agent":"openclaw-audit","Accept":"application/vnd.github+json"}
for repo in ["VoltAgent/awesome-openclaw-skills", "openclaw/clawhub"]:
    try:
        r = requests.get("https://api.github.com/repos/%s" % repo, headers=H, timeout=30)
        if r.status_code != 200:
            print("  %-40s rc=%s" % (repo, r.status_code)); continue
        j = r.json()
        print("  %-40s ★%s ｜ default=%s ｜ size=%d KB" % (repo, j["stargazers_count"], j["default_branch"], j["size"]))
        rb = j["default_branch"]
        t = requests.get("https://api.github.com/repos/%s/git/trees/%s?recursive=1" % (repo, rb), headers=H, timeout=60)
        if t.status_code == 200:
            tree = t.json().get("tree", [])
            sk = [x["path"] for x in tree if x["path"].endswith("SKILL.md")]
            print("      SKILL.md 总数: %d ｜ 总条目 %d ｜ truncated=%s" % (len(sk), len(tree), t.json().get("truncated")))
            tops = sorted({x["path"].split("/")[0] for x in tree})[:12]
            print("      顶层目录:", ", ".join(tops))
            KW = ["ocr","pdf","assert","regress","encod","valid","audit","lint","md2docx","docx","office","spreadsheet"]
            cand = sorted({p.split("/")[-2] for p in sk if any(k in p.lower() for k in KW)})
            print("      ★ 与本方缺口相关候选 %d 个:" % len(cand))
            for c in cand[:30]: print("         - %s" % c)
    except Exception as e:
        print("  %-40s 失败 %s" % (repo, str(e)[:80]))

print()
print("="*94); print("### C. git 能否恢复 17 组缺失引用（历史里有吗）"); print("="*94)
for kw in ["references/dashboard_patterns.md","references/okr-guide.md","references/douyin-ops.md",
            "scripts/verify-geometry.py","scripts/list_paradigms.py","references/china-market.md"]:
    r = subprocess.run(["git","-C",ROOT,"log","--all","--diff-filter=D","--name-only","--","*%s"%kw.split("/")[-1]],
                       capture_output=True, timeout=40)
    out = r.stdout.decode("utf-8","replace").strip()
    st = "曾存在可恢复: " + out.split("\n")[0][:60] if out else "★git 历史里也没有"
    print("  %-46s %s" % (kw, st))
