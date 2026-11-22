# -*- coding: utf-8 -*-
import openpyxl, io

p = r"C:\Users\ericz\Desktop\2026.10.25 近期重点工作任务台账（资管+投资+产发）.xlsx"
wb = openpyxl.load_workbook(p, data_only=True)
out = ["SHEETS: " + " | ".join(wb.sheetnames)]
for ws in wb.worksheets:
    out.append("")
    out.append("=" * 100)
    out.append("SHEET: %s  dims=%s  max_row=%s max_col=%s" % (ws.title, ws.dimensions, ws.max_row, ws.max_column))
    out.append("=" * 100)
    for row in ws.iter_rows():
        vals = []
        for c in row:
            v = c.value
            if v is None:
                v = ""
            vals.append(str(v).replace("\n", " / "))
        if any(x.strip() for x in vals):
            out.append("[R%d] " % row[0].row + " || ".join(vals))

dest = r"D:\B166ER-openclaw\workspace\toolbox\_extract_fazhan\taizhang_2026-10-25.txt"
io.open(dest, "w", encoding="utf-8").write("\n".join(out))
print("OK lines=%d" % len(out))
