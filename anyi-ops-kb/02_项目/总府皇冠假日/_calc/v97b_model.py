# -*- coding: utf-8 -*-
"""
v97b 三路径经济测算模型（自下而上 · 部门级 · 单一数据源）
生成：2026-11-15｜产业发展部

【口径体系（已与 A3 台账、P&L 逐项对账验证）】
  口径B（利润表，不含服务费）：总收入 − 部门直接成本 = GOP
                            GOP − 未分摊(A&G+POM+IT+销售+能源) = 洲际 GOP
                            洲际 GOP − 许可费 = 调整后 GOP
                            调整后 GOP − 奖励管理费 − 非经营性(利息) = 净营业利润
  口径A（业主台账，含服务费）：＝ 口径B + 服务费；服务费 ≈ 口径B客房 × 10.06%
  验证（2026 年 1-10 月）：3,177.15 − 1,681.96 = 1,495.19 ≈ 洲际 GOP 1,495.20 ✓
                        5,065.06 + 338.47 = 5,403.53 = 含服总收入 ✓

【评价口径】
  项目口径 NPV/IRR（不含存量债务利息，存量债务为各路径共同项，单列集团口径影响）
  评价期 20 年（基准），折现率 8%；敏感性另给 30 年、±2pp、ADR ±10%、OCC ±5pp、CAPEX ±15%
"""
import json, os, io

