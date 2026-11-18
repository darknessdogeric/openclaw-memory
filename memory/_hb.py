# -*- coding: utf-8 -*-
import io, sys, os, re, json, glob, hashlib, difflib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
TB = os.path.join(ROOT,"toolbox")
TI = json.load(open(os.path.join(ROOT,"output","audit_skills","TOOL_INDEX.json"), encoding="utf-8"))

print("="*100); print("### A. hb 家族 246 件 —— 内容差异有多大？"); print("="*100)
hb = sorted([p for p in glob.glob(os.path.join(TB,"*.py")) if os.path.basename(p).startswith("hb")])
print("  文件数: %d" % len(hb))
def norm(p):
    t = open(p, encoding="utf-8", errors="replace").read()
    # 抹掉文件名里带的数字 ID，再看还剩多少差异
    return re.sub(r"\d{3,}", "N", t)
base = norm(hb[0])
sig = {}
for p in hb:
    h = hashlib.md5(norm(p).encode("utf-8")).hexdigest()[:8]
    sig.setdefault(h, []).append(os.path.basename(p))
print("  抹掉数字ID后，正文模板相同的组数: %d" % len(sig))
for h, fs in sorted(sig.items(), key=lambda x: -len(x[1]))[:8]:
    print("     %s  %3d 件  例: %s" % (h, len(fs), ", ".join(fs[:3])))
# 抽两件看真差异
if len(hb) >= 2:
    a = open(hb[0], encoding="utf-8", errors="replace").read().split("\n")
    b = open(hb[-1], encoding="utf-8", errors="replace").read().split("\n")
    d = [l for l in difflib.unified_diff(a, b, lineterm="", n=0)][2:]
    print()
    print("  『%s』 vs 『%s』差异行 %d 条，前 18 条:" % (os.path.basename(hb[0]), os.path.basename(hb[-1]), len(d)))
    for l in d[:18]: print("     %s" % l[:132])

print()
print("="*100); print("### B. 280 个 orphan —— 是什么"); print("="*100)
orph = [(k,v) for k,v in TI.items() if v["category"]=="orphan"]
print("  数量 %d" % len(orph))
big = sorted(orph, key=lambda x: -x[1]["bytes"])[:10]
for k,v in big:
    print("     %-34s %6d B  %s" % (k.replace("toolbox/","")[:34], v["bytes"], (v["purpose"] or "(无 docstring)")[:52]))
print()
withdoc = sum(1 for k,v in TI.items() if v["has_docstring"])
print("  全库有 docstring 的: %d / %d" % (withdoc, len(TI)))
print("  orphan 里 size>20KB 的: %d（这些很可能是真工具，只是没写 docstring）" % sum(1 for k,v in orph if v["bytes"]>20000))

print()
print("="*100); print("### C. capability 112 件 —— owner 归属状况"); print("="*100)
cap = [(k,v) for k,v in TI.items() if v["category"]=="capability"]
print("  有 owner 的: %d ｜ 无 owner 的: %d" % (sum(1 for k,v in cap if v["owner_skill"]), sum(1 for k,v in cap if not v["owner_skill"])))
fam = {}
for k,v in cap: fam.setdefault(v["family"], []).append(k.replace("toolbox/",""))
print("  capability 同族分布（前 12）:")
for f, fs in sorted(fam.items(), key=lambda x: -len(x[1]))[:12]:
    print("     %-26s %2d 件  %s" % (f[:26], len(fs), ", ".join(fs[:3])))
