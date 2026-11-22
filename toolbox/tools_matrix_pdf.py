"""
工具清单 PDF：整合 05 + 12，按规模分级组织
- 5 级规模：< 5 家 / 5-20 / 20-50 / 50-100 / 100+
- 工具名 + 推荐栈 + 预算 + 实施周期
"""
import os
import sys
sys.path.insert(0, r"D:\B166ER-OpenClaw\workspace\toolbox")

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    HRFlowable, Table, TableStyle, KeepTogether,
)
from md_to_pdf import (
    register_fonts, CHINESE_FONT, make_page_decorator, get_styles, inline_md_to_html,
)

PDF_DIR = r"D:\B166ER-OpenClaw\workspace\outputs\酒管公司供应链工程-交付包-v1.0"
OUTPUT = os.path.join(PDF_DIR, "03-工具清单-供应链数字化工具矩阵-v1.0.pdf")

register_fonts()
styles = get_styles()


def cell(content, style="TableCell", center=False):
    align_style = "TableCellCenter" if center else "TableCell"
    return Paragraph(content, styles[align_style])


def style_with_center(name="TableCellCenter"):
    return ParagraphStyle(
        name, parent=styles["TableCell"],
        alignment=TA_CENTER,
    )


def build_cover():
    flowables = []
    flowables.append(Spacer(1, 4 * cm))
    flowables.append(Paragraph("酒管公司供应链数字化", ParagraphStyle(
        "CoverMain", parent=styles["Normal"],
        fontName=CHINESE_FONT, fontSize=32, leading=44,
        alignment=TA_CENTER, textColor=colors.HexColor("#1F4E79"),
    )))
    flowables.append(Paragraph("工具清单 v1.0", ParagraphStyle(
        "CoverSub", parent=styles["Normal"],
        fontName=CHINESE_FONT, fontSize=28, leading=38,
        alignment=TA_CENTER, textColor=colors.HexColor("#1F4E79"),
        spaceAfter=10,
    )))
    flowables.append(Spacer(1, 0.5 * cm))
    flowables.append(HRFlowable(width="50%", thickness=1.2, color=colors.HexColor("#1F4E79"), hAlign="CENTER"))
    flowables.append(Spacer(1, 0.5 * cm))
    flowables.append(Paragraph("按规模分级 · 5 档 · 推荐栈 + 预算 + 周期", ParagraphStyle(
        "CoverTag", parent=styles["Normal"],
        fontName=CHINESE_FONT, fontSize=14, leading=22,
        alignment=TA_CENTER, textColor=colors.HexColor("#5B9BD5"),
    )))
    flowables.append(Spacer(1, 3 * cm))
    flowables.append(Paragraph("整合自 05-供应链数字化工具矩阵.md + 12-工具选型决策树.md",
                               ParagraphStyle("CoverMeta", parent=styles["Normal"],
                                              fontName=CHINESE_FONT, fontSize=10, leading=16,
                                              alignment=TA_CENTER, textColor=colors.HexColor("#888888"))))
    flowables.append(Spacer(1, 0.4 * cm))
    flowables.append(Paragraph("作者：B166ER · 日期：2026-07-11 · 版本：v1.0",
                               ParagraphStyle("CoverMeta", parent=styles["Normal"],
                                              fontName=CHINESE_FONT, fontSize=11, leading=18,
                                              alignment=TA_CENTER, textColor=colors.HexColor("#404040"))))
    flowables.append(Spacer(1, 1 * cm))
    flowables.append(Paragraph("ERIC的B166ER出品",
                               ParagraphStyle("CoverBrand", parent=styles["Normal"],
                                              fontName=CHINESE_FONT, fontSize=12, leading=20,
                                              alignment=TA_CENTER, textColor=colors.HexColor("#1F4E79"))))
    flowables.append(PageBreak())
    return flowables


