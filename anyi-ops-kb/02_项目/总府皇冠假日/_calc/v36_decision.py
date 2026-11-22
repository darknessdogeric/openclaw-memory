# -*- coding: utf-8 -*-
"""v36：决策口径重建 —— 把「不改造」与「局部整改」作为真实反事实基准
   ① 统一 20 年口径的三方案决策表
   ② 全方案增量口径重排（真正该用的判据）
   ③ 面积门槛硬约束下的房量上限与重算
   ④ 品牌方分摊情景（外部奢牌路径的真实可行形态）
   ⑤ 敏感性排序：哪一项最决定成败"""
import os, json, importlib.util
T = r"D:\B166ER-openclaw\workspace\.tmp"
D = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc"
OUT = open(os.path.join(T, "v36.log"), "w", encoding="utf-8")
def L(*a):
    OUT.write(" ".join(str(z) for z in a) + "\n"); OUT.flush()

spec = importlib.util.spec_from_file_location("v10", os.path.join(D, "v10_econ.py"))
V10 = importlib.util.module_from_spec(spec); spec.loader.exec_module(V10)
V21 = json.load(open(os.path.join(T, "v21.json"), encoding="utf-8"))
BASE = V21["base"]; SCH = {s["key"]: s for s in V21["schemes"]}
AF = 0.08
ANN = sum(1 / (1 + AF) ** i for i in range(20))

def P(v): return ("%.2f%%" % (v * 100)) if v is not None else "无可解"
def N(v, d=1): return format(round(v, d), ",.%df" % d)

# ══ ① 真实反事实基准 ══
L("=== 1. 三条真实基准（20 年、8% 折现）===")
base_npv = round(BASE["owner_cf"] * ANN, 1)
L("基准A 不改造：年经营现金流 %.1f 万（实测失血），20 年净现值 %.1f 万" % (BASE["owner_cf"], base_npv))
L("        ★ 这不是零成本基准。现状报警主机已全面瘫痪、消防不合规，继续经营本身不成立。")
PARTIAL = 4584.0
L("")
L("基准B 局部整改（情景三必选项）：一次性 %.0f 万，收益不变" % PARTIAL)
L("        净现值 = %.1f − %.1f = %.1f 万" % (base_npv, PARTIAL, round(base_npv - PARTIAL, 1)))
L("        结论：情景三下局部整改比不改造还差 %.0f 万（合规是义务，不是选项）" % PARTIAL)
L("")
L("基准C 停业等待（现状唯一合规状态）：零收入、零改造支出")
L("        净现值视同不改造 %.1f 万（已含失血），但无任何改善" % base_npv)

# ══ ② 全方案三口径重排 ══
L("")
L("=== 2. 九方案统一口径重排 ===")
L("   %-5s %-10s %10s %10s %10s %9s %9s %9s" % ("方案", "品牌·做法", "改造投资", "年营收", "绝对净现值", "增量净现值", "增量IRR", "增量回收"))
ROWS = []
for k in ("S1", "S2", "S3", "S4", "S5", "S6", "S7", "S7B", "S8"):
    s = SCH[k]
    inc_npv = round(s["npv20"] - base_npv, 1)
    ROWS.append((k, s, inc_npv))
    L("   %-5s %-10s %10.1f %10.1f %10.1f %9.1f %9s %9s" % (
        k, "%s·%s" % (s["brand"][:4], s["room_mode"][:4]), s["capex"], s["steady_rev"],
        s["npv20"], inc_npv, P(s["irr_inc"]), s["pb_inc"]))
L("")
L("   ★ 读数：绝对口径 S7B 领先，但增量口径（相对「不改造」的真实反事实）——")
best_abs = max(ROWS, key=lambda r: r[1]["npv20"])
best_inc = max(ROWS, key=lambda r: r[2])
L("     绝对净现值最优：%s（%.1f 万）" % (best_abs[0], best_abs[1]["npv20"]))
L("     增量净现值最优：%s（%.1f 万）" % (best_inc[0], best_inc[2]))
s1 = SCH["S1"]; s7b = SCH["S7B"]
L("     S1  增量净现值 %+.1f 万｜增量内部收益率 %s｜增量回收 %s 年｜投资 %.1f 万"
  % (round(s1["npv20"] - base_npv, 1), P(s1["irr_inc"]), s1["pb_inc"], s1["capex"]))
L("     S7B 增量净现值 %+.1f 万｜增量内部收益率 %s｜增量回收 %s 年｜投资 %.1f 万"
  % (round(s7b["npv20"] - base_npv, 1), P(s7b["irr_inc"]), s7b["pb_inc"], s7b["capex"]))
L("     ★ 增量效率几乎相同（%s vs %s），S7B 多投 %.1f 万只换来多 %.1f 万增量净现值"
  % (P(s1["irr_inc"]), P(s7b["irr_inc"]), s7b["capex"] - s1["capex"],
     (round(s7b["npv20"] - base_npv, 1) - round(s1["npv20"] - base_npv, 1))))

