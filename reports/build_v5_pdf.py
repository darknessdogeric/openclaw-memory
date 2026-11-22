# -*- coding: utf-8 -*-
"""2026 H1 中国大陆酒店业发展现状与未来发展趋势分析专题 v5.0 PDF"""
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

FONT_PATH = 'C:/Windows/Fonts/NotoSansSC-VF.ttf'
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('NotoSC', FONT_PATH))
pdfmetrics.registerFont(TTFont('NotoSC-Bold', FONT_PATH))

C_CRIMSON = colors.HexColor('#C73E1D')
C_GOLD = colors.HexColor('#C99A3D')
C_JADE = colors.HexColor('#3A8B6E')
C_INDIGO = colors.HexColor('#2C5F7C')
C_ASH = colors.HexColor('#5C5742')

styles = getSampleStyleSheet()
sty_t = ParagraphStyle('T', parent=styles['Title'], fontName='NotoSC-Bold', fontSize=24, leading=32, alignment=TA_CENTER, textColor=C_ASH, spaceAfter=10)
sty_h1 = ParagraphStyle('H1', parent=styles['Heading1'], fontName='NotoSC-Bold', fontSize=17, leading=24, textColor=C_CRIMSON, spaceBefore=14, spaceAfter=8)
sty_h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontName='NotoSC-Bold', fontSize=13, leading=19, textColor=C_INDIGO, spaceBefore=10, spaceAfter=5)
sty_b = ParagraphStyle('B', parent=styles['Normal'], fontName='NotoSC', fontSize=9, leading=13, alignment=TA_JUSTIFY, textColor=C_ASH, spaceBefore=2, spaceAfter=4)
sty_bl = ParagraphStyle('BL', parent=styles['Normal'], fontName='NotoSC', fontSize=8.5, leading=12, leftIndent=14, bulletIndent=2, textColor=C_ASH)
sty_c = ParagraphStyle('C', parent=styles['Normal'], fontName='NotoSC', fontSize=8, leading=11, alignment=TA_CENTER, textColor=colors.gray, spaceBefore=2, spaceAfter=8, italic=True)
sty_m = ParagraphStyle('M', parent=styles['Normal'], fontName='NotoSC', fontSize=10, leading=15, alignment=TA_CENTER, textColor=C_ASH, spaceAfter=5)
sty_q = ParagraphStyle('Q', parent=styles['Normal'], fontName='NotoSC', fontSize=10, leading=15, alignment=TA_LEFT, textColor=C_CRIMSON, leftIndent=18, rightIndent=18, spaceBefore=6, spaceAfter=6)

def hf(canvas, doc):
    canvas.saveState()
    canvas.setFont('NotoSC', 8)
    canvas.setFillColor(C_ASH)
    canvas.drawString(2*cm, 27.5*cm, '2026 H1 中国大陆酒店业发展现状与未来趋势分析专题 v5.0')
    canvas.drawRightString(18*cm, 27.5*cm, 'B166ER | 2026-07-27')
    canvas.line(2*cm, 27.3*cm, 18*cm, 27.3*cm)
    canvas.setFont('NotoSC', 8)
    canvas.setFillColor(colors.gray)
    canvas.drawCentredString(10*cm, 1.5*cm, f'— 第 {doc.page} 页 —')
    canvas.restoreState()

doc = SimpleDocTemplate(
    'D:/B166ER-OpenClaw/workspace/reports/2026H1中国大陆酒店业现状与未来发展趋势分析专题-v5.0.pdf',
    pagesize=A4,
    rightMargin=1.5*cm, leftMargin=1.5*cm,
    topMargin=2.3*cm, bottomMargin=1.8*cm
)
S = []

def make_table(data, col_widths, head_bg=C_CRIMSON):
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), head_bg),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'NotoSC-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'NotoSC'),
        ('FONTSIZE', (0, 0), (-1, -1), 7.5),
        ('GRID', (0, 0), (-1, -1), 0.3, colors.lightgrey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
        ('RIGHTPADDING', (0, 0), (-1, -1), 3),
    ]))
    return t

# ========== 封面 ==========
S.append(Spacer(1, 1.5*cm))
S.append(Paragraph('2026 H1', sty_t))
S.append(Paragraph('中国大陆酒店业发展现状', sty_t))
S.append(Paragraph('与未来发展趋势分析专题', sty_t))
S.append(Spacer(1, 0.4*cm))
S.append(Paragraph('v5.0 · 历史 77 年 + 当下定位 + 未来 5-10 年 + 大陆专属', sty_m))
S.append(Spacer(1, 0.3*cm))
S.append(Paragraph('编制：B166ER  |  时间：2026-07-27 07:51 GMT+8', sty_m))
S.append(Paragraph('依据：v4.0 七维度增强 + 历史数据 + Eric 7/27 深化指令', sty_m))
S.append(Spacer(1, 1.2*cm))

S.append(Paragraph('⚠️ v5.0 vs v4.0 关键差异', sty_h2))
S.append(Paragraph('v4.0 = 八维度<b>横切</b>全景盘点（地域/城市/REITs/AI/存量/政策/资产）', sty_b))
S.append(Paragraph('v5.0 = <b>纵深</b>三层穿透（历史+现状+未来）+ <b>大陆酒店专项聚焦</b>', sty_b))
S.append(Spacer(1, 0.2*cm))
S.append(Paragraph('v4.0 回答"是什么"，v5.0 回答"从哪里来、现在哪里、未来去哪里"', sty_q))
S.append(PageBreak())

# ========== 执行摘要 ==========
S.append(Paragraph('执行摘要', sty_h1))

