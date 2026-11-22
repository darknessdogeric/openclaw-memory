# -*- coding: utf-8 -*-
"""恢复被列索引错误破坏的 5 行 + 补 表31 第一列；并 dump 表31 核对"""
import io, os, sys, re
T = r"D:\B166ER-openclaw\workspace\.tmp"
LOG = open(os.path.join(T, "fixrows2.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
def esc(s): return s.encode("unicode_escape").decode("ascii")
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
MD = os.path.join(KB, "总府皇冠改造_立项报告_集团汇报件_v1.0_2026-11-13.md")
t = open(MD, encoding="utf-8").read()
lines = t.split("\n")

# 先 dump 表31 结构（md 级：连续的表格行）
L("=== 表31 区域（md 中所有含 12.71% / 逐方向优劣 的表行）===")
for i, l in enumerate(lines):
    if l.startswith("|") and ("\u4f18\u52bf" in l or "\u52a3\u52bf" in l or "12.71" in l or "\u9010\u65b9\u5411\u4f18\u52a3" in l):
        L("  L%-5d %s" % (i, esc(l[:150])))

FIX = [
 ("\u6301\u7eed\u4e0b\u964d",
  "| \u5bbe\u5ba2\u652f\u4ed8\u80fd\u529b | \u9ad8 | \u4f4e | \u6301\u7eed\u4e0b\u964d |"),
 ("94.8%\uff08Pass\uff09",
  "| Engineering | \u672a\u5355\u5217 | 94.8%\uff08Pass\uff09 | 72.8%\uff08Fail\uff09 | \u65ad\u5761 |"),
 ("89.5%\uff08Pass\uff09",
  "| FSMS | \u672a\u5355\u5217 | 89.5%\uff08Pass\uff09 | 86.3% | \u7565\u964d |"),
 ("76.0% / 68 \u9879",
  "| Overall / \u4e0d\u5408\u89c4\u9879\u6570 | \u672a\u5355\u5217\uff08\u5206\u9879\u6700\u9ad8 95.92%\uff09 | 76.0% / 68 \u9879 | 71.7% / 80 \u9879 | \u4e0d\u5408\u89c4\u9879 +63% |"),
 ("\u65b9\u5411\u4e09\u591a\u51fa\u6362\u724c\u4e13\u9879",
  "| **\u5408\u8ba1** | **5,495** | **10,520** | \u65b9\u5411\u4e09\u591a\u51fa\u6362\u724c\u4e13\u9879 2,600 \u4e07\u5143\uff08VI \u5168\u5957 + \u7cfb\u7edf\u91cd\u5efa + \u4f1a\u5458\u8fc7\u6e21 + \u5ba2\u7528\u54c1\u5e03\u8349\uff09 |"),
 ("\u221212.71%",
  "| \u4e8c \u6cbf\u7528\u7687\u51a0 + 3 \u6539 2 | 10 \u5e74 IRR \u221212.71%\uff0c\u52a8\u6001\u56de\u6536 28.7 \u5e74 |"),
]
done = 0
for key, newrow in FIX:
    hit = None
    for i, l in enumerate(lines):
        if l.startswith("|") and key in l:
            hit = i; break
    if hit is None:
        L("[MISS]", esc(key)); continue
    lines[hit] = newrow
    done += 1
    L("[OK]", esc(key), "->", esc(newrow[:120]))
t = "\n".join(lines)
open(MD, "w", encoding="utf-8").write(t)
L("rewritten:", done, "/", len(FIX))

sys.path.insert(0, r"D:\B166ER-openclaw\workspace\.tmp")
from md2docx_cn import convert
out = os.path.join(REP, "总府皇冠改造_立项报告_集团汇报件_v1.0_2026-11-13.docx")
convert(MD, out)
L("DOCX %.1f KB" % (os.path.getsize(out)/1024))

from docx import Document
d = Document(out)
n = 0
for ti, tb in enumerate(d.tables, 1):
    for ri, row in enumerate(tb.rows):
        for ci, cell in enumerate(row.cells):
            if cell.text.strip() in ("", "\u2014", "-", "\uff0f", "/"):
                n += 1
                L("  REMAIN 表%d 行%d 列%d : %s" % (ti, ri, ci, esc(" || ".join(c.text.strip()[:22] for c in row.cells))))
L("剩余空白格:", n)
L("表格总数:", len(d.tables))
