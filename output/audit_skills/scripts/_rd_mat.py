# -*- coding: utf-8 -*-
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = "D:/B166ER-openclaw/workspace"
def show(rel, head=0, tbl=0, key=0):
    p = os.path.join(ROOT, rel)
    if not os.path.exists(p):
        print("!! MISSING:", rel); return
    t = open(p, encoding="utf-8", errors="replace").read()
    print("=" * 100)
    print("FILE:", rel, "|", os.path.getsize(p), "B")
    print("=" * 100)
    lines = t.split("\n")
    if head:
        print("--- 章节 ---")
        for l in lines:
            if re.match(r"^#{1,4}\s+", l.strip()):
                print("  ", l.strip()[:120])
    if tbl:
        print("--- 表格行 ---")
        n = 0
        for l in lines:
            s = l.strip()
            if s.startswith("|") and s.count("|") >= 3:
                print("  ", s[:200]); n += 1
                if n >= tbl: break
    if key:
        print("--- 关键行 ---")
        n = 0
        for l in lines:
            s = l.strip()
            if any(k in s for k in ["信源", "等级", "优先级", "主源", "一手", "回源", "核验", "排查", "反爬", "兜底"]):
                print("  ", s[:200]); n += 1
                if n >= key: break
    print()
show("anyi-ops-kb/04_行业研究/2026国庆酒店行业全景/信源矩阵2026国庆排查总表_2026-10-11.md", head=1, tbl=16, key=10)
show("anyi-ops-kb/00_方法论/市场报告范式_v1.0_2026-10-16.md", head=1, key=14)
show("anyi-ops-kb/00_全域商业市场认知/02_资本资产金融/05_信源矩阵扩展KLM_资本资产金融_v1.0_2026-10-25.md", head=1, tbl=10, key=8)
