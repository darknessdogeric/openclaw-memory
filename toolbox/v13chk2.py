import openpyxl
V = r"C:\Users\ericz\Desktop\一企一策分析表_管理建议修订版_v1.3_合并集团口径_2026-11-12.xlsx"
O = r"C:\Users\ericz\Desktop\安逸一企一策分析表-1107.xlsx"
wv = openpyxl.load_workbook(V, data_only=True); wsv = wv["一企一策测算表"]
wo = openpyxl.load_workbook(O, data_only=True); woo = wo.active
ok = diff = pend = 0
for r in range(2, 30):
    nm = wsv.cell(r,2).value
    if not nm: break
    u = wsv.cell(r,23).value; n = wsv.cell(r,16).value
    ov = woo.cell(r,25).value
    if not (isinstance(u,(int,float)) and isinstance(n,(int,float))):
        pend += 1; continue
    calc = round(u-n, 2)
    if isinstance(ov,(int,float)) and abs(calc-round(ov,2))<0.05:
        ok += 1
    else:
        diff += 1
        print("  DIFF %s v1.3=%s 原件=%s" % (nm, calc, ov))
print("经营现金流复算：吻合 %d 行 / 不一致 %d 行 / 待补 %d 行" % (ok, diff, pend))
# 房量完备度
wsi = wv["酒店经营指标"]
have = [wsi.cell(r,2).value for r in range(2, wsi.max_row+1)
        if wsi.cell(r,2).value and isinstance(wsi.cell(r,4).value,(int,float))]
print("房量已取得 %d 家：%s" % (len(have), have))
