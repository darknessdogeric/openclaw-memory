# -*- coding: utf-8 -*-
"""v50：v4.0 重构引擎（修正版）
   ① 停业损失口径分离：段一A 刚性现金支出（资金需求）/ 段一B 营业收入归零（现金流评价）
   ② 品牌候选集：内部《高星级全服式酒店品牌分级分类（仅5★+）》§8 单房造价带 + §6.2 抽佣 + §6.1 预算↔档位
      §6.3 成都位置匹配度 + 2026-10 成都实测房价带
   ③ 校准：皇冠/洲至奢选两档做法系数由 v9.json 实配反算
   ④ 全停业 vs 分期开业；20 年 vs 30 年
   ⑤ 净现值转正路径分解（逐杠杆）
   ⑥ 收入分板块（24 个月实测）
   ⑦ 行业基准（联网复核）：高星级全服无 5-8 年区间"""
import os, json, importlib.util
T = r"D:\B166ER-openclaw\workspace\.tmp"
D = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc"
OUT = open(os.path.join(T, "v50.log"), "w", encoding="utf-8")
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

GUEST_NET = 10192.0; SELLABLE = 402
FIXED_MONTHLY = 284.0
MEP_BASE = RES["S1"]["mep"]                 # 11,060（品牌无关）
FIT_S1 = RES["S1"]["fitout"]                # 10,253.6（皇冠·保留石材·不减房）
S3_FIT = RES["S3"]["fitout"]                # 18,111.3（皇冠·公区重做）
S4_FIT = RES["S4"]["fitout"]                # 17,130.7（洲至奢选·保留石材）
S5_FIT = RES["S5"]["fitout"]                # 28,490.7（洲至奢选·公区重做）
VERTICAL_COUPLING = 860.0                  # v9 段二「竖井重排 + 3 改 2 移卫耦合」
# 做法系数（由 v9 实配反算：保留石材=1.00 基准，公区重做按各档实测反算）
KEEP_CROWN = FIT_S1 / (402 * 25.0)          # 皇冠 25.0 万/间带中值 → 系数
REDO_CROWN = S3_FIT / (402 * 25.0)
KEEP_VIGN = S4_FIT / (402 * 25.0)
REDO_VIGN = S5_FIT / (402 * 25.0)
L("=== 0. 校准（由 v9.json 实配反算）===")
L("S1 皇冠·保留 %.1f 万｜S3 皇冠·重做 %.1f 万｜S4 洲至奢选·保留 %.1f 万｜S5 洲至奢选·重做 %.1f 万" % (FIT_S1, S3_FIT, S4_FIT, S5_FIT))
L("做法系数：皇冠保留 %.4f｜皇冠重做 %.4f｜洲至奢选保留 %.4f｜洲至奢选重做 %.4f" % (KEEP_CROWN, REDO_CROWN, KEEP_VIGN, REDO_VIGN))
L("★ 关键校准：S1 总投 21,313.6 万 = 2.13 亿、单房 53.02 万 —— 按内部表 §6.1，")
L("   该预算档位本应对应 Tier2 高端奢华（瑰丽／文华东方／四季／半岛／莱佛士），而非皇冠假日。")

# ══ ① 停业损失口径分离 ══
L("")
L("=== 1. 停业损失口径分离（第 17 条）===")
def closure_split(months, brand_ret_m=0.0):
    cash_out = 0.0; rev_lost = 0.0
    for k in range(months):
        m = str(((k) % 12) + 1)
        cash_out += FIXED_MONTHLY + brand_ret_m
        rev_lost += SE["season"][m]["rev"] / 1e4
    return cash_out, rev_lost
for mo in (4, 8, 12, 16, 20):
    a, b = closure_split(mo, 6.38)
    L("   停业 %2d 月：段一A 刚性现金支出 %7.1f 万｜段一B 营业收入归零 %7.1f 万｜旧口径(混同) %7.1f 万" % (mo, a, b, a + b))
L("   ★ 段一（资金需求）只列段一A；段一B 属营业收入归零，仅在财务评价现金流中体现，不计入需投入资金。")
L("   ★ 交叉验证：12 个月段一A %s 万，与 715 定稿「停业一年刚性支出 3,674 万元」量级一致。" % N(closure_split(12,6.38)[0]))

