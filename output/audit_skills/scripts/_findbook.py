# -*- coding: utf-8 -*-
import io, sys, os, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
DESK = os.path.join(HOME,"Desktop")
KB4 = os.path.join(ROOT,"anyi-ops-kb","04_方法论")
SI = os.path.join(HOME,"self-improving")

def rel(p):
    try: return os.path.relpath(p, HOME).replace(os.sep,"/")
    except Exception: return p.replace(os.sep,"/")

print("="*100); print("### A. 全盘找《纹样设计速查手册》"); print("="*100)
KW = ["纹样","速查手册"]
roots = [DESK, os.path.join(ROOT,"anyi-ops-kb"), os.path.join(ROOT,"output"),
         os.path.join(ROOT,"memory"), os.path.join(HOME,"Downloads"), os.path.join(HOME,"Documents"),
         os.path.join(HOME,"OneDrive")] 
hits=[]
for r in roots:
    if not os.path.isdir(r): continue
    for base, dirs, fs in os.walk(r):
        dirs[:] = [d for d in dirs if d not in ("node_modules",".git","__pycache__",".chroma_db","venv",".venv")]
        for f in fs:
            if any(k in f for k in KW):
                p=os.path.join(base,f)
                try: hits.append((os.path.getsize(p), rel(p)))
                except Exception: pass
hits.sort(reverse=True)
print("  文件名命中 %d 件:" % len(hits))
for sz,p in hits[:40]: print("     %9d B  %s" % (sz,p))
if not hits: print("     （无文件名命中）")

print()
print("="*100); print("### B. 文本内提及『纹样』"); print("="*100)
cnt=0
for r in [os.path.join(ROOT,"memory"), os.path.join(ROOT,"anyi-ops-kb"), SI]:
    for base, dirs, fs in os.walk(r):
        dirs[:] = [d for d in dirs if d not in ("node_modules",".git","__pycache__",".chroma_db")]
        for f in fs:
            if not f.endswith((".md",".txt")): continue
            p=os.path.join(base,f)
            try:
                if os.path.getsize(p)>2_000_000: continue
                t=open(p,encoding="utf-8",errors="replace").read()
            except Exception: continue
            for m in re.finditer(r".{0,50}纹样.{0,70}", t):
                print("   %s" % m.group(0).replace("\n"," ")[:140].strip()); cnt+=1
                if cnt>=20: break
            if cnt>=20: break
        if cnt>=20: break
    if cnt>=20: break
print("  提及 %d 处" % cnt)

print()
print("="*100); print("### C. 既有『方法论书籍内化』清单"); print("="*100)
MD = os.path.join(KB4,"方法论书籍内化")
for f in sorted(glob.glob(os.path.join(MD,"*.md"))):
    print("   %7d B  %s" % (os.path.getsize(f), os.path.basename(f)))
sample = os.path.join(MD,"《版式之道》核心内化笔记_v1.0_2026-10-11.md")
if os.path.exists(sample):
    print()
    print("  ---- 格式样本：《版式之道》前 55 行 ----")
    print("\n".join(open(sample,encoding="utf-8",errors="replace").read().split("\n")[:55]))
