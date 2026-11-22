# -*- coding: utf-8 -*-
"""从 (3)(2) 原台账筛出产发部行，逐字保留原文本与样式，生成产发部专版"""
import os
from copy import copy
import openpyxl

SRC = r"C:\Users\ericz\Desktop\2026.10.25 近期重点工作任务台账（资管+投资+产发）(3)(2).xlsx"
OUT = r"C:\Users\ericz\Desktop\产业发展部\2026.10.25 近期重点工作任务台账（产发部专版）.xlsx"

# 产发部相关行的"重点工作"原文（程序化筛选，不重打单元格内容）
KEEP = [
    "6个酒店改造",
    "重庆文旅集团合作",
    "大理拓展项目合作",
    "安逸礼物(暂定名)合作项目工作",
    "十五五规划",
    "对接集团科创部各项事务",
    "对接集团产发部各项事务",
    "国堰宾馆主题文化酒店改造项目",
    "旅游列车项目",
    "总府皇冠改造方案",
    "其他跟进项目",
    "锦绣天府号列车试运行主题活动",
    "希尔顿花园酒店项目",
]

wb = openpyxl.load_workbook(SRC)
ws = wb.active

HDR = 3
TPL = 4
styles = [copy(ws.cell(TPL, c)._style) for c in range(1, 6)]
row_h = ws.row_dimensions[TPL].height

# 先采集要保留的行（值 + 样式），再清空
kept = []
for r in range(HDR + 1, ws.max_row + 1):
    name = ws.cell(r, 2).value
    if name is None:
        continue
    nm = str(name).strip()
    if nm in KEEP:
        vals = [ws.cell(r, c).value for c in range(1, 6)]
        kept.append((r, vals))

print("matched rows:", len(kept), [k[0] for k in kept])

# 清除所有数据行
if ws.max_row >= TPL:
    ws.delete_rows(TPL, ws.max_row - TPL + 1)

# 标题行：仅改 A1 与 E1，其余不动
ws.cell(1, 1).value = "近期重点工作进展 投资+资管+产发（产业发展部专版）"

# 回写保留行（逐字复制原值 + 原样式）
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
print("SAVED:", OUT)
print("ROWS:", len(kept), "SIZE:", os.path.getsize(OUT))
