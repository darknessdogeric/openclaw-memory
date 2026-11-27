# -*- coding: utf-8 -*-
import io, sys, os, re, glob, shutil, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
SK = os.path.join(ROOT,"skills","pattern-design-cn")

# 1) 底库入技能（自包含）
d = os.path.join(SK,"data"); os.makedirs(d, exist_ok=True)
for f in ["纹样索引.json","纹样构词法分析.json"]:
    src = os.path.join(ROOT,"output","book_纹样设计速查手册",f)
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(d,f))
print("1) 底库入技能:", sorted(os.listdir(d)))

# 2) 读国堰最新品牌定位（今天 11:34 改过）
DESK = os.path.join(HOME,"Desktop","产业发展部","旗下酒店","国堰宾馆")
print()
print("2) 国堰最新文件（按 mtime）：")
cands=[]
for base, dirs, fs in os.walk(DESK):
    for f in fs:
        if f.endswith(".md"):
            p=os.path.join(base,f)
            try: cands.append((os.path.getmtime(p), p))
            except Exception: pass
cands.sort(reverse=True)
import datetime
for mt,p in cands[:8]:
    print("   %s %7d B  %s" % (datetime.datetime.fromtimestamp(mt).strftime("%m-%d %H:%M"), os.path.getsize(p),
                               os.path.relpath(p,DESK).replace(os.sep,"/")[:76]))
print()
KEY = ["定位","品牌","主张","客群","主题","叙事","视觉","调性","定位语","slogan","年轻","Z世代","中产","度假","文创","IP"]
for mt,p in cands[:4]:
    t=open(p,encoding="utf-8",errors="replace").read()
    print("   ── %s ──" % os.path.basename(p))
    for l in t.split("\n"):
        s=l.strip()
        if not s or s.startswith("|") or s.startswith("#"): continue
        if any(k in s for k in ["定位","主张","客群","叙事","调性","年轻","Z世代","文化定位","品牌定位","主题","调性","人群"]):
            print("      · %s" % s[:150])
    print()
