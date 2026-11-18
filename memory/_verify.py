# -*- coding: utf-8 -*-
import io, sys, os, glob, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
KB4 = os.path.join(ROOT,"anyi-ops-kb","04_方法论")
AUD = os.path.join(ROOT,"output","audit_skills")
print("=== 交付物（方法论项目文件夹，非桌面）===")
for f in sorted(glob.glob(os.path.join(KB4,"*技能库与范式库*"))):
    print("  %8d B  %s" % (os.path.getsize(f), os.path.relpath(f, ROOT).replace(os.sep,"/")))
print()
print("=== 审计正本 output/audit_skills/ ===")
for f in sorted(os.listdir(AUD)):
    p = os.path.join(AUD,f)
    if os.path.isfile(p): print("  %8d B  %s" % (os.path.getsize(p), f))
print("  scripts/ 归档临时脚本 %d 个" % len(glob.glob(os.path.join(AUD,"scripts","*.py"))))
print()
print("=== 关键文件 ===")
for p in [os.path.join(ROOT,"toolbox","skill_router.py"), os.path.join(ROOT,"toolbox","selfcheck.py"),
          os.path.join(ROOT,"toolbox","md2docx.py"), os.path.join(ROOT,"AGENTS.md"),
          os.path.join(ROOT,"memory","2026-11-18.md")]:
    print("  %8d B  %s" % (os.path.getsize(p), os.path.relpath(p,ROOT).replace(os.sep,"/")))
print()
print("=== 归档区（可回滚）===")
for d in [os.path.join(ROOT,"toolbox","_archive","legacy_docx_variants_2026-11-18"),
          os.path.join(ROOT,"skills","_archive","idle_2026-11-18")]:
    if os.path.isdir(d):
        print("  %s  (%d 件)" % (os.path.relpath(d,ROOT).replace(os.sep,"/"), len(os.listdir(d))))
print()
print("=== 路由实测 ===")
import subprocess
r = subprocess.run([sys.executable, os.path.join(ROOT,"toolbox","skill_router.py"), "--task", "把一份 md 转成带表格的 docx"],
                   capture_output=True, timeout=120)
print(r.stdout.decode("utf-8","replace")[:900])
