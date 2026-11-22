# -*- coding: utf-8 -*-
"""v52：v4.0 最终模型
   造价模型锚定 v9 实配两个基准（皇冠保留 / 洲至奢选保留），拆为「客房 + 公区 + 其他」三段
   产出 v52.json：12 品牌分级分类造价与价值排序、停业口径、收入板块、NPV 转正路径、人防三方案"""
import os, json, importlib.util
T = r"D:\B166ER-openclaw\workspace\.tmp"
D = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc"
OUT = open(os.path.join(T, "v52.log"), "w", encoding="utf-8")
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

# ══ 造价锚点（v9 实配反算：客房 / 公区 / 其他）═══════════════════════
def split_of(k):
    x = RES[k]
    room = x["room_total"]; pub = x["pub_total"]
    other = x["fitout"] - room - pub
    return dict(room=room, pub=pub, other=other, fit=x["fitout"], mep=x["mep"],
                per_key_room=room / x["n_rooms"], months=x["months"], n=x["n_rooms"])
ANCH = {k: split_of(k) for k in ("S1","S2","S3","S4","S5","S7","S8")}
L("=== 0. v9 实配拆分（造价模型的两个校准基准）===")
for k, a in ANCH.items():
    L("  %-4s 房量%3d 客房%8.1f(单间%6.2f万) 公区%8.1f 其他%7.1f 装修合计%9.1f 机电%8.1f 停业%2d月"
      % (k, a["n"], a["room"], a["per_key_room"], a["pub"], a["other"], a["fit"], a["mep"], a["months"]))
BASE_KEEP = ANCH["S1"]; BASE_KEEP_V = ANCH["S4"]
L("  ★ 基准一 S1（皇冠·保留石材·不减房）：客房单间 %.2f 万｜公区 %.1f 万｜其他 %.1f 万" % (BASE_KEEP["per_key_room"], BASE_KEEP["pub"], BASE_KEEP["other"]))
L("  ★ 基准二 S4（洲至奢选·保留石材·不减房）：客房单间 %.2f 万｜公区 %.1f 万｜其他 %.1f 万" % (BASE_KEEP_V["per_key_room"], BASE_KEEP_V["pub"], BASE_KEEP_V["other"]))
REDO_RATIO_ROOM = ANCH["S3"]["per_key_room"] / BASE_KEEP["per_key_room"]
REDO_RATIO_PUB = ANCH["S3"]["pub"] / BASE_KEEP["pub"]
L("  ★ 公区重做系数：客房 %.3f｜公区 %.3f（由 S3/S1 反算）" % (REDO_RATIO_ROOM, REDO_RATIO_PUB))
L("  ★ 3 改 2 客房单间：皇冠 %.2f 万（移卫耦合）｜外部奢牌 %.2f 万" % (ANCH["S2"]["per_key_room"], ANCH["S7"]["per_key_room"]))
L("  ★ 外部奢牌（S7）客房单间 %.2f 万 —— 超内部表超奢华带上限 72 万/间，决策性对照。" % ANCH["S7"]["per_key_room"])