T = r"D:\B166ER-openclaw\workspace\.tmp"
LOG = open(os.path.join(T, "v97b.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()

# ============================================================
# 一、基线（全部可溯源，来源见 src 字段）
# ============================================================
B = {
    # 口径A（台账）
    "rev_A_fy2025": 7099.54, "rev_A_ttm": 6442.73, "rev_A_2026_10m": 5403.53,
    "rev_A_yoy_2026_10m": -0.1173,
    "mix_A_fy2025": {"客房": 0.6677, "餐饮": 0.1239, "会议": 0.1416, "其它": 0.0669},
    "mix_A_ttm":    {"客房": 0.6810, "餐饮": 0.1400, "会议": 0.1280, "其它": 0.0510},
    # 口径B（利润表，2026 1-10 月实际）
    "rev_B_10m": 5065.06, "svc_charge_10m": 338.47,
    "gop_10m": 3177.15, "ihg_gop_10m": 1495.20, "adj_gop_10m": 1393.90,
    "license_10m": 101.30, "incentive_10m": 69.69, "nonop_10m": 1740.71,
    "netop_10m": -416.51, "fraud_check": "5,065.06 + 338.47 = 5,403.53 ✓；3,177.15 − 1,681.96 = 1,495.19 ✓",
    # 成本（2026 1-10 月实际 → 年化）
    "c_labor_10m": 1820.08, "c_energy_10m": 437.70, "c_pom_10m": 228.63,
    "c_ag_10m": 578.18, "c_sm_10m": 347.97, "c_it_10m": 89.48,
    # 部门营业利润率（2026 1-10 月，口径B）
    "dept_margin": {"房务部": 0.7724, "餐饮部": 0.2907, "其他营运": 0.0752, "Misc": 1.0000},
    # 房量与经营
    "rooms": 402, "room_nights_year": 146730,
    "occ_ttm": 0.7253, "adr_A_ttm": 412.09, "revpar_ttm": 298.70,
    "occ_24m": 0.7255, "adr_A_24m": 427.42, "revpar_24m": 310.07,
    # 口径B 拆分基线（FY2025 推算）
    "room_B_fy2025": 4309.5, "svc_pct_of_room_B": 0.1006, "rev_B_fy2025": 6666.0,
    "room_A_fy2025": 4740.4,
    "nonroom_B_fy2025": 2356.5, "nonroom_margin_blend": 0.3404,
    # ★ 年化系数：P&L 成本项为 2026 年 1—10 月累计，年化须 ×1.2（12/10），不得 ×12
    "annualize_10m": 1.2,
    # 固定项
    "interest_annual": 2088.85, "depreciation_fy2025": 387.0,
    "license_pct_rev_B": 0.02, "incentive_pct": 0.05,
    # 停业期（业主已测算）
    "shutdown_labor_monthly": 109.34, "shutdown_labor_annual": 1312.08,
    "shutdown_staff": 52, "total_staff": 218,
    # 资产与债务
    "valuation_total": 69923.42, "valuation_net": 60914.78, "valuation_date": "2025-09-04",
    "book_net": 14382.0, "debt": 60677.0, "mortgage": 20000.0,
    "src": "业主两批资料（业主资料(2)、近24个月经营指标、2026年10月利润表37表、客源结构与客户反馈）；"
           "川同力达成房预估函（2025）第0915号；人力数据统计-2026.10.30；F2-29 沟通纪要",
}
BENCH = {
    "comp_adr": 416.29, "comp_occ": 0.6637, "comp_revpar": 276.71, "rgi": 107.90,
    "comp_adr_yoy_3m": -0.0414, "comp_revpar_yoy_3m": -0.0420,
    "comp_adr_yoy_12m": -0.1056, "comp_revpar_yoy_12m": -0.1146,
    "unsourced_1280": {"adr": 1280, "occ": 0.763, "revpar": 977,
        "verdict": "无法溯源·合成数·不得使用（与业主 STR 原件 ADR 差 3.07 倍）"},
    "spring_high_end_capacity": 989,
    "spring_high_end_note": "春熙路核心圈 900 元以上高价段实测总供给仅 989 间（洲至奢选 335＋尼依格罗 230＋瑞吉 282＋居舍 142）",
}

# ============================================================
# 二、路径参数
#   CAPEX_SPLIT：产业发展部测算，待 A2 工程范围核定后替换（单位万元）
#   锚点：2024 年总府实业〔2024〕11 号专题报告 预计工程费总投资 18,000 万元
#        2019 洲际总部 PIP 报告 初步造价 18,000—20,000 万元（含 IHG 技术支持费 100 万元）
# ============================================================
CAPEX_ANCHOR = {"2024报告_预计工程费总投资": 18000.0,
                "2024报告_三分项": {"建筑安装工程费": 3456.08, "基础设施配套工程费": 1383.08,
                                    "设备购置及安装工程费": 1556.56},
                "2019PIP_初步造价区间": [18000.0, 20000.0], "IHG技术支持费": 100.0,
                "status": "★ 待 A2 工程范围核定后定稿"}

PATHS = {
"P1": {"name": "路径一 · 底线整改（局部改造，维持洲际皇冠假日，402 间）",
    "tier": "A 高端全服务五星", "rooms": 402,
    "brand": "维持洲际皇冠假日委托管理（合同到期 2029-09-27）",
    "adr_excl_svc": 680.0, "adr_lo": 600.0, "adr_hi": 760.0,
    "occ": 0.730, "occ_lo": 0.700, "occ_hi": 0.760,
    "downtime": 6, "nonroom_capability": 1.00,
    "adr_basis": "洲际体系同商圈实证展示价（环球中心 757／世纪城 697）＋协议价体系（370-500）锁定上限 600-760；不得按 880 元以上立项",
    "fee_mode": "delegate", "capex": None, "capex_src": "A2 待核定",
    "capex_split": {
        "消防系统整体更新（报警主机＋前端＋线路＋泵房管网）": 2600.0,
        "供水管网整体更换（1995 敷设管体与阀件）": 1450.0,
        "机电设备更新（空调水系统／冷源／配电／电梯）": 2350.0,
        "报建、验收与专项评价": 220.0,
        "基本预备费（8%）": 529.6},
    "recommend": None},
"P2": {"name": "路径二 · 整体改造（洲际体系内换牌洲至奢选，209 间）",
    "tier": "B UPPER SCALE", "rooms": 209,
    "brand": "洲至奢选（特许管理，客房收入 5%）；洲际方已书面同意换牌并可申请豁免提前终止违约金",
    "adr_excl_svc": 950.0, "adr_lo": 900.0, "adr_hi": 1000.0,
    "occ": 0.690, "occ_lo": 0.640, "occ_hi": 0.740,
    "downtime": 12, "nonroom_capability": 1.05,
    "adr_basis": "本地实测洲至奢选 900-1,500 元；同档次实证保守取 900-1,000；209 间对应 RevPAR 须≥597 元方能守住现状客房收入",
    "fee_mode": "franchise", "capex": None, "capex_src": "A2 待核定",
    "capex_split": {
        "客房重做（含卫浴）209 间": 4200.0,
        "机电及隐蔽工程": 3900.0,
        "公区改造（全日餐厅／大堂社交／宴会强化／行政酒廊）": 3100.0,
        "后场与工区": 1300.0,
        "消防系统整体更新": 2600.0,
        "供水管网整体更换": 1450.0,
        "智能化与客控": 900.0,
        "VI 与品牌工程": 380.0,
        "电梯与特种设备": 380.0,
        "报建与审批": 320.0,
        "基本预备费（8%）": 1901.0},
    "recommend": None},
"P3": {"name": "路径三 · 整体改造（对外引入品牌／合作伙伴，188 间）",
    "tier": "A/B 之间（按 UPPER SCALE 档落地，不得按顶奢立项）", "rooms": 188,
    "brand": "外部品牌待定情景（康莱德／柏悦／Sofitel 等）；不得发函或承诺",
    "adr_excl_svc": 1200.0, "adr_lo": 1180.0, "adr_hi": 1290.0,
    "occ": 0.690, "occ_lo": 0.640, "occ_hi": 0.740,
    "downtime": 12, "nonroom_capability": 1.05,
    "adr_basis": "本地实测尼依格罗 1,180-1,400 元；188 间对应 RevPAR 须≥663 元",
    "fee_mode": "franchise", "capex": None, "capex_src": "A2 待核定",
    "capex_split": {
        "客房重做（含卫浴）188 间": 4700.0,
        "机电及隐蔽工程": 4200.0,
        "公区改造": 3600.0,
        "后场与工区": 1400.0,
        "消防系统整体更新": 2600.0,
        "供水管网整体更换": 1450.0,
        "智能化与客控": 1100.0,
        "VI 与品牌工程": 480.0,
        "电梯与特种设备": 380.0,
        "外部品牌 PIP 追加要求": 900.0,
        "报建与审批": 420.0,
        "基本预备费（8%）": 1985.0},
    "recommend": None},
"P4": {"name": "路径四 · 自创旗舰品牌（仅作参考，不主推）",
    "tier": "A/B 之间（自定标准）", "rooms": 209,
    "brand": "自创品牌（从零建立）",
    "adr_excl_svc": 900.0, "adr_lo": 800.0, "adr_hi": 1000.0,
    "occ": 0.660, "occ_lo": 0.600, "occ_hi": 0.720,
    "downtime": 14, "nonroom_capability": 1.00,
    "adr_basis": "自创品牌首 3-5 年无品牌溢价，须按同档次市场水平倒推，不得自定",
    "fee_mode": "selfbrand", "capex": None, "capex_src": "A4 待补足",
    "capex_split": {
        "客房重做（含卫浴）209 间": 4400.0,
        "机电及隐蔽工程": 4100.0,
        "公区改造": 3400.0,
        "后场与工区": 1500.0,
        "消防系统整体更新": 2600.0,
        "供水管网整体更换": 1450.0,
        "智能化与客控": 1000.0,
        "自创品牌体系（VI／PIP／注册／培训／会员与分销）": 2600.0,
        "电梯与特种设备": 380.0,
        "报建与验收": 340.0,
        "基本预备费（8%）": 1977.0},
    "recommend": None},
}

# ============================================================
# 三、测算内核
# ============================================================
def npv(rate, cfs): return sum(cf / ((1 + rate) ** i) for i, cf in enumerate(cfs))
def irr(cfs, lo=-0.90, hi=2.0, tol=1e-8):
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
    """返回达产年（口径B 万元）的经营结构"""
    adr = p["adr_excl_svc"] if adr is None else adr
    occ = p["occ"] if occ is None else occ
    nc = p["nonroom_capability"] if nonroom_cap is None else nonroom_cap
    rn = p["rooms"] * 365
    room_B = rn * occ * adr / 10000.0
    svc = room_B * B["svc_pct_of_room_B"]
    room_A = room_B + svc
    # 非房：基线随入住率弹性 0.8 次方，再乘改造能力系数
    occ_ratio = occ / B["occ_ttm"]
    nonroom_B = B["nonroom_B_fy2025"] * (occ_ratio ** 0.8) * nc
    rev_B = room_B + nonroom_B
    rev_A = rev_B + svc
    # GOP：房务部按口径B客房收入 × 房务部率；非房按混合率
    gop = room_B * B["dept_margin"]["房务部"] + nonroom_B * B["nonroom_margin_blend"]
    # 未分摊成本年化（2026 1-10 月 × 12）
    scale_room = p["rooms"] / B["rooms"]
    ANN = B["annualize_10m"]
    undist = {
        "A&G（行政及总办）": B["c_ag_10m"] * ANN * (0.75 + 0.25 * scale_room),
        "POM（工程部维保）": B["c_pom_10m"] * ANN * (0.70 + 0.30 * scale_room),
        "IT & Telecom（电脑及电信）": B["c_it_10m"] * ANN,
        "S&M（市场销售，含渠道佣金）": B["c_sm_10m"] * ANN * occ_ratio,
        "Energy（未分摊能源）": B["c_energy_10m"] * ANN * (0.55 + 0.45 * scale_room),
    }
    undist_total = sum(undist.values())
    ihg_gop = gop - undist_total
    if p["fee_mode"] == "delegate":
        license = rev_B * B["license_pct_rev_B"]
        incentive = max(0.0, ihg_gop - license) * B["incentive_pct"]
    elif p["fee_mode"] == "franchise":
        license = room_B * 0.05
        incentive = 0.0
    else:  # selfbrand
        license = 0.0
        incentive = 0.0
    adj_gop = ihg_gop - license - incentive
    return {"room_B": room_B, "svc": svc, "room_A": room_A, "nonroom_B": nonroom_B,
            "rev_B": rev_B, "rev_A": rev_A, "gop": gop, "undist": undist,
            "undist_total": undist_total, "ihg_gop": ihg_gop, "license": license,
            "incentive": incentive, "adj_gop": adj_gop, "adr": adr, "occ": occ}

def project_cf(p, capex, life=20, rate=0.08, ramp=6, sustain_capex_pct=0.02,
               adr=None, occ=None, nonroom_cap=None, brand_share=0.0, subsidy=0.0,
               downtime=None):
    """项目口径自由现金流（不含存量债务利息）"""
    dt = p["downtime"] if downtime is None else downtime
    st = annual_op(p, adr, occ, nonroom_cap)
    owner_capex = capex * (1 - brand_share) - subsidy
    # 停业期：业主已测算的在岗人工 + 维保 + 最低运行能耗（口径B 口径，不含利息）
    dt_monthly = (B["shutdown_labor_monthly"]
                  + B["c_pom_10m"] / 10 * 0.6
                  + B["c_energy_10m"] / 10 * 0.25)
    cfs = [-owner_capex]
    dt_cf = -dt_monthly
    for _ in range(dt): cfs.append(dt_cf)
    # 复业爬坡
    for m in range(ramp):
        k = 0.45 + (0.85 - 0.45) * (m / max(1, ramp - 1))
        r = annual_op(p, adr, occ, nonroom_cap)
        # 爬坡期按比例缩放收入与变动成本
        rev_B = r["rev_B"] * k; room_B = r["room_B"] * k; svc = r["svc"] * k
        gop = r["gop"] * k
        undist = r["undist_total"] * (0.85 + 0.15 * k)
        ihg = gop - undist
        lic = r["license"] * k; inc = r["incentive"] * k
        adj = ihg - lic - inc
        # 爬坡期变动成本已含在 gop 内；固定成本按 0.8 计（部分保留）
        sustain = rev_B * sustain_capex_pct / 12
        cfs.append((adj - undist * 0 + 0) * 0 + adj - 0)  # adj 已扣 undist
        cfs[-1] = adj - sustain
    # 稳定期
    for y in range(life):
        r = annual_op(p, adr, occ, nonroom_cap)
        adj = r["adj_gop"]
        sustain = r["rev_B"] * sustain_capex_pct
        cfs.append(adj - sustain)
    res = {"npv": npv(rate, cfs), "irr": irr(cfs), "payback": payback(cfs),
           "owner_capex": owner_capex, "cfs": cfs,
           "shutdown_cf_total": dt_cf * dt, "stable": st}
    return res

# ============================================================
# 四、跑数
# ============================================================
results = {}
for k, p in PATHS.items():
    capex = round(sum(p["capex_split"].values()), 2)
    p["capex"] = capex
    r = project_cf(p, capex)
    st = r["stable"]
    results[k] = {
        "name": p["name"], "tier": p["tier"], "rooms": p["rooms"], "downtime": p["downtime"],
        "capex": capex, "capex_split": p["capex_split"],
        "owner_capex": round(r["owner_capex"], 2),
        "adr": st["adr"], "occ": st["occ"],
        "room_rev_A": round(st["room_A"], 2), "nonroom_rev_B": round(st["nonroom_B"], 2),
        "rev_A_stable": round(st["rev_A"], 2), "rev_B_stable": round(st["rev_B"], 2),
        "vs_base_rev_A": round(st["rev_A"] - B["rev_A_fy2025"], 2),
        "gop": round(st["gop"], 2), "undist": round(st["undist_total"], 2),
        "ihg_gop": round(st["ihg_gop"], 2), "license": round(st["license"], 2),
        "incentive": round(st["incentive"], 2), "adj_gop": round(st["adj_gop"], 2),
        "op_cf_stable": round(st["adj_gop"] - st["rev_B"] * 0.02, 2),
        "shutdown_cf_total": round(r["shutdown_cf_total"], 2),
        "npv": round(r["npv"], 2),
        "irr_pct": (round(r["irr"] * 100, 2) if r["irr"] is not None else None),
        "payback_yr": (round(r["payback"], 2) if r["payback"] is not None else None),
        "undist_detail": {kk: round(vv, 2) for kk, vv in st["undist"].items()},
    }
    L("%s capex=%.0f 房量=%d 达产营收A=%.0f 调整后GOP=%.0f 经营现金流=%.0f NPV=%.0f IRR=%s 回收=%s" % (
        k, capex, p["rooms"], st["rev_A"], st["adj_gop"],
        st["adj_gop"] - st["rev_B"] * 0.02, r["npv"], results[k]["irr_pct"], results[k]["payback_yr"]))

# ============================================================
# 五、盈亏平衡约束
# ============================================================
be = {}
for k, p in PATHS.items():
    rn = p["rooms"] * 365
    req = B["room_A_fy2025"] * 10000 / rn          # 守住现状口径A客房收入所需 RevPAR
    assumed = rn * p["occ"] * p["adr_excl_svc"] * 1.1006 / 10000
    be[k] = {"rooms": p["rooms"], "required_revpar": round(req, 0),
             "assumed_revpar": round(assumed, 0), "gap": round(assumed - req, 0),
             "pass": assumed >= req}
    L("盈亏平衡 %s: 守住现状客房收入需 RevPAR %.0f 元｜方案 RevPAR %.0f 元｜差 %+.0f → %s" % (
        k, req, assumed, assumed - req, "通过" if assumed >= req else "不通过"))

# ============================================================
# 六、敏感性
# ============================================================
sens = {}
for k, p in PATHS.items():
    capex = p["capex"]; s = {}
    for lbl, kw in (("ADR -10%", dict(adr=p["adr_excl_svc"] * 0.9)),
                    ("ADR 基准", dict()),
                    ("ADR +10%", dict(adr=p["adr_excl_svc"] * 1.1)),
                    ("OCC -5pp", dict(occ=p["occ"] - 0.05)),
                    ("OCC 基准", dict()),
                    ("OCC +5pp", dict(occ=p["occ"] + 0.05)),
                    ("CAPEX -15%", dict()),
                    ("CAPEX 基准", dict()),
                    ("CAPEX +15%", dict())):
        if lbl == "CAPEX -15%": r = project_cf(p, capex * 0.85, **kw)
        elif lbl == "CAPEX +15%": r = project_cf(p, capex * 1.15, **kw)
        else: r = project_cf(p, capex, **kw)
        s[lbl] = round(r["npv"], 0)
    for lbl, kw in (("折现率 6%", dict(rate=0.06)), ("折现率 8%", dict(rate=0.08)),
                    ("折现率 10%", dict(rate=0.10))):
        s[lbl] = round(project_cf(p, capex, **kw)["npv"], 0)
    for lbl, kw in (("评价期 10 年", dict(life=10)), ("评价期 20 年", dict(life=20)),
                    ("评价期 30 年", dict(life=30))):
        s[lbl] = round(project_cf(p, capex, **kw)["npv"], 0)
    for lbl, bs in (("品牌方承担 0%", 0.0), ("品牌方承担 20%", 0.20), ("品牌方承担 30%", 0.30)):
        s[lbl] = round(project_cf(p, capex, brand_share=bs)["npv"], 0)
    sens[k] = s
    L("敏感性 %s: %s" % (k, json.dumps(s, ensure_ascii=False)))

# ============================================================
# 七、集团口径补充（存量债务利息刚性）
# ============================================================
grp = {}
for k, p in PATHS.items():
    r = results[k]
    grp[k] = {"interest_annual": B["interest_annual"],
              "shutdown_interest_outflow": round(B["interest_annual"] / 12 * p["downtime"], 2),
              "note": "存量债务 60,677 万元刚性，各路径共同项；集团口径现金流须叠加"}
    L("集团口径 %s: 停业期利息流出 %.0f 万元" % (k, grp[k]["shutdown_interest_outflow"]))

OUT = {"meta": {"title": "v97b 三路径经济测算（自下而上·部门级）", "date": "2026-11-15",
                "口径": "收入=口径A（含服务费）用于呈现；成本与利润=口径B（P&L），两者 1.1006 倍可复算桥接",
                "评价": "项目口径 NPV/IRR（不含存量债务利息，存量债务为各路径共同项）；评价期 20 年；折现率 8%",
                "capex_anchor": CAPEX_ANCHOR, "capex_status": "产业发展部测算，待 A2 工程范围核定后定稿",
                "禁止": "★ 不得使用「春熙路 1,280 元／76.3%／977 元」—— 无法溯源的合成数"},
       "base": B, "bench": BENCH, "paths": PATHS,
       "results": results, "breakeven": be, "sensitivity": sens, "group_view": grp}
io.open(os.path.join(T, "v97b.json"), "w", encoding="utf-8").write(json.dumps(OUT, ensure_ascii=False, indent=1))
L("写出 v97b.json")
L("DONE")