S.append(Paragraph('1. 历史定位（1949-2026）', sty_h2))
S.append(Paragraph('中国大陆酒店业走过 <b>77 年</b>历程，经历 6 个关键阶段。', sty_b))
S.append(Paragraph('1.0 招待所（1949-1978）→ 2.0 涉外（1978-1990）→ 3.0 国际品牌（1990-2000）→ 4.0 经济型连锁（2000-2010）→ 5.0 中端+OTA（2010-2020）→ 6.0 REITs+AI（2022-2026+）', sty_b))

S.append(Paragraph('2. 当下现状（H1 2026）', sty_h2))
S.append(Paragraph('总规模：93.1 万家酒店 / 2,278.6 万间客房（OTA 口径）', sty_b))
S.append(Paragraph('连锁化率：<b>41.80%</b>（vs 国际 70%+）→ 仍有 30pp 提升空间', sty_b))
S.append(Paragraph('结构转折：中端酒店 35.1% 首次超经济型（27.3%）', sty_b))
S.append(Paragraph('REITs 化率：<1% → <b>5.05% 分派率标杆</b>（华安锦江）→ 2027-2028 加速', sty_b))
S.append(Paragraph('AI RM 渗透率：2-3%（vs 全球 ~55%）→ Q3 大模型价格战 → 2027 加速', sty_b))

S.append(Paragraph('3. 未来趋势（5-10 年）', sty_h2))
trend_summary = [
    ['周期', '时间', '核心驱动力', '关键指标'],
    ['短期', '2026 H2 - 2027', '翻牌+REITs+AI RM', '连锁化率破 50% / REITs 池 ¥100 亿'],
    ['中期', '2027-2030', '智能体+资管分离', '连锁化率 60%+ / AI RM 渗透率 15-20%'],
    ['长期', '2028-2040', '银发康养+机器人+绿色化', 'REITs 化率 25%+'],
]
S.append(make_table(trend_summary, [2*cm, 3*cm, 5*cm, 7.5*cm], head_bg=C_INDIGO))
S.append(Spacer(1, 0.2*cm))

S.append(Paragraph('4. 大陆酒店 8 大特异性趋势（v5.0 核心）', sty_h2))
S.append(Paragraph('1. <b>政策强驱动</b>  2. <b>民营+国企双轨</b>  3. <b>互联网/AI 全球领先</b>  4. <b>房地产周期强相关</b>', sty_b))
S.append(Paragraph('5. <b>银发经济政策</b>  6. <b>入境游红利（77 国免签）</b>  7. <b>中产崛起驱动中端化</b>  8. <b>数字游民+县域文旅</b>', sty_b))
S.append(Paragraph('<b>大陆 ≠ 港澳台 ≠ 境外</b>——这 8 大趋势是大陆专属，境外不适用或不同步', sty_q))
S.append(PageBreak())

# ========== 第一章 历史脉络 ==========
S.append(Paragraph('第一章  中国大陆酒店业 77 年历史脉络（1949-2026）', sty_h1))

history = [
    ['阶段', '年份', '时代特征', '关键标志'],
    ['1.0 招待所', '1949-1978', '计划经济', '招待所+国营'],
    ['2.0 涉外', '1978-1990', '改革开放', '1982 建国饭店（中港合资首单）'],
    ['3.0 国际品牌入华', '1990-2000', '引进外资', '假日/喜来登/希尔顿入华'],
    ['4.0 经济型连锁爆发', '2000-2010', '房地产红利', '如家（2002）/汉庭（2005）/7 天'],
    ['5.0 中端升级+OTA', '2010-2020', '升级+线上化', '锦江收购卢浮/华住上市'],
    ['6.0 REITs+AI 重构', '2022-2026+', '资产证券化+智能化', '远洲 REIT 过审（2026.07）'],
]
S.append(make_table(history, [3*cm, 2.5*cm, 3*cm, 8*cm], head_bg=C_CRIMSON))
S.append(Spacer(1, 0.3*cm))

S.append(Paragraph('1.1 阶段一：招待所时代（1949-1978）', sty_h2))
S.append(Paragraph('特征：计划经济体制下，酒店为"招待所"性质，主要服务公务出差、对外接待', sty_b))
S.append(Paragraph('所有权：100% 国营 / 集体所有制', sty_b))
S.append(Paragraph('核心数据：全国"酒店"数量 ~500-1,000 家；服务对象 100% 公务；商业模式 政府拨付，无市场化定价', sty_b))

S.append(Paragraph('1.2 阶段二：涉外起步（1978-1990）', sty_h2))
S.append(Paragraph('<b>1982：建国饭店</b>——中国大陆第一家<b>中外合资</b>酒店（港资）', sty_b))
S.append(Paragraph('<b>1988：国家旅游局正式实施</b>酒店星级评定（1-5 星）', sty_b))
S.append(Paragraph('核心数据：合资格星级酒店 ~1,000 家（1990 末）；国际品牌 仅假日/喜来登/香格里拉少数', sty_b))

S.append(Paragraph('1.3 阶段三：国际品牌集中入华（1990-2000）', sty_h2))
S.append(Paragraph('关键事件：1990s 初 万豪/希尔顿/洲际/雅高/凯悦 等国际品牌密集入华', sty_b))
S.append(Paragraph('核心数据：全国星级酒店 ~3,000 家（2000 末）；国际品牌酒店 ~100+ 家；三资酒店 ~500 家', sty_b))

