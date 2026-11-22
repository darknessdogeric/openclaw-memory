# -*- coding: utf-8 -*-
"""v7 终版：CAPEX 按房型面积分档 + 公区分功能建面（保留石材/拆除重做）
   月度现金流（停业期只有流出无流入）｜声誉全渠道｜20年主口径 + 10年门槛复核"""
import io, os, sys, re, json, importlib.util
from collections import Counter
D = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc"
T = r"D:\B166ER-openclaw\workspace\.tmp"
LOG = open(os.path.join(T, "v7f.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()

spec = importlib.util.spec_from_file_location("v6", os.path.join(D, "v6_launch.py"))
V = importlib.util.module_from_spec(spec); spec.loader.exec_module(V)
SE = V.SE

# ═════════ 1. 房型底表 ═════════
RD = os.path.join(D, "batch1_extra",
    "1. 物业基础档案 工程部 2026. 11.2_② 客房总数与房型构成（标准间、大床房、套房、无障碍房）及各房型净面积 OK_房间分布表.xls.txt")
rooms = []
for line in open(RD, encoding="utf-8").read().split("\n"):
    if line.strip().startswith(("备注", "---", "#")):
        continue
    if re.match(r"^\|?\s*\d+楼", line.strip()):
        continue
    for cell in line.split("|"):
        m = re.match(r"^(\d{3,4})\s+(.*)$", cell.strip())
        if not m:
            continue
        no, tags = m.group(1), m.group(2)
        fl = int(no[:-2])
        if fl < 5 or fl > 24:
            continue
        tl = [t for t in re.split(r"[、,，]", tags) if t]
        if "小套房" in tl: typ = "小套房"
        elif "套房" in tl: typ = "套房"
        elif "障碍房" in tl: typ = "无障碍房"
        elif "大床" in tl: typ = "大床房"
        elif "小床" in tl: typ = "小床房"
        elif "可变床" in tl: typ = "可变床房"
        else: typ = "其他房"
        rooms.append(dict(fl=fl, typ=typ, band="行政层" if fl >= 17 else "普通层"))
CNT = Counter((r["band"], r["typ"]) for r in rooms)
TOTAL_ROOMS = len(rooms)
L("房型:", dict(CNT), "合计", TOTAL_ROOMS)

AREA_STD = {"普通层": 19.6, "行政层": 17.0}
AREA_SUI = {"普通层": 37.0, "行政层": 33.0}
AREA_SML = {"普通层": 30.0, "行政层": 28.0}
def area_of(band, typ, to32):
    if to32:
        if typ == "套房": return 55.0
        if typ == "小套房": return 50.0
        if typ == "无障碍房": return 48.0
        return 48.0
    if typ == "套房": return AREA_SUI[band]
    if typ == "小套房": return AREA_SML[band]
    if typ == "无障碍房": return 25.0
    return AREA_STD[band]

RATE_ROOM = {
 "沿用皇冠·不减房": {"标准": 3200, "套房": 4200, "小套房": 3800, "无障碍": 3600},
 "沿用皇冠·3改2":   {"标准": 5600, "套房": 6800, "小套房": 6200, "无障碍": 6000},
 "换奢牌·不减房":   {"标准": 10500, "套房": 13000, "小套房": 12000, "无障碍": 11500},
 "换奢牌·3改2":     {"标准": 11500, "套房": 14000, "小套房": 13000, "无障碍": 12500},
}
def room_capex(tier, to32):
    rate = RATE_ROOM[tier]; out = {}
    for (band, typ), n in CNT.items():
        a = area_of(band, typ, to32)
        if typ == "套房": r = rate["套房"]
        elif typ == "小套房": r = rate["小套房"]
        elif typ == "无障碍房": r = rate["无障碍"]
        else: r = rate["标准"]
        out[(band, typ)] = dict(n=n, area=a, rate=r, wan=round(n * a * r / 10000.0, 1))
    return out

# ═════════ 2. 公区 ═════════
PUBLIC = [
 ("P1", "大堂及前台", 5467.8, "《物业基础档案·工程概况》大堂 5,467.8㎡；1F 建面 5,473.92㎡"),
 ("P2", "全日餐饮与酒吧", 1574.0, "《物业基础档案·工程概况》餐厅 1,574㎡、490 餐位；厨房 1,975.4㎡"),
 ("P3", "宴会与会议", 1860.0, "宴会厅 600㎡ + 350㎡；14 间会议室约 65㎡/间"),
 ("P4", "行政酒廊", 277.0, "21F 行政酒廊 221㎡ + 酒廊会议室 56㎡"),
 ("P5", "客房层公共区（走廊、电梯厅、布草间）", 12453.0, "客房层建面 22,645.47㎡ − 客房套内 10,192㎡"),
 ("P6", "娱乐康体（水疗、泳池、健身）", 3780.0, "《物业基础档案·工程概况》娱乐部 3,780㎡"),
 ("P7", "后场（厨房、员工区、洗衣、仓储、工程）", 6000.0, "厨房 1,975.4㎡ + 地下及后勤功能区改造范围"),
]
RATE_PUB = {
 "保留石材·功能更新": {"P1": 2200, "P2": 2800, "P3": 2600, "P4": 3800, "P5": 1600, "P6": 2000, "P7": 800},
 "拆除重做·全面更新": {"P1": 4800, "P2": 4200, "P3": 3600, "P4": 6000, "P5": 2600, "P6": 3200, "P7": 1200},
 "奢牌级·拆除重做": {"P1": 6800, "P2": 5400, "P3": 4800, "P4": 8200, "P5": 3200, "P6": 4600, "P7": 1200},
 "奢牌级·保留石材": {"P1": 4000, "P2": 3600, "P3": 3200, "P4": 5400, "P5": 2400, "P6": 3200, "P7": 1000},
}
def public_capex(scn):
    out = []
    for code, name, a, note in PUBLIC:
        r = RATE_PUB[scn][code]
        out.append(dict(code=code, name=name, area=a, rate=r, wan=round(a * r / 10000.0, 1), note=note))
    return out

# ═════════ 3. 方向 ═════════
def base_items(v6key, room_wan, pub_wan, brand=0, art=0, preopen=0, cont=0.05, spa=0):
    skip = ("客房改造", "公区改造", "公区必要整改", "品牌专项（VI/客用品/钥匙卡/PIP 销项）",
            "品牌专项（VI 全套）", "品牌专项（外部奢牌 VI + 品牌方条件）", "艺术品与在地策展",
            "开业前费用", "不可预见费", "康养 SPA 与泳池迁址", "康养 SPA 与旗舰泳池")
    it = [(nm, v, note) for nm, v, note in V.CAPEX[v6key]["items"] if nm not in skip]
    it.append(("客房改造（按房型面积分档）", round(room_wan), "见客房改造分项表"))
    it.append(("公共区域改造（按功能区建面）", round(pub_wan), "见公共区域分项表"))
    if spa: it.append(("康体水疗升级", spa, "现有水疗与泳池升级改造"))
    if brand: it.append(("品牌专项（视觉识别系统与客用品）", brand, "换牌全案"))
    if art: it.append(("艺术品与在地策展", art, "在地文化策展"))
    if preopen: it.append(("开业前费用", preopen, "国际酒店管理公司开业前标准"))
    sub = sum(x[1] for x in it)
    it.append(("不可预见费", round(sub * cont), "%.1f%%" % (cont * 100)))
    return it

DIRS = {}
def mk(key, name, tier, rooms_capex, rooms_rev, adr, lux, to32, pub_scn, v6key,
       brand, art, preopen, cont, closure_m, spa=0):
    rm = room_capex(tier, to32); pb = public_capex(pub_scn)
    items = base_items(v6key, sum(v["wan"] for v in rm.values()), sum(v["wan"] for v in pb),
                       brand, art, preopen, cont, spa)
    tot = sum(x[1] for x in items)
    DIRS[key] = dict(key=key, name=name, tier=tier, rooms_capex=rooms_capex, rooms_rev=rooms_rev,
        adr=adr, lux=lux, rooms_map=rm, pub_map=pb, items=items, capex=tot,
        per_key=round(tot / rooms_capex, 2), pub_scn=pub_scn, closure_m=closure_m, to32=to32)
    L("=== %s ===" % key)
    L("  %s" % name)
    L("  总投资 %s 万 | 改造口径单间 %.2f 万 | 客房 %s 万 | 公区 %s 万 | 停业 %d 个月" %
      (tot, tot / rooms_capex, round(sum(v['wan'] for v in rm.values())),
       round(sum(v['wan'] for v in pb)), closure_m))
    return DIRS[key]

mk("D1", "方向一 沿用皇冠·不减房（官方总房量 415 间，可售 402 间）", "沿用皇冠·不减房",
   415, 402, 750.0, False, False, "保留石材·功能更新", "D1", 420, 0, 0, 0.05, 12, spa=300)
mk("D2", "方向二 沿用皇冠·3改2 至 268 间", "沿用皇冠·3改2",
   268, 268, 750.0, False, True, "保留石材·功能更新", "D2", 420, 380, 240, 0.05, 16)
mk("D3", "方向三 换奢牌·不减房（402 间）", "换奢牌·不减房",
   402, 402, 880.0, True, False, "奢牌级·拆除重做", "D3", 780, 1250, 320, 0.08, 18)
mk("D4", "方向四 换奢牌·3改2 至 268 间", "换奢牌·3改2",
   268, 268, 880.0, True, True, "奢牌级·拆除重做", "D3", 780, 1250, 320, 0.08, 20)
mk("D3R", "方向三 换奢牌·不减房·公区保留石材（402 间）", "换奢牌·不减房",
   402, 402, 880.0, True, False, "奢牌级·保留石材", "D3", 780, 1250, 320, 0.08, 18)
mk("D1X", "方向一 沿用皇冠·不减房·公区拆除重做（402 间）", "沿用皇冠·不减房",
   402, 402, 750.0, False, False, "拆除重做·全面更新", "D1", 420, 0, 0, 0.05, 14, spa=300)

# ═════════ 4. 声誉（全渠道）════════════════
REP_CH = [
 ("国内在线旅行社平台（携程、美团、去哪儿、飞猪、同程）", 0.42, "评分下调→自然排序与转化率下降；复业后需重新累积评价"),
 ("国际在线旅行社（Agoda、Booking、Trip.com）", 0.18, "境外客源评分基数下滑最明显"),
 ("品牌会员体系（国际酒店管理公司会员与积分）", 0.14, "会员积分失效、客史迁移、复业后活跃度重建"),
 ("协议客户与商旅（政企协议、长住与公司客户）", 0.16, "协议中断后重建周期最长，黏性客户流失"),
 ("旅行社与团队客房（旅游批发与团体）", 0.05, "团房配额与渠道关系中断"),
 ("会议婚宴与本地客源", 0.05, "本地宴席与会议提前锁定替代场地"),
]
def reputation(steady_rev):
    rows = []; tot = 0.0
    for nm, share, note in REP_CH:
        y1 = steady_rev * share * 0.085
        y2 = steady_rev * share * 0.030
        one = steady_rev * share * 0.012
        w = round(y1 + y2 + one, 1); tot += w
        rows.append(dict(name=nm, share=share, y1=round(y1,1), y2=round(y2,1), rebuild=round(one,1), wan=w, note=note))
    return rows, round(tot, 1)

# ═════════ 5. 月度现金流 ═════════
SEASON = {m: SE["season"][m]["rev"] / 1e4 for m in range(1, 13)}
SEASON_SUM = sum(SEASON.values())
def irr(cf, lo=-0.99, hi=10.0):
    def f(r): return sum(c / (1+r)**i for i, c in enumerate(cf))
    try:
        if f(lo) * f(hi) > 0: return None
    except Exception:
        return None
    for _ in range(400):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0: hi = mid
        else: lo = mid
    return (lo + hi) / 2
def npv(cf, r=0.08): return round(sum(c / (1+r)**i for i, c in enumerate(cf)), 1)
def payback(cf):
    c = 0.0
    for i, x in enumerate(cf):
        c += x
        if c >= 0: return i + 1
    return None
def dyn_payback(cf, r=0.08):
    c = 0.0
    for i, x in enumerate(cf):
        c += x / (1+r)**i
        if c >= 0: return i + 1
    return None

def run(dk_key, plan="全停业", horizon=20, extra_capex=0.0):
    d = DIRS[dk_key]
    capex = d["capex"] + extra_capex
    rooms_rev = d["rooms_rev"]; adr = d["adr"]; lux = d["lux"]
    gop_rate = 0.402 if lux else 0.293
    occ = 0.70
    room_rev_y = rooms_rev * 365 * occ * adr / 1e4
    total_rev_y = room_rev_y * 1.42
    brand_base = total_rev_y * (0.025 if lux else 0.020)
    brand_ret_m = brand_base * 0.35 / 12.0 if lux else 0.0
    S = 13
    if plan == "全停业":
        phases = [(S, d["closure_m"], 0)]
        total_months = d["closure_m"]
        capex_profile = [(S, d["closure_m"], capex)]
        reopen_at = S + total_months
    else:
        phases = [(S, 10, 160), (S + 10, 10, 255), (S + 20, 999, 415)]
        total_months = 30
        capex_profile = [(S, 10, capex * 0.60), (S + 10, 10, capex * 0.30), (S + 20, 10, capex * 0.10)]
        reopen_at = S + 20
    mcf = []
    for t in range(1, horizon * 12 + 1):
        rooms_open = 0
        for (ps, dur, ro) in phases:
            if ps <= t < ps + dur:
                rooms_open = ro
        op_ratio = rooms_open / rooms_rev if rooms_rev else 0
        if op_ratio >= 0.999:
            rev = 0.0
        else:
            m = ((t - 1) % 12) + 1
            base_m = total_rev_y / 12.0 * SEASON[m] / (SEASON_SUM / 12.0)
            since = t - reopen_at
            ramp = 1.0
            if since >= 0:
                ramp = min(1.0, 0.62 + 0.038 * since)
            rev = base_m * op_ratio * ramp
        gop = rev * gop_rate
        r_ = rev / total_rev_y if total_rev_y else 0
        fee_base = brand_base * r_
        fee_mkt = total_rev_y * (0.025 if lux else 0.030) * r_
        fee_loy = total_rev_y * 0.020 * r_
        fee_res = total_rev_y * (0.015 if lux else 0.0) * r_
        fee_ffe = total_rev_y * (0.040 if lux else 0.020) * r_
        inc = gop * (0.10 if lux else 0.06)
        owner = gop - fee_base - fee_mkt - fee_loy - fee_res - fee_ffe - inc
        cash = owner
        in_construction = any(ps <= t < ps + dur for (ps, dur, ro) in phases if ro == 0 or True) and t >= S
        if t >= S and t < reopen_at + 20:
            cash -= 284.0 * (1.0 if op_ratio == 0 else (1.0 - 0.35 * op_ratio))
            cash -= brand_ret_m
        for (ps, dur, amt) in capex_profile:
            if ps <= t < ps + dur:
                cash -= amt / dur
        since0 = t - reopen_at
        if since0 >= 0:
            if since0 < 12: cash -= total_rev_y * 0.085 / 12.0
            elif since0 < 24: cash -= total_rev_y * 0.030 / 12.0
            if since0 < 6: cash -= total_rev_y * 0.012 / 6.0
        mcf.append(cash)
    acf = [round(sum(mcf[y*12:(y+1)*12]), 1) for y in range(horizon)]
    cf10 = acf[:10]
    og = (total_rev_y * gop_rate - brand_base - total_rev_y*(0.025 if lux else 0.030)
          - total_rev_y*0.020 - total_rev_y*(0.015 if lux else 0)
          - total_rev_y*(0.040 if lux else 0.020) - total_rev_y*gop_rate*(0.10 if lux else 0.06))
    return dict(dk=dk_key, name=d["name"], plan=plan, capex=capex, per_key=d["per_key"],
        rooms=rooms_rev, adr=adr, steady_rev=round(total_rev_y, 1), room_rev=round(room_rev_y, 1),
        gop_rate=gop_rate, owner_gop_steady=round(og, 1), pub_scn=d["pub_scn"],
        acf=acf, irr20=irr(acf), irr10=irr(cf10), npv20=npv(acf), npv10=npv(cf10),
        pb=payback(acf), dpb=dyn_payback(acf), pb10=payback(cf10),
        rep=reputation(total_rev_y))

RES = {}
for k in ("D1", "D2", "D3", "D4", "D3R", "D1X"):
    r = run(k); RES[k] = r
    L("--- %s ---" % k)
    L("  投资 %s 万 单间 %.2f 万 | 稳态营收 %s 万 | 业主GOP %s 万" % (r["capex"], r["per_key"], r["steady_rev"], r["owner_gop_steady"]))
    L("  IRR20 %s | IRR10 %s | NPV20 %s | 静态 %s | 动态 %s | 声誉 %s 万" %
      (("%.2f%%" % (r["irr20"]*100)) if r["irr20"] else "无",
       ("%.2f%%" % (r["irr10"]*100)) if r["irr10"] else "无",
       r["npv20"], r["pb"], r["dpb"], r["rep"][1]))
for k in ("D1", "D3"):
    r = run(k, "分期半停业", extra_capex=2800); RES[k + "_P"] = r
    L("--- %s 分期半停业 ---" % k)
    L("  投资 %s 万 | IRR20 %s | NPV20 %s | 静态 %s | 动态 %s" %
      (r["capex"], ("%.2f%%" % (r["irr20"]*100)) if r["irr20"] else "无", r["npv20"], r["pb"], r["dpb"]))

json.dump({k: {kk: vv for kk, vv in v.items() if kk != "acf"} for k, v in RES.items()},
          open(os.path.join(T, "v7f.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({k: v["acf"] for k, v in RES.items()}, open(os.path.join(T, "v7f_cfs.json"), "w", encoding="utf-8"))
L("DONE")
