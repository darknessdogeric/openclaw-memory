# -*- coding: utf-8 -*-
"""
总府皇冠假日酒店改造升级项目 · 立项经济测算引擎 v6.0 (2026-11-08)

v6 相对 v4/v5 的四项升级（均为本轮全网调研 + 合同一手证据驱动）：
 ① 停业期损失由"均摊 815 万/月"改为"按 24 个月实测逐月曲线 × 固定成本"，并显式决策开工月份
 ② 品牌费用由"打包费率"改为 HMA 制度性分解（base / incentive / marketing / loyalty /
    reservation / IT / training / reimbursables / pre-opening），并新增停业期品牌保留费
 ③ 新增"分期开业（不停业/短停业）"情景，与"一次全停业"并列
 ④ 新增国资口径校验层（IRR 门槛 / 静态回收期 / 资产负债率 / 评估值）

口径：USALI 13 部门制 · 国际联号口径 · 10/20/30 年 · 含隐性成本 · 月度建模
"""
import io, os, sys, json, math
from collections import OrderedDict

_D = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc"
OUT_DIR = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\测算与中间产物"
os.makedirs(OUT_DIR, exist_ok=True)

# ══════════════════════════════════════════════════════════════════
# 0. 实测季节性曲线（2024/10–2026/09，来自《近24个月主要经营指标》）
# ══════════════════════════════════════════════════════════════════
def load_seasonal():
    p = os.path.join(_D, "seasonal_24m.json")
    d = json.load(open(p, encoding="utf-8"))
    s = {int(k): v for k, v in d["season"].items()}
    avg_adr = sum(s[m]["adr"] for m in s) / 12.0
    avg_occ = sum(s[m]["occ"] for m in s) / 12.0
    avg_fnb = sum(s[m]["fnb_ratio"] for m in s) / 12.0
    avg_banq = sum(s[m]["banq_ratio"] for m in s) / 12.0
    avg_rev = sum(s[m]["rev"] for m in s) / 12.0
    for m in s:
        s[m]["adr_idx"] = s[m]["adr"] / avg_adr
        s[m]["occ_idx"] = s[m]["occ"] / avg_occ
        s[m]["fnb_idx"] = s[m]["fnb_ratio"] / avg_fnb
        s[m]["banq_idx"] = s[m]["banq_ratio"] / avg_banq
    return dict(season=s, avg_adr=avg_adr, avg_occ=avg_occ, avg_fnb=avg_fnb,
                avg_banq=avg_banq, avg_rev=avg_rev)

SE = load_seasonal()

# ── 停业期固定成本（第二批次实测口径，万元/月）────────────────────
FIXED_COST = dict(labor_full=182.0, labor_split=70.0, utility=45.81,
                  utility_retention=0.65, maint_contract=3.64, base=231.4, split=115.0)
# 人工 182.0 = 2026 年 1-10 月累计人工成本 1,820.08 万元 ÷ 10；
# 水电气 45.81 = 24 个月实测合计 1,099.39 万元 ÷ 24；合同维保 3.64 = 43.72 万 ÷ 12

# ══════════════════════════════════════════════════════════════════
# 1. HMA 品牌费用制度性分解库（Hotel Development Guide 2026-10 区间
#    + F2-29 洲际一手口径 + 品牌方会议纪要）
# ══════════════════════════════════════════════════════════════════
HMA_INDUSTRY = OrderedDict([
    ("基础管理费 Base Fee",      dict(basis="总营收(不含增值税)", rng="2.0%–4.0%", note="与盈利无关，照付；收入定义至关重要")),
    ("激励费 Incentive Fee",     dict(basis="GOP 或 AGOP(分级)", rng="5.0%–15.0%", note="门槛与结构显著影响结果")),
    ("预订/分销 Reservation",    dict(basis="每单 或 客房收入%", rng="差异极大", note="高量系统可能很可观")),
    ("品牌营销 Marketing",       dict(basis="客房收入%", rng="1.0%–3.0%", note="系统性、通常不可谈")),
    ("忠诚度计划 Loyalty",       dict(basis="每住/每积分/营收%", rng="可变", note="视品牌渗透率与客群结构")),
    ("IT/系统费 IT & Systems",   dict(basis="固定或可变", rng="可变", note="日益重要，常带调整条款")),
    ("培训与质保 Training&QA",   dict(basis="固定/周期性", rng="可变", note="支持品牌标准，可能随新举措上浮")),
    ("可报销费用 Reimbursables", dict(basis="按合同", rng="可变", note="需透明度与加成(markup)审查")),
    ("开业前费用 Pre-opening",   dict(basis="按合同", rng="—", note="⭐ 常按 6–12 个月基础费计，须计入开业成本")),
])