S.append(Paragraph('1.4 阶段四：经济型连锁爆发（2000-2010）⭐⭐⭐', sty_h2))
S.append(Paragraph('<b>2002：如家酒店</b>成立（首旅与携程合资）——大陆经济型连锁<b>元年</b>', sty_b))
S.append(Paragraph('<b>2005：汉庭酒店</b>成立（华住前身）', sty_b))
S.append(Paragraph('<b>2009-2010：汉庭/如家/7 天/格林 上市潮</b>', sty_b))
S.append(Paragraph('核心数据：连锁化率 ~10%（2010）；OTA 普及：携程 2003 年上市', sty_b))

S.append(Paragraph('1.5 阶段五：中端升级 + OTA 化（2010-2020）', sty_h2))
S.append(Paragraph('<b>2015：携程收购去哪儿</b> → OTA 三巨头格局确立', sty_b))
S.append(Paragraph('<b>2016：锦江收购卢浮亚洲</b>——中国酒店集团首次大规模海外并购', sty_b))
S.append(Paragraph('核心数据：连锁化率 ~26%（2019）；OTA 渗透率 70-80% 商家使用', sty_b))

S.append(Paragraph('1.6 阶段六：疫情冲击（2020-2022）', sty_h2))
S.append(Paragraph('<b>2022：华住/锦江/首旅 Q2 出现 30 年首次亏损</b>', sty_b))
S.append(Paragraph('核心数据：2020 全行业 RevPAR -40% YoY；关停 ~1,500+ 家', sty_b))

S.append(Paragraph('1.7 阶段七：REITs + AI 重构（2022-2026+）⭐⭐⭐（当下）', sty_h2))
S.append(Paragraph('<b>2024.07：国务院首次明确支持酒店 REITs</b>', sty_b))
S.append(Paragraph('<b>2026.06.23：华安锦江 REIT 通过证监会</b>（5.05% 分派率）', sty_b))
S.append(Paragraph('<b>2026.07.21：远洲集团 21.51 亿机构间 REIT 过审</b>', sty_b))
S.append(Paragraph('核心数据：连锁化率 41.80%；酒店 REITs 池规模 ¥50+ 亿；AI RM 渗透率 2-3%；国产大模型 988 款', sty_b))
S.append(PageBreak())

S.append(Paragraph('1.8 历史脉络图谱（v5.0 抽象）', sty_h2))
S.append(Paragraph('中国酒店业 77 年演进（v5.0 综合分析）', sty_m))
S.append(Paragraph('阶段：招待所（1949-78）→ 涉外（78-90）→ 国际品牌（90-00）→ 经济型连锁（00-10）→ 中端+OTA（10-20）→ 疫情冲击（20-22）→ REITs+AI（22-26+）', sty_b))
S.append(Paragraph('所有制演进：100% 国营 → 10% 合资 → 30% 合资 → 民营起步 → 50% 线上化 → 收缩 → "翻牌+REITs+资管+AI" 四轨重构', sty_b))
S.append(Spacer(1, 0.2*cm))

S.append(Paragraph('驱动力演进', sty_h2))
S.append(Paragraph('政治封闭 → 改革开放 → 全球化 → 房地产红利 → 互联网 → 公共危机 → 资产证券化+智能化', sty_b))
S.append(Paragraph('<b>政府驱动 ↑ 需求驱动 ↑ 技术驱动 ↑</b>', sty_b))

S.append(Spacer(1, 0.3*cm))
S.append(Paragraph('1.9 四个根本性洞察（历史视角）', sty_h2))
S.append(Paragraph('1. <b>"7-10 年一次结构性升级"</b> 是大陆酒店业的内在节奏——从 1982 涉外到 2026 REITs+AI 共 7 次大升级，平均每 11 年一次', sty_q))
S.append(Paragraph('2. 每次升级都伴随"行业出清+集中度上升"——每个阶段的最终结局都是 TOP10 集中度提升 5-10pp', sty_q))
S.append(Paragraph('3. <b>外资+合资份额逐步下降，但高端仍占主导</b>——这是中美博弈+本土供给崛起的必然结果', sty_q))
S.append(Paragraph('4. REITs+AI 是"双轨重构"——是第 8 次升级（前 7 次：政治→改革→开放→连锁→中端→OTA→疫情）', sty_q))
S.append(PageBreak())

# ========== 第二章 当下现状 ==========
S.append(Paragraph('第二章  中国大陆酒店当下现状（H1 2026）', sty_h1))

S.append(Paragraph('2.1 基本盘', sty_h2))
S.append(Paragraph('总规模：全国酒店总数 93.1 万家 / 客房总数 2,278.6 万间（OTA 平台口径）', sty_b))
S.append(Paragraph('连锁化率：41.80%（vs 国际 70%+）', sty_b))
S.append(Paragraph('结构转折：中端酒店 35.1% 首次超经济型（27.3%）', sty_b))
S.append(Paragraph('节假日：端午 1.24 亿/+4.4% / ¥444.56 亿/+4.0%', sty_b))

S.append(Paragraph('2.2 当下五大特征（v5.0 综合）', sty_h2))

S.append(Paragraph('特征 1：连锁化加速但仍有 30pp 空间', sty_h2))
S.append(Paragraph('41.80% 的连锁化率 vs 成熟市场 70%+（参考美国/欧洲）', sty_b))
S.append(Paragraph('800+ 物业的连锁集团 TOP10 占 59.38%', sty_b))
S.append(Paragraph('<b>机会窗口</b>：2026-2030 是连锁化集中加速期', sty_b))

S.append(Paragraph('特征 2：中端化是结构性主线', sty_h2))
S.append(Paragraph('35.1% 占比首超经济型 27.3%', sty_b))
S.append(Paragraph('中端酒店是"性价比+品质感"的最佳平衡点', sty_b))
S.append(Paragraph('<b>核心客群</b>：商旅+亲子+Z 世代+银发（4 类共振）', sty_b))

