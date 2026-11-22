# 校验：1107表的"股东回报要求"列是否 = 实缴资本 x 3.5%
import openpyxl
wb = openpyxl.load_workbook(r"C:\Users\ericz\Desktop\安逸一企一策分析表-1107.xlsx", data_only=True)
ws = wb.active
print("%-14s %10s %10s %10s %10s %s" % ("主体","实缴","净资产*3.5%","表内值","推断口径","利润总额-回报=股东投资损益"))
for r in range(2, 30):
    nm = ws.cell(r,2).value
    if not nm: break
    paid = ws.cell(r,5).value; eq = ws.cell(r,11).value; req = ws.cell(r,23).value
    inv = ws.cell(r,24).value; pt = ws.cell(r,20).value
    if not isinstance(paid,(int,float)): continue
    calc_paid = round(paid*0.035, 2)
    calc_eq = round(eq*0.035, 2) if isinstance(eq,(int,float)) else None
    match = "实缴x3.5%" if req is not None and abs(req-calc_paid)<0.02 else ("净资产x3.5%" if req is not None and calc_eq is not None and abs(req-calc_eq)<0.02 else "?")
    chk = ""
    if all(isinstance(x,(int,float)) for x in (pt,req,inv)):
        chk = "OK" if abs((pt-req)-inv)<0.02 else "不符"
    print("%-14s %10s %10s %10s %10s %s  %s" % (nm, paid, calc_eq, req, match, chk, ""))
