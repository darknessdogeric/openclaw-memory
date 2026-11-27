# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
P = r"D:\B166ER-openclaw\workspace\memory\小红书海报\_g16_bio.py"
t = open(P, encoding="utf-8").read()
if "BODY = GRAPH + SCAF" in t:
    t = t.replace("BODY = GRAPH + SCAF", "BODY = GRAPH + CASE + SCAF")
    print("fixed: CASE restored into BODY")
else:
    print("WARN anchor missing")
open(P, "w", encoding="utf-8").write(t)
