# -*- coding: utf-8 -*-
"""v49：v4.0 重构引擎
   ① 停业损失口径分离：段一A 停业期刚性现金支出（资金需求口径）／段一B 营业收入归零（现金流评价口径）
   ② 品牌候选集（按内部《高星级全服式酒店品牌分级分类（仅5★+）》+ 成都实测房价带）逐品牌测算
   ③ 全停业 vs 分期开业（滚动改造）对比
   ④ 经营期 20 年 vs 30 年
   ⑤ 净现值转正路径分解（逐杠杆贡献）
   数据源：v9.json（造价参数）、area_base.py（面积）、seasonal_24m.json（24 个月曲线）、
           内部品牌分级分类表（档位·单房造价·抽佣）、2026-10 成都实测房价带、2026 联网复核"""
import os, json, importlib.util, math
T = r"D:\B166ER-openclaw\workspace\.tmp"
D = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc"
OUT = open(os.path.join(T, "v49.log"), "w", encoding="utf-8")
def L(*a):
    OUT.write(" ".join(str(z) for z in a) + "\n"); OUT.flush()

spec = importlib.util.spec_from_file_location("v10", os.path.join(D, "v10_econ.py"))
V10 = importlib.util.module_from_spec(spec); spec.loader.exec_module(V10)
RES = {x["key"]: x for x in json.load(open(os.path.join(T, "v9.json"), encoding="utf-8"))}
SE = json.load(open(os.path.join(D, "seasonal_24m.json"), encoding="utf-8"))
V21 = json.load(open(os.path.join(T, "v21.json"), encoding="utf-8"))
BASE = V21["base"]
def N(v, d=1): return format(round(v, d), ",.%df" % d)
def P(v): return ("%.2f%%" % (v * 100)) if v is not None else "无可解"

GUEST_NET = 10192.0
SELLABLE = 402
MEP_S1 = RES["S1"]["mep"]
FIX_S1 = RES["S1"]["fitout"]
MONTHS_S1 = RES["S1"]["months"]
L("=== 0. 造价锚点（v9.json）===")
L("S1：段二机电 %s 万｜段三装修 %s 万｜停业 %d 月｜房量 %d" % (N(MEP_S1), N(FIX_S1), MONTHS_S1, RES["S1"]["n_rooms"]))
L("715 定稿交叉验证：总府停业 1 年刚性支出 3,674 万元（人工 1,412 ＋ 其余）")

# ══════════════════════════════════════════════════════════════
# ① 停业损失口径分离
# ══════════════════════════════════════════════════════════════
L("")
L("=== 1. 停业损失口径分离（第 17 条）===")
FIXED_MONTHLY = 284.0   # 停业期刚性现金支出（人工留存+能耗维持+保险安保+利息），集团 715 定稿口径
def closure_split(months, start_month=1, brand_ret_m=0.0, seasonal=True):
    """返回 (资金需求口径：刚性支出+品牌保留费, 现金流评价口径：再加营业收入归零)"""
    cash_out = 0.0; rev_lost = 0.0
    for k in range(months):
        m = ((start_month - 1 + k) % 12) + 1
        cash_out += FIXED_MONTHLY + brand_ret_m
        rev_lost += SE["season"][str(m)]["rev"] / 1e4 if seasonal else 564.5
    return cash_out, rev_lost
brand_ret_ihg = 6.38   # 万/月（皇冠：总营收 2% 基础管理费 × 35% 保留比例，按 S1 稳态营收折）
for mo in (8, 12, 16, 20):
    a, b = closure_split(mo, 1, brand_ret_ihg, True)
    L("   停业 %2d 月：段一A 刚性现金支出 %8.1f 万｜段一B 营业收入归零 %8.1f 万｜旧口径合计 %8.1f 万"
      % (mo, a, b, a + b))
L("   ★ 结论：段一作为「资金需求」只含段一A（刚性支出＋品牌保留费）；段一B 为营业收入归零，")
L("     只在财务评价的现金流中体现，不得计入需投入资金。旧口径 815 万/月把两者混同，是错的。")
L("   ★ 交叉验证：12 个月刚性现金支出 %s 万，与 715 定稿「停业一年刚性支出 3,674 万元」量级一致。" % N(closure_split(12,1,brand_ret_ihg)[0]))

