import openpyxl, io
p = r"C:\Users\ericz\Desktop\一企一策分析表_管理建议修订版_v1.1_2026-11-11.xlsx"
wb = openpyxl.load_workbook(p, data_only=True)
out = ["SHEETS: " + " | ".join(wb.sheetnames)]
ws = wb["一企一策测算表"]
hdr = [ws.cell(1, c).value for c in range(1, 9)]
out.append("HDR: " + " | ".join(str(h) for h in hdr))
for r in range(2, 30):
    if not ws.cell(r, 2).value: break
    out.append("")
    out.append("R%d %s | 原:%s" % (r, ws.cell(r,2).value, str(ws.cell(r,3).value)[:50]))
    out.append("    新:%s" % str(ws.cell(r,4).value)[:110])
    out.append("    [%s] %s | 序%s | 投:%s | 缺:%s" % (ws.cell(r,5).value, str(ws.cell(r,6).value)[:40],
        ws.cell(r,7).value, str(ws.cell(r,8).value)[:22], str(ws.cell(r,9).value)[:22]))
s2 = wb["修订汇总"]
out.append("")
out.append("=== 修订汇总页 ===")
for i in range(1, 11):
    a = s2.cell(i,1).value
    if not a: break
    out.append("  %s | %s" % (a, str(s2.cell(i,2).value)[:60]))
io.open(r"D:\B166ER-openclaw\workspace\toolbox\_verify\v11.txt","w",encoding="utf-8").write("\n".join(out))
print("OK rows=%d" % (len([1 for r in range(2,30) if ws.cell(r,2).value])))
