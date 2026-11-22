import openpyxl
p = r"C:\Users\ericz\Desktop\一企一策分析表_管理建议修订版_v1.3_合并集团口径_2026-11-12.xlsx"
O = r"C:\Users\ericz\Desktop\安逸一企一策分析表-1107.xlsx"
wb = openpyxl.load_workbook(p); ws = wb["一企一策测算表"]
wo = openpyxl.load_workbook(O); woo = wo.active
bad = 0
for r in range(2, 30):
    nm = ws.cell(r,2).value
    if not nm: break
    f = ws.cell(r,32).value
    u = ws.cell(r,23).value; n = ws.cell(r,16).value
    ov = woo.cell(r,25).value
    calc = round(u-n,2) if isinstance(u,(int,float)) and isinstance(n,(int,float)) else None
    ok = "OK" if (calc is not None and isinstance(ov,(int,float)) and abs(calc-ov)<0.05) else ("待补" if calc is None else "DIFF")
    if ok not in ("OK","待补"): bad += 1
    print("%-10s %-16s U-N=%-12s 原件=%-12s %s" % (nm, str(f)[:16], calc, ov, ok))
print("不一致行数:", bad)
