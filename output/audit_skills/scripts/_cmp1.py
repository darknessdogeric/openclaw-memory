# -*- coding: utf-8 -*-
import io, sys, os, re, glob, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"

print("="*94); print("### A. 既有轮子 docx-md-bridge/scripts/md_to_docx.py —— 有没有同一个表格 bug？"); print("="*94)
p = os.path.join(ROOT, "skills", "docx-md-bridge", "scripts", "md_to_docx.py")
t = open(p, encoding="utf-8", errors="replace").read()
print("  文件 %d B ｜ 行 %d" % (len(t), t.count("\n")+1))
# 找表格分隔行判定
for i, l in enumerate(t.split("\n")):
    if re.search(r"(\|---|is_sep|separator|split\(\"\|\")", l):
        print("   L%-4d %s" % (i+1, l.strip()[:120]))
print()
print("  ★ 关键函数片段:")
m = re.search(r"def\s+(\w*table\w*|\w*sep\w*|\w*parse\w*)\s*\([^)]*\)\s*:", t)
if m:
    st = t.rindex("\n", 0, m.start())+1
    print("\n".join("      "+x for x in t[st:st+1400].split("\n")[:30]))
else:
    for mm in re.finditer(r"^\s*def\s+(\w+)\(", t, re.M):
        print("      def", mm.group(1))
print()
print("="*94); print("### B. 我今天造的 toolbox/md2docx.py —— 修了什么"); print("="*94)
q = os.path.join(ROOT, "toolbox", "md2docx.py")
if os.path.exists(q):
    t2 = open(q, encoding="utf-8", errors="replace").read()
    print("  %d B" % len(t2))
    m2 = re.search(r"def\s+is_sep.*?:", t2, re.S)
    if m2: print("   " + m2.group(0)[:300].replace("\n","\n   "))
