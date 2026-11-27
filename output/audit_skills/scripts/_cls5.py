# -*- coding: utf-8 -*-
import io, sys, os, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
TB = os.path.join(ROOT,"toolbox")

print("="*100); print("### A. 『目录域』到底是不是真 TOC 字段"); print("="*100)
for p in [os.path.join(TB,"md_to_docx.py"), os.path.join(TB,"md_to_docx_v1.0.py"), os.path.join(TB,"v4_to_docx.py")]:
    t = open(p, encoding="utf-8", errors="replace").read()
    hits = [(i+1,l) for i,l in enumerate(t.split("\n")) if re.search(r"(目录|TOC|fldChar|instrText)", l)]
    print("  %-22s 命中 %d" % (os.path.basename(p), len(hits)))
    for i,l in hits[:6]: print("        L%-4d %s" % (i,l.strip()[:120]))

print()
print("="*100); print("### B. 真正引用 toolbox 克隆（排除 canonical 路径与自审脚本）"); print("="*100)
SCAN_DIRS = [os.path.join(ROOT,"toolbox"), os.path.join(ROOT,"skills"), os.path.join(ROOT,"memory")]
files = []
for d in SCAN_DIRS:
    for base, dirs, fs in os.walk(d):
        dirs[:] = [x for x in dirs if x not in ("__pycache__",".chroma_db",".git","node_modules","archive")]
        for f in fs:
            if f.endswith((".md",".py",".json",".js")): files.append(os.path.join(base,f))
for f in [os.path.join(ROOT,"AGENTS.md"), os.path.join(ROOT,"MEMORY.md")]:
    if os.path.exists(f): files.append(f)
clones = ["md_to_docx.py","md_to_docx_clean.py","md_to_docx_v1.0.py","md_to_docx_v2.py","md_to_docx_v3.py","v4_to_docx.py","md2gongwen_docx.py"]
for c in clones:
    hits = []
    for f in files:
        if os.path.basename(f) == c: continue
        try: t = open(f, encoding="utf-8", errors="replace").read()
        except Exception: continue
        for m in re.finditer(re.escape(c), t):
            ctx = t[max(0,m.start()-70):m.start()+len(c)+10].replace("\n"," ")
            # 只关心指向 toolbox 的引用
            if "toolbox" in ctx or "toolbox" in t[max(0,m.start()-160):m.start()]:
                hits.append((os.path.relpath(f, ROOT).replace(os.sep,"/"), ctx[-90:]))
                break
    print("  %-22s 指向 toolbox 的引用 %d" % (c, len(hits)))
    for h,cx in hits[:5]: print("        %-46s …%s" % (h[:46], cx.strip()[:70]))

print()
print("="*100); print("### C. KB_04_方法论 现有内容（范式库正本位置）"); print("="*100)
kb4 = os.path.join(ROOT,"anyi-ops-kb","04_方法论")
print("  存在:", os.path.isdir(kb4))
if os.path.isdir(kb4):
    for f in sorted(glob.glob(os.path.join(kb4,"**","*"))):
        if os.path.isfile(f):
            print("     %8d B  %s" % (os.path.getsize(f), os.path.relpath(f,kb4).replace(os.sep,"/")))

print()
print("="*100); print("### D. AGENTS.md 收尾关卡原文（要在此挂路由）"); print("="*100)
ag = open(os.path.join(ROOT,"AGENTS.md"), encoding="utf-8", errors="replace").read()
lines = ag.split("\n")
st = next((i for i,l in enumerate(lines) if "收尾关卡" in l), None)
if st is not None:
    for i in range(st, min(st+26, len(lines))):
        print("  L%-4d %s" % (i+1, lines[i][:126]))
