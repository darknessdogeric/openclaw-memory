# -*- coding: utf-8 -*-
"""v51：v4.0 重构模型（口径全部校正后重算）
   校正项：
   ① 改造前基线：24 个月实测均值 ADR 427.4 元 / OCC 72.55% → 客房收入 4,551.8 万（USALI 利润表交叉验证）
      旧值 363.99 元为 2026-09 单月低点，低估客房收入 771.6 万（20.4%）
   ② 收入板块显式建模：客房 / 餐饮 / 会议 / 其他（不再用单一非房系数）
   ③ 停业损失口径分离：段一A 刚性现金支出（资金需求）/ 段一B 营业收入归零（现金流评价）
   ④ 品牌候选集：内部《高星级全服式酒店分级分类（仅5★+）》§8 单房造价带 + §6.2 抽佣 + §6.3 成都位置
      + 2026-10 成都实测房价带（缺口按同档位在营品牌推定并标注）
   ⑤ 净现值为正的可行路径分解
   ⑥ 自建品牌路径（锦宾国际）单列
   ⑦ 人防（部分地下层六级）专项处置三方案与造价"""
import os, json, importlib.util
T = r"D:\B166ER-openclaw\workspace\.tmp"
D = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc"
OUT = open(os.path.join(T, "v51.log"), "w", encoding="utf-8")
def L(*a):
    OUT.write(" ".join(str(z) for z in a) + "\n"); OUT.flush()
spec = importlib.util.spec_from_file_location("v10", os.path.join(D, "v10_econ.py"))
V10 = importlib.util.module_from_spec(spec); spec.loader.exec_module(V10)
RES = {x["key"]: x for x in json.load(open(os.path.join(T, "v9.json"), encoding="utf-8"))}
SE = json.load(open(os.path.join(D, "seasonal_24m.json"), encoding="utf-8"))
MM = SE["months"]
def N(v, d=1): return format(round(v, d), ",.%df" % d)
def P(v): return ("%.2f%%" % (v * 100)) if v is not None else "无可解"
GUEST_NET = 10192.0; SELLABLE = 402
FIXED_MONTHLY = 284.0

# ══ ① 改造前基线（24 个月实测）═════════════════════════════════════
ADR0 = sum(x["adr"] for x in MM) / 24
OCC0 = sum(x["occ"] for x in MM) / 24
REV0 = sum(x["rev"] for x in MM) / 1e4 / 2
ROOM0 = sum(x["room"] for x in MM) / 1e4 / 2
FNB0 = sum(x["fnb"] for x in MM) / 1e4 / 2
BANQ0 = sum(x["banq"] for x in MM) / 1e4 / 2
MISC0 = sum(x["misc"] for x in MM) / 1e4 / 2
GOP0 = sum(x["gop"] for x in MM) / 1e4 / 2
LAB0 = sum(x["labor"] for x in MM) / 1e4 / 2
ENG0 = sum(x["energy"] for x in MM) / 1e4 / 2
MNT0 = sum(x["maint"] for x in MM) / 1e4 / 2
BASE = dict(rooms=SELLABLE, adr=ADR0, occ=OCC0, room_rev=ROOM0, fnb=FNB0, banq=BANQ0,
            misc=MISC0, total_rev=REV0, gop=GOP0, gop_rate=GOP0 / REV0, labor=LAB0,
            energy=ENG0, maint=MNT0, old_adr=363.99, old_occ=0.7078, old_room_rev=3780.2)
L("=== 1. 改造前基线（24 个月实测，USALI 利润表交叉验证）===")
L("   平均房价 %.1f 元｜出租率 %.2f%%｜每间可售房收入 %.1f 元" % (ADR0, OCC0 * 100, sum(x["trevpar"] for x in MM) / 24))
L("   营业收入 %s 万｜客房 %s（%.1f%%）｜餐饮 %s（%.1f%%）｜会议 %s（%.1f%%）｜其他 %s（%.1f%%）"
  % (N(REV0), N(ROOM0), ROOM0/REV0*100, N(FNB0), FNB0/REV0*100, N(BANQ0), BANQ0/REV0*100, N(MISC0), MISC0/REV0*100))
L("   反算校验：%d 间 × 365 × %.4f × %.1f = %s 万元  vs USALI 实测客房收入 %s 万元"
  % (SELLABLE, OCC0, ADR0, N(SELLABLE*365*OCC0*ADR0/1e4), N(ROOM0)))