def build_overview():
    """总览表：5 档规模对比"""
    flowables = []
    flowables.append(Paragraph("一、5 档规模 · 总览", ParagraphStyle(
        "Section", parent=styles["Normal"],
        fontName=CHINESE_FONT, fontSize=22, leading=30,
        textColor=colors.HexColor("#1F4E79"),
        spaceBefore=8, spaceAfter=12,
    )))
    flowables.append(HRFlowable(width="60%", thickness=0.8, color=colors.HexColor("#1F4E79"), spaceAfter=12))
    flowables.append(Paragraph(
        "本工具清单按酒店规模划分为 5 档，从微小型到集团型，"
        "每个规模档给出推荐工具栈、年度预算、实施周期与核心特征。",
        styles["Normal"]
    ))
    flowables.append(Spacer(1, 0.4 * cm))

    # 总览大表
    data = [
        [Paragraph("<b>档位</b>", styles["TableHeader"]),
         Paragraph("<b>规模</b>", styles["TableHeader"]),
         Paragraph("<b>年度预算</b>", styles["TableHeader"]),
         Paragraph("<b>实施周期</b>", styles["TableHeader"]),
         Paragraph("<b>核心特征</b>", styles["TableHeader"])],
        [Paragraph("微小型", styles["TableCell"]),
         Paragraph("< 5 家", styles["TableCell"]),
         Paragraph("5-20 万", styles["TableCell"]),
         Paragraph("1-2 周", styles["TableCell"]),
         Paragraph("业务优先 · 数字化辅助", styles["TableCell"])],
        [Paragraph("小型", styles["TableCell"]),
         Paragraph("5-20 家", styles["TableCell"]),
         Paragraph("30-80 万", styles["TableCell"]),
         Paragraph("1-2 个月", styles["TableCell"]),
         Paragraph("标准化 + 灵活性平衡", styles["TableCell"])],
        [Paragraph("中型 ★", styles["TableCell"]),
         Paragraph("20-50 家", styles["TableCell"]),
         Paragraph("80-200 万", styles["TableCell"]),
         Paragraph("3-6 个月", styles["TableCell"]),
         Paragraph("体系化建设期", styles["TableCell"])],
        [Paragraph("大型", styles["TableCell"]),
         Paragraph("50-100 家", styles["TableCell"]),
         Paragraph("300-800 万", styles["TableCell"]),
         Paragraph("6-12 个月", styles["TableCell"]),
         Paragraph("数字化转型期", styles["TableCell"])],
        [Paragraph("集团型", styles["TableCell"]),
         Paragraph("> 100 家", styles["TableCell"]),
         Paragraph("800-3000 万", styles["TableCell"]),
         Paragraph("12-24 个月", styles["TableCell"]),
         Paragraph("全面数字化", styles["TableCell"])],
    ]
    tbl = Table(data, colWidths=[2 * cm, 2 * cm, 2.5 * cm, 2.5 * cm, 8 * cm], repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F7FB")]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BFBFBF")),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        # 中型行高亮
        ("BACKGROUND", (0, 3), (-1, 3), colors.HexColor("#FFF2CC")),
    ]))
    flowables.append(tbl)
    flowables.append(Spacer(1, 0.4 * cm))

    return flowables


