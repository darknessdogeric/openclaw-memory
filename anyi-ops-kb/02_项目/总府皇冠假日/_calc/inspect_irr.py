# -*- coding: utf-8 -*-
"""Inspect hotel_irr_calc.py interface + locate the Excel template."""
import io, sys, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

F = r"D:\B166ER-openclaw\workspace\toolbox\hotel_irr_calc.py"
src = open(F, encoding="utf-8").read()
lines = src.split("\n")
print(f"=== {os.path.basename(F)}  {len(lines)} lines / {len(src)} chars ===\n")

print("--- top-level defs / constants ---")
for i, l in enumerate(lines, 1):
    if re.match(r"^(def |class |PRESETS|RAMP|COST|DEPRE|CURVE|TIER|HOTEL|TAX|INS)", l) or \
       re.match(r"^[A-Z][A-Z_0-9]{2,}\s*=", l):
        print(f"L{i}: {l[:160]}")

print("\n--- PRESETS keys ---")
m = re.search(r"PRESETS\s*=\s*\{", src)
if m:
    d = 0; j = m.end() - 1; k = j
    for k in range(j, len(src)):
        if src[k] == "{": d += 1
        elif src[k] == "}":
            d -= 1
            if d == 0: break
    body = src[j:k + 1]
    for mm in re.finditer(r"[\"'](\w+)[\"']\s*:\s*\{", body):
        print("  -", mm.group(1))

print("\n--- labor_in_gop / rent_annual / npv / 敏感性 ---")
for i, l in enumerate(lines, 1):
    if any(k in l for k in ("labor_in_gop", "rent_annual", "sensitiv", "npv", "NPV")):
        print(f"L{i}: {l.strip()[:150]}")

print("\n--- CLI (argparse / argv / main) ---")
for i, l in enumerate(lines, 1):
    if any(k in l for k in ("argparse", "add_argument", "sys.argv", "def main", "__main__")):
        print(f"L{i}: {l.strip()[:150]}")

print("\n--- 残值 / 生命周期 ---")
for i, l in enumerate(lines, 1):
    if any(k in l for k in ("residual", "残值", "horizon", "n_years", "life", "Y10")):
        print(f"L{i}: {l.strip()[:130]}")

print("\n=== Excel 模版定位 ===")
for d in [r"C:\Users\ericz\Desktop\产业发展部\改造测算",
          r"C:\Users\ericz\Desktop\产业发展部",
          r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府四川宾馆",
          r"D:\B166ER-openclaw\workspace\toolbox"]:
    if os.path.isdir(d):
        xs = [f for f in os.listdir(d) if f.lower().endswith((".xlsx", ".xls"))]
        print(f"[{d}]")
        for f in sorted(xs)[:12]:
            print("   ", f)
    else:
        print(f"[{d}] NOT FOUND")