# ══════════════════════════════════════════════════════════════════
# 2. 品牌档位参数（USALI 13 部门制口径；GOP 率取国际基准区间中值）
# ══════════════════════════════════════════════════════════════════
TIER = {
 "intl_current_crowne": dict(
    name="皇冠 3.0 现状口径（委托）",
    mix=dict(rooms=0.649, fnb=0.134, banq=0.144, other=0.020, misc=0.053),
    dept_gop=dict(rooms=0.30, fnb=0.16, banq=0.26, other=0.40, misc=0.60),
    mix_basis="业主实测（2024/10–2026/09 均值）"),
 "intl_upper_upscale": dict(
    name="上奢 / 高端全服务（洲至奢选级）",
    mix=dict(rooms=0.625, fnb=0.250, banq=0.075, other=0.030, misc=0.020),
    dept_gop=dict(rooms=0.58, fnb=0.19, banq=0.28, other=0.45, misc=0.85),
    mix_basis="国际联号标准库"),
 "intl_luxury": dict(
    name="奢华 / 顶奢（外部奢牌级）",
    mix=dict(rooms=0.575, fnb=0.350, banq=0.050, other=0.020, misc=0.005),
    dept_gop=dict(rooms=0.60, fnb=0.20, banq=0.29, other=0.46, misc=0.85),
    mix_basis="国际联号标准库"),
}

