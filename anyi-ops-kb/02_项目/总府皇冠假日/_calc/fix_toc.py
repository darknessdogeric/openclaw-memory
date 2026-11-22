# -*- coding: utf-8 -*-
"""修复：目录重建误删第一章标题 + 全量终检"""
import io, os, sys, re, glob
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
LOG = open(os.path.join(T, "fix_toc.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
def esc(s): return str(s).encode("unicode_escape").decode("ascii")

MD = os.path.join(KB, "总府皇冠改造_立项报告_集团汇报件_v3.0_2026-11-14.md")
t = open(MD, encoding="utf-8").read()

# ① 恢复被删的第一章标题
if "## 一、立项依据与项目概述" not in t:
    anchor = "### （一）项目基本情况"
    assert anchor in t, "锚点缺失"
    t = t.replace(anchor, "## 一、立项依据与项目概述\n\n" + anchor, 1)
    L("[FIX] 恢复第一章标题")

# ② 重建目录（安全版：只替换目录条目区，不动正文）
m = re.search(r"^## 目录\n", t, re.M)
assert m
head = t[:m.end()]
body = t[m.end():]
lines = body.split("\n")
# 找正文起点：第一个 "## " 且不是目录条目行
start = None
for i, l in enumerate(lines):
    if l.startswith("## "):
        start = i
        break
assert start is not None, "未找到正文起点"
# 目录条目区 = lines[0:start]，去掉尾部空行
toc_area = [l for l in lines[:start] if l.strip()]
rest = "\n".join(lines[start:])
h2s = [l[3:].strip() for l in rest.split("\n") if l.startswith("## ")]
toc = "\n".join("%d. %s" % (i + 1, h) for i, h in enumerate(h2s))
t = head + toc + "\n\n" + rest
L("目录重建: %d 条" % len(h2s))

# ③ 目录与正文标题一致性校验
toc_items = re.findall(r"^\d+\. (.+)$", toc, re.M)
body_items = [l[3:].strip() for l in rest.split("\n") if l.startswith("## ")]
ok = (toc_items == body_items)
L("目录与正文一致:", ok, "| 目录", len(toc_items), "正文", len(body_items))
if not ok:
    for a, b in zip(toc_items, body_items):
        if a != b: L("  差异:", esc(a), "!=", esc(b))
    L("  目录:", [esc(x) for x in toc_items])
    L("  正文:", [esc(x) for x in body_items])

open(MD, "w", encoding="utf-8").write(t)
L("MD bytes:", len(t.encode("utf-8")))

# ④ 出 Word
sys.path.insert(0, r"D:\B166ER-openclaw\workspace\.tmp")
from md2docx_cn import convert
out = os.path.join(REP, "总府皇冠改造_立项报告_集团汇报件_v3.0_2026-11-14.docx")
convert(MD, out)
L("DOCX %.1f KB" % (os.path.getsize(out)/1024))

# ⑤ 全量终检
from docx import Document
d = Document(out)
blank = 0
for ti, tb in enumerate(d.tables, 1):
    for ri, row in enumerate(tb.rows):
        for ci, cell in enumerate(row.cells):
            if cell.text.strip() in ("", "\u2014", "-", "\uff0f", "/"):
                blank += 1
                L("  BLANK 表%d 行%d 列%d" % (ti, ri, ci))
L("docx: 段落 %d / 表格 %d / 空白格 %d" % (len(d.paragraphs), len(d.tables), blank))
h_doc = [p.text.strip() for p in d.paragraphs if p.style.name.startswith("Heading") and p.text.strip()]
L("docx 标题数: %d" % len(h_doc))
for h in h_doc[:20]:
    L("   " + esc(h[:70]))
EMO = "[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U00002B50\uFE0F\u200D\u2764\u2B06\u2B07\u2B05\u274C\u2705\u26A0\u26A1\u2139\u24C2\u2B55]"
L("emoji:", len(re.findall(EMO, t)), "| ?? 占位:", len(re.findall(r"\?\?", t)), "| __ 标记:", len(re.findall(r"_{3,}", t)))
bad = [l for l in t.split("\n") if l.startswith("#") and ("|" in l or "**" in l or len(l) > 95)]
L("标题异常:", len(bad))
for b in bad[:5]: L("   !", esc(b[:100]))
L("DONE")