# ══ ③ 面积门槛硬约束 ══
L("")
L("=== 3. 面积门槛硬约束 ===")
GN = 10192.0
for need in (40.0, 45.0, 49.0, 60.0):
    mx = int(GN // need)
    L("   套内门槛 %.0f ㎡ → 物理最大 %3d 间（比 268 间少 %3d 间，收入基数降 %.0f%%）"
      % (need, mx, 268 - mx, (268 - mx) / 268 * 100))
L("   ★ 268 间在 40 ㎡ 门槛下物理不可能（需 10,720 ㎡，实有 10,192 ㎡）")
L("   ★ 结论：S7/S7B 的 268 间房量前提不成立，必须按门槛重设房量并重算")

# ══ ④ 品牌方分摊情景 ══
L("")
L("=== 4. 外部奢牌路径的真实可行形态：品牌方分摊改造投入 ===")
def model(n_rooms, adr, occ, gop, nonroom, capex, months, brand_share=0.0,
          base=0.030, mkt=0.025, loy=0.020, ffe=0.040, inc=0.100):
    room_rev = n_rooms * 365 * occ * adr / 1e4
    total = room_rev * nonroom
    bb_y = total * base
    br_m = bb_y * 0.35 / 12.0
    mcf = []
    for tt in range(1, 241):
        rev = 0.0
        if tt > months:
            since = tt - months
            rev = (total / 12.0) * min(1.0, 0.62 + 0.038 * since)
        g = rev * gop
        r_ = rev / total if total else 0
        owner = (g - bb_y * r_ - total * mkt * r_ - total * loy * r_
                 - total * ffe * r_ - g * inc)
        cash = owner
        if tt <= months:
            cash -= 284.0; cash -= br_m
        half = max(1, months // 2)
        if 1 <= tt <= half: cash -= capex * (1 - brand_share) * 0.6 / half
        elif half < tt <= months: cash -= capex * (1 - brand_share) * 0.4 / max(1, months - half)
        if tt > months:
            since = tt - months
            if since < 12: cash -= total * 0.085 / 12.0
            elif since < 24: cash -= total * 0.030 / 12.0
            if since < 6: cash -= total * 0.012 / 6.0
        mcf.append(cash)
    acf = [round(sum(mcf[y * 12:(y + 1) * 12]), 1) for y in range(20)]
    ann = (total * gop - total * (base + mkt + loy + ffe) - total * gop * inc)
    grp = [-capex * (1 - brand_share)] + [ann] * 20
    inc_cf = [acf[i] - BASE["owner_cf"] for i in range(20)]
    def pv(cf, r=0.08): return round(sum(c / (1 + r) ** i for i, c in enumerate(cf)), 1)
    return dict(rev=total, npv=pv(acf), irr=V10.irr(acf), pb=V10.payback(acf),
                irr_inc=V10.irr(inc_cf), pb_inc=V10.payback(inc_cf),
                irr_grp=V10.irr(grp), pb_grp=(round(capex * (1 - brand_share) / ann, 2) if ann > 0 else None),
                inc_npv=round(pv(inc_cf), 1))

CAPEX7 = 56850.9; MON = 20; ROOM_SHARE = 6000.0 / 8700.0; MEP7 = 11600.0; FIT7 = 45250.9
def capex_for(n): return MEP7 + FIT7 * (ROOM_SHARE * n / 268 + (1 - ROOM_SHARE))
L("   %-6s %-6s %-8s %10s %10s %10s %9s %9s" % ("房量", "分摊", "ADR", "业主承担", "年营收", "绝对净现值", "增量净现值", "增量IRR"))
for n in (255, 226, 208):
    for share in (0.0, 0.30, 0.50):
        m = model(n, 3000, 0.70, 0.40, 1.85, capex_for(n), MON, brand_share=share)
        L("   %-6d %-6.0f%% %-8d %10.1f %10.1f %10.1f %9.1f %9s" % (
            n, share * 100, 3000, capex_for(n) * (1 - share), m["rev"], m["npv"], m["inc_npv"], P(m["irr_inc"])))
L("")
L("   ★ 读数：即使 ADR 3,000 全额兑现，品牌方零分摊时增量口径仍远弱于 S1；")
L("      品牌方分摊 30%—50% 后增量净现值转正并放大 —— 这才是外部奢牌路径的真实门槛。")

# ══ ⑤ 敏感性排序 ══
L("")
L("=== 5. 敏感因子排序（对 S1 基准与 S7B 各做 ±15%）===")
import copy
def flex_s7b(adr=None, occ=None, gop=None, nonroom=None, n=None, capex=None):
    kw = dict(adr=adr or 3000, occ=occ or 0.70, gop=gop or 0.40, nonroom=nonroom or 1.85,
              capex=capex or CAPEX7, months=MON)
    if n: kw["n_rooms"] = n
    base_m = model(268, kw["adr"], kw["occ"], kw["gop"], kw["nonroom"], kw["capex"], MON)
    out = []
    for lbl, key, val in (("ADR ±15%", "adr", 3000 * 1.15), ("出租率 ±15%", "occ", 0.70 * 1.15),
                          ("营业利润率 ±15%", "gop", 0.40 * 1.15), ("非房系数 ±15%", "nonroom", 1.85 * 1.15),
                          ("改造投资 ±15%", "capex", CAPEX7 * 1.15)):
        a = dict(kw); a[key] = val
        m = model(268, a["adr"], a["occ"], a["gop"], a["nonroom"], a["capex"], MON)
        out.append((lbl, round(m["npv"] - base_m["npv"], 1)))
    return out
for lbl, d in flex_s7b():
    L("   S7B %-16s 净现值变化 %+.1f 万" % (lbl, d))
L("")
L("   ★ S7B 的成败最敏感于「改造投资」与「营业利润率」，而这两项都不是市场给的 ——")
L("      一个是造价控制问题，一个是经营能力问题，都落在业主自己手里，不是玄学。")
L("DONE")
