# -*- coding: utf-8 -*-
import io, sys, os, re, glob, json, shutil, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
WS = os.path.join(ROOT, "skills")
import requests
H = {"User-Agent":"openclaw-audit","Accept":"application/vnd.github+json"}

# ============ 1. 三组"真冲突"的真相 ============
print("="*94); print("### A. 三组真冲突 —— 是不是同目录嵌套两份？"); print("="*94)
for skill in ["B166ER","last30days","openviking"]:
    print()
    for base,lab in [(WS,"WS"),(os.path.join(HOME,"skills"),"HOME")]:
        for f in glob.glob(os.path.join(base,"**","SKILL.md"), recursive=True):
            t = open(f, encoding="utf-8", errors="replace").read()
            m = re.search(r"^name:\s*(.+)$", t, re.M)
            nm = (m.group(1).strip() if m else os.path.basename(os.path.dirname(f)))
            if nm != skill and os.path.basename(os.path.dirname(f)) != skill: continue
            rel = os.path.relpath(f, base).replace(os.sep,"/")
            print("   %-6s %-58s %7d B" % (lab, rel[:58], len(t)))

# ============ 2. 从 GitHub 官方注册表装真填补缺口的 ============
print()
print("="*94); print("### B. 从 GitHub 安装（openclaw/clawhub 官方注册表）"); print("="*94)
WANT = {
 "writing-evals":        "自检/回归/评测写法 —— 补『断言与自检』缺口",
 "autoreview":          "自动代码审阅 —— 补『验证断言』缺口",
 "technical-documentation": "技术文档写作规范 —— 补『范式库写作』",
}
t = requests.get("https://api.github.com/repos/openclaw/clawhub/git/trees/main?recursive=1", headers=H, timeout=60)
tree = {x["path"]: x for x in t.json().get("tree",[])}
for name, why in WANT.items():
    base = ".agents/skills/%s/" % name
    files = [p for p in tree if p.startswith(base) and tree[p]["type"] == "blob"]
    if not files:
        print("   ★ %-28s 注册表里没有" % name); continue
    dst = os.path.join(WS, name)
    os.makedirs(dst, exist_ok=True)
    got = 0
    for p in files:
        rel = p[len(base):]
        if not rel: continue
        r = requests.get("https://raw.githubusercontent.com/openclaw/clawhub/main/%s" % p, headers=H, timeout=40)
        if r.status_code != 200: continue
        out = os.path.join(dst, rel.replace("/", os.sep))
        os.makedirs(os.path.dirname(out), exist_ok=True)
        open(out, "wb").write(r.content)
        got += 1
    has = os.path.exists(os.path.join(dst, "SKILL.md"))
    print("   %s %-28s %2d 文件 ｜ SKILL.md=%s ｜ %s" % ("OK " if has else "★", name, got, has, why))
