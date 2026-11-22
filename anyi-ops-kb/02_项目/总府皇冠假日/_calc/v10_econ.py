# -*- coding: utf-8 -*-
"""v10：以 v9 三段式造价为输入，重跑经济测算，生成新的第六、九章，并更新结论
   口径：段一 停业损失（现金流内）｜段二 机电水电强弱电及隐蔽工程（品牌无关）｜段三 装修改造（品牌相关）
   三套口径并列：全口径 / 集团口径（改造后年经营现金流÷改造投资）/ 增量口径（相对不改造反事实）"""
import io, os, sys, json, importlib.util
T = r"D:\B166ER-openclaw\workspace\.tmp"
D = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc"
LOG = open(os.path.join(T, "v10.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()

for name in ("v9_engine", "area_base", "v8_caliber"):
    spec = importlib.util.spec_from_file_location(name, os.path.join(D, name + ".py"))
    m = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(m)
        if name == "v9_engine": V9 = m
        elif name == "area_base": AB = m
        else: V8 = m
    except Exception as e:
        L(name, "note:", str(e)[:160])
RES = V9.RES

# ══ 品牌经营参数 ══
BRAND_OP = {
 "皇冠假日":  dict(adr=750.0, gop=0.300, base=0.020, mkt=0.030, loy=0.020, ffe=0.020, inc=0.060, nonroom=1.42),
 "洲至奢选":  dict(adr=830.0, gop=0.400, base=0.025, mkt=0.025, loy=0.020, ffe=0.030, inc=0.100, nonroom=1.42),
 "外部奢牌":  dict(adr=880.0, gop=0.420, base=0.030, mkt=0.025, loy=0.020, ffe=0.040, inc=0.100, nonroom=1.42),
}
FIXED_MONTH = 284.0        # 停业期固定支出（人工+利息+能耗维持）
BASE_CF = -1924.0          # 改造前年均经营现金流（业主口径实测）
CLOSURE_MONTHS_LOSS = 815.0

def irr(cf, lo=-0.99, hi=10.0):
    def f(r): return sum(c / (1 + r) ** i for i, c in enumerate(cf))
    try:
        if f(lo) * f(hi) > 0: return None
    except Exception:
        return None
    for _ in range(400):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0: hi = mid
        else: lo = mid
    return (lo + hi) / 2

def npv(cf, r=0.08): return round(sum(c / (1 + r) ** i for i, c in enumerate(cf)), 1)
def payback(cf):
    c = 0.0
    for i, x in enumerate(cf):
        c += x
        if c >= 0: return i + 1
    return None
def dyn_payback(cf, r=0.08):
    c = 0.0
    for i, x in enumerate(cf):
        c += x / (1 + r) ** i
        if c >= 0: return i + 1
    return None

def econ(x, adr_mul=1.0, occ_mul=1.0, capex_mul=1.0, mep_override=None, months_override=None):
    b = BRAND_OP[x["brand"]]
    n = x["n_rooms"]
    months = x["months"] if months_override is None else months_override
    mep = x["mep"] if mep_override is None else mep_override
    capex = (mep + x["fitout"]) * capex_mul          # 改造投资（不含停业损失）
    room_rev_y = n * 365 * 0.70 * occ_mul * b["adr"] * adr_mul / 1e4
    total_rev_y = room_rev_y * b["nonroom"]
    brand_base_y = total_rev_y * b["base"]
    brand_ret_m = brand_base_y * 0.35 / 12.0 if x["brand"] != "皇冠假日" else 0.0
    mcf = []
    for t in range(1, horizon := 20 * 12 + 1):
        rev = 0.0
        if t > months:
            since = t - months
            ramp = min(1.0, 0.62 + 0.038 * since)
            m = ((t - 1) % 12) + 1
            base_m = total_rev_y / 12.0
            rev = base_m * ramp
        gop = rev * b["gop"]
        r_ = rev / total_rev_y if total_rev_y else 0
        owner = (gop
                 - brand_base_y * r_
                 - total_rev_y * b["mkt"] * r_
                 - total_rev_y * b["loy"] * r_
                 - total_rev_y * b["ffe"] * r_
                 - gop * b["inc"])
        cash = owner
        if t <= months:
            cash -= FIXED_MONTH
            cash -= brand_ret_m
        for (ps, dur, amt) in capex_sched(x, months):
            if ps <= t < ps + dur:
                cash -= amt / dur
        if t > months:
            since = t - months
            if since < 12: cash -= total_rev_y * 0.085 / 12.0
            elif since < 24: cash -= total_rev_y * 0.030 / 12.0
            if since < 6: cash -= total_rev_y * 0.012 / 6.0
        mcf.append(cash)
    acf = [round(sum(mcf[y * 12:(y + 1) * 12]), 1) for y in range(20)]
    cf10 = acf[:10]
    # 增量口径：相对"不改造"反事实
    inc_cf = [acf[i] - BASE_CF for i in range(20)]
    # 集团口径：改造后经营现金流等额年金 + 改造投资，不含爬坡与停业
    group_cf = [-capex] + [(total_rev_y * b["gop"]
                            - total_rev_y * (b["base"] + b["mkt"] + b["loy"] + b["ffe"])
                            - total_rev_y * b["gop"] * b["inc"])] * 20
    grp_ann = (total_rev_y * b["gop"]
               - total_rev_y * (b["base"] + b["mkt"] + b["loy"] + b["ffe"])
               - total_rev_y * b["gop"] * b["inc"])
    return dict(
        dk=x["key"], brand=x["brand"], name="%s %s·%s·%s" % (x["key"], x["brand"], x["pub_mode"], x["room_mode"]), capex=round(capex, 1),
        n_rooms=n, adr=b["adr"], steady_rev=round(total_rev_y, 1),
        owner_ann=round(grp_ann, 1),
        irr20=irr(acf), npv20=npv(acf), pb=payback(acf), dpb=dyn_payback(acf),
        irr10=irr(cf10), npv10=npv(cf10), pb10=payback(cf10),
        irr_inc=irr(inc_cf), npv_inc=npv(inc_cf), pb_inc=payback(inc_cf),
        irr_grp=irr(group_cf), npv_grp=npv(group_cf),
        pb_grp=round(capex / grp_ann, 2) if grp_ann > 0 else None,
        acf=acf)

def capex_sched(x, months):
    """改造投资按施工期分摊：首 60% 在前段、40% 在后段"""
    c = x["mep"] + x["fitout"]
    half = max(1, months // 2)
    return [(1, half, c * 0.6), (1 + half, months - half, c * 0.4)]

ECON = []
for x in RES:
    if x["key"] == "S8":
        continue
    e = econ(x); ECON.append(e)
    L("--- %s %s·%s·%s ---" % (e["dk"], e["brand"], x["pub_mode"], x["room_mode"]))
    L("  改造投资 %s 万（机电 %s ＋ 装修 %s）｜停业损失 %s 万" % (e["capex"], x["mep"], x["fitout"], x["loss"]))
    L("  全口径 IRR %s ｜ NPV %s ｜ 静态 %s" % (("%.2f%%" % (e["irr20"]*100)) if e["irr20"] else "无", e["npv20"], e["pb"]))
    L("  集团口径 IRR %s ｜ 静态回收 %s 年 ｜ 增量口径 IRR %s ｜ 静态 %s" %
      (("%.2f%%" % (e["irr_grp"]*100)) if e["irr_grp"] else "无", e["pb_grp"],
       ("%.2f%%" % (e["irr_inc"]*100)) if e["irr_inc"] else "无", e["pb_inc"]))
json.dump(ECON, open(os.path.join(T, "v10_econ.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
L("DONE")
