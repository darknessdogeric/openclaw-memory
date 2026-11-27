# -*- coding: utf-8 -*-
import io, sys, os, glob, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
HOME = os.path.expanduser("~")
print("=== ① 内化笔记（方法论书籍内化目录）===")
KB4 = os.path.join(ROOT,"anyi-ops-kb","04_方法论","方法论书籍内化")
for f in sorted(glob.glob(os.path.join(KB4,"*.md"))):
    print("   %7d B  %s" % (os.path.getsize(f), os.path.basename(f)))
print()
print("=== ② 技能层 ===")
SK = os.path.join(ROOT,"skills","pattern-design-cn")
for base, dirs, fs in os.walk(SK):
    for f in fs:
        p = os.path.join(base,f)
        print("   %7d B  %s" % (os.path.getsize(p), os.path.relpath(p,SK).replace(os.sep,"/")))
print()
print("=== ③ 底库与存证 ===")
EV = os.path.join(ROOT,"output","book_纹样设计速查手册")
for f in sorted(os.listdir(EV)):
    p=os.path.join(EV,f)
    if os.path.isfile(p): print("   %8d B  %s" % (os.path.getsize(p), f))
print()
print("=== ④ 国堰落地清单 + 索引回写 ===")
DESK = os.path.join(HOME,"Desktop","产业发展部","旗下酒店","国堰宾馆")
for f in sorted(glob.glob(os.path.join(DESK,"文创改造","*纹样*"))):
    print("   %7d B  %s" % (os.path.getsize(f), os.path.relpath(f,DESK).replace(os.sep,"/")))
idx = os.path.join(DESK,"00_国堰宾馆文创改造_文件索引.md")
t = open(idx, encoding="utf-8").read()
print("   索引已含纹样行:", "纹样选型清单" in t)
print()
print("=== ⑤ 路由实测（纹样任务能否被召回）===")
r = subprocess.run([sys.executable, os.path.join(ROOT,"toolbox","skill_router.py"),
                    "--task","国堰客房布衣要配一款传统纹样，选哪个"], capture_output=True, timeout=150)
o = r.stdout.decode("utf-8","replace")
print("\n".join(o.split("\n")[:16]))
print()
print("=== ⑥ 规模 ===")
REG=json.load(open(os.path.join(ROOT,"output","audit_skills","SKILL_REGISTRY.json"),encoding="utf-8"))
W=json.load(open(os.path.join(ROOT,"output","audit_skills","WORKFLOWS.json"),encoding="utf-8"))
P=json.load(open(os.path.join(ROOT,"output","audit_skills","PARADIGM_REGISTRY.json"),encoding="utf-8"))
IDX=json.load(open(os.path.join(EV,"纹样索引.json"),encoding="utf-8"))
print("  技能 %d ｜ 范式 %d ｜ 工作流 %d ｜ 纹样底库 %d 条" % (
    len(REG), len(P), len(W), len(IDX.get("index_meihua",[]))+len(IDX.get("numbered_4722198",[]))))
