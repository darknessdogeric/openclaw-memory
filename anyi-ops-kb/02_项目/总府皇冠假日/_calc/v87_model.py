# -*- coding: utf-8 -*-
"""v87：唯一权威模型（单一数据源 v87.json）
   —— 合并 v50/v52/v70 三版差异，固定为唯一版本
   ① 停业损失口径分离：段一A 刚性现金支出（计入资金需求）／段一B 营业收入归零（仅入现金流）
   ② 收入四板块（客房/餐饮/会议/其他），非房占比按同档次酒店收入结构基准
   ③ 造价三分口径：机电设备（全楼）/ 客房改造（单间）/ 公区改造（单平）
   ④ 房量由品牌客房面积要求反推（OTA 实测优先），移卫耦合折损 8%
   ⑤ 自有品牌路径同口径单列
   输出 v87.json：brands / own / paths / closure / base / tiers"""
import os, json, importlib.util
T = r"D:\B166ER-openclaw\workspace\.tmp"
D = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc"
OUT = open(os.path.join(T, "v87.log"), "w", encoding="utf-8")
def L(*a):
    OUT.write(" ".join(str(z) for z in a) + "\n"); OUT.flush()
spec = importlib.util.spec_from_file_location("v10", os.path.join(D, "v10_econ.py"))
V10 = importlib.util.module_from_spec(spec); spec.loader.exec_module(V10)
RES = {x["key"]: x for x in json.load(open(os.path.join(T, "v9.json"), encoding="utf-8"))}
SE = json.load(open(os.path.join(D, "seasonal_24m.json"), encoding="utf-8"))
MM = SE["months"]

GUEST_NET = 10192.0; SELLABLE = 402; FIXED_MONTHLY = 284.0
MOVE_WC = 0.08; VERTICAL = 860.0
ROOM_KEEP = RES["S1"]["room_total"] / RES["S1"]["n_rooms"]     # 14.70 万/间
PUB_KEEP = RES["S1"]["pub_total"]                              # 3,554.7 万
MEP = RES["S1"]["mep"]                                        # 11,060 万
OTHER_KEEP = RES["S1"]["fitout"] - RES["S1"]["room_total"] - RES["S1"]["pub_total"]  # 788.3 万
REDO_PUB = RES["S3"]["pub_total"] / PUB_KEEP

