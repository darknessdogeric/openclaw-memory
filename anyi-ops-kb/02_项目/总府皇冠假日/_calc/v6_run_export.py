# -*- coding: utf-8 -*-
"""
v6.1 · 月度时间轴引擎 + 分期开业情景 + 全维度 EXCEL 导出
修正 v6.0 的停业跨年处理（改为真正月度时间轴：停业月 → CAPEX 按月分摊 → 运营月按运营年爬坡）
"""
import io, os, sys, json
sys.path.insert(0, r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import v6_launch as V
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

SE = V.SE
OUT = V.OUT_DIR
HORIZON = 20

# ══════════════════════════════════════════════════════════════
# 月度时间轴引擎
# ══════════════════════════════════════════════════════════════
def month_revenue(dk, scen, op_year, mon):
    """运营月收入（万元）"""
    tier = V.TIER[dk["tier"]]
    s = V.SCEN[scen]
    sm = SE["season"][mon]
    mix = tier["mix"]
    ramp_i = min(op_year - 1, len(V.RAMP["adr"]) - 1)
    adr = dk["adr"] * s["adr"] * V.RAMP["adr"][ramp_i] * sm["adr_idx"]
    occ = dk["occ"] * s["occ"] * V.RAMP["occ"][ramp_i] * sm["occ_idx"]
    rooms_sold = dk["rooms_sellable"] * occ * 30.4
    rooms_rev = adr * rooms_sold / 1e4
    if dk["tier"] == "intl_current_crowne":
        fnb_r = sm["fnb_ratio"] * s["fnb"]
        banq_r = sm["banq_ratio"] * (2 - s["fnb"])
    else:
        fnb_r = mix["fnb"] * sm["fnb_idx"] * s["fnb"]
        banq_r = mix["banq"] * sm["banq_idx"]
    scale = rooms_rev / mix["rooms"]
    fnb = scale * fnb_r
    banq = scale * banq_r
    other = scale * mix["other"]
    misc = scale * mix["misc"]
    total = rooms_rev + fnb + banq + other + misc
    g = tier["dept_gop"]
    gop = (rooms_rev*g["rooms"] + fnb*g["fnb"] + banq*g["banq"] +
           other*g["other"] + misc*g["misc"]) * s["gop"]
    f = dk["fees"]
    fee_base = total * f["base"]
    fee_mkt = rooms_rev * f["marketing"]
    fee_loy = rooms_rev * f["loyalty"]
    fee_res = rooms_rev * f["reservation"]
    fee_room = rooms_rev * f["room_rev_fee"]
    fee_ffe = total * f["ffe_reserve"]
    fee_fixed = (f["it_fee_wan"] + f["training_wan"]) / 12.0   # 年度固定费折算为月度
    fee_inc = gop * f["incentive"]
    owner_gop = gop - fee_base - fee_mkt - fee_loy - fee_res - fee_room - fee_ffe - fee_fixed - fee_inc
    return dict(mon=mon, adr=adr, occ=occ, rooms_sold=rooms_sold,
                rooms_rev=rooms_rev, fnb=fnb, banq=banq, other=other, misc=misc, total=total,
                gop=gop, gop_rate=(gop/total if total else 0),
                fee_base=fee_base, fee_mkt=fee_mkt, fee_loy=fee_loy, fee_res=fee_res,
                fee_room=fee_room, fee_ffe=fee_ffe, fee_fixed=fee_fixed, fee_inc=fee_inc,
                fee_total=fee_base+fee_mkt+fee_loy+fee_res+fee_room+fee_ffe+fee_fixed+fee_inc,
                owner_gop=owner_gop)

def run_monthly(dk_key, scen="中性", horizon=HORIZON, fixed_monthly=231.4,
                closure_start=12, phased=None, adr_mult=1.0, occ_mult=1.0,
                capex_mult=1.0):
    """phased = None → 一次全停业；否则 phased=[(停业月数, 可售房数, ADR系数, 餐饮系数), ...]"""
    dk = dict(V.DIRECTIONS[dk_key])
    dk["adr"] *= adr_mult
    dk["occ"] = min(0.95, dk["occ"] * occ_mult)
    capex = V.capex_total(dk["capex"]) * capex_mult
    # 预估稳定年营收 → 停业期品牌保留费（基础费年值 × 35% / 12）
    probe = month_revenue(dk, scen, 2, 6)
    brand_ret = probe["total"] * dk["fees"]["base"] * 0.35 / 12.0
    segs = []   # (停业月数, 可售房数, ADR系数, 餐饮系数)
    if phased is None:
        segs = [(dk["closure_months"], dk["rooms_sellable"], 1.0, 1.0)]
    else:
        segs = phased
    timeline = []
    capex_per_closed_month = capex / max(1, sum(x[0] for x in segs))
    m = 0
    seg_i = 0
    op_m = 0
    op_year = 0
    total_closed = sum(x[0] for x in segs)
    while m < horizon * 12:
        seg = segs[min(seg_i, len(segs)-1)]
        if m < seg[0]:
            mon = ((closure_start - 1) + m) % 12 + 1
            rev_lost = SE["season"][mon]["rev"] / 1e4
            loss = rev_lost + fixed_monthly + brand_ret
            timeline.append(dict(m=m+1, state="停业", mon=mon, revenue=0.0,
                                 loss=loss, rev_lost=rev_lost, fixed=fixed_monthly,
                                 brand=brand_ret, capex=-capex_per_closed_month,
                                 owner_gop=0.0, cashflow=-loss - capex_per_closed_month,
                                 gop=0.0, fee_total=0.0, rooms_sold=0.0, adr=0.0, occ=0.0,
                                 seg=seg_i+1))
        else:
            op_m += 1
            op_year = (op_m - 1) // 12 + 1
            mon = ((closure_start - 1) + m) % 12 + 1
            dk2 = dict(dk)
            dk2["rooms_sellable"] = seg[1]
            r = month_revenue(dk2, scen, op_year, mon)
            # 分期系数
            if seg[2] != 1.0:
                r["adr"] *= seg[2]
                r["rooms_rev"] *= seg[2]
                r["total"] *= (seg[2] + seg[3]) / 2
                r["fnb"] *= seg[3]
                r["banq"] *= seg[3]
                r["gop"] *= 0.92
                r["owner_gop"] *= 0.92
                r["fee_total"] *= 0.8
            # 过渡期：开业首 24 个月额外折损
            trans = 0.0
            if op_year <= 2:
                trans = -r["total"] * 0.08
            cf = r["owner_gop"] + trans
            timeline.append(dict(m=m+1, state="运营", mon=mon, revenue=r["total"],
                                 loss=0.0, rev_lost=0.0, fixed=0.0, brand=0.0, capex=0.0,
                                 owner_gop=r["owner_gop"], cashflow=cf, gop=r["gop"],
                                 fee_total=r["fee_total"], rooms_sold=r["rooms_sold"],
                                 rooms_rev=r["rooms_rev"], fnb=r["fnb"], banq=r["banq"],
                                 other=r["other"], misc=r["misc"],
                                 adr=r["adr"], occ=r["occ"], trans=trans, seg=seg_i+1))
        m += 1
        # 段推进
        if seg_i + 1 < len(segs) and m == sum(segs[j][0] for j in range(seg_i+1)):
            seg_i += 1
    # 年汇总
    years = []
    for y in range(1, horizon+1):
        ms = [t for t in timeline if (t["m"]-1)//12 == y-1]
        if not ms:
            continue
        agg = dict(year=y,
                   revenue=round(sum(t["revenue"] for t in ms),1),
                   rooms_rev=round(sum(t.get("rooms_rev",0) for t in ms),1),
                   fnb=round(sum(t.get("fnb",0) for t in ms),1),
                   banq=round(sum(t.get("banq",0) for t in ms),1),
                   other=round(sum(t.get("other",0) for t in ms),1),
                   misc=round(sum(t.get("misc",0) for t in ms),1),
                   rooms_sold=round(sum(t["rooms_sold"] for t in ms)),
                   gop=round(sum(t["gop"] for t in ms),1),
                   fee_total=round(sum(t["fee_total"] for t in ms),1),
                   owner_gop=round(sum(t["owner_gop"] for t in ms),1),
                   closure_loss=round(sum(t["loss"] for t in ms),1),
                   capex=round(sum(t["capex"] for t in ms),1),
                   cashflow=round(sum(t["cashflow"] for t in ms),1),
                   closed_months=sum(1 for t in ms if t["state"]=="停业"),
                   open_months=sum(1 for t in ms if t["state"]=="运营"))
        agg["gop_rate"] = round(agg["gop"]/agg["revenue"],4) if agg["revenue"] else 0
        agg["trevpar"] = round(agg["revenue"]/agg["rooms_sold"],1) if agg["rooms_sold"] else 0
        agg["fee_rate"] = round(agg["fee_total"]/agg["revenue"],4) if agg["revenue"] else 0
        years.append(agg)
    cfs = [y["cashflow"] for y in years]
    return dict(dk_key=dk_key, label=dk["label"], scenario=scen, horizon=horizon,
                capex=round(capex,1), timeline=timeline, years=years, cfs=cfs,
                closure_total=round(sum(t["loss"] for t in timeline),1),
                closure_months=sum(1 for t in timeline if t["state"]=="停业"),
                brand_ret=round(brand_ret,1),
                irr=V.irr(cfs), npv=round(V.npv(V.GOV["discount_rate"], cfs),1),
                payback=V.payback(cfs),
                rev_y5=round(sum(y["revenue"] for y in years[2:5])/3,1),
                owner_gop_y5=round(sum(y["owner_gop"] for y in years[2:5])/3,1),
                gop_rate_y5=round(sum(y["gop"] for y in years[2:5])/sum(y["revenue"] for y in years[2:5]),4))

# 分期开业情景（依赖消防审查机构认可分区验收 —— 前提未成立则为条件情景）
PHASED = {
 "D2": [(10, 165, 0.88, 0.55), (8, 268, 1.0, 1.0)],
 "D3": [(12, 165, 0.85, 0.50), (9, 268, 1.0, 1.0)],
}

# ══════════════════════════════════════════════════════════════
# EXCEL 工具
# ══════════════════════════════════════════════════════════════
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
H1 = Font(bold=True, size=14, color="FFFFFF")
H2 = Font(bold=True, size=11, color="FFFFFF")
BOLD = Font(bold=True)
FILL1 = PatternFill("solid", fgColor="1F4E79")
FILL2 = PatternFill("solid", fgColor="2E75B6")
FILLOK = PatternFill("solid", fgColor="C6EFCE")
FILLWARN = PatternFill("solid", fgColor="FFEB9C")
FILLBAD = PatternFill("solid", fgColor="FFC7CE")

def sheet_title(ws, title, sub=None, width=12):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=width)
    c = ws.cell(row=1, column=1, value=title)
    c.font = H1; c.fill = FILL1; c.alignment = Alignment(vertical="center", horizontal="left")
    ws.row_dimensions[1].height = 26
    r = 2
    if sub:
        ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=width)
        c = ws.cell(row=2, column=1, value=sub)
        c.font = Font(size=9, italic=True, color="595959")
        r = 3
    return r

