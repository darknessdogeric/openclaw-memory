# -*- coding: utf-8 -*-
"""v42：文创化改造情景测算（在地文化溢价能否撑起财务）
   情景 S1 基线 vs S1+文创化（CPI 溢价 / 非房系数提升 / 文化预算）
   对比 S7B，给出「五星档+文创」与「外部奢牌」的路径比较"""
import os, json, importlib.util
T = r"D:\B166ER-openclaw\workspace\.tmp"
D = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc"
OUT = open(os.path.join(T, "v42.log"), "w", encoding="utf-8")
def L(*a):
    OUT.write(" ".join(str(z) for z in a) + "\n"); OUT.flush()

spec = importlib.util.spec_from_file_location("v10", os.path.join(D, "v10_econ.py"))
V10 = importlib.util.module_from_spec(spec); spec.loader.exec_module(V10)
V21 = json.load(open(os.path.join(T, "v21.json"), encoding="utf-8"))
BASE = V21["base"]; SCH = {s["key"]: s for s in V21["schemes"]}
S1 = SCH["S1"]; S7B = SCH["S7B"]
AF = 0.08
BASE_NPV = round(BASE["owner_cf"] * sum(1 / (1 + AF) ** i for i in range(20)), 1)
def P(v): return ("%.2f%%" % (v * 100)) if v is not None else "无可解"
def N(v, d=1): return format(round(v, d), ",.%df" % d)

L("=== 0. 现状参数 ===")
L("不改造基准净现值 %s 万（年失血 %.1f 万）" % (N(BASE_NPV), BASE["owner_cf"]))
L("S1 现状：ADR %.0f｜房量 %d｜停业 %d 月｜改造投资 %s 万｜停业损失 %s 万" %
  (S1["adr"], S1["n_rooms"], S1["months"], N(S1["capex"]), N(S1["loss"])))
brand_cost_y = S1["steady_rev"] * 0.02 + S1["steady_rev"] * 0.03 + S1["steady_rev"] * 0.02 + S1["steady_rev"] * 0.02 + S1["steady_rev"] * 0.30 * 0.06
L("模型隐含品牌相关成本 %.1f 万/年（基础2%%+营销3%%+忠诚2%%+储备2%%+激励6%%）" % brand_cost_y)
L("集团台账实际：每年向洲际支付 900 万元品牌相关费用 → 模型取值高于实际 %.0f 万/年，属偏保守" % (brand_cost_y - 900))

