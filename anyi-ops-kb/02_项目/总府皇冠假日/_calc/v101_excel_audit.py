# -*- coding: utf-8 -*-
"""v101：测算附表 Excel（十张表）＋ 正文自审"""
import json, os, io, sys, re
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

sys.stdout.reconfigure(encoding="utf-8")
T = r"D:\B166ER-openclaw\workspace\.tmp"
KB = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\总府皇冠假日"
TGT = r"C:\Users\ericz\Desktop\产业发展部\旗下酒店\总府皇冠假日酒店"
CAL = os.path.join(TGT, "测算与中间产物")
os.makedirs(CAL, exist_ok=True)
XLSX = os.path.join(CAL, "总府皇冠改造_可行性研究报告_测算附表_v6.0_2026-11-15.xlsx")
D = json.load(open(os.path.join(T, "v98.json"), encoding="utf-8"))
B, R, S, BE, PATHS = D["base"], D["results"], D["sensitivity"], D["breakeven"], D["paths"]
KS = ["P1", "P2", "P3", "P4"]

HD = PatternFill("solid", fgColor="1F4E5F")
HD2 = PatternFill("solid", fgColor="2E6E8E")
SUB = PatternFill("solid", fgColor="DCE6EC")
TOT = PatternFill("solid", fgColor="F3E6C8")
WHT = Font(color="FFFFFF", bold=True, size=10)
B10 = Font(bold=True, size=10)
N10 = Font(size=10)
THIN = Side(style="thin", color="B0BEC5")
BD = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

wb = Workbook(); wb.remove(wb.active)

