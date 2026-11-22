# -*- coding: utf-8 -*-
"""
v98 最终测算模型 —— 总府皇冠假日酒店改造项目三路径 + 第四条参考路径
产业发展部｜2026-11-15
单一数据源；整合 A1（市场定位）/ A2（合规工程）/ A3（经营财务）/ A4（品牌合同）四份底稿

【口径体系（A3 已与台账、P&L 逐项对账验证）】
  口径B（利润表·不含服务费）：TOTAL REVENUE − 部门直接成本 = GOP
                              GOP − 未分摊(A&G+POM+IT&S&M+Energy) = 洲际 GOP
                              洲际 GOP − 许可费 − 奖励管理费 − 非经营性(利息) = 净营业利润
  口径A（业主台账·含服务费）＝ 口径B + 服务费；服务费 ≈ 口径B客房 × 10.06%
  验证：5,065.06 + 338.47 = 5,403.53 ✓ ／ 3,177.15 − 1,681.96 = 1,495.19 ✓

【评价口径】
  项目口径 NPV / IRR / 静态回收期（不含存量债务利息——存量债务 60,677 万元为各路径共同项，另列集团口径）
  评价期 20 年（基准），折现率 8%；敏感性另给 30 年、±2pp、ADR ±10%、OCC ±5pp、CAPEX ±15%、房量、费率
"""
import json, os, io

T = r"D:\B166ER-openclaw\workspace\.tmp"
LOG = open(os.path.join(T, "v98.log"), "w", encoding="utf-8")
def L(*a):
    LOG.write(" ".join(str(z) for z in a) + "\n"); LOG.flush()

