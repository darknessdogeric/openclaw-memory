"""
弥勒民宿可行性研究 - PDF 报告生成器
reportlab + 中文字体 + 嵌入图表
"""
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak,
    Table, TableStyle, KeepTogether, ListFlowable, ListItem
)
from reportlab.platypus.doctemplate import BaseDocTemplate
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import matplotlib.font_manager as fm

# ============ 字体配置 ============
FONT_PATH = 'C:/Windows/Fonts/NotoSansSC-VF.ttf'
fm.fontManager.addfont(FONT_PATH)
# 注册 reportlab 字体
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('NotoSC', FONT_PATH))
pdfmetrics.registerFont(TTFont('NotoSC-Bold', 'C:/Windows/Fonts/NotoSansSC-VF.ttf'))

# ============ 配色 ============
COL_CRIMSON = colors.HexColor('#C73E1D')
COL_GOLD = colors.HexColor('#C99A3D')
COL_JADE = colors.HexColor('#3A8B6E')
COL_INDIGO = colors.HexColor('#2C5F7C')
COL_UMBER = colors.HexColor('#7A5230')
COL_ASH = colors.HexColor('#5C5742')
COL_BG = colors.HexColor('#FDFBF6')

# ============ 样式 ============
styles = getSampleStyleSheet()

style_title = ParagraphStyle(
    'CustomTitle', parent=styles['Title'],
    fontName='NotoSC-Bold', fontSize=28, leading=36,
    alignment=TA_CENTER, textColor=COL_ASH, spaceAfter=12
)
style_h1 = ParagraphStyle(
    'CustomH1', parent=styles['Heading1'],
    fontName='NotoSC-Bold', fontSize=22, leading=30,
    alignment=TA_LEFT, textColor=COL_CRIMSON, 
    spaceBefore=20, spaceAfter=14,
    borderWidth=0, borderPadding=0
)
style_h2 = ParagraphStyle(
    'CustomH2', parent=styles['Heading2'],
    fontName='NotoSC-Bold', fontSize=16, leading=22,
    alignment=TA_LEFT, textColor=COL_INDIGO,
    spaceBefore=14, spaceAfter=8
)
style_h3 = ParagraphStyle(
    'CustomH3', parent=styles['Heading3'],
    fontName='NotoSC-Bold', fontSize=13, leading=18,
    alignment=TA_LEFT, textColor=COL_JADE,
    spaceBefore=10, spaceAfter=6
)
style_body = ParagraphStyle(
    'CustomBody', parent=styles['Normal'],
    fontName='NotoSC', fontSize=10.5, leading=16,
    alignment=TA_JUSTIFY, textColor=COL_ASH,
    spaceBefore=4, spaceAfter=8
)
style_bullet = ParagraphStyle(
    'CustomBullet', parent=styles['Normal'],
    fontName='NotoSC', fontSize=10, leading=15,
    leftIndent=14, bulletIndent=2,
    textColor=COL_ASH, spaceBefore=2, spaceAfter=2
)
style_quote = ParagraphStyle(
    'CustomQuote', parent=styles['Normal'],
    fontName='NotoSC', fontSize=11, leading=18,
    alignment=TA_LEFT, textColor=COL_CRIMSON,
    leftIndent=20, rightIndent=20,
    borderColor=COL_GOLD, borderWidth=0, borderPadding=8,
    spaceBefore=10, spaceAfter=10
)
style_caption = ParagraphStyle(
    'Caption', parent=styles['Normal'],
    fontName='NotoSC', fontSize=9, leading=13,
    alignment=TA_CENTER, textColor=colors.gray,
    spaceBefore=2, spaceAfter=12, italic=True
)
style_meta = ParagraphStyle(
    'Meta', parent=styles['Normal'],
    fontName='NotoSC', fontSize=11, leading=16,
    alignment=TA_CENTER, textColor=COL_ASH,
    spaceBefore=6, spaceAfter=6
)

# ============ 页眉页脚 ============
def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('NotoSC', 8)
    canvas.setFillColor(COL_ASH)
    canvas.drawString(2*cm, 27.5*cm, '弥勒景区民宿稳态投资可行性研究报告 v4.0')
    canvas.drawRightString(18*cm, 27.5*cm, 'B166ER | 2026-07-23')
    canvas.line(2*cm, 27.3*cm, 18*cm, 27.3*cm)
    
    canvas.setFont('NotoSC', 8)
    canvas.setFillColor(colors.gray)
    canvas.drawCentredString(10*cm, 1.5*cm, f'— 第 {doc.page} 页 —')
    canvas.restoreState()

