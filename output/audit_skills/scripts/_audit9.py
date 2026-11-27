# -*- coding: utf-8 -*-
import io, sys, os, re, glob, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
import requests
H = {"User-Agent":"openclaw-audit","Accept":"application/vnd.github+json"}

print("="*94); print("### A. ★ TOOLS.md —— 本该是技能总索引，它去哪了？"); print("="*94)
p = os.path.join(ROOT, "TOOLS.md")
print("  当前存在:", os.path.exists(p))
r = subprocess.run(["git","-C",ROOT,"status","--porcelain","--","TOOLS.md"], capture_output=True, timeout=40)
print("  git status:", r.stdout.decode("utf-8","replace").strip() or "(clean)")
r2 = subprocess.run(["git","-C",ROOT,"log","--all","--oneline","--","TOOLS.md"], capture_output=True, timeout=40)
print("  git log:", r2.stdout.decode("utf-8","replace").strip()[:200] or "(无提交)")
r3 = subprocess.run(["git","-C",ROOT,"show","HEAD:TOOLS.md"], capture_output=True, timeout=40)
if r3.returncode == 0:
    b = r3.stdout
    print("  ★ HEAD 里有 TOOLS.md: %d B ｜ 技能相关行 %d" % (len(b), sum(1 for l in b.decode("utf-8","replace").split("\n") if "skill" in l.lower() or "Skill" in l)))
    head = b.decode("utf-8","replace").split("\n")
    for i,l in enumerate(head[:26]):
        if l.strip(): print("     L%-3d %s" % (i+1, l[:118]))
else:
    print("  ★ HEAD 里也没有 TOOLS.md")

print()
print("="*94); print("### B. GitHub：能补我三个缺口的现成技能"); print("="*94)
for cat in ["pdf-and-documents","notes-and-pkm","data-and-analytics","cli-utilities"]:
    try:
        rr = requests.get("https://raw.githubusercontent.com/VoltAgent/awesome-openclaw-skills/main/categories/%s.md" % cat,
                         headers={"User-Agent":"openclaw-audit"}, timeout=30)
        if rr.status_code != 200: 
            print("  %-26s rc=%s" % (cat, rr.status_code)); continue
        t = rr.text
        rows = re.findall(r"^\|\s*\[?([^\]|]{2,60})\]?[^|]*\|\s*([^|]{2,90})", t, re.M)
        print()
        print("  【%s】 %d 行" % (cat, len(rows)))
        for a,b2 in rows[:14]:
            print("     %-46s %s" % (a.strip()[:46], b2.strip()[:56]))
    except Exception as e:
        print("  %-26s 失败 %s" % (cat, str(e)[:60]))
