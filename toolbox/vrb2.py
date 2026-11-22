import openpyxl, io
p = r"C:\Users\ericz\Desktop\省旅投与人保财险合作清单_酒店板块已填_2026-11-12.xlsx"
wb = openpyxl.load_workbook(p, data_only=True)
ws = wb.active
out = ["SHEET: %s" % ws.title]
for c in range(1, 12):
    v = ws.cell(3, c).value
    out.append("--- C%d [%s]" % (c, ws.cell(2, c).value))
    out.append(str(v))
io.open(r"D:\B166ER-openclaw\workspace\toolbox\_verify\rb2.txt","w",encoding="utf-8").write("\n".join(out))
print("OK")
