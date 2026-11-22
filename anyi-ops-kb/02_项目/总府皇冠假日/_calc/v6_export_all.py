# -*- coding: utf-8 -*-
"""生成 4 个 EXCEL：方向一/二/三 全维度 + 三方向对比与国资口径校验"""
import io, os, sys, json
sys.path.insert(0, r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日\_calc")
import v6_launch as V
import v6_run_export as E
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

OUT = V.OUT_DIR
H1 = Font(bold=True, size=14, color="FFFFFF"); H2 = Font(bold=True, size=11, color="FFFFFF")
BOLD = Font(bold=True); FILL1 = PatternFill("solid", fgColor="1F4E79")
FILL2 = PatternFill("solid", fgColor="2E75B6"); FILLOK = PatternFill("solid", fgColor="C6EFCE")
FILLWARN = PatternFill("solid", fgColor="FFEB9C"); FILLBAD = PatternFill("solid", fgColor="FFC7CE")
THIN = Side(style="thin", color="BFBFBF"); BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

# ═════ 时间计划（每方向）═════════════════════════════════════
TIMELINE = {
 "D1": [
  ("M0","品牌达标项清单 + 三年 PIP 遗留项销项计划","2027 Q1","产业发展部 + 酒店运营","不依赖品牌谈判"),
  ("M1","改造方案决策 + 启动施工（规划节点）","2027 H1–H2","集团 + 产业发展部","对内投资与工程决策"),
  ("M2","深化设计 + 消防报审完成","2027 Q4","设计院 + 总包","与减房无关，路径更短"),
  ("M3","长周期设备下单锁定（冷源 8–10月 / 变压器 6–8月 / 电梯 8–10月）","2027 Q2","工程部","停业前必须下单"),
  ("M4","⭐ 停业开工（12 月开工最省）","2028 Q1","总包","⭐ 开工月份价值 456 万（18月口径）／组合口径 9,431 万"),
  ("M5","机电主体 + 竖井重排完工","2029 Q1","总包","T3 机电主体 10–12 月"),
  ("M6","公区整改 + 品牌审计整改 + 三方验收 + 试运营","2029 Q2","总包 + 品牌方","T6 零浮动 2–3 月"),
  ("M7","⭐ 重新开业","2029 Q3","酒店运营","提前于规划 2030，为后续改造留出窗口"),
 ],
 "D2": [
  ("M0","⭐ 品牌材料包 + 内部口径准备（不启动正式谈判）","2027 Q1","产业发展部","F2-29 已给技术路径与商务口径"),
  ("M1","改造方案决策 + 启动施工（规划节点）","2027 H1–H2","集团 + 产业发展部","决策输入 = 两条品牌意向的并集标准"),
  ("M2","深化设计 + 消防报审 + 减房结构专项预沟通","2027 Q4","设计院 + 总包","⭐ 减房结构专项须与消防报审同步"),
  ("M3","长周期设备下单锁定 + FF&E 与艺术品选型启动","2027 Q2","工程部","停业前必须下单"),
  ("M4","⭐ 停业开工（12 月开工最省）","2027 Q4","总包","⭐ 12 月为全年唯一亏损月 → 停业即止损"),
  ("M5","机电主体 + 竖井重排 + 移卫水平管线（同一破除期）","2028 Q3","总包","⭐ 三者必须同属一个破除期"),
  ("M6","减房结构 + 客房硬装 + FF&E 进场","2029 Q1","总包","T2 真瓶颈 8–10 月"),
  ("M7","机电与隐蔽工程完工 + 公区改造","2029 Q2","总包","T3/T4 交叉"),
  ("M8","康养 SPA + 泳池迁址 + 艺术品陈设 + VI 全套替换","2029 Q3","总包 + 品牌方","⭐ VI：导视/印刷品/客用品/员工着装/楼顶标识"),
  ("M9","品牌审计整改 + 三方验收 + 试运营","2029 Q4","品牌方 + 第三方","T6 零浮动"),
  ("M10","⭐ 正式开业（规划 2030 目标）","2030 Q1","酒店运营","⭐ 与丽晶成都 2029Q3（180 间）错峰"),
 ],
 "D3": [
  ("M0","外部奢华品牌接洽与遴选（探索项，不在洲际建议清单内）","2027 Q1","产业发展部","⚠ 无 IHG 先例，审计记录不可跨品牌复用"),
  ("M1","改造方案决策 + 启动施工","2027 H2","集团 + 产业发展部","需品牌方先行接受"),
  ("M2","深化设计 + 消防报审 + 品牌方 FLS 专项","2028 Q1","设计院 + 总包","外部品牌条件更严"),
  ("M3","⭐ 停业开工","2028 Q1","总包","停业 20 月，为三方向最长"),
  ("M4","竖井重排 + 机电主体","2029 Q1","总包",""),
  ("M5","减房 + 客房奢牌级全改（含结构/移卫/全卫/进口石材）","2029 Q4","总包","268 间 × 40 万"),
  ("M6","公区奢牌级 + 旗舰 SPA + 艺术策展","2030 Q1","总包","周期基本不可压缩"),
  ("M7","品牌审计 + 三方验收 + 试运营","2030 Q2","品牌方 + 第三方",""),
  ("M8","⭐ 重新开业","2030 Q3","酒店运营","⚠ 已过规划 2030 节点"),
 ],
}

# ═════ 不停业 / 短停业论证 ══════════════════════════════════════
NONSTOP = [
 ("消防 · 火灾自动报警系统","1996 线路、绝缘值严重不达标，2026-07 全面瘫痪","🔴 必须全停",
  "主机回路板烧毁 + 1996 线路整体失效 → 属系统级更换，非分区可解决；且报警系统为全楼联动，分区施工期间无有效火灾探测 → 🔴 **消防侧是硬约束**"),
 ("消防 · 喷淋管网","1994 年敷设，整体更换","🔴 必须全停","管网为楼层内全覆盖 + 立管贯通，分区拆除即破坏未拆区段 → 只能一次全换"),
 ("消防 · 报审与重新验收","减房结构 + 消防同步报审","🔴 必须全停","⭐ **这是 R-01 的真正门槛**：改造后须整体重新报审验收；分区验收须消防审查机构明确认可（品牌方已表态『可以接受』，但非审批机关）"),
 ("机电 · 冷源主机","4 台约克离心机约 1,230KW，R11 冷媒","🔴 必须全停","主机房与冷冻水管为全楼服务核心，更换期必然影响全部楼层 → 宜在客房改造同窗期一次完成"),
 ("机电 · FCU 542 台 + 冷冻水管","1996 年产品 / 三年 43 次爆管、100% 老化","🔴 必须全停","末端数量巨大，与客房改造同层作业；若先做机电后做客房，将两次破除同一楼层"),
 ("机电 · 4 台变压器 + 34 面低压柜","1996 年产品","🟡 可分区","变配电室集中于特定层，可分段切换；但须与消防电源、发电与储油同窗"),
 ("给排水 · 1996 生活给水热水管网","整体老化","🟡 可分区","可逐层切换，但竖井内须与冷媒管/强电分离重排 → ⭐ 与竖井重排同窗"),
 ("隐蔽 · 竖井分层重排","1996 各系统同井叠加、无分层","🔴 必须与移卫同窗","⭐⭐ **竖井重排 + 移卫水平管线必须同属一个『破除期』** —— 分两期做 = 隐蔽工程做两遍，工期造价翻倍"),
 ("客房 · 3 改 2 移卫","拆除隔墙 + 卫浴移位 + 管线重排","🟢 可按楼层分区","⭐ **这是唯一天然可分区的工序**：按楼层分批改造，每层完成即恢复该层客房"),
 ("公区 · 大堂/宴会/ADD","大堂 5,468 ㎡、宴会 600/350 ㎡","🟡 可分区","大堂与宴会可后置；但公区是品牌审计必检项，须在开业前完成"),
 ("泳池 · 负 B2 迁 4F/屋顶","政府多次要求整改","🟢 可后置","泳池非客房主工序，可在一期之后"),
 ("康体 SPA / 艺术品 / VI","品牌标准项","🟢 可后置","⭐ 可在一期开业后再做，但品牌审计可能不通过 → 须与品牌方确认可分期达标"),
]

def add_timeline_sheet(wb, dk_key):
    ws = wb.create_sheet("11_改造时间计划")
    r = E.sheet_title(ws, "11 · 改造时间计划（对齐规划：2027 决策开工 / 2030 重新开业）",
                      "里程碑按『改造决策与品牌决策解耦』设计：品牌商务谈判不作为开工前提", 6)
    r = E.hdr(ws, r, ["里程碑","内容","目标时点","责任方","备注"], [10,58,18,22,44])
    for m in TIMELINE[dk_key]:
        f = [FILLOK if "⭐" in m[1] else None]*5
        r = E.put(ws, r, list(m), fills=f)
    r += 1
    ws.cell(row=r, column=1, value="⭐ 关键路径：T2 减房结构改造 8–10 月为真瓶颈，与竖井重排、移卫水平管线三者耦合｜T6 品牌审计整改+三方验收 2–3 月零浮动").font = Font(bold=True, color="C00000")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=6)

