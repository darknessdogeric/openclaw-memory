"""Generate 2026 May Day Hotel Market Report PPT with charts."""
from pptx import Presentation
from pptx.util import Inches, Pt, Cm, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION
from pptx.chart.data import CategoryChartData
import os

# === Color Scheme ===
DARK_BLUE = RGBColor(0, 51, 102)
MID_BLUE = RGBColor(0, 90, 156)
LIGHT_BLUE = RGBColor(68, 146, 208)
ACCENT_ORANGE = RGBColor(245, 128, 37)
ACCENT_GREEN = RGBColor(46, 139, 87)
ACCENT_RED = RGBColor(200, 60, 60)
DARK_GRAY = RGBColor(51, 51, 51)
MID_GRAY = RGBColor(128, 128, 128)
LIGHT_GRAY = RGBColor(240, 240, 240)
WHITE = RGBColor(255, 255, 255)
BLACK = RGBColor(0, 0, 0)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

def add_bg(slide, color=WHITE):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_title_bar(slide, title_text, subtitle_text=None):
    """Dark blue title bar at top."""
    from pptx.util import Inches, Pt
    bar = slide.shapes.add_shape(
        1, Inches(0), Inches(0), prs.slide_width, Inches(1.1)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = DARK_BLUE
    bar.line.fill.background()

    txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.15), Inches(11.5), Inches(0.7))
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = title_text
    p.font.size = Pt(30)
    p.font.bold = True
    p.font.color.rgb = WHITE

    if subtitle_text:
        txBox2 = slide.shapes.add_textbox(Inches(0.8), Inches(0.72), Inches(11.5), Inches(0.35))
        tf2 = txBox2.text_frame
        p2 = tf2.paragraphs[0]
        p2.text = subtitle_text
        p2.font.size = Pt(14)
        p2.font.color.rgb = RGBColor(180, 210, 240)

    # Accent line
    line = slide.shapes.add_shape(
        1, Inches(0), Inches(1.1), prs.slide_width, Inches(0.05)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = ACCENT_ORANGE
    line.line.fill.background()

def add_footer(slide, page_num, source="数据来源：交通运输部 | 同程旅行 | 酒店之家 | 浩华 | 中信证券 | B166ER分析"):
    txBox = slide.shapes.add_textbox(Inches(0.8), Inches(6.95), Inches(11.5), Inches(0.4))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = source
    p.font.size = Pt(8)
    p.font.color.rgb = MID_GRAY

    txBox2 = slide.shapes.add_textbox(Inches(12.2), Inches(6.95), Inches(0.8), Inches(0.4))
    tf2 = txBox2.text_frame
    p2 = tf2.paragraphs[0]
    p2.text = str(page_num)
    p2.font.size = Pt(10)
    p2.font.color.rgb = MID_BLUE
    p2.alignment = PP_ALIGN.RIGHT

def add_kpi_box(slide, left, top, width, height, label, value, sub_value=None, color=DARK_BLUE):
    """KPI metric box."""
    box = slide.shapes.add_shape(1, left, top, width, height)
    box.fill.solid()
    box.fill.fore_color.rgb = color
    box.line.fill.background()

    txBox = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.4))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = label
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(200, 200, 200)

    txBox2 = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.55), width - Inches(0.4), Inches(0.5))
    tf2 = txBox2.text_frame
    p2 = tf2.paragraphs[0]
    p2.text = value
    p2.font.size = Pt(28)
    p2.font.bold = True
    p2.font.color.rgb = WHITE

    if sub_value:
        txBox3 = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(1.05), width - Inches(0.4), Inches(0.3))
        tf3 = txBox3.text_frame
        p3 = tf3.paragraphs[0]
        p3.text = sub_value
        p3.font.size = Pt(10)
        p3.font.color.rgb = RGBColor(180, 210, 240)

def add_bullet_list(slide, left, top, width, height, items, title=None):
    """Bullet text block."""
    if title:
        txBox = slide.shapes.add_textbox(left, top, width, Inches(0.35))
        tf = txBox.text_frame
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(16)
        p.font.bold = True
        p.font.color.rgb = DARK_BLUE
        top += Inches(0.4)

    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.text = f"▸ {item}"
        p.font.size = Pt(13)
        p.font.color.rgb = DARK_GRAY
        p.space_after = Pt(8)

