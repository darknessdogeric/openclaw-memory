# -*- coding: utf-8 -*-
import sys, os
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
BASE = r"D:\B166ER-openclaw\workspace\memory\小红书海报"
REN = os.path.join(BASE, "_p6_render.py")
r = open(REN, encoding="utf-8-sig").read()
old = """      if (el.clientHeight > 46 && el.scrollHeight > el.clientHeight + 2)
        issues.push("纵向溢出: " + (el.className || el.tagName) + " :: " + tx(el).slice(0,22));"""
new = """      if (el.clientHeight > 24 && el.scrollHeight > el.clientHeight + 2) {
        const cs = getComputedStyle(el);
        const fs = parseFloat(cs.fontSize) || 16;
        const lh = parseFloat(cs.lineHeight) || 0;
        if (lh > fs * 1.3) issues.push("纵向溢出: " + (el.className || el.tagName) + " :: " + tx(el).slice(0,22));
      }"""
if old in r:
    r = r.replace(old, new)
    print("checker: line-height aware")
else:
    print("checker: pattern MISS")
open(REN, "w", encoding="utf-8", newline=chr(10)).write(r)
