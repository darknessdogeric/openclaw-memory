# -*- coding: utf-8 -*-
"""一企一策分析范式 · 空白模板生成器 v1.0"""
import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, FormulaRule

OUT = r"C:\Users\ericz\Desktop\一企一策分析表_空白模板_v1.0_2026-11-11.xlsx"
FONT = '等线'
NAVY = '1F3864'
GREY = 'F2F2F2'
YELL = 'FFF2CC'
RED = 'FFC7CE'
ORNG = 'FFE0B2'
GRN = 'D9EAD3'

thin = Side(style='thin', color='BFBFBF')
BD = Border(left=thin, right=thin, top=thin, bottom=thin)

wb = openpyxl.Workbook()

# ============ 字段定义（32 列：原 27 + 新增 5）============
COLS = [
    ("序号", 6), ("公司名称", 18), ("管理建议", 34), ("注册资本", 11), ("实缴资本", 11),
    ("资产总额", 12), ("负债总额", 12), ("有息负债", 11), ("财务费用", 11), ("资产负债率", 11),
    ("净资产", 12), ("累计损益", 12), ("出售价格", 11), ("出租价格", 11), ("营业收入", 11),
    ("EBITDA", 11), ("员工人数", 10), ("人工成本", 11), ("折旧摊销", 11), ("利润总额", 11),
    ("净利润", 11), ("ROE", 10), ("股东回报要求", 12), ("股东投资损益", 12), ("经营现金流", 12),
    ("房产面积", 11), ("土地面积", 11),
    ("处置优先级", 10), ("策略代码", 12), ("牵头主体", 16), ("关键节点", 16), ("下一步动作", 30),
]
NOTE = [
    "序号", "主体全称", "策略词典 12 类之一，须含动作与条件", "万元", "万元", "万元", "万元",
    "万元", "万元/年", "=负债/资产，自动", "万元", "万元", "万元", "万元/年", "万元", "万元",
    "人", "万元", "万元", "万元", "万元", "=净利/净资产，净资产≤0 显示 N/A", "%", "万元",
    "万元", "㎡", "㎡", "自动：1 最高", "S01-S12", "责任部门＋责任人", "日期", "可执行的一句话",
]
# 计算列（数据区第 4 行起）
CALC = {
    "J": "=IF(F{0}=\"\",\"\",G{0}/F{0})",
    "V": "=IF(K{0}<=0,\"N/A\",U{0}/K{0})",
    "AB": "=IFERROR(ROUND(ABS(IF(K{0}<0,K{0},0)+L{0}),0),0)",
    "AC": "=IF(AND(ISNUMBER(P{0}),ISNUMBER(I{0}),I{0}<>0),ROUND(P{0}/I{0},2),\"\")",
    "AD": "=IF(AND(ISNUMBER(M{0}),ISNUMBER(N{0}),N{0}<>0),ROUND(M{0}/N{0},1),\"\")",
    "AE": "=IF(AND(ISNUMBER(M{0}),ISNUMBER(N{0}),N{0}<>0),ROUND(N{0}/M{0},1),\"\")",
}

STRATEGY = [
    ("S01", "集团与本部定位", "不适用（合并或本部口径）", "现金流优先／轻重分离／标杆打造；股东回报、资产价值最大化、资本运营", "本部董事会"),
    ("S02", "破产重整与及时止损", "资产负债率>1 且累计损益巨大且无自我造血", "破产重整；增量投入的每一分钱都是保命钱的浪费", "战投条线＋法务"),
    ("S03", "关停清算与注销退出", "资不抵债且无存续价值", "停业、清算、注销；员工分流安置同步完成", "资产经营条线"),
    ("S04", "闲置资产出租优先、其次出售", "营业收入≈0 或无经营团队", "闲置，优先出售，出售先出租，能租多少就租多少", "资产经营条线"),
    ("S05", "优先出租还债", "EBITDA<财务费用（利息覆盖不足）", "优先出租；租金不能覆盖利息则出售还债", "资产经营条线"),
    ("S06", "人资分离、本部统一管资产", "小体量、资产少、人员少", "人资分离，由本部统一管理资产出租或资产出售", "本部＋人力"),
    ("S07", "及时改造，打造自营标杆", "净资产为正、资产负债率健康、资产规模与区位值得自营", "及时改造，打造自营标杆", "产发部＋运管"),
    ("S08", "分年度经营转正路线图", "经营可持续但短期未达标", "2027年GOP转正→2028年经营现金流转正→2029年利润总额转正→2030年ROE 3.5%", "产发部＋运管"),
    ("S09", "存量资产盘活与对外转让", "有土地房产、可持续经营无必要", "挂牌出让、附条件挂牌出租、改造运营、资产合作", "资产经营条线"),
    ("S10", "品牌与运营输出（轻资产）", "有品牌与管理体系、无需自投", "自营轻资产管理平台；品牌授权与委托管理输出", "产发部"),
    ("S11", "止损且不新增投入", "经营无改善空间但短期须维持", "止损／退出／出租／关停，不新增投入", "资产经营条线"),
    ("S12", "尽快决策（待定）", "关键数据缺失、出售与出租均未定价", "尽快决策：出租／自营；限期补齐数据", "本部＋产发部"),
]

