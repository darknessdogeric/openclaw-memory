# -*- coding: utf-8 -*-
import io, os, sys, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"

def esc(s): return s.encode("unicode_escape").decode("ascii")

print("=== KB 根目录 .md（按 mtime 倒序前 6，文件名转 ASCII 安全）===")
for f in sorted(glob.glob(os.path.join(KB, "*.md")), key=os.path.getmtime, reverse=True)[:6]:
    print("  %8d  %s" % (os.path.getsize(f), esc(os.path.basename(f))))

print("\n=== 找 55000-70000 字节且含'第一部分'的 md ===")
for f in glob.glob(os.path.join(KB, "*.md")):
    sz = os.path.getsize(f)
    if 50000 < sz < 75000:
        head = open(f, encoding="utf-8").read(3000)
        print("  CAND %8d %s  含'第一部分'=%s 含'立项报告'=%s" % (
            sz, esc(os.path.basename(f)), ("第一部分" in head), ("立项报告" in head)))

print("\n=== 改造报告交付 docx（ASCII 安全）===")
for f in sorted(glob.glob(os.path.join(TGT, "改造报告交付", "*.docx"))):
    print("  %8d  %s" % (os.path.getsize(f), esc(os.path.basename(f))))
