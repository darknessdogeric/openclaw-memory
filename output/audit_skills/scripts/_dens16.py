# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
P = r"D:\B166ER-openclaw\workspace\memory\小红书海报\_g16_bio.py"
t = open(P, encoding="utf-8").read()

REPL = [
 (".gap{height:64px}", ".gap{height:88px}"),
 (".node{position:relative;background:#ffffff;border:1.5px solid rgba(28,25,23,.16);border-radius:8px;padding:13px 14px;text-align:center}",
  ".node{position:relative;background:#ffffff;border:1.5px solid rgba(28,25,23,.16);border-radius:8px;padding:18px 15px;text-align:center}"),
 (".nmech{border-color:rgba(160,95,38,.42);background:#fdfaf4;padding:14px 10px}",
  ".nmech{border-color:rgba(160,95,38,.42);background:#fdfaf4;padding:20px 11px}"),
 (".nout{text-align:left;padding:14px 15px}", ".nout{text-align:left;padding:19px 16px}"),
 (".case{margin-top:8px;background:#ffffff;border:1.5px solid rgba(160,95,38,.45);border-radius:8px;padding:18px 20px}",
  ".case{margin-top:10px;background:#ffffff;border:1.5px solid rgba(160,95,38,.45);border-radius:8px;padding:23px 22px}"),
 (".u25 .utext{flex:1;font-size:16.5px;color:#57534e;line-height:1.58}",
  ".u25 .utext{flex:1;font-size:17.5px;color:#57534e;line-height:1.6}"),
 (".scaf{background:#ffffff;border:1px solid rgba(28,25,23,.13);border-radius:7px;padding:18px 22px}",
  ".scaf{background:#ffffff;border:1px solid rgba(28,25,23,.13);border-radius:7px;padding:23px 24px}"),
 (".spost{flex:1;background:linear-gradient(180deg,#a05f26,#7f4619);border-radius:0 0 5px 5px;height:50px;",
  ".spost{flex:1;background:linear-gradient(180deg,#a05f26,#7f4619);border-radius:0 0 5px 5px;height:58px;"),
 (".nrow{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}",
  ".nrow{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}"),
]

hit = 0
for a, b in REPL:
    if a in t:
        t = t.replace(a, b)
        hit += 1
    else:
        print("MISS:", a[:52])
open(P, "w", encoding="utf-8").write(t)
print("replaced:", hit, "/", len(REPL))