def add_nonstop_sheet(wb, dk_key):
    ws = wb.create_sheet("12_不停业与短停业论证")
    r = E.sheet_title(ws, "12 · ⭐ 可否不停业 / 短停业完成改造（逐工序判定）",
                      "结论：★ 完全不停业 —— 不可能；★ 分区分期（短停业）—— 技术上可行，但取决于消防审查机构是否认可分区验收（红线 R-01）", 5)
    r = E.hdr(ws, r, ["工序 / 系统","现状","可否不停业","技术依据","判定等级"], [30,42,14,66,14])
    for nm, cur, can, why in NONSTOP:
        lvl = "🔴 硬约束" if "必须全停" in can else ("🟡 可分区" if "分区" in can else "🟢 可后置")
        f = FILLBAD if "必须全停" in can else (FILLWARN if "可分区" in can else FILLOK)
        r = E.put(ws, r, [nm, cur, can, why, lvl], fills=[None,None,f,None,f])
    r += 2
    for k, v in [
        ("★ 结论一：完全不停业 —— 不可能", "消防报警（系统级、全楼联动）+ 喷淋管网（楼层全覆盖+立管贯通）+ 冷源主机（核心机房+全楼冷冻水）三项属硬约束，改造期无有效火灾探测与空调保障，开业即违规"),
        ("★ 结论二：短停业（分区分期）—— 技术可行", "客房 3 改 2 移卫是唯一天然可按楼层分区的工序；竖井重排可按竖井分区；机电可分段切换；公区/SPA/艺术品/VI 可后置"),
        ("★ 结论三：真正的卡点是审批，不是技术", "⭐ 品牌方已明确『可以接受分期改造、不整体停业』（F2-29 纪要原文），但消防报审与重新验收的批准机关是消防审查机构 —— ⭐ **该机关是否认可分区验收，是全案唯一的外部开关（R-01）**"),
        ("★ 结论四：短停业的量级（方向二中性情景）", "一次全停业 18 月 → 停业损失 15,273 万、IRR 9.49%、NPV +2,944 万、回收 9.7 年；★ 分期开业 → 停业损失 8,416 万、IRR 21.48%、NPV +16,597 万、回收 5.5 年；★ 损失减少 6,857 万，IRR +12.0 个百分点"),
        ("★ 结论五：技术与财务的耦合", "⭐ 短停业不仅是省钱，更是工期方案：它把方向二的『一次 18 个月空窗』拆成『10 个月 + 8 个月两次窗口 + 中间部分营业』，从而在 2030 开业前多出约 8 个月爬坡期 —— ⭐ 这正是第十部分 M4 一期开业预留缓冲的财务价值"),
    ]:
        c1 = ws.cell(row=r, column=1, value=k); c1.font = Font(bold=True, size=11, color="C00000"); c1.border = BORDER
        c1.alignment = Alignment(vertical="top", wrap_text=True)
        c2 = ws.cell(row=r, column=2, value=v); c2.border = BORDER
        c2.alignment = Alignment(vertical="top", wrap_text=True)
        ws.merge_cells(start_row=r, start_column=2, end_row=r, end_column=5)
        ws.row_dimensions[r].height = 46
        r += 1

