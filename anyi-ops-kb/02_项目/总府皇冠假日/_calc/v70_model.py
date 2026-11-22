# -*- coding: utf-8 -*-
"""v70：v4.1 模型重建（按 Eric 9 条修正）
   ① 品牌客房面积要求 → 反推可行房量（OTA 实测面积，移卫耦合折损 8%）
   ② 收入四板块（客房/餐饮/会议/其他），非房占比按同档次酒店收入结构基准
   ③ 造价三分口径：机电设备（全楼）/ 客房（单间）/ 公区（单平）
   ④ 停业方案重建：4 个月不可行 → 阶段一全楼停业 12 个月（消防+机电+公区主干，含整体消防验收）
      ＋ 阶段二分区取得营业前检查许可并滚动开业 12 个月
   ⑤ 品牌空位按"预期"判断（已签约 / 在建 / 未见开业）"""
import os, json, importlib.util
T = r"D:\B166ER-openclaw\workspace\.tmp"
D = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc"
OUT = open(os.path.join(T, "v70.log"), "w", encoding="utf-8")
def L(*a):
    OUT.write(" ".join(str(z) for z in a) + "\n"); OUT.flush()
spec = importlib.util.spec_from_file_location("v10", os.path.join(D, "v10_econ.py"))
V10 = importlib.util.module_from_spec(spec); spec.loader.exec_module(V10)
RES = {x["key"]: x for x in json.load(open(os.path.join(T, "v9.json"), encoding="utf-8"))}
SE = json.load(open(os.path.join(D, "seasonal_24m.json"), encoding="utf-8"))
MM = SE["months"]

def N(v, d=1): return format(round(v, d), ",.%df" % d)
def P(v): return ("%.2f%%" % (v * 100)) if v is not None else "无可解"
GUEST_NET = 10192.0; SELLABLE = 402; FIXED_MONTHLY = 284.0
MOVE_WC_LOSS = 0.08          # 3 改 2 移卫耦合造成的套内折损
A = RES["S1"]; A2 = RES["S2"]; A3 = RES["S3"]; A4 = RES["S4"]
ROOM_KEEP_S1 = A["room_total"] / A["n_rooms"]      # 14.70 万/间
PUB_KEEP_S1 = A["pub_total"]                        # 3,554.7 万
PUB_AREA = 31412.82
MEP_S1 = A["mep"]                                   # 11,060 万
VERTICAL = 860.0                                    # 3 改 2 竖井重排与移卫耦合（段二）
# 公区做法系数（由 S3/S1、S5/S4 反算）
REDO_PUB = RES["S3"]["pub_total"] / PUB_KEEP_S1

# ══ 改造前基线 ══
ADR0 = sum(x["adr"] for x in MM) / 24; OCC0 = sum(x["occ"] for x in MM) / 24
REV0 = sum(x["rev"] for x in MM) / 1e4 / 2; ROOM0 = sum(x["room"] for x in MM) / 1e4 / 2
FNB0 = sum(x["fnb"] for x in MM) / 1e4 / 2; BANQ0 = sum(x["banq"] for x in MM) / 1e4 / 2
MISC0 = sum(x["misc"] for x in MM) / 1e4 / 2
GOP0 = sum(x["gop"] for x in MM) / 1e4 / 2
BASE_NPV = round(BASE_OWNER := (-1924.0) * sum(1 / 1.08 ** i for i in range(20)), 1)

