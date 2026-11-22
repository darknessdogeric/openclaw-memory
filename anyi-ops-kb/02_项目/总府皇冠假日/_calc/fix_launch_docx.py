# -*- coding: utf-8 -*-
import io, os, sys, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
REP = os.path.join(TGT, "改造报告交付")
sys.path.insert(0, r"D:\B166ER-openclaw\workspace\.tmp")
from md2docx_cn import convert

# 清掉误生成的 README docx
stray = os.path.join(REP, "00_项目总览_README.docx")
if os.path.exists(stray):
    os.remove(stray); print("removed stray:", os.path.basename(stray))

# 精确定位立项报告 md
cands = [f for f in glob.glob(os.path.join(KB, "*.md")) if "立项报告" in os.path.basename(f)]
assert len(cands) == 1, cands
md = cands[0]
out = os.path.join(REP, os.path.splitext(os.path.basename(md))[0] + ".docx")
convert(md, out)
print("DOCX:", os.path.basename(out), "%.1f KB" % (os.path.getsize(out)/1024))
print("MD src:", os.path.basename(md), "%.1f KB" % (os.path.getsize(md)/1024))

print("\n=== 改造报告交付 目录（全部）===")
for f in sorted(glob.glob(os.path.join(REP, "*"))):
    print("  %-74s %7.1f KB" % (os.path.basename(f), os.path.getsize(f)/1024))
print("\n=== 测算与中间产物 ===")
for f in sorted(glob.glob(os.path.join(TGT, "测算与中间产物", "*"))):
    print("  %-74s %7.1f KB" % (os.path.basename(f), os.path.getsize(f)/1024))