# ============================================================
# 一、基线与基准（全部可溯源）
# ============================================================
BASE = {
    "rev_A_fy2025": 7099.54, "rev_A_ttm": 6442.73, "rev_A_2026_10m": 5403.53,
    "rev_A_yoy_2026_10m": -0.1173,
    "room_A_fy2025": 4740.4, "room_A_ttm": 4387.7,
    "nonroom_A_fy2025": 2359.1, "nonroom_A_ttm": 2055.0,
    "mix_A_ttm": {"客房": 0.6810, "餐饮": 0.1400, "会议": 0.1280, "其它": 0.0510},
    "rev_B_10m": 5065.06, "svc_10m": 338.47, "gop_10m": 3177.15,
    "ihg_gop_10m": 1495.20, "adj_gop_10m": 1393.90, "license_10m": 101.30,
    "imf_10m": 69.69, "nonop_10m": 1740.71, "netop_10m": -416.51,
    "cost_10m": {"人工": 1820.08, "能源": 437.70, "POM": 228.63, "A&G": 578.18,
                 "S&M": 347.97, "IT": 89.48},
    "dept_margin": {"房务部": 0.7724, "餐饮部": 0.2907, "其他营运": 0.0752, "Misc": 1.0000},
    "rooms": 402, "room_nights_year": 146730, "suite_area_total": 10192.0,
    "suite_area_per_room": 25.35,
    "occ_ttm": 0.7253, "adr_A_ttm": 412.09, "revpar_ttm": 298.70,
    "occ_24m": 0.7255, "adr_A_24m": 427.42, "revpar_24m": 310.07,
    "room_B_fy2025": 4309.5, "svc_pct_of_room_B": 0.1006, "rev_B_fy2025": 6666.0,
    "nonroom_B_fy2025": 2356.5, "nonroom_margin_blend": 0.3404, "annualize_10m": 1.2,
    "interest_annual": 2088.85, "depreciation_fy2025": 387.0,
    "license_pct_rev_B": 0.02, "imf_pct": 0.05,
    "shutdown_labor_monthly": 109.34, "shutdown_staff": 52, "total_staff": 218,
    "valuation_total": 69923.42, "valuation_net": 60914.78, "valuation_date": "2025-09-04",
    "book_net": 14382.0, "debt": 60677.0, "mortgage": 20000.0,
    "audit_2026": {"brand_standard": 0.603, "brand_safety": 0.737, "fail_items": 80, "fail_pct": 0.717},
    "src": "业主两批资料（业主资料(2)、近24个月经营指标、2026年10月利润表37表、客源结构与客户反馈、"
           "人力数据统计、F2-29、专项限制条件、关于能否消防分批验收的回复）；川同力达成房预估函（2025）第0915号；"
           "业主方 STR 竞对原件；总府实业〔2024〕11号专题报告；2019 洲际总部 PIP",
}
BENCH = {
    # ★★ 重大修正（2026-11-15，Eric 指出）：业主方 STR 竞争组四家成员
    #    Galaxy Minyoun / Somerset Riverview / Minyoun Dongda / Shimao Yuluxe
    #    —— 无一家为国际联号酒店，却与洲际体系酒店做 RGI 对标。
    #    因此该组【不能作为市场定位与定价依据】，仅可作业主内部收益管理对标工具。
    #    下述 comp_*/rgi 数值仅用于运营对标叙述，不得用于定位判定、不得进入收入测算。
    "str_comp_status": "★ 仅作运营对标工具，不作市场定位依据（四成员无一家国际联号）",
    "str_comp_members": ["Galaxy Minyoun Chengdu Hotel（Minyoun，359 间）",
                         "Somerset Riverview Chengdu（Somerset，200 间）",
                         "Minyoun Chengdu Dongda Hotel（Minyoun，333 间）",
                         "Shimao Yuluxe Hotel Chengdu（Yuluxe，286 间）"],
    "comp_adr": 416.29, "comp_occ": 0.6637, "comp_revpar": 276.71, "rgi": 107.90,
    "comp_adr_yoy_3m": -0.0414, "comp_revpar_yoy_3m": -0.0420,
    "comp_adr_yoy_12m": -0.1056, "comp_revpar_yoy_12m": -0.1146,
    "tf_vs_comp": {"adr": 0.990, "revpar": 1.079, "rgi_delta": 7.90},
    "tf_vs_comp_caveat": "★ 该对照基于非联号竞对组，仅说明总府在本地同档次运营表现不弱；"
                         "不得据此得出「定价不失位」结论。同级别国际联号对标另见 A5 竞对组",
    "ihg_chain_anchor": {"成都天府皇冠假日（邻环球中心/世纪城，Agoda常规101-150美元）": 905, "成都世纪城天堂洲际大饭店": 800, "成都西区皇冠假日（347间/2018装修）": 692, "成都温江皇冠假日（458间/2016装修）": 607, "成都新希望高新皇冠假日（347间/2018装修）": 293,
                         "note": "★ 联网核实 2026-11-15：洲际体系在成都五家可核验实体价格阶梯；总府 Agoda 常规区间 51-75 美元（约370-540元）、位置分 9.4 为六项最高、客房质素及舒适度 7.7 为六项最低。路径一基准 ADR 620 取西区 692 与温江 607 之间，位置分显著优于两者"},
    "unsourced_1280": {"adr": 1280, "occ": 0.763, "revpar": 977,
        "verdict": "★ 无法溯源·合成数·不得使用（与业主 STR 原件 ADR 差 3.07 倍、RevPAR 差 3.53 倍）；"
                   "「成都高于全国 37%」随之失效"},
    "high_end_capacity_900plus": 989,
    "high_end_note": "春熙路核心圈 900 元以上高价段实测总供给仅 989 间（洲至奢选 335＋尼依格罗 230＋瑞吉 282＋居舍 142）",
}
ENGINEERING = {
    "partition_fire": "★ 不可行。消防泵房（B2F 单一）、消防控制室（B1F 单一联动主机）、消防水源"
                      "（B2 水池约 1,100 ㎡＋屋面水箱约 230 ㎡）、防排烟、竖向管网均为全楼单一系统，"
                      "不满足保卫部《回复》四项条件中的「独立性」要求；防火分隔本身失功能（井道门未锁、"
                      "门选器失灵，IHG 审计定级 Critical）；疏散楼梯净宽仅 1.09 m 且无完整核算书。",
    "partition_solution": "分期施工、整体验收、分期开业；验收与开业必须整体",
    "contract_710": "合同附件 A 第 7.10 条：酒店翻新改造期间照常营业区域的所有消防人身安全系统务必能正常使用"
                    " → 「分期改造不停业」与消防整改在合同层面互斥",
    "fire_acceptance_1998": "1998-08-07 成都市公安局《建筑工程消防验收意见书》合格，但载明「建筑如有改建、"
                             "内部装修、用途变更等，应向原审核机构申报重新审核」；业主资料中无任何改造后重新审核文件",
    "dur": {"P1": "6—9 个月（全停；分区滚动不可行）", "P2": "18—24 个月 ＋ 开业准备 3—6 个月",
            "P3": "24—36 个月", "P4": "含品牌体系搭建期，长于 P3"},
    "rooms_by_brand": {"皇冠 2026 标准 ≥35 ㎡": 291, "洲至奢选 洲际方条件 ≥40 ㎡": 254,
                       "洲至奢选 实测基础房 45 ㎡": 226, "康莱德 46 ㎡": 205,
                       "尼依格罗 50 ㎡": 188, "丽晶/LXR 60 ㎡": 157, "瑞吉 65 ㎡": 145},
    "coupling_note": "上表为无耦合折损的理论上限（10,192 ÷ 面积要求）；实操按 1.08 移卫耦合折损再降，"
                     "如洲至奢选 45 ㎡ 口径为 226 间（理论）／209 间（实操）",
}
CONTRACT = {
    "term": "2019-09-28 至 2029-09-27；到期不续、不自动续约（第 2.3 条）",
    "p6": "第 2.1 条：业主须 2020-09-27 启动 PIP、2021-09-27 完成并经管理人验收，否则管理人有权"
          "「单方提前解除…无需承担任何违约责任」。事实：PIP 自 2011 年挂账，2024/2025/2026 三次审计各列"
          "1 条「未执行 PIP 计划」，2026 年总体评级 Fail（80 项，71.7%）",
    "funding": "第 1(c) 条：业主应提供酒店改造所需全部资金 → 改造资金 100% 业主承担",
    "system_fee": "第 6.3 条：系统费替换为科技服务费、营销及预订进款、频繁旅行进款等；F2-29 明确各项基金收费一致"
                  " → 不可把系统费当作换牌节约",
    "audit_fee": "P9：审计费归业主承担，合同无封顶；P11—P12：激励费分档；P14：替代系统费",
    "data": "附件 E 1.4：IHG、业主及各自关联公司在协议终止后均可免费继续使用源自 PMS 的客户数据",
    "brand_standard_room": "2026 皇冠建造设计标准：标准客房净面积 ≥35 ㎡、净宽 ≥3.9 m（标准号 [958140]/[958148]）"
                            " → 现状 25.35 ㎡/间不达标",
    "unread": ["押金/保证金条款", "审计费上限", "业主方提前解约违约金（均应在未提供的 1996 年原管理合同中）"],
}
CAPEX_ANCHOR = {"2024报告_预计工程费总投资": 18000.0,
                "2024报告_三分项": {"建筑安装工程费": 3456.08, "基础设施配套工程费": 1383.08,
                                    "设备购置及安装工程费": 1556.56},
                "2019PIP_初步造价区间": [18000.0, 20000.0], "IHG技术支持费": 100.0,
                "status": "★ 产业发展部测算，待第三方工程量清单核定后定稿"}