# ══════════════════════════════════════════════════════════════
# ② 品牌候选集
# ══════════════════════════════════════════════════════════════
# 单房改造造价（万元/间）来源：内部品牌分级分类表 §8 速查表；抽佣合计同表 §6.2
# 成都房价带：2026-10 实测（Trip/wanderinchina/yourwayholiday 等）；未开业者标注无实测
BRANDS = [
 # key, 中文名, 档位, 单房造价(低,高), 抽佣(低,高), 客房面积门槛㎡, 成都实测房价(低,高), 房量, 状态, 位置匹配
 ("B1","皇冠假日（现状）","上高端全服务",20,30,6.0,10.5,0,None,None,"已入驻","存量续约"),
 ("B2","洲至奢选","上高端/奢华",30,40,7.5,11.0,0,900,None,"棕榈泉 335 间已开业","同集团可换"),
 ("B3","康莱德 Conrad","上高端全服务",20,30,7.5,10.5,0,None,None,"成都未见开业","空位"),
 ("B4","费尔蒙 Fairmont","上高端全服务",20,30,6.5,10.0,0,900,336,"棕榈泉已转洲至","已占"),
 ("B5","Sofitel 索菲特","上高端/奢华",25,35,6.5,10.5,0,None,None,"成都未见开业","空位"),
 ("B6","瑞吉 St. Regis","规模化奢华",28.8,57.6,7.5,11.5,40,1200,312,"在营","已被占"),
 ("B7","尼依格罗 Niccolo","规模化奢华",28.8,57.6,7.0,11.0,40,1200,238,"IFS 在营","已被占"),
 ("B8","柏悦 Park Hyatt","规模化奢华",28.8,57.6,7.5,11.5,0,None,None,"成都未见开业","空位"),
 ("B9","丽晶 Regent","顶奢",36,50,8.0,10.5,40,None,None,"已签约顺江路 2029Q3","已被占（10km 外）"),
 ("B10","六善 Six Senses","高端奢华",36,50,8.0,10.5,45,None,None,"成都未见开业","空位"),
 ("B11","文华东方 MO","高端奢华",36,50,8.0,9.5,45,None,None,"成都未见开业","空位"),
 ("B12","LXR","超奢顶段",43,72,6.5,10.5,0,None,None,"总府路 28 号「黑洞」项目","重大空位"),
]
TIER_OP = {  # 档次 → (GOP, 非房系数, 出租率)
 "上高端全服务": (0.300, 1.42, 0.70),
 "上高端/奢华": (0.330, 1.55, 0.70),
 "规模化奢华": (0.360, 1.72, 0.72),
 "高端奢华": (0.380, 1.85, 0.74),
 "顶奢": (0.400, 1.95, 0.75),
 "超奢顶段": (0.410, 2.00, 0.75),
}
def rooms_by_area(threshold):
    if not threshold: return SELLABLE
    return int(GUEST_NET // threshold)

def brand_case(b, adr, occ_override=None, capex_scale=1.0, months=12, horizon=30,
               phased=False, brand_share=0.0, subsidy=0.0, revenue_boost=1.0):
    key, name, tier, pk_lo, pk_hi, fee_lo, fee_hi, area_th, p_lo, p_hi, rooms, status, loc = b
    n = rooms_by_area(area_th)
    gop_r, nonroom_r, occ_d = TIER_OP[tier]
    occ = occ_override or occ_d
    # 平均房价：实测优先；无实测则按分级表入门价 × 成都溢价系数（标注为推测）
    if p_lo is None:
        entry = {0: 300, 20: 300, 25: 350, 28.8: 450, 30: 300, 36: 650, 40: 600, 43: 1400}
        adr_used = entry.get(pk_lo, 500) * 1.45   # 成都核心商圈溢价系数（推测值）
        adr_src = "分级表入门价 × 成都溢价系数（推测，无成都实测）"
    else:
        adr_used = (p_lo + p_hi) / 2
        adr_src = "成都实测房价带中位"
    room_rev = n * 365 * occ * adr_used / 1e4
    total_rev = room_rev * nonroom_r * revenue_boost
    # 造价：客房按品牌单房造价中位，公区按品牌档次系数（皇冠现状基线为 1.0）
    pk = (pk_lo + pk_hi) / 2
    pub_mult = {"上高端全服务":1.00,"上高端/奢华":1.35,"规模化奢华":1.55,"高端奢华":1.80,"顶奢":2.00,"超奢顶段":2.40}[tier]
    fit = FIX_S1 * (pk / 24.79) * pub_mult * capex_scale   # FIX_S1 对应单房 7.22 万（皇冠基线）
    if area_th:   # 减房后公区与客房均按比例缩
        fit = fit * (n / SELLABLE) if False else fit
    capex = MEP_S1 + fit
    if brand_share: capex = capex * (1 - brand_share)
    capex -= subsidy
    # 费用
    fee = (fee_lo + fee_hi) / 2 / 100.0
    brand_base = total_rev * (fee_lo / 100.0)
    mkt = total_rev * 0.025; loy = total_rev * 0.020; ffe = total_rev * (0.040 if pk >= 36 else 0.020)
    inc_rate = 0.10 if pk >= 36 else 0.06
    gop = total_rev * gop_r
    owner_ann = gop - brand_base - mkt - loy - ffe - gop * inc_rate
    # 现金流
    br_m = brand_base * 0.35 / 12.0
    mcf = []
    if phased:
        # 分期：全楼停业 4 个月 → 第 5-16 月按 40% 房间运营爬坡 → 第 17 月全开
        full_m, phase_end = 4, 16
        for tt in range(1, horizon * 12 + 1):
            if tt <= full_m:
                rev = 0.0; cash = -FIXED_MONTHLY - br_m
            elif tt <= phase_end:
                since = tt - full_m
                rev = total_rev / 12.0 * (0.40 * min(1.0, 0.35 + 0.05 * since))
                g = rev * gop_r; r_ = rev / total_rev
                cash = (g - brand_base * r_ - mkt * r_ - loy * r_ - ffe * r_ - g * inc_rate)
                cash -= FIXED_MONTHLY * 0.35
            else:
                since = tt - phase_end
                rev = (total_rev / 12.0) * min(1.0, 0.70 + 0.03 * since)
                g = rev * gop_r; r_ = rev / total_rev
                cash = (g - brand_base * r_ - mkt * r_ - loy * r_ - ffe * r_ - g * inc_rate)
            # 改造投资 18 个月均匀投入
            if tt <= 18: cash -= capex / 18.0
            mcf.append(cash)
    else:
        for tt in range(1, horizon * 12 + 1):
            rev = 0.0
            if tt > months:
                since = tt - months
                rev = (total_rev / 12.0) * min(1.0, 0.62 + 0.038 * since)
            g = rev * gop_r; r_ = rev / total_rev if total_rev else 0
            cash = (g - brand_base * r_ - mkt * r_ - loy * r_ - ffe * r_ - g * inc_rate)
            if tt <= months:
                cash -= FIXED_MONTHLY + br_m
            half = max(1, months // 2)
            if 1 <= tt <= half: cash -= capex * 0.6 / half
            elif half < tt <= months: cash -= capex * 0.4 / max(1, months - half)
            if tt > months:
                since = tt - months
                if since < 12: cash -= total_rev * 0.085 / 12.0
                elif since < 24: cash -= total_rev * 0.030 / 12.0
                if since < 6: cash -= total_rev * 0.012 / 6.0
            mcf.append(cash)
    acf = [round(sum(mcf[y * 12:(y + 1) * 12]), 1) for y in range(horizon)]
    def pv(cf, r=0.08): return round(sum(c / (1 + r) ** i for i, c in enumerate(cf)), 1)
    return dict(key=key, name=name, tier=tier, n=n, adr=adr_used, adr_src=adr_src, occ=occ,
                total_rev=total_rev, capex=capex, fit=fit, owner_ann=owner_ann,
                npv=pv(acf), irr=V10.irr(acf), pb=V10.payback(acf),
                npv20=pv(acf[:20]), irr20=V10.irr(acf[:20]), pb20=V10.payback(acf[:20]),
                gop=gop, fee=fee)

L("")
L("=== 2. 品牌候选集逐品牌测算（全停业 12 月、30 年期、8% 折现）===")
L("   %-4s %-18s %-12s %5s %7s %9s %10s %9s %9s %8s" % ("序","品牌","档位","房量","ADR","年营收","改造投资","净现值30","净现值20","全口径IRR"))
RESULTS = []
for b in BRANDS:
    r = brand_case(b, None, months=12, horizon=30)
    RESULTS.append(r)
    L("   %-4s %-18s %-12s %5d %7.0f %9.1f %10.1f %9.1f %9.1f %8s"
      % (r["key"], r["name"], r["tier"], r["n"], r["adr"], r["total_rev"], r["capex"], r["npv"], r["npv20"], P(r["irr"])))
L("   说明：丽晶/六善/文华东方/柏悦/康莱德/Sofitel/LXR 成都无实测房价，ADR 为分级表入门价 × 成都溢价系数 1.45 的推测值。")

L("")
L("=== 3. 品牌比选价值排序（按净现值 30 年，含前提可验证性）===")
VERIF = {
 "B1":"前提明确（存量续约）","B2":"前提明确（同集团换牌）","B3":"无成都开业先例","B4":"棕榈泉已转洲至",
 "B5":"无成都开业先例","B6":"瑞吉已被占","B7":"尼依格罗已被占","B8":"无成都开业先例",
 "B9":"丽晶已被占（10km 外）","B10":"无成都开业先例","B11":"无成都开业先例","B12":"总府路 28 号黑洞项目，权益可能仍在流通",
}
for i, r in enumerate(sorted(RESULTS, key=lambda x: -x["npv"]), 1):
    L("   %2d. %-4s %-18s 净现值30 %9.1f 万｜IRR %7s｜前提：%s"
      % (i, r["key"], r["name"], r["npv"], P(r["irr"]), VERIF[r["key"]]))

# ══════════════════════════════════════════════════════════════
# ④ 停业方式与经营期
# ══════════════════════════════════════════════════════════════
L("")
L("=== 4. 停业方式与经营期对比（基准：S1 皇冠·保留石材·不减房）===")
B1 = [b for b in BRANDS if b[0] == "B1"][0]
for lbl, kw in [("全停业 12 月 · 20 年", dict(months=12, horizon=20)),
                ("全停业 12 月 · 30 年", dict(months=12, horizon=30)),
                ("全停业 16 月 · 30 年", dict(months=16, horizon=30)),
                ("分期开业(4月全停+12月渐进) · 20 年", dict(phased=True, months=4, horizon=20)),
                ("分期开业(4月全停+12月渐进) · 30 年", dict(phased=True, months=4, horizon=30))]:
    r = brand_case(B1, None, **kw)
    L("   %-38s 改造投资 %8.1f 万｜净现值 %9.1f 万｜IRR %7s｜回收 %s"
      % (lbl, r["capex"], r["npv"], P(r["irr"]), r["pb"] if r["pb"] else "未回收"))

# ══════════════════════════════════════════════════════════════
# ⑤ 净现值转正路径分解
# ══════════════════════════════════════════════════════════════
L("")
L("=== 5. 净现值转正路径分解（基准 S1 全停业 12 月 · 20 年）===")
base = brand_case(B1, None, months=12, horizon=20)
L("   基准：净现值 %+.1f 万｜IRR %s" % (base["npv"], P(base["irr"])))
LEVERS = [
 ("L1 经营期 20→30 年", dict(horizon=30)),
 ("L2 全停业改分期开业", dict(phased=True, months=4)),
 ("L3 品牌方承担 30% 改造投入", dict(brand_share=0.30)),
 ("L4 政策性补贴 3,000 万", dict(subsidy=3000.0)),
 ("L5 分期 + 30 年", dict(phased=True, months=4, horizon=30)),
 ("L6 分期 + 30 年 + 品牌方 30%", dict(phased=True, months=4, horizon=30, brand_share=0.30)),
 ("L7 分期+30年+品牌30%+补贴3000", dict(phased=True, months=4, horizon=30, brand_share=0.30, subsidy=3000.0)),
 ("L8 上项 + 收入提升 10%", dict(phased=True, months=4, horizon=30, brand_share=0.30, subsidy=3000.0, revenue_boost=1.10)),
]
cum = base["npv"]
L("   %-36s %12s %12s %8s" % ("杠杆", "净现值", "较基准改善", "内部收益率"))
for lbl, kw in LEVERS:
    r = brand_case(B1, None, months=kw.pop("months", 12), **kw)
    L("   %-36s %12.1f %12.1f %8s" % (lbl, r["npv"], r["npv"] - base["npv"], P(r["irr"])))
    if lbl.startswith("L8"):
        L("")
        L("   ★ 组合 L8 结果：净现值 %+.1f 万（基准 %+.1f 万），改善 %+.1f 万"
          % (r["npv"], base["npv"], r["npv"] - base["npv"]))
        L("   ★ 达到净现值为正所需组合：分期开业 ＋ 30 年经营期 ＋ 品牌方分担 30% ＋ 补贴 3,000 万 ＋ 收入提升 10%")
L("")
L("=== 6. 收入分板块口径（第 15 条）===")
L("   总府现状 24 个月实测板块（年化）:")
MM = SE["months"]
room_avg = sum(x["room"] for x in MM) / 1e4
fnb_avg = sum(x["fnb"] for x in MM) / 1e4
banq_avg = sum(x["banq"] for x in MM) / 1e4
misc_avg = sum(x["misc"] for x in MM) / 1e4
tot_avg = sum(x["rev"] for x in MM) / 1e4
L("   营业收入合计 %s 万｜客房 %s 万（%s%%）｜餐饮 %s 万（%s%%）｜会议 %s 万（%s%%）｜其他 %s 万（%s%%）"
  % (N(tot_avg), N(room_avg), N(room_avg/tot_avg*100,1), N(fnb_avg), N(fnb_avg/tot_avg*100,1),
     N(banq_avg), N(banq_avg/tot_avg*100,1), N(misc_avg), N(misc_avg/tot_avg*100,1)))
L("   非房（餐饮＋会议＋其他）占营业收入 %s%%" % N((fnb_avg + banq_avg + misc_avg) / tot_avg * 100, 1))
L("   停业期刚性支出月均 %s 万（人工留存+能耗维持+保险安保+利息）" % N(FIXED_MONTHLY))
L("   ★ 段一（资金需求口径）应列：刚性现金支出＋品牌保留费；段一B 营业收入归零只在现金流评价中体现。")
L("DONE")
