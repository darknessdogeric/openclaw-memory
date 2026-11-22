# -*- coding: utf-8 -*-
"""v21：按品牌档次重建定价与经营模型
   ① 三档价位 620/750/880 = 五星级低/中/高（皇冠假日、洲至奢选可引用高档值）
   ② 外部奢牌 = 成都两档真实价格带：1,500—2,000（主流奢华）与 3,000+（顶级设计型）
   ③ 新增「改造前基线 vs 改造后」收入对照（改房的必要性判据）
   ④ GOP 率、非房收入系数、品牌费率随档次调整
"""
import io, os, sys, re, json, importlib.util
T = r"D:\B166ER-openclaw\workspace\.tmp"
D = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc"
LOG = open(os.path.join(T, "v21.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()

RES = {x["key"]: x for x in json.load(open(os.path.join(T, "v9.json"), encoding="utf-8"))}
spec = importlib.util.spec_from_file_location("v10", os.path.join(D, "v10_econ.py"))
V10 = importlib.util.module_from_spec(spec)
try: spec.loader.exec_module(V10)
except Exception as e: L("v10 note:", str(e)[:160])

def N(v, d=1): return format(round(v, d), ",.%df" % d)
def P(v): return ("%.2f%%" % (v * 100)) if v is not None else "无可解内部收益率"

# ══════════ 档次经营参数 ══════════
# 依据：成都实际房价带（2026 实测）+ 行业基准（酒店分级分类基准参数体系 v1.0）
TIER = {
 "皇冠假日": dict(
    label="皇冠假日（洲际集团高端有限服务）", tier="五星高端",
    adr=(620.0, 750.0, 880.0),          # 五星级低/中/高
    adr_note="620/750/880 为五星级低/中/高；成都 2024 五星级 ADR 736.66 元（重庆口径）、2025 成都高端及中高端平均每间可售房收入 834 元可作交叉校验",
    occ=0.70, gop=0.300, nonroom=1.42,
    base=0.020, mkt=0.030, loy=0.020, ffe=0.020, inc=0.060),
 "洲至奢选": dict(
    label="洲至奢选（洲际集团奢华档，成都棕榈泉 335 间已开业）", tier="五星至奢华之间",
    adr=(750.0, 880.0, 880.0),          # Eric 指示：可引用五星高档值
    adr_note="按 Eric 指示引用五星高档值 880 元；洲至奢选成都棕榈泉实价约 900 元起（$127 起），可交叉校验",
    occ=0.70, gop=0.330, nonroom=1.55,
    base=0.025, mkt=0.025, loy=0.020, ffe=0.030, inc=0.080),
 "外部奢牌": dict(
    label="外部奢牌（丽晶、康莱德、费尔蒙、金普顿等）", tier="奢华",
    adr=(1500.0, 1750.0, 3000.0),      # 成都两档真实价格带
    adr_note="成都奢华实际两档：1,500—2,000 元（瑞吉 1,500—2,000、华尔道夫 1,400—1,800、尼依格罗 1,180—1,800）与 3,000+ 元（居舍 2,000—3,000）；本表取 1,500/1,750/3,000 三档，分别对应主流奢华与顶级设计型",
    occ=0.70, gop=0.400, nonroom=1.85,
    base=0.030, mkt=0.025, loy=0.020, ffe=0.040, inc=0.100),
}

# ══════════ 改造前基线（实测，不改造）══════════
BASE = dict(
    rooms=402, adr=363.99, occ=0.7078,
    rooms_rev=402 * 365 * 0.7078 * 363.99 / 1e4,
    total_rev=564.5 * 12,           # 近 24 个月月均 564.5 万 × 12
    owner_cf=-1924.0,               # 年均经营现金流（业主口径实测）
    rooms_total=415, sellable=402,
)
BASE["nonroom_ratio"] = BASE["total_rev"] / BASE["rooms_rev"]
L("=== 改造前基线 ===")
L("  402 间在售｜平均房价 %.2f 元｜出租率 %.2f%%" % (BASE["adr"], BASE["occ"] * 100))
L("  客房年收入 %.1f 万｜总营业收入 %.1f 万｜业主经营现金流 %.1f 万" %
  (BASE["rooms_rev"], BASE["total_rev"], BASE["owner_cf"]))
L("  非房/客房 = %.3f" % BASE["nonroom_ratio"])

# ══════════ 方案定义 ══════════
# key, 品牌, 公区做法, 房量做法, ADR 档位序号, 可行性
SCHEMES = [
 ("S1",  "皇冠假日", "保留", "不减房", 1, "基准候选：投资最低、无换牌摩擦"),
 ("S2",  "皇冠假日", "保留", "3改2",  1, "减房后收入基数下降，且面积口径须复核"),
 ("S3",  "皇冠假日", "重做", "不减房", 1, "公区重做提升观感，但段三投资抬升"),
 ("S4",  "洲至奢选", "保留", "不减房", 1, "五星高档房价，品牌升级有限"),
 ("S5",  "洲至奢选", "重做", "不减房", 1, "奢牌级公区全量重做"),
 ("S6",  "洲至奢选", "重做", "3改2",  1, "面积与公区同时达标"),
 ("S7",  "外部奢牌", "重做", "3改2",  1, "主流奢华价格带（1,750 元）"),
 ("S7B","外部奢牌", "重做", "3改2",  2, "顶级设计型价格带（3,000 元）"),
 ("S8",  "外部奢牌", "重做", "不减房", 1, "不可行：25.35 ㎡ 低于所有候选奢牌客房面积门槛"),
]

def run_one(key, brand, pub_mode, room_mode, adr_idx):
    t = TIER[brand]
    x = RES[key if key in RES else ("S7" if key == "S7B" else key)]
    n_rooms = x["n_rooms"]
    adr = t["adr"][adr_idx]
    mep = x["mep"]; fit = x["fitout"]; months = x["months"]
    # 改造投资（与 v9 一致）
    capex = mep + fit
    # 经营模型（用 v10 的现金流结构，但替换品牌参数）
    b = dict(adr=adr, gop=t["gop"], base=t["base"], mkt=t["mkt"], loy=t["loy"],
             ffe=t["ffe"], inc=t["inc"], nonroom=t["nonroom"], occ=t["occ"])
    room_rev_y = n_rooms * 365 * b["occ"] * adr / 1e4
    total_rev_y = room_rev_y * b["nonroom"]
    brand_base_y = total_rev_y * b["base"]
    brand_ret_m = brand_base_y * 0.35 / 12.0 if brand != "皇冠假日" else 0.0
    horizon = 20
    mcf = []
    for tt in range(1, horizon * 12 + 1):
        rev = 0.0
        if tt > months:
            since = tt - months
            ramp = min(1.0, 0.62 + 0.038 * since)
            rev = (total_rev_y / 12.0) * ramp
        gop = rev * b["gop"]; r_ = rev / total_rev_y if total_rev_y else 0
        owner = (gop - brand_base_y * r_ - total_rev_y * b["mkt"] * r_
                 - total_rev_y * b["loy"] * r_ - total_rev_y * b["ffe"] * r_
                 - gop * b["inc"])
        cash = owner
        if tt <= months:
            cash -= 284.0
            cash -= brand_ret_m
        half = max(1, months // 2)
        if 1 <= tt <= half: cash -= capex * 0.6 / half
        elif half < tt <= months: cash -= capex * 0.4 / max(1, months - half)
        if tt > months:
            since = tt - months
            if since < 12: cash -= total_rev_y * 0.085 / 12.0
            elif since < 24: cash -= total_rev_y * 0.030 / 12.0
            if since < 6: cash -= total_rev_y * 0.012 / 6.0
        mcf.append(cash)
    acf = [round(sum(mcf[y * 12:(y + 1) * 12]), 1) for y in range(horizon)]
    cf10 = acf[:10]
    ann = (total_rev_y * b["gop"] - total_rev_y * (b["base"] + b["mkt"] + b["loy"] + b["ffe"])
           - total_rev_y * b["gop"] * b["inc"])
    grp = [-capex] + [ann] * 20
    inc_cf = [acf[i] - BASE["owner_cf"] for i in range(20)]
    def pv(cf, r=0.08): return round(sum(c / (1 + r) ** i for i, c in enumerate(cf)), 1)
    return dict(
        key=key, brand=brand, pub_mode=pub_mode, room_mode=room_mode, adr=adr,
        adr_idx=adr_idx, n_rooms=n_rooms, months=months,
        capex=capex, mep=mep, fit=fit, total_need=capex + 815.0 * months,
        loss=815.0 * months,
        steady_rev=total_rev_y, rooms_rev=room_rev_y, revpar=adr * b["occ"],
        owner_ann=round(ann, 1),
        rev_vs_base=round(total_rev_y - BASE["total_rev"], 1),
        rev_ratio=round(total_rev_y / BASE["total_rev"], 3),
        irr20=V10.irr(acf), npv20=pv(acf), pb20=V10.payback(acf),
        irr10=V10.irr(cf10), npv10=pv(cf10), pb10=V10.payback(cf10),
        irr_grp=V10.irr(grp), npv_grp=pv(grp),
        pb_grp=round(capex / ann, 2) if ann > 0 else None,
        irr_inc=V10.irr(inc_cf), npv_inc=pv(inc_cf), pb_inc=V10.payback(inc_cf),
        acf=acf)

OUT = []
for key, brand, pm, rm, ai, feas in SCHEMES:
    r = run_one(key, brand, pm, rm, ai)
    r["feas"] = feas
    OUT.append(r)
    L("--- %s %s·%s·%s | ADR %.0f | 房量 %d | 停业 %d 月" %
      (key, brand, pm, rm, r["adr"], r["n_rooms"], r["months"]))
    L("  稳态年营收 %.1f 万（改造前 %.1f 万，增量 %+.1f 万，倍数 %.2f）" %
      (r["steady_rev"], BASE["total_rev"], r["rev_vs_base"], r["rev_ratio"]))
    L("  改造投资 %.1f 万｜总需求 %.1f 万｜全口径 IRR %s NPV %s 静态 %s" %
      (r["capex"], r["total_need"], P(r["irr20"]), r["npv20"], r["pb20"]))
    L("  集团口径 IRR %s 回收 %s ｜ 增量口径 IRR %s 静态 %s" %
      (P(r["irr_grp"]), r["pb_grp"], P(r["irr_inc"]), r["pb_inc"]))

json.dump(dict(base=BASE, tier={k: {kk: (list(vv) if isinstance(vv, tuple) else vv)
                                 for kk, vv in v.items()} for k, v in TIER.items()},
               schemes=OUT),
          open(os.path.join(T, "v21.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
L("DONE")
