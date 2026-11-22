"""
合并 13 个 MD 为综合主报告 PDF
- 完整目录页（13 章节 + 页码估算）
- 每个章节前加分页
- 最后加"使用指南"页（基于 10-产品矩阵与使用指南.md）
"""
import os
import sys
import glob
sys.path.insert(0, r"D:\B166ER-OpenClaw\workspace\toolbox")

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    HRFlowable, Table, TableStyle, KeepTogether,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from md_to_pdf import (
    register_fonts, parse_markdown_lines, tokens_to_flowables,
    inline_md_to_html, CHINESE_FONT, make_page_decorator, get_styles,
)

PDF_DIR = r"D:\B166ER-OpenClaw\workspace\outputs\酒管公司供应链工程-交付包-v1.0\02-分章节PDFs"
OUTPUT = r"D:\B166ER-OpenClaw\workspace\outputs\酒管公司供应链工程-交付包-v1.0\01-综合主报告-酒管公司供应链工程全维度体系-v1.0.pdf"

# 章节定义：(编号, MD 文件名, 显示标题)
CHAPTERS = [
    ("01", "01-主报告-酒店供应链工程全维度体系.md", "统筹·体系·架构·工具·数字化联动·经营·响应·成本"),
    ("02", "02-酒管公司供应链工程实施方案.md", "实施方案"),
    ("03", "03-分级分类酒店供应链体系架构.md", "分级分类体系架构"),
    ("04", "04-供应商分级管理手册.md", "供应商分级管理"),
    ("05", "05-供应链数字化工具矩阵.md", "供应链数字化工具矩阵"),
    ("06", "06-供应链KPI体系.md", "供应链 KPI 体系"),
    ("07", "07-应急供应链SOP手册.md", "应急供应链 SOP"),
    ("08", "08-成本控制与TCO模型.md", "成本控制与 TCO 模型"),
    ("09", "09-供应链工程实施检查清单.md", "实施检查清单"),
    ("10", "10-产品矩阵与使用指南.md", "产品矩阵与使用指南"),
    ("11", "11-数据与经营同步方法.md", "数据与经营同步"),
    ("12", "12-工具选型决策树.md", "工具选型决策树"),
    ("13", "13-技术架构类型选择.md", "技术架构类型选择"),
]

register_fonts()
styles = get_styles()


def build_cover(styles):
    """封面页"""
    flowables = []
    flowables.append(Spacer(1, 5 * cm))
    flowables.append(Paragraph("酒管公司供应链工程", ParagraphStyle(
        "CoverMain", parent=styles["Normal"],
        fontName=CHINESE_FONT, fontSize=36, leading=48,
        alignment=TA_CENTER, textColor=colors.HexColor("#1F4E79"),
    )))
    flowables.append(Spacer(1, 0.8 * cm))
    flowables.append(Paragraph("全维度体系 · 综合主报告", ParagraphStyle(
        "CoverSub", parent=styles["Normal"],
        fontName=CHINESE_FONT, fontSize=20, leading=28,
        alignment=TA_CENTER, textColor=colors.HexColor("#404040"),
    )))
    flowables.append(Spacer(1, 1.5 * cm))
    flowables.append(HRFlowable(width="50%", thickness=1.5, color=colors.HexColor("#1F4E79"), hAlign="CENTER"))
    flowables.append(Spacer(1, 0.5 * cm))
    flowables.append(Paragraph("13 章整合 · 完整目录 · 适合通读", ParagraphStyle(
        "CoverTag", parent=styles["Normal"],
        fontName=CHINESE_FONT, fontSize=14, leading=22,
        alignment=TA_CENTER, textColor=colors.HexColor("#5B9BD5"),
    )))
    flowables.append(Spacer(1, 4 * cm))
    flowables.append(Paragraph("作者：B166ER", ParagraphStyle(
        "CoverMeta", parent=styles["Normal"],
        fontName=CHINESE_FONT, fontSize=12, leading=20,
        alignment=TA_CENTER, textColor=colors.HexColor("#404040"),
    )))
    flowables.append(Paragraph("日期：2026-07-11", ParagraphStyle(
        "CoverMeta", parent=styles["Normal"],
        fontName=CHINESE_FONT, fontSize=12, leading=20,
        alignment=TA_CENTER, textColor=colors.HexColor("#404040"),
    )))
    flowables.append(Paragraph("版本：v1.0", ParagraphStyle(
        "CoverMeta", parent=styles["Normal"],
        fontName=CHINESE_FONT, fontSize=12, leading=20,
        alignment=TA_CENTER, textColor=colors.HexColor("#404040"),
    )))
    flowables.append(Spacer(1, 1 * cm))
    flowables.append(HRFlowable(width="60%", thickness=0.6, color=colors.HexColor("#888888"), hAlign="CENTER"))
    flowables.append(Spacer(1, 0.4 * cm))
    flowables.append(Paragraph("ERIC的B166ER出品", ParagraphStyle(
        "CoverBrand", parent=styles["Normal"],
        fontName=CHINESE_FONT, fontSize=13, leading=20,
        alignment=TA_CENTER, textColor=colors.HexColor("#1F4E79"),
    )))
    return flowables


