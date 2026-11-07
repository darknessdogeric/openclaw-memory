# -*- coding: utf-8 -*-
import ast, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
P = r"D:\B166ER-openclaw\workspace\memory\小红书海报\_p6_content.py"
t = open(P, encoding="utf-8-sig").read()
L = t.split(chr(10))
print("total lines:", len(L))
print("BOM in text:", t.count(chr(65279)))
for k in range(1, len(L) + 1):
    src = chr(10).join(L[:k])
    try:
        ast.parse(src)
    except SyntaxError as e:
        print("FIRST FAIL after line", k)
        print("  msg :", e.msg)
        for j in range(max(0, k - 4), min(len(L), k + 1)):
            print("  L%d: %s" % (j + 1, repr(L[j])[:180]))
        break
else:
    print("ALL PREFIXES OK")
