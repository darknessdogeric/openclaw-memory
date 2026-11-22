# -*- coding: utf-8 -*-
import openpyxl
E = r"C:\Users\ericz\Desktop\一企一策分析表_管理建议修订版_v1.2_含酒店经营指标维度_2026-11-12.xlsx"
O = r"C:\Users\ericz\Desktop\安逸一企一策分析表-1107.xlsx"
we = openpyxl.load_workbook(E); wso = we["一企一策测算表"]
wo = openpyxl.load_workbook(O); woo = wo.active
print("列位: 16=财务费用(N) 17=资产负债率(O) 22=营业收入(T) 23=EBITDA(U) 25=人工成本(W) 32=经营现金流(AF)")
print()
print("%-10s | %-22s | %-12s | %-12s | %-12s | %s" % ("主体","Eric版C32公式","EBITDA(U)","财务费用(N)","U-N应为","1107原件值"))
for r in range(2, 30):
    nm = wso.cell(r,2).value
    if not nm: break
    f = wso.cell(r,32).value
    u = wso.cell(r,23).value; n = wso.cell(r,16).value
    ov = woo.cell(r,25).value if r <= 29 else None
    calc = (u - n) if isinstance(u,(int,float)) and isinstance(n,(int,float)) else None
    print("%-10s | %-22s | %-12s | %-12s | %-12s | %s" % (nm, str(f)[:22], u, n, calc, ov))
print()
print("=== 房量列(35)现状 ===")
for r in range(2, 30):
    nm = wso.cell(r,2).value
    if not nm: break
    print("  %-10s 房量=%s  RGI=%s  回收期=%s" % (nm, wso.cell(r,35).value, wso.cell(r,36).value, wso.cell(r,37).value))
