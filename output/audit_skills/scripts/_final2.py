# -*- coding: utf-8 -*-
import io, sys, os, glob, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
KB4 = os.path.join(ROOT,"anyi-ops-kb","04_方法论")
AUD = os.path.join(ROOT,"output","audit_skills")
print("=== 交付物（方法论项目文件夹）===")
for f in sorted(glob.glob(os.path.join(KB4,"*技能库与范式库*"))):
    print("  %8d B  %s" % (os.path.getsize(f), os.path.basename(f)))
print("  --- 已归档 ---")
for f in sorted(glob.glob(os.path.join(KB4,"_归档_被取代版本","*技能库*"))):
    print("  %8d B  %s" % (os.path.getsize(f), os.path.basename(f)))
print()
print("=== 审计正本 output/audit_skills/ ===")
for f in sorted(glob.glob(os.path.join(AUD,"*.json"))):
    print("  %8d B  %s" % (os.path.getsize(f), os.path.basename(f)))
print("  scripts/ 归档脚本 %d 个" % len(glob.glob(os.path.join(AUD,"scripts","*.py"))))
print()
print("=== 归档区（全部可回滚）===")
for d in [os.path.join(ROOT,"toolbox","_archive","legacy_docx_variants_2026-11-18"),
          os.path.join(ROOT,"toolbox","_archive","hb_family_2026-11-18"),
          os.path.join(ROOT,"skills","_archive","idle_2026-11-18")]:
    if os.path.isdir(d):
        n=len(os.listdir(d)); sz=sum(os.path.getsize(os.path.join(d,x)) for x in os.listdir(d) if os.path.isfile(os.path.join(d,x)))
        print("  %-58s %3d 件 / %.0f KB" % (os.path.relpath(d,ROOT).replace(os.sep,"/"), n, sz/1024.0))
print()
print("=== 关键文件 ===")
for p in [os.path.join(ROOT,"toolbox","skill_router.py"), os.path.join(ROOT,"toolbox","selfcheck.py"),
          os.path.join(ROOT,"toolbox","md2docx.py"), os.path.join(ROOT,"AGENTS.md"),
          os.path.join(ROOT,"MEMORY.md"), os.path.join(ROOT,"memory","2026-11-18.md"),
          os.path.join(ROOT,"skills","tool-index-builder","SKILL.md"),
          os.path.join(ROOT,"skills","skill-registry-builder","SKILL.md")]:
    print("  %8d B  %s" % (os.path.getsize(p), os.path.relpath(p,ROOT).replace(os.sep,"/")))
print()
print("=== 规模对比 ===")
tbpy = [p for p in glob.glob(os.path.join(ROOT,"toolbox","*.py")) if not os.path.basename(p).startswith("_")]
REG=json.load(open(os.path.join(AUD,"SKILL_REGISTRY.json"),encoding="utf-8"))
T=json.load(open(os.path.join(AUD,"TOOL_INDEX.json"),encoding="utf-8"))
W=json.load(open(os.path.join(AUD,"WORKFLOWS.json"),encoding="utf-8"))
P=json.load(open(os.path.join(AUD,"PARADIGM_REGISTRY.json"),encoding="utf-8"))
print("  技能 %d ｜ 范式 %d ｜ 工作流 %d ｜ 工具 %d ｜ toolbox 非临时脚本 %d ｜ 断言 22" % (len(REG),len(P),len(W),len(T),len(tbpy)))
