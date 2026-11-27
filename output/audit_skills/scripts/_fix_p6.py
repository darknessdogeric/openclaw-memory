# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
P = r"D:\B166ER-openclaw\workspace\memory\小红书海报\_p6_content.py"
t = open(P, encoding="utf-8").read()
print("before len:", len(t))
for bad, good in ((chr(34)*3 + "," + chr(34) + ",", chr(34)*3 + ","),
                  (chr(34)*3 + "," + chr(39) + ",", chr(34)*3 + ","),
                  (chr(34)*3 + chr(34) + "," + chr(34) + chr(34) + ",", chr(34)*3 + ",")):
    n = t.count(bad)
    if n:
        print("fix", repr(bad), "x", n)
        t = t.replace(bad, good)
open(P, "w", encoding="utf-8").write(t)
print("after len:", len(t))
# 校验语法
import ast
try:
    ast.parse(t)
    print("SYNTAX OK")
except SyntaxError as e:
    print("SYNTAX FAIL line", e.lineno, ":", e.text)
