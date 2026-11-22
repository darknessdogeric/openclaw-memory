# -*- coding: utf-8 -*-
"""① 读集团汇报模板 PDF 结构 ② 参考产发部既往工作汇报 docx ③ 扫成品空白格"""
import io, os, sys, glob, re
T = r"D:\B166ER-openclaw\workspace\.tmp"
LOG = open(os.path.join(T, "tpl.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
def esc(s): return s.encode("unicode_escape").decode("ascii")

ROOTS = [r"C:\Users\ericz\Desktop\产业发展部", r"D:\B166ER-openclaw"]
def find_by(kw, exts):
    out = []
    for root in ROOTS:
        if not os.path.isdir(root): continue
        for dp, ds, fs in os.walk(root):
            if any(x in dp for x in ("node_modules", ".git", "第一批次文件", "第二批次文件")):
                ds[:] = []
                continue
            for f in fs:
                if f.endswith(exts) and kw in f:
                    out.append(os.path.join(dp, f))
    return out

L("=== 1. 集团汇报模板 PDF ===")
for p in find_by("汇报材料", (".pdf",)):
    L("  FOUND:", esc(p), "%.1f KB" % (os.path.getsize(p)/1024))
    import pymupdf
    d = pymupdf.open(p)
    L("  页数:", d.page_count)
    for i in range(min(d.page_count, 3)):
        txt = d[i].get_text()
        L("  ---- PAGE %d ----" % (i+1))
        for ln in txt.split("\n"):
            if ln.strip():
                L("    " + esc(ln.strip()[:100]))

L("\n=== 2. 产发部既往工作汇报 docx（体例参考）===")
for p in find_by("川宾口径", (".docx",))[:1]:
    L("  FOUND:", esc(p))
    from docx import Document
    doc = Document(p)
    L("  段落数:", len(doc.paragraphs), " 表格数:", len(doc.tables))
    n = 0
    for par in doc.paragraphs:
        if par.text.strip():
            L("  [%s] %s" % (par.style.name, esc(par.text.strip()[:90])))
            n += 1
            if n > 28: break
    for ti, tb in enumerate(doc.tables[:2], 1):
        L("  --- 表%d (%d行x%d列) ---" % (ti, len(tb.rows), len(tb.columns)))
        for r in tb.rows[:5]:
            L("     " + " | ".join(esc(c.text.strip()[:26]) for c in r.cells))

L("\n=== 3. 成品 docx 表格空白格扫描 ===")
DOC = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店\改造报告交付\总府皇冠改造_立项报告_集团汇报件_v1.0_2026-11-13.docx"
from docx import Document
d2 = Document(DOC)
tot = 0
for ti, tb in enumerate(d2.tables, 1):
    blanks = []
    for ri, row in enumerate(tb.rows):
        for ci, cell in enumerate(row.cells):
            tx = cell.text.strip()
            if tx in ("", "—", "-", "／", "/"):
                blanks.append((ri, ci))
    if blanks:
        tot += len(blanks)
        head = " | ".join(c.text.strip()[:14] for c in tb.rows[0].cells)[:96]
        L("  表%-3d 空白%2d  首行: %s" % (ti, len(blanks), esc(head)))
L("  表格 %d 个，空白格 %d" % (len(d2.tables), tot))