def build_toc(styles):
    """目录页"""
    flowables = []
    flowables.append(Spacer(1, 1 * cm))
    flowables.append(Paragraph("目  录", ParagraphStyle(
        "TOCTitle", parent=styles["Normal"],
        fontName=CHINESE_FONT, fontSize=28, leading=40,
        alignment=TA_CENTER, textColor=colors.HexColor("#1F4E79"),
        spaceAfter=12,
    )))
    flowables.append(HRFlowable(width="60%", thickness=1.2, color=colors.HexColor("#1F4E79"), hAlign="CENTER"))
    flowables.append(Spacer(1, 0.6 * cm))
    flowables.append(Paragraph("Table of Contents", ParagraphStyle(
        "TOCSub", parent=styles["Normal"],
        fontName=CHINESE_FONT, fontSize=10, leading=18,
        alignment=TA_CENTER, textColor=colors.HexColor("#888888"),
        spaceAfter=14,
    )))

    # 章节列表（基于编号估算页码起始位置）
    page_estimates = {
        "01": "1", "02": "22", "03": "33", "04": "46",
        "05": "55", "06": "63", "07": "73", "08": "82",
        "09": "92", "10": "100", "11": "107", "12": "118",
        "13": "127",
    }
    # 章节标题
    toc_rows = [["编号", "章节", "页码"]]
    toc_data = []
    toc_data.append([Paragraph("<b>编号</b>", styles["TableHeader"]),
                     Paragraph("<b>章节</b>", styles["TableHeader"]),
                     Paragraph("<b>页码</b>", styles["TableHeader"])])
    for num, fname, title in CHAPTERS:
        toc_data.append([
            Paragraph(f"<b>{num}</b>", styles["TableCell"]),
            Paragraph(f"{num} - {title}", styles["TableCell"]),
            Paragraph(page_estimates.get(num, "—"), styles["TableCell"]),
        ])
    # 附加：附录
    toc_data.append([
        Paragraph("附", styles["TableCell"]),
        Paragraph("附录 · 使用指南（基于 10-产品矩阵与使用指南）", styles["TableCell"]),
        Paragraph("138", styles["TableCell"]),
    ])

    tbl = Table(toc_data, colWidths=[2 * cm, 13 * cm, 2 * cm], repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("ALIGN", (-1, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F7FB")]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BFBFBF")),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    flowables.append(tbl)
    flowables.append(Spacer(1, 0.8 * cm))

    # 阅读路径提示
    flowables.append(Paragraph("5 大产品阅读路径", ParagraphStyle(
        "PathTitle", parent=styles["Normal"],
        fontName=CHINESE_FONT, fontSize=14, leading=22,
        textColor=colors.HexColor("#1F4E79"),
        spaceBefore=10, spaceAfter=6,
    )))
    path_data = [
        [Paragraph("<b>角色</b>", styles["TableHeader"]),
         Paragraph("<b>优先阅读章节</b>", styles["TableHeader"])],
        [Paragraph("CEO/CFO 决策层", styles["TableCell"]),
         Paragraph("01 → 06 → 02 → 09", styles["TableCell"])],
        [Paragraph("项目组（实施）", styles["TableCell"]),
         Paragraph("01 → 02 → 09 → 03 → 04 → 05 → 06", styles["TableCell"])],
        [Paragraph("采购总监", styles["TableCell"]),
         Paragraph("01 → 03 → 04 → 05 → 06 → 08 → 07", styles["TableCell"])],
        [Paragraph("采购经理", styles["TableCell"]),
         Paragraph("04 → 06 → 08 → 07 → 03", styles["TableCell"])],
        [Paragraph("IT 负责人", styles["TableCell"]),
         Paragraph("05 → 02 → 06 → 01", styles["TableCell"])],
    ]
    path_tbl = Table(path_data, colWidths=[4 * cm, 13 * cm], repeatRows=1)
    path_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2E75B6")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F7FB")]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BFBFBF")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    flowables.append(path_tbl)

    return flowables