L("   营业利润 %s 万元（部门营业利润率 %.1f%%）｜人工 %s 万｜能耗 %s 万｜维修 %s 万"
  % (N(GOP0), GOP0/REV0*100, N(LAB0), N(ENG0), N(MNT0)))
L("   ★ 旧稿基线：ADR 363.99（2026-09 单月低点）× OCC 70.78%% → 客房收入 3,780.2 万，低估 %.1f 万元（%.1f%%）。"
  % (ROOM0 - 3780.2, (ROOM0/3780.2-1)*100))
L("   ★ 总营收 %s 万无误，但旧稿收入结构错误（客房实为 %.1f%%，非 55.8%%）。" % (N(REV0), ROOM0/REV0*100))
NONROOM_SHARE = (FNB0+BANQ0+MISC0)/REV0
SPLIT = dict(fnb=FNB0/(FNB0+BANQ0+MISC0), banq=BANQ0/(FNB0+BANQ0+MISC0), misc=MISC0/(FNB0+BANQ0+MISC0))

# ══ ② 停业损失口径分离 ════════════════════════════════════════════
L("")
L("=== 2. 停业损失口径分离 ===")
def closure_split(months, brand_ret_m=0.0):
    co = 0.0; rl = 0.0
    for k in range(months):
        m = str((k % 12) + 1)
        co += FIXED_MONTHLY + brand_ret_m
        rl += SE["season"][m]["rev"] / 1e4 / 2
    return co, rl
CL = {}
for mo in (4, 8, 12, 16, 20):
    a, b = closure_split(mo, 6.38); CL[mo] = (a, b)
    L("   停业 %2d 月：段一A 刚性现金支出 %7.1f 万（计入资金需求）｜段一B 营业收入归零 %7.1f 万（仅入现金流）" % (mo, a, b))
L("   ★ 715 定稿交叉验证：停业一年刚性支出 3,674 万元，本模型 12 个月段一A %s 万元。" % N(CL[12][0]))

# ══ ③ 品牌候选集 ══════════════════════════════════════════════════
# 内部表 §8 单房改造造价带（万元/间）｜§6.2 抽佣合计｜§6.3 成都位置
# 2026-10 成都实测房价带（元/间/晚）
BRANDS = [
 # key, 名称, 档次, 内部表带(低,高), 抽佣(低,高), 面积门槛㎡, 成都实测价(低,高), 已有房量, 成都现状, 特征, 位置空位
 ("B01","皇冠假日（现状续约）","上高端全服务",20,30,6.0,10.5,0,None,None,402,"在营 30 年｜IHG One Rewards 体系｜会员匹配评分 48（五强垫底）","存量续约"),
 ("B02","洲至奢选 Vignette","高端奢华",36,50,7.5,11.0,0,900,1500,335,"成都棕榈泉 335 间 2026 年已开业｜同属 IHG 体系｜「特色奢华酒店收藏家」定位｜实测约 900 元起（$127）","同集团可换"),
 ("B03","康莱德 Conrad","上高端全服务",20,30,7.5,10.5,0,None,None,None,"希尔顿系｜设计驱动｜Hilton Honors 会员匹配 88 分（五强最高）｜成都未见开业","空位"),
 ("B04","费尔蒙 Fairmont","上高端全服务",20,30,6.5,10.0,0,900,2200,336,"地标建筑导向｜Accor ALL 体系｜成都唯一原费尔蒙物业即现洲至奢选棕榈泉（实测 900—2,200 元）｜无独立在营物业","已被占"),
 ("B05","Sofitel 索菲特","高端奢华",36,50,6.5,10.5,0,None,None,None,"雅高系｜设计驱动｜成都未见开业","空位"),
 ("B06","瑞吉 St. Regis","规模化奢华",28.8,57.6,7.5,11.5,40,1200,2000,312,"万豪系｜管家服务｜太升南路｜春熙路核心圈外围｜实测 1,200—2,000 元（另测 980—2,500 元）","已被占"),
 ("B07","尼依格罗 Niccolo","规模化奢华",28.8,57.6,7.0,11.0,40,1200,1800,238,"九龙仓｜IFS 3 号楼｜大慈寺景｜春熙路正位｜实测 1,200—1,800 元（另测 1,191—2,800 元）","已被占"),
 ("B08","柏悦 Park Hyatt","规模化奢华",28.8,57.6,7.5,11.5,0,None,None,None,"凯悦系｜Hyatt Dynasty｜成都未见开业","空位"),
 ("B09","丽晶 Regent","高端奢华",36,50,8.0,10.5,40,None,None,None,"IHG 顶奢｜锦江顺江路已签约 2029Q3 开业｜距本项目约 10 公里","已被占"),
 ("B10","六善 Six Senses","高端奢华",36,50,8.0,10.5,45,None,None,None,"IHG 奢华板块｜养生导向｜成都未见开业","空位"),
 ("B11","文华东方 MO","高端奢华",36,50,8.0,9.5,45,None,None,None,"怡和系｜姿态高｜成都未见开业","空位"),
 ("B12","LXR 希尔顿超奢","超奢华",43,72,6.5,10.5,0,None,None,None,"希尔顿超奢｜中国仅西安官宣 1 家｜成都总府路 28 号曾单方官宣后无落地","重大空位"),
]
TIER_OP = {"上高端全服务":(0.300,0.70),"规模化奢华":(0.360,0.72),"高端奢华":(0.380,0.74),"超奢华":(0.410,0.75)}
NONROOM_T = {"上高端全服务":NONROOM_SHARE,"规模化奢华":0.35,"高端奢华":0.38,"超奢华":0.42}
PRICE_ANCHOR = {"上高端全服务":(750.0,900.0),"规模化奢华":(1200.0,2000.0),
                "高端奢华":(1500.0,2200.0),"超奢华":(2000.0,3000.0)}