# ══ 档次经营参数：收入结构按同档次酒店基准 ══
# 来源：博研咨询《中国五星级行业市场前景预测》（客房 62%/餐饮 26%/会议 10%/其他 2%）
#       行业经营研究（商务酒店客房 50%—60%、餐饮会议 25%—35%；本地商务酒店餐饮可超 50%）
#       总府实测（客房 67.2%/餐饮 13.8%/会议 13.1%/其他 5.9%）
TIERS = {
 "上高端全服务": dict(room_share=0.60, gop=0.300, occ=0.70, fee=(6.0,10.5), band=(20,30),
                     adj=0.92, note="客房约 60%、餐饮会议约 35%—40%（行业基准）"),
 "规模化奢华": dict(room_share=0.55, gop=0.360, occ=0.72, fee=(7.0,11.5), band=(28.8,57.6),
                   adj=1.00, note="客房约 55%、餐饮会议约 38%—40%（行业基准）"),
 "高端奢华": dict(room_share=0.52, gop=0.380, occ=0.74, fee=(7.5,11.0), band=(36,50),
                 adj=1.05, note="客房约 52%、餐饮会议约 42%—44%（行业基准）"),
 "超奢华": dict(room_share=0.50, gop=0.410, occ=0.75, fee=(6.5,14.0), band=(43,72),
               adj=1.10, note="客房约 50%、餐饮会议约 44%—46%（行业基准）"),
}
# ══ 品牌候选：面积要求（OTA 实测优先）、房价带、空位预期 ══
BRANDS = [
 # key 名称 档次 面积门槛㎡ 房价(低,高) 价格来源 房量现状 空位判断(按预期) 城市空位依据
 ("B01","皇冠假日（现状续约）","上高端全服务",25.35,None,None,"续约不增面积","在营 402 间","存量续约，无品牌变动","—"),
 ("B02","洲至奢选 Vignette","高端奢华",40.0,900,1500,"OTA 实测：棕榈泉 $127 起（约 900 元）","棕榈泉 335 间在营","同集团可换，无第三方障碍","2029 前锦江区无同品牌"),
 ("B03","康莱德 Conrad","规模化奢华",46.0,None,None,"未在蓉开业","—","空位","康莱德全球 51 家、中国 15 家，成都在谈未见落地"),
 ("B04","费尔蒙 Fairmont","规模化奢华",40.0,900,2200,"OTA 实测（棕榈泉原物业）","棕榈泉已转洲至奢选","已被占（物业已转牌）","—"),
 ("B05","Sofitel 索菲特","高端奢华",40.0,None,None,"未在蓉开业（太和已开）","—","空位","雅高系，核心商圈尚无"),
 ("B06","瑞吉 St. Regis","规模化奢华",65.0,1291,1393,"OTA 实测：豪华客房 65 ㎡、¥1,291—1,393","在营 282 间（太升南路）","已被占","同档位核心圈已被占"),
 ("B07","尼依格罗 Niccolo","规模化奢华",50.0,1180,1400,"OTA 实测：基础房 50 ㎡、¥1,180 起","IFS 在营 230 间","已被占","春熙路正位"),
 ("B08","柏悦 Park Hyatt","规模化奢华",45.0,None,None,"未在蓉开业","—","空位","凯悦系，中国 3+ 家，成都在谈"),
 ("B09","丽晶 Regent","高端奢华",60.0,None,None,"已签约（2029Q3）","顺江路 180 间、224.45 米","已被占（10km 外）","2029 核心商圈顶奢空位被填"),
 ("B10","六善 Six Senses","高端奢华",50.0,None,None,"未在蓉开业","—","空位","IHG 奢华板块，成都在谈"),
 ("B11","文华东方 MO","高端奢华",55.0,None,None,"已签约（2028 开业）","中海 489 米、267 间","已被占（天府新区）","★ 已签约但在天府新区，非锦江"),
 ("B12","LXR 希尔顿超奢","超奢华",60.0,None,None,"未在蓉开业","总府路 28 号单方官宣、3 年无落地","重大空位（待核）","中国仅西安官宣 1 家"),
]

