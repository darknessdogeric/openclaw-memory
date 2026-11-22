# -*- coding: utf-8 -*-
"""三年品牌方审计：Executive Summary + 逐项不合规观察（适配性评估的硬证据）"""
import io, os, sys, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

OUT = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc\brand_fit"
DST = os.path.join(OUT, "_AUDIT.md")

def find(y):
    for p in glob.glob(os.path.join(OUT, f"*{y}*.txt")):
        if "Non" in os.path.basename(p) and "Compliant" in os.path.basename(p):
            return p
    for p in glob.glob(os.path.join(OUT, f"*{y}*.txt")):
        if "Non" in os.path.basename(p):
            return p
    return None

with open(DST, "w", encoding="utf-8") as o:
    for y in ("2024", "2025", "2026"):
        p = find(y)
        o.write(f"\n\n{'='*90}\n## {y} 年 IHG 品牌标准审计 · Standards Evaluation Non-Compliant Report\n{'='*90}\n\n")
        if not p:
            o.write("(未找到)\n"); continue
        t = open(p, encoding="utf-8").read()
        body = t.split("\n\n", 1)[1] if "\n\n" in t else t
        pages = body.split("===== PAGE ")
        # P1 + P2 = 封面 + Executive Summary
        for pg in pages[1:3]:
            o.write(f"\n----- PAGE {pg.split(' ')[0]} -----\n")
            o.write(pg.split("\n", 1)[1][:3500])
        # 其余页：抓 Question / Observation 的实质内容行
        o.write(f"\n\n### 逐项不合规明细（{y}）\n")
        for pg in pages[3:]:
            lines = [l.strip() for l in pg.split("\n")]
            num = pg.split(" ")[0]
            body_lines = [l for l in lines[1:] if l and not set(l) <= set("| ") and l != "Question" and l != "Observation"]
            if not body_lines:
                continue
            o.write(f"\n- **P{num}** " + " ｜ ".join(body_lines[:14])[:1400])

print("audit digest:", os.path.getsize(DST), "bytes")
