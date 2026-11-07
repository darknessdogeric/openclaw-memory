# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
LIB = r"D:\B166ER-openclaw\workspace\memory\小红书海报\_p6_lib.py"
t = open(LIB, encoding="utf-8-sig").read()
if "def page(" in t:
    print("page() already present")
else:
    add = open(r"D:\B166ER-openclaw\workspace\memory\_p6_pagefn.txt", encoding="utf-8").read()
    t = t.rstrip() + chr(10) + chr(10) + add.rstrip() + chr(10)
    open(LIB, "w", encoding="utf-8", newline=chr(10)).write(t)
    print("page() appended")
print("lib bytes:", len(t))