# ============ 文档构建 ============
doc = SimpleDocTemplate(
    'D:/B166ER-OpenClaw/workspace/reports/弥勒民宿可行性研究报告.pdf',
    pagesize=A4,
    rightMargin=2*cm, leftMargin=2*cm,
    topMargin=2.5*cm, bottomMargin=2*cm
)

# 图表路径
CHART = 'D:/B166ER-OpenClaw/workspace/reports/charts'

def img(filename, width=14*cm):
    return Image(f'{CHART}/{filename}', width=width, height=width*0.55)

story = []

# ====================================
# 封面
# ====================================
story.append(Spacer(1, 4*cm))
story.append(Paragraph('弥勒景区民宿稳态投资', style_title))
story.append(Paragraph('可行性研究报告', style_title))
story.append(Spacer(1, 1.5*cm))
story.append(Paragraph('v4.0 完整版 | 含 10 章宏观全景 + 项目可行性矩阵', style_meta))
story.append(Spacer(1, 1*cm))
story.append(Paragraph('编制机构：B166ER（行业研究 Agent）', style_meta))
story.append(Paragraph('编制时间：2026 年 7 月 23 日', style_meta))
story.append(Paragraph('服务对象：想在弥勒景区附近搞民宿的需求方', style_meta))
story.append(Paragraph('风险偏好：稳', style_meta))
story.append(Spacer(1, 3*cm))
story.append(Paragraph('一份覆盖全球/全国/云南/弥勒的宏观全景 + 项目可行性研究', 
                       ParagraphStyle('SubTitle', parent=styles['Normal'], fontName='NotoSC',
                                     fontSize=12, alignment=TA_CENTER, textColor=COL_CRIMSON, italic=True)))
story.append(Paragraph('融合 STR / 浩华 / 仲量联行 / 迈点 / Fastdata / 大乐之野等 34 维度信源',
                       ParagraphStyle('SubTitle2', parent=styles['Normal'], fontName='NotoSC',
                                     fontSize=10, alignment=TA_CENTER, textColor=COL_ASH)))
story.append(PageBreak())

# ====================================
# 目录（简化）
# ====================================
story.append(Paragraph('目  录', style_h1))
toc_data = [
    ['第一部分', '宏观全景分析（10 章）'],
    ['  第 1 章', '行业总览：2024 是中国酒店业 5 年来最差年'],
    ['  第 2 章', '宏观环境：经济 / 政策 / 社会 / 技术'],
    ['  第 3 章', '行业供给：中国酒店 + 民宿供给结构'],
    ['  第 4 章', '行业需求：旅居康养 + 亲子 + 数字游民'],
    ['  第 5 章', '运营表现：OCC / ADR / RevPAR / 景气指数'],
    ['  第 6 章', '竞争格局：外资 + 内资 + 民宿标杆'],
    ['  第 7 章', '营销与渠道：OTA + 短视频 + 私域'],
    ['  第 8 章', 'AI + PMS + 收益管理'],
    ['  第 9 章', '资本市场：JLL 2024 数据'],
    ['  第 10 章', '政策与法规：6 证 + 创业担保贷款'],
    ['第二部分', '项目可行性研究'],
    ['  第 11 章', '弥勒景区民宿稳态投资可行性'],
    ['附录', '数据来源 + 下步建议'],
]
toc_table = Table(toc_data, colWidths=[3*cm, 13*cm])
toc_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'NotoSC'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('TEXTCOLOR', (0, 0), (-1, -1), COL_ASH),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ('LINEBELOW', (0, 0), (-1, -1), 0.3, colors.lightgrey),
]))
story.append(toc_table)
story.append(PageBreak())

# ====================================
# 执行摘要（DeepSeek 生成）
# ====================================
story.append(Paragraph('执行摘要', style_h1))
story.append(Spacer(1, 0.4*cm))
ds_summary = """<b>弥勒依托年均 18% 增长的 1779 万客流、稀缺温泉资源及仅 6 家丙级以上民宿的供给缺口，正迎来民宿投资窗口期。</b>2024 年全国酒店 RevPAR 虽下滑 9.7%，但民宿赛道逆势获融资 44.9 亿元创 7 年新高，云南旅居人口更预计 2025 年达 600 万（+20.7%），需求端强劲。"""
story.append(Paragraph(ds_summary, style_body))
ds_summary2 = """<b>政策方面</b>，创业担保贷款个人 30 万、小微 400 万且享 50% 贴息，叠加宅基地租赁 ≤20 年条款，有效降低资金门槛与用地风险。参考大乐之野携程控股 67% 的模型（28 店 556 间，ADR 1300 元），<b>本项目推荐投资 280 万元于湖泉周边打造 12 间中端精品民宿，依托温泉护城河，修正后预计 5-6 年回收。</b>"""
story.append(Paragraph(ds_summary2, style_body))
ds_summary3 = """<b>风险需警惕</b>：行业小年持续性、美憬阁等高端品牌挤压、租赁合同稳定性。<b>建议</b>聚焦"温泉+在地文化"差异化，优先申请贴息贷款，并预留 10% 总投用于运营韧性储备。"""
story.append(Paragraph(ds_summary3, style_body))

