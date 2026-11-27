# -*- coding: utf-8 -*-
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
TB = os.path.join(ROOT,"toolbox")

print("="*100); print("### A. 正本 docx-md-bridge 全文（要往里合并 列表/目录域）"); print("="*100)
p = os.path.join(ROOT,"skills","docx-md-bridge","scripts","md_to_docx.py")
t = open(p, encoding="utf-8", errors="replace").read()
for i,l in enumerate(t.split("\n")):
    print("  L%-4d %s" % (i+1, l))

print()
print("="*100); print("### B. md_to_docx.py 的列表/目录实现（要移植的片段）"); print("="*100)
p2 = os.path.join(TB,"md_to_docx.py")
t2 = open(p2, encoding="utf-8", errors="replace").read()
for i,l in enumerate(t2.split("\n")):
    if re.search(r"(List|TOC|目录|bullet|numbered|def |add_|^\s*if|^\s*for)", l):
        print("  L%-4d %s" % (i+1, l[:150]))

print()
print("="*100); print("### C. v4_to_docx.py 的分页实现"); print("="*100)
p3 = os.path.join(TB,"v4_to_docx.py")
t3 = open(p3, encoding="utf-8", errors="replace").read()
for i,l in enumerate(t3.split("\n")):
    if re.search(r"(page_break|add_page_break|分页)", l):
        print("  L%-4d %s" % (i+1, l[:150]))
