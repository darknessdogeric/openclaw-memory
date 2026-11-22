# -*- coding: utf-8 -*-
import openpyxl, io

SRC = r"C:\Users\ericz\Desktop\2026.10.25 近期重点工作任务台账（资管+投资+产发）(3)(2).xlsx"
wb = openpyxl.load_workbook(SRC)
ws = wb.active

def fillinfo(cell):
    f = cell.fill
    if f is None:
        return "none", "none"
    pt = f.patternType
    fg = f.fgColor
    rgb = fg.rgb if fg is not None and fg.type == "rgb" else None
    theme = fg.theme if fg is not None and fg.type == "theme" else None
    indexed = fg.indexed if fg is not None and fg.type == "indexed" else None
    return str(pt), "rgb=%s theme=%s indexed=%s" % (rgb, theme, indexed)

out = []
out.append("max_row=%s max_col=%s" % (ws.max_row, ws.max_column))
out.append("")
out.append("=== 每行填充色（列A序号 / 列B重点工作 / 各列fill） ===")
for r in range(1, ws.max_row + 1):
    no = ws.cell(r, 1).value
    nm = ws.cell(r, 2).value
    fills = []
    for c in range(1, 6):
        pt, det = fillinfo(ws.cell(r, c))
        fills.append("C%d:%s|%s" % (c, pt, det))
    out.append("[R%d] no=%r name=%r" % (r, no, str(nm)[:34] if nm else None))
    for x in fills:
        out.append("      " + x)

dest = r"D:\B166ER-openclaw\workspace\toolbox\_extract_fazhan\tz_fills.txt"
io.open(dest, "w", encoding="utf-8").write("\n".join(out))
print("OK")