# ============================================================
# 二、路径定义
# ============================================================
PATHS = {
"P1": {"name": "路径一 · 底线整改（局部改造，维持洲际皇冠假日与 402 间）",
    "tier": "A 高端全服务五星", "rooms": 402,
    "brand": "维持洲际皇冠假日委托管理（合同至 2029-09-27，到期不续约）",
    "adr_excl_svc": 620.0, "adr_lo": 600.0, "adr_hi": 760.0,
    "occ": 0.7175, "occ_lo": 0.700, "occ_hi": 0.760,
    "downtime": 8, "downtime_lo": 6, "downtime_hi": 9, "nonroom_capability": 1.00,
    "adr_basis": "★ 同属洲际体系在成都的皇冠假日实证展示价（环球中心 757／世纪城 697）＋协议价体系（370-500）"
                 "锁定上限 600-760；不依赖业主 STR 竞对组；不得按 880 元以上立项",
    "adr_basis_note": "★ 取 A1 推导区间 6,339—8,029 万元客房收入的中值偏低位（ADR 620×OCC 71.75%），"
                       "刻意保守；ADR×OCC=444.9 元/间夜，位于 A1 区间下四分位",
    "fee_mode": "delegate",
    "capex_split": {
        "火灾自动报警系统整体更新（主机＋前端＋线路）": 900.0,
        "消防泵房与管网（喷淋 2 台／消火栓 2 台／竖向分区管网）": 1250.0,
        "应急照明与疏散指示系统整体更新": 380.0,
        "防火门与井道门修复补齐": 220.0,
        "给排水冷水管网分区更新与阀门更换": 1450.0,
        "冷源更换（4 台 R11 淘汰冷媒机组＋辅机）": 2100.0,
        "风系统与末端（AHU 11＋新风 20＋FCU 542）": 1450.0,
        "配电更新（干变 4 台／低压柜 34 面／高压柜）": 1150.0,
        "电梯 14 台更新与特种设备检验": 380.0,
        "锅炉 4 台及配套更新": 520.0,
        "消防报建与重新审核（1998 意见书要求）": 260.0,
        "基本预备费（8%）": 1006.0},
    "key_risk": "2026 皇冠标准要求客房净面积 ≥35 ㎡、净宽 ≥3.9 m，现状 25.35 ㎡ 不达标 → "
                "维持 402 间即持续不符合品牌标准；叠加 PIP 6.10 条未执行，洲际方依 P6 有单方解除权",
    "recommend": None},
"P2": {"name": "路径二 · 整体改造（洲际体系内换牌洲至奢选，209 间）",
    "tier": "B UPPER SCALE", "rooms": 209,
    "brand": "洲至奢选（特许管理，客房收入 5%，取消激励管理费）；洲际方已书面记录可换牌并可申请豁免提前终止违约金",
    "adr_excl_svc": 950.0, "adr_lo": 900.0, "adr_hi": 1000.0,
    "occ": 0.690, "occ_lo": 0.640, "occ_hi": 0.740,
    "downtime": 26, "downtime_lo": 21, "downtime_hi": 30, "nonroom_capability": 1.05,
    "adr_basis": "本地实测洲至奢选 900-1,500 元；同档次实证保守取 900-1,000；"
                 "209 间对应 RevPAR 须≥597 元方能守住现状客房收入 4,740 万元",
    "fee_mode": "franchise_ihg",
    "capex_split": {
        "客房重做 209 间（含卫浴，套内 45 ㎡）": 4180.0,
        "机电及隐蔽工程（冷源／风系统／末端／竖井）": 4600.0,
        "公区改造（全日餐厅扩容／大堂社交酒吧／宴会强化／行政酒廊）": 3100.0,
        "后场与工区": 1300.0,
        "消防系统整体更新": 2530.0,
        "给排水管网整体更换": 1450.0,
        "智能化与客控": 900.0,
        "VI 全面更换（导视／印刷品／客用品／工装）": 380.0,
        "电梯与特种设备": 380.0,
        "消防报建与 1998 意见书重新审核": 320.0,
        "基本预备费（8%）": 1914.0},
    "key_risk": "洲际方现有载体为沟通纪要（非正式函件）；违约金「可以申请豁免」非已豁免；"
                "40 ㎡ 面积条件、书面费率表、VI 全换清单与费用承担均须书面确认（7 项）",
    "recommend": None},
"P3": {"name": "路径三 · 整体改造（对外引入品牌／合作伙伴，205 间）",
    "tier": "A/B 之间（按 UPPER SCALE 档落地，不得按顶奢立项）", "rooms": 205,
    "brand": "外部品牌待定情景（康莱德／柏悦／Sofitel 等）；不得发函或承诺",
    "adr_excl_svc": 1180.0, "adr_lo": 1100.0, "adr_hi": 1290.0,
    "occ": 0.690, "occ_lo": 0.640, "occ_hi": 0.740,
    "downtime": 30, "downtime_lo": 27, "downtime_hi": 36, "nonroom_capability": 1.05,
    "adr_basis": "本地实测尼依格罗 1,180-1,400 元（下沿取值）；康莱德无成都实测面积与房价，为异地代理样本；"
                 "205 间对应 RevPAR 须≥634 元方能守住现状客房收入",
    "fee_mode": "franchise_ext",
    "capex_split": {
        "客房重做 205 间（含卫浴，套内 46 ㎡）": 4930.0,
        "机电及隐蔽工程": 4900.0,
        "公区改造": 3600.0,
        "后场与工区": 1400.0,
        "消防系统整体更新": 2530.0,
        "给排水管网整体更换": 1450.0,
        "智能化与客控": 1100.0,
        "VI 与品牌工程": 480.0,
        "电梯与特种设备": 380.0,
        "外部品牌 PIP 追加要求": 900.0,
        "消防报建与重新审核": 420.0,
        "基本预备费（8%）": 2029.0},
    "key_risk": "外部品牌在蓉空位基本不成立：文华东方（2022-10 签约中海 489m／267 间／2028）、"
                "丽晶（2026-07 签约新希望顺江路／约 180 间／2029Q3）、尼依格罗、瑞吉本地均已有门店；"
                "柏悦与 LXR 在成都仅见传闻，须品牌方官方确认；评估函载明土地共用宗「分割后不能独立使用」",
    "recommend": None},
"P4": {"name": "路径四 · 自创旗舰品牌（仅作参考，不主推）",
    "tier": "A/B 之间（自定标准）", "rooms": 209,
    "brand": "自创品牌（从零建立）",
    "adr_excl_svc": 900.0, "adr_lo": 800.0, "adr_hi": 1000.0,
    "occ": 0.660, "occ_lo": 0.600, "occ_hi": 0.720,
    "downtime": 30, "downtime_lo": 27, "downtime_hi": 36, "nonroom_capability": 1.00,
    "adr_basis": "自创品牌首 3—5 年无品牌溢价，须按同档次市场水平倒推，不得自定",
    "fee_mode": "selfbrand",
    "capex_split": {
        "客房重做 209 间（含卫浴）": 4400.0,
        "机电及隐蔽工程": 4800.0,
        "公区改造": 3400.0,
        "后场与工区": 1500.0,
        "消防系统整体更新": 2530.0,
        "给排水管网整体更换": 1450.0,
        "智能化与客控": 1000.0,
        "自创品牌体系（VI／物化 PIP／注册／培训／会员与分销）": 2600.0,
        "电梯与特种设备": 380.0,
        "消防报建与重新审核": 340.0,
        "基本预备费（8%）": 1940.0},
    "key_risk": "★ 结构性门槛而非投入产出比：安逸会会员 160 万 vs 万豪 1.5 亿＋／锦江约 2 亿／华住 2.7 亿（差 5—10 倍）；"
                "2030 中央预订率目标 35% vs 对标 50—70%；无跨集团会员互通、无海外会员；集团尚无已运营成功的自有高端样板店；"
                "且安逸集团品牌体系认知 v1.6（2026-09-11）已将「总府皇冠假日」归入"
                "「第二组·专业化合作型·国际品牌委托经营」，自有品牌旗舰型为四川宾馆／花园宾馆／国堰宾馆 —— 与集团已定型品牌架构直接冲突",
    "recommend": None},
}

