# -*- coding: utf-8 -*-
import io, sys, os, re, json, glob, shutil, ast, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
AUD = os.path.join(ROOT,"output","audit_skills")
SC = os.path.join(ROOT,"toolbox","selfcheck.py")

print("="*100); print("### A. 内容级依赖检测（不靠名字）"); print("="*100)
REG = json.load(open(os.path.join(AUD,"SKILL_REGISTRY.json"), encoding="utf-8"))
EXT = re.compile(r"\b(arkcli|gstack|npx\s+[\w@\-\/\.]+|npm\s+i\s+[\w@\-\/\.]+|pip\s+install\s+[\w\-\.]+|brew\s+install\s+[\w\-\.]+|uv\s+(?:tool\s+)?(?:pip\s+)?install\s+[\w\-\.]+|docker\s+run\s+[\w\-\/\.]+)", re.I)
BINS = ["node","npm","npx","uv","docker","git","arkcli","gstack","playwright","python3","brew"]
import shutil as sh
which = {b:(sh.which(b) or "") for b in BINS}
dep_map = {}
for r in REG:
    d = os.path.dirname(r["canonical"])
    deps = set()
    for f in glob.glob(os.path.join(d,"**","*"), recursive=True):
        if not os.path.isfile(f) or os.path.getsize(f) > 400000: continue
        if not f.endswith((".md",".py",".sh",".json",".js",".ts",".txt")): continue
        try: t = open(f, encoding="utf-8", errors="replace").read()
        except Exception: continue
        for m in EXT.finditer(t):
            g = m.group(1).lower()
            tok = g.split()[0]
            deps.add(tok)
    r["ext_deps"] = sorted(deps)
    dep_map[r["name"]] = deps
miss = sorted({x for v in dep_map.values() for x in v if x not in ("node","npm","npx","uv","docker","git","python3","brew")})
print("  检出外部二进制依赖: %s" % (", ".join(miss) if miss else "无"))
cnt = {}
for n,v in dep_map.items():
    if v: cnt.setdefault(tuple(sorted(v)), []).append(n)
for k,v in sorted(cnt.items(), key=lambda x:-len(x[1])):
    ready = all(which.get(x) for x in k)
    print("   依赖 %-28s %3d 个技能 ｜ 就绪=%s ｜ 例: %s" % (", ".join(k), len(v), ready, ", ".join(v[:3])))

# 重新判定闲置
CORPUS = []
for pat in [os.path.join(ROOT,"memory","*.md"), os.path.join(HOME,"self-improving","**","*.md"),
            os.path.join(ROOT,"anyi-ops-kb","**","*.md")]:
    for f in glob.glob(pat, recursive=True):
        try: CORPUS.append(open(f, encoding="utf-8", errors="replace").read()[:200000])
        except Exception: pass
blob = "\n".join(CORPUS)
verdict = []
for r in REG:
    n = r["name"]
    if blob.count(n) > 0:
        r["status"] = "active"; r["idle_verdict"] = ""
        continue
    deps = dep_map[n]
    blocking = [x for x in deps if not which.get(x)]
    if blocking:
        v = "阻塞：缺 %s —— 保留在库但标未就绪，路由时跳过" % ", ".join(blocking)
        act = "hold"
    elif deps:
        v = "依赖就绪（%s）—— 建议纳入固定工作流以激活" % ", ".join(deps)
        act = "activate"
    else:
        v = "无外部依赖且未被调用 —— 建议归档（内容多为流程说明，无可执行件）"
        act = "archive"
    r["status"] = "idle_pending_activation" if act in ("hold","activate") else "idle_candidate_archive"
    r["idle_verdict"] = v
    verdict.append({"name":n,"deps":deps,"action":act,"verdict":v,"path":r["canonical"],"bytes":r["bytes"],"files":r["files"]})