def build_tier(tier_num, tier_name, scale, budget, period, features, tools, alternative=None, page_break=True):
    """单个档位的详情页"""
    flowables = []
    if page_break:
        flowables.append(PageBreak())

    # 档位标题
    flowables.append(Paragraph(f"二、{tier_num} · {tier_name}", ParagraphStyle(
        "TierTitle", parent=styles["Normal"],
        fontName=CHINESE_FONT, fontSize=24, leading=32,
        textColor=colors.HexColor("#1F4E79"),
        spaceBefore=8, spaceAfter=8,
    )))
    flowables.append(HRFlowable(width="60%", thickness=1.0, color=colors.HexColor("#1F4E79"), spaceAfter=12))

    # 核心信息表
    info_data = [
        [Paragraph("<b>项目</b>", styles["TableHeader"]),
         Paragraph("<b>说明</b>", styles["TableHeader"])],
        [Paragraph("<b>酒店规模</b>", styles["TableCell"]),
         Paragraph(scale, styles["TableCell"])],
        [Paragraph("<b>年度预算</b>", styles["TableCell"]),
         Paragraph(budget, styles["TableCell"])],
        [Paragraph("<b>实施周期</b>", styles["TableCell"]),
         Paragraph(period, styles["TableCell"])],
        [Paragraph("<b>核心特征</b>", styles["TableCell"]),
         Paragraph(features, styles["TableCell"])],
    ]
    info_tbl = Table(info_data, colWidths=[3 * cm, 14 * cm], repeatRows=1)
    info_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#5B9BD5")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F7FB")]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BFBFBF")),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    flowables.append(info_tbl)
    flowables.append(Spacer(1, 0.4 * cm))

    # 推荐工具栈
    flowables.append(Paragraph("推荐工具栈", styles["H3"]))

    stack_data = [[Paragraph("<b>工具</b>", styles["TableHeader"]),
                   Paragraph("<b>作用</b>", styles["TableHeader"]),
                   Paragraph("<b>说明</b>", styles["TableHeader"])]]
    for tool_name, tool_func, tool_note in tools:
        stack_data.append([
            Paragraph(f"<b>{tool_name}</b>", styles["TableCell"]),
            Paragraph(tool_func, styles["TableCell"]),
            Paragraph(tool_note, styles["TableCell"]),
        ])
    stack_tbl = Table(stack_data, colWidths=[5 * cm, 4.5 * cm, 7.5 * cm], repeatRows=1)
    stack_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F7FB")]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BFBFBF")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    flowables.append(stack_tbl)
    flowables.append(Spacer(1, 0.4 * cm))

    if alternative:
        flowables.append(Paragraph("备选方案", styles["H3"]))
        flowables.append(Paragraph(alternative, styles["Normal"]))
        flowables.append(Spacer(1, 0.3 * cm))

    # 选型决策提示
    flowables.append(Paragraph("选型决策", styles["H3"]))
    flowables.append(Paragraph(
        f"<b>问自己</b>：3 个核心问题 → "
        f"① 你的酒店数是否在 {scale} 区间？"
        f"② 年度预算是否覆盖 {budget}？"
        f"③ 实施周期是否能承受 {period}？",
        styles["Normal"]
    ))

    return flowables


def build_decision_tree():
    """选型决策树"""
    flowables = []
    flowables.append(PageBreak())
    flowables.append(Paragraph("三、选型决策树", ParagraphStyle(
        "Section", parent=styles["Normal"],
        fontName=CHINESE_FONT, fontSize=22, leading=30,
        textColor=colors.HexColor("#1F4E79"),
        spaceBefore=8, spaceAfter=12,
    )))
    flowables.append(HRFlowable(width="60%", thickness=0.8, color=colors.HexColor("#1F4E79"), spaceAfter=12))

    flowables.append(Paragraph("3.1 SRM 选型决策", styles["H2"]))
    flowables.append(Paragraph(
        "<b>Q1</b>: 你的酒店规模？<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;< 20 家 → 简道云 + 钉钉<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;20-50 家 → 甄云 SRM（推荐）<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;50-100 家 → 用友/金蝶 SRM<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;> 100 家 → SAP Ariba / Oracle",
        styles["Normal"]
    ))
    flowables.append(Spacer(1, 0.3 * cm))

    flowables.append(Paragraph(
        "<b>Q2</b>: 你的年度预算？<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;< 10 万/年 → SaaS 套件<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;10-50 万/年 → 甄云<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;50-200 万/年 → 用友/金蝶<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;> 200 万/年 → SAP / Oracle",
        styles["Normal"]
    ))
    flowables.append(Spacer(1, 0.4 * cm))

    flowables.append(Paragraph("3.2 仓储选型决策", styles["H2"]))
    flowables.append(Paragraph(
        "<b>Q</b>: 仓库数量？<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;1-5 个 → 简道云 + 一物一码<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;5-20 个 → C-WMS<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;20-50 个 → SAP EWM / 富勒<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;> 50 个 → 自研 + IoT",
        styles["Normal"]
    ))
    flowables.append(Spacer(1, 0.4 * cm))

    flowables.append(Paragraph("3.3 按核心痛点选型", styles["H2"]))
    pain_data = [
        [Paragraph("<b>核心痛点</b>", styles["TableHeader"]),
         Paragraph("<b>核心工具</b>", styles["TableHeader"]),
         Paragraph("<b>辅助工具</b>", styles["TableHeader"]),
         Paragraph("<b>预算分配</b>", styles["TableHeader"])],
        [Paragraph("采购成本太高", styles["TableCell"]),
         Paragraph("SRM + AI 比价", styles["TableCell"]),
         Paragraph("京东企业购、同驿商城", styles["TableCell"]),
         Paragraph("60% SRM + 30% AI + 10% 其他", styles["TableCell"])],
        [Paragraph("库存积压严重", styles["TableCell"]),
         Paragraph("WMS + AI 需求预测", styles["TableCell"]),
         Paragraph("SRM、智能补货系统", styles["TableCell"]),
         Paragraph("50% WMS + 30% AI + 20% SRM", styles["TableCell"])],
        [Paragraph("供应商质量差", styles["TableCell"]),
         Paragraph("SRM + 质量追溯系统", styles["TableCell"]),
         Paragraph("一物一码、IoT", styles["TableCell"]),
         Paragraph("50% SRM + 30% 追溯 + 20% IoT", styles["TableCell"])],
        [Paragraph("响应速度慢", styles["TableCell"]),
         Paragraph("移动化 + RPA + 应急系统", styles["TableCell"]),
         Paragraph("钉钉/企微、智能告警", styles["TableCell"]),
         Paragraph("40% 移动化 + 30% RPA + 30% 应急", styles["TableCell"])],
        [Paragraph("决策不科学", styles["TableCell"]),
         Paragraph("BI + 数据中台 + AI", styles["TableCell"]),
         Paragraph("KPI 仪表盘、预测算法", styles["TableCell"]),
         Paragraph("50% BI + 30% AI + 20% 数据中台", styles["TableCell"])],
    ]
    pain_tbl = Table(pain_data, colWidths=[3 * cm, 4 * cm, 4 * cm, 6 * cm], repeatRows=1)
    pain_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F7FB")]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BFBFBF")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    flowables.append(pain_tbl)

    return flowables