# ============================================================
# 三、测算内核
# ============================================================
def npv(rate, cfs): return sum(cf / ((1 + rate) ** i) for i, cf in enumerate(cfs))
def irr(cfs, lo=-0.90, hi=2.0, tol=1e-9):
    try: f_lo, f_hi = npv(lo, cfs), npv(hi, cfs)
    except ZeroDivisionError: return None
    if f_lo * f_hi > 0: return None
    for _ in range(400):
        mid = (lo + hi) / 2
        try: f_mid = npv(mid, cfs)
        except ZeroDivisionError: return None
        if abs(f_mid) < tol: return mid
        if f_lo * f_mid <= 0: hi, f_hi = mid, f_mid
        else: lo, f_lo = mid, f_mid
    return (lo + hi) / 2
def payback(cfs):
    cum = 0.0
    for i, cf in enumerate(cfs):
        prev = cum; cum += cf
        if prev < 0 <= cum and cf != 0: return i - 1 + (-prev / cf)
    return None

def annual_op(p, adr=None, occ=None, nonroom_cap=None):
    adr = p["adr_excl_svc"] if adr is None else adr
    occ = p["occ"] if occ is None else occ
    nc = p["nonroom_capability"] if nonroom_cap is None else nonroom_cap
    rn = p["rooms"] * 365
    room_B = rn * occ * adr / 10000.0
    svc = room_B * BASE["svc_pct_of_room_B"]
    occ_ratio = occ / BASE["occ_ttm"]
    nonroom_B = BASE["nonroom_B_fy2025"] * (occ_ratio ** 0.8) * nc
    rev_B = room_B + nonroom_B
    gop = room_B * BASE["dept_margin"]["房务部"] + nonroom_B * BASE["nonroom_margin_blend"]
    scale_room = p["rooms"] / BASE["rooms"]
    ANN = BASE["annualize_10m"]
    undist = {
        "A&G（行政及总办）": BASE["cost_10m"]["A&G"] * ANN * (0.75 + 0.25 * scale_room),
        "POM（工程部维保）": BASE["cost_10m"]["POM"] * ANN * (0.70 + 0.30 * scale_room),
        "IT & Telecom": BASE["cost_10m"]["IT"] * ANN,
        "S&M（市场销售，含渠道佣金）": BASE["cost_10m"]["S&M"] * ANN * occ_ratio,
        "Energy（未分摊能源）": BASE["cost_10m"]["能源"] * ANN * (0.55 + 0.45 * scale_room),
    }
    undist_total = sum(undist.values())
    ihg_gop = gop - undist_total
    mode = p["fee_mode"]
    if mode == "delegate":
        license = rev_B * BASE["license_pct_rev_B"]
        imf = max(0.0, ihg_gop - license) * BASE["imf_pct"]
        fee_total = license + imf
    elif mode == "franchise_ihg":
        license = room_B * 0.05; imf = 0.0; fee_total = license
    elif mode == "franchise_ext":
        license = room_B * 0.05; imf = 0.0; fee_total = license
    else:
        license = 0.0; imf = 0.0
        fee_total = room_B * 0.03     # 自建品牌需自建预订与分销渠道成本
    adj_gop = ihg_gop - fee_total
    return {"room_B": room_B, "svc": svc, "room_A": room_B + svc, "nonroom_B": nonroom_B,
            "rev_B": rev_B, "rev_A": rev_B + svc, "gop": gop, "undist": undist,
            "undist_total": undist_total, "ihg_gop": ihg_gop, "license": license,
            "imf": imf, "fee_total": fee_total, "adj_gop": adj_gop, "adr": adr, "occ": occ}