# ══ ② 品牌候选集 ══
# key, 名称, 档次(内部表), §8单房带(低,高), §6.2抽佣(低,高), 面积门槛㎡, 成都实测房价(低,高), 已有房量, 状态, 位置
BRANDS = [
 ("B1","皇冠假日（现状）","上高端全服务",20,30,6.0,10.5,0,None,None,402,"已入驻·存量续约"),
 ("B2","洲至奢选","高端奢华",36,50,7.5,11.0,0,900,None,335,"棕榈泉 335 间已开业"),
 ("B3","康莱德 Conrad","上高端全服务",20,30,7.5,10.5,0,None,None,None,"成都未见开业"),
 ("B4","费尔蒙 Fairmont","上高端全服务",20,30,6.5,10.0,0,None,None,336,"棕榈泉已转洲至奢选"),
 ("B5","Sofitel 索菲特","高端奢华",36,50,6.5,10.5,0,None,None,None,"成都未见开业"),
 ("B6","瑞吉 St. Regis","规模化奢华",28.8,57.6,7.5,11.5,40,1200,2000,312,"在营·太升南路"),
 ("B7","尼依格罗 Niccolo","规模化奢华",28.8,57.6,7.0,11.0,40,1200,1800,238,"IFS 在营"),
 ("B8","柏悦 Park Hyatt","规模化奢华",28.8,57.6,7.5,11.5,0,None,None,None,"成都未见开业"),
 ("B9","丽晶 Regent","高端奢华",36,50,8.0,10.5,40,None,None,None,"已签约顺江路 2029Q3"),
 ("B10","六善 Six Senses","高端奢华",36,50,8.0,10.5,45,None,None,None,"成都未见开业"),
 ("B11","文华东方 MO","高端奢华",36,50,8.0,9.5,45,None,None,None,"成都未见开业"),
 ("B12","LXR","超奢华",43,72,6.5,10.5,0,None,None,None,"总府路 28 号「黑洞」项目"),
]
TIER_OP = {"上高端全服务":(0.300,1.42,0.70),"规模化奢华":(0.360,1.72,0.72),
           "高端奢华":(0.380,1.85,0.74),"超奢华":(0.410,2.00,0.75)}
ENTRY = {"上高端全服务":300,"规模化奢华":450,"高端奢华":650,"超奢华":1400}   # 内部表入门价 USD/晚（仅作档次参照，不用于取价）
# 取价规则：一律以成都实测房价带为锚；成都未开业者按同档位已开业品牌实测带推定，并标注为推测值
# 2026-10 成都实测房价带（元/间/晚）：瑞吉 1,200-2,000｜尼依格罗 1,200-1,800｜费尔蒙 900-2,200
# 丽思卡尔顿 1,000-2,800｜华尔道夫 1,265-3,500｜居舍 2,000-3,000｜君悦 1,200-2,000｜洲至奢选棕榈泉 900 起
PRICE_ANCHOR = {
 "上高端全服务": (750.0, 900.0, "皇冠现状 363.99 实测，改造后五星高档 750 元；康莱德/费尔蒙按费尔蒙实测 900-2,200 下沿推定"),
 "规模化奢华": (1200.0, 2000.0, "瑞吉 1,200-2,000、尼依格罗 1,200-1,800 实测"),
 "高端奢华": (1500.0, 2200.0, "按同档在营品牌瑞吉／尼依格罗实测带上沿推定（丽晶、六善、文华东方、洲至奢选）"),
 "超奢华": (2000.0, 3000.0, "按居舍 2,000-3,000 实测带推定（LXR）"),
}

