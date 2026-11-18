# -*- coding: utf-8 -*-
import io, sys, os, json, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
m = open(os.path.join(ROOT,"MEMORY.md"), encoding="utf-8", errors="replace").read()
print("=== MEMORY.md %d B 尾部 30 行 ===" % len(m))
print("\n".join(m.split("\n")[-30:]))
print()
print("=== project 标记数 ===", m.count("<!-- project:"))
WFP = os.path.join(ROOT,"output","audit_skills","WORKFLOWS.json")
W = json.load(open(WFP, encoding="utf-8"))
print()
print("=== 工作流里 ★待补 的条目 ===")
for w in W:
    if any(str(p).startswith("★") for p in w.get("paradigms",[])):
        print("  %-24s %s" % (w["task"], w.get("paradigms")))
