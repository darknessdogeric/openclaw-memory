import io, openpyxl
SRC = r"C:\Users\ericz\Desktop\省旅游投资集团与人保财险合作事项对接联系清单.xlsx"
wb = openpyxl.load_workbook(SRC, data_only=True)
out = ["SHEETS: " + " | ".join(wb.sheetnames)]
for ws in wb.worksheets:
    out.append("")
    out.append("=" * 100)
    out.append("SHEET: %s  dims=%s max_row=%s max_col=%s" % (ws.title, ws.dimensions, ws.max_row, ws.max_column))
    out.append("=" * 100)
    for row in ws.iter_rows():
        vals = []
        for c in row:
            v = c.value
            vals.append("" if v is None else str(v).replace("\n", " / "))
        if any(x.strip() for x in vals):
            out.append("[R%d] " % row[0].row + " || ".join(vals))
    if ws.merged_cells.ranges:
        out.append("MERGED: " + ", ".join(str(r) for r in list(ws.merged_cells.ranges)[:60]))
io.open(r"D:\B166ER-openclaw\workspace\toolbox\_extract_fazhan\renbao_list.txt","w",encoding="utf-8").write("\n".join(out))
print("OK lines=%d" % len(out))
