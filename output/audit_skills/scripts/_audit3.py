# -*- coding: utf-8 -*-
import io, sys, os, re, glob, json, hashlib, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
R = json.load(open(os.path.join(ROOT,"output","audit_skills","inventory.json"), encoding="utf-8"))

print("="*94); print("### A. AGENTS.md 里的技能调用逻辑（现状）"); print("="*94)
ag = open(os.path.join(ROOT,"AGENTS.md"), encoding="utf-8", errors="replace").read()
for i,l in enumerate(ag.split("\n")):
    if re.search(r"(skill|Skills|clawhub|可用 skills|available_skills)", l):
        print("  L%-4d %s" % (i+1, l.strip()[:150]))
print()
print("  ★ AGENTS.md 中是否存在「技能路由表 / 决策树」:", "是" if re.search(r"(路由表|决策树|什么时候用哪个技能)", ag) else "否")
print("  ★ 是否存在「技能总索引」:", "是" if "SKILLS_INDEX" in ag or "技能索引" in ag else "否")

print()
print("="*94); print("### B. 27 组「同名不同内容」的技能 —— 谁是权威？"); print("="*94)
LOCS = [("WS", os.path.join(ROOT,"skills")), ("HOME", os.path.join(HOME,"skills")), ("CLAUDE", os.path.join(HOME,".claude","skills"))]
def load(loc):
    out = {}
    base = dict(LOCS)[loc]
    for f in glob.glob(os.path.join(base,"**","SKILL.md"), recursive=True):
        t = open(f, encoding="utf-8", errors="replace").read()
        nm = os.path.basename(os.path.dirname(f))
        m = re.search(r"^name:\s*(\S+)", t, re.M)
        out[m.group(1) if m else nm] = (f, t)
    return out
cache = {l: load(l) for l,_ in LOCS}
conf = []
for k, locs in R["dupes"]["differ"]:
    detail = []
    for l in locs:
        f, t = cache[l].get(k, (None,""))
        detail.append("%s(%d B)" % (l, len(t)))
    conf.append((k, detail))
for k, d in conf[:30]:
    print("  %-34s %s" % (k[:34], " | ".join(d)))
print("  → 共 %d 组冲突" % len(conf))
# 谁更新
print()
print("  ★ 按 mtime 判定最近版本（谁更新谁权威）：")
newer = collections = 0
cnt_by_loc = {"WS":0,"HOME":0,"CLAUDE":0}
for k, locs in R["dupes"]["differ"]:
    ts = {}
    for l in locs:
        f = cache[l].get(k,(None,""))[0]
        if f and os.path.exists(f): ts[l] = os.path.getmtime(f)
    if ts:
        w = max(ts, key=lambda x: ts[x]); cnt_by_loc[w] += 1
print("     ", cnt_by_loc)

print()
print("="*94); print("### C. 三处目录的性质对比（是不是同源？）"); print("="*94)
import datetime
for l, base in LOCS:
    if not os.path.isdir(base): continue
    fs = [f for f in glob.glob(os.path.join(base,"**","SKILL.md"), recursive=True)]
    mt = [os.path.getmtime(f) for f in fs]
    tot = sum(os.path.getsize(f) for f in fs)
    print("  %-8s %3d 份 / %7.1f KB ｜ 最早 %s ｜ 最近 %s" % (l, len(fs), tot/1024.0,
        datetime.datetime.fromtimestamp(min(mt)).strftime("%Y-%m-%d") if mt else "-",
        datetime.datetime.fromtimestamp(max(mt)).strftime("%Y-%m-%d") if mt else "-"))
# 是否同一套
ws = set(os.path.basename(os.path.dirname(f)) for f in glob.glob(os.path.join(LOCS[0][1],"**","SKILL.md"), recursive=True))
hm = set(os.path.basename(os.path.dirname(f)) for f in glob.glob(os.path.join(LOCS[1][1],"**","SKILL.md"), recursive=True))
cm = set(os.path.basename(os.path.dirname(f)) for f in glob.glob(os.path.join(LOCS[2][1],"**","SKILL.md"), recursive=True))
print()
print("  目录名交集：WS∩HOME %d ｜ WS∩CLAUDE %d ｜ HOME∩CLAUDE %d ｜ 三者共有 %d" % (
    len(ws&hm), len(ws&cm), len(hm&cm), len(ws&hm&cm)))
print("  仅在 WS: %d ｜ 仅在 HOME: %d ｜ 仅在 CLAUDE: %d" % (len(ws-hm-cm), len(hm-ws-cm), len(cm-ws-hm)))

print()
print("="*94); print("### D. 8 个无 description + 42 个引用缺失 明细"); print("="*94)
print("  无 description:", ", ".join(R["nodesc"]))
print()
from collections import Counter
c = Counter(k for k,_ in R["broken_ref"])
for k,n in c.most_common(18): print("     引用缺失 %-32s %d 处" % (k[:32], n))
