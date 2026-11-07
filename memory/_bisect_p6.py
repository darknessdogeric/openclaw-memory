# -*- coding: utf-8 -*-
import ast, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
P = r"D:\B166ER-openclaw\workspace\memory\小红书海报\_p6_content.py"
L = open(P, encoding="utf-8").read().split(chr(10))
print("total lines:", len(L))
for k in range(1, len(L) + 1):
    src = chr(10).join(L[:k])
    try:
        ast.parse(src)
    except SyntaxError as e:
        print("FIRST FAIL after adding line", k)
        print("  msg  :", e.msg)
        print("  line :", repr(L[k-1])[:200])
        print("  prev :", repr(L[k-2])[:200] if k >= 2 else "")
        break
else:
    print("ALL PREFIXES OK - full file parses")