def build_chapter(num, md_path, chapter_title, styles, is_appendix=False, skip_first_h1=True):
    """构建单个章节的 flowables"""
    flowables = []
    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()
    tokens = parse_markdown_lines(md_text)

    # 章节封面（小型）
    chapter_intro_style = ParagraphStyle(
        "ChapterIntro", parent=styles["Normal"],
        fontName=CHINESE_FONT, fontSize=22, leading=32,
        textColor=colors.HexColor("#1F4E79"),
        alignment=TA_LEFT, spaceBefore=10, spaceAfter=8,
    )
    chapter_sub_style = ParagraphStyle(
        "ChapterSub", parent=styles["Normal"],
        fontName=CHINESE_FONT, fontSize=12, leading=20,
        textColor=colors.HexColor("#888888"),
        spaceAfter=12,
    )
    flowables.append(Spacer(1, 1.5 * cm))
    flowables.append(Paragraph(f"第 {num} 章", ParagraphStyle(
        "ChapterNum", parent=styles["Normal"],
        fontName=CHINESE_FONT, fontSize=14, leading=22,
        textColor=colors.HexColor("#5B9BD5"),
        spaceAfter=4,
    )))
    flowables.append(Paragraph(chapter_title, chapter_intro_style))
    flowables.append(HRFlowable(width="40%", thickness=1.0, color=colors.HexColor("#1F4E79"), spaceAfter=10))
    flowables.append(Paragraph(f"对应分章节文件：{os.path.basename(md_path)}", chapter_sub_style))
    flowables.append(PageBreak())

    # 正文（跳过第一个 H1，因为我们已经单独渲染了章节标题）
    if skip_first_h1:
        # 找到第一个 H1 并跳过
        filtered = []
        skipped = False
        for tok in tokens:
            if tok["type"] == "h" and tok["level"] == 1 and not skipped:
                skipped = True
                continue
            filtered.append(tok)
        tokens = filtered

    body = tokens_to_flowables(tokens, styles)
    flowables.extend(body)
    return flowables


