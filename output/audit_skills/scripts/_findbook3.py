# -*- coding: utf-8 -*-
import io, sys, os, re, glob, datetime, zipfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
HOME = os.path.expanduser("~")
def rel(p):
    try: return os.path.relpath(p, HOME).replace(os.sep,"/")
    except Exception: return p.replace(os.sep,"/")
def recent(p):
    try:
        return datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d %H:%M")
    except Exception: return "?"
print("="*100); print("### A. 接收目录明细（最近 7 天优先）"); print("="*100)
DIRS = [os.path.join(HOME,"Downloads"), os.path.join(HOME,"Documents","WXWork"),
        os.path.join(HOME,"Documents","WeChat Files"), os.path.join(HOME,"Desktop"),
        os.path.join(HOME,"OneDrive"), os.path.join(HOME,"Documents")]
cut = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
for d in DIRS:
    if not os.path.isdir(d): continue
    print()
    print("  ── %s ──" % rel(d))
    items=[]
    for base, dirs, fs in os.walk(d):
        dirs[:] = [x for x in dirs if x not in ("node_modules",".git","__pycache__")]
        for f in fs:
            p=os.path.join(base,f)
            try: items.append((os.path.getmtime(p), os.path.getsize(p), p))
            except Exception: pass
    items.sort(reverse=True)
    for mt, sz, p in items[:18]:
        print("     %s %9d B  %s" % (recent(p), sz, rel(p)[:88]))
print()
print("="*100); print("### B. WPS 企业云盘（书可能在这里）"); print("="*100)
WPS = os.path.join(HOME,"WPS Cloud")
if os.path.isdir(WPS):
    n=0
    for base, dirs, fs in os.walk(WPS):
        dirs[:] = [x for x in dirs if x not in ("node_modules",".git")]
        for f in fs:
            n+=1
            if n<=40: print("     %9d B  %s" % (os.path.getsize(os.path.join(base,f)), rel(os.path.join(base,f))[:96]))
    print("  合计 %d 个文件" % n)
else:
    print("  WPS Cloud 目录不存在")
print()
print("="*100); print("### C. 近 14 天内新增/修改的文档（desktop+downloads+docs+kb）"); print("="*100)
KW = ["纹样","速查"]
found=[]
for d in [os.path.join(HOME,"Desktop"), os.path.join(HOME,"Downloads"), os.path.join(HOME,"Documents"),
          r"D:\anyi-ops-kb", os.path.join(HOME,"WPS Cloud")]:
    if not os.path.isdir(d): continue
    for base, dirs, fs in os.walk(d):
        dirs[:] = [x for x in dirs if x not in ("node_modules",".git","__pycache__")]
        for f in fs:
            p=os.path.join(base,f)
            try:
                if os.path.getmtime(p) < (datetime.datetime.now()-datetime.timedelta(days=14)).timestamp(): continue
            except Exception: continue
            found.append((os.path.getmtime(p), os.path.getsize(p), p))
found.sort(reverse=True)
print("  近 14 天动的文件 %d 个，前 30:" % len(found))
for mt,sz,p in found[:30]:
    print("     %s %9d B  %s" % (recent(p), sz, rel(p)[:90]))