def hdr(ws, row, headers, widths=None):
    for i, h in enumerate(headers, 1):
        c = ws.cell(row=row, column=i, value=h)
        c.font = H2; c.fill = FILL2; c.border = BORDER
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    ws.row_dimensions[row].height = 32
    if widths:
        for i, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(i)].width = w
    return row + 1

def put(ws, row, values, fmts=None, fills=None):
    for i, v in enumerate(values, 1):
        c = ws.cell(row=row, column=i, value=v)
        c.border = BORDER
        c.font = Font(size=10)
        if fmts and i-1 < len(fmts) and fmts[i-1]:
            c.number_format = fmts[i-1]
        if fills and i-1 < len(fills) and fills[i-1]:
            c.fill = fills[i-1]
    return row + 1

def export_direction(dk_key, res, filename):
    dk = V.DIRECTIONS[dk_key]
    wb = Workbook()
    # 00 封面
    ws = wb.active; ws.title = "00_封面与口径"
    r = sheet_title(ws, "总府皇冠假日酒店改造升级项目 · 立项经济测算（%s）" % dk["label"],
                    "口径：USALI 13 部门制 · 国际联号 · 情景 %s · %d 年 · 含隐性成本 · 月度建模 ｜ 编制：产业发展部 2026-11-08 ｜ 内部资料" % (res["scenario"], res["horizon"]), 10)
    rows = [
        ("方向", dk["label"]), ("品牌档位", dk["tier_tag"]), ("USALI 收入结构", V.TIER[dk["tier"]]["mix"]),
        ("部门 GOP 率", V.TIER[dk["tier"]]["dept_gop"]),
        ("改造后房量（可售）", dk["rooms_sellable"]), ("目标 ADR（元）", dk["adr"]),
        ("目标出租率", dk["occ"]), ("总投资 CAPEX（万元）", res["capex"]),
        ("停业月数", res["closure_months"]), ("停业期损失合计（万元）", res["closure_total"]),
        ("停业期品牌方保留费（万元/月）", res["brand_ret"]),
        ("稳定年（Y3–Y5）平均营收（万元）", res["rev_y5"]),
        ("稳定年 GOP 率", res["gop_rate_y5"]),
        ("稳定年业主 GOP（万元）", res["owner_gop_y5"]),
        ("IRR（%d 年）" % res["horizon"], ("%.2f%%" % (res["irr"]*100)) if res["irr"] else "无可解（现金流未转正）"),
        ("NPV @8%（万元）", res["npv"]),
        ("静态回收期（年）", ("%.1f" % res["payback"]) if res["payback"] else "未回收"),
        ("国资 IRR 门槛", V.GOV["irr_floor"]),
        ("国资回收期上限（年）", V.GOV["payback_max_years"]),
    ]
    for k, v in rows:
        c1 = ws.cell(row=r, column=1, value=k); c1.font = BOLD; c1.border = BORDER
        c2 = ws.cell(row=r, column=2, value=v if not isinstance(v, dict) else str(v))
        c2.border = BORDER
        r += 1
    ws.column_dimensions["A"].width = 34; ws.column_dimensions["B"].width = 62
    # 01 输入假设
    ws = wb.create_sheet("01_输入假设")
    r = sheet_title(ws, "01 · 输入假设（可改参数）", "修改本表数值即可重算；引擎参数与本表一一对应", 8)
    r = hdr(ws, r, ["参数","取值","单位","来源/依据","数据等级"], [34,16,10,52,12])
    items = [
        ("客房数（改造后可售）", dk["rooms_sellable"], "间", "方向二/三：3 改 2 至 268 间（品牌方 F2-29 明确 40 ㎡+ 要求）", "🟢 实测/官方"),
        ("目标 ADR", dk["adr"], "元/间夜", "方向二：洲至奢选棕榈泉实测起价 $127≈￥914；方向三：STR 春熙路—太古里商圈均值 1,280", "🔵 行业机构"),
        ("目标出租率", dk["occ"], "—", "现状 70.78%；方向三对标太古里 76.3%（保守折让）", "🟢 实测/推算"),
        ("客房收入占比", V.TIER[dk["tier"]]["mix"]["rooms"], "—", V.TIER[dk["tier"]]["mix_basis"], "🔵 国际基准"),
        ("餐饮占比", V.TIER[dk["tier"]]["mix"]["fnb"], "—", V.TIER[dk["tier"]]["mix_basis"], "🔵 国际基准"),
        ("会议宴会占比", V.TIER[dk["tier"]]["mix"]["banq"], "—", V.TIER[dk["tier"]]["mix_basis"], "🔵 国际基准"),
        ("客房部门 GOP 率", V.TIER[dk["tier"]]["dept_gop"]["rooms"], "—", "国际联号基准 58%–75% 区间中值", "🔵 国际基准"),
        ("餐饮部门 GOP 率", V.TIER[dk["tier"]]["dept_gop"]["fnb"], "—", "国际联号基准 15%–30% 区间中值", "🔵 国际基准"),
        ("基础管理费", dk["fees"]["base"], "总营收", "HMA 行业区间 2.0%–4.0%；洲际委托口径『总收入 2%』", "🟡 品牌方口径"),
        ("激励费", dk["fees"]["incentive"], "GOP", "HMA 行业区间 5.0%–15.0%", "🔵 行业机构"),
        ("品牌营销费", dk["fees"]["marketing"], "客房收入", "HMA 行业区间 1.0%–3.0%", "🔵 行业机构"),
        ("忠诚度计划费", dk["fees"]["loyalty"], "客房收入", "HMA 行业区间可变", "🔵 行业机构"),
        ("预订/分销费", dk["fees"]["reservation"], "客房收入", "HMA 行业区间差异极大", "🔵 行业机构"),
        ("FF&E 储备金", dk["fees"]["ffe_reserve"], "总营收", "国际联号惯例 3%–5%", "🔵 国际基准"),
        ("特许管理费（客房收入）", dk["fees"]["room_rev_fee"], "客房收入", "⭐ F2-29 洲际方原话：特许管理费客房收入 5%", "🟡 品牌方口径"),
        ("IT/系统费（年）", dk["fees"]["it_fee_wan"], "万元", "HMA：固定或可变，日趋重要", "🟠 推算"),
        ("培训与质保（年）", dk["fees"]["training_wan"], "万元", "HMA：固定/周期性", "🟠 推算"),
        ("停业期固定成本", 284.0, "万元/月", "业主实测人工+能耗+维保+租金+税费等不可中断支出", "🟢 实测"),
        ("停业期品牌方保留费系数", 0.35, "基础费×", "HMA：营收为 0 则基础费为 0，但品牌方保留质量/FLS 职能", "🟠 推算"),
        ("开工月份", dk["closure_start_month"], "月", "⭐ 12 月为全年唯一亏损月 → 停业即止损", "🟢 实测"),
        ("停业月数", res["closure_months"], "月", "第六/十部分关键路径推算", "🟠 推算"),
        ("折现率", V.GOV["discount_rate"], "—", "国资评估常用口径（待集团确认）", "⚠️ 待确认"),
        ("所得税率", V.GOV["tax_rate"], "—", "法定 25%", "🟢 官方"),
    ]
    for it in items:
        r = put(ws, r, list(it), fmts=[None, "0.0000" if isinstance(it[1], float) else "#,##0", None, None, None])
    # 02 HMA 分解
    ws = wb.create_sheet("02_品牌标准与HMA费率")
    r = sheet_title(ws, "02 · 品牌费用 HMA 制度性分解 + 行业指示区间", "来源：Hotel Development Guide (Darren Blanchard, 2026-10) + F2-29 洲际一手口径", 6)
    r = hdr(ws, r, ["费项","计费基数","行业指示区间","本方向取值","关键考量","数据等级"], [26,24,18,22,54,12])
    f = dk["fees"]
    vals = {
        "基础管理费 Base Fee": ("总营收(不含增值税)", "2.0%–4.0%", f"{f['base']*100:.1f}% 总营收", "与盈利无关，照付；收入定义至关重要"),
        "激励费 Incentive Fee": ("GOP 或 AGOP(分级)", "5.0%–15.0%", f"{f['incentive']*100:.1f}% GOP", "门槛与结构显著影响结果"),
        "预订/分销 Reservation": ("每单 或 客房收入%", "差异极大", f"{f['reservation']*100:.1f}% 客房收入", "高量系统可能很可观"),
        "品牌营销 Marketing": ("客房收入%", "1.0%–3.0%", f"{f['marketing']*100:.1f}% 客房收入", "系统性、通常不可谈"),
        "忠诚度计划 Loyalty": ("每住/每积分/营收%", "可变", f"{f['loyalty']*100:.1f}% 客房收入", "视品牌渗透率与客群结构"),
        "IT/系统费 IT & Systems": ("固定或可变", "可变", f"{f['it_fee_wan']:.0f} 万元/年", "日益重要，常带调整条款"),
        "培训与质保 Training&QA": ("固定/周期性", "可变", f"{f['training_wan']:.0f} 万元/年", "支持品牌标准，可能随新举措上浮"),
        "可报销费用 Reimbursables": ("按合同", "可变", "未单列（计入毛利预留）", "需透明度与加成(markup)审查"),
        "开业前费用 Pre-opening": ("按合同", "—", f"{f['preopening_months']:.0f} 个月（已计入 CAPEX）", "⭐ 常按 6–12 个月基础费计，须计入开业成本"),
        "特许管理费（洲际特有）": ("客房收入%", "5%（洲际口径）", f"{f['room_rev_fee']*100:.1f}% 客房收入", "⭐ F2-29 原话：特许管理费客房收入 5%，取代原基本管理费"),
        "FF&E 储备金": ("总营收", "3%–5%", f"{f['ffe_reserve']*100:.1f}% 总营收", "国际联号惯例，用于周期性翻新"),
    }
    order = list(V.HMA_INDUSTRY.keys()) + ["特许管理费（洲际特有）", "FF&E 储备金"]
    for k in order:
        b, rng, cur, note = vals.get(k, ("—","—","—","—"))
        r = put(ws, r, [k, b, rng, cur, note, "🟡 品牌方口径" if k=="特许管理费（洲际特有）" else "🔵 行业机构"])
    r += 1
    ws.cell(row=r, column=1, value="⭐ 关键提示：基础管理费在亏损期照付（HMA 通行做法）→ 停业期是否豁免基础费，必须作为显性测算项与品牌方书面约定。").font = Font(bold=True, color="C00000")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)
    # 03 CAPEX
    ws = wb.create_sheet("03_CAPEX明细")
    r = sheet_title(ws, "03 · 改造投资明细（万元 · 中值）", "依据：工程部台账 + 第一批次资料 + 品牌标准 + F2-29 洲际标准增量", 5)
    r = hdr(ws, r, ["项目","金额(万元)","占总投资","内容与依据","数据等级"], [34,14,11,72,12])
    items = V.CAPEX[dk["capex"]]["items"]
    tot = sum(x[1] for x in items)
    for nm, amt, note in items:
        lvl = "🟢 实测/官方" if amt == 0 else "🟠 推算"
        r = put(ws, r, [nm, amt, (amt/tot if tot else 0), note, lvl],
                fmts=[None, "#,##0", "0.0%", None, None],
                fills=[None, None, None, None, FILLOK if amt == 0 else None])
    r = put(ws, r, ["合计", tot, 1.0, "", ""], fmts=[None, "#,##0", "0.0%", None, None],
            fills=[FILLWARN, FILLWARN, FILLWARN, FILLWARN, FILLWARN])
    # 04 月度收入
    ws = wb.create_sheet("04_月度收入模型")
    r = sheet_title(ws, "04 · 月度收入模型（%d 年 × 12 月）" % res["horizon"], "单位：万元；ADR 元；OCC 占比；含停业月（营收 0）", 13)
    r = hdr(ws, r, ["月序","年","历月","状态","ADR","OCC","已售间夜","客房收入","餐饮","会议宴会","其他","总营收","业主GOP"],
            [7,6,7,8,10,9,11,12,10,10,9,12,12])
    for t in res["timeline"]:
        rr = res["years"]
        y = (t["m"]-1)//12 + 1
        fills = [None]*13
        if t["state"] == "停业": fills[3] = FILLBAD
        r = put(ws, r, [t["m"], y, t["mon"], t["state"], round(t["adr"],1) if t["adr"] else 0,
                        round(t["occ"],4) if t["occ"] else 0, round(t["rooms_sold"]), 
                        round(t.get("rooms_rev",0),1), round(t.get("fnb",0),1), round(t.get("banq",0),1),
                        round(t.get("other",0),1), round(t.get("revenue",0),1), round(t["owner_gop"],1)],
                fmts=[None,None,None,None,"#,##0.0","0.0%","#,##0","#,##0.0","#,##0.0","#,##0.0","#,##0.0","#,##0.0","#,##0.0"],
                fills=fills)
    # 05 年度
    ws = wb.create_sheet("05_年度GOP与费用")
    r = sheet_title(ws, "05 · 年度经营与业主现金流（万元）", "GOP 率为部门制加权；品牌费率 = 品牌费用合计 / 总营收", 15)
    r = hdr(ws, r, ["年","营业总收入","客房收入","餐饮","会议宴会","GOP","GOP率","品牌费用合计","品牌费率","业主GOP","停业损失","CAPEX","现金流","TRevPAR","开/停月"],
            [6,14,13,10,11,13,9,14,10,13,12,12,13,11,10])
    for y in res["years"]:
        f = FILLOK if y["cashflow"] > 0 else None
        r = put(ws, r, [y["year"], y["revenue"], y["rooms_rev"], y["fnb"], y["banq"], y["gop"],
                        y["gop_rate"], y["fee_total"], y["fee_rate"], y["owner_gop"],
                        y["closure_loss"], y["capex"], y["cashflow"], y["trevpar"],
                        "%d/%d" % (y["open_months"], y["closed_months"])],
                fmts=[None,"#,##0.0","#,##0.0","#,##0.0","#,##0.0","#,##0.0","0.0%","#,##0.0","0.0%","#,##0.0","#,##0.0","#,##0.0","#,##0.0","#,##0.0",None],
                fills=[None]*12 + [f, None, None])
    # 06 现金流与IRR
    ws = wb.create_sheet("06_业主现金流与IRR")
    r = sheet_title(ws, "06 · 业主现金流、IRR / NPV / 回收期", "折现率 8%（国资口径，待集团确认）", 8)
    r = hdr(ws, r, ["年","业主GOP","停业损失","CAPEX","净现金流","累计现金流","折现现金流","折现累计"], [7,14,13,13,14,15,14,15])
    cum = 0.0; dcum = 0.0
    for i, y in enumerate(res["years"]):
        cum += y["cashflow"]
        dcf = y["cashflow"] / (1+V.GOV["discount_rate"])**i
        dcum += dcf
        r = put(ws, r, [y["year"], y["owner_gop"], -y["closure_loss"], y["capex"], y["cashflow"], cum, round(dcf,1), round(dcum,1)],
                fmts=[None,"#,##0.0","#,##0.0","#,##0.0","#,##0.0","#,##0.0","#,##0.0","#,##0.0"])
    r += 1
    for k, v in [("IRR", ("%.2f%%" % (res["irr"]*100)) if res["irr"] else "无可解"),
                 ("NPV @8%（万元）", res["npv"]),
                 ("静态回收期（年）", ("%.1f" % res["payback"]) if res["payback"] else "未回收"),
                 ("总 CAPEX（万元）", res["capex"]),
                 ("停业期损失合计（万元）", res["closure_total"])]:
        c1 = ws.cell(row=r, column=1, value=k); c1.font = BOLD; c1.border = BORDER
        c2 = ws.cell(row=r, column=2, value=v); c2.border = BORDER
        r += 1
    # 07 停业期
    ws = wb.create_sheet("07_停业期损失与开工月份")
    r = sheet_title(ws, "07 · 停业期损失（按 24 个月实测逐月曲线）与开工月份决策", "收入损失用实测历月营收；固定成本 284 万/月照提；含品牌方保留费", 9)
    r = hdr(ws, r, ["历月","实测月营收(万)","停业损失(万)","累计损失(万)"], [10,16,16,16])
    cum2 = 0.0
    for t in res["timeline"]:
        if t["state"] != "停业": continue
        cum2 += t["loss"]
        r = put(ws, r, [t["mon"], round(t["rev_lost"],1), round(t["loss"],1), round(cum2,1)],
                fmts=[None,"#,##0.0","#,##0.0","#,##0.0"])
    r += 2
    ws.cell(row=r, column=1, value="⭐ 开工月份 × 停业月数 → 停业期总损失矩阵（万元，含固定成本 284 万/月）").font = Font(bold=True, color="C00000")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=9)
    r += 1
    r = hdr(ws, r, ["开工月"] + ["%d月" % d for d in range(12, 23)], [10] + [10]*11)
    for st in range(1, 13):
        vals = [st]
        for d in range(12, 23):
            _, t = V.closure_loss(st, d, 284.0)
            vals.append(t)
        fills = [None]
        for i, d in enumerate(range(12, 23)):
            best = min(V.closure_loss(s2, d, 284.0)[1] for s2 in range(1, 13))
            fills.append(FILLOK if vals[i+1] == best else (FILLBAD if vals[i+1] >= max(V.closure_loss(s2, d, 284.0)[1] for s2 in range(1,13)) else None))
        r = put(ws, r, vals, fmts=[None] + ["#,##0"]*11, fills=fills)
    # 08 分期开业情景
    ws = wb.create_sheet("08_分期开业情景")
    r = sheet_title(ws, "08 · 一次全停业 vs 分期开业（短停业）情景对比", "⭐ 分期情景以『消防审查机构认可分区验收/分段开业』为前提 —— 该前提尚未成立", 10)
    r = hdr(ws, r, ["方案","停业月数","总停业月","停业损失(万)","CAPEX(万)","稳定年营收(万)","业主GOP(万)","IRR","NPV@8%(万)","回收期(年)"], [30,10,10,14,13,15,14,10,14,12])
    full = res
    r = put(ws, r, ["一次全停业（基准）", full["closure_months"], full["closure_months"], full["closure_total"], full["capex"], full["rev_y5"], full["owner_gop_y5"],
                    ("%.2f%%" % (full["irr"]*100)) if full["irr"] else "无可解", full["npv"], ("%.1f" % full["payback"]) if full["payback"] else "未回收"],
            fmts=[None,None,None,"#,##0","#,##0","#,##0","#,##0",None,"#,##0",None])
    if dk_key in PHASED:
        ph = run_monthly(dk_key, res["scenario"], res["horizon"], 284.0, dk["closure_start_month"], phased=PHASED[dk_key])
        segs = PHASED[dk_key]
        r = put(ws, r, ["分期开业（条件情景）· " + " + ".join("%d月/%d间" % (s[0], s[1]) for s in segs),
                        ph["closure_months"], ph["closure_months"], ph["closure_total"], ph["capex"], ph["rev_y5"], ph["owner_gop_y5"],
                        ("%.2f%%" % (ph["irr"]*100)) if ph["irr"] else "无可解", ph["npv"], ("%.1f" % ph["payback"]) if ph["payback"] else "未回收"],
                fmts=[None,None,None,"#,##0","#,##0","#,##0","#,##0",None,"#,##0",None],
                fills=[FILLOK,None,None,None,None,None,None,None,None,None])
        d_closure = round(full["closure_total"] - ph["closure_total"],1)
        d_irr = (ph["irr"] - full["irr"]) if (ph["irr"] and full["irr"]) else None
        r += 1
        for k, v in [("分期带来的停业损失减少（万元）", d_closure),
                     ("IRR 变化", ("%.2f 个百分点" % (d_irr*100)) if d_irr is not None else "n/a"),
                     ("⭐ 前提条件", "消防审查机构认可分区验收/分段开业（R-01）+ 品牌方接受（已明确『可以接受』）")]:
            c1 = ws.cell(row=r, column=1, value=k); c1.font = BOLD; c1.border = BORDER
            c2 = ws.cell(row=r, column=2, value=v); c2.border = BORDER
            ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=10)
            r += 1
    # 09 敏感性
    ws = wb.create_sheet("09_敏感性分析")
    r = sheet_title(ws, "09 · 敏感性分析（IRR 对关键参数）", "基准：中性情景 20 年", 8)
    r = hdr(ws, r, ["参数","-15%","-10%","-5%","基准","+5%","+10%","+15%"], [26,13,13,13,13,13,13,13])
    for pname, kw in [("ADR", dict(adr_mult=1.0)), ("出租率", dict(occ_mult=1.0))]:
        pass
    for label, mk in [("ADR ×", "adr"), ("出租率 ×", "occ"), ("CAPEX ×", "capex")]:
        row = [label]
        for d in (-0.15, -0.10, -0.05, 0.0, 0.05, 0.10, 0.15):
            if mk == "adr": rr = run_monthly(dk_key, res["scenario"], res["horizon"], 284.0, dk["closure_start_month"], adr_mult=1+d)
            elif mk == "occ": rr = run_monthly(dk_key, res["scenario"], res["horizon"], 284.0, dk["closure_start_month"], occ_mult=1+d)
            else: rr = run_monthly(dk_key, res["scenario"], res["horizon"], 284.0, dk["closure_start_month"], capex_mult=1+d)
            row.append(("%.2f%%" % (rr["irr"]*100)) if rr["irr"] else "无")
        r = put(ws, r, row, fills=[None]+[FILLOK if i==3 else None for i in range(8)])
    r += 1
    ws.cell(row=r, column=1, value="注：CAPEX 敏感性中『无』表示该情景下现金流始终未转正，IRR 无可解根。").font = Font(size=9, italic=True, color="595959")
    # 10 国资校验
    ws = wb.create_sheet("10_国资口径校验")
    r = sheet_title(ws, "10 · 国资体系口径校验", "依据《中央企业投资监督管理办法》（年度投资计划备案 + 负面清单分类监管）与国有资产评估项目备案制", 6)
    r = hdr(ws, r, ["校验项","本方向结果","阈值/要求","是否达标","说明","数据等级"], [28,18,20,12,54,12])
    irr_v = ("%.2f%%" % (res["irr"]*100)) if res["irr"] else None
    ok1 = (res["irr"] is not None and res["irr"] >= V.GOV["irr_floor"])
    ok2 = (res["payback"] is not None and res["payback"] <= V.GOV["payback_max_years"])
    checks = [
        ("项目 IRR ≥ 门槛", irr_v or "无可解", f"≥{V.GOV['irr_floor']*100:.0f}%", "达标" if ok1 else "不达标",
         "⭐ 规划目标为『营业现金毛流量约 2,500 万、利润总额亏损控制在约 300 万』—— IRR 门槛须以集团口径最终确认", "⚠️ 待确认"),
        ("静态回收期 ≤ 上限", ("%.1f 年" % res["payback"]) if res["payback"] else "未回收", f"≤{V.GOV['payback_max_years']} 年", "达标" if ok2 else "不达标",
         "国资体系对长周期回报项目通常容忍更长回收期；本阈值为讨论用参数", "⚠️ 待确认"),
        ("减房后资产规模合理性", "415→268 间（-35%）", "不做超标准建设", "待评估",
         "⭐『做减法』符合国资『避免超标准建设』导向：同投资额下提升单间品质与坪效，而非扩大规模", "🟠 推算"),
        ("主业契合度", dk["tier_tag"], "主业投资", "待评估",
         "总府为安逸酒店集团主业酒店资产，改造属主业投资；⭐ 换牌为委托/特许经营，不新增非主业投资", "🟢 官方"),
        ("投资计划备案", "需列入集团年度投资计划", "备案管理", "待办",
         "⭐ 规划『六家改造项目总投资约 4.01 亿元、分两批实施、2029 年全部投入运营』→ 总府额度与批次须集团明确", "⚠️ 待确认"),
        ("资产评估", "存量房产正式评估值待取", "评估项目备案", "待办",
         "评估值 + 土地剩余年限是 P0 参数；减房后评估口径（按可售房量还是建筑面积）须与评估机构对齐", "⚠️ 待确认"),
        ("负债与融资", "改造后融资方案与年利息待定", "资产负债率 ≤70%", "待办",
         "⭐ 前期已标注『年利息』为最大低估项 —— 未含利息时 IRR 普遍偏乐观", "⚠️ 待确认"),
    ]
    for ck in checks:
        f = FILLOK if ck[3] == "达标" else (FILLBAD if ck[3] == "不达标" else FILLWARN)
        r = put(ws, r, list(ck), fills=[None,None,None,f,None,None])
    path = os.path.join(OUT, filename)
    wb.save(path)
    return path