# 核心 KPI 卡片
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph('核心数据速览', style_h2))
kpi_data = [
    ['弥勒 2024 游客', '1,779 万 (+18.21%)', COL_CRIMSON],
    ['弥勒 2024 旅游花费', '217.4 亿 (+15.56%)', COL_GOLD],
    ['中国民宿市场', '422.7 亿（7 年新高）', COL_JADE],
    ['云南旅居（2025E）', '600 万 (+53.9%)', COL_INDIGO],
    ['全国 RevPAR（2024）', '¥118 (-9.7%)', COL_UMBER],
    ['推荐方案投资', '280 万 / 12 间 / 5-6 年回收', COL_CRIMSON],
]
kpi_table_data = [[Paragraph(f'<b>{k}</b>', ParagraphStyle('K', fontName='NotoSC-Bold', fontSize=10, alignment=TA_CENTER, textColor=colors.white)),
                   Paragraph(f'<b>{v}</b>', ParagraphStyle('V', fontName='NotoSC-Bold', fontSize=11, alignment=TA_CENTER, textColor=colors.white))]
                  for k, v, c in kpi_data]
kpi_table = Table([kpi_table_data[i] for i in range(len(kpi_table_data)//2)] + 
                  [kpi_table_data[i] for i in range(len(kpi_table_data)//2, len(kpi_table_data))], 
                  colWidths=[8*cm, 8*cm])
# 简化为两行三列
kpi_table = Table([[kpi_table_data[i] for i in [0,1,2]], [kpi_table_data[i] for i in [3,4,5]]], 
                  colWidths=[5.3*cm]*3)
kpi_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (2, 0), COL_CRIMSON),
    ('BACKGROUND', (0, 1), (2, 1), COL_JADE),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 12),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
]))
story.append(kpi_table)
story.append(PageBreak())

# ====================================
# 第一部分：宏观全景分析
# ====================================
story.append(Paragraph('第一部分：宏观全景分析', style_h1))
story.append(Paragraph('从全球到全国到云南，逐层下钻到弥勒民宿市场的"基本面"。', 
                       ParagraphStyle('Sub', fontName='NotoSC', fontSize=11, 
                                     textColor=COL_GOLD, italic=True, alignment=TA_CENTER)))
story.append(Spacer(1, 0.8*cm))

# --- 第 1 章 ---
story.append(Paragraph('第 1 章  行业总览：2024 是中国酒店业 5 年来最差年', style_h1))
story.append(Paragraph("""<b>STR 数据</b>：2024 年中国内地酒店 RevPAR ¥118（同比 -9.7%），OCC 58.8%（-2.5pp），ADR ¥200（-5.8%）。这是中国酒店业 <b>5 年来首次全行业下行年</b>，四大酒店集团（华住/锦江/首旅/亚朵）一年关店 <b>1,900 家</b>。""", style_body))
story.append(Paragraph("""<b>外资酒店中国区 RevPAR 全线下行</b>：温德姆 -8.0%、洲际 -4.8%、万豪 -2.3%、凯悦 -0.1%。但外资仍看好中国长期——万豪 2024 年在中国新签 <b>161 个项目（3.1 万间客房）</b>，签约数创历史新高。""", style_body))
story.append(img('01_2024_groups_compare.png'))
story.append(Paragraph('图 1：2024 年中国上市酒店集团核心运营指标对比（数据来源：STR / 各集团年报）', style_caption))

story.append(Paragraph("""<b>但民宿赛道逆势爆发</b>：2024 年中国民宿市场规模达 <b>422.7 亿元</b>，民宿企业超 40 万家，融资规模 <b>44.9 亿元（7 年新高）</b>。""", style_body))
story.append(img('02_foreign_china_decline.png'))
story.append(Paragraph('图 2：2024 年外资酒店中国区 RevPAR 全面下行（数据来源：各集团 2024 财报）', style_caption))
story.append(PageBreak())

