# -*- coding: utf-8 -*-
import io, sys, os, re, glob, json, hashlib, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
import requests
H = {"User-Agent":"openclaw-audit","Accept":"application/vnd.github+json"}

print("="*94); print("### A. 核『B166ER Knowledge & Skill Router』真实状态"); print("="*94)
for base in [os.path.join(ROOT,"skills"), os.path.join(HOME,"skills")]:
    for f in glob.glob(os.path.join(base,"**","*Router*","SKILL.md"), recursive=True) + glob.glob(os.path.join(base,"**","*router*","SKILL.md"), recursive=True):
        sz = os.path.getsize(f)
        body = open(f, encoding="utf-8", errors="replace").read()
        print("  %-72s %6d B ｜ 内容 %d 字" % (os.path.relpath(f, base).replace(os.sep,"/")[:72], sz, len(body.strip())))
        if body.strip(): print("     首行:", body.strip().split("\n")[0][:90])

print()
print("="*94); print("### B. CLAUDE 独有的 66 个技能是什么"); print("="*94)
def names(base):
    out = {}
    for f in glob.glob(os.path.join(base,"**","SKILL.md"), recursive=True):
        b = open(f,"rb").read()
        m = re.search(rb"^name:\s*(\S+)", b, re.M)
        out[m.group(1).decode("utf-8","replace") if m else os.path.basename(os.path.dirname(f))] = f
    return out
WS = names(os.path.join(ROOT,"skills")); HM = names(os.path.join(HOME,"skills")); CL = names(os.path.join(HOME,".claude","skills"))
uniq_cl = sorted(set(CL) - set(WS) - set(HM))
print("  CLAUDE 独有: %d 个" % len(uniq_cl))
print("  ", ", ".join(uniq_cl[:70]))
fam = {}
for n in uniq_cl:
    k = "gstack" if n.startswith("gstack") else ("arkcli" if n.startswith("arkcli") else "other")
    fam[k] = fam.get(k,0)+1
print("  家族分布:", fam)

print()
print("="*94); print("### C. awesome-openclaw-skills 真实结构（categories/）"); print("="*94)
r = requests.get("https://api.github.com/repos/VoltAgent/awesome-openclaw-skills/contents/categories", headers=H, timeout=40)
if r.status_code == 200:
    cats = [i["name"] for i in r.json()]
    print("  categories 数: %d" % len(cats))
    print("  ", ", ".join(cats[:30]))
    t = requests.get("https://api.github.com/repos/VoltAgent/awesome-openclaw-skills/git/trees/main?recursive=1", headers=H, timeout=60)
    if t.status_code == 200:
        tr = t.json().get("tree",[])
        print("  全树条目: %d" % len(tr))
        mds = [x["path"] for x in tr if x["path"].lower().endswith((".md",".mdx"))]
        print("  .md/.mdx 文件: %d" % len(mds))
        KW = ["ocr","pdf","assert","regress","encod","valid","audit","lint","docx","office","spread","test"]
        cand = sorted({p for p in mds if any(k in p.lower() for k in KW)})
        print("  ★ 与本方缺口相关候选 %d:" % len(cand))
        for c in cand[:26]: print("     ", c[:96])
else:
    print("  categories API rc=%s" % r.status_code)

print()
print("="*94); print("### D. openclaw/clawhub 里的 69 个技能（官方注册表）"); print("="*94)
t = requests.get("https://api.github.com/repos/openclaw/clawhub/git/trees/main?recursive=1", headers=H, timeout=60)
if t.status_code == 200:
    tr = t.json().get("tree",[])
    sk = [x["path"] for x in tr if x["path"].endswith("SKILL.md")]
    print("  SKILL.md: %d" % len(sk))
    for p in sorted(sk)[:40]: print("     ", p[:96])