def add_bar_chart(slide, left, top, width, height, title, categories, values, color_list=None):
    """Add a bar chart."""
    chart_data = CategoryChartData()
    chart_data.categories = categories
    chart_data.add_series('', values)

    chart_frame = slide.shapes.add_chart(
        XL_CHART_TYPE.BAR_CLUSTERED, left, top, width, height, chart_data
    )
    chart = chart_frame.chart
    chart.has_legend = False
    
    plot = chart.plots[0]
    series = plot.series[0]
    if color_list:
        for idx, color in enumerate(color_list):
            point = series.points[idx]
            point.format.fill.solid()
            point.format.fill.fore_color.rgb = color
    else:
        series.format.fill.solid()
        series.format.fill.fore_color.rgb = MID_BLUE

    chart.category_axis.tick_labels.font.size = Pt(10)
    chart.value_axis.visible = False
    chart.has_title = False

    # Title as textbox
    txBox = slide.shapes.add_textbox(left, top - Inches(0.4), width, Inches(0.35))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE

def add_pie_chart(slide, left, top, width, height, title, categories, values, colors=None):
    """Add a donut/pie chart."""
    chart_data = CategoryChartData()
    chart_data.categories = categories
    chart_data.add_series('', values)

    chart_frame = slide.shapes.add_chart(
        XL_CHART_TYPE.DOUGHNUT, left, top, width, height, chart_data
    )
    chart = chart_frame.chart
    chart.has_legend = True
    chart.legend.position = XL_LEGEND_POSITION.BOTTOM
    chart.legend.include_in_layout = False
    chart.legend.font.size = Pt(9)

    plot = chart.plots[0]
    if colors:
        for idx, color in enumerate(colors):
            if idx < len(plot.series[0].points):
                point = plot.series[0].points[idx]
                point.format.fill.solid()
                point.format.fill.fore_color.rgb = color

    chart.has_title = False
    txBox = slide.shapes.add_textbox(left, top - Inches(0.35), width, Inches(0.3))
    tf = txBox.text_frame
    p = tf.paragraphs[0]
    p.text = title
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = DARK_BLUE

# ===== SLIDE 1: Cover =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BLUE)

# Large title
txBox = slide.shapes.add_textbox(Inches(1.5), Inches(1.5), Inches(10), Inches(1.5))
tf = txBox.text_frame
p = tf.paragraphs[0]
p.text = "2026年五一小长假"
p.font.size = Pt(48)
p.font.bold = True
p.font.color.rgb = WHITE
p.alignment = PP_ALIGN.LEFT

p2 = tf.add_paragraph()
p2.text = "全国酒店市场全面预测分析报告"
p2.font.size = Pt(36)
p2.font.color.rgb = ACCENT_ORANGE
p2.alignment = PP_ALIGN.LEFT

# Subtitle
txBox2 = slide.shapes.add_textbox(Inches(1.5), Inches(3.5), Inches(10), Inches(0.8))
tf2 = txBox2.text_frame
p3 = tf2.paragraphs[0]
p3.text = "收益管理驱动 · 业主视角 · 首日数据验证 · 18数据源交叉分析"
p3.font.size = Pt(16)
p3.font.color.rgb = RGBColor(180, 210, 240)

# Date line
txBox3 = slide.shapes.add_textbox(Inches(1.5), Inches(4.5), Inches(10), Inches(0.5))
tf3 = txBox3.text_frame
p4 = tf3.paragraphs[0]
p4.text = "报告版本 V2.0  |  2026年5月1日 22:00  |  B166ER Research"
p4.font.size = Pt(12)
p4.font.color.rgb = RGBColor(150, 180, 200)

# Accent bar at bottom
bar = slide.shapes.add_shape(1, Inches(0), Inches(7.2), prs.slide_width, Inches(0.3))
bar.fill.solid()
bar.fill.fore_color.rgb = ACCENT_ORANGE
bar.line.fill.background()

