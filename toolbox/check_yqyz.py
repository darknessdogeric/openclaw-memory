# -*- coding: utf-8 -*-
import openpyxl, io
SRC = r"C:\Users\ericz\Desktop\安逸一企一策分析表-1107.xlsx"
wb = openpyxl.load_workbook(SRC, data_only=True)
ws = wb.active
def num(v):
    return float(v) if isinstance(v, (int, float)) else None
out = ["序号 | 公司 | 资产负债率 | 净资产 | 累计损益 | EBITDA | 财务费用 | 收入 | 出售 | 出租 | 原建议 || 范式判定 || 是否一致"]
mismatch = []
for r in range(2, ws.max_row + 1):
    nm = ws.cell(r, 2).value
    if not nm: continue
    g = lambda i: num(ws.cell(r, i).value)
    orig = ws.cell(r, 3).value or ""
    debt_ratio = g(10); eq = g(11); cum = g(12); ebitda = g(16); fin = g(9)
    rev = g(15); sell = g(13); rent = g(14)
    # 范式判定
    if nm in ("安逸合并", "安逸本部"):
        code, why = "S01", "集团/本部定位"
    elif debt_ratio is not None and debt_ratio > 1:
        if (ebitda is not None and ebitda > 0) and (rev or 0) > 3000:
            code, why = "S02", "资不抵债但有经营与重组价值"
        elif (ebitda is not None and ebitda <= 0) or (rev or 0) < 100:
            code, why = "S03", "资不抵债且无造血"
        else:
            code, why = "S02/S05", "资不抵债"
    elif rev is not None and (rev < 100 or (ebitda is not None and ebitda <= 0)):
        code, why = "S04", "闲置或无经营"
    elif ebitda is not None and fin not in (None, 0) and ebitda < fin:
        code, why = "S05", "EBITDA<财务费用，利息覆盖不足"
    elif (rev or 0) >= 1000 and (eq or 0) > 0:
        code, why = "S07/S08", "有经营基础可自营"
    else:
        code, why = "S08/S11", "可持续但未达标"
    # 与原建议关键词比对
    kw = {
        "S01": ["现金流", "股东视角", "轻资产"],
        "S02": ["破产", "止损"],
        "S03": ["清算", "停业", "关停", "注销", "退出"],
        "S04": ["出租", "出售", "闲置"],
        "S05": ["出租", "出售", "还债"],
        "S07": ["改造", "标杆"],
        "S08": ["转正", "GOP", "ROE"],
        "S11": ["止损", "退出"],
    }.get(code, [])
    ok = "一致" if (not kw or any(k in orig for k in kw)) else "★需复核"
    if ok.startswith("★"):
        mismatch.append((nm, orig, code, why))
    out.append("%s | %s | %s | %s | %s | %s | %s | %s | %s | %s | %s || %s %s || %s" % (
        ws.cell(r,1).value, nm, debt_ratio, eq, cum, ebitda, fin, rev, sell, rent,
        orig[:34], code, why, ok))
out.append("")
out.append("=== 需复核 %d 行 ===" % len(mismatch))
for nm, orig, code, why in mismatch:
    out.append("  %s | 原: %s | 范式: %s (%s)" % (nm, orig[:40], code, why))
io.open(r"D:\B166ER-openclaw\workspace\toolbox\_extract_fazhan\yqyz_check.txt","w",encoding="utf-8").write("\n".join(out))
print("需复核行数:", len(mismatch))
print("\n".join(out[-12:]))