# ══════════════════════════════════════════════════════════════════
# 3. CAPEX 全维度明细（万元，中值；工程部台账 + 第一批次资料 + 品牌标准）
# ══════════════════════════════════════════════════════════════════
CAPEX = {
 "D1": dict(name="方向一 · 沿用皇冠 + 仅机电安全与品牌达标（不换牌、不减房）", items=[
   ("客房改造",            0,     "不减房不换牌 → 不做客房重做"),
   ("★电梯范围修正",      0,     "第二批次：1#-8# 已于 2022-2026 陆续更换曳引机/钢丝绳/控制系统 → 维持现状避免二次报废；真正老旧为 9#-11#、14#-16# 共 6 台（2018 登记、以维修投运、9# 故障频繁）→ 计入机电行"),
   ("★锅炉移出范围",      0,     "第二批次：燃气热水锅炉 2.8MW×2 + 1.75MW×2 系 2009-12 投用、设计 15 年、状态正常、每年年检；真空相变锅炉不属特种设备 → 移出本轮改造"),
   ("消防系统",            1180,  "1994 喷淋整体更换 + 1996 报警线路全换 + 防排烟/应急/疏散 + 电气火灾监控 + 防火门监控 + 报审验收；★气体灭火 1 套已于 2018-06 配置（配电室/机房）→ 改为覆盖范围评估；消防水炮 0 台（大堂/宴会厅大空间）→ 新增配置；★报警主机存在 2024-06（消防台账）与 2018-06（弱电台账）矛盾，须回工程部逐项核实"),
   ("强弱电与智能化",      380,   "IB/桥架分层 + 网络与 IPTV + 客控 + 门锁 + 安防门禁 + 治安监控数字化 + IHG Connect 满版"),
   ("机电（冷源/末端/配电/垂直交通）", 1900, "4 台约克离心机 1,230KW 换环保冷媒 + 冷却塔 + AHU 6 台 + 中筒新风机组 25 台（5.5KW×5 + 2.2KW×20）+ FCU 542 台 + 冷冻热水管 100% 更新 + 4 台变压器（1996，设计 20 年）/34 面低压柜/9 面电容柜投运 + 9#-11#、14#-16# 电梯 6 台整机或大修 + 发电机组 2 台（1996，设计 15 年）更新 + 新增主供 6,500KVA/备用 3,250KVA 两路高压更换期临时供电方案"),
   ("给排水隐蔽与末端（新增）", 260, "★第二批次新增：排污泵 14 台（1996 投用，设计 5 年，至 2026 已 30 年，1 台已坏采购中，全部集中于 B2F 空调机房/游泳池隔壁/水泵房/分水器隔壁/员餐厨房侧）整体更新 + 管道阀门整体更换（锈蚀严重、关闭不畅、部分不能开关）+ 排污管内壁锈蚀 90% 段落更换 + 中水回用设备现为『无』"),
   ("储油与发电合规（新增）", 140, "★第二批次新增：原室内 0.8m³ 油箱、原储备油箱因市政安全管理要求已拆除 → 新建室外储油罐 + 输油泵 + 管道 + 消防与市政审批；蓄电池组 2 组（设计 3 年）更新"),
   ("给排水与水处理",      180,   "1996 生活给水热水管网 + 污排水 + 二次供水 + B2 输油管更换"),
   ("隐蔽工程（竖井局部）", 320,   "1996 各系统同竖井叠加 → 分层重排（局部）"),
   ("公区必要整改",        260,   "大堂地面渗漏 + 宴会厅 6F 地面墙毯 + 员工区/后勤区域"),
   ("康体与水疗",          0,     "皇冠 3.0 不含康体 → 规划缺项；但第二批次评估报告显示 B1F 已有水疗中心、B2F 有泳池与健身 → 属升级改造而非从零新增"),
   ("景观庭院与市政界面",  80,    "人行道/外围走道 + 前后庭院"),
   ("节能与绿色化",        190,   "围护保温 + 照明设备节能 + 可申报设备更新补助 ≤300 万 + 金树叶绿色饭店 15 万"),
   ("品牌专项（VI/客用品/钥匙卡/PIP 销项）", 420, "IHG Connect + 环保钥匙卡 + 枕套/被子印花 + 客用壶 + 环保客用品 + 楼顶 LOGO + VI 替换 + 三年 PIP 遗留项销项"),
   ("艺术品与在地策展",    0,     "皇冠 3.0 无强制"),
   ("开业前费用",          0,     "不换牌"),
   ("不可预见费",          185,   "3.9%"),
 ]),
 "D2": dict(name="方向二 · 洲至奢选 + 3 改 2 至 268 间（套内 40 ㎡+）", items=[
   ("客房改造",            3800,  "268 间 × 14.2 万（硬装+FF&E）｜第七部分口径一致；含移卫与管线重排"),
   ("消防系统",            1180,  "同上"),
   ("强弱电与智能化",      760,   "IB + 客控（中控）+ 门锁 + 安防 + 数字化监控 + IHG Connect"),
   ("机电（冷源/末端/配电/垂直交通）", 1900, "同上"),
   ("给排水隐蔽与末端（新增）", 260, "同上"),
   ("储油与发电合规（新增）", 140, "同上"),
   ("给排水与水处理",      180,   "同上"),
   ("隐蔽工程（竖井重排 + 移卫耦合）", 860, "竖井分层重排 + 移卫水平管线 + 隔墙 + 防水 + 垂直运输通道"),
   ("公区改造",            1480,  "大堂 5,468㎡ 品牌社交客厅 + 咖啡厅 + ADD 扩容 80–135 席 + 宴会 600/350㎡ + 14 会议室 + 行政酒廊 21F；★利用既有 B1F 水疗中心与 B2F 泳池健身、4F 办公层、1F 空置租赁餐饮"),
   ("康养 SPA 与泳池迁址",  620,   "负 B2 泳池迁 4F/屋顶（消除政府整改硬伤）+ 特色餐饮 1 处 + 康体水疗体系"),
   ("景观庭院与市政界面",  180,   "前后庭院市政界面 + 屋顶花园（4F 与屋顶 L 型连通）"),
   ("节能与绿色化",        190,   "同上"),
   ("品牌专项（VI 全套）",  420,   "洲际 VI 替换：导视牌 + 印刷品 + 客用品外观 + 员工着装 + 楼顶标识（『总府』名称可保留）"),
   ("艺术品与在地策展",    380,   "在地文化『一店一策』：空间/服务/产品三处落地 + 房型按年代命名"),
   ("开业前费用",          240,   "HMA 标准：pre-opening 费（特许口径按专项服务费计）"),
   ("不可预见费",          525,   "5.0%"),
 ]),
 "D3": dict(name="方向三 · 外部奢华品牌 + 3 改 2 + 奢牌级全改 + 旗舰 SPA + 艺术策展", items=[
   ("客房改造",            10720, "268 间 × 40 万（奢牌级：结构/移卫/全卫/进口石材与手工木饰面/收藏级陈设/套房比例提升）｜第七部分口径一致"),
   ("消防系统",            1180,  "同上"),
   ("强弱电与智能化",      860,   "同上 + 外部品牌系统对接"),
   ("机电（冷源/末端/配电/垂直交通）", 1900, "同上"),
   ("给排水隐蔽与末端（新增）", 260, "同上"),
   ("储油与发电合规（新增）", 140, "同上"),
   ("给排水与水处理",      180,   "同上"),
   ("隐蔽工程（竖井重排 + 移卫耦合）", 860, "同上"),
   ("公区改造",            2250,  "奢牌级公区 + 品牌故事线空间 + 旗舰级入口"),
   ("康养 SPA 与旗舰泳池", 1450,  "旗舰级水疗 + 屋顶泳池 + 特色餐饮 2 处"),
   ("景观庭院与市政界面",  260,   "奢牌级景观"),
   ("节能与绿色化",        190,   "同上"),
   ("品牌专项（外部奢牌 VI + 品牌方条件）", 780, "外部品牌 VI 全套 + 品牌方认可供应商 + FLS 专项 + 指定品牌名录"),
   ("艺术品与在地策展",    1250,  "艺术策展级投入"),
   ("开业前费用",          320,   "HMA pre-opening（基础费年值 × 约 6 个月）"),
   ("不可预见费",          1675,  "8.0%"),
 ]),
}

