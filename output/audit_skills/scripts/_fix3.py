# -*- coding: utf-8 -*-
import io, sys, os, re, json, glob, shutil, ast, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
AUD = os.path.join(ROOT,"output","audit_skills")
SC = os.path.join(ROOT,"toolbox","selfcheck.py")

# ============ 1. C14 改用祖先判据（与注册表生成同口径） ============
t = open(SC, encoding="utf-8", errors="replace").read()
old_c14 = '''    disk = set()
    for base in (os.path.join(ROOT,"skills"), os.path.join(HOME,"skills"), os.path.join(HOME,".claude","skills")):
        if not os.path.isdir(base):
            continue
        for f in glob.glob(os.path.join(base,"*","SKILL.md")):
            d = os.path.basename(os.path.dirname(f))
            if d.startswith("_"): continue
            tx = open(f, encoding="utf-8", errors="replace").read()
            m = re.search(r"^name:\\s*(.+)$", tx, re.M)
            disk.add((m.group(1).strip() if m else d).strip('"\\''))'''
new_c14 = '''    disk = set()
    # ★ 与注册表生成同口径：祖先目录若含 SKILL.md 则视为技能内部副本，不算独立技能
    for base in (os.path.join(ROOT,"skills"), os.path.join(HOME,"skills"), os.path.join(HOME,".claude","skills")):
        if not os.path.isdir(base):
            continue
        for f in glob.glob(os.path.join(base,"**","SKILL.md"), recursive=True):
            d = os.path.dirname(f)
            anc = os.path.relpath(d, base).split(os.sep)[:-1]
            if any(os.path.exists(os.path.join(base, *anc[:i+1], "SKILL.md")) for i in range(len(anc))):
                continue
            tx = open(f, encoding="utf-8", errors="replace").read()
            m = re.search(r"^name:\\s*(.+)$", tx, re.M)
            disk.add((m.group(1).strip() if m else os.path.basename(d)).strip('"\\''))'''
assert old_c14 in t, "C14 原文未命中"
t = t.replace(old_c14, new_c14, 1)

# ============ 2. 新增 C19：范式库可路由 + 工作流绑定范式 ============
C19 = '''# ---------------- C19 范式库可路由（2026-11-18 技能库审计新增） ----------------
@check("C19", "范式须可路由（有触发词）且工作流须绑定范式", "150 条范式若 143 条无『何时用』＝ 有范式但调不出来，与技能同款病")
def c19():
    p = os.path.join(ROOT, "output", "audit_skills", "PARADIGM_REGISTRY.json")
    if not os.path.exists(p):
        return False, "缺 PARADIGM_REGISTRY.json", []
    try:
        P = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        return False, "范式注册表解析失败 %s" % str(e)[:50], []
    nokw = [x.get("file","?") for x in P if not (x.get("keywords") or x.get("when"))]
    if nokw:
        return False, "无触发词 %d 条: %s" % (len(nokw), ",".join(nokw[:3])), nokw[:5]
    wf = os.path.join(ROOT, "output", "audit_skills", "WORKFLOWS.json")
    if not os.path.exists(wf):
        return False, "缺 WORKFLOWS.json", []
    W = json.load(open(wf, encoding="utf-8"))
    nb = [w.get("task","?") for w in W if not (w.get("paradigms") or [])]
    if nb:
        return False, "未绑定范式的工作流 %d 条: %s" % (len(nb), ",".join(nb[:3])), nb[:5]
    return True, "范式 %d 条全部可路由 ｜ %d 条工作流全部绑定范式" % (len(P), len(W)), []

'''
anchor = "def run(as_json=False):"
assert anchor in t and "C19" not in t
t = t.replace(anchor, C19 + anchor, 1)
ast.parse(t)
open(SC,"w",encoding="utf-8",newline="\n").write(t)
print("✔ C14 已改祖先判据 ｜ C19 已插入 ｜ selfcheck %d B" % len(t))

# ============ 3. 闲置技能裁决 ============
print()
print("="*100); print("### 闲置技能裁决（依赖是否就绪）"); print("="*100)
BINS = ["node","npm","npx","python3","uv","docker","brew","arkcli","gstack","git"]
which = {b: (shutil.which(b) or "") for b in BINS}
print("  环境可用: %s" % ", ".join("%s=%s" % (b, "有" if which[b] else "无") for b in BINS))
REG = json.load(open(os.path.join(AUD,"SKILL_REGISTRY.json"), encoding="utf-8"))
CORPUS = []
for pat in [os.path.join(ROOT,"memory","*.md"), os.path.join(HOME,"self-improving","*.md"),
            os.path.join(HOME,"self-improving","**","*.md"), os.path.join(ROOT,"anyi-ops-kb","**","*.md")]:
    for f in glob.glob(pat, recursive=True):
        try: CORPUS.append(open(f, encoding="utf-8", errors="replace").read()[:200000])
        except Exception: pass
blob = "\n".join(CORPUS)
DEPMAP = [("arkcli","arkcli"),("gstack","gstack"),("playwright-cli","node"),("plan-","gstack"),
          ("design-","node"),("autoplan","gstack"),("canary","node"),("review","gstack"),
          ("qa","gstack"),("ship","gstack"),("ship","node")]
idle, verdict = [], []
for r in REG:
    n = r["name"]
    if blob.count(n) > 0: continue
    idle.append(n)
    dep = ""
    for pref, b in DEPMAP:
        if n.startswith(pref) or pref == n:
            dep = b; break
    ready = bool(which.get(dep)) if dep else True
    if dep and not ready:
        v = "需外部依赖（%s 未装）—— 保留但不路由，标注为未就绪" % dep
    elif dep:
        v = "依赖就绪（%s）—— 纳入工作流即可激活" % dep
    else:
        v = "无外部依赖 —— 建议纳入工作流或归档"
    verdict.append({"name":n,"dep":dep,"ready":ready,"verdict":v,"path":r["canonical"]})
json.dump(verdict, open(os.path.join(AUD,"IDLE_VERDICT.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
cnt = {}
for v in verdict:
    k = v["verdict"].split("——")[0].strip()
    cnt[k] = cnt.get(k,0)+1
print("  闲置（从未被语料提及）%d 个:" % len(idle))
for k,v in cnt.items(): print("     %-40s %d 个" % (k, v))
# 把 status 写回注册表
st = {v["name"]: v for v in verdict}
for r in REG:
    v = st.get(r["name"])
    r["status"] = "idle_pending_activation" if v else "active"
    if v: r["idle_verdict"] = v["verdict"]
json.dump(REG, open(os.path.join(AUD,"SKILL_REGISTRY.json"),"w",encoding="utf-8"), ensure_ascii=False, indent=1)
print("  注册表已标 status：active %d ｜ idle_pending_activation %d" % (
    sum(1 for r in REG if r["status"]=="active"), sum(1 for r in REG if r["status"]!="active")))

# ============ 4. 跑自检 ============
print()
r = subprocess.run([sys.executable, SC], capture_output=True, timeout=400)
print(r.stdout.decode("utf-8","replace"))
print("退出码:", r.returncode)
