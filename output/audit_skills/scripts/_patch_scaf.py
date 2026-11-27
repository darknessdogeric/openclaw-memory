# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
P = r"D:\B166ER-openclaw\workspace\memory\小红书海报\_g16_bio.py"
t = open(P, encoding="utf-8").read()
Q = chr(34) * 3

t = t.replace(".gap{height:52px}", ".gap{height:64px}")

lines = [
 "SCAF = " + Q,
 "<div class=\"scaf\">",
 "  <div class=\"slab\">人类行为秩序</div>",
 "  <div class=\"sposts\">",
 "    <div class=\"spost\">稀 缺</div>",
 "    <div class=\"spost\">稀 缺</div>",
 "    <div class=\"spost\">稀 缺</div>",
 "  </div>",
 "  <div class=\"swarn\">彻底抽掉这根脚手架，系统<b>不一定会自动升维</b>，更可能先经历<b>失稳甚至坍塌</b>。</div>",
 "</div>",
 Q,
 "",
]
scaf = chr(10).join(lines)

if "SCAF = " in t:
    print("SCAF already present")
else:
    if "BODY = GRAPH + CASE" in t:
        t = t.replace("BODY = GRAPH + CASE", scaf + "BODY = GRAPH + SCAF")
        print("scaffold inserted")
    else:
        print("WARN: BODY anchor not found")

open(P, "w", encoding="utf-8").write(t)
print("bytes:", len(t))