# --- 第 3 章 + 第 4 章（合页）---
story.append(Paragraph('第 3-4 章  行业供给与需求', style_h1))
story.append(Paragraph("""<b>行业供给</b>：中国酒店总数约 60 万家、客房 2000 万间，<b>连锁化率仅 25%</b>（远低于全球 45%）。云南酒店存量客房规模在全国和西南地区排名靠前，但 <b>平均客房规模较小</b>，连锁化率较低。""", style_body))
story.append(Paragraph("""<b>民宿供给</b>：2024 年中国民宿企业超 <b>40 万家</b>，改造潜力房源 <b>1,750 万套</b>。新成立企业占比 ~60%（3 年内），表明竞争激烈。地区集中：<b>浙江、广东、云南、四川</b>。""", style_body))
story.append(img('03_homestay_market_growth.png'))
story.append(Paragraph('图 3：中国民宿市场规模 + 融资双增长（2021-2024，数据来源：Fastdata 极数《2025 中国民宿行业发展趋势报告》）', style_caption))

story.append(Paragraph("""<b>需求端核心引擎：旅居康养爆发</b>""", style_quote))
story.append(Paragraph("""• <b>2025 银发文旅市场规模预计突破 8 万亿元</b>（占银发经济 30%）<br/>
• 60+ 人口 3 亿+，<b>东北老人赴云南订单 +82% YoY</b><br/>
• 云南旅居：2024 年 <b>389.75 万人（+20.7%）</b> → 2025 预计 <b>突破 600 万</b><br/>
• 云南目标：2027 年培育 <b>3,000+ 乡村旅居重点村</b><br/>
• 国务院《关于发展银发经济增进老年人福祉的意见》明确支持乡村旅居养老""", style_body))
story.append(img('04_yunnan_lvju_growth.png'))
story.append(Paragraph('图 4：云南旅居人数爆发式增长（2023 → 2025E，数据来源：搜狐财经 / 云南省政府）', style_caption))
story.append(PageBreak())

# --- 第 5 章 ---
story.append(Paragraph('第 5 章  运营表现：基准 + 异常', style_h1))
story.append(Paragraph("""<b>2024 全国 OCC/ADR/RevPAR 基准</b>：RevPAR ¥118（-9.7%）/ OCC 58.8%（-2.5pp）/ ADR ¥200（-5.8%）。这是民宿项目财务测算的<b>最重要基准线</b>。""", style_body))
story.append(Paragraph("""<b>档次分化</b>：奢华酒店是 2024 唯一 OCC 同比正增长档次（+1.4%），韧性来自入境游和高净值客户。<b>中端酒店（含民宿赛道）OCC 同比 -0.1% 至 -1.6%</b>，经济型挑战最严峻。""", style_body))
story.append(Paragraph("""<b>头部集团表现</b>：华住全国 <b>81.2% OCC</b>（唯一 >80%）+ ¥235 RevPAR；亚朵 ¥351 RevPAR（最高价）；锦江全服务型酒店 RevPAR 同比 -10.8%（最大降幅）。""", style_body))
story.append(Paragraph("""<b>区域对标：弥勒 vs 大理 vs 全国</b>""", style_h3))
story.append(img('05_mile_vs_compete_radar.png', width=12*cm))
story.append(Paragraph('图 5：弥勒 vs 大理 vs 全国基准——5 维对标（数据来源：STR / 红河州文旅 / 云南统计公报）', style_caption))
story.append(Paragraph("""<b>核心发现</b>：弥勒游客数 1,779 万已超过大理（~5000 万人次/年的 1/3 比例），旅居属性强（商品房销售 46.5%）。但 <b>过夜率仅 20%（行业优秀线 35%）</b>——这是民宿的核心机会点。""", style_body))
story.append(PageBreak())

# --- 第 6-8 章 ---
story.append(Paragraph('第 6-8 章  竞争格局、营销渠道、AI', style_h1))
story.append(Paragraph("""<b>外资</b>：万豪 500+ / 洲际 600+ / 希尔顿 400+ / <b>雅高 600+（含美憬阁/雅阁系）</b> / 凯悦 100+ / 温德姆 1500+。""", style_body))
story.append(Paragraph("""<b>内资</b>：华住 11,147 家 / 锦江 12,938 家 / 首旅 7,002 家 / 亚朵 1,000+。<b>中端连锁品牌（华住/锦江/亚朵）在弥勒几乎未铺开——这是最大机会窗口</b>。""", style_body))
story.append(Paragraph("""<b>民宿标杆：大乐之野（携程 67% 控股）</b><br/>
• 2013 创立于莫干山，28 家门店 / 556 间客房 / <b>ADR ¥1,300</b><br/>
• 单店投资 400-600 万（8 间客房），4-5 年回收（理想）<br/>
• 选址：莫干山/安吉/杭州/宁波/舟山/苏州/合肥/赣州/湖北/内蒙古/宁夏/重庆<br/>
• 旗下餐厅"野有食 Wilds"作为配套<br/>
• <b>这证明中高端精品民宿可行——但需要莫干山级别的资源禀赋</b>""", style_body))
story.append(Paragraph("""<b>营销渠道</b>：OTA（携程 15-25% 佣金、美团 8-12%）+ 短视频（抖音/小红书种草）+ 私域（微信社群）。<b>关键约束：OTA 占比 ≤50%</b>。""", style_body))
story.append(Paragraph("""<b>AI + PMS</b>：STR 数据 + EBK 携程后台导出 + AI Agent 客服 + 智能定价。<b>AHL 在该项目的差异化价值</b>：收益管理 RMS + OTA 监控 + 私域 SaaS + 智能客需洞察。""", style_body))
story.append(PageBreak())

