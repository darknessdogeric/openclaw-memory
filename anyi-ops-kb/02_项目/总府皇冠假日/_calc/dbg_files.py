# -*- coding: utf-8 -*-
import io, os, sys, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
print("KB exists:", os.path.isdir(KB))
print("--- 所有 .md ---")
for f in sorted(glob.glob(os.path.join(KB, "*.md"))):
    print("  %8d  %s" % (os.path.getsize(f), os.path.basename(f)))
print("--- 递归找 含'立项' 或 2026-11-08 的文件 ---")
for root, dirs, fs in os.walk(KB):
    for f in fs:
        if "立项" in f or "2026-11-08" in f:
            print("  ", os.path.join(root, f).replace(KB, ""))