def sheet(name, headers, rows, widths=None, note=None, freeze="A2"):
    ws = wb.create_sheet(name)
    r0 = 1
    if note:
        ws.cell(1, 1, note).font = Font(size=9, italic=True, color="555555")
        ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=max(3, len(headers)))
        r0 = 2
    for j, h in enumerate(headers, 1):
        c = ws.cell(r0, j, h); c.fill = HD; c.font = WHT
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BD
    for i, row in enumerate(rows, r0 + 1):
        isTot = str(row[0]).startswith("合计") or str(row[0]).startswith("小计")
        for j, v in enumerate(row, 1):
            c = ws.cell(i, j, v)
            c.font = B10 if isTot else N10
            c.border = BD
            if isinstance(v, (int, float)):
                c.number_format = '#,##0.00' if abs(v) < 10000 else '#,##0'
                c.alignment = Alignment(horizontal="right", vertical="center")
            else:
                c.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
            if isTot: c.fill = TOT
    for j, w in enumerate(widths or [22] * len(headers), 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.freeze_panes = ws.cell(r0 + 1, 1)
    ws.row_dimensions[r0].height = 30
    return ws

# 01 改造前基线
rows = [
    ["营业收入（万元，口径A 含服务费）", 7948, 7937, 7099.54, 6442.73, 5403.53, "业主资料(2)；近24个月经营指标；2026年10月利润表"],
    ["同比", None, -0.0014, -0.1055, None, -0.1173, "2026年1-10月同比"],
    ["经营毛利润（万元）", 1504, 1506, 1580.64, None, 1393.90, "台账加总，与业主口径差63.64万，采用台账值"],
    ["净营业利润（万元）", None, None, None, None, -416.51, "2026年1-10月，扣奖励管理费与非经营性费用后"],
    ["平均房价（元，含服务费）", None, None, 435.95, 412.09, 428.50, "近24个月均值427.42"],
    ["出租率", None, None, 0.7410, 0.7253, 0.8245, "近24个月均值72.55%"],
    ["每间可售房收入（元）", None, None, 323.04, 298.70, 353.30, "近24个月均值310.07"],
    ["客房收入（万元）", None, None, 4740.4, 4387.7, None, "口径A"],
    ["餐饮收入（万元）", None, None, 879.6, 901.9, None, "口径A"],
    ["会议收入（万元）", None, None, 1005.3, 823.4, None, "口径A"],
    ["其它收入（万元）", None, None, 474.9, 329.7, None, "口径A"],
    ["非房收入占比", None, None, 0.3323, 0.3190, None, "FY2025／滚动12个月"],
    ["人工成本（万元，年化）", None, None, 2530.0, 2269.4, 2184.1, "2026年1-10月1820.08万×1.2"],
    ["能耗成本（万元，年化）", None, None, 572.3, 548.6, 525.2, "P&L Energy"],
    ["维保成本（万元）", None, None, 183.81, 145.70, None, "口径A全口径；合同类2026年43.72万"],
    ["洲际许可费（万元，年化）", None, None, None, 121.56, None, "总收入×2.00%"],
    ["奖励管理费（万元，年化）", None, None, None, 83.63, None, "(洲际GOP−许可费)×5.00%（最低档）"],
    ["利息等非经营性费用（万元，年化）", None, None, 2088.85, 2088.85, 2088.85, "月均174.07万，存量债务60677万刚性"],
    ["折旧摊销（万元）", 722, 711, 387.0, None, None, "业主口径；2025年降幅45.6%无台账"],
    ["客房数（间）", None, None, 402, 402, 402, "面积台账415间；在售402间三方一致"],
    ["总府历年营业收入（万元）", 7948, 7937, 7100, None, 5403.53, "2023/2024/2025/2026年1-10月"],
]
sheet("01 改造前基线", ["指标", "2023年", "2024年", "2025年", "滚动12个月", "2026年1-10月", "口径与来源"],
      rows, [30, 12, 12, 14, 14, 15, 42],
      note="口径A=业主台账含服务费；口径B=利润表不含服务费；台账客房收入＝口径B客房收入×1.10（已验证）")

# 02 面积要求与房量
rows = [["客房套内总面积（㎡）", 10192.0, "刚性约束"],
        ["现状单间套内（㎡）", 25.35, "10192÷402＝25.35，现存建筑无移卫耦合折损"],
        ["移卫耦合折损系数（改造后）", 1.08, "新品牌标准重做时计入"],
        ["现状在售房量（间）", 402, "实测"]]
for n, a, s_ in [("皇冠 2026 标准 ≥35㎡", 35, "品牌建造设计标准 [958140]/[958148]"),
                 ("洲至奢选 洲际方条件 ≥40㎡", 40, "F2-29 沟通纪要"),
                 ("洲至奢选 实测基础房 45㎡", 45, "成都棕榈泉房型实测"),
                 ("康莱德 46㎡", 46, "异地代理样本"),
                 ("尼依格罗 50㎡", 50, "本地实测"),
                 ("丽晶/LXR 60㎡", 60, "品牌标准"),
                 ("瑞吉 65㎡", 65, "本地实测")]:
    theo = int(10192 / a); prac = int(10192 / (1.08 * a))
    rows.append(["%s 理论上限（间）" % n, theo, "%s；按1.08折损实操 %d 间" % (s_, prac)])
rows += [["路径二 洲至奢选基准房量（间）", 209, "按45㎡×1.08折损"],
         ["路径三 外部品牌基准房量（间）", 205, "按康莱德46㎡×1.08折损"],
         ["路径一 维持房量（间）", 402, "不减房；但不满足皇冠2026标准≥35㎡"]]
sheet("02 面积要求与房量", ["项目", "数值", "说明"], rows, [34, 14, 52],
      note="客房套内总面积 10,192 ㎡ 为刚性约束；减房是整体改造路径的核心代价")

# 03 分路径投资明细
allkeys = []
for k in KS:
    for kk in PATHS[k]["capex_split"]:
        if kk not in allkeys: allkeys.append(kk)
rows = []
for kk in allkeys:
    r = [kk]
    for k in KS:
        r.append(PATHS[k]["capex_split"].get(kk, 0))
    rows.append(r)
rows.append(["合计"] + [PATHS[k]["capex"] for k in KS])
rows.append(["业主承担比例"] + [1.0, 1.0, 1.0, 1.0])
rows.append(["注：合同第1(c)条 业主应提供酒店改造所需全部资金；路径二至路径四在公共必选工程9,884万元基础上增加客房、公区、后场、智能化与品牌工程"])
sheet("03 分路径投资明细", ["费用项（万元）", "路径一", "路径二", "路径三", "路径四"], rows, [46, 14, 14, 14, 14],
      note="投资估算为产业发展部测算，待第三方工程量清单核定后定稿；锚点：2024年专题报告工程费18,000万元、2019年PIP初步造价18,000—20,000万元")

# 04 达产经营测算
items = [("房量（间）", "rooms"), ("平均房价（元，不含服务费）", "adr"), ("出租率", "occ"),
         ("达产每间可售房收入（元，含服务费）", "revpar_A"), ("客房收入（万元）", "room_rev_A"),
         ("非房收入（万元）", "nonroom_rev_B"), ("营业收入合计（万元）", "rev_A_stable"),
         ("较改造前基线7,099.54万元（万元）", "vs_base_rev_A"), ("营业毛利润（万元）", "gop"),
         ("未分摊成本（万元）", "undist"), ("洲际集团口径营业毛利润（万元）", "ihg_gop"),
         ("品牌与许可费用（万元）", "fee_total"), ("调整后营业毛利润（万元）", "adj_gop"),
         ("达产年经营现金流（万元）", "op_cf_stable"), ("经营现金流占收入比", "op_cf_margin")]
rows = [[lb] + [R[k][key] for k in KS] for lb, key in items]
rows.append(["停业期（月）"] + [R[k]["downtime"] for k in KS])
rows.append(["业主投资（万元）"] + [R[k]["owner_capex"] for k in KS])
rows.append(["停业期净现金流出（万元）"] + [-R[k]["shutdown_cf_total"] for k in KS])
sheet("04 达产经营测算", ["项目", "路径一", "路径二", "路径三", "路径四"], rows, [34, 15, 15, 15, 15],
      note="收入=口径A（含服务费）；成本与利润=口径B（利润表）；两口径1.1006倍可复算桥接")

# 05 现金流与评价
rows = [["业主投资（万元）"] + [R[k]["owner_capex"] for k in KS],
        ["停业期（月）"] + [R[k]["downtime"] for k in KS],
        ["停业期净现金流出（万元）"] + [-R[k]["shutdown_cf_total"] for k in KS],
        ["项目口径净现值（万元）"] + [R[k]["npv"] for k in KS],
        ["内部收益率"] + [R[k]["irr_pct"] / 100 if R[k]["irr_pct"] is not None else None for k in KS],
        ["静态投资回收期（年）"] + [R[k]["payback_yr"] for k in KS],
        ["集团口径：停业期利息流出（万元）"] + [D["group_view"][k]["shutdown_interest_outflow"] for k in KS],
        ["评价期（年）", 20, 20, 20, 20],
        ["折现率", 0.08, 0.08, 0.08, 0.08],
        ["注：项目口径不含存量债务利息（60,677万元、2,088.85万元/年为各路径共同项）"]]
sheet("05 现金流与评价", ["项目", "路径一", "路径二", "路径三", "路径四"], rows, [34, 15, 15, 15, 15],
      note="项目口径 NPV/IRR/静态回收期；评价期20年，折现率8%；敏感性见 06 表")

# 06 敏感性
keys = []
for k in KS:
    for kk in S[k]:
        if kk not in keys: keys.append(kk)
rows = [[kk] + [S[k].get(kk) for k in KS] for kk in keys]
rows.append(["基准净现值"] + [R[k]["npv"] for k in KS])
sheet("06 敏感性分析", ["情景（净现值，万元）"] + ["路径一", "路径二", "路径三", "路径四"], rows,
      [30, 15, 15, 15, 15],
      note="★「平均房价不提升（维持现状）」为最关键情景：路径一由＋3,021万元转为−5,227万元；路径二至路径四对房价与房量极不敏感")

# 07 盈亏平衡约束
rows = [["守住现状客房收入所需每间可售房收入（元）"] + [BE[k]["required_revpar"] for k in KS],
        ["本方案达产每间可售房收入（元）"] + [BE[k]["assumed_revpar"] for k in KS],
        ["差额（元）"] + [BE[k]["gap"] for k in KS],
        ["是否通过"] + ["通过" if BE[k]["pass"] else "不通过" for k in KS],
        ["现状客房收入（万元，口径A）", B["room_A_fy2025"], B["room_A_fy2025"], B["room_A_fy2025"], B["room_A_fy2025"]]]
sheet("07 盈亏平衡约束", ["项目", "路径一", "路径二", "路径三", "路径四"], rows, [36, 15, 15, 15, 15],
      note="减房路径在收入侧并非不可行；不成立的原因是投资额与停业期")

# 08 品牌与费率对照
rows = [["品牌方案", PATHS["P1"]["brand"], PATHS["P2"]["brand"], PATHS["P3"]["brand"], PATHS["P4"]["brand"]],
        ["档次定位", PATHS["P1"]["tier"], PATHS["P2"]["tier"], PATHS["P3"]["tier"], PATHS["P4"]["tier"]],
        ["洲际许可费口径", "总收入×2.00%", "客房收入×5%（特许）", "客房收入×5%（特许）", "自建分销成本约3%"],
        ["奖励管理费", "（洲际GOP−许可费）×5.00%（最低档）", "取消", "取消", "不适用"],
        ["年费率影响（万元）", 0.0, 31.3, 31.3, 0.0],
        ["盈亏平衡营业毛利润率", "不适用", "34.0%—37.1%", "34.0%—37.1%", "不适用"],
        ["近24个月越过该水平月数", "不适用", "3个月", "3个月", "不适用"],
        ["洲际方书面记录", "维持现状合同", "可换牌并可申请豁免违约金；名称可商榷保留；同意分期不停业", "无", "无"],
        ["正式无异议函", "不适用", "未取得（现有载体为沟通纪要）", "不适用", "不适用"],
        ["客史与会员留存", "全部保留", "全部保留（合同附件E 1.4条）", "须从零重建", "须从零重建"],
        ["在蓉品牌空位（2026-11）", "不适用", "成立（棕榈泉2026-01换牌336间为唯一同城先例）", "文华东方、丽晶、尼依格罗、瑞吉均不成立", "不适用"],
        ["品牌方首问必须包含", "不适用", "基础房型最小净面积及卫生间是否计入套内、净宽度最小要求", "同上", "不适用"]]
sheet("08 品牌与费率对照", ["项目", "路径一", "路径二", "路径三", "路径四"], rows, [24, 30, 40, 30, 30],
      note="★费率结构本身不构成路径二的经济理由；路径二的经济理由必须来自房价与出租率，而房价提升的代价是房量削减")

# 09 停业期参数
rows = [["保留在岗人数（人）", 52, 52, 52, 52, "业主《实施改造期间人员方案测算》"],
        ["人房比（按各路径房量）", 0.13, 0.25, 0.25, 0.25, "房量减少后人房比上升"],
        ["保留在岗人工成本（万元/月）", 109.34, 109.34, 109.34, 109.34, "含社保公积金与工会会费；停业期不另计离职补偿"],
        ["方案一 全年工资（万元）", 1312.08, 1312.08, 1312.08, 1312.08, "第1个月按合同约定，第2-12月按成都市最低工资"],
        ["方案二 全年工资（万元）", 1200.71, 1200.71, 1200.71, 1200.71, "第2-12月按最低工资70%"],
        ["维保合同类固定支出（万元/月）", 3.64, 3.64, 3.64, 3.64, "2026年合同台账43.72万元/年"],
        ["最低运行能耗（万元/月）", 10.94, 10.94, 10.94, 10.94, "安保、保留设备、防冻、消防；无停业期实测值"],
        ["管理费与品牌费（万元/月）", 17.10, 17.10, 17.10, 17.10, "合同原件未提供，是否可减免无法确认，保守按常计取"],
        ["免租可能性", "不适用", "不适用", "不适用", "不适用", "物业业主自持，外部租金＝0，无免租空间"],
        ["停业期利息刚性（万元/月）", 174.07, 174.07, 174.07, 174.07, "存量债务60,677万元"],
        ["停业期月数", 8, 26, 30, 30, "A2 工期基线：路径一6—9月；路径二18—24月＋开业准备3—6月；路径三24—36月"],
        ["复业爬坡期（月）", 6, 6, 6, 6, "爬坡系数0.45→0.85；台账无同店停业复业先例"],
        ["停业期净现金流出（万元）"] + [-R[k]["shutdown_cf_total"] for k in KS] + ["人工＋维保＋最低能耗"],
        ["集团口径停业期利息流出（万元）"] + [D["group_view"][k]["shutdown_interest_outflow"] for k in KS] + ["各路径共同项"]]
sheet("09 停业期参数", ["参数", "路径一", "路径二", "路径三", "路径四", "来源与说明"], rows,
      [28, 14, 14, 14, 14, 46],
      note="停业期损失测算参数；★消防分批验收不可行，全部路径按整体验收、整体开业测算")

# 10 审批与产权约束
rows = [["人防工程", "地下空间是否按人防标准配置、竣工资料、是否已备案", "未查找到相关资料", "全部路径", "基准取保持现状不动并补齐资料；如要求功能腾挪增加800—1,500万元并延长工期"],
        ["消防验收", "1998-08-07《建筑工程消防验收意见书》合格，但要求改建后向原审核机构重新审核", "业主无任何改造后重新审核文件", "全部路径", "改造设计完成后一并申报；档案室补齐竣工图纸"],
        ["载客量与房量", "无消防验收时载客量、核定房量历史文件", "未查找相关资料", "全部路径", "房量与载客量变更审批可行性须向主管部门确认"],
        ["供电", "主供线6500KVA（荔川线925#）／备用线3250KVA（平院线904#经沙帽街电子大厦开关站）", "双路＋应急发电机", "全部路径", "备电容量与1600kW发电机组油箱须按品牌标准复核"],
        ["特种设备-电梯", "14台（缺12#、13#），1996年投运，9#故障频繁", "登记证齐备但14页文件中无一份定期检验报告", "全部路径", "立即补做定期检验后再定更换范围"],
        ["特种设备-锅炉", "4台真空相变热水锅炉，2009-12投用，设计15年，已服役16年9个月", "是否属特种设备待检验机构认定", "全部路径", "若属特种设备则登记与定期检验为强制项"],
        ["结构", "无既有结构安全鉴定报告、无沉降与裂缝观测记录、无加固历史", "酒店目测未发现建筑结构问题", "全部路径", "3改2须专业机构设计核定；无结构结论无法出图"],
        ["风貌与限高", "是否涉及历史建筑、风貌保护、临街界面管控、高度与立面限制", "未见具体限制文件", "全部路径", "按无限制处理，但须建管部门书面确认"],
        ["停车", "停车位配建指标与实际数量、大巴停靠条件", "未固定大巴车位", "全部路径", "换牌后大巴需求须纳入交通评估"],
        ["抵押", "2026年假日酒店大楼抵押20,000万元给兴业银行成都分行", "评估时点2025-09-04尚未设押", "全部路径", "产权状态变更须先获抵押权人书面同意"],
        ["土地", "划拨性质，住宿餐饮用地，分摊8,512.43㎡，共用宗", "评估函载明分割后不能独立使用", "全部路径", "需补缴土地出让金；路径三只能整体品牌合作"],
        ["经营管理合同", "2019-09-28至2029-09-27，到期不续约", "P6项下管理人享有单方解除权", "全部路径", "底线整改后主动提交PIP完成计划与节点，化解解除权风险"],
        ["合同附件A 7.10", "翻新改造期间照常营业区域的所有消防人身安全系统务必能正常使用", "与分期改造不停业互斥", "全部路径", "分期施工、整体验收、分期开业"],
        ["八部门审批对接", "规划、住建、消防、人防、供电、环保、市场监管、文旅", "业主《报建与审批限制》表全部空白", "全部路径", "投资决策前逐项对接，结论可能改变路径选择"]]
sheet("10 审批与产权约束", ["事项", "现状事实", "缺口或结论待核", "适用范围", "应对措施"], rows,
      [18, 44, 30, 12, 48],
      note="★第三方安全检测评估结论尚未出具，涉及「是否必须整改」的最终判定以该评估报告为准")

wb.save(XLSX)
print("Excel:", XLSX, round(os.path.getsize(XLSX) / 1024), "KB", len(wb.sheetnames), "sheets")

# ══════════ 正文自审 ══════════
MD = os.path.join(KB, "总府皇冠改造_可行性研究报告_v6.0_2026-11-15.md")
s = io.open(MD, encoding="utf-8").read()
print("\n=== 正文自审 ===")
EMO = ("[" + chr(92) + "U0001F300-" + chr(92) + "U0001FAFF" + chr(92) + "U00002600-" + chr(92) + "U000027BF"
       + chr(92) + "U00002B50" + chr(92) + "uFE0F" + chr(92) + "u200D" + chr(92) + "u2764" + chr(92) + "u2B06"
       + chr(92) + "u2B07" + chr(92) + "u2B05" + chr(92) + "u274C" + chr(92) + "u2705" + chr(92) + "u26A0"
       + chr(92) + "u26A1" + chr(92) + "u2139" + chr(92) + "u24C2" + chr(92) + "u2B55]")
print("emoji:", len(re.findall(EMO, s)), "｜★:", s.count("★"), "｜☆:", s.count("☆"))
# 表格空单元格
lines = s.split("\n")
intbl = False; blank = 0; ntab = 0
for l in lines:
    if l.strip().startswith("|"):
        if not intbl: intbl = True; ntab += 1; continue
        cells = [c.strip() for c in l.strip().strip("|").split("|")]
        if all(re.match(r"^:?-{2,}:?$", c or "-") for c in cells): continue
        for c in cells:
            if c == "": blank += 1
    else:
        intbl = False
print("表格数:", ntab, "｜空白单元格:", blank)
# 目录 vs 正文
m = re.search(r"^## 目录\n", s, re.M)
ls = s[m.end():].split("\n")
start = next((i for i, l in enumerate(ls) if l.startswith("## ")), None)
toc = [re.sub(r"^\d+\.\s", "", l).strip() for l in ls[:start] if re.match(r"^\d+\.\s", l)]
bod = [l[3:].strip() for l in ls[start:] if l.startswith("## ")]
print("目录↔正文:", toc == bod, "（目录 %d / 正文 %d）" % (len(toc), len(bod)))
if toc != bod:
    for i in range(max(len(toc), len(bod))):
        a = toc[i] if i < len(toc) else "—"; b = bod[i] if i < len(bod) else "—"
        if a != b: print("   差异 %d: 目录=%s ｜ 正文=%s" % (i + 1, a, b))
figs = re.findall(r"!\[([^\]]*)\]\(([^)]+)\)", s)
print("图引用:", len(figs))
for cap, rel in figs:
    p = rel if os.path.isabs(rel) else os.path.join(KB, rel)
    print("   %-46s %s" % (cap[:44], "OK" if os.path.exists(p) else "缺失! " + rel))
# 关键数字命中
KEYS = ["＋3,021", "−19,699", "−22,862", "−24,046", "9.30%", "2.21%", "2.37%", "1.36%",
        "11,066", "21,054", "24,119", "24,340", "6,442.73", "5,403.53", "−416.51",
        "60,914.78", "14,382", "60,677", "2,088.85", "10,192", "25.35", "402 间",
        "1,280", "416.29", "107.90", "989 间", "75,564", "757", "697", "43 次",
        "0.0017", "7.10", "2.1 条", "2029-09-27", "−5,227", "9,884", "209 间", "205 间"]
miss = [k for k in KEYS if k not in s]
print("关键值缺失:", miss if miss else "无（%d 项全中）" % len(KEYS))
print("字数:", len(s), "｜字符:", len(s))
