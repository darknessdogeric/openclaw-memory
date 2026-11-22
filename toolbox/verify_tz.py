# -*- coding: utf-8 -*-
import openpyxl, io
p = r"C:\Users\ericz\Desktop\产业发展部\2026.10.31 产业发展部重点工作台账（产发部）.xlsx"
wb = openpyxl.load_workbook(p)
ws = wb.active
out = ["SHEETS: " + " | ".join(wb.sheetnames),
       "dims=%s max_row=%s max_col=%s" % (ws.dimensions, ws.max_row, ws.max_column),
       "freeze=%s" % ws.freeze_panes]
for row in ws.iter_rows(min_row=1, max_row=ws.max_row):
    vals = []
    for c in row:
        v = c.value
        if v is None:
            v = ""
        vals.append(str(v).replace("\n", " ⏎ "))
    if any(x.strip() for x in vals):
        out.append("[R%d] " % row[0].row + " || ".join(vals))
io.open(r"D:\B166ER-openclaw\workspace\toolbox\_verify\fazhan_taizhang_verify.txt","w",encoding="utf-8").write("\n".join(out))
print("rows=%d chars=%d" % (len(out), sum(len(x) for x in out)))
