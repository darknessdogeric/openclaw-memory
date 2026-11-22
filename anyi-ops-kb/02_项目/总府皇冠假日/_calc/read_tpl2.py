# -*- coding: utf-8 -*-
"""① 读模板 PDF 附件5《关于旗下酒店改造工作思路（讨论稿）》体例 ② 空白格上下文"""
import io, os, sys, re, glob
T = r"D:\B166ER-openclaw\workspace\.tmp"
LOG = open(os.path.join(T, "tpl2.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
def esc(s): return s.encode("unicode_escape").decode("ascii")

PDF = r"C:\Users\ericz\Desktop\产业发展部\安逸酒店集团改革发展工作专题汇报材料（715定稿）.pdf"
import pymupdf
d = pymupdf.open(PDF)
L("总页数:", d.page_count)
# 找附件5 起始页
start = None
for i in range(d.page_count):
    t = d[i].get_text()
    if "关于安逸酒店集团旗下酒店改造工作思路" in t and start is None:
        start = i
        L("附件5 出现在 PDF 第 %d 页(索引)" % (i + 1))
        for ln in t.split("\n"):
            if ln.strip():
                L("   >", esc(ln.strip()[:95]))
        break
L("\n=== 附件5 正文体例（起始后 6 页）===")
if start is not None:
    for i in range(start, min(start + 6, d.page_count)):
        L("---- PDF PAGE %d ----" % (i + 1))
        for ln in d[i].get_text().split("\n"):
            if ln.strip():
                L("   " + esc(ln.strip()[:100]))

L("\n=== 正文前 6 页体例（附件1 前）===")
for i in range(3, 9):
    L("---- PDF PAGE %d ----" % (i + 1))
    for ln in d[i].get_text().split("\n"):
        if ln.strip():
            L("   " + esc(ln.strip()[:100]))

L("\n=== 空白格上下文（成品 docx）===")
DOC = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店\改造报告交付\总府皇冠改造_立项报告_集团汇报件_v1.0_2026-11-13.docx"
from docx import Document
doc = Document(DOC)
for ti, tb in enumerate(doc.tables, 1):
    blanks = []
    for ri, row in enumerate(tb.rows):
        for ci, cell in enumerate(row.cells):
            if cell.text.strip() in ("", "—", "-", "／", "/"):
                blanks.append((ri, ci))
    if not blanks:
        continue
    L("### 表%d (%d行x%d列)" % (ti, len(tb.rows), len(tb.columns)))
    for ri in range(len(tb.rows)):
        cells = [c.text.strip() for c in tb.rows[ri].cells]
        if any((ri, ci) in blanks for ci in range(len(cells))):
            L("  行%d: %s" % (ri, " || ".join(esc(c[:30]) for c in cells)))
