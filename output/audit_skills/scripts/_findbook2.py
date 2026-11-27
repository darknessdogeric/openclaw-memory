# -*- coding: utf-8 -*-
import io, sys, os, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HOME = os.path.expanduser("~")
ROOT = r"D:\B166ER-openclaw\workspace"
def rel(p):
    try: return os.path.relpath(p, HOME).replace(os.sep,"/")
    except Exception: return p.replace(os.sep,"/")
KW = ["纹样","速查","pattern"]
SKIP = {"node_modules",".git","__pycache__",".chroma_db","venv",".venv","site-packages",
        "Windows","$Recycle.Bin","System Volume Information","Program Files","Program Files (x86)",
        "Microsoft","WindowsApps","Packages","Temp","tmp"}
print("="*100); print("### 全盘深搜（C:\\Users\\ericz 全域 + D:\\ 深 5 层）"); print("="*100)
hits=[]; scanned=0
# C 用户域
for base, dirs, fs in os.walk(HOME):
    dirs[:] = [d for d in dirs if d not in SKIP]
    for f in fs:
        scanned+=1
        if any(k in f for k in KW):
            p=os.path.join(base,f)
            try: hits.append((os.path.getsize(p), rel(p)))
            except Exception: pass
# D 盘深 5 层
for base, dirs, fs in os.walk("D:\\", topdown=True):
    depth = base.count("\\")
    dirs[:] = [d for d in dirs if d not in SKIP]
    if depth > 5: dirs[:] = []
    for f in fs:
        scanned+=1
        if any(k in f for k in KW):
            p=os.path.join(base,f)
            try: hits.append((os.path.getsize(p), rel(p)))
            except Exception: pass
print("  扫描文件数: %d ｜ 命中 %d 件" % (scanned, len(hits)))
hits.sort(reverse=True)
for sz,p in hits[:40]: print("     %9d B  %s" % (sz,p))
if not hits: print("     ★ 全盘无文件名命中")
print()
print("=== 常见电子书/接收目录是否存在 ===")
for d in ["Downloads","Documents","Desktop","OneDrive","Pictures","Videos","Music",
          os.path.join("Documents","WeChat Files"), os.path.join("Documents","Tencent Files"),
          os.path.join("Documents","WXWork"), "Books", "Kindle", "Zlibrary", "Z-Library"]:
    p = os.path.join(HOME, d)
    if os.path.isdir(p):
        n = len([x for x in os.listdir(p)])
        print("   ✔ %-42s %d 项" % (d, n))
    else:
        print("   · %-42s 不存在" % d)