TIERS = {
 "上高端全服务": dict(room_share=0.60, gop=0.300, occ=0.70, fee=(6.0,10.5), band=(20,30),
                     note="行业基准：客房约 50%—60%、餐饮会议约 25%—35%"),
 "规模化奢华": dict(room_share=0.55, gop=0.360, occ=0.72, fee=(7.0,11.5), band=(28.8,57.6),
                   note="行业基准，高端全服务典型结构"),
 "高端奢华": dict(room_share=0.52, gop=0.380, occ=0.74, fee=(7.5,11.0), band=(36,50),
                 note="高星奢华非房占比高于上高端"),
 "超奢华": dict(room_share=0.50, gop=0.410, occ=0.75, fee=(6.5,14.0), band=(43,72),
               note="顶奢非房占比最高"),
}
# 关键：OTA 实测面积（2026-10/11 复核）优先，未开业者按同档次样本推定并标注
BRANDS = [
 ("B01","皇冠假日（现状续约）","上高端全服务",25.35,None,None,"现状套内 25.35 ㎡，续约不增面积","在营 402 间","存量续约，无品牌变动","—"),
 ("B02","洲至奢选 Vignette","高端奢华",45.0,900,1500,"OTA 实测：标准房 45 ㎡／尊贵房 52 ㎡／行政层 54—58 ㎡／套房 106 ㎡；挂牌约 $127 起（约 900 元）","棕榈泉 335 间在营","同集团可换牌，无第三方障碍","洲际体系内换牌，无第三方谈判障碍"),
 ("B03","康莱德 Conrad","规模化奢华",46.0,None,None,"OTA 实测：康莱德北京基础房 46 ㎡／套房 94—106 ㎡","未在蓉开业","空位","全球 51 家、中国 15 家，成都在谈未见落地"),
 ("B04","费尔蒙 Fairmont","规模化奢华",45.0,900,2200,"OTA 实测：与洲至奢选为同一物业（棕榈泉），标准房 45 ㎡／尊贵房 52 ㎡","棕榈泉已转洲至奢选","已被占（物业已转牌）","唯一原费尔蒙物业已转洲至奢选棕榈泉"),
 ("B05","Sofitel 索菲特","高端奢华",40.0,None,None,"按同档次成都样本 40 ㎡ 推定（成都未见开业）","未在蓉开业（太和非核心）","空位","雅高系，核心商圈尚无"),
 ("B06","瑞吉 St. Regis","规模化奢华",65.0,1291,1393,"OTA 实测：豪华客房 65 ㎡、¥1,291—1,393、在营 282 间","在营 282 间（太升南路）","已被占","太升南路在营 282 间"),
 ("B07","尼依格罗 Niccolo","规模化奢华",50.0,1180,1400,"OTA 实测：基础房 50 ㎡、¥1,180—1,400、IFS 在营 230 间","IFS 在营 230 间","已被占","IFS 3 号楼在营 230 间"),
 ("B08","柏悦 Park Hyatt","规模化奢华",45.0,None,None,"按同档次样本 45 ㎡ 推定（成都未见开业）","未在蓉开业","空位","凯悦系，中国 3+ 家"),
 ("B09","丽晶 Regent","高端奢华",60.0,None,None,"公开表述为顶配大客房，按 60 ㎡ 推定（2029Q3 开业）","顺江路 180 间、224.45 米塔楼","已被占（10km 外）","2026-07-15 签约顺江路 D10 望江"),
 ("B10","六善 Six Senses","高端奢华",50.0,None,None,"按同档次样本 50 ㎡ 推定（成都未见开业）","未在蓉开业","空位","IHG 奢华板块"),
 ("B11","文华东方 MO","高端奢华",55.0,None,None,"文华东方 267 间／489 米塔楼，按 55 ㎡ 推定（2028 开业）","中海 489 米、267 间","已被占（天府新区）","2022-10-20 签约中海 489 米塔楼"),
 ("B12","LXR 希尔顿超奢","超奢华",60.0,None,None,"超奢档按 60 ㎡ 推定（成都未落地）","总府路 28 号 2023-03 单方官宣、3 年无落地","重大空位（待核）","中国仅西安官宣 1 家"),
]
ADR_DEFAULT = {"上高端全服务": 880.0, "规模化奢华": 1400.0, "高端奢华": 1750.0, "超奢华": 2400.0}