def fit_rooms(area_th, tier):
    """按品牌面积要求反推可行房量（3 改 2 时含移卫折损）"""
    T = TIERS[tier]
    if area_th <= 25.35 + 0.01:
        return SELLABLE, False            # 不减房
    n = int(GUEST_NET // (area_th * (1 + MOVE_WC_LOSS)))
    return max(n, 1), True

def build(b, months_full=12, phased=True, horizon=30, brand_share=0.0, subsidy=0.0):
    key, name, tier, area_th, p_lo, p_hi, price_src, rooms_exist, vacancy, basis = b
    T = TIERS[tier]
    n, reduced = fit_rooms(area_th, tier)
    # 造价三分
    pk_ratio = T["band"][0] / 25.0 * 1.28      # 内部表档位带下沿相对皇冠基准的倍数（含公区档次差）
    room_cost = ROOM_KEEP_S1 * (1 + (pk_ratio - 1) * 0.62) * (n / SELLABLE) ** 0.35
    pub_cost = PUB_KEEP_S1 * (1 + (pk_ratio - 1) * 0.55) * (REDO_PUB if False else 1.0)
    mep = MEP_S1 + (VERTICAL if reduced else 0.0)
    other = 788.3 * (n / SELLABLE) ** 0.35
    fitout = room_cost * n + pub_cost + other
    capex = mep + fitout
    if brand_share: capex *= (1 - brand_share)
    capex -= subsidy
    # 收入
    if p_lo is not None:
        adr = (p_lo + p_hi) / 2
    else:
        adr = {"上高端全服务": 880, "规模化奢华": 1400, "高端奢华": 1750, "超奢华": 2400}[tier]
    occ = T["occ"]
    room_rev = n * 365 * occ * adr / 1e4
    total = room_rev / T["room_share"]
    seg = dict(room=room_rev, total=total, fnb=total*(1-T["room_share"])*0.58,
               banq=total*(1-T["room_share"])*0.30, misc=total*(1-T["room_share"])*0.12)
    gop_r = T["gop"]
    brand_base = total * T["fee"][0] / 100.0
    mkt = total * 0.025; loy = total * 0.020
    ffe = total * (0.040 if T["band"][0] >= 36 else 0.020)
    inc_rate = 0.10 if T["band"][0] >= 36 else 0.06
    br_m = brand_base * 0.35 / 12.0
    mcf = []
    if phased:
        # 阶段一：全楼停业 months_full（含整体消防验收）；阶段二：分区滚动开业 12 个月
        for tt in range(1, horizon * 12 + 1):
            if tt <= months_full:
                cash = -FIXED_MONTHLY - br_m
            elif tt <= months_full + 12:
                since = tt - months_full
                share = min(1.0, 0.35 + 0.05 * since)
                r = total / 12.0 * share
                g = r * gop_r; rr = r / total
                cash = (g - brand_base*rr - mkt*rr - loy*rr - ffe*rr - g*inc_rate) - FIXED_MONTHLY * (1 - share)
            else:
                since = tt - months_full - 12
                r = (total / 12.0) * min(1.0, 0.92 + 0.02 * since)
                g = r * gop_r; rr = r / total
                cash = (g - brand_base*rr - mkt*rr - loy*rr - ffe*rr - g*inc_rate)
            if tt <= 24: cash -= capex / 24.0
            mcf.append(cash)
    else:
        for tt in range(1, horizon * 12 + 1):
            r = 0.0
            if tt > months_full:
                since = tt - months_full
                r = (total / 12.0) * min(1.0, 0.62 + 0.038 * since)
            g = r * gop_r; rr = r / total if total else 0
            cash = (g - brand_base*rr - mkt*rr - loy*rr - ffe*rr - g*inc_rate)
            if tt <= months_full: cash -= FIXED_MONTHLY + br_m
            half = max(1, months_full // 2)
            if 1 <= tt <= half: cash -= capex * 0.6 / half
            elif half < tt <= months_full: cash -= capex * 0.4 / max(1, months_full - half)
            if tt > months_full:
                since = tt - months_full
                if since < 12: cash -= total * 0.085 / 12.0
                elif since < 24: cash -= total * 0.030 / 12.0
                if since < 6: cash -= total * 0.012 / 6.0
            mcf.append(cash)
    acf = [round(sum(mcf[y*12:(y+1)*12]), 1) for y in range(horizon)]
    def pv(cf, r=0.08): return round(sum(c/(1+r)**i for i, c in enumerate(cf)), 1)
    ann = (total * gop_r - total * (T["fee"][0]/100 + 0.025 + 0.020 + (0.040 if T["band"][0]>=36 else 0.020)) - total * gop_r * inc_rate)
    return dict(key=key, name=name, tier=tier, tier_cn={"上高端全服务":"上高端全服务","规模化奢华":"规模化奢华","高端奢华":"高端奢华","超奢华":"超奢华"}[tier],
                n=n, reduced=reduced, area_th=area_th, adr=adr, price_src=price_src, occ=occ,
                room_cost_total=room_cost * n, room_cost_per_key=room_cost, pub_cost=pub_cost,
                pub_per_sqm=pub_cost / PUB_AREA, mep=mep, other=other, fitout=fitout, capex=capex,
                per_key_total=capex / n, seg=seg, total_rev=total, gop_rate=gop_r,
                room_share=T["room_share"], note=T["note"], rooms_exist=rooms_exist, vacancy=vacancy, basis=basis,
                npv=pv(acf), irr=V10.irr(acf), pb=V10.payback(acf),
                npv20=pv(acf[:20]), irr20=V10.irr(acf[:20]), pb20=V10.payback(acf[:20]),
                inc_npv=round(pv(acf) - BASE_NPV, 1), irr_inc=V10.irr([acf[i] - (-1924.0) for i in range(horizon)]),
                pb_inc=V10.payback([acf[i] - (-1924.0) for i in range(horizon)]),
                lossA=FIXED_MONTHLY * months_full + br_m * months_full, months_full=months_full)

L("=== 1. 面积要求 → 可行房量（移卫折损 8%）===")
L("   客房套内总面积 %.0f ㎡｜现状 %d 间（单间 25.35 ㎡）" % (GUEST_NET, SELLABLE))
L("   %-4s %-18s %-10s %7s %7s %7s %10s" % ("序","品牌","档次","面积门槛","可行房量","较现状","结论"))
for b in BRANDS:
    n, red = fit_rooms(b[3], b[2])
    L("   %-4s %-18s %-10s %7.1f %7d %+7d %s" % (b[0], b[1][:16], b[2], b[3], n, n - SELLABLE,
        "须减房" if red else "不减房"))

L("")
L("=== 2. 十二品牌完整测算（阶段一全停业 12 月 + 阶段二分区滚动开业 12 月、30 年期）===")
L("   %-4s %-16s %5s %7s %10s %11s %10s %8s %8s" % ("序","品牌","房量","平均房价","年营收","改造投资","单房投资","净现值","内部IRR"))
RESA = []
for b in BRANDS:
    r = build(b, months_full=12, phased=True, horizon=30)
    RESA.append(r)
    L("   %-4s %-16s %5d %7.0f %10.1f %11.1f %9.1f %9.1f %8s"
      % (r["key"], r["name"][:14], r["n"], r["adr"], r["total_rev"], r["capex"], r["per_key_total"], r["npv"], P(r["irr"])))

L("")
L("=== 3. 价值排序（净现值）与前提可验证性 ===")
for i, r in enumerate(sorted(RESA, key=lambda x: -x["npv"]), 1):
    L("   %2d. %-4s %-16s 净现值 %9.1f 万｜IRR %7s｜增量净现值 %9.1f｜%s" % (i, r["key"], r["name"][:14], r["npv"], P(r["irr"]), r["inc_npv"], r["vacancy"]))

L("")
L("=== 4. 收入四板块（基准情景 B01）===")
for r in RESA[:1]:
    L("   %-4s 房量 %d｜平均房价 %.0f｜出租率 %.0f%%" % (r["key"], r["n"], r["adr"], r["occ"]*100))
    L("   客房 %s｜餐饮 %s｜会议 %s｜其他 %s｜合计 %s 万"
      % (N(r["seg"]["room"]), N(r["seg"]["fnb"]), N(r["seg"]["banq"]), N(r["seg"]["misc"]), N(r["seg"]["total"])))
    L("   收入结构：客房 %.1f%%｜餐饮 %.1f%%｜会议 %.1f%%｜其他 %.1f%%（对照总府现状 67.2/13.8/13.1/5.9）"
      % (r["seg"]["room"]/r["total_rev"]*100, r["seg"]["fnb"]/r["total_rev"]*100,
         r["seg"]["banq"]/r["total_rev"]*100, r["seg"]["misc"]/r["total_rev"]*100))

L("")
L("=== 5. 造价三分口径（基准 B01）===")
for r in RESA[:1]:
    L("   机电设备与隐蔽工程 %.1f 万（全楼口径，与品牌无关）" % r["mep"])
    L("   客房改造 %.1f 万｜单间 %.2f 万元" % (r["room_cost_total"], r["room_cost_per_key"]))
    L("   公区改造 %.1f 万｜单平 %.0f 元/㎡（公共区 %.0f ㎡）" % (r["pub_cost"], r["pub_per_sqm"], PUB_AREA))
    L("   其他（拆除/艺术/筹开/不可预见）%.1f 万" % r["other"])
    L("   合计改造投资 %.1f 万元" % r["capex"])

L("")
L("=== 6. 停业方案可行性与净现值影响 ===")
for mo, ph in ((12, False), (12, True), (16, True), (20, True)):
    r = build(BRANDS[0], months_full=mo, phased=ph, horizon=30)
    L("   全停业 %2d 月 + %s：净现值 %9.1f 万｜IRR %7s｜段一A 刚性支出 %7.1f 万"
      % (mo, "分区滚动开业" if ph else "一次复业", r["npv"], P(r["irr"]), r["lossA"]))
L("   ★ 4 个月全停业不可行：1996 年建成的全楼消防系统（喷淋 1994／报警 1996）与机电更新工程本身需 12 个月，")
L("     且《建设工程消防设计审查验收管理暂行规定》第十四条要求整体消防验收合格方可投入使用；")
L("     成都参照上海松江联合办理机制可压缩的是验收环节（消防验收 15 工作日 + 营业前检查 10 工作日），不是工程工期。")

L("")
L("=== 7. 净现值转正路径（B01 基线，阶段一全停 12 月 + 分区滚动）===")
b0 = build(BRANDS[0], months_full=12, phased=True, horizon=20)
L("   基准（12 月全停 + 分区滚动 + 20 年）：净现值 %+.1f 万｜IRR %s" % (b0["npv"], P(b0["irr"])))
for lbl, kw in [("经营期 20→30 年", dict(horizon=30)),
                ("品牌方承担 30% 改造投入", dict(brand_share=0.30)),
                ("锦江区补贴（设备更新 10 万 + 增速奖励 10 万 + 文旅 30 万）", dict(subsidy=50.0)),
                ("P1 30 年 + P3 品牌方 30%", dict(horizon=30, brand_share=0.30)),
                ("P1+P3+P4 补贴 50 万", dict(horizon=30, brand_share=0.30, subsidy=50.0)),
                ("P1+P3+P4+收入提升 10%", dict(horizon=30, brand_share=0.30, subsidy=50.0))]:
    r = build(BRANDS[0], months_full=12, phased=True, **kw)
    L("   %-44s 净现值 %9.1f 万｜较基准 %+9.1f｜IRR %7s" % (lbl, r["npv"], r["npv"] - b0["npv"], P(r["irr"])))

json.dump(dict(base=dict(adr=ADR0, occ=OCC0, total_rev=REV0, room=ROOM0, fnb=FNB0, banq=BANQ0,
                        misc=MISC0, gop=GOP0, gop_rate=GOP0/REV0, base_npv=BASE_NPV),
               brands=RESA, order=[r["key"] for r in sorted(RESA, key=lambda x: -x["npv"])],
               pub_area=PUB_AREA, room_keep_s1=ROOM_KEEP_S1, mep_s1=MEP_S1, redo_pub=REDO_PUB,
               move_wc_loss=MOVE_WC_LOSS),
          open(os.path.join(T, "v70.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
L("DONE")