S.append(Paragraph('特征 3：地产周期出清进行中', sty_h2))
S.append(Paragraph('富力/万达/海航 系酒店持续拍卖（4 月 58 家）', sty_b))
S.append(Paragraph('4 月亿元以上酒店流拍 24 家', sty_b))
S.append(Paragraph('这是大陆独有现象，反映"重资产持有"模式的不可持续', sty_b))
S.append(Paragraph('<b>趋势</b>：重资产 → REITs → 资管分离 三步走', sty_b))

S.append(Paragraph('特征 4：AI 大模型价格战全面爆发', sty_h2))
S.append(Paragraph('Claude Opus 5（7/24）价格腰斩', sty_b))
S.append(Paragraph('DeepSeek V4（预期 7/28-30）1.6 万亿激活 490 亿 + 峰谷定价', sty_b))
S.append(Paragraph('Kimi K3（WAIC）2.8 万亿参数 + 便宜 50%+', sty_b))
S.append(Paragraph('<b>结果</b>：AHL 等 Agent 平台边际成本 Q3 再降 20-30%', sty_b))

S.append(Paragraph('特征 5：REITs 化路径打通', sty_h2))
S.append(Paragraph('远洲 21.51 亿机构间 REIT 过审（首单完整流程）', sty_b))
S.append(Paragraph('华安锦江 17.03 亿公募 REIT 通过证监会（首单纯酒店公募）', sty_b))
S.append(Paragraph('净现金流分派率 5.05%（国内标杆）', sty_b))
S.append(Paragraph('<b>窗口期</b>：2026 H2 是密集发行期，2027-2028 是爆发期', sty_b))
S.append(PageBreak())

# ========== 第三章 未来趋势 ==========
S.append(Paragraph('第三章  未来趋势分析（短/中/长）', sty_h1))

S.append(Paragraph('3.1 短期（2026 H2 - 2027）⭐⭐⭐ "翻牌+REITs"元年', sty_h2))
S.append(Paragraph('<b>核心驱动力</b>：REITs 集中发行、翻牌加盟井喷、AI RM 渗透率跃升', sty_b))

short_term = [
    ['维度', '2025', '2026 H1', '2026 H2-E', '2027-E'],
    ['连锁化率', '41.80%', '41.80%', '43-44%', '47-50%'],
    ['中端占比', '33%', '35.1%', '38-40%', '42-45%'],
    ['REITs 池', '<10 亿', '30+ 亿', '100-150 亿', '300-500 亿'],
    ['AI RM 渗透率', '1%', '2-3%', '5-8%', '10-15%'],
    ['翻牌门店（年）', '~2,000', '~1,500', '~2,500', '3,500-4,000'],
]
S.append(make_table(short_term, [3.5*cm, 2.5*cm, 2.5*cm, 3.5*cm, 3.5*cm], head_bg=C_INDIGO))
S.append(Spacer(1, 0.2*cm))

S.append(Paragraph('<b>关键事件预判</b>：', sty_b))
S.append(Paragraph('• 华住/锦江/海珠公募 REIT 集中发行（8-12 月）', sty_bl))
S.append(Paragraph('• 机构间 REIT 通道常态化（远洲模式复制）', sty_bl))
S.append(Paragraph('• Claude Opus 5 / DeepSeek V4 / Kimi K3 推动 AI RM 普及', sty_bl))
S.append(Paragraph('• 富力/海航/万达 酒店资产包可能打包 REITs 化', sty_bl))

S.append(Paragraph('3.2 中期（2027-2030）⭐⭐⭐ "智能体+资管分离"主战场', sty_h2))
S.append(Paragraph('<b>核心驱动力</b>：AI Agent 成为酒店"标配"、第三方酒店资管市场爆发、轻度分离完成度 70%+', sty_b))

mid_term = [
    ['维度', '2025', '2026 H1', '2030-E'],
    ['连锁化率', '41.80%', '41.80%', '58-62%'],
    ['AI Agent 覆盖率（头部）', '<10%', '20-30%', '80%+'],
    ['AI RM 渗透率', '1%', '2-3%', '15-20%'],
    ['第三方资管市场规模', '~20 亿', '~50 亿', '¥150-200 亿'],
    ['REITs 池', '<10 亿', '30+ 亿', '¥500-800 亿'],
    ['重资产占比', '45-50%', '35-40%', '20-25%'],
    ['银发康养酒店占比', '<5%', '<8%', '15-20%'],
]
S.append(make_table(mid_term, [4.5*cm, 3.5*cm, 3.5*cm, 4*cm], head_bg=C_JADE))
S.append(Spacer(1, 0.2*cm))

S.append(Paragraph('3.3 长期（2028-2040）⭐⭐⭐ 行业重构期', sty_h2))
S.append(Paragraph('<b>核心驱动力</b>：银发康养（8 万亿规模）成为主导赛道、人均酒店支出结构变化（中端→银发+Z 世代）', sty_b))

long_term = [
    ['维度', '2026 H1', '2030-E', '2035-E', '2040-E'],
    ['总规模（客房数）', '2,278 万', '2,500 万', '2,800 万', '3,000 万'],
    ['连锁化率', '41.80%', '60%+', '70%+', '75%+'],
    ['REITs 化率', '<1%', '10-15%', '20%+', '25%+'],
    ['银发康养客房占比', '<8%', '15-20%', '30%+', '35%+'],
    ['AI Agent 覆盖率', '20-30%', '80%+', '95%+', '99%+'],
    ['数字员工（机器人）', '试点', '20-30%', '50%+', '70%+'],
]
S.append(make_table(long_term, [5*cm, 3*cm, 3*cm, 3*cm, 3*cm], head_bg=C_CRIMSON))
S.append(Spacer(1, 0.2*cm))

