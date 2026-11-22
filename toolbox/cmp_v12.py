# -*- coding: utf-8 -*-
import openpyxl, io
A = r"C:\Users\ericz\Desktop\一企一策分析表_管理建议修订版_v1.2_含酒店经营指标维度_2026-11-12.xlsx"
B = r"C:\Users\ericz\Desktop\一企一策分析表_管理建议修订版_v1.2_对齐集团口径_2026-11-12.xlsx"
out = []
for tag, F in (("Eric版(含酒店经营指标维度)", A), ("我的版(对齐集团口径)", B)):
    wb = openpyxl.load_workbook(F, data_only=True)
    out.append("=" * 100)
    out.append("FILE %s | SHEETS: %s" % (tag, wb.sheetnames))
    out.append("=" * 100)
    for ws in wb.worksheets:
        out.append("-- SHEET %s dims=%s" % (ws.title, ws.dimensions))
        if ws.title.startswith("修订汇总") or ws.title.startswith("使用说明"):
            for i in range(1, 14):
                a = ws.cell(i,1).value
                if not a: break
                out.append("   %s | %s | %s" % (a, str(ws.cell(i,2).value)[:90], str(ws.cell(i,3).value)[:110]))
            out.append("")
            continue
        hdr = [ws.cell(1,c).value for c in range(1, ws.max_column+1)]
        out.append("   HDR(%d列): %s" % (len(hdr), " | ".join(str(h) for h in hdr if h)))
        for r in range(2, ws.max_row+1):
            nm = ws.cell(r,2).value
            if not nm: continue
            out.append("   R%d %s" % (r, nm))
            for c in range(1, ws.max_column+1):
                v = ws.cell(r,c).value
                if v is None: continue
                out.append("      [%s] %s" % (str(hdr[c-1])[:18], str(v)[:150]))
    out.append("")
io.open(r"D:\B166ER-openclaw\workspace\toolbox\_extract_fazhan\v12_cmp.txt","w",encoding="utf-8").write("\n".join(out))
print("OK lines=%d" % len(out))