# ══ 档次参数：内部表 §8 单房改造带 + 本项目校准后的客房/公区单价 ══
TIERS = {
 "上高端全服务": dict(band=(20,30), room_keep=14.70, room_redo=24.34, pub_keep=3554.7, pub_redo=6783.1,
                      other=788.3, gop=0.300, occ=0.70, fee=(6.0,10.5), tier_cn="上高端全服务"),
 "规模化奢华": dict(band=(28.8,57.6), room_keep=19.00, room_redo=31.00, pub_keep=4500.0, pub_redo=8400.0,
                  other=1200.0, gop=0.360, occ=0.72, fee=(7.0,11.5), tier_cn="规模化奢华"),
 "高端奢华": dict(band=(36,50), room_keep=23.83, room_redo=38.03, pub_keep=5585.9, pub_redo=10200.7,
                  other=1965.5, gop=0.380, occ=0.74, fee=(7.5,11.0), tier_cn="高端奢华"),
 "超奢华": dict(band=(43,72), room_keep=30.00, room_redo=52.98, pub_keep=7000.0, pub_redo=12923.2,
                other=2900.0, gop=0.410, occ=0.75, fee=(6.5,14.0), tier_cn="超奢华"),
}
# ══ 改造前基线（24 个月实测）═══════════════════════════════════════
ADR0 = sum(x["adr"] for x in MM) / 24; OCC0 = sum(x["occ"] for x in MM) / 24
REV0 = sum(x["rev"] for x in MM) / 1e4 / 2; ROOM0 = sum(x["room"] for x in MM) / 1e4 / 2
FNB0 = sum(x["fnb"] for x in MM) / 1e4 / 2; BANQ0 = sum(x["banq"] for x in MM) / 1e4 / 2
MISC0 = sum(x["misc"] for x in MM) / 1e4 / 2; GOP0 = sum(x["gop"] for x in MM) / 1e4 / 2
LAB0 = sum(x["labor"] for x in MM) / 1e4 / 2; ENG0 = sum(x["energy"] for x in MM) / 1e4 / 2
MNT0 = sum(x["maint"] for x in MM) / 1e4 / 2
BASE = dict(rooms=SELLABLE, adr=ADR0, occ=OCC0, room_rev=ROOM0, fnb=FNB0, banq=BANQ0, misc=MISC0,
            total_rev=REV0, gop=GOP0, gop_rate=GOP0/REV0, labor=LAB0, energy=ENG0, maint=MNT0,
            revpar=sum(x["trevpar"] for x in MM)/24)
SPLIT = dict(fnb=FNB0/(FNB0+BANQ0+MISC0), banq=BANQ0/(FNB0+BANQ0+MISC0), misc=MISC0/(FNB0+BANQ0+MISC0))
NONROOM_SHARE = (FNB0+BANQ0+MISC0)/REV0
L("")
L("=== 1. 改造前基线（24 个月实测，USALI 利润表交叉验证）===")
L("   ADR %.1f 元｜OCC %.2f%%｜每间可售房收入 %.1f 元｜营业收入 %s 万" % (ADR0, OCC0*100, BASE["revpar"], N(REV0)))
L("   客房 %s（%.1f%%）｜餐饮 %s（%.1f%%）｜会议 %s（%.1f%%）｜其他 %s（%.1f%%）"
  % (N(ROOM0), ROOM0/REV0*100, N(FNB0), FNB0/REV0*100, N(BANQ0), BANQ0/REV0*100, N(MISC0), MISC0/REV0*100))
L("   部门营业利润 %s 万（%.1f%%）｜人工 %s 万｜能耗 %s 万｜维修 %s 万"
  % (N(GOP0), GOP0/REV0*100, N(LAB0), N(ENG0), N(MNT0)))
L("   ★ 旧稿用 2026-09 单月低点 ADR 363.99 元，客房收入低估 %.1f 万元（%.1f%%）；本版已按 24 个月均值重建。"
  % (ROOM0-3780.2, (ROOM0/3780.2-1)*100))

# ══ 停业口径 ════════════════════════════════════════════════════════
def closure(months, brand_ret_m=0.0):
    co = 0.0; rl = 0.0
    for k in range(months):
        m = str((k % 12) + 1)
        co += FIXED_MONTHLY + brand_ret_m
        rl += SE["season"][m]["rev"] / 1e4 / 2
    return co, rl
CL = {str(m): closure(m, 6.38) for m in (4, 8, 12, 16, 20)}
L("")
L("=== 2. 停业损失口径分离 ===")
for m, (a, b) in CL.items():
    L("   停业 %2s 月：段一A 刚性现金支出 %7.1f 万（计入资金需求）｜段一B 营业收入归零 %7.1f 万（仅入现金流）" % (m, a, b))