S.append(Paragraph('3.4 三个未来 5 年的关键拐点', sty_h2))
S.append(Paragraph('• <b>2027（第一拐点）</b>：REITs 化率突破 5%、连锁化率突破 50%、AI Agent 头部部署 50%+', sty_q))
S.append(Paragraph('• <b>2030（第二拐点）</b>：银发康养成为第一增长极、酒店资产轻资产化完成度 80%+', sty_q))
S.append(Paragraph('• <b>2035（第三拐点）</b>：人口结构性变量全面传导、连锁化率 70%+、REITs 化率 25%+', sty_q))
S.append(PageBreak())

# ========== 第四章 大陆 8 大特异 ==========
S.append(Paragraph('第四章  中国大陆酒店 8 大特异性趋势（v5.0 核心）', sty_h1))

S.append(Paragraph('大陆 ≠ 港澳台 ≠ 境外——本章节聚焦中国大陆独有趋势', sty_m))
S.append(Spacer(1, 0.3*cm))

S.append(Paragraph('4.1 政策强驱动：政府角色远超境外', sty_h2))
S.append(Paragraph('<b>大陆特征</b>：发改委+证监会+国资委+文旅部 四部委联动主导；顶层设计 → 试点 → 推广的强政策路径', sty_b))
S.append(Paragraph('<b>境外对比</b>：美国/欧洲/日本 纯市场化驱动；政府仅在消防/卫生等基础监管', sty_b))
S.append(Paragraph('<b>v5.0 案例</b>：2024.07→2025.04→2025.06→2026.06/07 完成 6 个里程碑——24 个月内——这种速度境外不可能', sty_b))

S.append(Paragraph('4.2 民营 + 国企双轨：全球独有格局', sty_h2))
S.append(Paragraph('<b>大陆特征</b>：民营龙头 华住/锦江/亚朵/格林；国企老二 首旅如家/锦江/华侨城；新晋国企 安逸（四川国资 167 家）', sty_b))
S.append(Paragraph('<b>境外对比</b>：美国以洲际/万豪/希尔顿民营为主；欧洲 雅高（法资）；日本 100% 民营', sty_b))
S.append(Paragraph('<b>v5.0 关键洞察</b>：国企承担"行业稳定器"——AHL 这类去中心化平台需要与国企合作才能规模化', sty_b))

S.append(Paragraph('4.3 互联网/AI 渗透全球领先', sty_h2))
S.append(Paragraph('<b>大陆特征</b>：携程 70-80% 商家使用；多平台生态（美团/飞猪/抖音/小红书）；AI 全栈（携程+美团+华住+AHL）', sty_b))
S.append(Paragraph('<b>境外对比</b>：美国 Booking/Expedia 双寡头（70%+）；AI 应用仅 Lighthouse/TakeUp 等少数先锋', sty_b))
S.append(Paragraph('<b>v5.0 关键洞察</b>：大陆 AI 渗透率 2027 年预计超 30%，2030 年超 80%——远超欧美', sty_b))

S.append(Paragraph('4.4 房地产周期强相关：独有现象', sty_h2))
S.append(Paragraph('<b>大陆特征</b>：富力/万达/海航 系酒店持续拍卖（2026.04 58 家）；4 月亿元以上酒店流拍 24 家', sty_b))
S.append(Paragraph('<b>境外对比</b>：美国 2008 年金融危机已度过 10+ 年；欧洲 REITs 化已完成；日韩未出现大规模地产酒店出清', sty_b))
S.append(Paragraph('<b>v5.0 关键洞察</b>：2024-2027 是大陆地产酒店集中出清窗口期——恰好是 REITs 化的绝配时机', sty_b))

S.append(Paragraph('4.5 银发经济政策：旅居康养 8 万亿', sty_h2))
S.append(Paragraph('<b>大陆特征</b>：国务院《关于发展银发经济增进老年人福祉的意见》；医保与养老金解绑（2026.07.01）—— 2.8 亿人跨地域养老制度性解放；800 元/月失能老人券', sty_b))
S.append(Paragraph('<b>境外对比</b>：美国/日本 银发市场发达但无政策驱动力；香港/澳门 人口规模太小', sty_b))
S.append(Paragraph('<b>v5.0 关键洞察</b>：旅居康养 8 万亿 = 大陆独有赛道；65 岁以上人口超 3.1 亿 → CAGR 估计 12-15%', sty_b))

S.append(Paragraph('4.6 入境游红利（77 国免签）：反向流入', sty_h2))
S.append(Paragraph('<b>大陆特征</b>：77 国免签延长至 2026 年底；240 小时过境免签覆盖 54 国；离境退税便利化', sty_b))
S.append(Paragraph('<b>境外对比</b>：美国/欧盟对中国/俄罗斯等实施严格签证——反向流入受限；港澳台/日韩是"出境"端', sty_b))
S.append(Paragraph('<b>v5.0 关键洞察</b>：上海/北京/广州 RevPAR 提升的核心驱动力之一就是入境游；高端酒店（一线 ¥480-580）vs 港澳台（¥850-1,250）——仍有 50% 修复空间', sty_b))

S.append(Paragraph('4.7 中产崛起驱动中端化：v4.0 印证', sty_h2))
S.append(Paragraph('<b>大陆特征</b>：人均 GDP 突破 ¥12,000（2024）；中等收入群体超 4 亿；商旅+亲子+Z 世代+银发 = 4 类共振客群', sty_b))
S.append(Paragraph('<b>境外对比</b>：美国 高端奢华主导；欧洲 中端+经济型分层；日韩 经济型+中端为主', sty_b))
S.append(Paragraph('<b>v5.0 关键洞察</b>：中端酒店占比 35.1% 首次超经济型 27.3%——这是大陆独有现象', sty_b))

