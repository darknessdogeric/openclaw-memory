# -*- coding: utf-8 -*-
"""定位成品 docx 的 14 个空白格：表号 + 行列 + 整行内容"""
import io, os, sys
T = r"D:\B166ER-openclaw\workspace\.tmp"
LOG = open(os.path.join(T, "blanks.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
def esc(s): return s.encode("unicode_escape").decode("ascii")
from docx import Document
DOC = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店\改造报告交付\总府皇冠改造_立项报告_集团汇报件_v1.0_2026-11-13.docx"
d = Document(DOC)
n = 0
for ti, tb in enumerate(d.tables, 1):
    for ri, row in enumerate(tb.rows):
        cells = [c.text.strip() for c in row.cells]
        for ci, tx in enumerate(cells):
            if tx in ("", "—", "-", "／", "/"):
                n += 1
                L("表%-3d 行%-3d 列%-2d  空格" % (ti, ri, ci))
                L("        整行: " + " || ".join(esc(c[:34]) for c in cells))
L("\n空白格合计:", n)