json.dump(REG, open(os.path.join(AUD,"SKILL_REGISTRY.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump(verdict, open(os.path.join(AUD,"IDLE_VERDICT.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
ac = {}
for v in verdict: ac[v["action"]] = ac.get(v["action"],0)+1
print()
print("  闲置 %d 个，裁决: %s" % (len(verdict), ac))
for a in ("archive","hold","activate"):
    ex = [v["name"] for v in verdict if v["action"]==a][:10]
    if ex: print("     %-9s %d 个: %s" % (a, ac.get(a,0), ", ".join(ex)))

print()
print("="*100); print("### B. 执行归档（idle_candidate_archive）—— 移到 skills/_archive/，可回滚"); print("="*100)
ARC = os.path.join(ROOT,"skills","_archive","idle_2026-11-18")
os.makedirs(ARC, exist_ok=True)
moved = []
for v in verdict:
    if v["action"] != "archive": continue
    src = v["path"]; d = os.path.dirname(src)
    name = os.path.basename(d)
    dst = os.path.join(ARC, name)
    if os.path.exists(dst): continue
    base = os.path.dirname(d)
    # 若技能位于家族目录内（父目录也含 SKILL.md），只移动该技能目录
    shutil.move(d, dst)
    moved.append((name, v["bytes"]))
print("  已归档 %d 个技能 → skills/_archive/idle_2026-11-18/" % len(moved))
for n,b in moved: print("     %-28s %6d B" % (n, b))
json.dump({"date":"2026-11-18","rule":"闲置且无外部依赖 → 归档（可回滚：移回原位即可）",
           "archived":[{"name":n,"bytes":b} for n,b in moved],
           "hold_reason":"缺外部二进制，保留待装","activate_reason":"依赖就绪，建议纳入工作流"},
          open(os.path.join(AUD,"idle_archive_manifest_2026-11-18.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)

print()
print("="*100); print("### C. 修 C14 的 _archive 排除漏洞 + 重建注册表"); print("="*100)
t = open(SC, encoding="utf-8", errors="replace").read()
old = '''            d = os.path.dirname(f)
            anc = os.path.relpath(d, base).split(os.sep)[:-1]
            if any(os.path.exists(os.path.join(base, *anc[:i+1], "SKILL.md")) for i in range(len(anc))):
                continue'''
new = '''            d = os.path.dirname(f)
            rel = os.path.relpath(d, base).split(os.sep)
            if any(x.startswith("_") for x in rel):
                continue
            anc = rel[:-1]
            if any(os.path.exists(os.path.join(base, *anc[:i+1], "SKILL.md")) for i in range(len(anc))):
                continue'''
assert old in t
t = t.replace(old, new, 1)
ast.parse(t)
open(SC,"w",encoding="utf-8",newline="\n").write(t)
print("  ✔ C14 已排除 _ 开头目录（归档区不计入技能数）")

# 重建注册表（用同一排除规则）
def real_skills(base):
    out = {}
    if not os.path.isdir(base): return out
    for f in sorted(glob.glob(os.path.join(base,"**","SKILL.md"), recursive=True)):
        d = os.path.dirname(f); rel = os.path.relpath(d, base).split(os.sep)
        if any(x.startswith("_") for x in rel): continue
        anc = rel[:-1]
        if any(os.path.exists(os.path.join(base, *anc[:i+1], "SKILL.md")) for i in range(len(anc))): continue
        tx = open(f, encoding="utf-8", errors="replace").read()
        fm = {}
        if tx.startswith("---"):
            e = tx.find("\n---", 3)
            if e > 0:
                for line in tx[3:e].split("\n"):
                    if ":" in line:
                        k,v = line.split(":",1); fm[k.strip().lower()] = v.strip().strip("\"'")
        nm = fm.get("name") or os.path.basename(d)
        out[nm] = {"dir":os.path.basename(d),"path":f,"desc":fm.get("description",""),
                   "scripts":len(glob.glob(os.path.join(d,"scripts","*.py"))),
                   "refs":len(glob.glob(os.path.join(d,"references","*.md"))),
                   "bytes":len(tx),
                   "files":len([x for x in glob.glob(os.path.join(d,"**","*"),recursive=True) if os.path.isfile(x)])}
    return out
LOCS = [("WS",os.path.join(ROOT,"skills")),("HOME",os.path.join(HOME,"skills")),("CLAUDE",os.path.join(HOME,".claude","skills"))]
reg = {}
for lab, base in LOCS:
    for nm, i in real_skills(base).items():
        reg.setdefault(nm, {"name":nm,"locs":{}})["locs"][lab] = i
def canon(e):
    for lab in ("WS","CLAUDE","HOME"):
        if lab in e["locs"]: return lab, e["locs"][lab]
    return "WS", list(e["locs"].values())[0]
oldst = {r["name"]: r.get("status","active") for r in REG}
oldvd = {r["name"]: r.get("idle_verdict","") for r in REG}
rows = []
for nm, e in reg.items():
    lab, i = canon(e)
    rows.append({"name":nm,"canonical":i["path"],"canonical_loc":lab,"desc":i["desc"],
                 "scripts":i["scripts"],"refs":i["refs"],"bytes":i["bytes"],"files":i["files"],
                 "all_locs":sorted(e["locs"].keys()),"has_desc":bool(i["desc"]),
                 "status":oldst.get(nm,"active"),"idle_verdict":oldvd.get(nm,"")})
rows.sort(key=lambda r:r["name"].lower())
json.dump(rows, open(os.path.join(AUD,"SKILL_REGISTRY.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("  注册表重建: %d 条 ｜ active %d ｜ 标注 %d" % (len(rows), sum(1 for r in rows if r["status"]=="active"), sum(1 for r in rows if r["status"]!="active")))

print()
r = subprocess.run([sys.executable, SC], capture_output=True, timeout=400)
print(r.stdout.decode("utf-8","replace"))
print("退出码:", r.returncode)