# ===== SLIDE 2: Executive Summary KPI =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
add_title_bar(slide, "核心指标总览", "宏观出行 → 酒店绩效 → 供给格局 三维交叉验证")
add_footer(slide, 2)

add_kpi_box(slide, Inches(0.5), Inches(1.5), Inches(2.8), Inches(1.5), 
    "全社会跨区域流动量", "15.2亿人次", "同比 +4% · 创历史同期新高", DARK_BLUE)
add_kpi_box(slide, Inches(3.6), Inches(1.5), Inches(2.8), Inches(1.5), 
    "酒店 RevPAR 预测", "+5~7%", "中枢 +6% 🔼 首日数据上修", ACCENT_ORANGE)
add_kpi_box(slide, Inches(6.7), Inches(1.5), Inches(2.8), Inches(1.5), 
    "酒店 ADR（预订口径）", "+6~7%", "全档次转正 · 中高端实质性修复", MID_BLUE)
add_kpi_box(slide, Inches(9.8), Inches(1.5), Inches(2.8), Inches(1.5), 
    "供给端增速", "+6.5% ↓", "从年初+7.4%持续收敛", ACCENT_GREEN)

# Key judgment
txBox = slide.shapes.add_textbox(Inches(0.5), Inches(3.4), Inches(12.3), Inches(0.8))
tf = txBox.text_frame
p = tf.paragraphs[0]
p.text = "▍核心判断"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = DARK_BLUE

p2 = tf.add_paragraph()
p2.text = "2026年是中国弹性假期制度元年，首个五一以「人次扩张 + 行程延长」驱动增量。首日3.44亿人次验证预测基础，"
p2.font.size = Pt(14)
p2.font.color.rgb = DARK_GRAY
p3 = tf.add_paragraph()
p3.text = "跳城游（60%旅客串联2-3城）+ 海外替代游 + 宝藏小城爆发三重引擎超预期，供给增速收敛至+6.5%，供需共振格局正在形成。"
p3.font.size = Pt(14)
p3.font.color.rgb = DARK_GRAY

# Chart: RevPAR trend
add_bar_chart(slide, Inches(0.5), Inches(4.7), Inches(5.5), Inches(2.1),
    "RevPAR 季度修复趋势",
    ['Q1\n+3.1%', 'Q2 QTD\n+6.7%', '五一预测\n+5~7%'],
    [3.1, 6.7, 6.0],
    [LIGHT_BLUE, MID_BLUE, DARK_BLUE])

# Right side: Q2 outlook text
add_bullet_list(slide, Inches(6.5), Inches(4.7), Inches(6), Inches(2.1),
    [
        "浩华Q2景气指数回升至 -9（Q1为 -21），修复斜率确立",
        "三亚(+33)、深圳/上海住宿率转正，一线城市领跑修复",
        "供给端增速从年初+7.4%稳步下行至+6.5%",
        "政策支撑：中央政府政策指数+5，旅游趋势+11",
        "四重全年支撑：供给降速 + 春秋假 + 商旅低基数 + 头部分红"
    ], "浩华景气指数交叉验证")

# ===== SLIDE 3: 需求端 - 出行结构 =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
add_title_bar(slide, "需求端深度拆解", "五大结构性趋势重塑出行行为 | 首日数据验证")
add_footer(slide, 3)

# Donut: travel modes
add_pie_chart(slide, Inches(0.3), Inches(1.5), Inches(4.5), Inches(2.8),
    "出行方式结构（15.2亿人次）",
    ['公路 91.6%', '铁路 7.0%', '民航 0.8%', '水路 0.6%'],
    [91.6, 7.0, 0.8, 0.6],
    [MID_BLUE, LIGHT_BLUE, ACCENT_ORANGE, MID_GRAY])

# Donut: traveler demographics
add_pie_chart(slide, Inches(4.8), Inches(1.5), Inches(4.2), Inches(2.8),
    "客群画像（航空出行口径 · 首日数据）",
    ['年轻客群 41%', '亲子家庭 25%', '银发一族 13%', '入境/其他 21%'],
    [41, 25, 13, 21],
    [MID_BLUE, DARK_BLUE, ACCENT_GREEN, MID_GRAY])