# 4. 方向运行参数
# ══════════════════════════════════════════════════════════════════
DIRECTIONS = {
 "D1": dict(
   label="方向一 · 沿用皇冠（仅机电安全与品牌达标）",
   tier="intl_current_crowne", rooms=402, rooms_sellable=402,
   adr=460.0, occ=0.700, tier_tag="皇冠 3.0 / Upscale（竞争组实测锚定）",
   fees=dict(base=0.020, base_on="revenue", incentive=0.060, incentive_on="gop",
             marketing=0.030, marketing_on="room_rev", loyalty=0.020, loyalty_on="room_rev",
             reservation=0.000, it_fee_wan=0.0, training_wan=0.0,
             ffe_reserve=0.020, ffe_on="revenue", preopening_months=0.0,
             room_rev_fee=0.000, reimbursable_pct=0.0),
   closure_months=14, closure_start_month=12, closure_plan="full",
   phase2_rooms=0,
   capex="D1",
 ),
 "D2": dict(
   label="方向二 · 洲至奢选（3 改 2 至 268 间）",
   tier="intl_upper_upscale", rooms=268, rooms_sellable=268,
   adr=950.0, occ=0.700, tier_tag="洲至奢选 / Upper Upscale（无本地实证·备选）",
   fees=dict(base=0.000, base_on="revenue", incentive=0.000, incentive_on="gop",
             marketing=0.020, marketing_on="room_rev", loyalty=0.020, loyalty_on="room_rev",
             reservation=0.005, it_fee_wan=100.0, training_wan=40.0,
             ffe_reserve=0.030, ffe_on="revenue", preopening_months=6.0,
             room_rev_fee=0.050, reimbursable_pct=0.0),
   closure_months=18, closure_start_month=12, closure_plan="full",
   phase2_rooms=0,
   capex="D2",
 ),
 "D3": dict(
   label="方向三 · 外部奢华品牌（3 改 2 + 奢牌级全改）",
   tier="intl_luxury", rooms=268, rooms_sellable=268,
   adr=1280.0, occ=0.700, tier_tag="外部奢华品牌 / Luxury",
   fees=dict(base=0.030, base_on="revenue", incentive=0.100, incentive_on="gop",
             marketing=0.025, marketing_on="room_rev", loyalty=0.020, loyalty_on="room_rev",
             reservation=0.015, it_fee_wan=250.0, training_wan=80.0,
             ffe_reserve=0.040, ffe_on="revenue", preopening_months=6.0,
             room_rev_fee=0.000, reimbursable_pct=0.0),
   closure_months=20, closure_start_month=12, closure_plan="full",
   phase2_rooms=0,
   capex="D3",
 ),
}