def build_5_levels():
    """5 级数字化成熟度路径"""
    flowables = []
    flowables.append(PageBreak())
    flowables.append(Paragraph("四、5 级数字化成熟度路径", ParagraphStyle(
        "Section", parent=styles["Normal"],
        fontName=CHINESE_FONT, fontSize=22, leading=30,
        textColor=colors.HexColor("#1F4E79"),
        spaceBefore=8, spaceAfter=12,
    )))
    flowables.append(HRFlowable(width="60%", thickness=0.8, color=colors.HexColor("#1F4E79"), spaceAfter=12))
    flowables.append(Paragraph(
        "从 Excel 到数字孪生，酒管公司供应链数字化的 5 级路径：",
        styles["Normal"]
    ))
    flowables.append(Spacer(1, 0.3 * cm))

    lvl_data = [
        [Paragraph("<b>等级</b>", styles["TableHeader"]),
         Paragraph("<b>特征</b>", styles["TableHeader"]),
         Paragraph("<b>推荐工具</b>", styles["TableHeader"]),
         Paragraph("<b>投资</b>", styles["TableHeader"])],
        [Paragraph("L1 初始", styles["TableCell"]),
         Paragraph("Excel 表格", styles["TableCell"]),
         Paragraph("无", styles["TableCell"]),
         Paragraph("0", styles["TableCell"])],
        [Paragraph("L2 标准化", styles["TableCell"]),
         Paragraph("ERP 基础模块", styles["TableCell"]),
         Paragraph("用友 / 金蝶", styles["TableCell"]),
         Paragraph("10-50 万", styles["TableCell"])],
        [Paragraph("L3 集成化", styles["TableCell"]),
         Paragraph("SRM + WMS + BI", styles["TableCell"]),
         Paragraph("行业 SaaS", styles["TableCell"]),
         Paragraph("50-200 万", styles["TableCell"])],
        [Paragraph("L4 智能化", styles["TableCell"]),
         Paragraph("AI 预测 + IoT", styles["TableCell"]),
         Paragraph("AI 引擎 + IoT", styles["TableCell"]),
         Paragraph("200-500 万", styles["TableCell"])],
        [Paragraph("L5 自治化", styles["TableCell"]),
         Paragraph("数字孪生 + 自主决策", styles["TableCell"]),
         Paragraph("高级算法", styles["TableCell"]),
         Paragraph("500 万+", styles["TableCell"])],
    ]
    lvl_tbl = Table(lvl_data, colWidths=[2 * cm, 4.5 * cm, 4.5 * cm, 4 * cm], repeatRows=1)
    lvl_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F7FB")]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BFBFBF")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    flowables.append(lvl_tbl)
    flowables.append(Spacer(1, 0.4 * cm))

    flowables.append(Paragraph("升级路径", styles["H3"]))
    flowables.append(Paragraph(
        "<b>L1 → L2</b>：基础 ERP 上线<br/>"
        "<b>L2 → L3</b>：SRM / WMS / BI 集成<br/>"
        "<b>L3 → L4</b>：AI 能力嵌入<br/>"
        "<b>L4 → L5</b>：数字孪生 + 自治",
        styles["Normal"]
    ))
    flowables.append(Spacer(1, 0.4 * cm))

    flowables.append(Paragraph("AI 应用场景（2026 已成熟）", styles["H3"]))
    ai_data = [
        [Paragraph("<b>场景</b>", styles["TableHeader"]),
         Paragraph("<b>成熟度</b>", styles["TableHeader"]),
         Paragraph("<b>价值</b>", styles["TableHeader"])],
        [Paragraph("智能比价", styles["TableCell"]),
         Paragraph("★★★★★", styles["TableCell"]),
         Paragraph("节省 5-15% 成本", styles["TableCell"])],
        [Paragraph("需求预测", styles["TableCell"]),
         Paragraph("★★★★", styles["TableCell"]),
         Paragraph("减少 30% 库存", styles["TableCell"])],
        [Paragraph("智能验收", styles["TableCell"]),
         Paragraph("★★★", styles["TableCell"]),
         Paragraph("减少 50% 人工", styles["TableCell"])],
        [Paragraph("风险预警", styles["TableCell"]),
         Paragraph("★★★★", styles["TableCell"]),
         Paragraph("提前 30 天预警", styles["TableCell"])],
        [Paragraph("智能客服", styles["TableCell"]),
         Paragraph("★★★★★", styles["TableCell"]),
         Paragraph("节省 80% 人工", styles["TableCell"])],
        [Paragraph("合同审查", styles["TableCell"]),
         Paragraph("★★★★", styles["TableCell"]),
         Paragraph("节省 70% 时间", styles["TableCell"])],
    ]
    ai_tbl = Table(ai_data, colWidths=[4 * cm, 3 * cm, 8 * cm], repeatRows=1)
    ai_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#5B9BD5")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F7FB")]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BFBFBF")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    flowables.append(ai_tbl)
    flowables.append(Spacer(1, 0.4 * cm))

    flowables.append(Paragraph("AI 落地路径", styles["H3"]))
    flowables.append(Paragraph(
        "<b>第一阶段</b>：AI 比价 + 智能客服（最易落地）<br/>"
        "<b>第二阶段</b>：需求预测 + 风险预警<br/>"
        "<b>第三阶段</b>：智能验收 + 合同审查<br/>"
        "<b>第四阶段</b>：数字孪生 + 自治决策",
        styles["Normal"]
    ))

    return flowables


