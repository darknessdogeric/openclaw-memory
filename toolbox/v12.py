import openpyxl
p = r"C:\Users\ericz\Desktop\一企一策分析表_管理建议修订版_v1.2_对齐集团口径_2026-11-12.xlsx"
wb = openpyxl.load_workbook(p, data_only=True)
ws = wb["一企一策测算表"]
for r in range(2, 30):
    nm = ws.cell(r,2).value
    if not nm: break
    if nm in ("华龙宾馆","蒙顶山茶业","天府山庄","梦温泉","花园宾馆","新良宾馆","深圳川宾","乐山嘉州","金桥宾馆"):
        print("%-10s | %s | 序%s" % (nm, str(ws.cell(r,4).value)[:88], ws.cell(r,7).value))
