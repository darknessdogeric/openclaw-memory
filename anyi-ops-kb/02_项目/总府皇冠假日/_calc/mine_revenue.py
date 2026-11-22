# -*- coding: utf-8 -*-
"""Mine 总府皇冠 first-batch extracts for revenue-structure facts."""
import io, sys, os, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SRC = r"D:\B166ER-openclaw\workspace\.tmp\extract"
OUT = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc\zf_revenue_mine.txt"

PATS = [
    r"餐饮收入|餐饮[，,、]?\s*会议|营业收入构成|收入结构|收入构成",
    r"客房收入|客房\s*收入|客房[，,]?\s*餐饮|餐饮[，,]?\s*客房",
    r"会议.{0,12}(收入|营收|万元)|宴会.{0,12}(收入|营收|万元)",
    r"(康体|康乐|泳池|健身|水疗).{0,15}(收入|营收|万元|占比)",
    r"总营业收入|营业总收入|营业收入合计",
    r"客源结构|会员|中介|协议客户|会议团队|散客",
    r"RevPAR|出租率|ADR|平均房价",
]

files = sorted(glob.glob(os.path.join(SRC, "*.txt")))
print(f"files: {len(files)}")

hits = {i: [] for i in range(len(PATS))}
for fp in files:
    try:
        t = open(fp, encoding="utf-8", errors="replace").read()
    except Exception:
        continue
    lines = t.split("\n")
    for i, p in enumerate(PATS):
        for ln, l in enumerate(lines):
            if re.search(p, l):
                hits[i].append((os.path.basename(fp)[:58], ln, l.strip()[:220]))

with open(OUT, "w", encoding="utf-8") as f:
    for i, p in enumerate(PATS):
        f.write(f"\n{'='*92}\n### PATTERN {i}: {p}\n{'='*92}\n")
        seen = set()
        n = 0
        for fn, ln, l in hits[i]:
            k = l[:70]
            if k in seen:
                continue
            seen.add(k)
            f.write(f"[{fn} L{ln}] {l}\n")
            n += 1
            if n >= 45:
                break
        print(f"pattern {i}: {len(hits[i])} raw / {n} kept")
print("written", os.path.getsize(OUT))
