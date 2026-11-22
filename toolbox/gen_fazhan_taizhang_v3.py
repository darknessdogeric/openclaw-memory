# -*- coding: utf-8 -*-
"""按黄色填充(rgb=FFFFFF00)筛选产发部行，逐字保留原文本与样式"""
import os
from copy import copy
import openpyxl

SRC = r"C:\Users\ericz\Desktop\2026.10.25 近期重点工作任务台账（资管+投资+产发）(3)(2).xlsx"
OUT = r"C:\Users\ericz\Desktop\产业发展部\2026.10.25 近期重点工作任务台账（产发部专版）.xlsx"

YELLOW = "FFFFFF00"

wb = openpyxl.load_workbook(SRC)
ws = wb.active

def is_yellow(cell):
    f = cell.fill
    if f is None or f.patternType != "solid":
        return False
    fg = f.fgColor
    if fg is None or fg.type != "rgb" or fg.rgb is None:
        return False
    return str(fg.rgb).upper() == YELLOW

HDR = 3
TPL = 4
styles = [copy(ws.cell(TPL, c)._style) for c in range(1, 6)]
row_h = ws.row_dimensions[TPL].height

kept, dropped = [], []
for r in range(HDR + 1, ws.max_row + 1):
    if ws.cell(r, 2).value is None:
        continue
    cols = [c for c in range(1, 6) if is_yellow(ws.cell(r, c))]
    if cols:
        kept.append((r, [ws.cell(r, c).value for c in range(1, 6)], cols))
    else:
        dropped.append((r, ws.cell(r, 1).value, str(ws.cell(r, 2).value)))

print("YELLOW rows (%d):" % len(kept))
for r, vals, cols in kept:
    print("   R%-3d no=%-4s %-30s yellow_cols=%s" % (r, vals[0], str(vals[1])[:30], cols))
print("DROPPED rows (%d):" % len(dropped))
for r, no, nm in dropped:
    print("   R%-3d no=%-4s %s" % (r, no, nm[:36]))

# 清除全部数据行
if ws.max_row >= TPL:
    ws.delete_rows(TPL, ws.max_row - TPL + 1)

ws.cell(1, 1).value = "近期重点工作进展 投资+资管+产发（产业发展部专版）"

for i, (src_row, vals, cols) in enumerate(kept):
    r = TPL + i
    for c in range(1, 6):
        cell = ws.cell(row=r, column=c)
        cell.value = vals[c - 1]
        cell._style = copy(styles[c - 1])
        al = copy(cell.alignment)
        al.wrap_text = True
        al.vertical = 'top'
        cell.alignment = al
    if row_h:
        ws.row_dimensions[r].height = row_h

ws.freeze_panes = "C4"

os.makedirs(os.path.dirname(OUT), exist_ok=True)
wb.save(OUT)
print("SAVED:", OUT)
print("ROWS:", len(kept), "SIZE:", os.path.getsize(OUT))
