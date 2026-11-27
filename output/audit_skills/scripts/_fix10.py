# -*- coding: utf-8 -*-
import io, sys, os, re, ast, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
SC  = os.path.join(ROOT,"toolbox","selfcheck.py")
t = open(SC, encoding="utf-8", errors="replace").read()

old = '''        for f in glob.glob(os.path.join(base,"**","SKILL.md"), recursive=True):
            d = os.path.dirname(f)
            anc = os.path.relpath(d, base).split(os.sep)[:-1]
            if any(os.path.exists(os.path.join(base, *anc[:i+1], "SKILL.md")) for i in range(len(anc))):
                continue'''
new = '''        for f in glob.glob(os.path.join(base,"**","SKILL.md"), recursive=True):
            d = os.path.dirname(f)
            rel = os.path.relpath(d, base).split(os.sep)
            # ★ 与注册表生成器同一定义：_ 开头目录是归档区，不算在库技能
            if any(x.startswith("_") for x in rel):
                continue
            anc = rel[:-1]
            if any(os.path.exists(os.path.join(base, *anc[:i+1], "SKILL.md")) for i in range(len(anc))):
                continue'''
assert old in t, "C14 原文未命中"
t = t.replace(old, new, 1)
ast.parse(t)
open(SC,"w",encoding="utf-8",newline="\n").write(t)
print("✔ C14 已与注册表生成器统一口径（排除 _ 归档区 + 祖先判据）")

# C13/C17/C19 也顺带核：注册表条数与磁盘一致由 C14 保证
r = subprocess.run([sys.executable, SC], capture_output=True, timeout=400)
print(r.stdout.decode("utf-8","replace"))
print("退出码:", r.returncode)
