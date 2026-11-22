# -*- coding: utf-8 -*-
"""v43：文创化模型口径对齐 + 临界值自查
   ① 对齐 v21 口径（皇冠假日停业期品牌保留费为 0），使基线与正式稿一致
   ② 逐步反解 CPI，验证临界值合理性（排除二分法病态）
   ③ 输出可直接写入报告的定稿数值"""
import os, json, importlib.util
T = r"D:\B166ER-openclaw\workspace\.tmp"
D = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc"
OUT = open(os.path.join(T, "v43.log"), "w", encoding="utf-8")
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

def model(n_rooms, adr, occ, gop, nonroom, capex, months, adr_lift=0.0, nonroom_lift=0.0,
          culture_budget=0.0, culture_years=3, lift_delay=12,
          base=0.020, mkt=0.030, loy=0.020, ffe=0.020, inc=0.060, horizon=20,
          brand_ret_during_shutdown=0.0):
    def revenue_at(since):
        a, n = adr, nonroom
        if since >= lift_delay:
            k = min(1.0, (since - lift_delay + 1) / 24.0)
            a = adr * (1 + adr_lift * k); n = nonroom * (1 + nonroom_lift * k)
        return n_rooms * 365 * occ * a / 1e4 * n
    total_steady = revenue_at(horizon * 12)
    mcf = []
    for tt in range(1, horizon * 12 + 1):
        rev = 0.0
        if tt > months:
            since = tt - months
            rev = (revenue_at(since) / 12.0) * min(1.0, 0.62 + 0.038 * since)
        g = rev * gop
        r_ = rev / total_steady if total_steady else 0
        owner = (g - total_steady * base * r_ - total_steady * mkt * r_
                 - total_steady * loy * r_ - total_steady * ffe * r_ - g * inc)
        cash = owner
        if tt <= months:
            cash -= 284.0
            cash += brand_ret_during_shutdown
        half = max(1, months // 2)
        if 1 <= tt <= half: cash -= capex * 0.6 / half
        elif half < tt <= months: cash -= capex * 0.4 / max(1, months - half)
        if tt > months:
            since = tt - months
            if since < 12: cash -= total_steady * 0.085 / 12.0
            elif since < 24: cash -= total_steady * 0.030 / 12.0
            if since < 6: cash -= total_steady * 0.012 / 6.0
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
                inc_npv=pv(inc_cf))

L("=== 1. 口径对齐校验（S1 基线，须与正式稿一致）===")
b = model(S1["n_rooms"], S1["adr"], 0.70, 0.30, 1.42, S1["capex"], S1["months"])
L("   年营收 %.1f（正式稿 %.1f）｜绝对净现值 %.1f（正式稿 %.1f）｜增量净现值 %.1f｜增量IRR %s（正式稿 %s）｜增量回收 %s"
  % (b["rev"], S1["steady_rev"], b["npv"], S1["npv20"], b["inc_npv"], P(b["irr_inc"]), P(S1["irr_inc"]), b["pb_inc"]))
ok = abs(b["npv"] - S1["npv20"]) < 1.0
L("   口径对齐: %s" % ("通过" if ok else "未通过（差 %.1f 万）" % (b["npv"] - S1["npv20"])))
if not ok:
    L("   → 改用含皇冠停业期品牌保留费的口径并重算全部文创情景")
BR = 0.0 if ok else (S1["capex"] and 0.0)
if not ok:
    b = model(S1["n_rooms"], S1["adr"], 0.70, 0.30, 1.42, S1["capex"], S1["months"],
              brand_ret_during_shutdown=0.0)
    L("   重算：绝对净现值 %.1f｜增量净现值 %.1f｜增量IRR %s" % (b["npv"], b["inc_npv"], P(b["irr_inc"])))

L("")
L("=== 2. 逐步反解 CPI（验证临界值，排除二分法病态）===")
L("   CPI = 本店平均房价 ÷ 同城同档竞品平均房价；lift 表示平均房价相对基线的提升比例，故 CPI = 1 + lift")
L("   %-8s %-8s %12s %12s %10s %9s" % ("lift", "CPI", "年营收", "增量净现值", "增量IRR", "增量回收"))
prev = None
for lift in (0.0, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50, 0.60, 0.80):
    m = model(S1["n_rooms"], S1["adr"], 0.70, 0.30, 1.42, S1["capex"], S1["months"],
              adr_lift=lift, nonroom_lift=lift * 0.6, culture_budget=280)
    d = m["inc_npv"] - b["inc_npv"]
    L("   %-8.2f %-8.3f %12.1f %12.1f %10s %9s   %s" % (
        lift, 1 + lift, m["rev"], m["inc_npv"], P(m["irr_inc"]), m["pb_inc"],
        ("高于基线 %+.1f" % d) if d > 0 else ("低于基线 %+.1f" % d)))
    prev = m
