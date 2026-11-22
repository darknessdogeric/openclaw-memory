# -*- coding: utf-8 -*-
"""
v97 三路径经济测算模型（单一数据源）
生成：2026-11-15｜产业发展部
口径声明：
  1. 收入/房价/出租率一律用「口径A（含 10% 服务费）」，与业主《业主资料(2)》营业收入完全吻合；
     成本与利润用「口径B（利润表）」，两者有 1.1 倍可复算桥接，报告中显式标注。
  2. 改造前基线全部取自业主两批资料与业主方 STR 原件，不使用任何未溯源数字。
  3. 评价期 20 年（基准），折现率 8%，敏感性另给 30 年与 ±2pp。
"""
import json, os, io, math

T = r"D:\B166ER-openclaw\workspace\.tmp"
LOG = open(os.path.join(T, "v97_model.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()

# ============================================================
# 一、改造前基线（全部可溯源）
# ============================================================
BASE = {
    "rooms": 402,
    "room_nights_year": 146730,          # 402 × 365
    "occ_12m": 0.7253,                   # 滚动 12M（2025-10→2026-09）
    "adr_12m": 412.09,
    "revpar_12m": 298.70,
    "adr_24m": 427.42,
    "occ_24m": 0.7255,
    "revpar_24m": 310.07,
    "revenue_fy2025": 7099.54,           # 万元，口径A
    "revenue_ttm": 6442.73,
    "revenue_2026_10m": 5403.53,         # 2026 年 1-10 月，同比 -11.73%
    "mix_fy2025": {"客房": 0.6677, "餐饮": 0.1239, "会议": 0.1416, "其它": 0.0669},
    "mix_ttm":    {"客房": 0.6810, "餐饮": 0.1400, "会议": 0.1280, "其它": 0.0510},
    "room_rev_fy2025": 4740.4,           # = 7099.54 × 66.77%
    "room_rev_ttm": 4387.7,
    "nonroom_rev_fy2025": 2359.1,
    "nonroom_rev_ttm": 2055.0,
    "meeting_rev_ttm": 823.4,
    "net_op_profit_2026_10m": -416.51,   # 万元
    "cost_labor_fy2025": 2530.0,
    "cost_energy_ttm": 548.6,
    "cost_maintain_fy2025": 183.81,
    "interest_monthly": 174.07,          # 万元/月，2026 1-10 月 1,740.71 万
    "depreciation_fy2025": 387.0,
    "mgmt_fee_monthly": 17.10,           # 洲际许可费 10.13 + 奖励管理费 6.97
    "labor_during_shutdown_monthly": 109.34,   # 保留 52 人方案一 1,312.08 万/年
    "str_comp": {"adr_12m": 416.29, "occ_12m": 0.6637, "revpar_12m": 276.71, "rgi_12m": 107.90},
    "valuation": {"total": 69923.42, "net": 60914.78, "date": "2025-09-04"},
    "book_net": 14382.0,
    "debt": 60677.0,
    "mortgage": 20000.0,
}
# 竞对组与总府实测（用于报告正文的对照）
BENCH = {
    "comp_adr": 416.29, "comp_occ": 0.6637, "comp_revpar": 276.71, "rgi": 107.90,
    "tf_adr": 412.09, "tf_occ": 0.7253, "tf_revpar": 298.70,
    "comp_adr_yoy_3m": -0.0414, "comp_revpar_yoy_3m": -0.0420,
    "comp_adr_yoy_mom12": -0.1056, "comp_revpar_yoy_mom12": -0.1146,
    "unsourced": {"adr": 1280, "occ": 0.763, "revpar": 977,
                  "verdict": "无法溯源，不得使用；来源合成数，与业主 STR 原件相差 ADR 3.07 倍"},
}

def money(x): return round(x, 2)

# ============================================================
# 二、路径参数（capex/工期由 A2、A4 回填后定稿；此处为可核验锚点）
# ============================================================
# 投资锚点：
#   ① 2024 年总府实业〔2024〕11 号专题报告：预计工程费总投资 18,000 万元
#      （建筑安装工程费 3,456.08＋基础设施配套 1,383.08＋设备购置及安装 1,556.56＋其余费用及预备费、建设期利息）
#   ② 2019 洲际总部 PIP 报告：初步造价 18,000—20,000 万元（含 IHG 技术支持费 100 万元）
#   ③ 洲至奢选（棕榈泉）2026-01-01 开业，335 间，同产品形态近期实证
CAPEX_ANCHOR = {"2024报告工程费": 18000.0, "2019PIP区间": [18000.0, 20000.0], "IHG技术支持费": 100.0}

PATHS = {
    "P1": {
        "name": "路径一 · 底线整改（局部改造，维持皇冠假日，402 间）",
        "tier": "A 高端全服务五星",
        "rooms": 402,
        "brand": "维持洲际皇冠假日委托管理（合同到期 2029-09-27）",
        "downtime": 6,
        "adr": 680.0, "adr_lo": 600.0, "adr_hi": 760.0, "occ": 0.730, "occ_lo": 0.700, "occ_hi": 0.760,
        "adr_basis": "洲际体系同商圈实证展示价（环球中心 757／世纪城 697）与协议价体系（370-500）锁定上限 600-760；"
                     "不得按 880 元以上立项",
        "nonroom_ratio": 0.3323,   # 非房收入占营业收入比例（FY2025 实测）
        "capex": None, "capex_note": "待 A2 工程范围核定",
        "capex_split": None,
        "fee_pct": None,           # 管理费/品牌费占客房收入比例（待 A4 合同条款）
        "investment_share_brand": 0.0,   # 品牌方承担改造投入比例（基准 0，待谈判）
        "subsidy": 0.0,
        "recommended": None,
    },
    "P2": {
        "name": "路径二 · 整体改造（洲际体系内换牌洲至奢选，209 间）",
        "tier": "B UPPER SCALE",
        "rooms": 209,
        "brand": "洲至奢选（特许管理，客房收入 5%）；洲际方已书面同意换牌并可申请豁免提前终止违约金",
        "downtime": 12,
        "adr": 950.0, "adr_lo": 900.0, "adr_hi": 1000.0, "occ": 0.690, "occ_lo": 0.640, "occ_hi": 0.740,
        "adr_basis": "本地实测：洲至奢选 900-1,500 元；同档次实证保守取 900-1,000，"
                     "房量 209 间对应 RevPAR 须≥597 元方能守住现状客房收入",
        "nonroom_ratio": 0.3323,
        "capex": None, "capex_note": "待 A2 工程范围核定；锚点 2024 报告 18,000 万元",
        "capex_split": None,
        "fee_pct": 0.05,
        "investment_share_brand": 0.0,
        "subsidy": 0.0,
        "recommended": None,
    },
    "P3": {
        "name": "路径三 · 整体改造（对外引入品牌 / 合作伙伴）",
        "tier": "A/B 之间（外部品牌按 UPPER SCALE 档落地，不得按顶奢立项）",
        "rooms": 188,
        "brand": "外部品牌（待定情景：康莱德／柏悦／Sofitel 等；不得发函或承诺）",
        "downtime": 12,
        "adr": 1200.0, "adr_lo": 1180.0, "adr_hi": 1290.0, "occ": 0.690, "occ_lo": 0.640, "occ_hi": 0.740,
        "adr_basis": "本地实测：尼依格罗 1,180-1,400 元；房量 188 间对应 RevPAR 须≥663 元",
        "nonroom_ratio": 0.3323,
        "capex": None, "capex_note": "待 A2 工程范围核定；不低于路径二，另计外部品牌 PIP 追加",
        "capex_split": None,
        "fee_pct": 0.05,
        "investment_share_brand": 0.0,
        "subsidy": 0.0,
        "recommended": None,
    },
    "P4": {
        "name": "路径四 · 自创旗舰品牌（仅作参考，不主推）",
        "tier": "A/B 之间（自定标准）",
        "rooms": 209,
        "brand": "自创品牌（从零建立）",
        "downtime": 14,
        "adr": 900.0, "adr_lo": 800.0, "adr_hi": 1000.0, "occ": 0.660, "occ_lo": 0.600, "occ_hi": 0.720,
        "adr_basis": "自创品牌首 3-5 年无品牌溢价，须按同档次市场水平倒推，不得自定",
        "nonroom_ratio": 0.3323,
        "capex": None, "capex_note": "待 A4 补足；工程费＋品牌创建体系成本",
        "capex_split": None,
        "fee_pct": 0.0,
        "investment_share_brand": 0.0,
        "subsidy": 0.0,
        "recommended": None,
    },
}

# ============================================================
# 三、测算内核
# ============================================================
def npv(rate, cfs):
    return sum(cf / ((1 + rate) ** i) for i, cf in enumerate(cfs))

def irr(cfs, lo=-0.95, hi=3.0, tol=1e-7):
    f_lo, f_hi = npv(lo, cfs), npv(hi, cfs)
    if f_lo * f_hi > 0:
        return None
    for _ in range(300):
        mid = (lo + hi) / 2
        f_mid = npv(mid, cfs)
        if abs(f_mid) < tol: return mid
        if f_lo * f_mid <= 0: hi, f_hi = mid, f_mid
        else: lo, f_lo = mid, f_mid
    return (lo + hi) / 2

def payback(cfs):
    cum = 0
    for i, cf in enumerate(cfs):
        prev = cum; cum += cf
        if prev < 0 <= cum and cf != 0:
            return i - 1 + (-prev / cf)
    return None

def evaluate(p, capex, life=20, rate=0.08, occ=None, adr=None,
             fee_pct=None, brand_share=None, subsidy=None, downtime=None,
             ramp_months=6, nonroom_ratio=None):
    occ = p["occ"] if occ is None else occ
    adr = p["adr"] if adr is None else adr
    fee_pct = p.get("fee_pct") if fee_pct is None else fee_pct
    brand_share = p.get("investment_share_brand", 0.0) if brand_share is None else brand_share
    subsidy = p.get("subsidy", 0.0) if subsidy is None else subsidy
    downtime = p["downtime"] if downtime is None else downtime
    nonroom_ratio = p.get("nonroom_ratio", 0.3323) if nonroom_ratio is None else nonroom_ratio

    rooms = p["rooms"]
    rn_year = rooms * 365
    # 稳定期客房收入（含服务费口径）
    room_rev = rn_year * occ * adr / 10000.0
    total_rev = room_rev / (1 - nonroom_ratio)
    # 变动成本率（口径B 反推）：以 FY2025 经营毛利润 1,580.64 万 / 营业收入 7,099.54 万 = 22.26% 为起点，
    # 改造后产品力提升 → 毛利率改善，但人工与能耗随房量下降而下降、部分固定成本不变。
    # 采用「变动成本率不变 + 固定成本随房量部分调整」的方式，显式列出，避免把全部成本按比例缩放。
    var_cost_rate = 0.5545     # 1 - 0.2226 - 0.2229(毛利) 拆分口径，待校准
    # 固定成本（年化，万元）现状口径
    fix_base = {
        "labor": BASE["cost_labor_fy2025"],      # 2,530.0
        "energy": 548.6,
        "maintain": BASE["cost_maintain_fy2025"],# 183.81
        "mgmt_fee": BASE["mgmt_fee_monthly"] * 12,   # 205.2
        "interest": BASE["interest_monthly"] * 12,   # 2,088.84
    }
    # 房量缩放系数：人工按人房比缩放、能耗按间夜缩放、维保半固定、管理费按合同重定
    scale = rooms / BASE["rooms"]
    fix_new = {
        "labor": fix_base["labor"] * (0.45 + 0.55 * scale),   # 45% 固定＋55% 随房量
        "energy": fix_base["energy"] * scale,
        "maintain": fix_base["maintain"] * (0.6 + 0.4 * scale),
        "interest": fix_base["interest"],                      # 刚性
    }
    # 品牌/管理费：按客房收入比例
    fee_new = room_rev * (fee_pct or 0.0)

    # 停业期现金流出（每月）
    shutdown_monthly_fixed = (fix_base["labor"] / BASE["rooms"] * 0.55 * rooms / 12
                              + fix_base["interest"] / 12
                              + fix_base["maintain"] / 12
                              + fix_base["energy"] / 12 * 0.25   # 最低运行能耗
                              + BASE["mgmt_fee_monthly"])          # 合同未定，可能减免，按计收取（保守）
    shutdown_loss = shutdown_monthly_fixed * downtime

    # 资本开支：业主承担 = capex ×（1 - brand_share） - subsidy
    owner_capex = capex * (1 - brand_share) - subsidy
    # 折旧（简化：直线 20 年，改造资产；不计入现金流决策，仅作利润口径）
    cfs = []
    # t=0 资本开支
    cfs.append(-owner_capex)
    # 停业期
    for i in range(downtime):
        cfs.append(-shutdown_loss)
    # 复业爬坡
    ramp = []
    for m in range(ramp_months):
        # 爬坡系数：第1月 0.45 → 逐月提升至 0.85
        k = 0.45 + (0.85 - 0.45) * (m / max(1, ramp_months - 1))
        ramp.append(k)
    # 稳定期（life 年）
    for y in range(life):
        for m in range(12):
            idx = len(cfs)
            if idx < downtime + ramp_months:
                k = ramp[idx - downtime]
                occ_m = occ * k
                rr = rn_year / 12 * occ_m * adr / 10000.0
                tr = rr / (1 - nonroom_ratio)
            else:
                rr = room_rev / 12
                tr = total_rev / 12
            # 变动成本
            vc = tr * var_cost_rate
            # 固定成本（年化按月）
            fx = (fix_new["labor"] + fix_new["energy"] + fix_new["maintain"] + fix_new["interest"]) / 12
            fee_m = fee_new / 12
            cf = tr - vc - fx - fee_m
            cfs.append(cf)
    res = {
        "rooms": rooms, "downtime": downtime,
        "adr": adr, "occ": occ,
        "room_rev_stable": money(room_rev),
        "total_rev_stable": money(total_rev),
        "nonroom_rev_stable": money(total_rev - room_rev),
        "vs_base_room_rev": money(room_rev - BASE["room_rev_fy2025"]),
        "vs_base_total_rev": money(total_rev - BASE["revenue_fy2025"]),
        "fixed_cost_annual": money(sum(fix_new.values())),
        "fee_annual": money(fee_new),
        "owner_capex": money(owner_capex),
        "shutdown_loss_total": money(shutdown_loss),
        "npv": money(npv(rate, cfs)),
        "irr": (round(irr(cfs) * 100, 2) if irr(cfs) is not None else None),
        "payback_static": (round(payback(cfs), 2) if payback(cfs) is not None else None),
        "cfs": [money(x) for x in cfs],
    }
    return res

# ============================================================
# 四、跑四条路径（capex 锚点先用 2024 报告 18,000 万的合理分档，待 A2 定稿）
# ============================================================
# 临时分档（依据 2024 报告三分项构成比例，待 A2 工程范围核定后替换）
CAPEX_TMP = {
    # 底线整改：消防系统整体更新＋供水管网整体更新＋机电更新，不动客房与公区
    "P1": {"消防系统更新": 2600.0, "供水管网整体更换": 1450.0, "机电设备更新": 2350.0,
           "电梯与特种设备": 380.0, "报建与验收": 220.0, "预备费": 700.0},
    "P2": {"客房重做（含卫浴）": 4200.0, "机电及隐蔽工程": 3900.0, "公区改造": 3100.0,
           "后场与工区": 1300.0, "消防系统更新": 2600.0, "供水管网整体更换": 1450.0,
           "智能化与客控": 900.0, "VI与品牌工程": 380.0, "电梯与特种设备": 380.0,
           "报建与验收": 320.0, "预备费": 2090.0},
    "P3": {"客房重做（含卫浴）": 4700.0, "机电及隐蔽工程": 4200.0, "公区改造": 3600.0,
           "后场与工区": 1400.0, "消防系统更新": 2600.0, "供水管网整体更换": 1450.0,
           "智能化与客控": 1100.0, "VI与品牌工程": 480.0, "电梯与特种设备": 380.0,
           "外部品牌PIP追加": 900.0, "报建与审批": 420.0, "预备费": 2370.0},
    "P4": {"客房重做（含卫浴）": 4400.0, "机电及隐蔽工程": 4100.0, "公区改造": 3400.0,
           "后场与工区": 1500.0, "消防系统更新": 2600.0, "供水管网整体更换": 1450.0,
           "智能化与客控": 1000.0, "自创品牌体系（VI/PIP/注册/培训）": 2600.0,
           "电梯与特种设备": 380.0, "报建与验收": 340.0, "预备费": 2290.0},
}
results = {}
for k, p in PATHS.items():
    split = CAPEX_TMP[k]
    capex = sum(split.values())
    r = evaluate(p, capex)
    r["capex_split"] = split
    r["capex_total"] = money(capex)
    results[k] = r
    L("%s capex=%.1f 稳定期营收=%.1f 房量=%d NPV=%.1f IRR=%s 回收期=%s" % (
        k, capex, r["total_rev_stable"], p["rooms"], r["npv"], r["irr"], r["payback_static"]))

# ============================================================
# 五、敏感性
# ============================================================
sens = {}
for k, p in PATHS.items():
    capex = sum(CAPEX_TMP[k].values())
    s = {}
    # ADR ±10%
    for lbl, adr in (("adr_-10%", p["adr"] * 0.9), ("adr_base", p["adr"]), ("adr_+10%", p["adr"] * 1.1)):
        s[lbl] = evaluate(p, capex, adr=adr)["npv"]
    # 出租率 ±5pp
    for lbl, occ in (("occ_-5pp", max(0.3, p["occ"] - 0.05)), ("occ_base", p["occ"]), ("occ_+5pp", p["occ"] + 0.05)):
        s[lbl] = evaluate(p, capex, occ=occ)["npv"]
    # CAPEX ±15%
    for lbl, cp in (("capex_-15%", capex * 0.85), ("capex_base", capex), ("capex_+15%", capex * 1.15)):
        s[lbl] = evaluate(p, cp)["npv"]
    # 折现率
    for lbl, rt in (("rate_6%", 0.06), ("rate_8%", 0.08), ("rate_10%", 0.10)):
        s[lbl] = evaluate(p, capex, rate=rt)["npv"]
    # 评价期
    for lbl, lf in (("life_10y", 10), ("life_20y", 20), ("life_30y", 30)):
        s[lbl] = evaluate(p, capex, life=lf)["npv"]
    # 品牌方承担改造投入 0/20/30%
    for lbl, bs in (("brand_0%", 0.0), ("brand_20%", 0.20), ("brand_30%", 0.30)):
        s[lbl] = evaluate(p, capex, brand_share=bs)["npv"]
    sens[k] = {k2: money(v) for k2, v in s.items()}
    L("敏感性 %s: %s" % (k, json.dumps(sens[k], ensure_ascii=False)))

# ============================================================
# 六、盈亏平衡约束（守住现状客房收入所需 RevPAR）
# ============================================================
breakeven = {}
for k, p in PATHS.items():
    rn = p["rooms"] * 365
    be = BASE["room_rev_fy2025"] * 10000 / rn / 10000   # 万元/间夜 → 元/间夜
    breakeven[k] = {"rooms": p["rooms"], "required_revpar": money(BASE["room_rev_fy2025"] * 10000 / rn),
                    "assume_revpar": money(rn * p["occ"] * p["adr"] / 10000 / 10000),
                    "gap": money(rn * p["occ"] * p["adr"] / 10000 / 10000 - BASE["room_rev_fy2025"] * 10000 / rn)}
    L("盈亏平衡 %s: 需 RevPAR %.0f 元｜假设 %.0f 元｜差 %.0f" % (
        k, breakeven[k]["required_revpar"], breakeven[k]["assume_revpar"], breakeven[k]["gap"]))

OUT = {
    "meta": {"title": "v97 三路径经济测算", "date": "2026-11-15",
             "口径": "收入=口径A（含10%服务费）；成本=口径B（利润表）；评价期20年；折现率8%",
             "capex_status": "临时分档，待 A2 工程范围核定后定稿",
             "capex_anchor": CAPEX_ANCHOR},
    "base": BASE, "bench": BENCH, "paths": PATHS,
    "results": results, "sensitivity": sens, "breakeven": breakeven,
}
io.open(os.path.join(T, "v97.json"), "w", encoding="utf-8").write(json.dumps(OUT, ensure_ascii=False, indent=1))
L("写出 v97.json")
L("DONE")