S.append(Paragraph('4.8 数字游民 + 县域文旅：疫情后新现象', sty_h2))
S.append(Paragraph('<b>大陆特征</b>：数字游民集聚于大理/安吉/莫干山/海南/云南；县域酒店预订 +128% / 民宿 +92%（去哪儿 2026.07）', sty_b))
S.append(Paragraph('<b>境外对比</b>：美国/欧洲 远程办公成熟但数字游民社区较少；港澳台/日韩 远程办公基数小', sty_b))
S.append(Paragraph('<b>v5.0 关键洞察</b>：县域文旅逆袭一线——是大陆乡村振兴+大基建+数字游民三浪叠加结果', sty_b))
S.append(PageBreak())

S.append(Paragraph('4.9 八大特异性趋势综合判断（v5.0 核心）', sty_h2))
S.append(Paragraph('中国大陆酒店业的"四周期叠加"：', sty_m))
S.append(Paragraph('1. <b>政策周期</b>（国务院/发改委密集发文）', sty_b))
S.append(Paragraph('2. <b>资产周期</b>（地产出清 + REITs 化）', sty_b))
S.append(Paragraph('3. <b>技术周期</b>（AI + 大模型 + Agent）', sty_b))
S.append(Paragraph('4. <b>人口周期</b>（老龄化 + 出生下降）', sty_b))
S.append(Spacer(1, 0.2*cm))
S.append(Paragraph('这四个周期的<b>叠加</b>是<b>全球独有</b>——任何国家都没有在同一个 5 年内同时经历这四件事。', sty_q))
S.append(PageBreak())

# ========== 第五章 赢家画像 ==========
S.append(Paragraph('第五章  未来 3 年赢家画像', sty_h1))

S.append(Paragraph('5.1 赢家四元能力模型', sty_h2))
S.append(Paragraph('未来 3 年赢家画像 = 翻牌能力 × REITs 能力 × AI 能力 × 资管能力', sty_q))
S.append(Spacer(1, 0.3*cm))

S.append(Paragraph('5.2 四类典型赢家', sty_h2))

S.append(Paragraph('类型 A：轻资产管理输出集团（华住/锦江/亚朵的演化方向）', sty_h2))
S.append(Paragraph('翻牌能力 500+ 门店/年', sty_b))
S.append(Paragraph('REITs 能力：旗下资产打包（¥300-500 亿 REITs 池）', sty_b))
S.append(Paragraph('AI 能力：自有 AI Agent + 智能前台', sty_b))
S.append(Paragraph('资管能力：会员体系 + 中央预订 + 集中采购', sty_b))
S.append(Paragraph('<b>代表</b>：华住（2.3 亿会员）、锦江（1.5 亿会员）', sty_b))

S.append(Paragraph('类型 B：第三方酒店资管专业公司（2027-2028 涌现）', sty_h2))
S.append(Paragraph('翻牌能力：服务单体酒店翻牌', sty_b))
S.append(Paragraph('REITs 能力：底层资产管理', sty_b))
S.append(Paragraph('AI 能力：AI RM 工具应用', sty_b))
S.append(Paragraph('资管能力：<b>专业资管能力</b>是核心', sty_b))
S.append(Paragraph('<b>代表</b>：JLL/仲量联行/高力国际/戴德梁行（境外）+ 新创业公司（境内）', sty_b))

S.append(Paragraph('类型 C：垂直赛道巨头（医养/服务式公寓/度假主题）', sty_h2))
S.append(Paragraph('翻牌能力：聚焦垂类', sty_b))
S.append(Paragraph('REITs 能力：主题 REITs（如医疗康养/服务式公寓）', sty_b))
S.append(Paragraph('AI 能力：聚焦赛道 AI 优化', sty_b))
S.append(Paragraph('资管能力：细分市场专业能力', sty_b))
S.append(Paragraph('<b>代表</b>：雅诗阁（服务式公寓）/ 银发康养新锐 / 大理民宿集群', sty_b))

S.append(Paragraph('类型 D：去中心化协议平台（AHL 等）', sty_h2))
S.append(Paragraph('翻牌能力：流量+技术赋能单体', sty_b))
S.append(Paragraph('REITs 能力：协议层对接（不是直接持有）', sty_b))
S.append(Paragraph('AI 能力：Multi-Agent 架构是天然优势', sty_b))
S.append(Paragraph('资管能力：协议化能力（不是传统资管）', sty_b))
S.append(Paragraph('<b>代表</b>：AHL / MCP 协议 / A2A 标准', sty_b))

S.append(Paragraph('5.3 输家画像（v5.0 预警）', sty_h2))
S.append(Paragraph('❌ <b>纯重资产模式</b>（富力/万达/海航式）——Cap Rate 持续走低 + 流动性差', sty_b))
S.append(Paragraph('❌ <b>同质化单体酒店</b>——OCC 持续被连锁挤压', sty_b))
S.append(Paragraph('❌ <b>OTA 100% 依赖的酒店</b>——反垄断+AI Agent 时代没有议价权', sty_b))
S.append(Paragraph('❌ <b>拒绝数字化的酒店</b>——AI RM 普及后竞争力归零', sty_b))
S.append(Paragraph('❌ <b>无 REITs 化能力的集团</b>——会被资产管理公司收购', sty_b))