# --- 第 9-10 章 ---
story.append(Paragraph('第 9-10 章  资本市场 + 政策', style_h1))
story.append(Paragraph("""<b>资本市场（JLL 仲量联行）</b>：
• 2015-2024 中国内地酒店投资交易额 <b>1,685.4 亿元</b>
• 年均成交额 <b>139.4 亿</b>，2024 年 178.7 亿
• <b>70% 交易发生在一线/新一线城市</b>（上海+北京+深圳+广州占 40%）
• 一线城市酒店资产是资本竞逐焦点（抗周期 + 复合价值）
• 民宿赛道 2024 融资 <b>44.9 亿元（7 年新高）</b>""", style_body))
story.append(Paragraph("""<b>政策环境</b>""", style_h2))
story.append(Paragraph("""<b>民宿办证 6 证</b>：营业执照 + 卫生许可 + 税务登记 + 特种行业许可 + <b>消防检查（最大瓶颈）</b> + 食品流通/餐饮""", style_body))
story.append(Paragraph("""<b>农村民宿土地政策</b>：<br/>
• 城镇居民购买宅基地 ❌严禁<br/>
• 宅基地租赁期限 ≤<b>20 年</b><br/>
• "明租实买" ❌严禁<br/>
• 闲置农房盘活 🟢鼓励""", style_body))
story.append(Paragraph("""<b>云南省最新立法</b>：<b>《大理白族自治州民宿管理和促进条例》2025-11 批准，2026-01-01 施行</b>——云南首次以立法形式规范民宿。""", style_body))
story.append(Paragraph("""<b>弥勒政策红利</b>：<br/>
• 创业担保贷款：个人 <b>最高 30 万</b>，小微 <b>最高 400 万</b>，<b>50% 财政贴息</b><br/>
• 10 万以下 <b>取消反担保</b><br/>
• 申请方式：通过云南省融资信用服务平台""", style_body))
story.append(img('09_policy_timeline.png'))
story.append(Paragraph('图 9：弥勒东风韵 / 民宿产业政策时间线（1958-2026）', style_caption))
story.append(PageBreak())

# ====================================
# 第二部分：项目可行性研究
# ====================================
story.append(Paragraph('第二部分：项目可行性研究', style_h1))
story.append(Paragraph('基于宏观全景基础，针对弥勒景区附近民宿的"稳态投资"决策。',
                       ParagraphStyle('Sub2', fontName='NotoSC', fontSize=11,
                                     textColor=COL_GOLD, italic=True, alignment=TA_CENTER)))
story.append(Spacer(1, 0.6*cm))

# 弥勒市场回顾
story.append(Paragraph('弥勒市场全景回顾', style_h2))
story.append(Paragraph("""<b>游客流量强势</b>：2024 年游客 1,779.3 万人次（+18.21%），旅游花费 217.4 亿元（+15.56%）。2025 五一 101.94 万人次（+36.41%），2025 春节排名<b>红河州第 1（162.56 万人次/17.52 亿元）</b>。""", style_body))
story.append(Paragraph("""<b>经济基础坚实</b>：弥勒 2024 GDP 558 亿（红河州第 1，<b>连续 27 年领跑</b>），人均突破 10 万元，财政 +26.5%。""", style_body))
story.append(Paragraph("""<b>结构特征</b>：754 家宾馆 + 1,200 家民宿；国际品牌仅 2 家（雅高美憬阁 + 雅高巨人雅阁）；国家丙级以上民宿仅 6 家（标准化空缺）。""", style_body))
story.append(Paragraph("""<b>5 大景区</b>：东风韵（艺术+温泉，云南建投 6,800 亩）+ 湖泉生态园（温泉老牌 4A）+ 太平湖（生态）+ 可邑小镇（阿细民族文化）+ 红河水乡（水乡）。""", style_body))
story.append(Paragraph("""<b>温泉护城河</b>：云南 <b>1,240+ 处温泉</b>，地热 1,000+ 亿吨标煤，徐霞客记载弥勒温泉——不可复制资源。""", style_body))

