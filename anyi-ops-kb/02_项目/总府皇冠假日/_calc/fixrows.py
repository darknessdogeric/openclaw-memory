# -*- coding: utf-8 -*-
"""修复被破坏的表格行：整行重写（原始行取自 blanks.log）"""
import io, os, sys, re
T = r"D:\B166ER-openclaw\workspace\.tmp"
LOG = open(os.path.join(T, "fixrows.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
def esc(s): return s.encode("unicode_escape").decode("ascii")
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
MD = os.path.join(KB, "总府皇冠改造_立项报告_集团汇报件_v1.0_2026-11-13.md")
t = open(MD, encoding="utf-8").read()
lines = t.split("\n")

# (唯一定位串, 完整新行)
ROWFIX = [
 ("\u5bbe\u5ba2\u652f\u4ed8\u80fd\u529b",
  "| \u5bbe\u5ba2\u652f\u4ed8\u80fd\u529b | \u9ad8 | \u4f4e | \u6301\u7eed\u4e0b\u964d |"),
 ("\u6210\u90fd\u5168\u5e02\u9ad8\u7aef\u9152\u5e97",
  "| \u6210\u90fd\u5168\u5e02\u9ad8\u7aef\u9152\u5e97 | 2024 \u5e74 RevPAR 834 \u5143 | \u603b\u5e9c\u73b0\u72b6 RevPAR 257.6 \u5143\uff0c\u4ec5\u4e3a 31% |"),
 ("\u603b\u5e9c\uff08\u73b0\u72b6\uff09",
  "| \u603b\u5e9c\uff08\u73b0\u72b6\uff09 | \u603b\u5e9c\u8857 31 \u53f7 | 1996 \u5e74\u5efa\u6210\uff082014 \u5e74\u91cd\u88c5\uff09 | 415\uff08\u6b63\u5e38\u552e\u5356 351\uff09 | 25.35 \u33a1 | 30 \u5e74\u6d89\u5916\u57fa\u56e0 |"),
 ("Engineering",
  "| Engineering | \u672a\u5355\u5217 | 94.8%\uff08Pass\uff09 | 72.8%\uff08Fail\uff09 | \u65ad\u5761 |"),
 ("FSMS",
  "| FSMS | \u672a\u5355\u5217 | 89.5%\uff08Pass\uff09 | 86.3% | \u7565\u964d |"),
 ("Overall / \u4e0d\u5408\u89c4\u9879\u6570",
  "| Overall / \u4e0d\u5408\u89c4\u9879\u6570 | \u672a\u5355\u5217\uff08\u5206\u9879\u6700\u9ad8 95.92%\uff09 | 76.0% / 68 \u9879 | 71.7% / 80 \u9879 | \u4e0d\u5408\u89c4\u9879 +63% |"),
 ("\u827a\u672f\u54c1\u4e0e\u5728\u5730\u7b56\u5c55",
  "| \u827a\u672f\u54c1\u4e0e\u5728\u5730\u7b56\u5c55 | 0 | 380 | \u6cbf\u7528\u7687\u51a0 3.0 \u65e0\u5f3a\u5236\uff1b\u6362\u54c1\u724c\u540e\u6309\u5728\u5730\u6587\u5316\u201c\u4e00\u5e97\u4e00\u7b56\u201d\u6295\u5165 |"),
 ("\u5f00\u4e1a\u524d\u8d39\u7528 / \u80fd\u6e90\u8282\u80fd",
  "| \u5f00\u4e1a\u524d\u8d39\u7528 / \u80fd\u6e90\u8282\u80fd / \u666f\u89c2 / \u50a8\u6cb9 | 455 | 970 | \u542b pre-opening \u8d39\uff08\u65b9\u5411\u4e09\uff09\u3001\u8282\u80fd\u6539\u9020\u3001\u666f\u89c2\u5ead\u9662\u3001\u50a8\u6cb9\u4e0e\u53d1\u7535\u5408\u89c4 |"),
 ("| **\u5408\u8ba1**|",
  "| **\u5408\u8ba1** | **5,495** | **10,520** | \u65b9\u5411\u4e09\u591a\u51fa\u6362\u724c\u4e13\u9879 2,600 \u4e07\u5143\uff08VI \u5168\u5957 + \u7cfb\u7edf\u91cd\u5efa + \u4f1a\u5458\u8fc7\u6e21 + \u5ba2\u7528\u54c1\u5e03\u8349\uff09 |"),
 ("\u221210.27%",
  "| \u4e8c \u6cbf\u7528\u7687\u51a0 + 3 \u6539 2 | \u4e00\u6b21\u5168\u505c\u4e1a | 880 | \u221210.27% | \u672a\u56de\u6536 | 28.7 \u5e74 | \u4e0d\u8fbe\u6807 |"),
 ("1.19%",
  "| \u56db \u6362\u54c1\u724c + 3 \u6539 2 | \u4e00\u6b21\u5168\u505c\u4e1a | 1,150 | 1.19% | 9.5 \u5e74 | 13.3 \u5e74 | \u4e0d\u8fbe\u6807 |"),
 ("R-24",
  "| R-24 | \u505c\u4e1a\u671f\u8d44\u4ea7\u95f2\u7f6e\u6210\u672c\uff08\u6298\u65e7 2,195 \u4e07\u5143/\u5e74\u7167\u63d0\uff09 | \u9ad8 | \u4e2d | \u4f4e\uff08\u5df2\u5728\u73b0\u91d1\u6d41\u4e2d\uff09 | \u65e0\u9700\u989d\u5916\u5e94\u5bf9\uff1b\u4f46\u987b\u7eb3\u5165\u201c\u8425\u4e1a\u73b0\u91d1\u6bdb\u6d41\u91cf\u201d\u53e3\u5f84\u6f84\u6e05 | \u8d22\u52a1 | \u6301\u7eed |"),
]
done = 0
for key, newrow in ROWFIX:
    hit = None
    for i, l in enumerate(lines):
        if l.startswith("|") and key in l:
            hit = i; break
    if hit is None:
        L("[MISS]", esc(key)); continue
    lines[hit] = newrow
    done += 1
    L("[OK]", esc(key))
t = "\n".join(lines)
open(MD, "w", encoding="utf-8").write(t)
L("rows rewritten:", done, "/", len(ROWFIX))

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
                L("  REMAIN 表%d 行%d 列%d : %s" % (ti, ri, ci, esc(" || ".join(c.text.strip()[:20] for c in row.cells))))
L("剩余空白格:", n)