def fit_rooms(area_th):
    if area_th <= 25.35 + 0.01: return SELLABLE, False
    return int(GUEST_NET // (area_th * (1 + MOVE_WC))), True

def build(b, months_full=12, horizon=30, phased=True, brand_share=0.0, subsidy=0.0, own=False):
    key, name, tier, area_th, p_lo, p_hi, area_src, rooms_exist, vacancy, basis = b
    T = TIERS[tier]
    n, reduced = fit_rooms(area_th)
    pk_ratio = T["band"][0] / 25.0 * 1.28
    room_cost = ROOM_KEEP * (1 + (pk_ratio - 1) * 0.62) * (n / SELLABLE) ** 0.35
    pub_cost = PUB_KEEP * (1 + (pk_ratio - 1) * 0.55)
    mep = MEP + (VERTICAL if reduced else 0.0)
    other = OTHER_KEEP * (n / SELLABLE) ** 0.35
    if own:
        room_cost *= 0.92; pub_cost *= 0.95
    fitout = room_cost * n + pub_cost + other
    capex = mep + fitout
    if brand_share: capex *= (1 - brand_share)
    capex -= subsidy
    if p_lo is not None:
        adr = (p_lo + p_hi) / 2; price_src = "OTA 实测"
    else:
        adr = ADR_DEFAULT[tier]; price_src = "同档次样本推定"
    occ = T["occ"]
    room_rev = n * 365 * occ * adr / 1e4
    total = room_rev / T["room_share"]
    nr = 1 - T["room_share"]
    seg = dict(room=room_rev, total=total, fnb=total*nr*0.58, banq=total*nr*0.30, misc=total*nr*0.12)
    gop_r = T["gop"]
    fee_lo = 0.0 if own else T["fee"][0]
    brand_base = total * fee_lo / 100.0
    mkt = total * 0.025; loy = total * 0.020
    ffe = total * (0.040 if T["band"][0] >= 36 else 0.020)
    inc_rate = 0.10 if T["band"][0] >= 36 else 0.06
    gop = total * gop_r
    br_m = brand_base * 0.35 / 12.0
    mcf = []
    if phased:
        for tt in range(1, horizon*12+1):
            if tt <= months_full:
                cash = -FIXED_MONTHLY - br_m
            elif tt <= months_full + 12:
                since = tt - months_full
                share = min(1.0, 0.35 + 0.05*since)
                r = total/12.0*share; g = r*gop_r; rr = r/total
                cash = (g - brand_base*rr - mkt*rr - loy*rr - ffe*rr - g*inc_rate) - FIXED_MONTHLY*(1-share)
            else:
                since = tt - months_full - 12
                r = (total/12.0)*min(1.0, 0.70+0.03*since); g = r*gop_r; rr = r/total
                cash = (g - brand_base*rr - mkt*rr - loy*rr - ffe*rr - g*inc_rate)
            if tt <= 24: cash -= capex/24.0
            mcf.append(cash)
    else:
        for tt in range(1, horizon*12+1):
            r = 0.0
            if tt > months_full:
                since = tt - months_full
                r = (total/12.0)*min(1.0, 0.62+0.038*since)
            g = r*gop_r; rr = r/total if total else 0
            cash = (g - brand_base*rr - mkt*rr - loy*rr - ffe*rr - g*inc_rate)
            if tt <= months_full: cash -= FIXED_MONTHLY + br_m
            half = max(1, months_full//2)
            if 1 <= tt <= half: cash -= capex*0.6/half
            elif half < tt <= months_full: cash -= capex*0.4/max(1, months_full-half)
            if tt > months_full:
                since = tt - months_full
                if since < 12: cash -= total*0.085/12.0
                elif since < 24: cash -= total*0.030/12.0
                if since < 6: cash -= total*0.012/6.0
            mcf.append(cash)
    acf = [round(sum(mcf[y*12:(y+1)*12]), 1) for y in range(horizon)]
    def pv(cf, r=0.08): return round(sum(c/(1+r)**i for i, c in enumerate(cf)), 1)
    inc_cf = [acf[i] - (-1924.0) for i in range(horizon)]
    return dict(key=key, name=name, tier=tier, tier_cn=tier, band=TIERS[tier]["band"],
                n=n, reduced=reduced, area_th=area_th, area_src=area_src,
                rooms_exist=rooms_exist, vacancy=vacancy, basis=basis,
                adr=adr, price_src=price_src, occ=occ, room_share=TIERS[tier]["room_share"],
                gop_rate=gop_r, fee=(0.0 if own else TIERS[tier]["fee"][0]),
                room_cost_total=room_cost*n, room_cost_per_key=room_cost, pub_cost=pub_cost,
                pub_per_sqm=pub_cost/31412.82, mep=mep, other=other, fitout=fitout, capex=capex,
                per_key_total=capex/n, seg=seg, total_rev=total,
                npv=pv(acf), irr=V10.irr(acf), pb=V10.payback(acf),
                npv20=pv(acf[:20]), irr20=V10.irr(acf[:20]), pb20=V10.payback(acf[:20]),
                inc_npv=round(pv(inc_cf), 1), irr_inc=V10.irr(inc_cf), pb_inc=V10.payback(inc_cf),
                acf=acf)

# ── 改造前基线 ──
ADR0 = sum(x["adr"] for x in MM)/24; OCC0 = sum(x["occ"] for x in MM)/24
BASE = dict(rooms=SELLABLE, adr=ADR0, occ=OCC0,
            revpar=sum(x["trevpar"] for x in MM)/24,
            total_rev=sum(x["rev"] for x in MM)/1e4/2,
            room=sum(x["room"] for x in MM)/1e4/2, fnb=sum(x["fnb"] for x in MM)/1e4/2,
            banq=sum(x["banq"] for x in MM)/1e4/2, misc=sum(x["misc"] for x in MM)/1e4/2,
            gop=sum(x["gop"] for x in MM)/1e4/2,
            labor=sum(x["labor"] for x in MM)/1e4/2, energy=sum(x["energy"] for x in MM)/1e4/2,
            maint=sum(x["maint"] for x in MM)/1e4/2,
            base_npv=round((-1924.0)*sum(1/1.08**i for i in range(20)), 1))
BASE["gop_rate"] = BASE["gop"]/BASE["total_rev"]

# ── 停业口径 ──
def closure(months):
    co = 0.0; rl = 0.0
    for k in range(months):
        m = str((k % 12) + 1)
        co += FIXED_MONTHLY + 6.38
        rl += SE["season"][m]["rev"]/1e4
    return round(co,1), round(rl,1)
CL = {str(m): closure(m) for m in (4, 8, 12, 16, 20)}

RESA = []
for b in BRANDS:
    r = build(b); RESA.append(r)
    L("%-4s %-18s 面积%5.1f 房量%4d ADR%6.0f 营收%9.1f 投资%9.1f 净现值%+9.1f IRR%s"
      % (r["key"], r["name"][:16], r["area_th"], r["n"], r["adr"], r["total_rev"], r["capex"], r["npv"],
         ("%.2f%%" % (r["irr"]*100)) if r["irr"] is not None else "无"))
ORDER = [r["key"] for r in sorted(RESA, key=lambda x: -x["npv"])]
L("排序: " + " > ".join(ORDER))

own = build(BRANDS[0], own=True)
L("自有品牌: 净现值 %+.1f 万｜IRR %s｜单房 %.2f 万" % (own["npv"], ("%.2f%%" % (own["irr"]*100)) if own["irr"] else "无", own["per_key_total"]))

# ── 净现值转正路径（皇冠基准）──
b20 = build(BRANDS[0], horizon=20)
b30 = build(BRANDS[0], horizon=30)
PATHS = [("基准", "12 月全停 ＋ 分区滚动 ＋ 20 年", b20["npv"], b20["irr"], "—"),
         ("P1", "经营期 20→30 年", b30["npv"], b30["irr"], "项目客观属性（20-30 年长周期资产）"),
         ("P2", "品牌方承担 30% 改造投入", build(BRANDS[0], brand_share=0.30)["npv"],
          build(BRANDS[0], brand_share=0.30)["irr"], "谈判条件，权重最大"),
         ("P3", "锦江区补贴 50 万元", build(BRANDS[0], subsidy=50.0)["npv"],
          build(BRANDS[0], subsidy=50.0)["irr"], "政策窗口（有效期至 2026-12-31，须开工前入库）"),
         ("P4", "P1＋P2", build(BRANDS[0], horizon=30, brand_share=0.30)["npv"],
          build(BRANDS[0], horizon=30, brand_share=0.30)["irr"], "—"),
         ("P5", "P1＋P2＋P3", build(BRANDS[0], horizon=30, brand_share=0.30, subsidy=50.0)["npv"],
          build(BRANDS[0], horizon=30, brand_share=0.30, subsidy=50.0)["irr"], "—")]
for a, b, c, d, e in PATHS:
    L("%-4s %-30s 净现值%+9.1f｜IRR %s｜%s" % (a, b, c, ("%.2f%%" % (d*100)) if d is not None else "无", e))

CLOSE_CASES = []
for _mo, _ph, _lb in [(4, False, "全停业 4 月（原设想，不可行）"), (12, False, "全停业 12 月 ＋ 一次复业"),
                      (12, True, "全停业 12 月 ＋ 分区滚动开业"), (16, True, "全停业 16 月 ＋ 分区滚动开业"),
                      (20, True, "全停业 20 月 ＋ 分区滚动开业")]:
    _r = build(BRANDS[0], months_full=_mo, phased=_ph, horizon=30)
    CLOSE_CASES.append(dict(label=_lb, months=_mo, phased=_ph, npv=round(_r["npv"], 1),
                            irr=_r["irr"], A=CL[str(_mo)][0], B=CL[str(_mo)][1]))
json.dump(dict(base=BASE, brands=RESA, order=ORDER, own=own, closure=CL, paths=PATHS, close_cases=CLOSE_CASES,
               tiers=TIERS, brands_meta=[list(b) for b in BRANDS],
               constants=dict(guarst_net=GUEST_NET, sellable=SELLABLE, move_wc=MOVE_WC,
                              vertical=VERTICAL, mep=MEP, room_keep=ROOM_KEEP, pub_keep=PUB_KEEP,
                              other_keep=OTHER_KEEP, redo_pub=REDO_PUB, fixed_monthly=FIXED_MONTHLY,
                              pub_area=31412.82, adr_default=ADR_DEFAULT)),
          open(os.path.join(T, "v87.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
L("DONE")