TREE = [
    ("L0", "主体层级判定", "合并／本部 → 走 S01 定位口径；以下进入 L1", "按合并与本部分别出具建议"),
    ("L1", "是否资不抵债（资产负债率>1）",
     "是 → L1a；否 → L2",
     "资不抵债主体一律不给改造或投入类建议，此为红线"),
    ("L1a", "是否具备自我造血（EBITDA>0 且营业收入>1000）",
     "是 → S05 优先出租还债；否 → L1b",
     "有经营价值但资不抵债的，走出租还债，不走破产重整"),
    ("L1b", "是否具备重整或清算价值",
     "有重大可交易资产（出售价格>0 且显著高于账面）→ S02 破产重整；无 → S03 关停清算注销；小体量 → S06 人资分离",
     "★ 出售价格高、资产可交易的主体不走破产重整，走 S05 或 S09"),
    ("L2", "是否闲置（营业收入<100 或明确无经营团队）",
     "是 → S04 出租优先、其次出售；否 → L3",
     "★ 闲置以营业收入与经营团队判定，不得以 EBITDA 判定——改造标的改造前 EBITDA 必然为负"),
    ("L3", "EBITDA 能否覆盖财务费用（倍数≥1）",
     "否（<1）→ S05 优先出租还债；是 → L4", "倍数须用同一口径的 EBITDA 与财务费用"),
    ("L4", "是否值得自营（净资产>0、资产规模与区位支撑自营、且非资不抵债）",
     "是 → S07 及时改造打造自营标杆；否 → L5",
     "★ S07 前提：资产负债率<1 且净资产为正。资不抵债主体不得给改造建议"),
    ("L5", "经营是否可持续但短期未达标",
     "是 → S08 分年度转正路线图；否 → L6", "转正年度须与集团三年行动节点对齐"),
    ("L6", "是否非酒店主业或职能类公司",
     "是 → S06 人资分离 或 S10 平台定位；否 → L7", "职能与平台类主体不建议给改造类建议"),
    ("L7", "是否集团或本部主体",
     "是 → S01；否 → L8", "本部口径单列，不与子公司合并评价"),
    ("L8", "关键数据是否缺失、买卖均未定价",
     "是 → S12 尽快决策；否 → S09 存量资产盘活与对外转让", "S12 必须同时给出限期补数与决策人"),
]

CHECKS = [
    ("V01", "货币单位", "所有金额列单位为万元，必须在表头或说明页标注", "阻断", "单位混用会导致全部金额失真"),
    ("V02", "资产负债率", "必须由公式计算（负债/资产），不得手工填写", "阻断", "手填易与原始报表不一致"),
    ("V03", "ROE", "净资产≤0 时必须显示 N/A，不得显示为负数或 0", "阻断", "负净资产下 ROE 无经济含义"),
    ("V04", "负净资产主体", "净资产<0 的主体，管理建议必须落在 S02/S03/S04/S05/S06/S11 之一", "阻断", "资不抵债主体不得给改造或投入类建议"),
    ("V05", "资不抵债主体", "资产负债率>1 的主体，不得出现「改造」「投入」「自营」字样", "阻断", "与止损原则直接冲突"),
    ("V06", "管理建议取值", "必须落在策略词典 S01-S12 之内，不得自造表述", "阻断", "自造表述无法统计与对比"),
    ("V07", "处置优先级", "为空时由公式自动生成（负净资产绝对额＋累计亏损）", "提示", "确保高风险主体排在最前"),
    ("V08", "买卖定价主体", "有出售价格或出租价格的，必须同时填牵头主体与关键节点", "提示", "有价无主等于没决策"),
    ("V09", "利息覆盖不足", "EBITDA/财务费用<1 且建议出租的，必须注明「租金不覆盖利息则出售」", "提示", "防止出租方案掩盖偿债缺口"),
    ("V10", "落地三要素", "S07/S08 类建议必须同时填关键节点（日期）与下一步动作", "阻断", "没有节点和动作的建议无法跟踪"),
    ("V11", "改造类建议的前置", "管理建议含「改造」或「标杆」的，资产负债率必须小于 1 且净资产为正", "阻断",
     "华龙宾馆即属此类：资产负债率 203.2%、净资产 -144.66 万元，却给「及时改造，打造自营标杆」，与止损原则直接冲突"),
    ("V12", "闲置判定口径", "闲置以营业收入小于 100 万元或无经营团队判定，不得以 EBITDA 为负判定", "阻断",
     "改造标的在改造前 EBITDA 必然为负，若按 EBITDA 判定将把所有改造类建议误判为闲置"),
]

