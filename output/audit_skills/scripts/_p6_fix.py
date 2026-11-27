# -*- coding: utf-8 -*-
import sys, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BASE = r"D:\B166ER-openclaw\workspace\memory\小红书海报"

LIB = os.path.join(BASE, "_p6_lib.py")
t = open(LIB, encoding="utf-8-sig").read()

REPL = [
    (".body{flex:1 1 auto;display:flex;flex-direction:column;justify-content:space-evenly;gap:14px;min-height:0;padding:20px 0}",
     ".body{flex:1 1 auto;display:flex;flex-direction:column;justify-content:space-evenly;gap:16px;min-height:0;padding:26px 0}"),
    (".card{background:rgba(255,255,255,.045);border:1px solid rgba(233,228,218,.13);border-radius:8px;padding:19px 20px}",
     ".card{background:rgba(255,255,255,.045);border:1px solid rgba(233,228,218,.13);border-radius:8px;padding:26px 24px}"),
    (".g3c{background:rgba(255,255,255,.045);border:1px solid rgba(233,228,218,.13);border-radius:8px;padding:17px 15px}",
     ".g3c{background:rgba(255,255,255,.045);border:1px solid rgba(233,228,218,.13);border-radius:8px;padding:25px 18px}"),
    (".tl{display:flex;flex-direction:column;gap:11px}", ".tl{display:flex;flex-direction:column;gap:17px}"),
    (".tlrow .tx .p{font-size:16px;color:#a8a094;line-height:1.55}", ".tlrow .tx .p{font-size:16.5px;color:#a8a094;line-height:1.65}"),
    (".tlrow .tx .q{font-size:16.5px;color:#d8a06a;line-height:1.5;margin-top:5px;font-weight:600}",
     ".tlrow .tx .q{font-size:17px;color:#d8a06a;line-height:1.55;margin-top:7px;font-weight:600}"),
    (".gate .gp{font-size:16px;color:#a8a094;line-height:1.55}", ".gate .gp{font-size:16.5px;color:#a8a094;line-height:1.7}"),
    (".gate .gh{font-size:20px;font-weight:800;color:#e9e4da;margin-bottom:5px}", ".gate .gh{font-size:21px;font-weight:800;color:#e9e4da;margin-bottom:8px}"),
    (".figw{border:1px solid rgba(233,228,218,.12);border-radius:9px;padding:14px;background:rgba(255,255,255,.03)}",
     ".figw{border:1px solid rgba(233,228,218,.12);border-radius:9px;padding:18px;background:rgba(255,255,255,.03)}"),
    (".cmp .cc{font-size:17px;color:#e9e4da;line-height:1.5;background:rgba(255,255,255,.045);border:1px solid rgba(233,228,218,.12);border-radius:6px;padding:12px 14px}",
     ".cmp .cc{font-size:17.5px;color:#e9e4da;line-height:1.55;background:rgba(255,255,255,.045);border:1px solid rgba(233,228,218,.12);border-radius:6px;padding:17px 18px}"),
    (".cmp{display:grid;grid-template-columns:118px 1fr 1fr;gap:11px 14px;align-items:start}",
     ".cmp{display:grid;grid-template-columns:118px 1fr 1fr;gap:16px 16px;align-items:start}"),
    (".plaque{display:flex;flex-direction:column;gap:13px}", ".plaque{display:flex;flex-direction:column;gap:19px}"),
    (".plq .pt{font-size:18px;color:#c3bcb0;line-height:1.5;padding-top:4px}", ".plq .pt{font-size:19px;color:#c3bcb0;line-height:1.55;padding-top:4px}"),
    (".foot .q{font-size:24px;font-weight:800;line-height:1.5}", ".foot .q{font-size:26px;font-weight:800;line-height:1.5}"),
    (".foot .s{font-size:15px;color:#8e867a;margin-top:10px;line-height:1.6}", ".foot .s{font-size:15.5px;color:#8e867a;margin-top:12px;line-height:1.65}"),
    ("h1{font-size:60px;", "h1{font-size:63px;"),
    ("h2{font-size:44px;", "h2{font-size:46px;"),
    (".sub{font-size:21px;color:#a8a094;line-height:1.55;margin-top:14px}", ".sub{font-size:22px;color:#a8a094;line-height:1.55;margin-top:16px}"),
    (".card .d{font-size:18px;color:#c3bcb0;line-height:1.62}", ".card .d{font-size:18.5px;color:#c3bcb0;line-height:1.68}"),
]
hit = 0
for a, b in REPL:
    if a in t:
        t = t.replace(a, b)
        hit += 1
    else:
        print("  MISS:", a[:56])
open(LIB, "w", encoding="utf-8", newline=chr(10)).write(t)
print("lib css replaced:", hit, "/", len(REPL))

REN = os.path.join(BASE, "_p6_render.py")
r = open(REN, encoding="utf-8-sig").read()
r = r.replace("if (el.clientHeight > 30 && el.scrollHeight > el.clientHeight + 2)",
              "if (el.clientHeight > 46 && el.scrollHeight > el.clientHeight + 2)")
open(REN, "w", encoding="utf-8", newline=chr(10)).write(r)
print("checker threshold patched")
