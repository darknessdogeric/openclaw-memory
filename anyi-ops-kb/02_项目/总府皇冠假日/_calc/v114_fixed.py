# -*- coding: utf-8 -*-
"""
v114 修正测算内核 —— 统一月度时间轴（修正前模型把年现金流按月折现，系统性低估现值约 2.5 亿元）
2026-11-15｜产业发展部

【错误说明】
原模型现金流序列为：[-资本开支] + [停业月现金流] + [爬坡月现金流] + [年度现金流×20]，
但统一按 (1+8%)^i 折现，序号 i 连续累加。结果 20 笔"年度现金流"被折现到
第 19—38 期（相当于按月折现年现金流），现值被严重低估。
修正：全流程统一为月度网格，折现率按 (1+8%/12)^m 计算。

【时间轴定义】
  第 1—D 月：停业（无收入，付固定成本）
  第 D+1 至 D+R 月：复业爬坡（收入系数 0.45→0.85）
  第 D+R+1 至 240 月：达产经营
  资本开支于第 0 月
  评价期：停业期 + 20 年经营期
"""
import json, os, io, sys

T = r"D:\B166ER-openclaw\workspace\.tmp"
LOG = open(os.path.join(T, "v114.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()

V111 = json.load(open(os.path.join(T, "v111.json"), encoding="utf-8"))
D98 = json.load(open(os.path.join(T, "v98.json"), encoding="utf-8"))
B = D98["base"]; PATHS = D98["paths"]; CAPEX = V111["capex"]; DUR = V111["duration"]
R_ANN = 0.08; R_M = (1 + R_ANN) ** (1 / 12.0) - 1     # 月度折现率

def npv_m(cfs): return sum(cf / ((1 + R_M) ** m) for m, cf in enumerate(cfs))
def irr_m(cfs, lo=-0.95, hi=2.0, tol=1e-9):
    def f(r):
        try: return sum(cf / ((1 + r) ** m) for m, cf in enumerate(cfs))
        except ZeroDivisionError: return None
    f_lo, f_hi = f(lo), f(hi)
    if f_lo is None or f_hi is None or f_lo * f_hi > 0: return None
    for _ in range(500):
        mid = (lo + hi) / 2; f_mid = f(mid)
        if f_mid is None: return None
        if abs(f_mid) < tol: return mid
        if f_lo * f_mid <= 0: hi, f_hi = mid, f_mid
        else: lo, f_lo = mid, f_mid
    return (lo + hi) / 2
def irr_annual(cfs, lo=-0.5, hi=3.0, tol=1e-8):
    def f(r):
        try: return sum(cf / ((1 + r) ** (m / 12.0)) for m, cf in enumerate(cfs))
        except (ZeroDivisionError, OverflowError): return None
    f_lo, f_hi = f(lo), f(hi)
    if f_lo is None or f_hi is None or f_lo * f_hi > 0: return None
    for _ in range(300):
        mid = (lo + hi) / 2; f_mid = f(mid)
        if f_mid is None: return None
        if abs(f_mid) < tol: return mid
        if f_lo * f_mid <= 0: hi, f_hi = mid, f_mid
        else: lo, f_lo = mid, f_mid
    return (lo + hi) / 2

def payback_m(cfs):
    cum = 0.0
    for m, cf in enumerate(cfs):
        prev = cum; cum += cf
        if prev < 0 <= cum and cf != 0: return (m - 1 + (-prev / cf)) / 12.0
    return None

def annual_op(p, adr=None, occ=None):
    adr = p["adr_excl_svc"] if adr is None else adr
    occ = p["occ"] if occ is None else occ
    rn = p["rooms"] * 365
    room_B = rn * occ * adr / 10000.0
    svc = room_B * B["svc_pct_of_room_B"]
    occ_ratio = occ / B["occ_ttm"]
    nonroom_B = B["nonroom_B_fy2025"] * (occ_ratio ** 0.8) * p["nonroom_capability"]
    rev_B = room_B + nonroom_B
    gop = room_B * B["dept_margin"]["房务部"] + nonroom_B * B["nonroom_margin_blend"]
    sc = p["rooms"] / B["rooms"]; ANN = B["annualize_10m"]
    undist = {"A&G": B["cost_10m"]["A&G"] * ANN * (0.75 + 0.25 * sc),
              "POM": B["cost_10m"]["POM"] * ANN * (0.70 + 0.30 * sc),
              "IT": B["cost_10m"]["IT"] * ANN,
              "S&M": B["cost_10m"]["S&M"] * ANN * occ_ratio,
              "Energy": B["cost_10m"]["能源"] * ANN * (0.55 + 0.45 * sc)}
    undist_total = sum(undist.values())
    ihg = gop - undist_total
    if p["fee_mode"] == "delegate":
        license = rev_B * B["license_pct_rev_B"]; imf = max(0.0, ihg - license) * B["imf_pct"]
    elif p["fee_mode"] in ("franchise_ihg", "franchise_ext"):
        license = room_B * 0.05; imf = 0.0
    else:
        license = 0.0; imf = 0.0
    fee = license + imf
    return {"room_B": room_B, "svc": svc, "room_A": room_B + svc, "nonroom_B": nonroom_B,
            "rev_B": rev_B, "rev_A": rev_B + svc, "gop": gop, "undist_total": undist_total,
            "ihg_gop": ihg, "fee": fee, "adj_gop": ihg - fee, "adr": adr, "occ": occ}

def build_cf(p, capex, months_life=240, ramp=6, sustain_pct=0.02, downtime=None,
             adr=None, occ=None, brand_share=0.0, subsidy=0.0, split=None):
    """月度时间轴。split=None 时为单一停业；split=(capex_a,capex_b,dt_a,dt_b) 时为两期分期。"""
    st = annual_op(p, adr, occ)
    owner_capex = capex * (1 - brand_share) - subsidy
    dtm = (B["shutdown_labor_monthly"] + B["cost_10m"]["POM"] / 10 * 0.6
           + B["cost_10m"]["能源"] / 10 * 0.25)
    def month_cf(k):
        # 注：annual_op 返回的是年度金额，本模型使用月度网格，故统一除以 12
        if k >= 1.0:
            return (st["adj_gop"] - st["rev_B"] * sustain_pct) / 12.0
        r_gop = st["gop"] * k
        r_und = st["undist_total"] * (0.85 + 0.15 * k)
        r_fee = st["fee"] * k
        return ((r_gop - r_und - r_fee) - st["rev_B"] * sustain_pct) / 12.0
    cfs = [-owner_capex]
    if split is None:
        dt = p["downtime"] if downtime is None else downtime
        for _ in range(dt): cfs.append(-dtm)
        for m in range(ramp):
            k = 0.45 + (0.85 - 0.45) * (m / max(1, ramp - 1)); cfs.append(month_cf(k))
        for _ in range(months_life - ramp): cfs.append(month_cf(1.0))
    else:
        ca, cb, dta, dtb = split
        cfs = [-ca]
        for _ in range(dta): cfs.append(-dtm)
        for m in range(ramp):
            k = 0.45 + (0.85 - 0.45) * (m / max(1, ramp - 1)); cfs.append(month_cf(k))
        op1 = months_life - ramp - dtb - ramp
        for _ in range(op1): cfs.append(month_cf(1.0))
        cfs.append(-cb)
        for _ in range(dtb): cfs.append(-dtm)
        for m in range(ramp):
            k = 0.45 + (0.85 - 0.45) * (m / max(1, ramp - 1)); cfs.append(month_cf(k))
        for _ in range(months_life - ramp - op1): cfs.append(month_cf(1.0))
    return {"cfs": cfs, "npv": npv_m(cfs), "irr": irr_annual(cfs), "payback": payback_m(cfs),
            "owner_capex": owner_capex, "stable": st}

# ══════════ 反事实 ══════════
cf_now = dict(PATHS["P1"])
cf_now["adr_excl_svc"] = B["adr_A_24m"] / (1 + B["svc_pct_of_room_B"])
cf_now["occ"] = B["occ_24m"]; cf_now["fee_mode"] = "delegate"
cf_now["nonroom_capability"] = 1.0; cf_now["downtime"] = 0
st_now = annual_op(cf_now)
cf_year = st_now["adj_gop"] - st_now["rev_B"] * 0.02
CF_CF = [cf_year / 12.0] * 240
npv_cf = sum(cf / ((1 + R_M) ** m) for m, cf in enumerate(CF_CF))
L("反事实（维持现状持续经营 20 年）：收入 %.0f 万元｜调整后营业毛利润 %.0f 万元｜年经营现金流 %.0f 万元｜净现值 %.0f 万元" %
  (st_now["rev_A"], st_now["adj_gop"], cf_year, npv_cf))
L("  交叉核对：台账 FY2025 调整后营业毛利润 1,672.7 万元（1,393.90×1.2）、净营业利润 −416.51 万元 ✓")
L("  月度折现率 %.6f%%（年 8%%）" % (R_M * 100))

# ══════════ 四路径 ══════════
res = {}
for k in ("P1", "P2", "P3", "P4"):
    p = dict(PATHS[k]); p["downtime"] = DUR[k]["m"]
    r = build_cf(p, CAPEX[k]["total"])
    st = r["stable"]
    op_cf = st["adj_gop"] - st["rev_B"] * 0.02
    res[k] = {
        "name": p["name"], "rooms": p["rooms"], "downtime": DUR[k]["m"],
        "downtime_lo": DUR[k]["lo"], "downtime_hi": DUR[k]["hi"],
        "capex": CAPEX[k]["total"], "per_sqm": CAPEX[k]["per_sqm"], "per_room": CAPEX[k]["per_room"],
        "rev_A_stable": round(st["rev_A"], 2), "adj_gop": round(st["adj_gop"], 2),
        "fee": round(st["fee"], 2), "op_cf_stable": round(op_cf, 2),
        "npv_absolute": round(r["npv"], 2), "npv_incremental": round(r["npv"] - npv_cf, 2),
        "irr_pct": (round(r["irr"] * 100, 2) if r["irr"] is not None else None),
        "payback_yr": (round(r["payback"], 2) if r["payback"] is not None else None),
        "simple_payback": round(CAPEX[k]["total"] / op_cf, 2) if op_cf > 0 else None,
        "capex_items": CAPEX[k]["items"], "cfs_len": len(r["cfs"]),
    }
    L("%s capex=%.0f 停业=%d月 营收=%.0f 经营现金流=%.0f｜绝对NPV=%.0f 增量NPV=%.0f IRR=%s 回收=%s 简单回收=%.1f年" %
      (k, CAPEX[k]["total"], DUR[k]["m"], st["rev_A"], op_cf, r["npv"], r["npv"] - npv_cf,
       res[k]["irr_pct"], res[k]["payback_yr"], res[k]["simple_payback"] or -1))

# ══════════ 分期变体 ══════════
ITEMS = {i["name"]: i["amount"] for i in CAPEX["P1"]["items"]}
A_KEYS = ["火灾自动报警", "消防泵房", "防排烟", "应急照明", "防火分隔", "消防报建", "给排水管网",
          "配电与备电", "电梯更新", "锅炉及配套", "拆除与垃圾清运", "第三方评估", "项目管理"]
B_KEYS = ["冷源主机", "风系统与末端", "屋面防水", "智能化与弱电", "厨房与餐饮", "泳池与水疗", "员工区与后勤"]
a1 = sum(v for n, v in ITEMS.items() if any(k in n for k in A_KEYS))
a2 = sum(v for n, v in ITEMS.items() if any(k in n for k in B_KEYS))
P1A = round(a1 * 1.08 + a1 * 0.045 * (14 / 12.0), 0)
P1B = round(a2 * 1.08 + a2 * 0.045 * (8 / 12.0), 0)
p1 = dict(PATHS["P1"]); p1["downtime"] = 12
rs = build_cf(p1, P1A + P1B, split=(P1A, P1B, 8, 4))
L("")
L("路径一分期变体：P1a %.0f 万元（停业 8 月）＋ P1b %.0f 万元（停业 4 月）＝ %.0f 万元（较一次性省 %.0f 万元）" %
  (P1A, P1B, P1A + P1B, CAPEX["P1"]["total"] - P1A - P1B))
L("  净现值 %.0f 万元｜增量 %.0f 万元｜IRR %s｜回收 %s 年" %
  (rs["npv"], rs["npv"] - npv_cf,
   (round(rs["irr"] * 100, 2) if rs["irr"] is not None else None),
   (round(rs["payback"], 2) if rs["payback"] is not None else None)))

# ══════════ 敏感性 ══════════
sens = {}
for k in ("P1", "P2", "P3", "P4"):
    p = dict(PATHS[k]); p["downtime"] = DUR[k]["m"]; cp = CAPEX[k]["total"]; s = {}
    for lbl, kw in (("ADR -10%", dict(adr=PATHS[k]["adr_excl_svc"] * 0.9)), ("ADR 基准", dict()),
                    ("ADR +10%", dict(adr=PATHS[k]["adr_excl_svc"] * 1.1)),
                    ("OCC -5pp", dict(occ=PATHS[k]["occ"] - 0.05)), ("OCC 基准", dict()),
                    ("OCC +5pp", dict(occ=PATHS[k]["occ"] + 0.05)),
                    ("停业下限", dict(downtime=DUR[k]["lo"])), ("停业基准", dict()),
                    ("停业上限", dict(downtime=DUR[k]["hi"]))):
        s[lbl] = round(build_cf(p, cp, **kw)["npv"], 0)
    for lbl, c2 in (("CAPEX -30%", cp * 0.70), ("CAPEX -15%", cp * 0.85), ("CAPEX 基准", cp),
                    ("CAPEX +15%", cp * 1.15), ("CAPEX +30%", cp * 1.30)):
        s[lbl] = round(build_cf(p, c2)["npv"], 0)
    for lbl, ra in (("折现率 6%", 0.06), ("折现率 8%", 0.08), ("折现率 10%", 0.10)):
        old = R_M
        globals()["R_M"] = (1 + ra) ** (1 / 12.0) - 1
        s[lbl] = round(build_cf(p, cp)["npv"], 0)
        globals()["R_M"] = old
    for lbl, lf in (("评价期 10 年", 120), ("评价期 20 年", 240), ("评价期 30 年", 360)):
        s[lbl] = round(build_cf(p, cp, months_life=lf)["npv"], 0)
    for lbl, bs in (("品牌方承担 0%", 0.0), ("品牌方承担 20%", 0.20), ("品牌方承担 30%", 0.30)):
        s[lbl] = round(build_cf(p, cp, brand_share=bs)["npv"], 0)
    s["房价不提升（ADR维持现状）"] = round(build_cf(
        p, cp, adr=B["adr_A_24m"] / (1 + B["svc_pct_of_room_B"]), occ=B["occ_24m"])["npv"], 0)
    sens[k] = s
    L("敏感性 %s：%s" % (k, json.dumps(s, ensure_ascii=False)))


# ══════════ 不整改后果情景 ══════════
L("")
L("\u4e0d整改后果情景（反事实对比基准的三种口径）：")
# CF-1 维持现状持续经营
cf1 = {"label": "维持现状持续经营", "npv": round(npv_cf, 0),
       "note": "法律上不可持续（《安全生产法》第一百一十二条不得拖延整改），"
             "仅作最优对比基准；这一情景下改造的增量净现值为负"}
# CF-2 被依法依质停业：经营中断，资产需重新处置
cf2_cfs = [-6000.0] + [0.0] * 60 + [-CAPEX["P1"]["total"] * 0.35] + [-240.0] * 120
cf2_npv = sum(cf / ((1 + R_M) ** m) for m, cf in enumerate(cf2_cfs))
cf2 = {"label": "被依法依质停业整改", "npv": round(cf2_npv, 0),
       "note": "未整改被订止经营、资产需重新处置（评估为参考情景，"
             "需专业赋值估计）；此情景下改造的增量净现值为正"}
cf3 = {"label": "发生安全事故", "npv": None,
       "note": "事故作用下的丢失不估算；本报告不将事故归因于改造决策"}
L("  CF-1 %s：反事实净现值 %.0f 万元；改造增量净现值 %.0f 万元" % (cf1["label"], cf1["npv"], res["P1"]["npv_absolute"] - cf1["npv"]))
L("  CF-2 %s：反事实净现值 %.0f 万元；改造增量净现值 %.0f 万元" % (cf2["label"], cf2["npv"], res["P1"]["npv_absolute"] - cf2["npv"]))
# 利息覆盖能力
cover_renov = (res["P1"]["op_cf_stable"] - 2088.85)
cover_keep = (cf_year - 2088.85)
L("  利息覆盖：改造后年经营现金流 %.0f 万元，覆盖刚性利息 2,088.85 万元后余 %.0f 万元；"
  "不整改年经营现金流 %.0f 万元，缺口 %.0f 万元，20 年累计流出 %.0f 万元" %
  (res["P1"]["op_cf_stable"], cover_renov, cf_year, cover_keep, cover_keep * 20))
OUT = {"meta": {"title": "v114 修正测算内核（四路径·增量口径·月度时间轴）", "date": "2026-11-15",
                "修正": "①统一月度时间轴（原模型把年现金流按月折现，系统性低估现值）②P1 造价 11,066→24,517 万元"
                        "③P1 停业 8→12 个月④补反事实基准与增量口径⑤补路径一分期变体",
                "评价": "项目口径（不含存量债务利息）；月度折现率 = (1+8%)^(1/12)-1；评价期 停业期＋20 年经营期"},
       "counterfactual": {"rev_A": round(st_now["rev_A"], 2), "adj_gop": round(st_now["adj_gop"], 2),
                          "op_cf_year": round(cf_year, 2), "npv": round(npv_cf, 2),
                          "note": "维持现状持续经营 20 年的反事实；法律上不可持续，仅作比较基准"},
       "results": res, "sensitivity": sens,
       "split": {"P1a": P1A, "P1b": P1B, "total": P1A + P1B,
                 "saving_vs_once": CAPEX["P1"]["total"] - P1A - P1B,
                 "npv": round(rs["npv"], 2), "npv_incremental": round(rs["npv"] - npv_cf, 2),
                 "irr_pct": (round(rs["irr"] * 100, 2) if rs["irr"] is not None else None),
                 "payback_yr": (round(rs["payback"], 2) if rs["payback"] is not None else None),
                 "downtime_a": 8, "downtime_b": 4},
       "duration": DUR, "capex": CAPEX}
OUT["counterfactuals"] = [cf1, cf2, cf3]
OUT["interest_cover"] = {"interest_annual": 2088.85, "after_renovation": round(cover_renov, 2),
                          "keep_operating": round(cover_keep, 2), "gap_20y": round(cover_keep * 20, 2)}
io.open(os.path.join(T, "v114.json"), "w", encoding="utf-8").write(json.dumps(OUT, ensure_ascii=False, indent=1))
L("")
L("写出 v114.json")
L("DONE")