def project_cf(p, capex, life=20, rate=0.08, ramp=6, sustain_pct=0.02,
               adr=None, occ=None, nonroom_cap=None, brand_share=0.0, subsidy=0.0,
               downtime=None, fee_mult=1.0):
    dt = p["downtime"] if downtime is None else downtime
    st = annual_op(p, adr, occ, nonroom_cap)
    owner_capex = capex * (1 - brand_share) - subsidy
    dt_monthly = (BASE["shutdown_labor_monthly"]
                  + BASE["cost_10m"]["POM"] / 10 * 0.6
                  + BASE["cost_10m"]["能源"] / 10 * 0.25)
    cfs = [-owner_capex]
    for _ in range(dt): cfs.append(-dt_monthly)
    for m in range(ramp):
        k = 0.45 + (0.85 - 0.45) * (m / max(1, ramp - 1))
        r = annual_op(p, adr, occ, nonroom_cap)
        rev_B = r["rev_B"] * k
        gop = r["gop"] * k
        undist = r["undist_total"] * (0.85 + 0.15 * k)
        ihg = gop - undist
        fee = r["fee_total"] * k * fee_mult
        adj = ihg - fee
        sustain = rev_B * sustain_pct / 12
        cfs.append(adj - sustain)
    for y in range(life):
        r = annual_op(p, adr, occ, nonroom_cap)
        sustain = r["rev_B"] * sustain_pct
        cfs.append(r["adj_gop"] * fee_mult - sustain)
    return {"npv": npv(rate, cfs), "irr": irr(cfs), "payback": payback(cfs),
            "owner_capex": owner_capex, "cfs": cfs, "shutdown_cf_total": -dt_monthly * dt,
            "stable": st, "dt_monthly": dt_monthly}

