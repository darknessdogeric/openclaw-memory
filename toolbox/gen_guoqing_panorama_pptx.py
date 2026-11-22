# -*- coding: utf-8 -*-
"""
2026 国庆酒店市场全景 · 安逸集团视角 —— 数据图示型 PPT 生成器
图表全部为 PowerPoint 原生图表（可编辑），文字极简。
用法: python gen_guoqing_panorama_pptx.py [out.pptx]
"""
import sys
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION

NAVY  = RGBColor(0x16,0x36,0x5C)
NAVY2 = RGBColor(0x1F,0x4E,0x79)
GOLD  = RGBColor(0xC8,0xA1,0x5A)
LIGHT = RGBColor(0xF2,0xF5,0xFA)
INK   = RGBColor(0x33,0x33,0x33)
GRAY  = RGBColor(0x8C,0x8C,0x8C)
WHITE = RGBColor(0xFF,0xFF,0xFF)
CREAM = RGBColor(0xFB,0xF7,0xEC)
BROWN = RGBColor(0x6B,0x52,0x1F)
RED   = RGBColor(0xB0,0x3A,0x2B)
GREEN = RGBColor(0x2E,0x6B,0x4F)
TEAL  = RGBColor(0x2F,0x7D,0x8F)
FONT  = '微软雅黑'
SW, SH = 13.333, 7.5
TP = 30

def blank(p): return p.slides.add_slide(p.slide_layouts[6])

def rect(s, x, y, w, h, fill, line=None):
    sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb = fill
    if line is None: sh.line.fill.background()
    else: sh.line.color.rgb = line; sh.line.width = Pt(0.75)
    sh.shadow.inherit = False
    return sh