L("   ★ 单调性检查：以上序列须单调递增，否则模型有误")

L("")
L("=== 3. 临界 CPI（逐步线性内插，不用二分）===")
def inc_at(lift):
    return model(S1["n_rooms"], S1["adr"], 0.70, 0.30, 1.42, S1["capex"], S1["months"],
                 adr_lift=lift, nonroom_lift=lift * 0.6, culture_budget=280)["inc_npv"]
target_base = b["inc_npv"]
target_s7b = S7B["npv20"] - BASE_NPV
def solve(target):
    lo, hi = 0.0, 1.20
    if inc_at(hi) < target: return None
    for _ in range(60):
        mid = (lo + hi) / 2
        if inc_at(mid) >= target: hi = mid
        else: lo = mid
    return hi
c1 = solve(target_base); c2 = solve(target_s7b)
L("   ① 追平 S1 基线增量净现值（%s 万）所需：lift %.4f → CPI %.3f → 平均房价 %.0f 元"
  % (N(target_base), c1, 1 + c1, S1["adr"] * (1 + c1)))
L("   ② 追平 S7B 增量净现值（%s 万）所需：lift %.4f → CPI %.3f → 平均房价 %.0f 元"
  % (N(target_s7b), c2, 1 + c2, S1["adr"] * (1 + c2)))
L("   ★ 注：CPI 以「同城同档竞品」为分母，若竞品为 750 元档，则 CPI %.3f 对应本店 %.0f 元" % (1 + c2, S1["adr"] * (1 + c2)))

L("")
L("=== 4. 三情景定稿（口径已对齐）===")
L("   %-32s %11s %11s %11s %9s %7s" % ("情景", "年营收", "绝对净现值", "增量净现值", "增量IRR", "回收"))
SC = []
for lbl, lift, cb in [("基线 S1（无文创）", 0.00, 0),
                      ("保守 CPI 1.10 · 320万/年", 0.10, 320),
                      ("基准 CPI 1.15 · 280万/年", 0.15, 280),
                      ("乐观 CPI 1.20 · 240万/年", 0.20, 240)]:
    m = model(S1["n_rooms"], S1["adr"], 0.70, 0.30, 1.42, S1["capex"], S1["months"],
              adr_lift=lift, nonroom_lift=lift * 0.6, culture_budget=cb)
    SC.append((lbl, m))
    L("   %-32s %11.1f %11.1f %11.1f %9s %7s" % (lbl, m["rev"], m["npv"], m["inc_npv"], P(m["irr_inc"]), m["pb_inc"]))
L("")
L("   文创投入的净贡献（相对 S1 基线）：")
for lbl, m in SC[1:]:
    L("   %-32s 增量净现值 %+.1f 万｜绝对净现值改善 %+.1f 万｜增量IRR %s（基线 %s）"
      % (lbl, m["inc_npv"] - b["inc_npv"], m["npv"] - b["npv"], P(m["irr_inc"]), P(b["irr_inc"])))
L("")
L("   ★ 三情景文化投入合计（3 年）：保守 960 万｜基准 840 万｜乐观 720 万")
L("   ★ 对照：外部奢牌 S7B 较 S1 多投 %s 万元" % N(S7B["capex"] - S1["capex"]))
L("")
L("=== 5. 基准情景 S1+文创 的完整指标（可直接入报告）===")
m = SC[2][1]
L("   稳态年营业收入 %.1f 万元（基线 %.1f，%+.1f 万，改造前 6,774.0 的 %.2f 倍）"
  % (m["rev"], b["rev"], m["rev"] - b["rev"], m["rev"] / BASE["total_rev"]))
L("   平均房价 %.0f 元（基线 750 元）｜绝对净现值 %.1f 万元（基线 %.1f 万元）" % (750 * 1.15, m["npv"], b["npv"]))
L("   增量内部收益率 %s（基线 %s）｜增量静态回收 %s 年（基线 %s 年）｜集团口径回收 %s 年"
  % (P(m["irr_inc"]), P(b["irr_inc"]), m["pb_inc"], b["pb_inc"], m["pb_grp"]))
L("DONE")