# 造价系数（由 v9 实配反算，按档次缩放）
KEEP_CROWN = RES["S1"]["fitout"] / (402 * 25.0)
REDO_CROWN = RES["S3"]["fitout"] / (402 * 25.0)
TIER_FIT = {"上高端全服务":1.0,"规模化奢华":1.45,"高端奢华":1.66,"超奢华":2.05}

def rooms_by_area(th): return SELLABLE if not th else int(GUEST_NET // th)

def revenue_segments(n, adr, occ, tier, boost=1.0):
    """显式建模：客房 → 总营收 → 餐饮/会议/其他"""
    room_rev = n * 365 * occ * adr / 1e4 * boost
    nonroom_share = NONROOM_T[tier]
    total = room_rev / (1 - nonroom_share)
    return dict(room=room_rev, total=total,
                fnb=total * nonroom_share * SPLIT["fnb"],
                banq=total * nonroom_share * SPLIT["banq"],
                misc=total * nonroom_share * SPLIT["misc"],
                nonroom_share=nonroom_share)

def brand_case(b, months=12, horizon=30, phased=False, brand_share=0.0, subsidy=0.0,
               boost=1.0, pub="保留", own_brand=False):
    key, name, tier, pk_lo, pk_hi, fee_lo, fee_hi, area_th, p_lo, p_hi, rooms_exist, feat, loc = b
    n = rooms_by_area(area_th)
    pk_mid = (pk_lo + pk_hi) / 2
    if own_brand:
        fit = pk_mid * n * KEEP_CROWN * 0.92     # 自有品牌无需外方标准溢价，按皇冠实配下调
        fee_lo, fee_hi = 0.0, 0.0
    else:
        kf = TIER_FIT[tier]
        kk = (KEEP_CROWN if pub == "保留" else REDO_CROWN) * kf / 1.0
        fit = pk_mid * n * kk
    if n < SELLABLE: fit += 860.0     # 竖井重排 + 3 改 2 移卫耦合（v9 段二）
    capex = 11060.0 + fit
    if brand_share: capex *= (1 - brand_share)
    capex -= subsidy
    if p_lo is not None and p_hi is not None:
        adr = (p_lo + p_hi) / 2; adr_src = "2026-10 成都实测房价带中位"
    else:
        lo, hi = PRICE_ANCHOR[tier]; adr = (lo + hi) / 2
        adr_src = "同档位成都实测带推定（成都未开业，推测值）"
    gop_r, occ = TIER_OP[tier]
    seg = revenue_segments(n, adr, occ, tier, boost)
    total = seg["total"]
    brand_base = total * fee_lo / 100.0
    mkt = total * 0.025; loy = total * 0.020
    ffe = total * (0.040 if pk_mid >= 36 else 0.020)
    inc_rate = 0.10 if pk_mid >= 36 else 0.06
    gop = total * gop_r
    br_m = brand_base * 0.35 / 12.0
    mcf = []
    if phased:
        full_m, phase_end = 4, 16
        for tt in range(1, horizon * 12 + 1):
            if tt <= full_m:
                cash = -FIXED_MONTHLY - br_m
            elif tt <= phase_end:
                since = tt - full_m
                r = total / 12.0 * (0.40 * min(1.0, 0.35 + 0.05 * since))
                gg = r * gop_r; rr = r / total
                cash = (gg - brand_base*rr - mkt*rr - loy*rr - ffe*rr - gg*inc_rate) - FIXED_MONTHLY*0.35
            else:
                since = tt - phase_end
                r = (total / 12.0) * min(1.0, 0.70 + 0.03 * since)
                gg = r * gop_r; rr = r / total
                cash = (gg - brand_base*rr - mkt*rr - loy*rr - ffe*rr - gg*inc_rate)
            if tt <= 18: cash -= capex / 18.0
            mcf.append(cash)
    else:
        for tt in range(1, horizon * 12 + 1):
            r = 0.0
            if tt > months:
                since = tt - months
                r = (total / 12.0) * min(1.0, 0.62 + 0.038 * since)
            gg = r * gop_r; rr = r / total if total else 0
            cash = (gg - brand_base*rr - mkt*rr - loy*rr - ffe*rr - gg*inc_rate)
            if tt <= months: cash -= FIXED_MONTHLY + br_m
            half = max(1, months // 2)
            if 1 <= tt <= half: cash -= capex * 0.6 / half
            elif half < tt <= months: cash -= capex * 0.4 / max(1, months - half)
            if tt > months:
                since = tt - months
                if since < 12: cash -= total * 0.085 / 12.0
                elif since < 24: cash -= total * 0.030 / 12.0
                if since < 6: cash -= total * 0.012 / 6.0
            mcf.append(cash)
    acf = [round(sum(mcf[y*12:(y+1)*12]), 1) for y in range(horizon)]
    def pv(cf, r=0.08): return round(sum(c/(1+r)**i for i, c in enumerate(cf)), 1)
    return dict(key=key, name=name, tier=tier, n=n, area_th=area_th, pk_mid=pk_mid,
                fee=(fee_lo+fee_hi)/2, adr=adr, adr_src=adr_src, occ=occ, fit=fit, capex=capex,
                per_key=capex/n, seg=seg, gop_rate=gop_r, loc=loc, feat=feat,
                npv=pv(acf), irr=V10.irr(acf), pb=V10.payback(acf),
                npv20=pv(acf[:20]), irr20=V10.irr(acf[:20]), pb20=V10.payback(acf[:20]))

L("")
L("=== 3. 品牌候选集测算（公区保留、全停业 12 月、30 年期、8% 折现）===")
L("   %-4s %-18s %-10s %4s %7s %9s %10s %10s %9s %9s" % ("序","品牌","档次","房量","平均房价","年营收","改造投资","单房投资","净现值30","内部IRR"))
RESA = []
for b in BRANDS:
    r = brand_case(b); RESA.append(r)
    L("   %-4s %-18s %-10s %4d %7.0f %9.1f %10.1f %9.1f %9.1f %9s"
      % (r["key"], r["name"][:16], r["tier"], r["n"], r["adr"], r["seg"]["total"], r["capex"], r["per_key"], r["npv"], P(r["irr"])))
L("   收入结构（基准 B01）：客房 %s｜餐饮 %s｜会议 %s｜其他 %s"
  % (N(RESA[0]["seg"]["room"]), N(RESA[0]["seg"]["fnb"]), N(RESA[0]["seg"]["banq"]), N(RESA[0]["seg"]["misc"])))

L("")
L("=== 4. 价值排序（净现值 30 年，含前提可验证性）===")
for i, r in enumerate(sorted(RESA, key=lambda x: -x["npv"]), 1):
    L("   %2d. %-4s %-18s 净现值 %9.1f 万｜单房 %6.1f 万｜IRR %7s｜%s"
      % (i, r["key"], r["name"][:16], r["npv"], r["per_key"], P(r["irr"]), r["loc"]))

L("")
L("=== 5. 自建品牌路径（锦宾国际）单列 ===")
own = brand_case(BRANDS[0], own_brand=True)
L("   集团自有高端品牌：抽佣 0｜净现值 %+.1f 万｜IRR %s｜单房投资 %6.1f 万"
  % (own["npv"], P(own["irr"]), own["per_key"]))
L("   对照 皇冠续约：净现值 %+.1f 万｜IRR %s" % (RESA[0]["npv"], P(RESA[0]["irr"])))

L("")
L("=== 6. 净现值转正路径（B01 皇冠基准）===")
base = brand_case(BRANDS[0], months=12, horizon=20)
L("   基准（全停业 12 月 · 20 年）：净现值 %+.1f 万｜IRR %s" % (base["npv"], P(base["irr"])))
PATHS = [
 ("P1 经营期 20→30 年", dict(horizon=30)),
 ("P2 全停业改分期开业", dict(phased=True, months=4)),
 ("P3 品牌方承担 30% 改造投入", dict(brand_share=0.30)),
 ("P4 政策性补贴 3,000 万", dict(subsidy=3000.0)),
 ("P5 分期开业 + 30 年", dict(phased=True, months=4, horizon=30)),
 ("P6 P5 + 品牌方 30%", dict(phased=True, months=4, horizon=30, brand_share=0.30)),
 ("P7 P6 + 补贴 3,000 万", dict(phased=True, months=4, horizon=30, brand_share=0.30, subsidy=3000.0)),
 ("P8 P7 + 收入提升 10%", dict(phased=True, months=4, horizon=30, brand_share=0.30, subsidy=3000.0, boost=1.10)),
]
for lbl, kw in PATHS:
    r = brand_case(BRANDS[0], months=kw.pop("months", 12), **kw)
    L("   %-28s 净现值 %9.1f 万｜较基准 %+9.1f｜IRR %7s" % (lbl, r["npv"], r["npv"]-base["npv"], P(r["irr"])))

L("")
L("=== 7. 人防（部分地下层六级）专项处置三方案 ====")
HUMAN = [("方案一 保持现状不动，仅补齐人防竣工资料与备案", "不触碰人防区，功能维持现状；须向成都警备区补报竣工资料并办理备案", 30, 70, "无施工风险，但 B2 泳池/员工厨房/冷源机房功能腾挪受限"),
         ("方案二 人防区功能腾挪并报请警备区变更", "将冷源机房与后场功能迁出人防区，局部拆除防护构件后重建并报批", 800, 1500, "触发人防工程变更审批，周期不可控；须先行取得警备区书面意见"),
         ("方案三 拆除人防功能并恢复普通地下室", "拆除防护结构与滤毒通风，恢复为普通地下室", 1500, 2600, "法律上须经警备区批准，实质不可能，不得作为基准方案")]
L("   %-38s %-58s %s" % ("方案", "内容", "造价（万元）｜风险"))
for a, b, c1, c2, d in HUMAN:
    L("   %-38s %-58s %d—%d｜%s" % (a, b, c1, c2, d))
L("   ★ 基准取方案一（30—70 万）。R-03 为唯一可能无法通过改造解决的项。")

L("")
L("=== 8. 敏感性（B01 基准，净现值 30 年）===")
b30 = brand_case(BRANDS[0], months=12, horizon=30)
for lbl, kw in [("平均房价 ±15%", dict(boost=1.15)), ("平均房价 −15%", dict(boost=0.85)),
                ("改造投资 ±15%", dict(subsidy=-21313.6*0.15)), ("改造投资 −15%", dict(subsidy=21313.6*0.15)),
                ("出租率 65%", None)]:
    if kw is None:
        continue
    r = brand_case(BRANDS[0], months=12, horizon=30, **kw)
    L("   %-18s 净现值 %9.1f 万｜较基准 %+9.1f" % (lbl, r["npv"], r["npv"]-b30["npv"]))

json.dump(dict(base=BASE, nonroom_split=SPLIT, brands=RESA, closure=CL, own=own,
               base_case=dict(npv=base["npv"], irr=base["irr"]),
               paths=[(l, dict(npv=brand_case(BRANDS[0], months=12, horizon=30)["npv"])) for l, _ in []]),
          open(os.path.join(T, "v51.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
L("DONE")