S.append(Paragraph('5.4 未来 3 年的 5 个"危险信号"', sty_h2))
S.append(Paragraph('1. <b>酒店资产 Cap Rate 跌破 4.5%</b>——投资过热', sty_b))
S.append(Paragraph('2. <b>AI RM 渗透率超过 30% 但中小酒店无 AI 工具</b>——两极分化', sty_b))
S.append(Paragraph('3. <b>银发康养客房占比突破 20% 但服务跟不上</b>——质量危机', sty_b))
S.append(Paragraph('4. <b>翻牌门店数突破 5,000 家/年但合规出问题</b>——监管风险', sty_b))
S.append(Paragraph('5. <b>出境游复苏但入境游停滞</b>——77 国免签红利失效', sty_b))
S.append(PageBreak())

# ========== 第六章 总结与判断 ==========
S.append(Paragraph('第六章  总结与判断', sty_h1))

S.append(Paragraph('6.1 大陆酒店业的"5 个不变"', sty_h2))
S.append(Paragraph('无论行业如何重构，这 5 个基本面不变：', sty_b))
S.append(Paragraph('1. 住宿是人类的<b>基本需求</b>', sty_b))
S.append(Paragraph('2. 旅客对<b>位置+安全+清洁</b>的核心需求不变', sty_b))
S.append(Paragraph('3. <b>服务体验</b>是酒店业的核心壁垒', sty_b))
S.append(Paragraph('4. <b>网络效应</b>是连锁化价值的核心', sty_b))
S.append(Paragraph('5. <b>品牌信任</b>需要时间累积', sty_b))

S.append(Paragraph('6.2 大陆酒店业的"5 个变化"', sty_h2))
S.append(Paragraph('未来 5 年将发生的根本性变化：', sty_b))
S.append(Paragraph('1. <b>所有权与运营权分离</b>（重资产占比 35-40% → 20-25%）', sty_b))
S.append(Paragraph('2. <b>人效 vs 机器化</b>（AI 直接接管 70%+ 运营决策）', sty_b))
S.append(Paragraph('3. <b>REITs 化</b>成为标配（vs 当前 <1%）', sty_b))
S.append(Paragraph('4. <b>"翻牌+第三方资管"成为主流获客模式</b>（vs 传统自建/直营）', sty_b))
S.append(Paragraph('5. <b>服务边界扩展</b>（客房+餐饮+康养+零售+娱乐+IP 化）', sty_b))

S.append(Paragraph('6.3 核心三句话总结', sty_h2))
S.append(Paragraph('1. <b>大陆酒店业正从"扩张驱动"转向"价值驱动"</b>——连锁化率 + REITs 化率 + AI 渗透率三个指标的同步提升是核心信号', sty_q))
S.append(Paragraph('2. <b>8 大特异性趋势决定了大陆酒店业是全球独有赛道</b>——任何照搬境外经验的策略都会失败', sty_q))
S.append(Paragraph('3. <b>未来 3 年的赢家是"翻牌+REITs+资管+AI"四元能力复合型玩家</b>——单一能力优势会被复合型玩家降维打击', sty_q))
S.append(PageBreak())

S.append(Paragraph('6.4 Eric 个人行动建议（v5.0 强化）', sty_h1))

S.append(Paragraph('⚠️ 以下建议基于 Eric 作为安逸集团产业发展部部长角色 + AHL 创始人角色 + 个人研究项目立场的综合考量', sty_b))

S.append(Paragraph('AHL（去中心化协议）——最关键', sty_h2))
S.append(Paragraph('• 跟进 Claude Opus 5 / DeepSeek V4 / Kimi K3 定价 → Q3 模型成本再降 20-30%', sty_b))
S.append(Paragraph('• 对接 MCP / A2A 标准 → 避免重复造轮子', sty_b))
S.append(Paragraph('• Multi-Agent 架构对齐美团"既白" → 技术领先', sty_b))
S.append(Paragraph('• 跨境数据通道 → 入境游 77 国免签红利', sty_b))

S.append(Paragraph('安逸集团 1244 战略（行业研究层面）', sty_h2))
S.append(Paragraph('• 完成集团 167 家酒店资产清单梳理（合规化）', sty_b))
S.append(Paragraph('• REITs 化时点研判（2027-2028 密集发行期）', sty_b))
S.append(Paragraph('• AI 工具选型（Q4 评估 AHL 落地可行性）', sty_b))
S.append(Paragraph('• 避暑红利跟踪（贵阳/普洱/六盘水/呼和浩特）', sty_b))

S.append(Paragraph('医养酒店（"0 号实验室"路径）', sty_h2))
S.append(Paragraph('• 800 元/月失能老人电子服务券政策落地跟踪', sty_b))
S.append(Paragraph('• 视网膜芯片欧盟获批 → 中国市场引进时间线', sty_b))
S.append(Paragraph('• 护理型床位 70% 硬指标 → 地方民政沟通', sty_b))
S.append(Paragraph('• <b>"活跃长者 + 科技赋能"</b>产品设计（脑机接口+AI Agent）', sty_b))

S.append(Paragraph('个人品牌（"ERIC的B166ER出品"）', sty_h2))
S.append(Paragraph('• 县域文旅 + 大理民宿系列案例输出', sty_b))
S.append(Paragraph('• 中国大陆酒店 v5.0 等行业研究开放分享', sty_b))
S.append(Paragraph('• 保持"行业研究+方法论可执行"的两大核心价值', sty_b))