# ============================================================
# 四、跑数
# ============================================================
results = {}
for k, p in PATHS.items():
    capex = round(sum(p["capex_split"].values()), 2)
    p["capex"] = capex
    r = project_cf(p, capex)
    st = r["stable"]
    op_cf = st["adj_gop"] - st["rev_B"] * 0.02
    results[k] = {
        "name": p["name"], "tier": p["tier"], "rooms": p["rooms"], "downtime": p["downtime"],
        "capex": capex, "capex_split": p["capex_split"],
        "owner_capex": round(r["owner_capex"], 2),
        "adr": st["adr"], "occ": st["occ"],
        "room_rev_A": round(st["room_A"], 2), "nonroom_rev_B": round(st["nonroom_B"], 2),
        "rev_A_stable": round(st["rev_A"], 2), "rev_B_stable": round(st["rev_B"], 2),
        "vs_base_rev_A": round(st["rev_A"] - BASE["rev_A_fy2025"], 2),
        "revpar_A": round(st["room_A"] * 10000 / (p["rooms"] * 365), 2),
        "gop": round(st["gop"], 2), "undist": round(st["undist_total"], 2),
        "ihg_gop": round(st["ihg_gop"], 2), "fee_total": round(st["fee_total"], 2),
        "adj_gop": round(st["adj_gop"], 2), "op_cf_stable": round(op_cf, 2),
        "op_cf_margin": round(op_cf / st["rev_A"], 4),
        "shutdown_cf_total": round(r["shutdown_cf_total"], 2),
        "npv": round(r["npv"], 2),
        "irr_pct": (round(r["irr"] * 100, 2) if r["irr"] is not None else None),
        "payback_yr": (round(r["payback"], 2) if r["payback"] is not None else None),
        "undist_detail": {kk: round(vv, 2) for kk, vv in st["undist"].items()},
        "key_risk": p["key_risk"],
    }
    L("%s capex=%.0f 房量=%d 停业=%d月 达产营收A=%.0f RevPAR_A=%.0f 调整后GOP=%.0f 经营现金流=%.0f NPV=%.0f IRR=%s 回收=%s" % (
        k, capex, p["rooms"], p["downtime"], st["rev_A"], results[k]["revpar_A"],
        st["adj_gop"], op_cf, r["npv"], results[k]["irr_pct"], results[k]["payback_yr"]))

