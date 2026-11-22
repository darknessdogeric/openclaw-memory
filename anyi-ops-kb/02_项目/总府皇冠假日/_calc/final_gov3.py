# -*- coding: utf-8 -*-
import io, os, sys, re, glob
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
LOG = open(r"D:\B166ER-openclaw\workspace\.tmp\final_gov.log", "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()

MD = os.path.join(KB, "总府皇冠改造_整体方案报告_集团汇报件_v1.0_2026-11-13.md")
t = open(MD, encoding="utf-8").read()
L("MD bytes:", len(t.encode("utf-8")))
L("--- 标题结构 ---")
for l in t.split("\n"):
    if re.match(r"^#{1,3} ", l):
        L("  " + l.encode("unicode_escape").decode("ascii")[:120])

# memory 追加层级修正说明
MEM = r"D:\B166ER-openclaw\workspace\memory\2026-11-13.md"
open(MEM, "a", encoding="utf-8").write(
"\n> 注：集团汇报件生成后又修一处层级标注缺陷——「二、改造必要性」原被合并为单一小节组、标题误取第一小节名，现改为 6 个独立小节；最终结构 H2=8 / H3=28 / H4=27，emoji 0，标题完整性自检 0 异常，DOCX 63.3 KB。\n")

L("\n--- 交付清单 ---")
for f in sorted(glob.glob(os.path.join(REP, "*.docx"))):
    L("  %-74s %7.1f KB" % (os.path.basename(f).encode("unicode_escape").decode("ascii"), os.path.getsize(f)/1024))
for f in sorted(glob.glob(os.path.join(TGT, "测算与中间产物", "*.xlsx"))):
    L("  [测算] %-68s %7.1f KB" % (os.path.basename(f).encode("unicode_escape").decode("ascii"), os.path.getsize(f)/1024))