SCEN = {
 "保守": dict(adr=0.88, occ=0.92, fnb=0.85, gop=0.92),
 "中性": dict(adr=1.00, occ=1.00, fnb=1.00, gop=1.00),
 "乐观": dict(adr=1.10, occ=1.05, fnb=1.12, gop=1.06),
}

# 国资口径校验阈值（参数化，供讨论）
GOV = dict(irr_floor=0.08, payback_max_years=15, gearing_max=0.70,
           discount_rate=0.08, tax_rate=0.25, eval_years=23)

RAMP = {
 "adr":  [0.95, 1.00, 1.00, 1.00, 1.00] + [round(0.98 - 0.008*i, 4) for i in range(25)],
 "occ":  [0.90, 1.00, 1.00, 1.00, 1.00] + [round(0.98 - 0.008*i, 4) for i in range(25)],
}

# ══════════════════════════════════════════════════════════════════
# 5. 停业期损失（按实测逐月曲线）
# ══════════════════════════════════════════════════════════════════
def closure_loss(start_month, months, fixed_monthly_wan=284.0, brand_retention_wan=0.0):
    """返回逐月明细与合计（万元）。收入损失用实测历月营收；固定成本照提；品牌保留费另计。"""
    rows = []
    tot = 0.0
    for k in range(months):
        m = ((start_month - 1 + k) % 12) + 1
        rev = SE["season"][m]["rev"] / 1e4
        loss = rev + fixed_monthly_wan + brand_retention_wan
        tot += loss
        rows.append(dict(month=m, rev_lost=round(rev, 1), fixed=fixed_monthly_wan,
                         brand=brand_retention_wan, loss=round(loss, 1)))
    return rows, round(tot, 1)

def closure_matrix(months_range=range(14, 23), fixed_monthly_wan=284.0):
    out = {}
    for start in range(1, 13):
        for dm in months_range:
            _, t = closure_loss(start, dm, fixed_monthly_wan)
            out[(start, dm)] = t
    return out

# ══════════════════════════════════════════════════════════════════
# 6. 收入模型（USALI 部门制 · 月度）
# ══════════════════════════════════════════════════════════════════
def monthly_revenue(dk, scen, year, months_in_service, ramp_y):
    """返回该年 12 个月的部门收入（万元）"""
    tier = TIER[dk["tier"]]
    s = SCEN[scen]
    season = SE["season"]
    base_mix = tier["mix"]
    use_measured_fnb = (dk["tier"] == "intl_current_crowne")
    rows = []
    for m in range(1, 13):
        sm = season[m]
        if months_in_service <= 0:
            rows.append(dict(month=m, adr=0, occ=0, rooms_rev=0, fnb=0, banq=0,
                             other=0, misc=0, total=0, rooms_sold=0))
            continue
        adr = dk["adr"] * s["adr"] * RAMP["adr"][ramp_y] * sm["adr_idx"]
        occ = dk["occ"] * s["occ"] * RAMP["occ"][ramp_y] * sm["occ_idx"]
        days = 30.4
        rooms_sold = adr and (dk["rooms_sellable"] * occ * days)
        rooms_rev = adr * rooms_sold / 1e4
        if use_measured_fnb:
            fnb_ratio = sm["fnb_ratio"] * s["fnb"]
            banq_ratio = sm["banq_ratio"] * (2 - s["fnb"])
            other_ratio = base_mix["other"]
            misc_ratio = base_mix["misc"]
        else:
            fnb_ratio = base_mix["fnb"] * sm["fnb_idx"] * s["fnb"]
            banq_ratio = base_mix["banq"] * sm["banq_idx"]
            other_ratio = base_mix["other"]
            misc_ratio = base_mix["misc"]
        scale = rooms_rev / base_mix["rooms"] if base_mix["rooms"] > 0 else 0
        fnb = scale * fnb_ratio
        banq = scale * banq_ratio
        other = scale * other_ratio
        misc = scale * misc_ratio
        total = rooms_rev + fnb + banq + other + misc
        rows.append(dict(month=m, adr=round(adr, 1), occ=round(occ, 4),
                         rooms_sold=round(rooms_sold, 1), rooms_rev=round(rooms_rev, 1),
                         fnb=round(fnb, 1), banq=round(banq, 1), other=round(other, 1),
                         misc=round(misc, 1), total=round(total, 1)))
    return rows