# ============================================================
# 五、盈亏平衡约束（守住现状口径A客房收入所需 RevPAR）
# ============================================================
be = {}
for k, p in PATHS.items():
    rn = p["rooms"] * 365
    req = BASE["room_A_fy2025"] * 10000 / rn
    assumed = results[k]["revpar_A"]
    be[k] = {"rooms": p["rooms"], "required_revpar": round(req, 0), "assumed_revpar": round(assumed, 0),
             "gap": round(assumed - req, 0), "pass": assumed >= req}
    L("盈亏平衡 %s: 需 RevPAR %.0f｜方案 %.0f｜差 %+.0f → %s" % (
        k, req, assumed, assumed - req, "通过" if assumed >= req else "不通过"))

# ============================================================
# 六、敏感性
# ============================================================
sens = {}
for k, p in PATHS.items():
    capex = p["capex"]; s = {}
    cases = [
        ("ADR -10%", dict(adr=p["adr_excl_svc"] * 0.9)),
        ("ADR 基准", dict()),
        ("ADR +10%", dict(adr=p["adr_excl_svc"] * 1.1)),
        ("OCC -5pp", dict(occ=p["occ"] - 0.05)),
        ("OCC 基准", dict()),
        ("OCC +5pp", dict(occ=p["occ"] + 0.05)),
        ("停业下限", dict(downtime=p["downtime_lo"])),
        ("停业基准", dict()),
        ("停业上限", dict(downtime=p["downtime_hi"])),
    ]
    for lbl, kw in cases:
        s[lbl] = round(project_cf(p, capex, **kw)["npv"], 0)
    for lbl, cp in (("CAPEX -15%", capex * 0.85), ("CAPEX 基准", capex), ("CAPEX +15%", capex * 1.15)):
        s[lbl] = round(project_cf(p, cp)["npv"], 0)
    for lbl, rt in (("折现率 6%", 0.06), ("折现率 8%", 0.08), ("折现率 10%", 0.10)):
        s[lbl] = round(project_cf(p, capex, rate=rt)["npv"], 0)
    for lbl, lf in (("评价期 10 年", 10), ("评价期 20 年", 20), ("评价期 30 年", 30)):
        s[lbl] = round(project_cf(p, capex, life=lf)["npv"], 0)
    for lbl, bs in (("品牌方承担 0%", 0.0), ("品牌方承担 20%", 0.20), ("品牌方承担 30%", 0.30)):
        s[lbl] = round(project_cf(p, capex, brand_share=bs)["npv"], 0)
    s["房价不提升（ADR维持现状）"] = round(
        project_cf(p, capex, adr=BASE["adr_A_24m"] / (1 + BASE["svc_pct_of_room_B"]),
                   occ=BASE["occ_24m"])["npv"], 0)
    if k in ("P2", "P3"):
        rm_key = next((kk for kk in p["capex_split"] if kk.startswith("客房重做")), None)
        rm_rate = p["capex_split"].get(rm_key, 0)
        for nr in (round(p["rooms"] * 0.8), p["rooms"], round(p["rooms"] * 1.2)):
            p2 = dict(p); p2["rooms"] = nr
            cap2 = capex - rm_rate + rm_rate / p["rooms"] * nr
            s["房量 %d 间" % nr] = round(project_cf(p2, cap2)["npv"], 0)
    sens[k] = s
    L("敏感性 %s: %s" % (k, json.dumps(s, ensure_ascii=False)))

