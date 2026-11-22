# -*- coding: utf-8 -*-
"""最后一处：R-17 行补齐列数 + 重出 Word + 清旧版"""
import io, os, sys, re, glob
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
LOG = open(os.path.join(T, "last.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()
def esc(s): return str(s).encode("unicode_escape").decode("ascii")

MD = os.path.join(KB, "总府皇冠改造_立项报告_集团汇报件_v2.0_2026-11-13.md")
t = open(MD, encoding="utf-8").read()
OLD = '| R-17 |**停业期声誉与评分继续下滑（全渠道六类口径）**| 停业前主动沟通与"改造故事"传播；分渠道对账与复业后两年营收折损监控 | 停业期净流出已计入现金流，方向一 1,389 万元、方向三 1,630 万元 |'
NEW = '| R-17 |**停业期声誉与评分继续下滑（全渠道六类口径）**| 中 | 停业前主动沟通与"改造故事"传播；分渠道对账与复业后两年营收折损监控 | 停业期净流出已计入现金流，方向一 1,389 万元、方向三 1,630 万元 |'
if OLD in t:
    t = t.replace(OLD, NEW); L("[FIX] R-17 行补齐第 3 列")
else:
    L("[MISS] R-17 行")
open(MD, "w", encoding="utf-8").write(t)

sys.path.insert(0, r"D:\B166ER-openclaw\workspace\.tmp")
from md2docx_cn import convert
out = os.path.join(REP, "总府皇冠改造_立项报告_集团汇报件_v2.0_2026-11-13.docx")
convert(MD, out)
L("DOCX %.1f KB" % (os.path.getsize(out)/1024))

from docx import Document
d = Document(out)
n = 0
for ti, tb in enumerate(d.tables, 1):
    for ri, row in enumerate(tb.rows):
        for ci, cell in enumerate(row.cells):
            if cell.text.strip() in ("", "—", "-", "／", "/"):
                n += 1
                L("  BLANK 表%d 行%d 列%d : %s" % (ti, ri, ci, " || ".join(esc(c.text.strip()[:28]) for c in row.cells)))
L("表格 %d，空白格 %d" % (len(d.tables), n))

# 清旧版与锁文件
for f in list(glob.glob(os.path.join(REP, "~$*"))) + \
         [os.path.join(REP, "总府皇冠改造_立项报告_集团汇报件_v1.0_2026-11-13.docx")]:
    if os.path.exists(f):
        try:
            os.remove(f); L("removed", os.path.basename(f).encode("unicode_escape").decode("ascii"))
        except Exception as e:
            L("SKIP(locked)", os.path.basename(f).encode("unicode_escape").decode("ascii"))
L("--- 上会件 ---")
for f in sorted(glob.glob(os.path.join(REP, "*.docx"))):
    if os.path.basename(f).startswith("~$"): continue
    L("  %-70s %7.1f KB" % (os.path.basename(f).encode("unicode_escape").decode("ascii"), os.path.getsize(f)/1024))
L("DONE")