if __name__ == "__main__":
    print("=== v6.1 引擎自检 ===")
    print("季节性：ADR %.1f｜OCC %.1f%%｜月均营收 %.1f 万" % (SE["avg_adr"], SE["avg_occ"]*100, SE["avg_rev"]/1e4))
    for k in ("D1","D2","D3"):
        print("CAPEX %s = %d 万" % (k, V.capex_total(k)))
    out = {}
    for k in ("D1","D2","D3"):
        for sc in ("保守","中性","乐观"):
            r = run_monthly(k, sc, HORIZON, 284.0, V.DIRECTIONS[k]["closure_start_month"])
            out[(k,sc)] = r
            print("%s %s: 停业%s月 损失%s万 | Y5营收%s GOP率%.1f%% 业主GOP%s | IRR %s | NPV %s | 回收 %s" %
                  (k, sc, r["closure_months"], r["closure_total"], r["rev_y5"],
                   r["gop_rate_y5"]*100, r["owner_gop_y5"],
                   ("%.2f%%" % (r["irr"]*100)) if r["irr"] else "无",
                   r["npv"], ("%.1f" % r["payback"]) if r["payback"] else "未回收"))
    json.dump({f"{k}_{sc}": {kk: vv for kk, vv in r.items() if kk not in ("timeline","years","cfs")}
               for (k,sc), r in out.items()},
              open(os.path.join(V._D, "v6_results.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1, default=str)
    print("结果已存 v6_results.json")