FIELDS = [
    ("序号", "基础", "主体序号，用于排序与引用", "正整数", "手工"),
    ("公司名称", "基础", "主体工商全称", "文本", "手工"),
    ("管理建议", "决策", "策略词典 12 类之一，须含动作、判定依据与条件句", "下拉＋文本", "下拉"),
    ("注册资本", "资本", "工商登记注册资本", "万元", "手工"),
    ("实缴资本", "资本", "实缴出资额", "万元", "手工"),
    ("资产总额", "资本", "期末资产总额", "万元", "手工"),
    ("负债总额", "资本", "期末负债总额", "万元", "手工"),
    ("有息负债", "债务", "短期借款＋长期借款＋应付债券等计息负债", "万元", "手工"),
    ("财务费用", "债务", "当期财务费用（利息支出为主）", "万元/年", "手工"),
    ("资产负债率", "债务", "负债总额/资产总额", "%", "公式"),
    ("净资产", "资本", "所有者权益合计", "万元", "手工"),
    ("累计损益", "资本", "累计未分配利润（可为负）", "万元", "手工"),
    ("出售价格", "处置", "整体或主要资产处置的评估／报价参考", "万元", "手工"),
    ("出租价格", "处置", "对外出租的年租金参考（按年）", "万元/年", "手工"),
    ("营业收入", "经营", "当期营业收入", "万元", "手工"),
    ("EBITDA", "经营", "息税折旧摊销前利润", "万元", "手工"),
    ("员工人数", "经营", "期末在册人数", "人", "手工"),
    ("人工成本", "成本", "当期人工成本合计", "万元", "手工"),
    ("折旧摊销", "成本", "当期折旧与摊销", "万元", "手工"),
    ("利润总额", "经营", "当期利润总额", "万元", "手工"),
    ("净利润", "经营", "当期净利润", "万元", "手工"),
    ("ROE", "经营", "净利润/净资产；净资产≤0 显示 N/A", "%", "公式"),
    ("股东回报要求", "资本", "股东对回报率或分红的底线要求", "%或万元", "手工"),
    ("股东投资损益", "资本", "股东口径的投资收益或分担", "万元", "手工"),
    ("经营现金流", "经营", "当期经营活动产生的现金流量净额", "万元", "手工"),
    ("房产面积", "资产", "自有房产建筑面积", "㎡", "手工"),
    ("土地面积", "资产", "自有及取得使用权的土地面积", "㎡", "手工"),
    ("处置优先级", "决策", "按负净资产绝对额与累计亏损自动排序，1 最高", "名次", "公式"),
    ("策略代码", "决策", "S01-S12，与管理建议一一对应", "下拉", "下拉"),
    ("牵头主体", "落地", "责任部门＋责任人", "文本", "手工"),
    ("关键节点", "落地", "该主体的下一个硬节点与日期", "文本", "手工"),
    ("下一步动作", "落地", "可执行的一句话动作，含交付物与时点", "文本", "手工"),
]


def style_head(ws, row, ncol):
    for c in range(1, ncol + 1):
        cell = ws.cell(row, c)
        cell.font = Font(name=FONT, size=9, bold=True, color='FFFFFF')
        cell.fill = PatternFill('solid', fgColor=NAVY)
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        cell.border = BD