def year_revenue(dk, scen, year, months_in_service, ramp_y):
    mr = monthly_revenue(dk, scen, year, months_in_service, ramp_y)
    tot = {k: round(sum(r[k] for r in mr), 1) for k in
           ("rooms_rev", "fnb", "banq", "other", "misc", "total")}
    tot["rooms_sold"] = round(sum(r["rooms_sold"] for r in mr), 0)
    return tot, mr

# ══════════════════════════════════════════════════════════════════
# 7. 费用与 GOP
# ══════════════════════════════════════════════════════════════════
def brand_fees(dk, rev):
    f = dk["fees"]
    def pct(val, basis):
        if basis == "revenue": return rev["total"] * val
        if basis == "room_rev": return rev["rooms_rev"] * val
        return 0.0
    base = pct(f["base"], f["base_on"])
    marketing = pct(f["marketing"], f["marketing_on"])
    loyalty = pct(f["loyalty"], f["loyalty_on"])
    reservation = pct(f["reservation"], "room_rev")
    room_fee = pct(f["room_rev_fee"], "room_rev")
    ffe = pct(f["ffe_reserve"], f["ffe_on"])
    it = f["it_fee_wan"]
    training = f["training_wan"]
    fixed = it + training
    return dict(base=base, marketing=marketing, loyalty=loyalty, reservation=reservation,
                room_rev_fee=room_fee, ffe_reserve=ffe, it=it, training=training,
                fixed=fixed, incentive=0.0, incentive_rate=f["incentive"])

def dept_gop(dk, rev, scen):
    tier = TIER[dk["tier"]]
    g = tier["dept_gop"]
    s = SCEN[scen]
    rooms_gop = rev["rooms_rev"] * g["rooms"] * s["gop"]
    fnb_gop = rev["fnb"] * g["fnb"] * s["gop"]
    banq_gop = rev["banq"] * g["banq"] * s["gop"]
    other_gop = rev["other"] * g["other"] * s["gop"]
    misc_gop = rev["misc"] * g["misc"] * s["gop"]
    gop = rooms_gop + fnb_gop + banq_gop + other_gop + misc_gop
    return dict(rooms=rooms_gop, fnb=fnb_gop, banq=banq_gop, other=other_gop, misc=misc_gop,
                total=gop, rate=(gop / rev["total"] if rev["total"] else 0))

# ══════════════════════════════════════════════════════════════════
# 8. 现金流 / IRR / NPV
# ══════════════════════════════════════════════════════════════════
def npv(rate, cfs):
    return sum(cf / (1 + rate) ** i for i, cf in enumerate(cfs))

def irr(cfs, lo=-0.95, hi=10.0, tol=1e-7):
    def f(r):
        return npv(r, cfs)
    try:
        if f(lo) * f(hi) > 0:
            return None
        for _ in range(200):
            mid = (lo + hi) / 2
            if f(lo) * f(mid) <= 0:
                hi = mid
            else:
                lo = mid
            if hi - lo < tol:
                break
        return (lo + hi) / 2
    except Exception:
        return None

def payback(cfs):
    cum = 0
    for i, cf in enumerate(cfs):
        prev = cum
        cum += cf
        if prev < 0 <= cum and cf != 0:
            return i + abs(prev / cf)
    return None

# ══════════════════════════════════════════════════════════════════
# 9. 主测算
# ══════════════════════════════════════════════════════════════════
def capex_total(key):
    return sum(x[1] for x in CAPEX[key]["items"])