# Right side: Key trends text
add_bullet_list(slide, Inches(0.3), Inches(4.5), Inches(12.5), Inches(2.8),
    [
        "🔵 跳城游：60%旅客串联2-3个目的地，线性串联订单占比超40%，租车自驾50%+，平均租期4.3天",
        "🔴 海外替代游：含税机票+13~15% & 国际取消率7.4% → 云南+89% 四川+76% 新疆+73% 广西+70%",
        "🟠 宝藏小城爆发：县域旅行+128%，丽水酒店热度+116% 龙岩+85% 赣州+75%，增速碾压一线",
        "🟢 Color Walk：色彩目的地搜索+200%，蓝色系+65% 绿色系+48%，情绪价值驱动目的地选择",
        "🟣 AI预订渗透：DeepTrip AI引导预订+80%，AI规划行程+60%，OTA入口被快速分流"
    ], "五大结构性趋势（首日数据验证）")


# ===== SLIDE 4: 供给端分析 =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
add_title_bar(slide, "供给端：增速收敛，供需共振", "全国酒店客房增速持续下行 | 连锁化率40.09% | 浩华：2025新增中档+酒店约9,800家")
add_footer(slide, 4)

# Supply trend chart
add_bar_chart(slide, Inches(0.5), Inches(1.6), Inches(6), Inches(2.6),
    "全国酒店客房量同比增速（%）",
    ['2026\n年初', '2月', '3月', '4月底'],
    [7.4, 7.0, 6.8, 6.5],
    [DARK_BLUE, MID_BLUE, LIGHT_BLUE, ACCENT_ORANGE])

# Competition chart: 四大集团
add_bar_chart(slide, Inches(7), Inches(1.6), Inches(5.8), Inches(2.6),
    "2025四大酒店集团净利润（亿元）",
    ['华住', '亚朵', '锦江', '首旅'],
    [50.8, 16.2, 9.25, 8.1],
    [DARK_BLUE, MID_BLUE, LIGHT_BLUE, MID_GRAY])

# Right text
add_bullet_list(slide, Inches(0.5), Inches(4.5), Inches(12.5), Inches(2.2),
    [
        "华住「一超」：253亿营收/50.8亿净利，124.6万间客房，推汉庭快捷攻存量改造",
        "亚朵崛起：98亿营收/16.2亿净利，零售业务占40%，「见野」品牌独立，品牌溢价最强",
        "锦江首旅承压：净利润<10亿，体量下滑，规模≠利润的时代到来",
        "行业逻辑切换：从「规模竞争」→「价值竞争」，连锁化率提升带来的定价权优势持续扩大",
        "存量改造成为主战场：开业5年以上酒店占60%，经济型占77.8%，翻牌/轻改造模式崛起"
    ], "竞争格局：一超多强，两极分化")

# ===== SLIDE 5: 分档次预测 =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
add_title_bar(slide, "分档次酒店预测（收益率视角）", "酒店之家4/20周数据 | ADR全面转正 | 中高端实质性修复")
add_footer(slide, 5)

# 4 KPI boxes for tiers
add_kpi_box(slide, Inches(0.3), Inches(1.5), Inches(3), Inches(1.3),
    "🏨 经济型 ADR ¥200-350", "RevPAR +5~7%", "OCC 90-98% · ADR +3.6%", DARK_BLUE)
add_kpi_box(slide, Inches(3.6), Inches(1.5), Inches(3), Inches(1.3),
    "🏨 中档型 ADR ¥350-600", "RevPAR +6~9%", "OCC 85-95% · ADR +3.9% · 亲子首选", ACCENT_ORANGE)
add_kpi_box(slide, Inches(6.9), Inches(1.5), Inches(3), Inches(1.3),
    "🏨 高档型 ADR ¥600-1,200", "RevPAR +4~7%", "OCC 75-88% · ADR +2.3%", MID_BLUE)
add_kpi_box(slide, Inches(10.2), Inches(1.5), Inches(3), Inches(1.3),
    "🏨 豪华型 ADR ¥1,200+", "RevPAR +2~4%", "OCC 65-78% · ADR +0.4%", ACCENT_GREEN)