def build_main():
    ws = wb.active
    ws.title = '一企一策测算表'
    n = len(COLS)
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=n)
    t = ws.cell(1, 1)
    t.value = '安逸酒店集团 一企一策分析表（范式模板 v1.0）　单位：万元 / ㎡ / 人　编制：产业发展部　版本：v1.0　2026-11-11'
    t.font = Font(name=FONT, size=13, bold=True, color='FFFFFF')
    t.fill = PatternFill('solid', fgColor=NAVY)
    t.alignment = Alignment(horizontal='center', vertical='center')
    ws.row_dimensions[1].height = 30

    for i, (name, w) in enumerate(COLS, 1):
        ws.cell(2, i).value = name
        ws.column_dimensions[get_column_letter(i)].width = w
    style_head(ws, 2, n)
    ws.row_dimensions[2].height = 34

    for i, nt in enumerate(NOTE, 1):
        cell = ws.cell(3, i)
        cell.value = nt
        cell.font = Font(name=FONT, size=8, italic=True, color='595959')
        cell.fill = PatternFill('solid', fgColor=GREY)
        cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
        cell.border = BD
    ws.row_dimensions[3].height = 26

    # 公式与格式（数据从第 4 行起，预置 60 行）
    first, last = 4, 63
    for r in range(first, last + 1):
        for col, f in CALC.items():
            ws[col + str(r)] = f.format(r)
        for c in range(1, n + 1):
            cell = ws.cell(r, c)
            cell.font = Font(name=FONT, size=9)
            cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            cell.border = BD
        ws.cell(r, 3).alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
        ws.cell(r, 32).alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
    ws.freeze_panes = 'D4'

    # 数据有效性
    dv = DataValidation(type='list', formula1='=策略词典!$A$2:$A$13', allow_blank=True,
                        showDropDown=False)
    dv.promptTitle = '管理建议'
    dv.prompt = '从策略词典 S01-S12 中选择，管理建议文字须与所选代码一致'
    dv.errorTitle = '取值不合规'
    dv.error = '管理建议必须落在策略词典 S01-S12 之内'
    ws.add_data_validation(dv)
    dv.add('C%d:C%d' % (first, last))

    dv2 = DataValidation(type='list', formula1='=策略词典!$A$2:$A$13', allow_blank=True,
                         showDropDown=False)
    ws.add_data_validation(dv2)
    dv2.add('AC%d:AC%d' % (first, last))

    # 条件格式
    ws.conditional_formatting.add('J%d:J%d' % (first, last),
                                  CellIsRule(operator='greaterThan', formula=['1'],
                                             fill=PatternFill('solid', fgColor=RED)))
    ws.conditional_formatting.add('K%d:K%d' % (first, last),
                                  CellIsRule(operator='lessThan', formula=['0'],
                                             font=Font(name=FONT, size=9, bold=True, color='9C0006')))
    ws.conditional_formatting.add('AD%d:AD%d' % (first, last),
                                  CellIsRule(operator='lessThanOrEqual', formula=['15'],
                                             fill=PatternFill('solid', fgColor=ORNG)))
    ws.conditional_formatting.add('AE%d:AE%d' % (first, last),
                                  CellIsRule(operator='greaterThanOrEqual', formula=['30'],
                                             fill=PatternFill('solid', fgColor=ORNG)))
    ws.conditional_formatting.add('AB%d:AB%d' % (first, last),
                                  FormulaRule(formula=['AND($AB%d="",$K%d<0)' % (first, first)],
                                              fill=PatternFill('solid', fgColor=YELL)))
    return ws


def sheet(name, headers, rows, widths, note_cols=None):
    ws = wb.create_sheet(name)
    for i, h in enumerate(headers, 1):
        ws.cell(1, i).value = h
        ws.column_dimensions[get_column_letter(i)].width = widths[i - 1]
    style_head(ws, 1, len(headers))
    ws.row_dimensions[1].height = 30
    for ri, row in enumerate(rows, 2):
        for ci, v in enumerate(row, 1):
            cell = ws.cell(ri, ci)
            cell.value = v
            cell.font = Font(name=FONT, size=9)
            cell.alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)
            cell.border = BD
            if ri % 2 == 1:
                cell.fill = PatternFill('solid', fgColor=GREY)
    ws.freeze_panes = 'A2'
    return ws


def build_dict():
    rows = [(a, b, c, d, e) for a, b, c, d, e in STRATEGY]
    ws = sheet('策略词典', ['策略代码', '策略名称', '触发条件', '建议句式模板', '通常牵头'],
               rows, [10, 22, 40, 52, 22])
    for r in range(2, len(rows) + 2):
        ws.cell(r, 1).font = Font(name=FONT, size=9, bold=True)
        ws.cell(r, 1).alignment = Alignment(horizontal='center', vertical='top')
    return ws