def build_usage_appendix(styles):
    """附录：使用指南（基于 10）"""
    flowables = []
    flowables.append(PageBreak())
    flowables.append(Spacer(1, 1 * cm))
    flowables.append(Paragraph("附录 · 产品使用指南", ParagraphStyle(
        "AppTitle", parent=styles["Normal"],
        fontName=CHINESE_FONT, fontSize=26, leading=36,
        textColor=colors.HexColor("#1F4E79"),
        alignment=TA_LEFT, spaceAfter=12,
    )))
    flowables.append(HRFlowable(width="60%", thickness=1.0, color=colors.HexColor("#1F4E79"), spaceAfter=14))
    flowables.append(Paragraph("（基于 10-产品矩阵与使用指南.md 整合）", ParagraphStyle(
        "AppSub", parent=styles["Normal"],
        fontName=CHINESE_FONT, fontSize=11, leading=18,
        textColor=colors.HexColor("#888888"), spaceAfter=14,
    )))

    # 使用建议
    flowables.append(Paragraph("一、5 大角色 · 阅读路径", styles["H2"]))
    flowables.append(Paragraph(
        "不同角色进入此交付包后，建议按以下优先级阅读，以最短路径获得最高决策价值。",
        styles["Normal"]
    ))
    role_data = [
        [Paragraph("<b>角色</b>", styles["TableHeader"]),
         Paragraph("<b>阅读路径</b>", styles["TableHeader"]),
         Paragraph("<b>目标</b>", styles["TableHeader"])],
        [Paragraph("CEO/CFO 决策层", styles["TableCell"]),
         Paragraph("01 → 06 → 02 → 09", styles["TableCell"]),
         Paragraph("理解全貌 · 看 KPI · 看实施方案 · 看检查清单", styles["TableCell"])],
        [Paragraph("项目组（实施）", styles["TableCell"]),
         Paragraph("01 → 02 → 09 → 03 → 04 → 05 → 06", styles["TableCell"]),
         Paragraph("从主报告到实施 SOP · 体系架构 · 供应商管理 · 工具矩阵 · KPI", styles["TableCell"])],
        [Paragraph("采购总监", styles["TableCell"]),
         Paragraph("01 → 03 → 04 → 05 → 06 → 08 → 07", styles["TableCell"]),
         Paragraph("体系架构 · 供应商分级 · 工具 · KPI · 成本控制 · 应急 SOP", styles["TableCell"])],
        [Paragraph("采购经理", styles["TableCell"]),
         Paragraph("04 → 06 → 08 → 07 → 03", styles["TableCell"]),
         Paragraph("供应商管理 · KPI · 成本控制 · 应急 · 体系", styles["TableCell"])],
        [Paragraph("IT 负责人", styles["TableCell"]),
         Paragraph("05 → 02 → 06 → 01", styles["TableCell"]),
         Paragraph("工具矩阵 · 实施方案 · 数据同步 · 主报告全貌", styles["TableCell"])],
    ]
    role_tbl = Table(role_data, colWidths=[3.2 * cm, 4.5 * cm, 9.3 * cm], repeatRows=1)
    role_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E79")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F7FB")]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BFBFBF")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
    ]))
    flowables.append(role_tbl)
    flowables.append(Spacer(1, 0.4 * cm))

    # 产品选包建议
    flowables.append(Paragraph("二、产品选包建议", styles["H2"]))
    pkg_data = [
        [Paragraph("<b>版本</b>", styles["TableHeader"]),
         Paragraph("<b>包含章节</b>", styles["TableHeader"]),
         Paragraph("<b>适用场景</b>", styles["TableHeader"])],
        [Paragraph("<b>速赢版</b><br/>(3 个月)", styles["TableCell"]),
         Paragraph("01 + 02 + 04 + 06 + 09", styles["TableCell"]),
         Paragraph("先跑通主流程 · KPI + 应急 · 验证可行性", styles["TableCell"])],
        [Paragraph("<b>标准版</b><br/>(6-12 个月)", styles["TableCell"]),
         Paragraph("01 + 02 + 03 + 04 + 05 + 06 + 08 + 09", styles["TableCell"]),
         Paragraph("完整体系 + 工具 + 成本控制 · 多数酒管公司首选", styles["TableCell"])],
        [Paragraph("<b>完整版</b><br/>(12-24 个月)", styles["TableCell"]),
         Paragraph("全部 13 份 + 思维导图", styles["TableCell"]),
         Paragraph("全维度建设 · 集团型酒管 · 含技术架构选型", styles["TableCell"])],
    ]
    pkg_tbl = Table(pkg_data, colWidths=[3 * cm, 5 * cm, 9 * cm], repeatRows=1)
    pkg_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2E75B6")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F7FB")]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BFBFBF")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    flowables.append(pkg_tbl)
    flowables.append(Spacer(1, 0.4 * cm))

    # 实施节奏
    flowables.append(Paragraph("三、3 阶段实施节奏", styles["H2"]))
    rhythm_data = [
        [Paragraph("<b>阶段</b>", styles["TableHeader"]),
         Paragraph("<b>时间</b>", styles["TableHeader"]),
         Paragraph("<b>关键动作</b>", styles["TableHeader"]),
         Paragraph("<b>产出</b>", styles["TableHeader"])],
        [Paragraph("阶段 1：基础", styles["TableCell"]),
         Paragraph("1-3 个月", styles["TableCell"]),
         Paragraph("治理结构 + 品类分级 + KPI 体系 + 应急 SOP", styles["TableCell"]),
         Paragraph("集采目录 + 供应商分级 + KPI 仪表盘 v1", styles["TableCell"])],
        [Paragraph("阶段 2：体系", styles["TableCell"]),
         Paragraph("4-9 个月", styles["TableCell"]),
         Paragraph("供应商全生命周期 + 工具矩阵 + 成本控制", styles["TableCell"]),
         Paragraph("SRM/WMS 选型上线 + TCO 模型落地", styles["TableCell"])],
        [Paragraph("阶段 3：智能化", styles["TableCell"]),
         Paragraph("10-24 个月", styles["TableCell"]),
         Paragraph("AI 比价 + 数字孪生 + ESG + 数据与经营同步", styles["TableCell"]),
         Paragraph("智能补货 + 碳排放报告 + 数字孪生 v1", styles["TableCell"])],
    ]
    rhythm_tbl = Table(rhythm_data, colWidths=[3 * cm, 2.5 * cm, 6 * cm, 5.5 * cm], repeatRows=1)
    rhythm_tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#5B9BD5")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F2F7FB")]),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BFBFBF")),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    flowables.append(rhythm_tbl)
    flowables.append(Spacer(1, 0.4 * cm))

    # 致谢
    flowables.append(Paragraph("四、版本与致谢", styles["H2"]))
    flowables.append(Paragraph(
        "<b>版本</b>：v1.0 · 2026-07-11<br/>"
        "<b>作者</b>：B166ER<br/>"
        "<b>出品</b>：ERIC的B166ER出品<br/>"
        "<b>配套交付</b>：13 份分章节 PDF + 工具清单 PDF + 思维导图 PNG（1x/2x）",
        styles["Normal"]
    ))
    flowables.append(Spacer(1, 0.4 * cm))
    flowables.append(Paragraph(
        "<i>本综合主报告整合了 13 章内容，是酒管公司供应链工程的\"母文档\"。"
        "每个章节可拆分为独立 SOP/工具/模板，按需取用。</i>",
        ParagraphStyle("AppQuote", parent=styles["Normal"],
                       fontName=CHINESE_FONT, fontSize=10, leading=16,
                       textColor=colors.HexColor("#555555"),
                       leftIndent=12, rightIndent=8,
                       backColor=colors.HexColor("#F8F8F8"),
                       borderColor=colors.HexColor("#1F4E79"),
                       borderWidth=0, leftBorderWidth=3,
                       borderPadding=6,
                       spaceBefore=8, spaceAfter=10,
        )
    ))

    return flowables


def main():
    # 装配全部内容
    all_flowables = []

    # 1. 封面
    all_flowables.extend(build_cover(styles))
    all_flowables.append(PageBreak())

    # 2. 目录
    all_flowables.extend(build_toc(styles))
    all_flowables.append(PageBreak())

    # 3. 章节（13 个）
    for i, (num, fname, title) in enumerate(CHAPTERS):
        md_path = os.path.join(PDF_DIR, fname)
        chapter_flows = build_chapter(num, md_path, title, styles, skip_first_h1=True)
        all_flowables.extend(chapter_flows)
        # 每章后分页
        all_flowables.append(PageBreak())

    # 4. 附录（使用指南）
    all_flowables.extend(build_usage_appendix(styles))

    # 构建 PDF
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title="酒管公司供应链工程全维度体系 v1.0",
        author="B166ER",
    )
    doc.build(
        all_flowables,
        onFirstPage=make_page_decorator("酒管公司供应链工程 · 综合主报告 v1.0"),
        onLaterPages=make_page_decorator("酒管公司供应链工程 · 综合主报告 v1.0"),
    )
    print(f"OK {OUTPUT}")
    print(f"Size: {os.path.getsize(OUTPUT):,} bytes")


if __name__ == "__main__":
    main()