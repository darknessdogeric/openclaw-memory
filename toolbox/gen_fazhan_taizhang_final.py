# -*- coding: utf-8 -*-
"""产发部专版台账：严格按 Eric 11:48 确认的 7 行（当前实际跟进工作内容）"""
import os
from copy import copy
import openpyxl

SRC = r"C:\Users\ericz\Desktop\2026.10.25 近期重点工作任务台账（资管+投资+产发）(3)(2).xlsx"
OUT = r"C:\Users\ericz\Desktop\产业发展部\2026.10.25 近期重点工作任务台账（产发部专版）.xlsx"

# Eric 2026-10-31 11:48 确认产发部当前负责的 7 项工作
KEEP = [
    "安逸礼物(暂定名)合作项目工作",
    "对接集团科创部各项事务",
    "对接集团产发部各项事务",
    "国堰宾馆主题文化酒店改造项目",
    "旅游列车项目",
    "总府皇冠改造方案",
    "其他跟进项目",
]

wb = openpyxl.load_workbook(SRC)
ws = wb.active
HDR, TPL = 3, 4
styles = [copy(ws.cell(TPL, c)._style) for c in range(1, 6)]
row_h = ws.row_dimensions[TPL].height

kept = []
for r in range(HDR + 1, ws.max_row + 1):
    nm = ws.cell(r, 2).value
    if nm is None:
        continue
    if str(nm).strip() in KEEP:
        kept.append((r, [ws.cell(r, c).value for c in range(1, 6)]))

assert len(kept) == 7, "matched %d rows, expected 7" % len(kept)
print("matched:", [(v[0], v[1]) for _, v in kept])

if ws.max_row >= TPL:
    ws.delete_rows(TPL, ws.max_row - TPL + 1)

ws.cell(1, 1).value = "近期重点工作进展 投资+资管+产发（产业发展部专版）"

for i, (src_row, vals) in enumerate(kept):
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
print("SAVED:", OUT, "ROWS:", len(kept), "SIZE:", os.path.getsize(OUT))