def run_direction(dk_key, scen="中性", horizon=20, fixed_monthly=231.4,
                  closure_months=None, closure_start=None, phased=False):
    dk = dict(DIRECTIONS[dk_key])
    if closure_months is not None:
        dk["closure_months"] = closure_months
    if closure_start is not None:
        dk["closure_start_month"] = closure_start
    cm = dk["closure_months"]
    cs = dk["closure_start_month"]
    capex = capex_total(dk["capex"])
    # 停业期品牌保留费：基础费年值的 35%（HMA 下营收为 0 则基础费为 0，但品牌方保留团队/质量职能）
    base_annual_est = capex * 0  # placeholder
    rev_y1 = None
    # 预估稳定年营收以估基础费
    _, r_est = year_revenue(dk, scen, 2, 12, 1)
    brand_ret = r_est["total"] * dk["fees"]["base"] * 0.35 / 12.0
    cl_rows, cl_total = closure_loss(cs, cm, fixed_monthly, brand_ret)
    # 年表
    rows = []
    cum_fc = 0.0
    for y in range(1, horizon + 1):
        # 停业期占用的月份放在第一年
        mis = 0
        if y == 1:
            mis = max(0, 12 - cm)
        ramp_y = min(y - 1, len(RAMP["adr"]) - 1)
        rev, mr = year_revenue(dk, scen, y, 12 - mis, ramp_y)
        bf = brand_fees(dk, rev)
        gf = dept_gop(dk, rev, scen)
        incentive = gf["total"] * dk["fees"]["incentive"]
        owner_gop = gf["total"] - bf["base"] - bf["marketing"] - bf["loyalty"] \
                    - bf["reservation"] - bf["room_rev_fee"] - bf["ffe_reserve"] \
                    - bf["fixed"] - incentive
        # 业主现金流
        capex_y = -capex if y == 1 else 0.0
        closure_y = -cl_total if y == 1 else 0.0
        cf = owner_gop - capex_y + closure_y
        # 过渡期折损
        trans = 0.0
        if y <= 2:
            trans = -rev["total"] * 0.10
            cf += trans
        rows.append(dict(year=y, revenue=rev["total"], rooms_rev=rev["rooms_rev"],
                         fnb=rev["fnb"], banq=rev["banq"], other=rev["other"], misc=rev["misc"],
                         rooms_sold=rev["rooms_sold"],
                         gop=gf["total"], gop_rate=gf["rate"],
                         fee_base=bf["base"], fee_marketing=bf["marketing"],
                         fee_loyalty=bf["loyalty"], fee_reservation=bf["reservation"],
                         fee_room_rev=bf["room_rev_fee"], fee_ffe=bf["ffe_reserve"],
                         fee_fixed=bf["fixed"], fee_incentive=incentive,
                         brand_fee_total=bf["base"]+bf["marketing"]+bf["loyalty"]+
                                         bf["reservation"]+bf["room_rev_fee"]+
                                         bf["ffe_reserve"]+bf["fixed"]+incentive,
                         owner_gop=owner_gop, capex=capex_y, closure=closure_y,
                         transition=trans, cashflow=cf, monthly=mr))
        cum_fc += cf
    cfs = [r["cashflow"] for r in rows]
    r = irr(cfs)
    return dict(direction=dk_key, label=dk["label"], scenario=scen, horizon=horizon,
                capex=capex, closure_months=cm, closure_start=cs,
                closure_rows=cl_rows, closure_total=cl_total,
                brand_retention_monthly=round(brand_ret, 1),
                yearly=rows, cfs=cfs,
                irr=r, npv=round(npv(GOV["discount_rate"], cfs), 1),
                payback=payback(cfs),
                owner_gop_y5=round(sum(x["owner_gop"] for x in rows[2:5])/3, 1),
                revenue_y5=round(sum(x["revenue"] for x in rows[2:5])/3, 1))

if __name__ == "__main__":
    print("=== v6 引擎自检 ===")
    print("季节性均值 ADR %.1f OCC %.1f%% 月均营收 %.1f 万" %
          (SE["avg_adr"], SE["avg_occ"]*100, SE["avg_rev"]/1e4))
    for k in ("D1","D2","D3"):
        print("CAPEX %s = %d 万" % (k, capex_total(k)))
    for k in ("D1","D2","D3"):
        r = run_direction(k, "中性", 20)
        print("%s 20y 中性: 营收Y5 %s | GOP率 %.1f%% | 业主GOP %s | IRR %s | NPV %s | 回收 %s" %
              (k, r["revenue_y5"], r["yearly"][4]["gop_rate"]*100, r["owner_gop_y5"],
               ("%.2f%%" % (r["irr"]*100)) if r["irr"] else "None",
               r["npv"], ("%.1f" % r["payback"]) if r["payback"] else "None"))
