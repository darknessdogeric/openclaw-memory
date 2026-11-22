# -*- coding: utf-8 -*-
"""Extract param schema from hotel_irr_calc.py + dump the 9-sheet Excel template."""
import io, sys, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

F = r"D:\B166ER-openclaw\workspace\toolbox\hotel_irr_calc.py"
src = open(F, encoding="utf-8").read()
lines = src.split("\n")

print("=== 1. calc_hotel_project 参数取值清单 ===")
body = "\n".join(lines[108:272])
req = sorted(set(re.findall(r"p\['([a-z_0-9]+)'\]", body)))
opt = sorted(set(re.findall(r"p\.get\('([a-z_0-9]+)'", body)))
print("\n必填 p['...']:")
for k in req:
    ln = next((i for i, l in enumerate(lines, 1) if f"p['{k}']" in l), None)
    ctx = ""
    for i, l in enumerate(lines, 1):
        if f"'{k}':" in l and i < 120:
            ctx = l.strip()[:110]
            break
    print(f"  {k:28s} {ctx}")
print("\n可选 p.get('...', 默认):")
for k in opt:
    for i, l in enumerate(lines, 1):
        if f"p.get('{k}'" in l:
            print(f"  {k:28s} {l.strip()[:110]}")
            break

print("\n=== 2. BENCHMARK 参数库(引擎内置) ===")
m = re.search(r"BENCHMARK\s*=\s*\{", src)
if m:
    d = 0; j = m.end() - 1
    for k in range(j, len(src)):
        if src[k] == "{": d += 1
        elif src[k] == "}":
            d -= 1
            if d == 0: break
    for ln in src[j:k + 1].split("\n"):
        if ln.strip():
            print("  " + ln.rstrip()[:190])

print("\n=== 3. RAMP_CURVES ===")
m = re.search(r"RAMP_CURVES\s*=\s*\{", src)
if m:
    d = 0; j = m.end() - 1
    for k in range(j, len(src)):
        if src[k] == "{": d += 1
        elif src[k] == "}":
            d -= 1
            if d == 0: break
    print(src[j:k + 1][:1400])

print("\n=== 4. DEPRECIATION ===")
m = re.search(r"DEPRECIATION\s*=\s*\[", src)
if m:
    j = m.end() - 1
    d = 0
    for k in range(j, len(src)):
        if src[k] == "[": d += 1
        elif src[k] == "]":
            d -= 1
            if d == 0: break
    print(src[j:k + 1][:1500])

print("\n=== 5. 九表 Excel 模版结构 ===")
XL = r"C:\Users\ericz\Desktop\产业发展部\改造测算\酒店投资测算通用模版_v1.0.xlsx"
if os.path.exists(XL):
    try:
        import openpyxl
        wb = openpyxl.load_workbook(XL, data_only=False)
        print("sheets:", wb.sheetnames)
        for ws in wb.worksheets:
            print(f"\n--- [{ws.title}] dims={ws.dimensions} max_row={ws.max_row} max_col={ws.max_column} ---")
            for r in range(1, min(ws.max_row, 14) + 1):
                vals = []
                for c in range(1, min(ws.max_column, 9) + 1):
                    v = ws.cell(r, c).value
                    if v is not None:
                        vals.append(f"{openpyxl.utils.get_column_letter(c)}{r}={str(v)[:46]}")
                if vals:
                    print("   " + " | ".join(vals))
    except Exception as e:
        print("ERR", e)
else:
    print("NOT FOUND:", XL)