def build_comparison(results):
    wb = Workbook()
    ws = wb.active; ws.title = "00_封面"
    r = E.sheet_title(ws, "总府皇冠假日酒店改造升级项目 · 三方向对比与国资口径校验",
                      "口径：USALI 部门制 · 国际联号 · 20 年 · 含隐性成本 · 月度建模 ｜ 编制：产业发展部 2026-11-08 ｜ 内部资料·注意保密", 8)
    ws.cell(row=r, column=1, value="本工作簿为总表；每方向的完整全维度测算见各自独立工作簿（10 个 Sheet）。").font = Font(size=10, italic=True)
    # 01 关键指标对比
    ws = wb.create_sheet("01_三方向关键指标对比")
    r = E.sheet_title(ws, "01 · 三方向关键指标对比（中性情景 · 20 年）", "金额单位：万元", 14)
    r = E.hdr(ws, r, ["指标","方向一 沿用皇冠","方向二 洲至奢选","方向三 外部奢牌","口径/说明"], [26,18,18,18,50])
    D = {k: results[(k,"中性")] for k in ("D1","D2","D3")}
    rows = [
      ("品牌档位", V.DIRECTIONS["D1"]["tier_tag"], V.DIRECTIONS["D2"]["tier_tag"], V.DIRECTIONS["D3"]["tier_tag"], "第四部分分级"),
      ("改造后房量（可售）", V.DIRECTIONS["D1"]["rooms_sellable"], V.DIRECTIONS["D2"]["rooms_sellable"], V.DIRECTIONS["D3"]["rooms_sellable"], "方向二/三：3 改 2 至 268 间（品牌方 F2-29 明确 40㎡+）"),
      ("目标 ADR（元）", V.DIRECTIONS["D1"]["adr"], V.DIRECTIONS["D2"]["adr"], V.DIRECTIONS["D3"]["adr"], "方向三对标 STR 春熙路—太古里商圈 1,280"),
      ("总投资 CAPEX", D["D1"]["capex"], D["D2"]["capex"], D["D3"]["capex"], "全维度明细见各方向 03_CAPEX明细"),
      ("停业月数", D["D1"]["closure_months"], D["D2"]["closure_months"], D["D3"]["closure_months"], "关键路径推算"),
      ("停业期损失", D["D1"]["closure_total"], D["D2"]["closure_total"], D["D3"]["closure_total"], "⭐ 按 24 个月实测逐月曲线 × 固定成本 284 万/月"),
      ("稳定年总营收", D["D1"]["rev_y5"], D["D2"]["rev_y5"], D["D3"]["rev_y5"], "Y3–Y5 均值"),
      ("稳定年 GOP 率", D["D1"]["gop_rate_y5"], D["D2"]["gop_rate_y5"], D["D3"]["gop_rate_y5"], "USALI 部门制加权"),
      ("稳定年品牌费率", 0.090, 0.103, 0.171, "HMA 分解后合计占营收比"),
      ("稳定年业主 GOP", D["D1"]["owner_gop_y5"], D["D2"]["owner_gop_y5"], D["D3"]["owner_gop_y5"], "GOP − 品牌费用合计"),
      ("⭐ IRR（20 年）", ("%.2f%%" % (D["D1"]["irr"]*100)) if D["D1"]["irr"] else "无可解", ("%.2f%%" % (D["D2"]["irr"]*100)) if D["D2"]["irr"] else "无可解", ("%.2f%%" % (D["D3"]["irr"]*100)) if D["D3"]["irr"] else "无可解", "⭐ 未含改造后融资年利息（P0 待补）"),
      ("NPV @8%", D["D1"]["npv"], D["D2"]["npv"], D["D3"]["npv"], "折现率 8%（国资口径，待集团确认）"),
      ("静态回收期（年）", ("%.1f" % D["D1"]["payback"]) if D["D1"]["payback"] else "未回收", ("%.1f" % D["D2"]["payback"]) if D["D2"]["payback"] else "未回收", ("%.1f" % D["D3"]["payback"]) if D["D3"]["payback"] else "未回收", ""),
      ("⭐ 分期开业 IRR", "不适用（不换牌，仍需全停）", ("%.2f%%" % (E.run_monthly("D2","中性",20,231.4,12,phased=E.PHASED["D2"])["irr"]*100)), ("%.2f%%" % (E.run_monthly("D3","中性",20,231.4,12,phased=E.PHASED["D3"])["irr"]*100)), "⭐ 条件：消防审查机构认可分区验收（R-01）"),
      ("⭐ 分期开业 停业损失", "—", E.run_monthly("D2","中性",20,231.4,12,phased=E.PHASED["D2"])["closure_total"], E.run_monthly("D3","中性",20,231.4,12,phased=E.PHASED["D3"])["closure_total"], "较一次全停业分别减少 6,857 / 6,761 万"),
      ("规划节点符合性", "✅ 2029Q3 开业（提前）", "✅ 2030Q1 开业（对齐 2030）", "⚠️ 2030Q3 开业（已过 2030）", "规划：2027 决策开工 / 2030 完成改造重新开业"),
    ]
    for i, rw in enumerate(rows):
        fills = [None]*5
        if i >= 10:
            fills[0] = FILLOK if (i in (10,) and rw[1] not in ("无可解",)) else None
        r = E.put(ws, r, list(rw), fills=fills)
    # 02 情景矩阵
    ws = wb.create_sheet("02_三情景矩阵")
    r = E.sheet_title(ws, "02 · 三方向 × 三情景（20 年）", "保守 / 中性 / 乐观；IRR 与 NPV @8%", 8)
    r = E.hdr(ws, r, ["方向","情景","CAPEX","停业损失","Y5 营收","业主GOP","IRR","NPV@8%"], [24,10,14,14,14,14,12,14])
    for k in ("D1","D2","D3"):
        for sc in ("保守","中性","乐观"):
            res = results[(k,sc)]
            f = FILLOK if (sc=="中性") else None
            r = E.put(ws, r, [k+" "+V.DIRECTIONS[k]["tier_tag"], sc, res["capex"], res["closure_total"],
                              res["rev_y5"], res["owner_gop_y5"],
                              ("%.2f%%" % (res["irr"]*100)) if res["irr"] else "无可解", res["npv"]],
                    fmts=[None,None,"#,##0","#,##0","#,##0","#,##0",None,"#,##0"], fills=[f]*8)
    # 03 开工月份
    ws = wb.create_sheet("03_开工月份敏感性")
    r = E.sheet_title(ws, "03 · 开工月份 × 停业月数 → 停业期总损失矩阵", "⭐ 12 月为全年唯一亏损月（毛利率 −0.7%）→ 停业即止损；绿色=该停业月数下最省", 13)
    r = E.hdr(ws, r, ["开工月"] + ["%d月" % d for d in range(12, 23)], [10]+[10]*11)
    for st in range(1,13):
        vals=[st]; fills=[None]
        for d in range(12,23):
            _, t = V.closure_loss(st, d, 231.4); vals.append(t)
        for d in range(12,23):
            best = min(V.closure_loss(s2,d,231.4)[1] for s2 in range(1,13))
            worst = max(V.closure_loss(s2,d,231.4)[1] for s2 in range(1,13))
            fills.append(FILLOK if vals[d-11]==best else (FILLBAD if vals[d-11]==worst else None))
        r = E.put(ws, r, vals, fmts=[None]+["#,##0"]*11, fills=fills)
    r += 1
    ws.cell(row=r, column=1, value="⭐ 读法：固定停业月数下，开工月份的价值有限（如 18 月口径仅 456 万）；⭐ 真正的量级来自『开工月份 × 停业月数』的组合选择 —— 12 月开工 + 尽可能短的停业期，是唯一能把停业损失压到最低的路径。").font = Font(bold=True, color="C00000")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=13)
    # 04 国资门槛
    ws = wb.create_sheet("04_国资门槛达标表")
    r = E.sheet_title(ws, "04 · 国资体系口径校验（三方向）", "依据《中央企业投资监督管理办法》（年度投资计划备案 + 负面清单分类监管）+ 国有资产评估项目备案制", 7)
    r = E.hdr(ws, r, ["校验项","方向一","方向二","方向三","阈值/要求","说明","数据等级"], [26,16,16,16,20,54,12])
    def ok(x): return "达标" if x else "不达标"
    D = {k: results[(k,"中性")] for k in ("D1","D2","D3")}
    irr_ok = {k: (D[k]["irr"] is not None and D[k]["irr"] >= V.GOV["irr_floor"]) for k in D}
    pb_ok = {k: (D[k]["payback"] is not None and D[k]["payback"] <= V.GOV["payback_max_years"]) for k in D}
    checks = [
      ("项目 IRR ≥ 8%", [("%s（%s）" % (("%.2f%%" % (D[k]["irr"]*100)) if D[k]["irr"] else "无", ok(irr_ok[k]))) for k in ("D1","D2","D3")], "≥8%",
       "⭐ 未含改造后融资年利息（P0）—— 计入后三方向 IRR 全部下降，须以集团口径最终确认", "⚠️ 待确认"),
      ("静态回收期 ≤ 15 年", [("%s（%s）" % (("%.1f 年" % D[k]["payback"]) if D[k]["payback"] else "未回收", ok(pb_ok[k]))) for k in ("D1","D2","D3")], "≤15 年",
       "国资体系对长周期回报项目通常容忍更长回收期；阈值为讨论用参数", "⚠️ 待确认"),
      ("『做减法』符合国资导向", ["✅ 415→402 间（不减房）","✅ 415→268 间（−35%）","✅ 415→268 间（−35%）"], "避免超标准建设",
       "⭐⭐ 同投资额下提升单间品质与坪效，而非扩大规模 —— 减房是国资导向下的最优解，不是缩水", "🟠 推算"),
      ("主业契合度", ["✅ 主业酒店资产","✅ 主业酒店资产","✅ 主业酒店资产"], "主业投资",
       "换牌为委托/特许经营，不新增非主业投资；不涉及金融或资金方案", "🟢 官方"),
      ("投资计划备案", ["待列入","待列入","待列入"], "年度投资计划备案管理",
       "⭐ 规划六家改造项目总投资约 4.01 亿元、分两批实施、2029 年全部投运 → 总府额度与批次须集团明确", "⚠️ 待确认"),
      ("资产评估备案", ["待办","待办","待办"], "评估项目备案 + 报告审核",
       "⭐ 存量房产正式评估值 + 土地剩余年限（P0）；减房后评估口径（按可售房量还是建面）须与评估机构对齐", "⚠️ 待确认"),
      ("负债与融资约束", ["待办","待办","待办"], "资产负债率 ≤70%",
       "⭐ 前期已标注『改造后融资年利息』为最大低估项", "⚠️ 待确认"),
      ("负面清单核查", ["待办","待办","待办"], "禁止类 / 特别监管类",
       "⭐ 需以集团投资管理口径正式出具结论；本表非最终意见", "⚠️ 待确认"),
    ]
    for nm, vals, thr, note, lvl in checks:
        fills = [None]*7
        for i, v in enumerate(vals):
            fills[i+1] = FILLOK if "达标" in str(v) else (FILLBAD if "不达标" in str(v) else FILLWARN)
        r = E.put(ws, r, [nm]+list(vals)+[thr, note, lvl], fills=fills)
    # 05 数据源
    ws = wb.create_sheet("05_数据源与口径")
    r = E.sheet_title(ws, "05 · 数据源、口径与模型边界", "⭐ 本表是上会材料的防错清单：任何数字必须能追到来源", 4)
    r = E.hdr(ws, r, ["类别","内容","来源","数据等级"], [18,64,48,12])
    srcs = [
      ("季节性曲线","24 个月逐月营收/ADR/出租率/餐饮占比/会议占比（2024/10–2026/09）","业主《近24个月总府皇冠假日酒店主要经营指标》","🟢 实测"),
      ("客房底数","名义 415 / 在建 402 / ★正常售卖 351（颜色还原）；客房层建筑 22,645.47 ㎡","工程部《楼层房间数量表》+《房间分布表》+ 财务可售间夜互证","🟢 实测"),
      ("品牌意向","两条路径：①全新一代摩登时尚皇冠假日（不改变现有结构）②洲至奢选（需 3 改 2 或套内 40㎡+）","洲际方《换牌品牌建议》+《F2-29 沟通纪要》","🟢 品牌方一手"),
      ("品牌费用结构","base/incentive/marketing/loyalty/reservation/IT/training/FFE/pre-opening 九项分解 + 行业指示区间","Hotel Development Guide (Darren Blanchard, 2026-10) + F2-29","🔵 行业机构"),
      ("市场基准","五星级 736 家 OCC 62.5% / ADR 755；春熙路—太古里 12 家 ADR 1,280 OCC 76.3% RevPAR 977；全国奢华 OCC 72.3% ADR 985","文旅部 2025 公报 / 浩华 / 戴德梁行 / STR","🔵 行业机构"),
      ("国资口径","年度投资计划备案 + 负面清单分类监管 + 资产评估项目备案制","《中央企业投资监督管理办法》、国资委评估备案通知","🟢 官方"),
      ("停业期损失","收入损失用实测历月营收 + 固定成本 284 万/月 + 品牌方保留费","实测经营数据 + 品牌合同惯例","🟢/🟠"),
      ("⚠️ 未纳入项","改造后融资年利息（P0）｜存量房产评估值与土地年限（P0）｜改造后部门 GOP 率（P0）｜『营业现金毛流量』定义口径","三项 P0 待补","⚠️ 待确认"),
      ("⚠️ 模型边界","未含通胀与名义价格曲线（模型为不变价）｜未含土地增值税与契税（评估值确定后另算）｜未含分年度限售与分红政策｜未含汇率（特许结算币种待定）","本表声明", "⚠️ 声明"),
    ]
    for s in srcs:
        r = E.put(ws, r, list(s), fills=[None,None,None,FILLWARN if "待确认" in s[3] or "声明" in s[3] else None])
    p = os.path.join(OUT, "总府皇冠改造_立项经济测算_三方向对比与国资口径校验_v1.0_2026-11-08.xlsx")
    wb.save(p)
    return p

if __name__ == "__main__":
    results = {}
    for k in ("D1","D2","D3"):
        for sc in ("保守","中性","乐观"):
            results[(k,sc)] = E.run_monthly(k, sc, 20, 231.4, V.DIRECTIONS[k]["closure_start_month"])
    names = {"D1":"方向一_沿用皇冠","D2":"方向二_洲至奢选","D3":"方向三_外部奢华品牌"}
    for k in ("D1","D2","D3"):
        p = E.export_direction(k, results[(k,"中性")], "总府皇冠改造_立项经济测算_%s_全维度_v1.0_2026-11-08.xlsx" % names[k])
        # 追加两个 sheet
        from openpyxl import load_workbook
        wb = load_workbook(p)
        add_timeline_sheet(wb, k); add_nonstop_sheet(wb, k)
        wb.save(p)
        print("OK", os.path.basename(p))
    p = build_comparison(results)
    print("OK", os.path.basename(p))