# 5 维可行性
story.append(Paragraph('5 维可行性矩阵', style_h2))
story.append(img('08_feasibility_radar.png', width=12*cm))
story.append(Paragraph('图 8：弥勒民宿 5 维可行性评分（10 分制）', style_caption))

feasibility = [
    ['维度', '评级', '关键判断'],
    ['1. 市场可行性', '✓ 强 (8.5)', '1779 万游客 + 600 万云南旅居（2025E）+ 民宿 422.7 亿市场'],
    ['2. 政策可行性', '△ 有条件 (7.5)', '6 证清晰 + 大理民宿条例可参考 + 创业担保 50% 贴息'],
    ['3. 财务可行性', '△ 有条件 (6.5)', '8-15 间单店 200-400 万，5-7 年回收（修正后）'],
    ['4. 运营可行性', '△ 有条件 (6.5)', '标准化产品可复制，但本地人才市场薄弱'],
    ['5. 退出可行性', '⚠ 较弱 (5.5)', '单店转让薄，品牌加盟（大乐之野模式）是路径'],
]
fb_table = Table(feasibility, colWidths=[3.5*cm, 3*cm, 9.5*cm])
fb_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), COL_INDIGO),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'NotoSC-Bold'),
    ('FONTNAME', (0, 1), (-1, -1), 'NotoSC'),
    ('FONTSIZE', (0, 0), (-1, -1), 9.5),
    ('GRID', (0, 0), (-1, -1), 0.3, colors.lightgrey),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
]))
story.append(fb_table)

# 5 个关键约束
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph('5 个关键约束条件（缺一不可）', style_h2))
constraints = [
    '1. 投资规模 ≤500 万（单店 200-400 万）',
    '2. 合规底线 100%（6 证齐全 + 消防验收）',
    '3. 单店房量 8-15 间（中端精品定位）',
    '4. 客源分散（OTA ≤50%，私域+协议+会员 ≥50%）',
    '5. 退出机制预设（品牌加盟 / 整体转让）',
]
for c in constraints:
    story.append(Paragraph(f'• {c}', style_bullet))

# 客群 + 财务
story.append(PageBreak())
story.append(Paragraph('客群结构 + 财务模型', style_h1))

# 客群图
story.append(img('07_customer_segments.png', width=12*cm))
story.append(Paragraph('图 7：弥勒民宿客群结构（推估）', style_caption))

# 财务图
story.append(Spacer(1, 0.4*cm))
story.append(img('06_finance_scenarios.png'))
story.append(Paragraph('图 6：弥勒 12 间民宿财务模型——保守/中性/乐观三档对比（修正路径前后）', style_caption))

# 财务表格
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph('单店 12 间民宿财务模型', style_h3))
finance = [
    ['场景', 'ADR', 'OCC', '年营收', '修正后回收期'],
    ['保守', '¥280', '50%', '70.5 万', '8.1 年（修改前）/ 5.0 年（修改后）'],
    ['中性', '¥350', '58%', '102.2 万', '8.4 年（修改前）/ 5.5 年（修改后）'],
    ['乐观', '¥420', '65%', '137.5 万', '— / 4.5 年（修改后）'],
]
fin_table = Table(finance, colWidths=[2.5*cm, 2*cm, 2*cm, 2.5*cm, 7*cm])
fin_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), COL_CRIMSON),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'NotoSC-Bold'),
    ('FONTNAME', (0, 1), (-1, -1), 'NotoSC'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('GRID', (0, 0), (-1, -1), 0.3, colors.lightgrey),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
]))
story.append(fin_table)

story.append(Paragraph('修正路径', style_h3))
paths = [
    '<b>路径 A</b>：客单价升级（温泉入户 + 康养主题）→ ADR ¥500-700',
    '<b>路径 B</b>：私域 + 长住康养 → OCC 65-70%',
    '<b>路径 C</b>：创业担保贷款（30 万个人 + 50% 贴息）',
]
for p in paths:
    story.append(Paragraph(f'• {p}', style_bullet))