def build_success_factors():
    """关键成功因素"""
    flowables = []
    flowables.append(PageBreak())
    flowables.append(Paragraph("五、关键成功因素", ParagraphStyle(
        "Section", parent=styles["Normal"],
        fontName=CHINESE_FONT, fontSize=22, leading=30,
        textColor=colors.HexColor("#1F4E79"),
        spaceBefore=8, spaceAfter=12,
    )))
    flowables.append(HRFlowable(width="60%", thickness=0.8, color=colors.HexColor("#1F4E79"), spaceAfter=12))

    factors = [
        ("1", "不要重复造轮子", "用成熟 SaaS，自研风险极大。除非 100+ 家门店，否则不自研核心模块。"),
        ("2", "移动优先", "采购员、验收员、仓管员都要能用手机完成工作。PC-only 系统会被绕过。"),
        ("3", "集成优先", "避免数据孤岛。工具必须能与 PMS/ERP/财务打通，否则形成数据孤岛。"),
        ("4", "数据沉淀", "所有交易都要进数据湖。每笔采购、每次验收、每张发票都要沉淀数据资产。"),
        ("5", "分阶段实施", "从核心场景开始。先打通 1 个品类，再扩展到全品类；先覆盖 1 个区域，再扩展到全国。"),
        ("6", "数据安全合规", "国产化要求？数据本地化？合规审计接口？这些都必须在选型前明确。"),
    ]
    for num, title, desc in factors:
        flowables.append(Paragraph(f"<b>{num}. {title}</b>", styles["H3"]))
        flowables.append(Paragraph(desc, styles["Normal"]))
        flowables.append(Spacer(1, 0.2 * cm))

    flowables.append(Spacer(1, 0.5 * cm))
    flowables.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#888888"), spaceAfter=12))
    flowables.append(Paragraph(
        "<i>本工具清单整合自 05-供应链数字化工具矩阵.md 与 12-工具选型决策树.md。"
        "更多细节请参考分章节 PDF 第 5 章与第 12 章。</i>",
        ParagraphStyle("Footer", parent=styles["Normal"],
                       fontName=CHINESE_FONT, fontSize=9, leading=14,
                       textColor=colors.HexColor("#888888"),
                       alignment=TA_CENTER,
                       spaceBefore=8, spaceAfter=4)
    ))

    return flowables