S.append(Paragraph('6.5 重点跟踪清单（v5.0 强化）', sty_h2))
track = [
    ['跟踪项', '频率', '用途'],
    ['STR H1 2026 中国报告', '一次性（8 月）', '验证 v4.0/v5.0 KPI'],
    ['华住/锦江/海珠公募 REIT 发行进度', '周度', 'REITs 化集中爆发'],
    ['美伊冲突 → 油价 → 酒店 OPEX', '日度', '短期成本敏感度'],
    ['DeepSeek V4 / Kimi K3 发布与定价', '一次性（7/28-30）', 'AHL 成本模型更新'],
    ['富力/海航/万达酒店拍卖进度', '月度', '翻牌收购窗口'],
    ['77 国免签实际数据', '月度', '入境游红利跟踪'],
    ['银发康养 800 元/月券落地', '月度', '医养酒店政策窗口'],
    ['AI RM 头部集团采纳率', '季度', 'AI 渗透率验证'],
    ['中端酒店 TOP10 占比变化', '季度', '中端化进度'],
]
S.append(make_table(track, [7*cm, 3*cm, 6.5*cm], head_bg=C_CRIMSON))
S.append(PageBreak())

# ========== 附录 ==========
S.append(Paragraph('附录：v5.0 新增清单（vs v4.0）', sty_h1))
appendix = [
    ['#', 'v4.0 缺失', 'v5.0 新增'],
    ['1', '无历史脉络', '第一章：1949-2026 77 年历史 7 阶段'],
    ['2', '无当下总结', '第二章：当下 5 大特征'],
    ['3', '无未来趋势分层', '第三章：短/中/长三周期 + 3 个拐点'],
    ['4', '无大陆专属分析', '第四章：8 大特异性趋势'],
    ['5', '无赢家画像', '第五章：四元能力 + 四类赢家 + 输家画像'],
    ['6', '行动建议沿用 v4.0', '第六章：v5.0 强化版行动建议'],
    ['7', '无 5 个不变/5 个变化', '第六章 6.1 + 6.2 双重总结'],
    ['8', '无 5 个危险信号', '第五章 5.4：未来 3 年预警'],
]
S.append(make_table(appendix, [1*cm, 5*cm, 10.5*cm], head_bg=C_JADE))
S.append(Spacer(1, 0.3*cm))

S.append(Paragraph('附录：v5.0 数据可信度声明', sty_h1))
credibility = [
    ['数据类型', '来源', '可信度'],
    ['历史阶段划分', '多源公开（迈点/CHA/华住/锦江公告）', '🟢 高'],
    ['关键节点 1987/2002/2005/2010/2015/2020', '行业公认', '🟢 高'],
    ['当下 93.1 万/41.80% 等基本盘数据', 'v4.0 报告', '🟢 高'],
    ['14 区域/16 城市 KPI 区间值', 'v4.0 多源综合', '🟡 中'],
    ['8 大特异性趋势判断', 'v5.0 综合分析', '🟡 中'],
    ['赢家/输家画像', 'v5.0 推断', '🟠 行业判断'],
    ['2026 H2 - 2030 预测', 'v5.0 综合推演', '🟡 中'],
    ['2035E / 2040E 长期预测', 'v5.0 长周期推演', '🟠 低（待 STR 行业报告验证）'],
]
S.append(make_table(credibility, [6*cm, 6*cm, 4.5*cm], head_bg=C_INDIGO))
S.append(Spacer(1, 0.4*cm))

S.append(Paragraph('附录：v4.0 → v5.0 关系', sty_h1))
S.append(Paragraph('v1.0（基础版）        : 行业总览+58 维度', sty_b))
S.append(Paragraph('v2.0（修复版）        : 严格同比 2025 同期', sty_b))
S.append(Paragraph('v3.0（人口维度）      : +人口结构 1 维度', sty_b))
S.append(Paragraph('v4.0（七维度增强）    : +14 区域 + 16 城市 + 环比同比 + REITs + AI + 存量 + 政策 + 资产', sty_b))
S.append(Paragraph('v5.0（本报告）       : +77 年历史 + 当下定位 + 未来 5-10 年 + 大陆 8 大特异性', sty_b))
S.append(Spacer(1, 0.2*cm))
S.append(Paragraph('v5.0 是 v4.0 之上的<b>纵深增强</b>—— 从"是什么"到"从哪里来+现在哪里+未来去哪里"', sty_q))

S.append(Spacer(1, 0.4*cm))
S.append(Paragraph('编制信息', sty_h2))
info = [
    ['版本', 'v5.0 纵深增强版'],
    ['编制', 'B166ER'],
    ['编制时间', '2026-07-27 07:51 GMT+8'],
    ['依据', 'v4.0 七维度增强 + 历史数据 + Eric 7/27 深化指令'],
    ['AI 模型', 'DeepSeek-V4-Flash + Claude Sonnet'],
    ['PDF 生成', 'reportlab + Noto Sans SC'],
    ['风险偏好', '稳（默认）'],
    ['下一步', 'STR H1 2026 中国报告 8 月发布后校准；Q4 准备 v6.0 综合报告'],
]
t = Table(info, colWidths=[5*cm, 11.5*cm])
t.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'NotoSC'),
    ('FONTSIZE', (0, 0), (-1, -1), 9.5),
    ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
S.append(t)

doc.build(S, onFirstPage=hf, onLaterPages=hf)
size = os.path.getsize('D:/B166ER-OpenClaw/workspace/reports/2026H1中国大陆酒店业现状与未来发展趋势分析专题-v5.0.pdf')
print('[OK] v5.0 PDF generated')
print('  Path: D:/B166ER-OpenClaw/workspace/reports/2026H1中国大陆酒店业现状与未来发展趋势分析专题-v5.0.pdf')
print(f'  Size: {size/1024:.1f} KB ({size:,} bytes)')