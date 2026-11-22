import openpyxl, io
p = r"C:\Users\ericz\Desktop\省旅投与人保财险合作清单_酒店板块已填_2026-11-12.xlsx"
wb = openpyxl.load_workbook(p, data_only=True)
ws = wb.active
out = ["SHEET: %s  max_row=%s" % (ws.title, ws.max_row)]
out.append("R1: " + str(ws.cell(1,1).value))
for c in range(1, 12):
    out.append("H%d: %s" % (c, ws.cell(2, c).value))
out.append("")
for r in (3,):
    for c in range(1, 12):
        v = ws.cell(r, c).value
        out.append("--- R%d C%d [%s]" % (r, c, ws.cell(2,c).value))
        out.append(str(v))
io.open(r"D:\B166ER-openclaw\workspace\toolbox\_verify\rb_hotel.txt","w",encoding="utf-8").write("\n".join(out))
print("OK")
