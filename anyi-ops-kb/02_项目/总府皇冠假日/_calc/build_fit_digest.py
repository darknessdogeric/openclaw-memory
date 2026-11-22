# -*- coding: utf-8 -*-
"""汇总：换牌品牌建议 + 洲际换牌摸底纪要 + 三年遗留整改项清单 + 三年审计不合规报告结构"""
import io, os, sys, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

OUT = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc\brand_fit"
DIG = os.path.join(OUT, "_DIGEST.md")
files = sorted(glob.glob(os.path.join(OUT, "*.txt")))
parts = []
for f in files:
    t = open(f, encoding="utf-8").read()
    body = t.split("\n\n", 1)[1] if "\n\n" in t else t
    parts.append((os.path.basename(f), body))

def pick(key):
    for n, b in parts:
        if key in n:
            return b
    return None

with open(DIG, "w", encoding="utf-8") as o:
    o.write("# 品牌方原始依据 · 汇总\n\n")
    o.write("## 【1】换牌至洲际系其他品牌时，洲际方给出的品牌建议与初步标准\n\n")
    b = pick("品牌建议与初步标准")
    o.write(b + "\n\n" if b else "(无)\n")
    o.write("\n## 【2】F2-29 沟通纪要 —— 洲际体系内可换品牌摸底\n\n")
    b = pick("F2-29")
    o.write(b + "\n\n" if b else "(无)\n")
    for y in ("2024", "2025", "2026"):
        o.write(f"\n## 【3】{y} 遗留整改项清单（业主侧）\n\n")
        b = pick(f"{y} 遗留整改项清单")
        o.write(b + "\n\n" if b else "(无)\n")

print("digest written:", os.path.getsize(DIG), "bytes")

# 审计 PDF 结构：每页首两行 + 不合规项计数
import pymupdf
for y in ("2024", "2025", "2026"):
    hits = [p for p in glob.glob(os.path.join(OUT, f"*{y}*Non-Compliant*.txt")) + glob.glob(os.path.join(OUT, f"*{y}*Non Compliance*.txt"))]
    if not hits:
        hits = [p for p in glob.glob(os.path.join(OUT, f"*{y}*.txt")) if "Non" in os.path.basename(p)]
    if not hits:
        print(f"\n--- {y}: 未找到审计 PDF 文本 ---")
        continue
    t = open(hits[0], encoding="utf-8").read()
    pages = t.split("===== PAGE ")
    print(f"\n--- {y} 审计不合规报告：{len(pages)-1} 页，{len(t)} 字符 ---")
    # 统计各类标记
    for pat in ("N/A", "NTS", "Non", "Non-Compliance", "Checklist", "Score", "%"):
        print(f"    {pat:<16} {t.count(pat):>4}")
    for pg in pages[1:]:
        lines = [l.strip() for l in pg.split("\n") if l.strip()]
        head = " | ".join(lines[1:5])[:150] if len(lines) > 1 else ""
        print(f"    P{pg.split(' ')[0]}: {head}")