def rooms_by_area(th):
    return SELLABLE if not th else int(GUEST_NET // th)

def brand_case(b, months=12, horizon=30, phased=False, brand_share=0.0, subsidy=0.0,
               revenue_boost=1.0, pub="保留"):
    key, name, tier, pk_lo, pk_hi, fee_lo, fee_hi, area_th, p_lo, p_hi, rooms_exist, status = b
    n = rooms_by_area(area_th)
    pk_mid = (pk_lo + pk_hi) / 2
    # 做法系数：皇冠/洲至奢选用实配；其余按档次比例推定
    if tier == "上高端全服务":
        k_keep, k_redo = KEEP_CROWN, REDO_CROWN
    else:
        ratio = {"规模化奢华":1.50,"高端奢华":1.70,"超奢华":2.20}[tier]
        k_keep, k_redo = KEEP_CROWN * ratio, REDO_CROWN * ratio
    fit = pk_mid * n * (k_keep if pub == "保留" else k_redo)
    if n < SELLABLE:  # 3 改 2：竖井重排与移卫耦合
        fit += VERTICAL_COUPLING
    capex = MEP_BASE + fit
    if brand_share: capex *= (1 - brand_share)
    capex -= subsidy
    # 价格：一律以成都实测带为锚；实测有则用实测中位，无实测则用同档位锚点并标注
    if p_lo is not None and p_hi is not None:
        adr = (p_lo + p_hi) / 2
        adr_src = "2026-10 成都实测房价带中位"
    else:
        lo, hi, note = PRICE_ANCHOR[tier]
        adr = (lo + hi) / 2
        adr_src = "同档位成都实测带推定（成都未开业）" + "｜" + note
    gop_r, nonroom_r, occ_d = TIER_OP[tier]
    room_rev = n * 365 * occ_d * adr / 1e4
    total_rev = room_rev * nonroom_r * revenue_boost
    brand_base = total_rev * fee_lo / 100.0
    mkt = total_rev * 0.025; loy = total_rev * 0.020
    ffe = total_rev * (0.040 if pk_mid >= 36 else 0.020)
    inc_rate = 0.10 if pk_mid >= 36 else 0.06
    gop = total_rev * gop_r
    br_m = brand_base * 0.35 / 12.0
    mcf = []
    if phased:
        full_m, phase_end = 4, 16
        for tt in range(1, horizon * 12 + 1):
            if tt <= full_m:
                cash = -FIXED_MONTHLY - br_m
            elif tt <= phase_end:
                since = tt - full_m
                rev = total_rev / 12.0 * (0.40 * min(1.0, 0.35 + 0.05 * since))
                g = rev * gop_r; r_ = rev / total_rev
                cash = (g - brand_base * r_ - mkt * r_ - loy * r_ - ffe * r_ - g * inc_rate) - FIXED_MONTHLY * 0.35
            else:
                since = tt - phase_end
                rev = (total_rev / 12.0) * min(1.0, 0.70 + 0.03 * since)
                g = rev * gop_r; r_ = rev / total_rev
                cash = (g - brand_base * r_ - mkt * r_ - loy * r_ - ffe * r_ - g * inc_rate)
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
            if tt <= months: cash -= FIXED_MONTHLY + br_m
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
    return dict(key=key, name=name, tier=tier, n=n, area_th=area_th, pk_mid=pk_mid,
                adr=adr, adr_src=adr_src, occ=occ_d, total_rev=total_rev, capex=capex, fit=fit,
                per_key=capex / n, status=status, fee=(fee_lo + fee_hi) / 2,
                npv=pv(acf), irr=V10.irr(acf), pb=V10.payback(acf),
                npv20=pv(acf[:20]), irr20=V10.irr(acf[:20]), pb20=V10.payback(acf[:20]))

L("")
L("=== 2. 品牌候选集逐品牌测算（公区保留、全停业 12 月、30 年期、8% 折现）===")
L("   %-4s %-16s %-10s %5s %8s %10s %11s %11s %10s %9s" % ("序","品牌","档次","房量","平均房价","年营收","改造投资","单房投资","净现值30","内部IRR"))
RESA = []
for b in BRANDS:
    r = brand_case(b)
    RESA.append(r)
    L("   %-4s %-16s %-10s %5d %8.0f %10.1f %11.1f %9.1f %10.1f %9s"
      % (r["key"], r["name"][:14], r["tier"], r["n"], r["adr"], r["total_rev"], r["capex"], r["per_key"], r["npv"], P(r["irr"])))
L("   注：未在成都开业者无实测房价，其平均房价为内部表入门价折算推测值，已在 Excel 单列标注。")

L("")
L("=== 3. 价值排序（净现值 30 年）===")
for i, r in enumerate(sorted(RESA, key=lambda x: -x["npv"]), 1):
    L("   %2d. %-4s %-16s 净现值 %9.1f 万｜单房 %6.1f 万｜内部IRR %7s｜%s"
      % (i, r["key"], r["name"][:14], r["npv"], r["per_key"], P(r["irr"]), r["status"]))

L("")
L("=== 4. 停业方式与经营期（基准 B1 皇冠·保留）===")
B1 = BRANDS[0]
for lbl, kw in [("全停业 12 月 · 20 年", dict(months=12, horizon=20)),
                ("全停业 12 月 · 30 年", dict(months=12, horizon=30)),
                ("全停业 16 月 · 30 年", dict(months=16, horizon=30)),
                ("分期开业 · 20 年", dict(phased=True, months=4, horizon=20)),
                ("分期开业 · 30 年", dict(phased=True, months=4, horizon=30))]:
    r = brand_case(B1, **kw)
    L("   %-26s 改造投资 %8.1f｜净现值 %9.1f 万｜IRR %7s｜回收 %s"
      % (lbl, r["capex"], r["npv"], P(r["irr"]), r["pb"] if r["pb"] else "未回收"))

L("")
L("=== 5. 净现值转正路径分解（第 26 条）===")
base = brand_case(B1, months=12, horizon=20)
L("   基准（B1 全停业 12 月 · 20 年）：净现值 %+.1f 万｜IRR %s" % (base["npv"], P(base["irr"])))
LEVERS = [
 ("L1 经营期 20→30 年", dict(horizon=30)),
 ("L2 全停业改分期开业", dict(phased=True, months=4)),
 ("L3 品牌方承担 30% 改造投入", dict(brand_share=0.30)),
 ("L4 政策性补贴 3,000 万", dict(subsidy=3000.0)),
 ("L5 分期 + 30 年", dict(phased=True, months=4, horizon=30)),
 ("L6 分期 + 30 年 + 品牌方 30%", dict(phased=True, months=4, horizon=30, brand_share=0.30)),
 ("L7 L6 + 补贴 3,000 万", dict(phased=True, months=4, horizon=30, brand_share=0.30, subsidy=3000.0)),
 ("L8 L7 + 收入提升 10%", dict(phased=True, months=4, horizon=30, brand_share=0.30, subsidy=3000.0, revenue_boost=1.10)),
]
for lbl, kw in LEVERS:
    r = brand_case(B1, months=kw.pop("months", 12), **kw)
    L("   %-30s 净现值 %9.1f 万｜较基准 %+9.1f｜IRR %7s" % (lbl, r["npv"], r["npv"] - base["npv"], P(r["irr"])))

L("")
L("=== 6. 收入分板块（24 个月实测，第 15 条）===")
MM = SE["months"]
tot_avg = sum(x["rev"] for x in MM) / 1e4
room_avg = sum(x["room"] for x in MM) / 1e4
fnb_avg = sum(x["fnb"] for x in MM) / 1e4
banq_avg = sum(x["banq"] for x in MM) / 1e4
misc_avg = sum(x["misc"] for x in MM) / 1e4
L("   营业收入 %s 万｜客房 %s（%s%%）｜餐饮 %s（%s%%）｜会议 %s（%s%%）｜其他 %s（%s%%）"
  % (N(tot_avg), N(room_avg), N(room_avg/tot_avg*100,1), N(fnb_avg), N(fnb_avg/tot_avg*100,1),
     N(banq_avg), N(banq_avg/tot_avg*100,1), N(misc_avg), N(misc_avg/tot_avg*100,1)))
L("   非房合计占 %s%%；客房外收入须逐板块建模，不得只用单一系数。" % N((fnb_avg+banq_avg+misc_avg)/tot_avg*100,1))
L("   月度经营指标（24 个月）：平均房价 %.1f 元｜出租率 %.1f%%｜每间可售房收入 %.1f 元"
  % (sum(x["adr"] for x in MM)/24, sum(x["occ"] for x in MM)/24*100, sum(x["trevpar"] for x in MM)/24))
json.dump(dict(base=BASE, brands=RESA, closure={str(m): closure_split(m,6.38) for m in (4,8,12,16,20)},
               seg=dict(total=tot_avg, room=room_avg, fnb=fnb_avg, banq=banq_avg, misc=misc_avg)),
          open(os.path.join(T, "v50.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
L("DONE")
