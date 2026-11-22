# -*- coding: utf-8 -*-
import openpyxl, io
SRC = r"C:\Users\ericz\Desktop\安逸一企一策分析表-1107.xlsx"
wb = openpyxl.load_workbook(SRC, data_only=True)
ws = wb.active
hdr = [ws.cell(1, c).value for c in range(1, 28)]
out = ["HDR: " + " | ".join(str(h) for h in hdr)]
rows = []
for r in range(2, ws.max_row + 1):
    nm = ws.cell(r, 2).value
    if not nm:
        continue
    vals = [ws.cell(r, c).value for c in range(1, 28)]
    rows.append(vals)
    out.append("")
    out.append("R%d %s" % (r, nm))
    out.append("   建议: %s" % vals[2])
    def g(i):
        v = vals[i]
        return float(v) if isinstance(v, (int, float)) else None
    # 派生：出售回收年数、出租回收年数、EBITDA覆盖利息倍数
    sell, rent = g(12), g(13)
    ebitda, fin = g(15), g(8)
    eq = g(10)
    if sell and rent:
        out.append("   出售/出租回收年数: %.1f 年" % (sell / rent))
    if ebitda is not None and fin not in (None, 0):
        out.append("   EBITDA/财务费用: %.2f 倍" % (ebitda / fin))
    if eq is not None and eq < 0:
        out.append("   负净资产: %.2f 万元" % eq)
# 汇总
neg = sum(v[10] for v in rows if isinstance(v[10], (int, float)) and v[10] < 0)
sell_sum = sum(v[12] for v in rows if isinstance(v[12], (int, float)))
rent_sum = sum(v[13] for v in rows if isinstance(v[13], (int, float)))
neg_n = len([v for v in rows if isinstance(v[10], (int, float)) and v[10] < 0])
out.append("")
out.append("=== 汇总 ===")
out.append("主体数 %d，其中净资产为负 %d 家" % (len(rows), neg_n))
out.append("负净资产合计 %.2f 万元" % neg)
out.append("有出售价格合计 %.2f 万元" % sell_sum)
out.append("有出租价格合计 %.2f 万元/年" % rent_sum)
out.append("全部出售回收年数 %.1f 年" % (sell_sum / rent_sum))
merged = rows[0]
out.append("安逸合并: 资产 %.0f 负债 %.0f 资产负债率 %.4f 累计损益 %.0f 财务费用 %.0f 经营现金流 %.0f"
           % (merged[5], merged[6], merged[9], merged[11], merged[8], merged[24]))
hq = rows[1]
out.append("安逸本部: 资产 %.0f 负债 %.0f 资产负债率 %.4f 净利润 %.0f 经营现金流 %.0f"
           % (hq[5], hq[6], hq[9], hq[20], hq[24]))
out.append("本部+全出租年收入 %.0f vs 合并财务费用 %.0f → 覆盖 %.2f 倍" % (rent_sum, merged[8], rent_sum / merged[8]))
io.open(r"D:\B166ER-openclaw\workspace\toolbox\_extract_fazhan\yqyz_calc.txt","w",encoding="utf-8").write("\n".join(out))
print("OK")