def main():
    all_flowables = []
    all_flowables.extend(build_cover())
    all_flowables.extend(build_overview())

    # 二、5 档规模详细
    # 档位 1：微小型
    all_flowables.extend(build_tier(
        "2.1", "微小型（< 5 家酒店）",
        "< 5 家",
        "5-20 万/年",
        "1-2 周",
        "业务优先 · 数字化辅助 · 1-2 个 IT 人员",
        [
            ("钉钉 / 企微", "基础平台", "OA + 审批 + 沟通"),
            ("简道云 / 钉钉宜搭", "采购申请 + 审批", "无代码搭建审批流"),
            ("京东企业购", "标准物资", "MRO 一站式采购"),
            ("同驿商城", "酒店专用", "布草/客用品平台"),
            ("钉钉表格", "台账 / 报表", "替代 Excel"),
            ("钉钉群", "沟通协同", "群通知 + 公告"),
        ],
        alternative="不需要专业 SRM / 不需要专业 WMS / 不需要 BI（Excel 足够）。重点是\"先用起来\"。",
        page_break=False,
    ))

    # 档位 2：小型
    all_flowables.extend(build_tier(
        "2.2", "小型（5-20 家酒店）",
        "5-20 家",
        "30-80 万/年",
        "1-2 个月",
        "标准化 + 灵活性平衡 · 1-3 个 IT 人员",
        [
            ("甄云 SRM SaaS", "供应商管理", "行业最成熟的 SRM SaaS"),
            ("简道云", "流程引擎", "采购申请 / 审批 / 对账"),
            ("京东企业购", "标准物资", "MRO 通用物资"),
            ("同驿商城", "酒店专用", "客房 / 餐饮用品"),
            ("简道云 / 钉钉宜搭", "轻量 WMS", "一物一码 + 条码"),
            ("FineBI Lite", "数据分析", "轻量 BI 仪表盘"),
        ],
        alternative="<b>备选 B</b>（行业 SaaS 优先）：携程商旅\"招采通\" + 同驿商城 + 神州一诺 + 钉钉表格 + 钉钉机器人。",
        page_break=True,
    ))

    # 档位 3：中型（推荐重点）
    all_flowables.extend(build_tier(
        "2.3", "中型（20-50 家酒店） ★ 推荐 ★",
        "20-50 家",
        "80-200 万/年",
        "3-6 个月",
        "体系化建设期 · 3-5 个 IT 人员",
        [
            ("用友 / 金蝶 Cloud", "ERP 底座", "财务 + 总账 + 报表"),
            ("甄云 SRM（推荐）", "供应商全生命周期", "寻源 / 准入 / 绩效 / 退出"),
            ("用友 / 金蝶 SRM", "备选 SRM", "或继续用甄云"),
            ("C-WMS", "仓储管理", "入库 / 出库 / 盘点"),
            ("FineBI", "数据分析", "采购 / 库存 / 供应商仪表盘"),
            ("同驿商城", "酒店专用", "客房 / 餐饮 / 工程物资"),
            ("京东企业购", "标准物资", "MRO 一站式"),
            ("阿里云 iPaaS", "系统集成", "PMS / 财务 / 钉钉对接"),
        ],
        alternative="<b>备选 A</b>（国内大厂套件）：用友/金蝶 Cloud + 用友/金蝶 SRM + 用友/金蝶 WMS + 用友/金蝶 BI + 同驿商城 + 京东企业购 + 钉钉/企微 + API 网关。",
        page_break=True,
    ))

    # 档位 4：大型
    all_flowables.extend(build_tier(
        "2.4", "大型（50-100 家酒店）",
        "50-100 家",
        "300-800 万/年",
        "6-12 个月",
        "数字化转型期 · 5-15 个 IT 人员",
        [
            ("用友 NC Cloud / 金蝶云苍穹", "企业级 ERP", "多组织 / 多账套"),
            ("用友 / 金蝶 SRM", "供应商全生命周期", "高级合同 / 招投标"),
            ("用友 / 金蝶 WMS", "仓储管理", "多仓 / 调拨 / 批次"),
            ("帆软 FineBI / Power BI", "高级数据分析", "数据中台 + BI"),
            ("同驿商城", "酒店专用", "深耕酒店专用物资"),
            ("京东企业购", "标准物资", "MRO 全品类"),
            ("钉钉/企微 + RPA", "流程自动化", "RPA 替代重复工作"),
            ("AI 平台", "智能比价 / 预测 / 补货", "自研或采购 AI 引擎"),
            ("阿里云 iPaaS", "系统集成", "复杂集成架构"),
            ("区块链平台", "溯源", "食材 / 布草溯源"),
        ],
        page_break=True,
    ))

    # 档位 5：集团型
    all_flowables.extend(build_tier(
        "2.5", "集团型（> 100 家酒店）",
        "> 100 家",
        "800-3000 万/年",
        "12-24 个月",
        "全面数字化 · 15+ 个 IT 人员",
        [
            ("SAP S/4HANA / Oracle ERP Cloud", "企业级 ERP 底座", "全球 500 强标配"),
            ("SAP Ariba / Oracle Procurement Cloud", "采购云", "全球最大采购网络"),
            ("SAP EWM", "仓储管理", "高复杂度仓库"),
            ("SAP IBP", "供应链计划", "需求 / 供应 / 库存计划"),
            ("自研 BI + AI 平台", "数据中台", "完全自主可控"),
            ("行业 SaaS 集成", "酒店专用物资", "同驿 / 京东 / 神州一诺"),
            ("区块链溯源平台", "可信追溯", "食材 / 布草"),
            ("数字孪生平台", "运营虚拟镜像", "采购-库存-消耗-补货"),
            ("自研数据中台", "数据资产", "湖仓一体"),
            ("智能决策系统", "AI 决策", "比价 / 预测 / 补货 / 风险"),
        ],
        page_break=True,
    ))

    # 三、选型决策树
    all_flowables.extend(build_decision_tree())

    # 四、5 级数字化成熟度路径
    all_flowables.extend(build_5_levels())

    # 五、关键成功因素
    all_flowables.extend(build_success_factors())

    # 构建 PDF
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title="酒管公司供应链数字化工具清单 v1.0",
        author="B166ER",
    )
    doc.build(
        all_flowables,
        onFirstPage=make_page_decorator("酒管公司供应链工程 · 工具清单 v1.0"),
        onLaterPages=make_page_decorator("酒管公司供应链工程 · 工具清单 v1.0"),
    )
    print(f"OK {OUTPUT}")
    print(f"Size: {os.path.getsize(OUTPUT):,} bytes")


if __name__ == "__main__":
    main()