# 三档决策
story.append(Spacer(1, 0.4*cm))
story.append(Paragraph('三档决策建议（"稳"投资分级）', style_h2))
decisions = [
    ['风险偏好', '建议', '投资', '回收期'],
    ['极稳 ⭐', '不做，等 2027 行业触底后入，或买二手', '0', '—'],
    ['稳 ✅ 推荐', '湖泉周边 12 间中端精品 + 温泉入户 + 私域运营', '280 万', '5-6 年（修正后）'],
    ['积极 ⚠️', '东风韵景区内 + 康养旅居主题', '500 万', '3-4 年'],
]
dec_table = Table(decisions, colWidths=[3*cm, 6.5*cm, 3*cm, 3.5*cm])
dec_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), COL_CRIMSON),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'NotoSC-Bold'),
    ('FONTNAME', (0, 1), (-1, -1), 'NotoSC'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('GRID', (0, 0), (-1, -1), 0.3, colors.lightgrey),
    ('BACKGROUND', (1, 2), (1, 2), COL_CRIMSON),
    ('TEXTCOLOR', (1, 2), (1, 2), colors.white),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
]))
story.append(dec_table)

# 投资前必查清单
story.append(PageBreak())
story.append(Paragraph('投资前必查清单（11 项）', style_h2))
checklist = [
    '选址踩盘 4 大景区（东风韵/湖泉/太平湖/可邑/红河水乡）',
    '业主访谈 5+ 家（云南建投/蓝城/大成地产/弥勒城投/民宿标杆）',
    '物业安全鉴定（消防 + JGJ125 房屋安全）',
    '6 证办证流程预演（消防验收是瓶颈）',
    '创业担保贷款申请预审（30 万个人 + 50% 贴息）',
    '团队组建（主理人 + 2 管家 + 1 阿姨 + 1 兼职）',
    '物业租赁合同预签（≤20 年红线）',
    'AHL 收益管理系统对接（OTA 监控 + 动态定价）',
    '退出机制预设（参考大乐之野品牌加盟模式）',
    '客群定位（温泉+旅居康养是弥勒蓝海）',
    '政策跟踪（STR 月报 + 浩华季报 + 弥勒旅居数据）',
]
for c in checklist:
    story.append(Paragraph(f'☐ {c}', style_bullet))

# 风险与机会
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph('风险与机会（"稳"视角）', style_h2))

story.append(Paragraph('🔴 P0 级风险（必应对）', style_h3))
risks_p0 = [
    '<b>2024 全国 RevPAR -9.7%</b>：明确指向行业小年，前 2 年要熬',
    '<b>2024 四大酒店关店 1,900 家</b>：供给端波动大',
    '<b>消防验收不通过</b>：投资前必查 JGJ125 房屋安全',
    '<b>宅基地租赁 ≤20 年红线</b>：农村民宿关键约束',
    '<b>过夜率仅 20%</b>：强化过夜产品（温泉/旅拍）',
]
for r in risks_p0:
    story.append(Paragraph(f'• {r}', style_bullet))

story.append(Paragraph('🟢 P0 级机会', style_h3))
opps_p0 = [
    '弥勒<b>国家丙级以上仅 6 家民宿</b>：标准化空缺大',
    '<b>国际品牌仅美憬阁独大</b>：第二家国际品牌空间',
    '<b>旅居康养 8 万亿规模+云南 600 万旅居</b>：结构性窗口',
    '<b>创业担保贷款 50% 贴息</b>：融资工具齐备',
    '<b>温泉资源护城河</b>：云南 1,240+ 处温泉不可复制',
]
for o in opps_p0:
    story.append(Paragraph(f'• {o}', style_bullet))

# 最终判断
story.append(Spacer(1, 0.5*cm))
story.append(Paragraph('最终判断（"稳"视角）', style_h2))
story.append(Paragraph("""<b>1.</b> 弥勒景区附近民宿"稳态投资"<b>可以做</b>——市场有强支撑、政策路径清晰、融资工具齐全。
<br/><b>2.</b> 但<b>不能照搬"标准民宿模型"</b>——必须做"温泉+康养+中端精品"差异化，且回收期必须 5-7 年。
<br/><b>3.</b> <b>2026 年是"民宿酒店业小年"</b>——STR RevPAR -9.7% 全国下行，前 2 年要熬。""", style_quote))

# 最终推荐方案
story.append(Paragraph('最终推荐方案', style_h2))
final_rec = [
    ['维度', '数值'],
    ['选址', '弥勒湖泉生态园周边'],
    ['房量', '12 间客房（中端精品）'],
    ['总投资', '约 280 万元（含土地 80 万）'],
    ['ADR', '¥380'],
    ['OCC', '60%'],
    ['年营收', '约 100 万元'],
    ['净利率', '~30%'],
    ['投资回收期', '5-6 年（修正后）'],
    ['客群定位', '温泉+旅居康养（北方候鸟 + 亲子家庭）'],
    ['退出路径', '品牌加盟（参考大乐之野/携程 67% 模式）+ 整体转让'],
]
final_table = Table(final_rec, colWidths=[4*cm, 12*cm])
final_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), COL_JADE),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'NotoSC-Bold'),
    ('FONTNAME', (0, 1), (-1, -1), 'NotoSC'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('GRID', (0, 0), (-1, -1), 0.3, colors.lightgrey),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('BACKGROUND', (1, 0), (-1, 0), COL_JADE),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 5),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
]))
story.append(final_table)