# ══ 品牌候选集 ══════════════════════════════════════════════════════
BRANDS = [
 ("B01","皇冠假日（现状续约）","上高端全服务",0,None,None,402,"在营 30 年｜IHG One Rewards（会员匹配评分 48，五强垫底）｜成都核心商圈唯一存续国际五星","存量续约"),
 ("B02","洲至奢选 Vignette","高端奢华",0,900,1500,335,"2026 年成都棕榈泉 335 间已开业｜同属 IHG 体系｜实测约 900 元起（$127）","同集团可换"),
 ("B03","康莱德 Conrad","上高端全服务",0,None,None,None,"希尔顿系｜设计驱动｜Hilton Honors 会员匹配 88 分（五强最高）｜成都未见开业","空位"),
 ("B04","费尔蒙 Fairmont","上高端全服务",0,900,2200,336,"Accor ALL 系｜地标建筑导向｜成都唯一原费尔蒙物业即现洲至奢选棕榈泉｜无独立在营物业","已被占"),
 ("B05","Sofitel 索菲特","高端奢华",0,None,None,None,"雅高系｜设计驱动｜成都未见开业（太和已开，非核心商圈）","空位"),
 ("B06","瑞吉 St. Regis","规模化奢华",40,1200,2000,312,"万豪系｜管家服务｜太升南路｜春熙路核心圈外围｜实测 1,200—2,000 元","已被占"),
 ("B07","尼依格罗 Niccolo","规模化奢华",40,1200,1800,238,"九龙仓｜IFS 3 号楼｜大慈寺景｜春熙路正位｜实测 1,200—1,800 元","已被占"),
 ("B08","柏悦 Park Hyatt","规模化奢华",0,None,None,None,"凯悦系｜Hyatt Dynasty｜成都未见开业","空位"),
 ("B09","丽晶 Regent","高端奢华",40,None,None,None,"IHG 顶奢｜锦江顺江路 2026-07-15 签约，2029Q3 开业｜距本项目约 10 公里","已被占"),
 ("B10","六善 Six Senses","高端奢华",45,None,None,None,"IHG 奢华板块｜养生导向｜成都未见开业","空位"),
 ("B11","文华东方 MO","高端奢华",45,None,None,None,"怡和系｜姿态高｜成都未见开业","空位"),
 ("B12","LXR 希尔顿超奢","超奢华",0,None,None,None,"希尔顿超奢｜中国仅西安官宣 1 家｜成都总府路 28 号 2023-03 单方官宣后 3 年无落地","重大空位"),
]
PRICE_ANCHOR = {"上高端全服务":(750.0,900.0),"规模化奢华":(1200.0,2000.0),
                "高端奢华":(1500.0,2200.0),"超奢华":(2000.0,3000.0)}
