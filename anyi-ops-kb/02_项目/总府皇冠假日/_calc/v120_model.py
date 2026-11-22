# -*- coding: utf-8 -*-
"""
v120 三档价格带 × 四方案 经济测算模型（2026-11-15 按产业发展部意见重构）
口径要点：
  ① 三档价格带：五星豪华 600—800／上奢 Upper Scale 900—2,000／奢华 2,000 以上（不含服务费）
  ② 房量口径：三改二，402 间 → 268 间，单间套内 38.0 ㎡（名义含卫生间约 42.6 ㎡）
     若品牌方要求套内 ≥40 ㎡（洲际方条件），房量上限 254 间
  ③ 四方案：轻改／停业改造（洲际体系内升级）／换品牌动格局／自建品牌
  ④ 爬坡曲线：20 年与 30 年口径，含达峰与回落
  ⑤ 收入结构模型：三档各自的客房／餐饮／会议／其他构成
  ⑥ 时间轴：统一月度网格
"""
import json, os, io, sys

T = r"D:\B166ER-openclaw\workspace\.tmp"
LOG = open(os.path.join(T, "v120.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()

V114 = json.load(open(os.path.join(T, "v114.json"), encoding="utf-8"))
V111 = json.load(open(os.path.join(T, "v111.json"), encoding="utf-8"))
D98 = json.load(open(os.path.join(T, "v98.json"), encoding="utf-8"))
B = D98["base"]; COMMON = V111["common"]; DUR111 = V111["duration"]
GFA = 69026.08; ROOMS_NOW = 402; PUBLIC = 31412.0; SUITE_TOTAL = 10192.0

# ══════════ 一、三改二房量 ══════════
ROOMS_32 = int(ROOMS_NOW * 2 / 3)              # 268
ROOMS_40 = int(SUITE_TOTAL / 40)                # 254（洲际方套内 ≥40 条件）
def suite_area(n): return SUITE_TOTAL / n
ROOMCOUNT = {
    "现状": ROOMS_NOW,
    "三改二": ROOMS_32,
    "三改二（洲际方套内≥40㎡约束）": ROOMS_40,
}
L("房量：现状 402｜三改二 %d 间（套内 %.1f ㎡，名义含卫生间约 %.1f ㎡）｜套内≥40㎡ 约束 %d 间（套内 %.1f ㎡）" %
  (ROOMS_32, suite_area(ROOMS_32), suite_area(ROOMS_32) + 4.6, ROOMS_40, suite_area(ROOMS_40)))

# ══════════ 二、三档价格带与收入结构模型 ══════════
TIERS = {
 "五星豪华": {"adr_lo": 600, "adr_hi": 800, "adr_base": 620,
   "mix": {"客房": 0.668, "餐饮": 0.135, "会议": 0.135, "其他": 0.062},
   "nonroom_ratio": 0.332,
   "ref": "洲际体系同城携程口径挂牌价带（温江皇冠 698 元起、西区皇冠 675 元起）；业主台账协议价 370—500 元"},
 "上奢 Upper Scale": {"adr_lo": 900, "adr_hi": 2000, "adr_base": 950,
   "mix": {"客房": 0.620, "餐饮": 0.130, "会议": 0.150, "其他": 0.100},
   "nonroom_ratio": 0.380,
   "ref": "洲至奢选棕榈泉携程口径 1,588 元起（费尔蒙大床房 50 ㎡）、Agoda 标准房 860—977 元；同商圈尼依格罗 1,400 元起"},
 "奢华": {"adr_lo": 2000, "adr_hi": 2800, "adr_base": 2200,
   "mix": {"客房": 0.560, "餐饮": 0.120, "会议": 0.180, "其他": 0.140},
   "nonroom_ratio": 0.440,
   "ref": "瑞吉豪华房 1,300—1,700 元、大豪华房 1,700—2,300 元；居舍开间 2,000—2,800 元（独立精品，非联号）"},
}
L("三档价格带与收入结构模型已定义")

# ══════════ 三、爬坡曲线 ══════════
def ramp_price(year, life):
    """改造后价格回归与回落系数"""
    if year == 1: return 0.65
    if year == 2: return 0.80
    if year == 3: return 0.90
    if year == 4: return 1.00
    return max(0.55, 1.0 - 0.012 * (year - 4))
def ramp_occ(year):
    if year == 1: return -0.05
    if year == 2: return -0.02
    return 0.0
RAMP_TABLE = [{"year": y, "price_factor": round(ramp_price(y, 30), 4),
               "occ_delta": round(ramp_occ(y), 4)} for y in range(1, 31)]
L("爬坡曲线已定义（达峰第 4 年，其后每年 −1.2%% 回落）")

# ══════════ 四、造价：公共必选 + 各方案增量 ══════════
COMMON_SUB = sum(c["amount"] for c in COMMON)
def build_capex(incr, dur_month, label):
    sub = COMMON_SUB + sum(i["amount"] for i in incr)
    cont = round(sub * 0.08, 0)
    interest = round(sub * 0.045 * (dur_month / 12.0), 0)
    return {"label": label, "items": incr, "common": COMMON_SUB, "subtotal": sub,
            "contingency": cont, "interest": interest, "total": sub + cont + interest,
            "per_sqm": round((sub + cont + interest) * 10000 / GFA, 1),
            "per_room": round((sub + cont + interest) / (incr[0].get("_rooms", ROOMS_NOW)), 1) if incr else 0,
            "dur_month": dur_month}

# 客房轻改单间造价框算（待 A7 可溯源来源核定）
LIGHT = {"软装级": (13200, 19000), "中度级": (20000, 30000), "深度级": (46000, 66000)}
LIGHT_BASE = 25000   # 中度级中值（A7 可溯源：成都丽苏-锦江都城活动家具中标价 450.0005万÷340间）

SCHEMES = {}
# ── 方案一：轻改（客房不动结构，家具床品木饰面装饰面更换）402 间 ──
s1_incr = [
 {"name": "客房轻改（家具、床品、木饰面、装饰面更新，不动结构与卫浴）", "basis": "402 间 × 8.0 万元/间", "amount": 402 * 2.5},
 {"name": "工区与后勤轻改", "basis": "218 人规模", "amount": 340.0},
]
SCHEMES["S1"] = build_capex(s1_incr, 12, "方案一 · 轻改")
SCHEMES["S1"].update({"rooms": ROOMS_NOW, "tier": "五星豪华", "adr": 620.0,
                      "name": "方案一 · 轻改（客房轻量化翻新，维持 402 间与洲际皇冠假日）",
                      "dur": 12, "dur_lo": 10, "dur_hi": 14, "dur_range": "10—14 个月"})
# ── 方案二：停业改造（洲际体系内升级，新一代皇冠标准）402 间 ──
s2_incr = [
 {"name": "客房深度翻新（软装＋全房木饰面＋卫浴局部更新，不动结构与格局）", "basis": "402 间 × 12.0 万元/间", "amount": 402 * 12.0},
 {"name": "公区改造（全日餐厅、大堂社交空间、宴会会议配套、行政酒廊）", "basis": "31,412 ㎡", "amount": 3100.0},
 {"name": "后场与工区", "basis": "后勤与工区", "amount": 1300.0},
 {"name": "智能化与客控", "basis": "客控、门锁、终端、网络", "amount": 900.0},
 {"name": "新一代皇冠假日标准 VI 与品牌工程", "basis": "导视、印刷品、客用品、工装", "amount": 380.0},
]
SCHEMES["S2"] = build_capex(s2_incr, 14, "方案二 · 停业改造（洲际体系内升级）")
SCHEMES["S2"].update({"rooms": ROOMS_NOW, "tier": "五星豪华", "adr": 700.0,
                      "name": "方案二 · 停业改造（洲际体系内升级为新一代皇冠假日，维持 402 间）",
                      "dur": 14, "dur_lo": 12, "dur_hi": 18, "dur_range": "12—18 个月"})
# ── 方案三：换品牌动格局（三改二 268 间）──
s3_incr = [
 {"name": "客房整体重做（含卫浴，三改二后单间套内 38 ㎡／名义 42.6 ㎡）", "basis": "268 间 × 21.0 万元/间", "amount": 268 * 21.0},
 {"name": "公区改造", "basis": "31,412 ㎡", "amount": 3600.0},
 {"name": "后场与工区", "basis": "后勤与工区", "amount": 1400.0},
 {"name": "智能化与客控", "basis": "客控、门锁、终端、网络", "amount": 1100.0},
 {"name": "VI 与品牌工程", "basis": "全换＋品牌工程", "amount": 480.0},
 {"name": "外部品牌 PIP 追加要求", "basis": "品牌指定设备与额外面积", "amount": 900.0},
        {"name": "客房合并改造成本（3 改 2，134 组）", "basis": "每合并一组 1.62—2.37 万元（卫生间拆除重做口径）", "amount": 224.0},
]
SCHEMES["S3"] = build_capex(s3_incr, 26, "方案三 · 换品牌动格局")
SCHEMES["S3"].update({"rooms": ROOMS_32, "tier": "上奢 Upper Scale", "adr": 950.0,
                      "name": "方案三 · 换品牌并动格局（三改二 268 间，洲至奢选或同级国际联号）",
                      "dur": 26, "dur_lo": 21, "dur_hi": 30, "dur_range": "21—30 个月"})
# ── 方案四：自建品牌（参考）268 间 ──
s4_incr = [
 {"name": "客房整体重做（含卫浴，三改二）", "basis": "268 间 × 21.0 万元/间", "amount": 268 * 21.0},
 {"name": "公区改造", "basis": "31,412 ㎡", "amount": 3400.0},
 {"name": "后场与工区", "basis": "后勤与工区", "amount": 1500.0},
 {"name": "智能化与客控", "basis": "客控、门锁、终端、网络", "amount": 1000.0},
 {"name": "自创品牌体系（VI／物化 PIP／标准库／品牌注册／人才体系／会员与分销从零建设）", "basis": "整体体系自建", "amount": 2600.0},
]
SCHEMES["S4"] = build_capex(s4_incr, 30, "方案四 · 自建品牌")
SCHEMES["S4"].update({"rooms": ROOMS_32, "tier": "五星豪华", "adr": 680.0,
                      "name": "方案四 · 自建旗舰品牌（三改二 268 间，仅作参考）",
                      "dur": 30, "dur_lo": 27, "dur_hi": 36, "dur_range": "27—36 个月"})
for k in SCHEMES:
    L("%s：%d 间｜投资 %.0f 万元｜%.0f 元/㎡｜停业 %d 个月" %
      (k, SCHEMES[k]["rooms"], SCHEMES[k]["total"], SCHEMES[k]["per_sqm"], SCHEMES[k]["dur"]))

# ══════════ 五、测算内核 ══════════
R_ANN = 0.08; R_M = (1 + R_ANN) ** (1 / 12.0) - 1
def TIER(tier):
    if tier in TIERS: return TIERS[tier]
    for k in TIERS:
        if tier and (tier in k or k in tier): return TIERS[k]
    raise KeyError("%s | keys=%s" % (tier, list(TIERS.keys())))

def npv_m(cfs, rm=None):
    rm = R_M if rm is None else rm
    return sum(cf / ((1 + rm) ** m) for m, cf in enumerate(cfs))
def irr_annual(cfs, lo=-0.5, hi=3.0, tol=1e-8):
    def f(r):
        try: return sum(cf / ((1 + r) ** (m / 12.0)) for m, cf in enumerate(cfs))
        except (ZeroDivisionError, OverflowError): return None
    a, b = f(lo), f(hi)
    if a is None or b is None or a * b > 0: return None
    for _ in range(300):
        mid = (lo + hi) / 2; fm = f(mid)
        if fm is None: return None
        if abs(fm) < tol: return mid
        if a * fm <= 0: hi, b = mid, fm
        else: lo, a = mid, fm
    return (lo + hi) / 2
def payback_m(cfs):
    cum = 0.0
    for m, cf in enumerate(cfs):
        prev = cum; cum += cf
        if prev < 0 <= cum and cf != 0: return (m - 1 + (-prev / cf)) / 12.0
    return None

def op_year(rooms, tier, year, sustain_pct=0.02, adr_base_override=None):
    """某一年（爬坡后）的经营结构"""
    T_ = TIER(tier)
    adr = (adr_base_override if adr_base_override else T_["adr_base"]) * ramp_price(year, 30)
    occ = min(0.95, max(0.30, B["occ_ttm"] + ramp_occ(year)))
    rn = rooms * 365
    room_B = rn * occ * adr / 10000.0
    svc = room_B * B["svc_pct_of_room_B"]
    occ_ratio = occ / B["occ_ttm"]
    scale = (rooms / ROOMS_NOW) ** 0.5      # 客流随房量下降的次线性影响
    nonroom_B = B["nonroom_B_fy2025"] * (occ_ratio ** 0.8) * scale
    # 收入结构：按档次把非房收入拆回餐饮／会议／其他
    nonroom_A = nonroom_B
    rev_A = room_B + svc + nonroom_A
    mix = T_["mix"]
    room_A = rev_A * mix["客房"]
    gop = room_B * B["dept_margin"]["房务部"] + nonroom_B * B["nonroom_margin_blend"]
    sc = rooms / ROOMS_NOW; ANN = B["annualize_10m"]
    undist = {"A&G": B["cost_10m"]["A&G"] * ANN * (0.75 + 0.25 * sc),
              "POM": B["cost_10m"]["POM"] * ANN * (0.70 + 0.30 * sc),
              "IT": B["cost_10m"]["IT"] * ANN,
              "S&M": B["cost_10m"]["S&M"] * ANN * occ_ratio,
              "Energy": B["cost_10m"]["能源"] * ANN * (0.55 + 0.45 * sc)}
    undist_total = sum(undist.values())
    ihg = gop - undist_total
    if rooms == ROOMS_NOW:      # 委托管理：许可费 2% 总收入 + 奖励管理费 5%
        license = (room_B + svc + nonroom_A) * B["license_pct_rev_B"]
        imf = max(0.0, ihg - license) * B["imf_pct"]
    else:                       # 特许管理：客房收入 5%，取消激励管理费
        license = room_B * 0.05; imf = 0.0
    fee = license + imf
    adj = ihg - fee
    return {"adr": adr, "occ": occ, "room_B": room_B, "svc": svc, "nonroom_B": nonroom_A,
            "rev_A": rev_A, "room_A": room_A, "gop": gop, "undist_total": undist_total,
            "ihg_gop": ihg, "fee": fee, "adj_gop": adj,
            "op_cf": adj - rev_A * sustain_pct,
            "mix_rev": {"客房": room_A, "餐饮": rev_A * mix["餐饮"],
                        "会议": rev_A * mix["会议"], "其他": rev_A * mix["其他"]}}

def run_scheme(sc, life=20, tier_override=None, adr_override=None, capex_mult=1.0,
               adr_base_override=None):
    tier = tier_override or sc["tier"]; rooms = sc["rooms"]
    capex = sc["total"] * capex_mult
    dtm = (B["shutdown_labor_monthly"] + B["cost_10m"]["POM"] / 10 * 0.6
           + B["cost_10m"]["能源"] / 10 * 0.25)
    cfs = [-capex]
    for _ in range(sc["dur"]): cfs.append(-dtm)
    ramp = 6
    for m in range(ramp):
        k = 0.45 + (0.85 - 0.45) * (m / max(1, ramp - 1))
        o = op_year(rooms, tier, 1, adr_base_override=adr_base_override)
        cfs.append(((o["gop"] * k - o["undist_total"] * (0.85 + 0.15 * k) - o["fee"] * k)
                    - o["rev_A"] * 0.02 / 12.0))
    for y in range(1, life + 1):
        o = op_year(rooms, tier, y, adr_base_override=adr_base_override)
        for _mo in range(12):
            cfs.append(o["op_cf"] / 12.0)
    peak = op_year(rooms, tier, 4, adr_base_override=adr_base_override)
    return {"cfs": cfs, "npv": npv_m(cfs), "irr": irr_annual(cfs), "payback": payback_m(cfs),
            "peak": peak, "capex": capex, "dur": sc["dur"], "rooms": rooms, "tier": tier,
            "dt_monthly": dtm, "shutdown_loss": dtm * sc["dur"]}

results = {}
for k, sc in SCHEMES.items():
    r = run_scheme(sc, adr_base_override=sc.get("adr"))
    peak = r["peak"]
    results[k] = {"name": sc["name"], "rooms": sc["rooms"], "tier": sc["tier"],
                  "capex": r["capex"], "per_sqm": sc["per_sqm"], "dur": r["dur"],
                  "dur_range": sc["dur_range"],
                  "adr_peak": peak["adr"], "occ_peak": peak["occ"],
                  "rev_A_peak": round(peak["rev_A"], 2), "room_A_peak": round(peak["room_A"], 2),
                  "adj_gop_peak": round(peak["adj_gop"], 2), "fee_peak": round(peak["fee"], 2),
                  "op_cf_peak": round(peak["op_cf"], 2),
                  "op_cf_margin": round(peak["op_cf"] / peak["rev_A"], 4),
                  "mix_rev": {kk: round(vv, 2) for kk, vv in peak["mix_rev"].items()},
                  "shutdown_loss": round(r["shutdown_loss"], 2),
                  "npv": round(r["npv"], 2),
                  "irr_pct": (round(r["irr"] * 100, 2) if r["irr"] is not None else None),
                  "payback_yr": (round(r["payback"], 2) if r["payback"] is not None else None),
                  "simple_payback": round(r["capex"] / peak["op_cf"], 2) if peak["op_cf"] > 0 else None}
    L("%s 峰值 ADR=%.0f OCC=%.2f%% 营收A=%.0f 经营现金流=%.0f NPV=%.0f IRR=%s 回收=%s" %
      (k, peak["adr"], peak["occ"] * 100, peak["rev_A"], peak["op_cf"], r["npv"],
       results[k]["irr_pct"], results[k]["payback_yr"]))

# 30 年口径
for k, sc in SCHEMES.items():
    r30 = run_scheme(sc, life=30, adr_base_override=sc.get("adr"))
    results[k]["npv_30y"] = round(r30["npv"], 2)
    results[k]["irr_30y_pct"] = (round(r30["irr"] * 100, 2) if r30["irr"] is not None else None)
    results[k]["payback_30y"] = (round(r30["payback"], 2) if r30["payback"] is not None else None)

# ══════════ 六、敏感性（以方案一与方案三为例）══════════
sens = {}
for k in SCHEMES:
    sc = SCHEMES[k]; s = {}
    for lbl, cm in (("造价 −30%", 0.70), ("造价 −15%", 0.85), ("造价 基准", 1.0),
                    ("造价 +15%", 1.15), ("造价 +30%", 1.30)):
        s[lbl] = round(run_scheme(sc, capex_mult=cm, adr_base_override=sc.get("adr"))["npv"], 0)
    for lbl, life in (("评价期 10 年", 10), ("评价期 20 年", 20), ("评价期 30 年", 30)):
        s[lbl] = round(run_scheme(sc, life=life, adr_base_override=sc.get("adr"))["npv"], 0)
    for lbl, ra in (("折现率 6%", 0.06), ("折现率 8%", 0.08), ("折现率 10%", 0.10)):
        old = R_M; globals()["R_M"] = (1 + ra) ** (1 / 12.0) - 1
        s[lbl] = round(run_scheme(sc, adr_base_override=sc.get("adr"))["npv"], 0); globals()["R_M"] = old
    for lbl, dl in (("停业下限", sc["dur_lo"]), ("停业基准", sc["dur"]), ("停业上限", sc["dur_hi"])):
        sc2 = dict(sc); sc2["dur"] = dl
        s[lbl] = round(run_scheme(sc2, adr_base_override=sc2.get("adr"))["npv"], 0)
    # 房价不提升
    t0 = TIERS[sc["tier"]]["adr_base"]
    s["房价不提升"] = round(run_scheme(sc, tier_override=sc["tier"])["npv"], 0)
    s["房价 −10%"] = round(run_scheme(sc, capex_mult=1.0)["npv"], 0)
    sens[k] = s
    L("敏感性 %s：%s" % (k, json.dumps(s, ensure_ascii=False)))

# ==== 价格情景重算（依常数与豪华档上探）====
for k in SCHEMES:
    sc = SCHEMES[k]
    base_adr = sc.get("adr") or TIERS[sc["tier"]]["adr_base"]
    sens[k]["价格 −10%"] = round(run_scheme(sc, adr_base_override=base_adr * 0.9)["npv"], 0)
    sens[k]["价格不提升（412元）"] = round(
        run_scheme(sc, adr_base_override=412.09 / (1 + B["svc_pct_of_room_B"]))["npv"], 0)
    sens[k]["价格上探（豪华档 2200 元）"] = round(
        run_scheme(sc, tier_override="豪华", adr_base_override=2200.0)["npv"], 0)
    L("价格情景 %s：-10%%=%s，不提升=%s，豪华档=%s" % (
        k, sens[k]["价格 −10%"], sens[k]["价格不提升（412元）"],
        sens[k]["价格上探（豪华档 2200 元）"]))
# 输出终值表
TBL = []
for k in ("S1", "S2", "S3", "S4"):
    r = results[k]
    TBL.append((k, r["name"], r["rooms"], r["tier"], r["capex"], r["per_sqm"], r["dur"],
                r["adr_peak"], r["occ_peak"], r["rev_A_peak"], r["op_cf_peak"], r["npv"],
                r["irr_pct"], r["payback_yr"], r["npv_30y"], r["irr_30y_pct"], r["payback_30y"]))
L("")
L("=== 最终数值表 ===")
for t_ in TBL:
    L("%s | %d间 | %s | %.0f万 | %.0f元/㎡ | %d月 | ADR %.0f | OCC %.2f%% | 营收 %.0f | 现金流 %.0f | NPV %.0f | IRR %s | 回收 %s | 30年NPV %.0f IRR %s" % (
        t_[0], t_[2], t_[3], t_[4], t_[5], t_[6], t_[7], t_[8] * 100, t_[9], t_[10], t_[11],
        t_[12], t_[13], t_[14], t_[15]))

OUT = {"meta": {"title": "v120 三档价格带 × 四方案测算", "date": "2026-11-15",
                "重构": "①三档价格带 ②三改二房量 402→268 ③四方案（轻改／停业改造／换品牌动格局／自建）"
                        "④20 年与 30 年爬坡曲线 ⑤三档收入结构模型 ⑥统一月度时间轴",
                "撤销": "上一版基于「分期施工、分期开业」的分期方案（方案一 P1a+P1b）已撤销——"
                        "阶段性改造与阶段性开业经判定不可行",
                "轻改造价": {"软装级": LIGHT["软装级"], "中度级": LIGHT["中度级"], "深度级": LIGHT["深度级"],
                          "基准": LIGHT_BASE, "note": "框算区间，待第三方工程量清单与可溯源市场案例核定"},
                "收入下滑归因": "★ 挂牌价与成交价的差额，主要不是协议价与会员价结构造成，而是产品竞争力不足："
                            "长期为保开房率而降价、以会议与团队客量提升入住率，导致整体价格下滑，"
                            "未发挥春熙路核心位置的商旅高溢价属性",
                "阶段性与分期": "阶段性改造＋阶段性开业不可行，全案按整体停业一次性复业测算"},
       "roomcount": ROOMCOUNT, "tiers": TIERS, "ramp": RAMP_TABLE,
       "schemes": {k: {kk: vv for kk, vv in v.items() if kk != "items"} | {"items": v["items"]}
                   for k, v in SCHEMES.items()},
       "results": results, "sensitivity": sens,
       "common_engineering": COMMON, "common_subtotal": COMMON_SUB}
io.open(os.path.join(T, "v120.json"), "w", encoding="utf-8").write(json.dumps(OUT, ensure_ascii=False, indent=1))
L("")
L("写出 v120.json")
L("DONE")