# ADR recovery chart
add_bar_chart(slide, Inches(0.3), Inches(3.2), Inches(6.2), Inches(2.4),
    "各档次ADR同比对比（2025五一 vs 2026五一）",
    ['经济型', '中档型', '高档型', '豪华型'],
    [3.6, 3.9, 2.3, 0.4],
    [DARK_BLUE, MID_BLUE, LIGHT_BLUE, MID_GRAY])

# Key insight
add_bullet_list(slide, Inches(7), Inches(3.2), Inches(5.8), Inches(2.4),
    [
        "2025年五一：各档次ADR「全面负值」",
        "2026年五一：各档次ADR「全面转正」",
        "经济/中档领涨（+3.6%/3.9%）→ 大众消费韧性最强",
        "高档实质性修复（-2.8%→+2.3%）→ 商务+休闲共振",
        "豪华滞后修复（-4.5%→+0.4%）→ 高端商务仍承压"
    ], "价格修复周期正式开启")

# OCC horizontal comparison
add_bar_chart(slide, Inches(0.3), Inches(5.9), Inches(6.2), Inches(1.3),
    "五一期间OCC预测区间（%）",
    ['经济型', '中档型', '高档型', '豪华型'],
    [94, 90, 82, 72],
    [DARK_BLUE, MID_BLUE, LIGHT_BLUE, MID_GRAY])

add_bullet_list(slide, Inches(7), Inches(5.9), Inches(5.5), Inches(1.3),
    [
        "县域品质酒店+76%、精品民宿+92% → 中档是最大受益者",
        "三亚亚龙湾高品质酒店+47% → 高档度假修复强劲",
        "跳城游连住需求 → 5晚+订单+10ppts → 跨档次套餐机会"
    ], "")

# ===== SLIDE 6: 城市分级与区域对比 =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
add_title_bar(slide, "城市分级与区域市场对比", "RevPAR预测 + 首日酒店入住热度验证")
add_footer(slide, 6)

# City tier bar chart
add_bar_chart(slide, Inches(0.3), Inches(1.5), Inches(6.2), Inches(2.6),
    "各城市等级 RevPAR 同比预测（%）",
    ['一线\n+4~6%', '准一线\n+6~10%', '二线\n+8~15%', '三四线/县域\n+15~30%'],
    [5, 8, 12, 22],
    [DARK_BLUE, MID_BLUE, LIGHT_BLUE, ACCENT_ORANGE])

# Region bar chart
add_bar_chart(slide, Inches(7), Inches(1.5), Inches(5.8), Inches(2.6),
    "七大区域 RevPAR 同比预测（%）",
    ['华东', '华南', '西南', '西北', '华中', '东北', '华北'],
    [8.5, 7.5, 10, 11.5, 6.5, 5, 4],
    [DARK_BLUE, MID_BLUE, MID_BLUE, ACCENT_ORANGE, LIGHT_BLUE, MID_GRAY, MID_GRAY])

# City heat data
txBox = slide.shapes.add_textbox(Inches(0.5), Inches(4.3), Inches(12.3), Inches(0.4))
tf = txBox.text_frame
p = tf.paragraphs[0]
p.text = "▍首日酒店入住热度飙升城市（同程大数据）"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = DARK_BLUE

# Heat table
table_data = [
    ['城市', '酒店热度同比', '驱动因素', '城市', '酒店热度同比', '驱动因素'],
    ['浙江丽水', '+116%', '古堰画乡·浙西山水', '广东广州', '+43%', '跳城游起点·岭南文化'],
    ['福建龙岩', '+85%', '客家土楼·红色文化', '山东青岛', '+40%', 'Color Walk蓝色系'],
    ['江西赣州', '+75%', '通天岩·宋城文化', '四川成都', '+37%', '替代游·美食之都'],
    ['县域整体', '+128%', '反向旅游·品质下沉', '湖北武汉', '+35%', '樱花延续·高校游'],
]
table = slide.shapes.add_table(len(table_data), len(table_data[0]), 
    Inches(0.3), Inches(4.8), Inches(12.7), Inches(2.0))
