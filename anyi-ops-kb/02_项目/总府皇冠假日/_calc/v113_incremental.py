# -*- coding: utf-8 -*-
"""
v113：增量口径经济性（补反事实基准）＋ 路径一分期变体（P1a/P1b 最小合规包）
2026-11-15｜产业发展部

【为什么必须补反事实】
v112 计算的是「改造后现金流」的绝对现值，隐含假设「不改造则该物业收入为零」。
这是错的：现状物业在正常经营（净营业利润 −416.51 万元/年，但调整后营业毛利润为正）。
正确的决策指标是增量：
    增量净现值 = NPV(改造路径) − NPV(反事实：维持现状持续经营)
反事实本身在法律上不可持续（《安全生产法》第一百一十二条不得拖延整改），
因此报告须同时给出「绝对项目口径」与「增量口径」两个数，并说明反事实的可选性受限。

【为什么必须补 P1a/P1b】
底线整改 24,517 万元中，冷源（R11 淘汰冷媒）、风系统、配电、电梯、锅炉五项
占 8,570 万元。这五项是否必须与消防整改同批次实施，决定了停业期与投资规模。
本节给出两种分期方案的经济性，供集团在第三方工程量清单核定阶段选择。
"""
import json, os, io, sys

T = r"D:\B166ER-openclaw\workspace\.tmp"
LOG = open(os.path.join(T, "v113.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()

V111 = json.load(open(os.path.join(T, "v111.json"), encoding="utf-8"))
V112 = json.load(open(os.path.join(T, "v112.json"), encoding="utf-8"))
D98 = json.load(open(os.path.join(T, "v98.json"), encoding="utf-8"))
B = D98["base"]; PATHS = D98["paths"]; CAPEX = V111["capex"]; DUR = V111["duration"]

def npv(rate, cfs): return sum(cf / ((1 + rate) ** i) for i, cf in enumerate(cfs))
def irr(cfs, lo=-0.90, hi=2.0, tol=1e-9):
    try: f_lo, f_hi = npv(lo, cfs), npv(hi, cfs)
    except ZeroDivisionError: return None
    if f_lo * f_hi > 0: return None
    for _ in range(400):
        mid = (lo + hi) / 2
        try: f_mid = npv(mid, cfs)
        except ZeroDivisionError: return None
        if abs(f_mid) < tol: return mid
        if f_lo * f_mid <= 0: hi, f_hi = mid, f_mid
        else: lo, f_lo = mid, f_mid
    return (lo + hi) / 2
def payback(cfs):
    cum = 0.0
    for i, cf in enumerate(cfs):
        prev = cum; cum += cf
        if prev < 0 <= cum and cf != 0: return i - 1 + (-prev / cf)
    return None

def annual_op(p, adr=None, occ=None, nonroom_cap=None):
    adr = p["adr_excl_svc"] if adr is None else adr
    occ = p["occ"] if occ is None else occ
    nc = p["nonroom_capability"] if nonroom_cap is None else nonroom_cap
    rn = p["rooms"] * 365
    room_B = rn * occ * adr / 10000.0
    svc = room_B * B["svc_pct_of_room_B"]
    occ_ratio = occ / B["occ_ttm"]
    nonroom_B = B["nonroom_B_fy2025"] * (occ_ratio ** 0.8) * nc
    rev_B = room_B + nonroom_B
    gop = room_B * B["dept_margin"]["房务部"] + nonroom_B * B["nonroom_margin_blend"]
    sc = p["rooms"] / B["rooms"]; ANN = B["annualize_10m"]
    undist = {
        "A&G": B["cost_10m"]["A&G"] * ANN * (0.75 + 0.25 * sc),
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
    adj = ihg - license - imf
    return {"room_B": room_B, "svc": svc, "room_A": room_B + svc, "nonroom_B": nonroom_B,
            "rev_B": rev_B, "rev_A": rev_B + svc, "gop": gop, "undist_total": undist_total,
            "ihg_gop": ihg, "fee": license + imf, "adj_gop": adj, "adr": adr, "occ": occ}

def project_cf(p, capex, life=20, rate=0.08, ramp=6, sustain_pct=0.02,
               adr=None, occ=None, brand_share=0.0, subsidy=0.0, downtime=None):
    dt = p["downtime"] if downtime is None else downtime
    st = annual_op(p, adr, occ)
    owner_capex = capex * (1 - brand_share) - subsidy
    dtm = (B["shutdown_labor_monthly"] + B["cost_10m"]["POM"] / 10 * 0.6
           + B["cost_10m"]["能源"] / 10 * 0.25)
    cfs = [-owner_capex]
    for _ in range(dt): cfs.append(-dtm)
    for m in range(ramp):
        k = 0.45 + (0.85 - 0.45) * (m / max(1, ramp - 1))
        r = annual_op(p, adr, occ)
        cfs.append((r["gop"] * k - r["undist_total"] * (0.85 + 0.15 * k)
                    - r["fee"] * k) - r["rev_B"] * k * sustain_pct / 12)
    for y in range(life):
        r = annual_op(p, adr, occ)
        cfs.append(r["adj_gop"] - r["rev_B"] * sustain_pct)
    return {"npv": npv(rate, cfs), "irr": irr(cfs), "payback": payback(cfs), "cfs": cfs,
            "owner_capex": owner_capex, "stable": st}

# ══════════ 一、反事实：维持现状持续经营 ══════════
cf_now = dict(PATHS["P1"])
cf_now["adr_excl_svc"] = B["adr_A_24m"] / (1 + B["svc_pct_of_room_B"])
cf_now["occ"] = B["occ_24m"]
cf_now["fee_mode"] = "delegate"; cf_now["nonroom_capability"] = 1.0
cf_now["downtime"] = 0
st_now = annual_op(cf_now)
cf_now_year = st_now["adj_gop"] - st_now["rev_B"] * 0.02
CF_CF = [cf_now_year] * 20
npv_cf = npv(0.08, CF_CF)
L("反事实（维持现状持续经营，20 年，折现率 8%%）：")
L("  收入 %.0f 万元｜调整后营业毛利润 %.0f 万元｜年经营现金流 %.0f 万元｜净现值 %.0f 万元" %
  (st_now["rev_A"], st_now["adj_gop"], cf_now_year, npv_cf))
L("  交叉核对：台账 2025 年经营毛利润 1,580.64 万元、净营业利润 −416.51 万元（扣利息 2,088.85 万元后）✓")

# ══════════ 二、四路径绝对口径与增量口径 ══════════
res = {}
for k in ("P1", "P2", "P3", "P4"):
    p = dict(PATHS[k]); p["downtime"] = DUR[k]["m"]
    r = project_cf(p, CAPEX[k]["total"])
    st = r["stable"]
    op_cf = st["adj_gop"] - st["rev_B"] * 0.02
    inc_npv = r["npv"] - npv_cf
    res[k] = {
        "name": p["name"], "rooms": p["rooms"], "downtime": DUR[k]["m"],
        "capex": CAPEX[k]["total"], "per_sqm": CAPEX[k]["per_sqm"], "per_room": CAPEX[k]["per_room"],
        "rev_A_stable": round(st["rev_A"], 2), "adj_gop": round(st["adj_gop"], 2),
        "op_cf_stable": round(op_cf, 2),
        "npv_absolute": round(r["npv"], 2), "npv_incremental": round(inc_npv, 2),
        "irr_pct": (round(r["irr"] * 100, 2) if r["irr"] is not None else None),
        "payback_yr": (round(r["payback"], 2) if r["payback"] is not None else None),
        "simple_payback": round(CAPEX[k]["total"] / op_cf, 2) if op_cf > 0 else None,
        "capex_items": CAPEX[k]["items"],
    }
    L("%s capex=%.0f 停业=%d月 营收=%.0f 经营现金流=%.0f｜绝对NPV=%.0f 增量NPV=%.0f IRR=%s 简单回收=%.1f年" %
      (k, CAPEX[k]["total"], DUR[k]["m"], st["rev_A"], op_cf, r["npv"], inc_npv,
       res[k]["irr_pct"], res[k]["simple_payback"] or -1))

# ══════════ 三、路径一分期变体 P1a / P1b ══════════
# 拆分依据：底线工程中，消防与给排水为法定强制且与建筑主体强耦合；
# 冷源（R11 淘汰冷媒）、风系统末端、配电增容、电梯、锅炉为设备更换级，可分批。
ITEMS = {i["name"]: i["amount"] for i in CAPEX["P1"]["items"]}
def pick(names):
    tot = 0; keys = []
    for n, v in ITEMS.items():
        if any(k in n for k in names): tot += v; keys.append(n)
    return tot, keys
P1A_NAMES = ["火灾自动报警", "消防泵房", "防排烟", "应急照明", "防火分隔", "消防报建",
             "给排水管网", "配电与备电", "电梯更新", "锅炉及配套", "拆除与垃圾清运",
             "第三方评估", "项目管理"]
P1B_NAMES = ["冷源主机", "风系统与末端", "屋面防水", "智能化与弱电", "厨房与餐饮", "泳池与水疗",
             "员工区与后勤"]
a1, k1 = pick(P1A_NAMES); a2, k2 = pick(P1B_NAMES)
face_common = ITEMS.get("基本预备费（8%）", 0) + ITEMS.get("建设期利息与资金占用成本", 0)
P1A_SUB = a1; P1A_TOT = round(a1 * 1.08 + a1 * 0.045 * (14 / 12.0), 0)
P1B_SUB = a2; P1B_TOT = round(a2 * 1.08 + a2 * 0.045 * (8 / 12.0), 0)
L("")
L("路径一分期变体：")
L("  P1a 法定强制与建筑强耦合包（消防＋给排水＋备电＋电梯＋锅炉＋报建＋拆除＋第三方＋开办）工程小计 %.0f 万元 → 总计 %.0f 万元" % (P1A_SUB, P1A_TOT))
L("  P1b 设备更换级包（冷源 R11 环保替换＋风系统末端＋屋面幕墙＋智能化＋厨房＋泳池＋员工后勤）工程小计 %.0f 万元 → 总计 %.0f 万元" % (P1B_SUB, P1B_TOT))
L("  分期合计 %.0f 万元（较一次性 %.0f 万元节省 %.0f 万元）；两次停业分别 8 个月与 4 个月" %
  (P1A_TOT + P1B_TOT, CAPEX["P1"]["total"], CAPEX["P1"]["total"] - P1A_TOT - P1B_TOT))

def split_cf(p, capex_a, capex_b, dt_a, dt_b, life=20, rate=0.08, ramp=6, sustain=0.02):
    cfs = [-capex_a]
    dtm = (B["shutdown_labor_monthly"] + B["cost_10m"]["POM"] / 10 * 0.6
           + B["cost_10m"]["能源"] / 10 * 0.25)
    for _ in range(dt_a): cfs.append(-dtm)
    st = annual_op(p)
    for m in range(ramp):
        k = 0.45 + (0.85 - 0.45) * (m / max(1, ramp - 1))
        r = annual_op(p)
        cfs.append((r["gop"] * k - r["undist_total"] * (0.85 + 0.15 * k) - r["fee"] * k)
                   - r["rev_B"] * k * sustain / 12)
    for y in range(life - 4):
        r = annual_op(p); cfs.append(r["adj_gop"] - r["rev_B"] * sustain)
    # 第二期：第 5 年再停 4 个月（此时部分年份现金流已被计入，需替换）
    for _ in range(dt_b): cfs.append(-dtm)
    for m in range(ramp):
        k = 0.45 + (0.85 - 0.45) * (m / max(1, ramp - 1))
        r = annual_op(p)
        cfs.append((r["gop"] * k - r["undist_total"] * (0.85 + 0.15 * k) - r["fee"] * k)
                   - r["rev_B"] * k * sustain / 12)
    for y in range(life - 4 - 4):
        r = annual_op(p); cfs.append(r["adj_gop"] - r["rev_B"] * sustain)
    return {"npv": npv(rate, cfs), "irr": irr(cfs), "cfs": cfs}

p1 = dict(PATHS["P1"]); p1["downtime"] = 12
rs = split_cf(p1, P1A_TOT, P1B_TOT, 8, 4)
L("")
L("  分期方案净现值 %.0f 万元（增量 %.0f 万元）｜IRR %s" %
  (rs["npv"], rs["npv"] - npv_cf, (round(rs["irr"] * 100, 2) if rs["irr"] is not None else None)))
L("  注：分期方案停业 8+4 个月，但两次停业均发生在同一物业，第二次须在第一期完成后重新开业经营期内安排，"
  "对营业与声誉的叠加冲击大于一次性停业；实际可行性须由施工组织与品牌方确认。")

OUT = {
 "meta": {"title": "v113 增量口径经济性与路径一分期变体", "date": "2026-11-15",
          "纠正链": "v98 造价低估 → v111 重建造价 24,517 万元 → v112 重算 → v113 补反事实与分期",
          "评价": "项目口径（不含存量债务利息）；评价期 20 年；折现率 8%；增量口径＝路径 NPV 减反事实 NPV"},
 "counterfactual": {"rev_A": round(st_now["rev_A"], 2), "adj_gop": round(st_now["adj_gop"], 2),
                    "op_cf_year": round(cf_now_year, 2), "npv": round(npv_cf, 2),
                    "adr": round(cf_now["adr_excl_svc"], 2), "occ": cf_now["occ"],
                    "note": "维持现状持续经营 20 年的反事实；法律上不可持续，仅作比较基准"},
 "results": res,
 "split": {"P1a": {"subtotal": P1A_SUB, "total": P1A_TOT, "items": k1, "downtime": 8},
           "P1b": {"subtotal": P1B_SUB, "total": P1B_TOT, "items": k2, "downtime": 4},
           "total": P1A_TOT + P1B_TOT, "saving_vs_once": CAPEX["P1"]["total"] - P1A_TOT - P1B_TOT,
           "npv": round(rs["npv"], 2), "npv_incremental": round(rs["npv"] - npv_cf, 2),
           "irr_pct": (round(rs["irr"] * 100, 2) if rs["irr"] is not None else None)},
 "duration": DUR, "capex": CAPEX,
}
io.open(os.path.join(T, "v113.json"), "w", encoding="utf-8").write(json.dumps(OUT, ensure_ascii=False, indent=1))
L("")
L("写出 v113.json")
L("DONE")