def build_tree():
    rows = [(a, b, c, d) for a, b, c, d in TREE]
    ws = sheet('判定决策树', ['层级', '判定问题', '分支走向', '执行说明'], rows, [8, 34, 44, 50])
    for r in range(2, len(rows) + 2):
        ws.cell(r, 1).font = Font(name=FONT, size=9, bold=True)
        ws.cell(r, 1).alignment = Alignment(horizontal='center', vertical='top')
    return ws


def build_checks():
    rows = [(a, b, c, d, e) for a, b, c, d, e in CHECKS]
    ws = sheet('数据校验规则', ['编号', '校验项', '规则', '级别', '为什么'], rows, [8, 18, 52, 10, 40])
    for r in range(2, len(rows) + 2):
        ws.cell(r, 4).alignment = Alignment(horizontal='center', vertical='top')
        if ws.cell(r, 4).value == '阻断':
            ws.cell(r, 4).fill = PatternFill('solid', fgColor=RED)
    return ws


def build_fields():
    rows = [(a, b, c, d, e) for a, b, c, d, e in FIELDS]
    ws = sheet('字段口径说明', ['字段', '分组', '口径定义', '单位／类型', '填写方式'], rows, [16, 10, 46, 14, 12])
    for r in range(2, len(rows) + 2):
        ws.cell(r, 5).alignment = Alignment(horizontal='center', vertical='top')
        if ws.cell(r, 5).value == '公式':
            ws.cell(r, 5).fill = PatternFill('solid', fgColor=GRN)
        elif ws.cell(r, 5).value == '下拉':
            ws.cell(r, 5).fill = PatternFill('solid', fgColor=YELL)
    return ws


def build_readme():
    ws = wb.create_sheet('使用说明', 1)
    ws.column_dimensions['A'].width = 22
    ws.column_dimensions['B'].width = 100
    items = [
        ('范式名称', '一企一策分析（安逸酒店集团）'),
        ('版本', 'v1.0　2026-11-11　编制：安逸酒店集团产业发展部'),
        ('来源', '《安逸一企一策分析表-1107》（28 行 × 27 列）反推固化；原始表结构与行文全部保留，新增 5 个落地字段'),
        ('一句话', '用同一套财务与经营维度，对集团内每一个经营主体独立给出一句可执行的管理建议，并落到牵头人、节点与下一步动作。'),
        ('使用步骤一', '填「一企一策测算表」第 4 行起的数据区；金额单位统一万元；资产负债率与 ROE 由公式自动生成，不要手填。'),
        ('使用步骤二', '管理建议从策略词典 S01-S12 下拉选择，文字须与代码一致；处置优先级、EBITDA 覆盖倍数、出售与出租回收年数自动算出。'),
        ('使用步骤三', '按「判定决策树」逐级判定，先判层级与是否资不抵债，再判闲置与利息覆盖，最后才谈改造或自营。'),
        ('使用步骤四', '每一行必须填满牵头主体、关键节点、下一步动作三项，否则该建议无法跟踪，本质等于没做。'),
        ('使用步骤五', '填完执行「数据校验规则」十条，阻断级问题清零后方可提交。'),
        ('更新机制', '触发更新：主体增减、财务数据更新（建议按季）、处置方案落地。版本号递增，并在表头标注版本与日期。'),
        ('责任分工', '产业发展部维护本表与范式；各主体数据由财务金融部与运营管理中心提供；管理建议由产发部牵头会签。'),
        ('三条底线', '一、资不抵债主体不得给改造或投入类建议；二、所有建议必须可执行、可跟踪、有节点；三、单位与口径不清的数据不进入本表。'),
    ]
    for i, (k, v) in enumerate(items, 1):
        a = ws.cell(i, 1, k); b = ws.cell(i, 2, v)
        a.font = Font(name=FONT, size=10, bold=True, color=NAVY)
        a.alignment = Alignment(horizontal='left', vertical='top')
        b.font = Font(name=FONT, size=10)
        b.alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)
        a.border = BD; b.border = BD
    return ws


build_main()
build_dict()
build_tree()
build_checks()
build_fields()
build_readme()
wb._sheets = [wb['使用说明'], wb['一企一策测算表'], wb['策略词典'],
               wb['判定决策树'], wb['数据校验规则'], wb['字段口径说明']]
os.makedirs(os.path.dirname(OUT), exist_ok=True)
wb.save(OUT)
print('SAVED:', OUT)
print('SHEETS:', wb.sheetnames)