table.table.style = 'Medium Style 2 - Accent 1'
for r, row in enumerate(table_data):
    for c, text in enumerate(row):
        cell = table.table.cell(r, c)
        cell.text = text
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(11)
            if r == 0:
                p.font.bold = True
                p.font.color.rgb = WHITE

# ===== SLIDE 7: 消费趋势 =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
add_title_bar(slide, "消费趋势与渠道变革", "从「流量驱动」到「体验复购」的范式迁移")
add_footer(slide, 7)

# Spending trend
add_bar_chart(slide, Inches(0.3), Inches(1.5), Inches(4.5), Inches(2.4),
    "消费升级指标（同比）",
    ['跟团游客单价', '机票均价', '5晚+连住订单', '县域品质酒店'],
    [13, 10, 10, 76],
    [DARK_BLUE, MID_BLUE, LIGHT_BLUE, ACCENT_ORANGE])

# Booking channel chart
add_bar_chart(slide, Inches(5.3), Inches(1.5), Inches(4.5), Inches(2.4),
    "预订渠道变化信号",
    ['OTA(携程)', 'AI助手\n(DeepTrip)', '酒店直销\n/会员', '抖音/小红书\n内容种草'],
    [1, 80, 1, 1],
    [DARK_BLUE, ACCENT_ORANGE, LIGHT_BLUE, MID_GRAY])

# Traveler behavior
add_bullet_list(slide, Inches(0.3), Inches(4.2), Inches(6), Inches(2.6),
    [
        "跨省出行占比 +15ppts（首日）",
        "住宿天数 +1~2天",
        "跳城游 60%串联2-3城，线性串联订单40%+",
        "租车自驾50%+，平均租期4.3天",
        "海外替代游客单价+13%，高品质特征"
    ], "出行行为变革")

add_bullet_list(slide, Inches(6.5), Inches(4.2), Inches(6), Inches(2.6),
    [
        "AI预订入口高速渗透（DeepTrip引导+80%）",
        "OTA反垄断调查中，佣金结构或调整",
        "Color Walk社交驱动目的地选择（+200%搜索）",
        "体验复购 > 流量驱动（同程研究院判断）",
        "酒店需确保数据结构化，被AI可读取"
    ], "渠道与营销变革")

# ===== SLIDE 8: 风险与操作建议 =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, WHITE)
add_title_bar(slide, "风险因素与业主操作建议", "定价窗口 · 产品策略 · 渠道布局")
add_footer(slide, 8)

# Risk table
risk_data = [
    ['风险因素', '概率', '影响', 'Day1 状态'],
    ['出境回流超预期（上行）', '高', '利好国内酒店', '✅ 已显现'],
    ['油价上行抑制航空', '中', '民航或弱于预测', '暂未显著'],
    ['消费力压制高客单价', '中', '豪华型ADR承压', '替代游偏高端部分对冲'],
    ['五一后需求透支回落', '中', '5月中下旬', '⚠️ 需警惕'],
    ['天气突变', '低', '局部', '全国晴好'],
]
table = slide.shapes.add_table(len(risk_data), len(risk_data[0]), 
    Inches(0.3), Inches(1.5), Inches(6.2), Inches(2.2))
table.table.style = 'Medium Style 2 - Accent 1'
for r, row in enumerate(risk_data):
    for c, text in enumerate(row):
        cell = table.table.cell(r, c)
        cell.text = text
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(11)
            if r == 0:
                p.font.bold = True
                p.font.color.rgb = WHITE

# Pricing windows on right
add_bullet_list(slide, Inches(7), Inches(1.5), Inches(5.5), Inches(2.2),
    [
        "🔴 5/1-5/2：峰值定价，首日3.44亿验证",
        "🟡 5/2-5/3：维持或微调，票价回落40%",
        "🟠 5/4-5/5：关注返程退房潮",
        "🟢 5/6-5/10：错峰余量定价"
    ], "定价窗口建议")

