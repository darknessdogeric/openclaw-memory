# -*- coding: utf-8 -*-
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
ROOT = r"D:\B166ER-openclaw\workspace"
SC = os.path.join(ROOT,"toolbox","selfcheck.py")
t = open(SC, encoding="utf-8").read()
ids = re.findall(r"@check\(\s*\"(C\d+)\"", t)
print("现有断言 %d 条: %s" % (len(ids), ", ".join(ids)))
nums = [int(x[1:]) for x in ids]
print("最大编号: C%02d ｜ 空闲下一个: C%02d" % (max(nums), max(nums)+1))
print("有无纹样断言:", "有" if "纹样底库" in t else "★无")
print()
print("=== C23-C26 原文（并行会话加的，照其风格写我的）===")
for m in re.finditer(r"# ---------------- (C2[3-9].*?)def ", t, re.S):
    blk = m.group(1)
    print(blk[:520].rstrip())
    print("   ...")
    print()
