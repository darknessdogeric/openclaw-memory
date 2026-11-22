# -*- coding: utf-8 -*-
"""v61：核对 MD 40 张表与 Word 39 张表的差异——确认无内容丢失"""
import io, os, re, json, glob
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
REP = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店\改造报告交付"
LOG = open(os.path.join(T, "v61.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
MD4 = os.path.join(KB, "总府皇冠改造_可行性研究报告_v4.0_2026-11-14.md")
lines = open(MD4, encoding="utf-8").read().split("\n")
from docx import Document
d = Document(os.path.join(REP, "总府皇冠改造_可行性研究报告_v4.0_2026-11-14.docx"))
doc_text = "\n".join(p.text for p in d.paragraphs) + "\n" + "\n".join(
    c.text for tb in d.tables for r in tb.rows for c in r.cells)

blocks = []; i = 0
while i < len(lines):
    if lines[i].startswith("|"):
        j = i
        while j < len(lines) and lines[j].startswith("|"): j += 1
        blocks.append((i + 1, j, lines[i:j]))
        i = j
    else:
        i += 1
L("MD 表块 %d ｜ Word 表 %d" % (len(blocks), len(d.tables)))

# 逐块取特征值核验内容是否都在 Word 中
missing = []
for ln, lend, blk in blocks:
    body = [b for b in blk if not re.match(r"^\|[\s:\-|]+\|$", b.strip())]
    probes = []
    for b in body[1:]:
        cs = [c.strip() for c in b.strip().strip("|").split("|")]
        for c in cs:
            c2 = c.replace("**", "")
            if len(c2) >= 4 and not re.match(r"^[\d.,%—\-/ ]+$", c2):
                probes.append(c2); break
    lost = [p for p in probes if p not in doc_text]
    if lost:
        missing.append((ln, blk[0].strip().strip("|").split("|")[0].strip(), lost[:3]))
L("内容缺失的表块: %d" % len(missing))
for ln, first, lost in missing:
    L("   L%d 首格[%s] 缺失特征值: %s" % (ln, first[:26], lost))

# MD 中 4 个首格为「项目」的表 vs Word 3 个
proj_md = [b[0] for b in blocks if b[2][0].strip().strip("|").split("|")[0].strip() == "项目"]
proj_doc = sum(1 for tb in d.tables if tb.cell(0, 0).text.strip() == "项目")
L("")
L("首格为「项目」：MD %d 张（行 %s）｜Word %d 张" % (len(proj_md), proj_md, proj_doc))
for tb in d.tables:
    if tb.cell(0, 0).text.strip() == "项目":
        L("   Word 首格[项目] 第二格: %s ｜ 行数 %d" % (tb.cell(0, 1).text[:26], len(tb.rows)))

# 全文数字覆盖核验：MD 表格中所有数值是否都在 Word
mdnums = set()
for ln, lend, blk in blocks:
    for b in blk:
        for c in re.findall(r"\d[\d,]*\.?\d*", b):
            mdnums.add(c.replace(",", ""))
docnums = set(re.findall(r"\d[\d,]*\.?\d*", doc_text.replace(",", "")))
notfound = sorted([x for x in mdnums if x not in docnums and len(x) >= 2], key=lambda z: -len(z))
L("")
L("MD 表内数值未出现在 Word 的: %d 项" % len(notfound))
for x in notfound[:15]: L("   %s" % x)
L("DONE")