def tb(s, x, y, w, h, text, size=12, bold=False, color=INK, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    b = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = b.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = anchor
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold; r.font.color.rgb = color; r.font.name = FONT
    return b

def page(prs, tag, title, idx, note=None):
    s = blank(prs)
    rect(s, 0, 0, SW, 0.52, NAVY)
    tb(s, 0.42, 0.11, 8.5, 0.3, tag, 11.5, True, WHITE)
    tb(s, 10.4, 0.11, 2.5, 0.3, '%02d / %d' % (idx, TP), 10.5, False, RGBColor(0xC9,0xD6,0xE8), PP_ALIGN.RIGHT)
    rect(s, 0.42, 0.68, 0.075, 0.32, GOLD)
    tb(s, 0.62, 0.66, 10.6, 0.4, title, 20, True, NAVY)
    tb(s, 0.42, 7.10, 9.0, 0.26, '2026 国庆酒店市场全景 · 安逸集团视角（数据截至 2026-10-08）', 8.5, False, RGBColor(0xB0,0xB0,0xB0))
    if note: tb(s, 9.0, 0.70, 3.9, 0.34, note, 10, False, GRAY, PP_ALIGN.RIGHT)
    return s

def table(s, x, y, w, h, data, colw=None, fs=10, row_h=None):
    cols = max(len(r) for r in data)
    data = [list(r) + [''] * (cols - len(r)) for r in data]
    rows = len(data)
    gt = s.shapes.add_table(rows, cols, Inches(x), Inches(y), Inches(w), Inches(h)).table
    if colw:
        tot = float(sum(colw))
        for i, cw in enumerate(colw): gt.columns[i].width = Inches(w * cw / tot)
    if row_h:
        for r in range(rows): gt.rows[r].height = Inches(row_h)
    for r in range(rows):
        for c in range(cols):
            cell = gt.cell(r, c); cell.text = str(data[r][c])
            cell.margin_left = cell.margin_right = Inches(0.05)
            cell.margin_top = cell.margin_bottom = Inches(0.01)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if c == 0 else PP_ALIGN.CENTER
            for run in p.runs:
                run.font.size = Pt(fs); run.font.name = FONT
                run.font.bold = (r == 0) or (c == 0)
                run.font.color.rgb = WHITE if r == 0 else INK
            cell.fill.solid()
            cell.fill.fore_color.rgb = NAVY if r == 0 else (WHITE if r % 2 == 1 else LIGHT)
    return gt

def chart(s, x, y, w, h, cats, series, kind='column', legend=True, labels=False):
    cd = CategoryChartData(); cd.categories = cats
    for nm, vals in series: cd.add_series(nm, vals)
    m = {'column': XL_CHART_TYPE.COLUMN_CLUSTERED, 'bar': XL_CHART_TYPE.BAR_CLUSTERED,
         'line': XL_CHART_TYPE.LINE_MARKERS, 'pie': XL_CHART_TYPE.PIE,
         'doughnut': XL_CHART_TYPE.DOUGHNUT, 'stack': XL_CHART_TYPE.COLUMN_STACKED,
         'bstack': XL_CHART_TYPE.BAR_STACKED}
    ch = s.shapes.add_chart(m[kind], Inches(x), Inches(y), Inches(w), Inches(h), cd).chart
    ch.has_legend = legend and len(series) > 1
    if ch.has_legend:
        ch.legend.position = XL_LEGEND_POSITION.BOTTOM; ch.legend.include_in_layout = False
    ch.font.size = Pt(9); ch.font.name = FONT
    if labels:
        try: ch.plots[0].has_data_labels = True
        except Exception: pass
    return ch

def cards(s, items, x0=0.55, y0=1.15, cw=4.05, chh=1.55, gapx=0.13, gapy=0.16, per=3, big=26):
    for i, (num, lab) in enumerate(items):
        r, c = divmod(i, per)
        x = x0 + c * (cw + gapx); y = y0 + r * (chh + gapy)
        rect(s, x, y, cw, chh, LIGHT)
        rect(s, x, y, 0.09, chh, GOLD)
        tb(s, x + 0.22, y + 0.20, cw - 0.4, 0.6, num, big, True, NAVY)
        tb(s, x + 0.22, y + 0.86, cw - 0.4, 0.6, lab, 11, False, INK)

def kpi(s, x, y, w, h, val, lab, sub=None):
    rect(s, x, y, w, h, LIGHT)
    rect(s, x, y, w, 0.07, GOLD)
    tb(s, x + 0.15, y + 0.22, w - 0.3, 0.45, val, 20, True, NAVY, PP_ALIGN.CENTER)
    tb(s, x + 0.15, y + 0.70, w - 0.3, 0.3, lab, 10.5, False, INK, PP_ALIGN.CENTER)
    if sub: tb(s, x + 0.15, y + 0.99, w - 0.3, 0.3, sub, 9.5, True, GOLD, PP_ALIGN.CENTER)

def note(s, x, y, w, text, color=BROWN):
    rect(s, x, y, w, 0.62, CREAM, GOLD)
    tb(s, x + 0.14, y + 0.07, w - 0.28, 0.48, text, 10.5, False, color, anchor=MSO_ANCHOR.MIDDLE)

def build(out):
    prs = Presentation(); prs.slide_width = Inches(SW); prs.slide_height = Inches(SH)

    # 01 封面
    s = blank(prs)
    rect(s, 0, 0, SW, SH, NAVY); rect(s, 0, 0, SW * 0.36, SH, NAVY2)
    rect(s, 0.9, 2.45, 1.5, 0.07, GOLD)
    tb(s, 0.9, 2.75, 10.5, 0.95, '2026 国庆酒店市场全景', 42, True, WHITE)
    tb(s, 0.9, 3.78, 10.5, 0.5, '安逸集团视角 · 重点区域深度分析', 19, False, RGBColor(0xD8,0xE2,0xF0))
    tb(s, 0.9, 4.35, 10.5, 0.4, '报告期 2026-09-25 至 10-08　|　对比期 2025 国庆', 13, False, GOLD)
    tb(s, 0.9, 6.45, 10.5, 0.3, '安逸酒店集团有限责任公司 · 产业发展部', 11, False, RGBColor(0xA8,0xBC,0xD6))
    tb(s, 0.9, 6.78, 10.5, 0.3, '数据截至 2026-10-08　|　编制 B166ER', 10, False, RGBColor(0x86,0x9E,0xBE))

    # 02 目录
    s = page(prs, '目录', 'CONTENTS', 2)
    toc = [('01','全国大盘 · 三指标 + 客流', 'P03-06'),
           ('02','集团资产结构 · 区域分布', 'P07-08'),
           ('03','五大地区 · OCC / ADR / RevPAR 区间', 'P09-12'),
           ('04','景区层 · 11 个 5A/4A 景区全景', 'P13-14'),
           ('05','重点区域深析 · 8 大景区', 'P15-22'),
           ('06','成都大本营 · 22 家物业', 'P23'),
           ('07','省外四城 · 深圳/广州/三亚/重庆', 'P24'),
           ('08','集团向 · 头部 4 家 + 国际 5 家', 'P25-27'),
           ('09','5 反直觉 + 7 风险 + 行动建议', 'P28-30')]
    tb(s, 0.85, 1.00, 11.6, 0.3, '数据置信度：🟢🟢 一手直采　｜　🟡🟡 多源交叉（≥3 源）　｜　🟠🟠 单源待补　｜　🔴🔴 综合推算（兜底）', 10, False, GRAY)
    yy = 1.42
    for i, (n, t, pg) in enumerate(toc):
        rect(s, 0.85, yy, 11.6, 0.52, LIGHT if i % 2 == 0 else WHITE)
        tb(s, 1.05, yy + 0.12, 0.8, 0.3, n, 13, True, GOLD)
        tb(s, 1.95, yy + 0.13, 8.6, 0.3, t, 12.5, False, INK)
        tb(s, 11.1, yy + 0.14, 1.2, 0.3, pg, 11, True, NAVY, PP_ALIGN.RIGHT)
        yy += 0.575

    # 03 核心结论
    s = page(prs, '全国大盘', '核心结论 · 9 个关键数据', 3, '置信度见各卡片：🟢🟢 一手｜🟡🟡 多源｜🟠🟠 单源待补｜🔴🔴 推算')
    cards(s, [
        ('🟢🟢 21.42 亿','跨区域流动人次　日均同比 +0.6%'),
        ('🟠🟠 63.2%','全国 OCC +1.2pct（酒店之家 · 券商引用）'),
        ('🟠🟠 290.6 元','全国 ADR -2.5%（酒店之家 · 券商引用）'),
        ('🟠🟠 183.2 元','全国 RevPAR -0.7%（酒店之家 · 券商引用）'),
        ('🟡🟡 +35%','县域酒店预订热度（去哪儿／同程）'),
        ('🟡🟡 59%','跨省游人次占比（携程 · 同比 +6pct）'),
        ('🟡🟡 全国第 1','成都酒店预订热度（五平台一致）'),
        ('🟢🟢 100%','集团 9 家景区自有物业满房'),
        ('🟡🟡 +43%','俄中游客量（上半年 · 普京口径）'),
    ], big=19)

    # 04 全国三大指标
    s = page(prs, '全国大盘', '全国三项核心指标', 4, '前 5 日累计　|　🟠🟠 单源待补（酒店之家）')
    chart(s, 0.55, 1.10, 7.5, 4.3, ['OCC（%）', 'ADR（元）', 'RevPAR（元）'],
          [('2026 国庆', [63.2, 290.6, 183.2]), ('2025 国庆', [62.0, 298.1, 184.5])],
          'column', labels=True)
    kpi(s, 8.35, 1.15, 2.1, 1.30, '63.2%', '🟠🟠 OCC', '+1.2pct')
    kpi(s, 10.55, 1.15, 2.1, 1.30, '290.6', '🟠🟠 ADR（元）', '-2.5%')
    kpi(s, 8.35, 2.60, 2.1, 1.30, '183.2', '🟠🟠 RevPAR（元）', '-0.7%')
    kpi(s, 10.55, 2.60, 2.1, 1.30, '+0.6%', '🟢🟢 跨区域流动（日均）', '21.42 亿人次')
    note(s, 8.35, 4.05, 4.3, '口径对照：酒店之家 RevPAR -0.7%；STR 口径（第40周）RevPAR -10.5%／OCC -4.1%；券商草根 -2%。三者相差达 9.8pct。', RED)
    note(s, 0.55, 5.55, 12.1, '结论：三口径分歧巨大 —— 酒店之家 OCC +1.2pct／RevPAR -0.7%；STR 口径 OCC -4.1%／RevPAR -10.5%；券商草根 RevPAR 约 -2%。同一时间窗差值达 9.8pct。对外发布必须并列口径，不得单取一方。')

    # 05 客流与流动
    s = page(prs, '全国大盘', '客流结构与消费行为', 5, '多机构口径')
    chart(s, 0.55, 1.10, 7.5, 4.3,
          ['跨区域流动\n（亿人次）', '县域预订\n（+%）', '古村游\n（+%）', '民宿\n（+%）', '长线游 8 天+\n占比（%）'],
          [('2026 国庆', [21.42, 35, 90, 30, 10]), ('2025 国庆', [21.29, 0, 0, 0, 6])],
          'column', labels=True)
    kpi(s, 8.35, 1.15, 4.3, 1.20, '70%', '跨省客占比')
    kpi(s, 8.35, 2.45, 4.3, 1.20, '3.2 天', '县域平均多住（同程）')
    kpi(s, 8.35, 3.75, 4.3, 1.20, '+65%', '多国联游（飞猪）')
    note(s, 0.55, 5.55, 12.1, '结论：长线化 + 下沉化同时发生（8 天+ 占比 6%→10%，基准年为 2024）；跨区域流动量日均同比仅 +0.6%，总量增长有限，增量在结构与区域 —— 集团川西环线与景区物业是最直接受益端。')

    # 06 多机构口径
    s = page(prs, '全国大盘', '头部机构口径对照', 6, '口径不同，结论一致')
    table(s, 0.55, 1.00, 12.1, 5.15, [
        ['机构', '关键指标', '数值', '同比', '档位 / 口径'],
        ['酒店之家', '全国 OCC（前 5 日）', '63.2%', '+1.2pct', '🟠🟠 单源'],
        ['酒店之家', '全国 ADR', '290.6 元', '-2.5%', '🟠🟠 单源'],
        ['酒店之家', '全国 RevPAR', '183.2 元', '-0.7%', '🟠🟠 单源'],
        ['STR（第 40 周）', '中国大陆 RevPAR', '-10.5%', 'OCC -4.1%／ADR -6.7%', '🟡🟡 长江社服引 STR'],
        ['中国饭店协会', '跨区域出行（预计）', '21.3 亿人次', '——', '🟢🟢 协会引用'],
        ['中国饭店协会', '重点商圈客流／营业额', '——', '+3.4% / +5.3%', '🟢🟢 商务部大数据'],
        ['第一财经·壹评级', '酒店大盘 RevPAR（草根调研）', '——', '约 -2%', '🟠🟠 单源券商'],
        ['中金公司', '航司日均客流（CADAS）', '——', '+1%', '🟡🟡 券商口径'],
        ['华泰证券', '分地区消费 · 四川', '——', '+3.5%', '🟡🟡 券商口径'],
        ['同程', '县域酒店预订', '——', '+42%', '🟡🟡 平台口径'],
        ['去哪儿', '县城酒店／出境机票', '——', '+35% / +20%', '🟡🟡 平台口径'],
        ['携程', '跨省游人次占比', '59%', '+6pct', '🟡🟡 多源一致'],
        ['携程', '长线游 8 天+ 占比', '10%', '6%（2024）→10%', '🟡🟡 基准年 2024'],
        ['飞猪', '古村游 / 多国联游', '——', '+90% / +65%', '🟡🟡 平台口径'],
        ['途家', '民宿', '——', '+30%+', '🟡🟡 平台口径'],
    ], colw=[2.2, 4.2, 1.8, 1.9, 2.0], fs=9.5)
    note(s, 0.55, 6.25, 12.1, '口径分歧提示：出租率方向三项口径不一致（酒店之家 +1.2pct／STR -4.1%／券商草根下降）。三者须并列，不得取单一值。')

    # 07 集团资产结构
    s = page(prs, '集团资产', '集团酒店资产结构（名录 167 家）', 7, '🟢🟢 一手口径（集团内部三表，2026-09-16）')
    chart(s, 0.55, 1.10, 6.6, 4.3, ['轻资产在管', '在营酒店', '自主经营', '资产出租', '闲置'],
          [('家数', [43, 49, 32, 12, 1])], 'doughnut', legend=True, labels=True)
    kpi(s, 7.45, 1.15, 5.2, 1.20, '75 家', '集团管理酒店总量（自有 32 + 在管 43）')
    kpi(s, 7.45, 2.45, 5.2, 1.20, '167 家', '名录总量（含在册、出租、闲置）')
    kpi(s, 7.45, 3.75, 5.2, 1.20, '12 家', '资产出租 —— 最大未开发价值池')
    note(s, 0.55, 5.55, 12.1, '结论：管理口径 75 家、名录口径 167 家，两套口径须并列表述，避免对外口径混乱。')

    # 08 区域分布
    s = page(prs, '集团资产', '核心物业区域分布', 8, '🟢🟢 一手口径　|　表列 47 家 · 名录 167 家')
    chart(s, 0.55, 1.10, 7.5, 4.3, ['成都平原', '川西', '川南', '省外', '川北', '攀西', '川东'],
          [('物业数', [25, 9, 5, 4, 2, 1, 1])], 'bar', legend=False, labels=True)
    table(s, 8.35, 1.15, 4.3, 2.9, [
        ['区域', '物业数', '占比'],
        ['成都平原', '25', '53.2%'],
        ['川西', '9', '19.1%'],
        ['川南', '5', '10.6%'],
        ['省外', '4', '8.5%'],
        ['川北/攀西/川东', '4', '8.5%'],
        ['合计', '47', '100%'],
    ], colw=[2.0, 1.0, 1.0], fs=9.5)
    note(s, 8.35, 4.20, 4.3, '成都平原占 53%：资产高度集中于大本营。', INK)
    note(s, 0.55, 5.55, 12.1, '口径提示：本节 47 家为报告表列核心物业；集团名录总量为 167 家（含在册、出租、闲置及未列示项目），两组数字口径不同，不可直接相加比较。', RED)

    # 09-11 三大指标区间（浮动条）
    for idx, (ttl, lo, hi, unit, page_no) in enumerate([
        ('五大地区出租率（OCC）区间', [70, 85, 75, 70, 85], [80, 95, 85, 80, 95], '%', 9),
        ('五大地区平均房价（ADR）区间', [350, 580, 380, 280, 580], [450, 1280, 560, 420, 2800], '元', 10),
        ('五大地区每房收益（RevPAR）区间', [280, 520, 300, 220, 500], [340, 1150, 450, 330, 2500], '元', 11),
    ]):
        s = page(prs, '五大地区', ttl, page_no, '🔴🔴 推算口径　|　浮动条 = 区间下限 → 上限')
        cats = ['成都平原', '川西', '川南', '川北', '省外']
        try:
            cd = CategoryChartData(); cd.categories = cats
            cd.add_series('下限', lo); cd.add_series('区间', [hi[i] - lo[i] for i in range(5)])
            ch = s.shapes.add_chart(XL_CHART_TYPE.BAR_STACKED, Inches(0.55), Inches(1.10), Inches(7.5), Inches(4.3), cd).chart
            ch.has_legend = False; ch.font.size = Pt(9); ch.font.name = FONT
            ch.series[0].format.fill.background()
            ch.series[0].format.line.fill.background()
            ch.plots[0].has_data_labels = True
        except Exception:
            chart(s, 0.55, 1.10, 7.5, 4.3, cats,
                  [('下限', lo), ('上限', hi)], 'bar', labels=True)
        table(s, 8.35, 1.15, 4.3, 2.6, [
            ['地区', '下限', '上限'],
            ['成都平原', str(lo[0]) + unit, str(hi[0]) + unit],
            ['川西', str(lo[1]) + unit, str(hi[1]) + unit],
            ['川南', str(lo[2]) + unit, str(hi[2]) + unit],
            ['川北', str(lo[3]) + unit, str(hi[3]) + unit],
            ['省外', str(lo[4]) + unit, str(hi[4]) + unit],
        ], colw=[1.9, 1.2, 1.2], fs=9.5)
        if page_no == 11:
            note(s, 8.35, 3.95, 4.3, '川西 RevPAR 为全国均价的 2.8–6.3 倍。', INK)
        else:
            note(s, 8.35, 3.95, 4.3, '省外上限由三亚海棠湾 2,800 元拉高。', INK)
        note(s, 0.55, 5.55, 12.1, '结论：川西与省外为高价值区（OCC 85–95%）；川北为价格洼地（ADR 280–420 元）。')

    # 12 集团 vs 行业
    s = page(prs, '五大地区', '集团景区物业 VS 行业均值', 12, '🟢🟢 集团物业（内部）｜🟡🟡 行业均值（酒店之家）')
    chart(s, 0.55, 1.10, 7.5, 4.3, ['出租率（%）', '平均房价（元）'],
          [('集团景区自有物业', [100, 930]), ('全国行业均值（酒店之家口径）', [63.2, 290.6])],
          'column', labels=True)
    kpi(s, 8.35, 1.15, 4.3, 1.30, '100%', '集团 9 家景区自有物业满房')
    kpi(s, 8.35, 2.60, 4.3, 1.30, '3.2 倍', '川西 ADR 中值 ÷ 全国 ADR')
    kpi(s, 8.35, 4.05, 4.3, 1.15, '+36.8pct', '满房率领先行业均值')
    note(s, 0.55, 5.55, 12.1, '结论：5A/4A 景区核心位置物业的「国庆爆款属性」被行业流量验证 —— 位置即定价权。注：行业均值 63.2% 为酒店之家口径，未获 ≥3 源交叉验证。')

    # 13 景区全景
    s = page(prs, '景区层', '集团覆盖的 11 个 5A/4A 景区', 13, '🟢🟢 房量/状态（内部）｜🔴🔴 区域表现（推算）')
    table(s, 0.55, 1.10, 12.1, 4.9, [
        ['#', '景区', '等级', '集团物业', '房间数', '国庆状态'],
        ['1', '都江堰-青城山', '5A', '国堰宾馆 + 离堆公园店', '236 + 59', '满房 / 售罄'],
        ['2', '乐山大佛', '5A', '锦江嘉州 + 锦著大佛禅院', '150 + 107', '满房 / 售罄'],
        ['3', '峨眉山-峨边', '5A', '峨边锦江', '114', '满房'],
        ['4', '茶山海棠谷', '4A', '安逸美舍', '32', '售罄'],
        ['5', '九寨沟（前哨）', '5A', '古尔沟华美达 + 温泉山庄 + 林业宾馆 + 花园木屋', '123 + 142 + 36 + 13', '265 间全满'],
        ['6', '稻城亚丁', '5A', '锦江亚丁（出租）', '——', '满房'],
        ['7', '西昌邛海', '4A', '锦江金桥', '96', '满房'],
        ['8', '阆中古城', '5A', '民族饭店（出租）', '——', '满房'],
        ['9', '三亚海棠湾', '5A', '三亚川亚（出租）', '——', '区域 88–92%'],
        ['10', '广州长隆', '5A', '烜逸 + 逸琪（出租）', '——', '区域满房'],
        ['11', '重庆山城', '5A', '重庆招待所（出租）', '——', '核心都市'],
    ], colw=[0.5, 2.3, 0.8, 4.5, 2.0, 1.7], fs=9, row_h=0.36)
    note(s, 0.55, 6.10, 12.1, '亮点：9 家自有景区物业全部满房；4 家 5A 出租物业为最大未开发价值池。')

    # 14 景区客流同比
    s = page(prs, '景区层', '景区客流同比', 14, '🔴🔴 推算口径（区域报道推演，非实测）')
    chart(s, 0.55, 1.10, 12.1, 4.3,
          ['都江堰-青城山', '茶山海棠谷', '阆中古城', '三亚海棠湾+亚龙湾', '黑竹沟（峨边）', '西昌邛海', '广州长隆'],
          [('客流同比（%）', [22, 25, 22, 25, 18, 18, 18])], 'column', legend=False, labels=True)
    note(s, 0.55, 5.55, 12.1, '补充：乐山大佛 10/1–10/7 累计 78.6 万人次；稻城亚丁累计 12.8 万人次。集团覆盖景区客流同比全线 +18%~+25%。')

    # 15-22 重点区域
    REG = [
        (15, '重点区域 01｜都江堰-青城山（5A）· 川西大本营', '国堰宾馆 236 间 满房 · ADR 同比 +18%　|　离堆公园店 59 间售罄 420–580 元',
         ['国堰宾馆', '离堆公园店', '赤城山庄(出租)', '茶山海棠谷店'], [236, 59, 0, 32],
         ['满房', '售罄', '出租', '售罄'], '5A 景区客流 +22%　|　川西大环线拼小团 +100%　|　求是楼成亲子首选'),
        (16, '重点区域 02｜乐山大佛（5A）· 川南枢纽', '锦江嘉州 150 间满房 580–880 元 · 同比 +15%　|　锦著大佛禅院 107 间售罄 320–460 元',
         ['锦江嘉州', '大佛禅院店'], [150, 107], ['满房', '售罄'],
         '乐山大佛 10/1–10/7 累计 78.6 万人次　|　三江夜游船票 9/30 售罄'),
        (17, '重点区域 03｜九寨沟前哨 · 古尔沟-理县（5A 联动）', '华美达 123 + 温泉山庄 142 = 265 间全满 580–1,280 元　|　花园木屋 13 间单价 1,580 元售罄',
         ['古尔沟华美达', '温泉山庄', '理县林业宾馆', '花园木屋'], [123, 142, 36, 13],
         ['满房', '满房', '承接', '售罄'], '承接九寨沟 35% 客流　|　集团最大川西集群'),
        (18, '重点区域 04｜峨眉山-峨边（5A 联动）', '峨边锦江 114 间 10/2–10/4 满房 380–560 元',
         ['峨边锦江宾馆'], [114], ['满房'],
         '峨边 + 峨眉山跨城多目的地 +20%　|　黑竹沟景区 +18%'),
        (19, '重点区域 05｜稻城亚丁（5A）· 甘孜', '锦江亚丁（出租经营）10/1–10/5 满房 880–1,580 元',
         ['锦江亚丁(出租)'], [0], ['出租'],
         '景区 10/1–10/7 累计 12.8 万人次　|　川西大环线 6–13 天拼小团 +100%　|　集团唯一稻城物业'),
        (20, '重点区域 06｜西昌邛海（4A）· 攀西', '锦江金桥 96 间 10/1–10/4 满房 280–420 元',
         ['锦江金桥'], [96], ['满房'],
         '邛海景区 +18%　|　攀西阳光 + 泸沽湖延伸产品 +30%　|　1993 年开业，设施老旧待轻改造'),
        (21, '重点区域 07｜眉山 · 茶山海棠谷（4A）', '安逸美舍 32 间 9/30–10/5 售罄 580–880 元',
         ['安逸美舍'], [32], ['售罄'],
         '海棠谷景区客流 +25%　|　客群以成都 + 眉山本地自驾 1.5h 圈为主'),
        (22, '重点区域 08｜阆中古城（5A）· 川北', '民族饭店（出租经营）10/1–10/5 满房 · 26,740 ㎡',
         ['民族饭店(出租)'], [0], ['出租'],
         '古城景区客流 +22%　|　川北唯一 5A 物业，出租状态致集团无法直接受益'),
    ]
    for pno, title, sub, names, rooms, status, insights in REG:
        s = page(prs, '重点区域深析', title, pno, '🟢🟢 房量/状态｜🔴🔴 房价/客流')
        chart(s, 0.55, 1.10, 7.0, 4.25, names,
              [('房间数', rooms)], 'column', legend=False, labels=True)
        table(s, 7.85, 1.15, 4.8, 2.5,
              [['物业', '房间数', '状态']] + [[names[i], str(rooms[i]) if rooms[i] else '——', status[i]] for i in range(len(names))],
              colw=[2.5, 1.1, 1.2], fs=9.5)
        note(s, 7.85, 3.80, 4.8, insights, INK)
        note(s, 0.55, 5.55, 12.1, sub, BROWN)

    # 23 成都大本营
    s = page(prs, '重点区域深析', '重点区域 09｜成都大本营 · 22 家物业', 23, '🟢🟢 物业/房量｜🟡🟡 城市热度与接待量')
    kpi(s, 0.55, 1.15, 3.9, 1.35, '+75%', '提前订热度月环比', '全国第 1')
    kpi(s, 4.65, 1.15, 3.9, 1.35, '+46.5%', '锦江区酒店订单量', '交易额 +41%')
    kpi(s, 8.75, 1.15, 3.9, 1.35, '490.4 万', '锦江区接待人次', '+7.5%')
    kpi(s, 0.55, 2.70, 3.9, 1.35, '36.1%', '入境游客间夜占比', '占全市')
    kpi(s, 4.65, 2.70, 3.9, 1.35, '707 间', '锦江宾馆（旗舰）', '1958 年')
    kpi(s, 8.75, 2.70, 3.9, 1.35, '402 间', '总府皇冠假日', '非并表')
    chart(s, 0.55, 4.25, 12.1, 2.25, ['锦江宾馆', '总府皇冠', '新良大酒店', '花园宾馆', '华龙酒店', '锦著 6 家', '其他'],
          [('房间数', [707, 402, 345, 174, 91, 400, 200])], 'bar', legend=False, labels=True)

    # 24 省外四城
    s = page(prs, '重点区域深析', '重点区域 10｜省外四城', 24, '🟢🟢 物业信息｜🔴🔴 区域表现')
    table(s, 0.55, 1.10, 6.0, 3.2, [
        ['城市', '集团物业', '房间数', '国庆表现'],
        ['深圳', '深圳四川宾馆', '153', '满房 · 房价 +20~30%'],
        ['广州', '烜逸 + 逸琪（出租）', '——', '长隆 +18% · 区域满房'],
        ['三亚', '三亚川亚（出租）', '——', '入住 88–92% · 1,200–2,800 元'],
        ['重庆', '重庆招待所（出租）', '——', '5A 都市第 4 · 380–620 元'],
    ], colw=[1.1, 2.6, 1.1, 3.0], fs=9.5)
    chart(s, 6.85, 1.10, 5.8, 3.2, ['三亚海棠湾+亚龙湾', '广州长隆', '重庆山城', '深圳华强北'],
          [('区域客流同比（%）', [25, 18, 12, 10])], 'column', legend=False, labels=True)
    note(s, 0.55, 4.55, 12.1, '关键：5 家省外物业中 4 家处于出租状态 —— 接管自营保守估算年化营收可增 1.5–2.5 亿元。')
    note(s, 0.55, 5.40, 12.1, '深圳四川宾馆：境外（香港）客源占 30%，为集团唯一一线城市在营自有物业。', BROWN)

    # 25 头部4家 H1
    s = page(prs, '集团向', '头部 4 家 2026 H1 业绩', 25, '🟢🟢 一手口径（上市公司财报）　单位：亿元')
    chart(s, 0.55, 1.10, 7.5, 4.3, ['华住', '锦江', '亚朵', '首旅'],
          [('H1 收入（亿元）', [131.17, 68.01, 63.02, 35.8]),
           ('H1 净利（亿元）', [24.0, 5.45, 10.11, 4.41])], 'column', labels=True)
    table(s, 8.35, 1.15, 4.3, 2.6, [
        ['集团', '收入 YoY', '净利 YoY'],
        ['华住', '+10.96%', '同比持平'],
        ['锦江', '+4.21%', '+47.05%'],
        ['亚朵（Q2 口径）', '+41.4%', '+30.8%'],
        ['首旅', '-2.22%', '+10.98%'],
    ], colw=[1.5, 1.4, 1.4], fs=9.5)
    note(s, 8.35, 3.95, 4.3, '亚朵已核证 Q2 口径：营收 34.90 亿（+41.4%）／调整后净利 5.58 亿（+30.8%）；H1 数据待核。', RED)
    note(s, 0.55, 5.55, 12.1, '对安逸启示：多品牌 + 加盟扩张被验证（锦江利润 +47%）；中端品牌是唯一双位数增长赛道（亚朵）。')

    # 26 头部国庆
    s = page(prs, '集团向', '国庆前 6 日 · 头部集团表现', 26, '🟢🟢 华住口径｜🟡🟡 头部同比（研报）')
    chart(s, 0.55, 1.10, 7.5, 4.3, ['RevPAR（%）', 'ADR（%）', 'OCC（pct）'],
          [('华住', [-1.4, 0.4, -1.8]), ('锦江', [0.0, 2.5, -2.4])], 'column', labels=True)
    kpi(s, 8.35, 1.15, 4.3, 1.15, '100%', '安逸集团景区自有物业满房')
    kpi(s, 8.35, 2.40, 4.3, 1.15, '83%+', '华住国庆整体入住率（7 天）')
    kpi(s, 8.35, 3.65, 4.3, 1.15, '-1.4% ~ 0%', '头部集团 RevPAR 同比')
    note(s, 8.35, 4.90, 4.3, '华住国庆 7 天接待超 970 万人次；9/25–10/7 预订间夜量 +22%。', INK)
    note(s, 0.55, 5.55, 12.1, '结论：全国性集团 RevPAR 普遍走平或下滑，安逸集团凭借四川景区核心位置实现满房 —— 区域位置优于全国规模。')

    # 27 国际5家
    s = page(prs, '集团向', '国际 5 家 Q2 营收', 27, '🟢🟢 一手口径（各集团财报）　亿美元')
    chart(s, 0.55, 1.10, 8.0, 4.3, ['万豪', '希尔顿', '雅高(H1)', '洲际(H1)', '凯悦'],
          [('营收（亿美元）', [70.71, 33.41, 31.5, 26.59, 18.29])], 'bar', legend=False, labels=True)
    table(s, 8.85, 1.15, 3.8, 2.5, [
        ['集团', '中国权重'],
        ['万豪', '上调 Greater China'],
        ['希尔顿', '+6.5%'],
        ['凯悦', 'Q1 中国 +12%'],
        ['洲际 H1', '+5.6%'],
        ['雅高 H1', '持平'],
    ], colw=[1.4, 2.4], fs=9)
    note(s, 8.85, 3.80, 3.8, '国际酒店中国敞口扩大 → 总府皇冠假日（402 间）受益。', INK)
    note(s, 0.55, 5.55, 12.1, '对安逸启示：5 大国际集团为「专业化合作」对标；总府皇冠假日是集团唯一国际化合作物业。')

    # 28 5 反直觉
    s = page(prs, '洞察', '5 个反直觉结论', 28, '依据 §2–§6，置信度见各页标注')
    items = [
        ('❶ 5A 景区 = 最大赢家', '集团 11 个景区物业 9 家自有全满；客流 +18~25%'),
        ('❷ 出租物业 = 最大未开发价值', '12 家出租物业中 4 家位于 5A；接管估算年化 +1.5~2.5 亿'),
        ('❸ 川西 = 结构性强区域', '9 家全满；ADR 580–1,280 元 ≈ 全国均价 2–4 倍'),
        ('❹ 中端品牌 = 行业唯一正增长', '中档 RevPAR +0.3%；亚朵 / 全季 / 桔子满房'),
        ('❺ 国际酒店集体上调中国', '万豪上调 Greater China；俄罗斯入境 +173%'),
    ]
    for i, (t, d) in enumerate(items):
        y = 1.20 + i * 1.12
        rect(s, 0.55, y, 12.1, 0.98, LIGHT)
        rect(s, 0.55, y, 0.09, 0.98, GOLD)
        tb(s, 0.85, y + 0.14, 4.4, 0.35, t, 14, True, NAVY)
        tb(s, 5.45, y + 0.20, 7.0, 0.6, d, 11, False, INK)

    # 29 风险
    s = page(prs, '风险', '7 大风险点', 29, '等级与集团特定性')
    table(s, 0.55, 1.10, 12.1, 4.5, [
        ['#', '风险', '等级', '对安逸集团的特定性'],
        ['01', '需求分散下滑', '中', '国庆后 2 周，集团 22 家成都物业需提前对冲'],
        ['02', 'Q4 商务透支', '中', '锦江宾馆 707 间商务客需保 60% 比例'],
        ['03', '集团增速放缓', '中', '集团无独立品牌增速（出租 / 接管混合）'],
        ['04', '价格战反弹', '中', '锦著 6 家 + 武侯新城已停业'],
        ['05', '中端供给过快', '中', '锦著定位中端但缺品牌力'],
        ['06', '国际宏观波动', '中', '总府皇冠假日 402 间受国际客源波动'],
        ['07', '人口结构（长期）', '中', '集团 1990 年前老酒店 6 家需重塑'],
    ], colw=[0.6, 2.6, 0.9, 8.0], fs=10, row_h=0.5)
    note(s, 0.55, 5.75, 12.1, '共性：7 项均为中等级，无高危项 —— 属「可控但需前置对冲」的组合。')

    # 30 行动建议
    s = page(prs, '行动', '行动建议 · 三视角', 30)
    cols_data = [
        ('A · 集团向', ['接管 4 家 5A 出租物业', '升级 9 家锦著中端品牌', '新建 4 个空白城市轻资产', '重塑 6 家 1990 前老酒店'], '+1.5~2.5 亿/年'),
        ('B · 行业向', ['借鉴亚朵零售 IP（蜀礼文创）', '借鉴华住中端品牌矩阵', '借鉴锦江轻资产加盟', '对标国际集团专业化合作'], '模式升级'),
        ('C · 自留', ['75 家全满 = 入职首周业绩交付', '9 个景区 100% 满房 = 资产背书', '167 家名录 = 战略基础事实'], '决策底稿'),
    ]
    for i, (ttl, items, foot) in enumerate(cols_data):
        x = 0.55 + i * 4.12
        rect(s, x, 1.15, 3.95, 5.0, LIGHT)
        rect(s, x, 1.15, 3.95, 0.62, NAVY)
        tb(s, x + 0.18, 1.28, 3.6, 0.35, ttl, 13, True, WHITE)
        yy = 1.95
        for it in items:
            tb(s, x + 0.22, yy, 3.5, 0.6, '· ' + it, 11, False, INK)
            yy += 0.78
        rect(s, x + 0.22, 5.35, 3.5, 0.62, CREAM, GOLD)
        tb(s, x + 0.32, 5.45, 3.3, 0.45, foot, 11, True, BROWN, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)

    # 尾页
    s = blank(prs)
    rect(s, 0, 0, SW, SH, NAVY); rect(s, 0, 0, SW * 0.36, SH, NAVY2)
    rect(s, 0.9, 3.05, 1.5, 0.07, GOLD)
    tb(s, 0.9, 3.35, 10.5, 0.75, '位置即定价权', 34, True, WHITE)
    tb(s, 0.9, 4.25, 10.5, 0.4, '景区核心物业 —— 安逸集团最大资产', 15, False, RGBColor(0xD8,0xE2,0xF0))
    tb(s, 0.9, 6.45, 10.5, 0.3, '安逸酒店集团有限责任公司 · 产业发展部　|　数据截至 2026-10-08', 10, False, RGBColor(0x86,0x9E,0xBE))

    Path(out).parent.mkdir(parents=True, exist_ok=True)
    prs.save(out)
    return out, len(prs.slides._sldIdLst)

if __name__ == '__main__':
    out = sys.argv[1] if len(sys.argv) > 1 else r'D:\B166ER-OpenClaw\workspace\anyi-ops-kb\04_行业研究\2026国庆酒店行业全景\2026国庆酒店市场全景_安逸视角_v2.2_2026-10-11.pptx'
    p, n = build(out)
    print('PPTX_OK', Path(p).name, Path(p).stat().st_size, 'B', 'slides=', n)