# Product & Channel strategy
add_bullet_list(slide, Inches(0.3), Inches(4.0), Inches(6), Inches(2.7),
    [
        "亲子套餐：59%亲子出行，家庭联通房+亲子活动是溢价抓手",
        "连住优惠：跳城游+5晚+订单+10ppts，推多城联动套餐",
        "Color Walk场景：色彩目的地周边酒店，社交媒体出片率第一",
        "县域精品民宿：提前15天爆满，中档连锁品牌下沉正当时"
    ], "产品策略")

add_bullet_list(slide, Inches(7), Inches(4.0), Inches(5.5), Inches(2.7),
    [
        "OTA为主但监管收紧，加强直销/会员渠道建设",
        "AI预订入口（DeepTrip等）崛起 → 酒店数据结构化是趋势性投入",
        "小红书/抖音内容种草 → 成交链路需打通",
        "落地租车平台 → 酒店+租车打包套餐新机会"
    ], "渠道策略")

# ===== SLIDE 9: 总结 =====
slide = prs.slides.add_slide(prs.slide_layouts[6])
add_bg(slide, DARK_BLUE)
# White text on dark

txBox = slide.shapes.add_textbox(Inches(1), Inches(0.8), Inches(11), Inches(0.7))
tf = txBox.text_frame
p = tf.paragraphs[0]
p.text = "核心结论"
p.font.size = Pt(36)
p.font.bold = True
p.font.color.rgb = WHITE

txBox2 = slide.shapes.add_textbox(Inches(1), Inches(1.8), Inches(11), Inches(1.2))
tf2 = txBox2.text_frame
p2 = tf2.paragraphs[0]
p2.text = "2026年五一是中国酒店行业「供需再平衡」的关键验证节点。"
p2.font.size = Pt(22)
p2.font.color.rgb = ACCENT_ORANGE
p2 = tf2.add_paragraph()
p2.text = "供给增速收敛 + 需求结构质变 + 价格修复确立 = 行业拐点。"
p2.font.size = Pt(20)
p2.font.color.rgb = RGBColor(200, 210, 230)

# Three columns
conclusions = [
    ("📊 量", "间夜量 +6~7%", "出行人次 +4%\n跳城游+替代游双引擎"),
    ("💰 价", "ADR +6~7%", "全档次转正\n中高端实质性修复"),
    ("🏗️ 供", "供给增速 +6.5%", "从+7.4%持续收敛\n供需共振格局形成"),
]
for i, (title, main, detail) in enumerate(conclusions):
    left = Inches(1 + i * 4)
    box = slide.shapes.add_shape(1, left, Inches(3.2), Inches(3.6), Inches(2.4))
    box.fill.solid()
    box.fill.fore_color.rgb = RGBColor(0, 70, 120)
    box.line.fill.background()

    tx = slide.shapes.add_textbox(left + Inches(0.3), Inches(3.4), Inches(3), Inches(0.5))
    p = tx.text_frame.paragraphs[0]
    p.text = title
    p.font.size = Pt(24)
    p.font.color.rgb = WHITE

    tx2 = slide.shapes.add_textbox(left + Inches(0.3), Inches(3.9), Inches(3), Inches(0.5))
    p = tx2.text_frame.paragraphs[0]
    p.text = main
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = ACCENT_ORANGE

    tx3 = slide.shapes.add_textbox(left + Inches(0.3), Inches(4.5), Inches(3), Inches(1))
    p = tx3.text_frame.paragraphs[0]
    p.text = detail
    p.font.size = Pt(13)
    p.font.color.rgb = RGBColor(180, 210, 240)

# Bottom text
txBox4 = slide.shapes.add_textbox(Inches(1), Inches(6.5), Inches(11), Inches(0.5))
tf4 = txBox4.text_frame
p4 = tf4.paragraphs[0]
p4.text = "完整复盘报告：5月12日  数据日历：DATA-CALENDAR.md  |  B166ER Research  2026"
p4.font.size = Pt(11)
p4.font.color.rgb = RGBColor(150, 180, 200)
p4.alignment = PP_ALIGN.CENTER

# Save
output = r'C:\Users\Administrator\Desktop\2026五一全国酒店市场预测分析报告.pptx'
prs.save(output)
print(f'PPT saved: {output}')
print(f'Slides: {len(prs.slides)}')