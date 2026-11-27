# -*- coding: utf-8 -*-
import io, sys, os, re, glob, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")

print("="*94); print("### A. ★ docx-md-bridge 能不能直接用？（我今天绕过了它）"); print("="*94)
d = os.path.join(ROOT, "skills", "docx-md-bridge")
for f in sorted(glob.glob(os.path.join(d, "**","*"))):
    if os.path.isfile(f):
        print("   %7d B  %s" % (os.path.getsize(f), os.path.relpath(f,d)))
# 真的跑一次
src = os.path.join(HOME,"self-improving","eval","encoding_baseline_2026-11-17.json")
test_md = os.path.join(ROOT,"output","_bridge_test.md")
open(test_md,"w",encoding="utf-8").write("# 标题一\n\n段落测试。\n\n| 列 A | 列 B |\n|---|---|\n| 1 | 2 |\n\n> 引用一行\n")
cands = []
for p in glob.glob(os.path.join(d,"**","*.py"), recursive=True):
    cands.append(p)
print()
print("  候选脚本:", [os.path.basename(x) for x in cands])
out = os.path.join(ROOT,"output","_bridge_test.docx")
for p in cands:
    try:
        r = subprocess.run([sys.executable, p, test_md, out], capture_output=True, timeout=120)
        ok = os.path.exists(out)
        print("  试跑 %-24s rc=%s 产出=%s %s" % (os.path.basename(p), r.returncode, ok,
              (r.stdout.decode("utf-8","replace")[:60] if ok else r.stderr.decode("utf-8","replace")[-160:])))
        if ok:
            import docx
            d2 = docx.Document(out)
            print("     → 段落 %d ｜ 表格 %d ｜ 表行 %d" % (len([x for x in d2.paragraphs if x.text.strip()]),
                  len(d2.tables), sum(len(t.rows) for t in d2.tables)))
            break
    except Exception as e:
        print("  试跑 %s 失败 %s" % (os.path.basename(p), str(e)[:80]))

print()
print("="*94); print("### B. 8 个无 description 的技能 —— 是什么/空文件吗"); print("="*94)
targets = ["cad-batch-processing","cost-governor","hotel-feasibility-report","interior-fullplan",
           "officecli","en","zh-CN","skill-vetter"]
for base,label in [(os.path.join(ROOT,"skills"),"WS"), (os.path.join(HOME,"skills"),"HOME"), (os.path.join(HOME,".claude","skills"),"CLAUDE")]:
    for t in targets:
        p = os.path.join(base, t, "SKILL.md")
        if os.path.exists(p):
            sz = os.path.getsize(p)
            body = open(p, encoding="utf-8", errors="replace").read()
            first = next((l.strip() for l in body.split("\n") if l.strip() and not l.startswith("---")), "")
            print("  %-7s %-26s %7d B  %s" % (label, t, sz, first[:62]))

print()
print("="*94); print("### C. 42 处「引用缺失」—— 真断 or 我正则误报？"); print("="*94)
R = json.load(open(os.path.join(ROOT,"output","audit_skills","inventory.json"), encoding="utf-8"))
from collections import Counter
cnt = Counter(k for k,_ in R["broken_ref"])
real = 0; falsep = 0
samples = []
for k,n in cnt.most_common(20):
    found = []
    for base in [os.path.join(ROOT,"skills"), os.path.join(HOME,"skills"), os.path.join(HOME,".claude","skills")]:
        for p in glob.glob(os.path.join(base,"**","SKILL.md"), recursive=True):
            b = open(p, encoding="utf-8", errors="replace").read()
            if re.search(r"^name:\s*%s\s*$" % re.escape(k), b, re.M):
                for m in re.finditer(r"(?:scripts|references|templates|assets)/([A-Za-z0-9_\-\.]+)", b):
                    cand = os.path.join(os.path.dirname(p), m.group(0).replace("/", os.sep))
                    if not os.path.exists(cand):
                        found.append(m.group(0))
                break
    st = "真缺失 %s" % found[0] if found else "误报（该技能在别处有配套文件）"
    if found: real += 1
    else: falsep += 1
    samples.append("  %-30s %s" % (k[:30], st))
print("\n".join(samples))
print("  → 粗判：真缺失 %d 组 / 误报 %d 组" % (real, falsep))

print()
print("="*94); print("### D. GitHub / clawhub 通路"); print("="*94)
CLI = os.path.join(HOME, "AppData", "Roaming", "npm", "openclaw.cmd")
r = subprocess.run([CLI,"clawhub","--help"], capture_output=True, timeout=60)
print("  clawhub --help rc=%s" % r.returncode)
print("  " + (r.stdout.decode("utf-8","replace")[:300] or r.stderr.decode("utf-8","replace")[:300]))
try:
    import requests
    rr = requests.get("https://api.github.com/search/repositories?q=openclaw+skills&per_page=3", timeout=30,
                      headers={"User-Agent":"openclaw-audit"})
    print("  GitHub API rc=%s total=%s" % (rr.status_code, rr.json().get("total_count","?")))
    for it in rr.json().get("items",[])[:3]:
        print("     %s  ★%s  %s" % (it["full_name"], it["stargazers_count"], (it.get("description") or "")[:60]))
except Exception as e:
    print("  GitHub API 失败:", str(e)[:100])