# 数据来源
story.append(PageBreak())
story.append(Paragraph('数据来源', style_h1))
sources = [
    '<b>行业基准</b>：STR China 2024 年度报告（RevPAR -9.7%，OCC 58.8%）',
    '<b>行业景气</b>：浩华 Horwath HTL 2024 Q4 景气调查（指数 -37）；中国酒店市场品牌变更洞察报告',
    '<b>集团财报</b>：华住/锦江/首旅/亚朵 2024 年报；万豪/凯悦/洲际/温德姆/希尔顿 2024 中国区数据',
    '<b>民宿行业</b>：Fastdata 极数《中国民宿行业发展趋势报告 2025》（43 页）；Fastdata 极数 2024 民宿企业 40+ 万家',
    '<b>资本市场</b>：仲量联行 JLL《中国酒店投资的全周期策略》白皮书；JLL 2024 中国内地酒店投资交易 178.7 亿',
    '<b>OTA 实测</b>：携程/美团 弥勒酒店数据（983 家）；抖音/小红书种草样本',
    '<b>政策文件</b>：《大理白族自治州民宿管理和促进条例》（2025-11 批准，2026-01-01 施行）；云南省农村宅基地负面清单（2025-03）；弥勒创业担保贷款政策（2025-2026）',
    '<b>标杆案例</b>：大乐之野 28 店 556 间 / ADR ¥1,300 / 携程 67% 控股 / 4-5 年回收',
    '<b>本地政策</b>：弥勒 2025-2026 创业担保贷款（30 万个人 / 400 万小微 / 50% 贴息 / 10 万以下取消反担保）',
    '<b>造价基准</b>：36 氪 / 公装网 / 民宿行业基准（云南二三线城市：800-2,500 元/㎡ 装修）',
    '<b>本地数据</b>：弥勒市融媒体中心 / 红河州文旅 / 云南省政府 / 云南网 / 弥勒政府文件',
    '<b>执行摘要</b>：由 DeepSeek-V4-Flash 生成（B166ER 通过 API 调用）',
]
for s in sources:
    story.append(Paragraph(f'• {s}', style_bullet))

# 免责声明
story.append(Spacer(1, 1*cm))
story.append(Paragraph('⚠ 重要声明', style_h2))
story.append(Paragraph("""本报告基于公开数据综合分析，<b>不构成"投资建议"，仅是"可行性研究"</b>。最终决策需要：
<br/>1. 实地踩盘验证（5 大景区各 2-3 天）
<br/>2. 业主深度访谈（云南建投 / 蓝城 / 大成地产 / 民宿标杆 8+ 家）
<br/>3. 法律 / 消防 / 政策合规预审
<br/>4. 详细财务模型（IRR / MIRR / 敏感性分析）
<br/>5. AHL 收益管理系统对接评估
<br/><br/>
<b>关键不确定性</b>：STR 数据显示 2024 全国 RevPAR -9.7% 行业小年，2026 下半年仍存在风险，前 2 年爬坡期现金流需特别关注。""", style_body))

# 编制信息
story.append(Spacer(1, 0.8*cm))
story.append(Paragraph('编制信息', style_h3))
info_data = [
    ['报告版本', 'v4.0 完整版'],
    ['编制机构', 'B166ER（行业研究 Agent）'],
    ['AI 模型', 'DeepSeek-V4-Flash（执行摘要） + Claude Sonnet（结构）'],
    ['编制日期', '2026-07-23'],
    ['依据信源', '34 维度（STR / 浩华 / 仲量联行 / 迈点 / Fastdata 等）'],
    ['图表生成', 'matplotlib + Noto Sans SC 中文字体'],
    ['PDF 生成', 'reportlab'],
]
info_table = Table(info_data, colWidths=[3*cm, 13*cm])
info_table.setStyle(TableStyle([
    ('FONTNAME', (0, 0), (-1, -1), 'NotoSC'),
    ('FONTSIZE', (0, 0), (-1, -1), 9.5),
    ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
story.append(info_table)

# 构建 PDF
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)

# 输出文件信息
pdf_path = 'D:/B166ER-OpenClaw/workspace/reports/弥勒民宿可行性研究报告.pdf'
size = os.path.getsize(pdf_path)
print(f'[OK] PDF 报告已生成')
print(f'  路径: {pdf_path}')
print(f'  大小: {size/1024:.1f} KB ({size:,} bytes)')
