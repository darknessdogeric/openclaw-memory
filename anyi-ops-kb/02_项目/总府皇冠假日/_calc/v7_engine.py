# -*- coding: utf-8 -*-
"""v7 引擎：CAPEX 按房型面积分档 + 公区分项（保留石材/拆除重做两情景）
   停业方案口径修正 + 声誉损失全渠道 + 10年/20年双口径门槛复核"""
import io, os, sys, re, json, importlib.util
D = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc"
T = r"D:\B166ER-openclaw\workspace\.tmp"
LOG = open(os.path.join(T, "v7.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()

spec = importlib.util.spec_from_file_location("v6", os.path.join(D, "v6_launch.py"))
V = importlib.util.module_from_spec(spec); spec.loader.exec_module(V)

# ═════════ 1. 解析房间分布表 → 房型清单 ═════════
RD = os.path.join(D, "batch1_extra",
    "1. 物业基础档案 工程部 2026. 11.2_② 客房总数与房型构成（标准间、大床房、套房、无障碍房）及各房型净面积 OK_房间分布表.xls.txt")
raw = open(RD, encoding="utf-8").read()
rooms = []
for line in raw.split("\n"):
    if not line.startswith("|") and " | " not in line:
        continue
    if re.search(r"\d+楼", line) and re.match(r"^\|?\s*\d+楼", line.strip()):
        continue
    if line.strip().startswith("备注") or line.strip().startswith("---") or line.strip().startswith("#"):
        continue
    for cell in line.split("|"):
        cell = cell.strip()
        m = re.match(r"^(\d{3,4})\s+(.*)$", cell)
        if not m:
            continue
        no, tags = m.group(1), m.group(2)
        fl = int(no[:-2]) if len(no) >= 3 else 0
        if fl < 5 or fl > 24:
            continue
        tl = [t for t in re.split(r"[、,，]", tags) if t]
        if "套房" in tl and "小套房" not in tl:
            typ = "套房"
        elif "小套房" in tl:
            typ = "小套房"
        elif "障碍房" in tl:
            typ = "无障碍房"
        elif "大床" in tl:
            typ = "大床房"
        elif "小床" in tl:
            typ = "小床房"
        elif "可变床" in tl:
            typ = "可变床房"
        else:
            typ = "其他房"
        rooms.append(dict(no=no, floor=fl, typ=typ,
                          area_band="行政层" if fl >= 17 else "普通层",
                          connect="联通门" in tl, tail="尾房" in tl,
                          kitchen="厨房" in tl, bad="状态差" in tl,
                          office="办公室" in tl))
from collections import Counter
cnt = Counter((r["area_band"], r["typ"]) for r in rooms)
L("房型计数:", dict(cnt), " 合计:", len(rooms))

# ═════════ 2. 房型面积（净 + 卫）═════════
AREA = {
 ("行政层","大床房"): 22.5, ("行政层","小床房"): 22.5, ("行政层","可变床房"): 22.5,
 ("行政层","套房"): 40.6, ("行政层","小套房"): 32.0, ("行政层","无障碍房"): 25.0,
 ("行政层","其他房"): 22.5,
 ("普通层","大床房"): 25.0, ("普通层","小床房"): 25.0, ("普通层","可变床房"): 25.0,
 ("普通层","套房"): 45.6, ("普通层","小套房"): 34.0, ("普通层","无障碍房"): 25.0,
 ("普通层","其他房"): 25.0,
}
# 面积来源：客房总面积 10,192㎡ ÷ 402 间在售 = 25.35㎡/间（含卫生间）
# 房型面积表抽样：普通层 16.39–22.59㎡（净）+卫；行政层 14.33–19.50㎡（净）+卫
# 套房：普通层 33.11/34.07/39.89/43.27；行政层 29.92/31.02/34.30/35.19

# ═════════ 3. 客房改造单价（元/㎡ 改造面积，含硬装+软装+家具装置设备）═════════
RATE_ROOM = {
 "沿用皇冠·不减房":  dict(标准=3200, 套房=4200, 无障碍=3600, 小套房=3800, 可变床=3200),
 "沿用皇冠·3改2":    dict(标准=5500, 套房=6800, 无障碍=6000, 小套房=6200, 可变床=5500),
 "换奢牌·不减房":    dict(标准=9800, 套房=12000, 无障碍=10500, 小套房=11000, 可变床=9800),
 "换奢牌·3改2":      dict(标准=9800, 套房=12000, 无障碍=10500, 小套房=11000, 可变床=9800),
}
# 3改2 后面积（扩至 40㎡+ 套内）
AREA_32 = dict(标准=45.6, 套房=58.0, 无障碍=46.0, 小套房=48.0, 可变床=45.6)

def room_capex(tier, to_32):
    """按房型面积分档计算客房改造投资（万元）"""
    amap = AREA_32 if to_32 else AREA
    rate = RATE_ROOM[tier]
    out = {}
    for (band, typ), n in cnt.items():
        a = amap.get((band, typ), amap.get((band, "大床房"), 25.0))
        if typ in ("套房", "小套房", "无障碍房"):
            r = rate.get(typ, rate["标准"])
        elif typ == "可变床房":
            r = rate["可变床"]
        else:
            r = rate["标准"]
        out[(band, typ)] = dict(n=n, area=a, rate=r, wan=round(n * a * r / 10000.0, 1))
    return out

# ═════════ 4. 公区面积底表（物业基础档案 工程概况 + 产权监理面积）═════════
PUBLIC = [
 ("大堂及前台", 5467.8, "工程概况：大堂 5,467.8㎡；1F 建面 5,473.92㎡"),
 ("全日餐饮与酒吧", 1574.0, "工程概况：餐厅 1,574㎡ / 490 餐位"),
 ("宴会与会议", 1860.0, "宴会 600㎡ + 350㎡；14 间会议室约 65㎡/间"),
 ("行政酒廊", 277.0, "21F 行政酒廊 221㎡ + 酒廊会议室 56㎡"),
 ("客房层公共区（走廊/电梯厅/布草）", 12453.0, "客房层建面 22,645.47㎡ − 客房套内 10,192㎡"),
 ("娱乐康体（水疗/泳池/健身）", 3780.0, "工程概况：娱乐部 3,780㎡"),
 ("后场（厨房/员工区/洗衣/仓储/工程）", 6000.0, "厨房 1,975.4㎡ + 地下及后勤功能区改造范围"),
]
RATE_PUBLIC = {
 "保留石材（功能更新+局部翻新）": dict(大堂=1800, 全日餐饮与酒吧=2200, 宴会与会议=2000, 行政酒廊=3000,
        客房层公共区=1100, 娱乐康体=1500, 后场=500),
 "拆除重做（全面拆除更新）": dict(大堂=4500, 全日餐饮与酒吧=3800, 宴会与会议=3200, 行政酒廊=5500,
        客房层公共区=2000, 娱乐康体=3000, 后场=800),
 "奢牌级拆除重做": dict(大堂=6500, 全日餐饮与酒吧=5200, 宴会与会议=4600, 行政酒廊=8000,
        客房层公共区=3000, 娱乐康体=4500, 后场=1000),
 "奢牌级保留石材": dict(大堂=3600, 全日餐饮与酒吧=3000, 宴会与会议=2800, 行政酒廊=5000,
        客房层公共区=2000, 娱乐康体=2800, 后场=800),
}
def public_capex(scn):
    out = []
    for name, a, note in PUBLIC:
        r = RATE_PUBLIC[scn].get(name, 1000)
        out.append(dict(name=name, area=a, rate=r, wan=round(a * r / 10000.0, 1), note=note))
    return out

# ═════════ 5. 机电/消防等硬约束（沿用 v6 已按台账逐项核定，不重复计列）═════════
def base_items(v6key, capex_room, capex_public, extra_brand=0.0, extra_art=0.0, extra_preopen=0.0, cont=0.039):
    it = []
    for nm, v, note in V.CAPEX[v6key]["items"]:
        if nm in ("客房改造", "公区改造", "公区必要整改", "品牌专项（VI/客用品/钥匙卡/PIP 销项）",
                  "品牌专项（VI 全套）", "品牌专项（外部奢牌 VI + 品牌方条件）",
                  "艺术品与在地策展", "开业前费用", "不可预见费",
                  "康养 SPA 与泳池迁址", "康养 SPA 与旗舰泳池", "景观庭院与市政界面"):
            continue
        it.append((nm, v, note))
    it.append(("客房改造（按房型面积分档）", round(capex_room, 0), "见客房改造分项表"))
    it.append(("公共区域改造", round(capex_public, 0), "见公共区域分项表"))
    if extra_brand:
        it.append(("品牌专项（视觉识别系统与客用品）", round(extra_brand, 0), "换牌全案"))
    if extra_art:
        it.append(("艺术品与在地策展", round(extra_art, 0), "在地文化策展"))
    if extra_preopen:
        it.append(("开业前费用", round(extra_preopen, 0), "国际酒店管理公司标准"))
    sub = sum(x[1] for x in it)
    it.append(("不可预见费", round(sub * cont, 0), "%.1f%%" % (cont * 100)))
    return it

DIRS = {}
# 方向一：沿用皇冠 · 不减房 · 公区保留石材
rm = room_capex("沿用皇冠·不减房", False)
pb = public_capex("保留石材（功能更新+局部翻新）")
DIRS["D1"] = dict(name="方向一 沿用皇冠·不减房（402 间）", tier="沿用皇冠", rooms=402, sellable=402,
    adr=750.0, occ=0.70, rooms_map=rm, pub_map=pb,
    items=base_items("D1", sum(v["wan"] for v in rm.values()), sum(v["wan"] for v in pb),
                     extra_brand=420, cont=0.039))
# 方向二：沿用皇冠 · 3改2 至 268 间 · 公区保留石材
rm = room_capex("沿用皇冠·3改2", True)
pb = public_capex("保留石材（功能更新+局部翻新）")
DIRS["D2"] = dict(name="方向二 沿用皇冠·3改2（268 间）", tier="沿用皇冠", rooms=268, sellable=268,
    adr=750.0, occ=0.70, rooms_map=rm, pub_map=pb,
    items=base_items("D2", sum(v["wan"] for v in rm.values()), sum(v["wan"] for v in pb),
                     extra_brand=420, cont=0.039))
# 方向三：换奢牌 · 不减房 · 公区奢牌级拆除重做
rm = room_capex("换奢牌·不减房", False)
pb = public_capex("奢牌级拆除重做")
DIRS["D3"] = dict(name="方向三 换奢牌·不减房（402 间）", tier="换奢牌", rooms=402, sellable=402,
    adr=880.0, occ=0.70, rooms_map=rm, pub_map=pb,
    items=base_items("D3", sum(v["wan"] for v in rm.values()), sum(v["wan"] for v in pb),
                     extra_brand=780, extra_art=1250, extra_preopen=320, cont=0.08))
# 方向四：换奢牌 · 3改2 至 268 间 · 公区奢牌级拆除重做
rm = room_capex("换奢牌·3改2", True)
pb = public_capex("奢牌级拆除重做")
DIRS["D4"] = dict(name="方向四 换奢牌·3改2（268 间）", tier="换奢牌", rooms=268, sellable=268,
    adr=880.0, occ=0.70, rooms_map=rm, pub_map=pb,
    items=base_items("D3", sum(v["wan"] for v in rm.values()), sum(v["wan"] for v in pb),
                     extra_brand=780, extra_art=1250, extra_preopen=320, cont=0.08))
# 情景：换奢牌·不减房 但公区保留石材
rm = room_capex("换奢牌·不减房", False)
pb = public_capex("奢牌级保留石材")
DIRS["D3s"] = dict(name="方向三 换奢牌·不减房·公区保留石材（402 间）", tier="换奢牌", rooms=402, sellable=402,
    adr=880.0, occ=0.70, rooms_map=rm, pub_map=pb,
    items=base_items("D3", sum(v["wan"] for v in rm.values()), sum(v["wan"] for v in pb),
                     extra_brand=780, extra_art=1250, extra_preopen=320, cont=0.08))

for k, d in DIRS.items():
    tot = sum(x[1] for x in d["items"])
    d["capex"] = tot
    d["per_key"] = round(tot / d["rooms"], 2)
    L("=== %s ===" % k)
    L("  总投资 %s 万 | 单间 %.2f 万 | 客房 %s 万 | 公区 %s 万" %
      (tot, d["per_key"], round(sum(v['wan'] for v in d['rooms_map'].values())),
       round(sum(v['wan'] for v in d['pub_map']))))

# ═════════ 6. 停业期损失 + 声誉损失（全渠道）═════════
SE = V.SE
def closure_loss(start_month, months, fixed_monthly=284.0, brand_ret=0.0):
    rows = []; tot = 0.0
    for k in range(months):
        m = ((start_month - 1 + k) % 12) + 1
        rev = SE["season"][m]["rev"] / 1e4
        loss = rev + fixed_monthly + brand_ret
        tot += loss
        rows.append(dict(month=m, rev_lost=round(rev, 1), fixed=fixed_monthly, brand=round(brand_ret, 1), loss=round(loss, 1)))
    return rows, round(tot, 1)

# 声誉损失：全渠道（停业期 + 复业后 24 个月），按稳态营收比例
REP_CH = [
 ("在线旅行社平台（携程/美团/去哪儿/飞猪/同程）", 0.42, "评分下调→自然排序与转化率下降；复业后需重新累积评价"),
 ("国际在线旅行社（Agoda/Booking/Trip.com）", 0.18, "境外客源评分基数下滑最明显"),
 ("品牌会员体系（国际酒店管理公司会员与积分）", 0.14, "会员积分失效、客史迁移、复业后活跃度重建"),
 ("协议客户与商旅（政企协议、长住与公司客户）", 0.16, "协议中断后重建周期最长，黏性客户流失"),
 ("旅行社与团队客房（旅游批发与团体）", 0.05, "团房配额与渠道关系中断"),
 ("会议婚宴与本地客源", 0.05, "本地宴席与会议提前锁定替代场地"),
]
def reputation_loss(steady_rev, months_closed, reopen_years=2):
    """停业期无营收流入；声誉损失体现为复业后 24 个月相对正常爬坡的额外缺口 + 一次性重建费用"""
    out = []
    tot = 0.0
    for nm, share, note in REP_CH:
        # 复业后第1年按营收折损 8.5%、第2年 3.0%（渠道恢复速度差异）
        d1 = steady_rev * share * 0.085 * reopen_years * 0.75
        d2 = steady_rev * share * 0.030 * reopen_years * 0.25
        oneoff = steady_rev * share * 0.012
        w = round(d1 + d2 + oneoff, 1)
        tot += w
        out.append(dict(name=nm, share=share, y1=round(d1, 1), y2=round(d2, 1), rebuild=round(oneoff, 1), wan=w, note=note))
    return out, round(tot, 1)

# ═════════ 7. 现金流与门槛复核（10年窗口 + 20年全周期）═════════
def run(dk_key, scen="中性", horizon=20, closure_months=14, closure_start=12, phased=False):
    d = DIRS[dk_key]
    capex = d["capex"]
    rooms = d["rooms"]
    adr, occ = d["adr"], d["occ"]
    # 稳定年营收（按房量、房价、出租率估算，口径：客房收入 + 餐饮会议等非客房收入）
    occ_n = occ
    rooms_rev = rooms * 365 * occ_n * adr / 1e4
    total_rev = rooms_rev * 1.42  # 非客房收入系数（餐饮/会议/康体）
    brand_base = total_rev * 0.025 if d["tier"] == "换奢牌" else total_rev * 0.020
    brand_ret = brand_base * 0.35 / 12.0
    cl_rows, cl_total = closure_loss(closure_start, closure_months, 284.0, brand_ret)
    # 稳定年业主经营利润
    gop_rate = 0.402 if d["tier"] == "换奢牌" else 0.293
    gop = total_rev * gop_rate
    fees = dict(base=brand_base, marketing=total_rev * (0.025 if d["tier"]=="换奢牌" else 0.030),
                loyalty=total_rev * 0.020, reservation=total_rev * (0.015 if d["tier"]=="换奢牌" else 0.0),
                ffe=total_rev * (0.040 if d["tier"]=="换奢牌" else 0.020))
    incentive = gop * (0.10 if d["tier"]=="换奢牌" else 0.06)
    owner_gop = gop - fees["base"] - fees["marketing"] - fees["loyalty"] - fees["reservation"] - fees["ffe"] - incentive
    # 年现金流
    cfs = []
    for y in range(1, horizon + 1):
        mis = max(0, 12 - closure_months) if y == 1 else 0
        ramp = 0.90 if y == 1 else (1.00 if y == 2 else 1.0)
        rev_y = total_rev * ramp * (1 - mis / 12.0 if y == 1 else 1.0)
        gop_y = rev_y * gop_rate
        og = gop_y - (fees["base"]/1.0*rev_y/total_rev if total_rev else 0) - (fees["marketing"]*rev_y/total_rev) \
             - (fees["loyalty"]*rev_y/total_rev) - (fees["reservation"]*rev_y/total_rev) \
             - (fees["ffe"]*rev_y/total_rev) - gop_y*(incentive/gop if gop else 0)
        cf = og - (capex if y == 1 else 0.0)
        # 复业后声誉折损（Y2、Y3）
        if y in (2, 3):
            cf -= total_rev * (0.085 if y == 2 else 0.030)
        cfs.append(cf)
    def irr(cf, lo=-0.95, hi=10.0, tol=1e-9):
        def npv(r): return sum(c / (1+r)**i for i, c in enumerate(cf))
        if npv(lo) * npv(hi) > 0: return None
        for _ in range(300):
            mid = (lo+hi)/2
            if npv(lo) * npv(mid) <= 0: hi = mid
            else: lo = mid
        return (lo+hi)/2
    def payback(cf):
        c = 0.0
        for i, x in enumerate(cf):
            c += x
            if c >= 0: return i+1
        return None
    def dyn_payback(cf, r=0.08):
        c = 0.0
        for i, x in enumerate(cf):
            c += x / (1+r)**i
            if c >= 0: return i+1
        return None
    npvf = lambda cf, r=0.08: round(sum(c/(1+r)**i for i, c in enumerate(cf)), 1)
    cfs10 = cfs[:10]
    return dict(
        dk=dk_key, name=d["name"], capex=capex, per_key=d["per_key"], rooms=rooms,
        steady_rev=round(total_rev, 1), owner_gop=round(owner_gop, 1),
        gop_rate=gop_rate, closure_months=closure_months, closure_total=cl_total,
        irr20=irr(cfs), irr10=irr(cfs10), npv20=npvf(cfs), npv10=npvf(cfs10),
        pb20=payback(cfs), dpb20=dyn_payback(cfs), pb10=payback(cfs10),
        cfs=cfs, rep=reputation_loss(total_rev, closure_months),
    )

res = {}
for k in ("D1", "D2", "D3", "D4", "D3s"):
    r = run(k)
    res[k] = r
    L("--- %s ---" % k)
    L("  总投资 %s 万 单间 %.2f 万 | 稳态营收 %s 万 | 业主经营利润 %s 万" % (r["capex"], r["per_key"], r["steady_rev"], r["owner_gop"]))
    L("  IRR20 %s | IRR10 %s | NPV20 %s | 静态 %s | 动态 %s | 停业损失 %s 万" %
      (("%.2f%%" % (r["irr20"]*100)) if r["irr20"] else "无", ("%.2f%%" % (r["irr10"]*100)) if r["irr10"] else "无",
       r["npv20"], r["pb20"], r["dpb20"], r["closure_total"]))
    L("  声誉损失合计 %s 万（分渠道 %s）" % (r["rep"][1], [x["wan"] for x in r["rep"][0]]))

json.dump({k: {kk: vv for kk, vv in v.items() if kk != "cfs"} for k, v in res.items()},
          open(os.path.join(T, "v7_result.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({k: v["cfs"] for k, v in res.items()}, open(os.path.join(T, "v7_cfs.json"), "w", encoding="utf-8"))
L("DONE")