def model(n_rooms, adr, occ, gop, nonroom, capex, months, adr_lift=0.0, nonroom_lift=0.0,
          culture_budget=0.0, culture_years=3, lift_delay=12,
          base=0.020, mkt=0.030, loy=0.020, ffe=0.020, inc=0.060, horizon=20):
    """adr_lift/nonroom_lift 在复业 lift_delay 个月后分两年逐步到位；culture_budget 为复业后年度文化预算（万元/年）"""
    def revenue_at(since):
        a = adr; n = nonroom
        if since >= lift_delay:
            k = min(1.0, (since - lift_delay + 1) / 24.0)
            a = adr * (1 + adr_lift * k)
            n = nonroom * (1 + nonroom_lift * k)
        return n_rooms * 365 * occ * a / 1e4 * n
    total_steady = revenue_at(horizon * 12)
    mcf = []
    for tt in range(1, horizon * 12 + 1):
        rev = 0.0
        if tt > months:
            since = tt - months
            ramp = min(1.0, 0.62 + 0.038 * since)
            rev = (revenue_at(since) / 12.0) * ramp
        g = rev * gop
        r_ = rev / total_steady if total_steady else 0
        owner = (g - total_steady * base * r_ - total_steady * mkt * r_
                 - total_steady * loy * r_ - total_steady * ffe * r_ - g * inc)
        cash = owner
        if tt <= months:
            cash -= 284.0
            cash -= total_steady * base * 0.35 / 12.0
        half = max(1, months // 2)
        if 1 <= tt <= half: cash -= capex * 0.6 / half
        elif half < tt <= months: cash -= capex * 0.4 / max(1, months - half)
        if tt > months:
            since = tt - months
            if since < 12: cash -= total_steady * 0.085 / 12.0
            elif since < 24: cash -= total_steady * 0.030 / 12.0
            if since < 6: cash -= total_steady * 0.012 / 6.0
            # 文化预算：复业后 culture_years 年
            if since < culture_years: cash -= culture_budget / 12.0
        mcf.append(cash)
    acf = [round(sum(mcf[y * 12:(y + 1) * 12]), 1) for y in range(horizon)]
    ann = (total_steady * gop - total_steady * (base + mkt + loy + ffe) - total_steady * gop * inc)
    grp = [-capex] + [ann] * horizon
    inc_cf = [acf[i] - BASE["owner_cf"] for i in range(horizon)]
    def pv(cf, r=AF): return round(sum(c / (1 + r) ** i for i, c in enumerate(cf)), 1)
    return dict(rev=total_steady, npv=pv(acf), irr=V10.irr(acf), pb=V10.payback(acf),
                irr_grp=V10.irr(grp), pb_grp=(round(capex / ann, 2) if ann > 0 else None),
                irr_inc=V10.irr(inc_cf), pb_inc=V10.payback(inc_cf),
                inc_npv=pv(inc_cf), acf=acf)

L("")
L("=== 1. S1 基线复算（校验与正式稿一致）===")
b = model(S1["n_rooms"], S1["adr"], 0.70, 0.30, 1.42, S1["capex"], S1["months"])
L("   稳态年营收 %.1f 万（正式稿 %.1f）｜绝对净现值 %.1f（正式稿 %.1f）｜增量净现值 %.1f｜增量IRR %s（正式稿 %s）"
  % (b["rev"], S1["steady_rev"], b["npv"], S1["npv20"], b["inc_npv"], P(b["irr_inc"]), P(S1["irr_inc"])))

L("")
L("=== 2. S1 + 文创化改造情景（在地说 = 策展溢价指数 CPI）===")
L("   CPI 定义沿用国堰 KPI 口径：本店平均房价 ÷ 同城同档竞品平均房价，目标 ≥1.15，Kill 判据 <1.10")
L("   %-34s %10s %10s %10s %9s %8s" % ("情景", "年营收", "绝对净现值", "增量净现值", "增量IRR", "增量回收"))
scen = []
for lbl, cpi, nrlift, cb in [
    ("基线 S1（无文创）", 0.00, 0.00, 0),
    ("保守 CPI 1.10 · 预算320万/年", 0.10, 0.06, 320),
    ("基准 CPI 1.15 · 预算280万/年", 0.15, 0.09, 280),
    ("乐观 CPI 1.20 · 预算240万/年", 0.20, 0.12, 240),
]:
    m = model(S1["n_rooms"], S1["adr"], 0.70, 0.30, 1.42, S1["capex"], S1["months"],
              adr_lift=cpi, nonroom_lift=nrlift, culture_budget=cb)
    scen.append((lbl, m))
    L("   %-34s %10.1f %10.1f %10.1f %9s %8s" % (lbl, m["rev"], m["npv"], m["inc_npv"], P(m["irr_inc"]), m["pb_inc"]))

L("")
L("=== 3. 文化投资本身是否划算（增量口径：文创情景 − S1 基线）===")
base_m = scen[0][1]
for lbl, m in scen[1:]:
    d_incn = m["inc_npv"] - base_m["inc_npv"]
    L("   %-34s 增量净现值 %+.1f 万｜增量IRR %s" % (lbl, d_incn, P(m["irr_inc"])))
L("   ★ 判定标准：文创情景增量净现值 > 0 且高于 S7B 的增量净现值 %+.1f 万，则五星档+文创优于外部奢牌" % (S7B["npv20"] - BASE_NPV))

L("")
L("=== 4. 路径比较：五星档+文创 vs 外部奢牌 ===")
s4 = scen[2][1]
L("   %-22s %12s %12s %10s %10s" % ("路径", "改造投资", "增量净现值", "增量IRR", "增量回收"))
L("   %-22s %12s %12s %10s %10s" % ("S1 五星档基线", N(S1["capex"]), N(base_m["inc_npv"]), P(base_m["irr_inc"]), base_m["pb_inc"]))
L("   %-22s %12s %12s %10s %10s" % ("S1 + 文创化（基准）", N(S1["capex"]), N(s4["inc_npv"]), P(s4["irr_inc"]), s4["pb_inc"]))
L("   %-22s %12s %12s %10s %10s" % ("S4 洲至奢选", N(SCH["S4"]["capex"]), N(SCH["S4"]["npv20"] - BASE_NPV), P(SCH["S4"]["irr_inc"]), SCH["S4"]["pb_inc"]))
L("   %-22s %12s %12s %10s %10s" % ("S7B 外部奢牌（上限）", N(S7B["capex"]), N(S7B["npv20"] - BASE_NPV), P(S7B["irr_inc"]), S7B["pb_inc"]))

L("")
L("=== 5. 文创溢价的临界值（增量净现值 = S1 基线 时所需 CPI）===")
lo, hi = 0.0, 0.60
for _ in range(50):
    mid = (lo + hi) / 2
    m = model(S1["n_rooms"], S1["adr"], 0.70, 0.30, 1.42, S1["capex"], S1["months"],
              adr_lift=mid, nonroom_lift=mid * 0.6, culture_budget=280)
    if m["inc_npv"] > base_m["inc_npv"]: hi = mid
    else: lo = mid
L("   文创化投入需产生至少 CPI = %.3f（即平均房价 %.0f 元）才不劣于 S1 基线" % ((lo + hi) / 2, S1["adr"] * (1 + (lo + hi) / 2)))
lo2, hi2 = 0.0, 0.60
for _ in range(50):
    mid = (lo2 + hi2) / 2
    m = model(S1["n_rooms"], S1["adr"], 0.70, 0.30, 1.42, S1["capex"], S1["months"],
              adr_lift=mid, nonroom_lift=mid * 0.6, culture_budget=280)
    if m["inc_npv"] > (S7B["npv20"] - BASE_NPV): hi2 = mid
    else: lo2 = mid
L("   需 CPI = %.3f（平均房价 %.0f 元）才追平 S7B 外部奢牌的增量净现值" % ((lo2 + hi2) / 2, S1["adr"] * (1 + (lo2 + hi2) / 2)))

L("")
L("=== 6. CPI 1.15 下 S1 的关键指标（对照正式稿）===")
m = scen[2][1]
L("   稳态年营收 %.1f 万（基线 %.1f，+%+.1f 万，倍数 %.2f 对改造前 6,774.0）"
  % (m["rev"], base_m["rev"], m["rev"] - base_m["rev"], m["rev"] / BASE["total_rev"]))
L("   平均房价 %.0f 元（基线 %.0f）｜绝对净现值 %.1f 万（基线 %.1f）" % (S1["adr"] * 1.15, S1["adr"], m["npv"], base_m["npv"]))
L("   ★ 文创化后绝对净现值仍为 %s → 与 S7B 的 +16,916.8 万仍有差距，须如实报集团" % ("正" if m["npv"] > 0 else "负"))
L("DONE")
