# -*- coding: utf-8 -*-
import openpyxl, io
OUT = r"C:\Users\ericz\Desktop\一企一策分析表_管理建议修订版_v1.2_含酒店经营指标维度_2026-11-12.xlsx"
ORIG = r"C:\Users\ericz\Desktop\安逸一企一策分析表-1107.xlsx"
out = []

# 1) 原件 1107 的经营现金流列公式
wbo = openpyxl.load_workbook(ORIG)
wso = wbo.active
out.append("=== 1107 原件 经营现金流(第25列)公式与值 ===")
for r in range(2, 30):
    nm = wso.cell(r, 2).value
    if not nm: break
    out.append("R%-2d %-10s C25公式=%-28r 值=%-12s | C15营收=%-10s C16EBITDA=%-8s C9财务费用=%-10s" % (
        r, nm, wso.cell(r,25).value, wso.cell(r,25).value if not isinstance(wso.cell(r,25).value,str) else '(公式)',
        wso.cell(r,15).value, wso.cell(r,16).value, wso.cell(r,9).value))

# 2) Eric版 酒店经营指标 全表
wb = openpyxl.load_workbook(OUT, data_only=True)
ws = wb["酒店经营指标"]
out.append("")
out.append("=== Eric版 酒店经营指标（关键列） ===")
cols = {1:'序',2:'主体',3:'业态',4:'房数',6:'营收',7:'人工',8:'人工率',9:'EBITDA',12:'ADR',13:'OCC',14:'RevPAR',15:'RGI',16:'对标组',17:'GOP率',18:'FT上限',19:'改造投资',20:'增量GOP',21:'回收期',22:'完备度'}
for r in range(2, ws.max_row+1):
    nm = ws.cell(r,2).value
    if not nm: continue
    out.append("R%-2d %s" % (r, " | ".join("%s=%s" % (v, ws.cell(r,k).value) for k,v in cols.items() if ws.cell(r,k).value is not None)))

# 3) 指标口径卡
ws2 = wb["指标口径卡"]
out.append("")
out.append("=== 指标口径卡 ===")
for r in range(1, ws2.max_row+1):
    vals = [str(ws2.cell(r,c).value) for c in range(1, ws2.max_column+1) if ws2.cell(r,c).value is not None]
    if vals: out.append("  " + " | ".join(vals))

# 4) Eric版测算表的列头与几条
ws3 = wb["一企一策测算表"]
hdr = [ws3.cell(1,c).value for c in range(1, ws3.max_column+1)]
out.append("")
out.append("=== Eric版 测算表列数=%d ===" % len([h for h in hdr if h]))
out.append(" | ".join("%d:%s" % (i+1,h) for i,h in enumerate(hdr) if h))
for r in (2,9,14):
    nm = ws3.cell(r,2).value
    if nm:
        out.append("R%d %s :: 建议=%s" % (r, nm, str(ws3.cell(r,4).value)[:100]))

io.open(r"D:\B166ER-openclaw\workspace\toolbox\_extract_fazhan\eric_v12.txt","w",encoding="utf-8").write("\n".join(out))
print("OK lines=%d" % len(out))