# ============================================================
# 七、集团口径补充（存量债务利息刚性，各路径共同项）
# ============================================================
grp = {}
for k, p in PATHS.items():
    grp[k] = {"interest_annual": BASE["interest_annual"],
              "shutdown_interest_outflow": round(BASE["interest_annual"] / 12 * p["downtime"], 2),
              "note": "存量债务 60,677 万元刚性，各路径共同项；集团口径现金流须叠加"}
    L("集团口径 %s: 停业期利息流出 %.0f 万元" % (k, grp[k]["shutdown_interest_outflow"]))

OUT = {"meta": {"title": "v98 三路径经济测算（整合 A1/A2/A3/A4）", "date": "2026-11-15",
                "口径": "收入=口径A（含服务费）呈现；成本与利润=口径B（P&L）；两口径 1.1006 倍可复算桥接",
                "评价": "项目口径 NPV/IRR/静态回收期（不含存量债务利息，该项为各路径共同项另列）；评价期 20 年；折现率 8%",
                "capex_anchor": CAPEX_ANCHOR, "capex_status": "产业发展部测算，待第三方工程量清单核定",
                "禁止引用": "★ 「春熙路 1,280 元／76.3%／977 元」——无法溯源的合成数，不得使用",
                "mandate": "《关于总府皇冠假日酒店重大安全隐患专题会纪要》（2026-10-16）第三条"},
       "base": BASE, "bench": BENCH, "engineering": ENGINEERING, "contract": CONTRACT,
       "paths": PATHS, "results": results, "breakeven": be, "sensitivity": sens, "group_view": grp}
io.open(os.path.join(T, "v98.json"), "w", encoding="utf-8").write(json.dumps(OUT, ensure_ascii=False, indent=1))
L("写出 v98.json")
L("DONE")
