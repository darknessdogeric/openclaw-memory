# -*- coding: utf-8 -*-
import io, sys, os, re, glob, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")

print("="*94); print("### A. TOOLS.md —— 恢复源（git HEAD）"); print("="*94)
r = subprocess.run(["git","-C",ROOT,"show","HEAD:TOOLS.md"], capture_output=True, timeout=60)
if r.returncode == 0:
    b = r.stdout
    print("  HEAD 版本: %d B ｜ 行 %d" % (len(b), b.count(b"\n")+1))
    t = b.decode("utf-8","replace")
    heads = [l for l in t.split("\n") if l.startswith("#")]
    print("  章节:")
    for h in heads: print("     ", h[:96])
    skill_lines = [l for l in t.split("\n") if re.search(r"skills[\\/]", l)]
    print("  含技能路径的行: %d" % len(skill_lines))
    for l in skill_lines[:14]: print("     ", l.strip()[:104])
    open(os.path.join(ROOT,"output","audit_skills","TOOLS_HEAD.md"),"wb").write(b)
    print("  已导出: output/audit_skills/TOOLS_HEAD.md")
else:
    print("  ★ HEAD 里没有")

print()
print("="*94); print("### B. 8 个无 description 技能的原文头部（用于写准确描述）"); print("="*94)
targets = ["cad-batch-processing","cost-governor","hotel-feasibility-report","interior-fullplan",
           "officecli","en","zh-CN","skill-vetter"]
for base,lab in [(os.path.join(ROOT,"skills"),"WS"),(os.path.join(HOME,"skills"),"HOME")]:
    for t in targets:
        f = os.path.join(base,t,"SKILL.md")
        if not os.path.exists(f): continue
        txt = open(f, encoding="utf-8", errors="replace").read()
        print()
        print("  --- %s/%s (%d B) ---" % (lab,t,len(txt)))
        print("\n".join("      "+x for x in txt.split("\n")[:14]))

print()
print("="*94); print("### C. HOME/skills 是不是 WS 的副本（junction/硬链接/独立）"); print("="*94)
import hashlib
def md5(p): return hashlib.md5(open(p,"rb").read()).hexdigest()[:8]
wsmap = {}
for f in glob.glob(os.path.join(ROOT,"skills","**","SKILL.md"), recursive=True):
    wsmap.setdefault(md5(f), []).append(f)
same = 0; diff = 0
for f in glob.glob(os.path.join(HOME,"skills","**","SKILL.md"), recursive=True):
    h = md5(f)
    if h in wsmap: same += 1
    else: diff += 1
print("  HOME 中与 WS 内容逐字节相同: %d ｜ 不同: %d" % (same, diff))
try:
    import subprocess as sp
    out = sp.run(["cmd","/c","dir","/AL","%s" % os.path.join(HOME,"skills")], capture_output=True, timeout=40)
    j = out.stdout.decode("gbk","replace")
    print("  是否符号链接/Junction:", "是" if ("SYMLINK" in j or "JUNCTION" in j) else "否（真实目录）")
except Exception as e:
    print("  判定失败", str(e)[:60])

print()
print("="*94); print("### D. OpenClaw 实际读取哪个技能目录"); print("="*94)
cfg = os.path.join(ROOT,"openclaw.json")
if os.path.exists(cfg):
    c = open(cfg, encoding="utf-8", errors="replace").read()
    for m in re.finditer(r'"[^"]*skills[^"]*"\s*:\s*("[^"]*"|\[[^\]]*\])', c):
        print("   ", m.group(0)[:120])
else:
    print("   openclaw.json 不存在")
for f in [os.path.join(HOME,".openclaw","openclaw.json"), os.path.join(ROOT,"..","openclaw.json")]:
    if os.path.exists(f):
        c = open(f, encoding="utf-8", errors="replace").read()
        hits = re.findall(r'"[^"]*skills?[^"]*"\s*:\s*("[^"]*"|\[[^\]]*\])', c)
        print("   %s -> %s" % (f, hits[:3] if hits else "无 skills 字段"))
print()
print("  AGENTS.md 里 skills 目录的表述:")
ag = open(os.path.join(ROOT,"AGENTS.md"), encoding="utf-8", errors="replace").read()
for l in ag.split("\n"):
    if re.search(r"skills[/\\]|技能", l) and re.search(r"位置|目录|位置\*\*|扫描", l):
        print("     ", l.strip()[:118])
