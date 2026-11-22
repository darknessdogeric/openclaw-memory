# -*- coding: utf-8 -*-
import openpyxl, io
p = r"C:\Users\ericz\Desktop\产业发展部\2026.10.25 近期重点工作任务台账（产发部专版）.xlsx"
wb = openpyxl.load_workbook(p)
ws = wb.active
out = ["dims=%s max_row=%s freeze=%s" % (ws.dimensions, ws.max_row, ws.freeze_panes)]
for row in ws.iter_rows(min_row=1, max_row=ws.max_row):
    vals = []
    for c in row:
        v = c.value
        if v is None:
            v = ""
        vals.append(str(v).replace("\n", " ⏎ "))
    if any(x.strip() for x in vals):
        out.append("[R%d] " % row[0].row + " || ".join(vals))
io.open(r"D:\B166ER-openclaw\workspace\toolbox\_verify\tz_yellow8.txt","w",encoding="utf-8").write("\n".join(out))
print("rows=%d" % len(out))