def rooms_by_area(th): return SELLABLE if not th else int(GUEST_NET // th)

def build(b, months=12, horizon=30, phased=False, brand_share=0.0, subsidy=0.0, boost=1.0,
          pub="保留", own=False, room_mode="不减房"):
    key, name, tier, area_th, p_lo, p_hi, rooms_exist, feat, loc = b
    T = TIERS[tier]; n = rooms_by_area(area_th)
    rp = T["room_keep"] if pub == "保留" else T["room_redo"]
    if room_mode == "3改2":
        rp = {"上高端全服务":20.04,"规模化奢华":26.00,"高端奢华":32.00,"超奢华":45.00}[tier]
    room = rp * n
    puba = T["pub_keep"] if pub == "保留" else T["pub_redo"]
    if room_mode == "3改2": puba = puba * 1.15     # 公区不随房量减少，结转至较少房量
    other = T["other"] * (n / SELLABLE if room_mode == "3改2" else 1.0)
    if own: room = room * 0.92; puba = puba * 0.95   # 自有品牌无需外方标准溢价
    fit = room + puba + other + (860.0 if room_mode == "3改2" else 0.0)
    capex = 11060.0 + fit
    if brand_share: capex *= (1 - brand_share)
    capex -= subsidy
    fee_lo, fee_hi = (0.0, 0.0) if own else T["fee"]
    if p_lo is not None:
        adr = (p_lo + p_hi) / 2; adr_src = "2026-10 成都实测房价带"
    else:
        lo, hi = PRICE_ANCHOR[tier]; adr = (lo + hi) / 2
        adr_src = "同档位成都实测带推定（成都未开业，推测值）"
    occ = T["occ"]; gop_r = T["gop"]
    room_rev = n * 365 * occ * adr / 1e4 * boost
    nr_share = NONROOM_SHARE if tier == "上高端全服务" else {"规模化奢华":0.35,"高端奢华":0.38,"超奢华":0.42}[tier]
    total = room_rev / (1 - nr_share)
    seg = dict(room=room_rev, total=total, fnb=total*nr_share*SPLIT["fnb"],
               banq=total*nr_share*SPLIT["banq"], misc=total*nr_share*SPLIT["misc"])
    brand_base = total * fee_lo / 100.0
    mkt = total * 0.025; loy = total * 0.020
    ffe = total * (0.040 if T["band"][0] >= 36 else 0.020)
    inc_rate = 0.10 if T["band"][0] >= 36 else 0.06
    br_m = brand_base * 0.35 / 12.0
    mcf = []
    if phased:
        full_m, phase_end = 4, 16
        for tt in range(1, horizon*12+1):
            if tt <= full_m: cash = -FIXED_MONTHLY - br_m
            elif tt <= phase_end:
                s = tt - full_m
                r = total/12.0*(0.40*min(1.0, 0.35+0.05*s)); g = r*gop_r; rr = r/total
                cash = (g-brand_base*rr-mkt*rr-loy*rr-ffe*rr-g*inc_rate) - FIXED_MONTHLY*0.35
            else:
                s = tt - phase_end
                r = (total/12.0)*min(1.0, 0.70+0.03*s); g = r*gop_r; rr = r/total
                cash = (g-brand_base*rr-mkt*rr-loy*rr-ffe*rr-g*inc_rate)
            if tt <= 18: cash -= capex/18.0
            mcf.append(cash)
    else:
        for tt in range(1, horizon*12+1):
            r = 0.0
            if tt > months:
                s = tt - months; r = (total/12.0)*min(1.0, 0.62+0.038*s)
            g = r*gop_r; rr = r/total if total else 0
            cash = (g-brand_base*rr-mkt*rr-loy*rr-ffe*rr-g*inc_rate)
            if tt <= months: cash -= FIXED_MONTHLY + br_m
            h = max(1, months//2)
            if 1 <= tt <= h: cash -= capex*0.6/h
            elif h < tt <= months: cash -= capex*0.4/max(1, months-h)
            if tt > months:
                s = tt - months
                if s < 12: cash -= total*0.085/12.0
                elif s < 24: cash -= total*0.030/12.0
                if s < 6: cash -= total*0.012/6.0
            mcf.append(cash)
    acf = [round(sum(mcf[y*12:(y+1)*12]),1) for y in range(horizon)]
    def pv(cf, r=0.08): return round(sum(c/(1+r)**i for i,c in enumerate(cf)),1)
    return dict(key=key, name=name, tier=tier, tier_cn=T["tier_cn"], band=T["band"], n=n, area_th=area_th,
                room_mode=room_mode, pub=pub, adr=adr, adr_src=adr_src, occ=occ, fee=(fee_lo+fee_hi)/2,
                room_cost=room, pub_cost=puba, other_cost=other, fit=fit, capex=capex, per_key=capex/n,
                seg=seg, gop_rate=gop_r, feat=feat, loc=loc,
                npv=pv(acf), irr=V10.irr(acf), pb=V10.payback(acf),
                npv20=pv(acf[:20]), irr20=V10.irr(acf[:20]), pb20=V10.payback(acf[:20]))

L("")
L("=== 3. 12 品牌分级分类造价与价值排序（保留石材、不减房、全停业 12 月、30 年期、8%）===")
L("   %-4s %-18s %-8s %4s %8s %9s %10s %9s %10s %9s" % ("序","品牌","档次","房量","平均房价","年营收","改造投资","单房投资","净现值30","内部IRR"))
RESA = []
for b in BRANDS:
    r = build(b); RESA.append(r)
    L("   %-4s %-18s %-8s %4d %8.0f %9.1f %10.1f %9.1f %10.1f %9s"
      % (r["key"], r["name"][:16], r["tier_cn"], r["n"], r["adr"], r["seg"]["total"], r["capex"], r["per_key"], r["npv"], P(r["irr"])))
ORDER = sorted(RESA, key=lambda x: -x["npv"])
L("")
L("   价值排序：")
for i, r in enumerate(ORDER, 1):
    L("   %2d. %-4s %-18s 净现值 %9.1f 万｜单房 %6.1f 万｜IRR %7s｜%s" % (i, r["key"], r["name"][:16], r["npv"], r["per_key"], P(r["irr"]), r["loc"]))

L("")
L("=== 4. 3 改 2 情景（按品牌面积门槛）===")
R32 = []
for b in BRANDS:
    if b[3] == 0: continue
    r = build(b, room_mode="3改2"); R32.append(r)
    L("   %-4s %-18s 房量%3d｜客房单间%6.2f 万｜改造投资%9.1f 万｜净现值%9.1f 万｜IRR %7s"
      % (r["key"], r["name"][:16], r["n"], r["room_cost"]/r["n"], r["capex"], r["npv"], P(r["irr"])))

L("")
L("=== 5. 自建品牌路径 ===")
own = build(BRANDS[0], own=True)
L("   集团自有高端品牌（锦宾国际体系，零抽佣）：净现值 %+.1f 万｜IRR %s｜单房 %6.1f 万"
  % (own["npv"], P(own["irr"]), own["per_key"]))
L("   对照 皇冠续约：净现值 %+.1f 万｜IRR %s" % (RESA[0]["npv"], P(RESA[0]["irr"])))

L("")
L("=== 6. 净现值转正路径（B01 皇冠基准）===")
b20 = build(BRANDS[0], months=12, horizon=20)
b30 = build(BRANDS[0], months=12, horizon=30)
PATHS = [("P1 经营期 20→30 年", dict(horizon=30)),
         ("P2 全停业改分期开业（4 月全停 + 12 月渐进）", dict(phased=True, months=4)),
         ("P3 品牌方承担 30% 改造投入", dict(brand_share=0.30)),
         ("P4 政策性补贴 3,000 万", dict(subsidy=3000.0)),
         ("P5 P2 + P1", dict(phased=True, months=4, horizon=30)),
         ("P6 P5 + P3", dict(phased=True, months=4, horizon=30, brand_share=0.30)),
         ("P7 P6 + P4", dict(phased=True, months=4, horizon=30, brand_share=0.30, subsidy=3000.0)),
         ("P8 P7 + 收入提升 10%", dict(phased=True, months=4, horizon=30, brand_share=0.30, subsidy=3000.0, boost=1.10))]
PATHROWS = []
L("   基准（B01 全停业 12 月 · 20 年）：净现值 %+.1f 万｜IRR %s" % (b20["npv"], P(b20["irr"])))
for lbl, kw in PATHS:
    r = build(BRANDS[0], months=kw.pop("months", 12), **kw)
    PATHROWS.append((lbl, r["npv"], r["irr"]))
    L("   %-38s 净现值 %9.1f 万｜较基准 %+9.1f｜IRR %7s" % (lbl, r["npv"], r["npv"]-b20["npv"], P(r["irr"])))

L("")
L("=== 7. 人防（部分地下层六级）三方案 ====")
HUMAN = [("方案一 保持现状不动，仅补齐人防竣工资料与备案", "不触碰人防区，功能维持现状；向成都警备区补报竣工资料并办理备案", 30, 70,
          "无施工风险；B2 泳池、员工厨房、冷源机房功能腾挪受限"),
         ("方案二 人防区功能腾挪并报请警备区变更", "将冷源机房与后场功能迁出人防区，局部拆除防护构件后重建并报批", 800, 1500,
          "触发人防工程变更审批，周期不可控；须先取得警备区书面意见"),
         ("方案三 拆除人防功能并恢复普通地下室", "拆除防护结构与滤毒通风，恢复为普通地下室", 1500, 2600,
          "须经警备区批准，实质不可能，不得作为基准方案")]

json.dump(dict(base=BASE, seg_split=SPLIT, nonroom_share=NONROOM_SHARE, anchors=ANCH,
               tiers=TIERS, brands=RESA, order=[r["key"] for r in ORDER], r32=R32, own=own,
               closure=CL, paths=[(l, n, i) for l, n, i in PATHROWS],
               b20=dict(npv=b20["npv"], irr=b20["irr"]), b30=dict(npv=b30["npv"], irr=b30["irr"]),
               human=[list(x) for x in HUMAN],
               brands_meta=[list(b) for b in BRANDS],
               price_anchor=PRICE_ANCHOR),
          open(os.path.join(T, "v52.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
L("DONE")
