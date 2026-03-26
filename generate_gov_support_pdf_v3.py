# -*- coding: utf-8 -*-
"""
Generate AHL Government Support Policy PDF V3 - Full Coverage with Match Degree
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER
import os

# Register Chinese fonts
font_path = "C:/Windows/Fonts/simhei.ttf"
pdfmetrics.registerFont(TTFont('SimHei', font_path))

# Colors
DARK_BLUE = HexColor('#1a365d')
LIGHT_BLUE = HexColor('#3182ce')
ACCENT = HexColor('#e53e3e')
GREEN = HexColor('#38a169')
GRAY = HexColor('#718096')
ORANGE = HexColor('#dd6b20')
PURPLE = HexColor('#805ad5')
LIGHT_GRAY = HexColor('#edf2f7')
RED = HexColor('#c53030')
YELLOW = HexColor('#d69e2e')

output_path = r"C:\Users\ericz\.openclaw\workspace\ppt_output\AHL-Tech\AHL-政府扶持政策全景申报表.pdf"
doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    rightMargin=1.2*cm,
    leftMargin=1.2*cm,
    topMargin=1.2*cm,
    bottomMargin=1.2*cm
)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='MainTitle', fontName='SimHei', fontSize=18, leading=24, textColor=DARK_BLUE, alignment=TA_CENTER, spaceAfter=8))
styles.add(ParagraphStyle(name='SubTitle', fontName='SimHei', fontSize=9, leading=12, textColor=GRAY, alignment=TA_CENTER, spaceAfter=15))
styles.add(ParagraphStyle(name='Section', fontName='SimHei', fontSize=12, leading=16, textColor=DARK_BLUE, spaceBefore=12, spaceAfter=6))
styles.add(ParagraphStyle(name='SubSection', fontName='SimHei', fontSize=10, leading=13, textColor=LIGHT_BLUE, spaceBefore=8, spaceAfter=4))
styles.add(ParagraphStyle(name='Body', fontName='SimHei', fontSize=8, leading=11, textColor='#2d3748', spaceAfter=3))
styles.add(ParagraphStyle(name='Small', fontName='SimHei', fontSize=7, leading=9, textColor=GRAY, spaceAfter=2))

story = []

# Title
story.append(Paragraph("AHL项目政府扶持政策全景申报表 V3.0", styles['MainTitle']))
story.append(Paragraph("能报尽报 · 匹配度全量化 · 可操作清单", styles['SubTitle']))
story.append(Paragraph("当前位置: 四川省成都市 | 目的: 最大化争取各地政府政策支持", styles['SubTitle']))
story.append(Spacer(1, 8))

# AHL与政策匹配框架
story.append(Paragraph("一、AHL核心特征与政策匹配框架", styles['Section']))
table_match = [
    ['AHL核心特征', '匹配政策方向', '匹配度'],
    ['AI大模型应用', 'AI专项、数字化转型、科技创新', '⭐⭐⭐⭐⭐'],
    ['文旅产业赋能', '文旅发展专项、智慧旅游、文旅融合', '⭐⭐⭐⭐⭐'],
    ['住宿业平台', '现代服务业、平台经济、中小企业扶持', '⭐⭐⭐⭐'],
    ['科技创新属性', '高新企业认定、研发费用加计扣除', '⭐⭐⭐⭐⭐'],
    ['创业阶段', '创新创业专项、人才引进、孵化器', '⭐⭐⭐⭐'],
    ['带动就业', '稳就业专项、人才专项', '⭐⭐⭐'],
]
t_match = Table(table_match, colWidths=[3.5*cm, 5.5*cm, 2*cm])
t_match.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ffffff')),
]))
story.append(t_match)
story.append(PageBreak())

# 国家级政策
story.append(Paragraph("二、国家级政策 (可全国申报)", styles['Section']))

story.append(Paragraph("2.1 科技部政策", styles['SubSection']))
table_data1 = [
    ['政策名称', '申报时间', '支持方式', '匹配度', '优先级'],
    ['国家重点研发计划', '全年受理', '¥500-3000万', '⭐⭐⭐⭐', 'P2'],
    ['科技型中小企业技术创新基金', '全年受理', '¥10-100万', '⭐⭐⭐⭐⭐', 'P1'],
    ['高新技术企业认定', '4/7/10月', '所得税15%', '⭐⭐⭐⭐⭐', 'P0'],
    ['科技型中小企业认定', '全年受理', '税收优惠+补贴', '⭐⭐⭐⭐⭐', 'P0'],
]
t1 = Table(table_data1, colWidths=[5*cm, 2.5*cm, 2.5*cm, 1.5*cm, 1.5*cm])
t1.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 7),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (0, 2), HexColor('#c6f6d5')),
    ('BACKGROUND', (0, 3), (0, 4), HexColor('#c6f6d5')),
    ('BACKGROUND', (-1, 1), (-1, 2), HexColor('#feb2b2')),
    ('BACKGROUND', (-1, 3), (-1, 4), HexColor('#feb2b2')),
]))
story.append(t1)
story.append(Spacer(1, 6))

story.append(Paragraph("2.2 工信部政策", styles['SubSection']))
table_data2 = [
    ['政策名称', '申报时间', '支持方式', '匹配度', '优先级'],
    ['AI大模型专项', 'Q2-Q3', '算力+¥500万+', '⭐⭐⭐⭐⭐', 'P1'],
    ['专精特新中小企业', '全年受理', '¥50-200万', '⭐⭐⭐⭐', 'P1'],
    ['软件企业税收优惠', '全年认证', '增值税即征即退', '⭐⭐⭐⭐⭐', 'P0'],
    ['数字化转型专项行动', 'Q2-Q3', '¥100-500万', '⭐⭐⭐⭐⭐', 'P1'],
]
t2 = Table(table_data2, colWidths=[5*cm, 2.5*cm, 2.5*cm, 1.5*cm, 1.5*cm])
t2.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), LIGHT_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 7),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (0, 1), HexColor('#c6f6d5')),
    ('BACKGROUND', (0, 2), (0, 2), HexColor('#fbd38d')),
    ('BACKGROUND', (0, 3), (0, 3), HexColor('#c6f6d5')),
    ('BACKGROUND', (0, 4), (0, 4), HexColor('#c6f6d5')),
]))
story.append(t2)
story.append(Spacer(1, 6))

story.append(Paragraph("2.3 文旅部政策 (AHL最匹配)", styles['SubSection']))
table_data3 = [
    ['政策名称', '申报时间', '支持方式', '匹配度', '优先级'],
    ['文化和旅游科技创新工程', '3-4月', '¥100-500万', '⭐⭐⭐⭐⭐', 'P1'],
    ['国家文化和旅游科技创新项目', '9-10月', '¥50-300万', '⭐⭐⭐⭐⭐', 'P1'],
    ['文旅部重点实验室', '全年申请', '算力+资金', '⭐⭐⭐⭐', 'P2'],
    ['文旅融合发展专项', '5-6月', '¥50-500万', '⭐⭐⭐⭐⭐', 'P1'],
    ['智慧旅游创新示范项目', '6-7月', '¥100-300万', '⭐⭐⭐⭐⭐', 'P1'],
]
t3 = Table(table_data3, colWidths=[5*cm, 2.5*cm, 2.5*cm, 1.5*cm, 1.5*cm])
t3.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), GREEN),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 7),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f0fff4')),
]))
story.append(t3)
story.append(PageBreak())

# 四川省政策
story.append(Paragraph("三、四川省政策 (当前位置 - 重点申报)", styles['Section']))

story.append(Paragraph("3.1 省级政策", styles['SubSection']))
table_sc1 = [
    ['政策名称', '申报时间', '支持方式', '匹配度', '优先级'],
    ['四川省科技计划项目', '3-4月', '¥50-500万', '⭐⭐⭐⭐⭐', 'P1'],
    ['四川省文旅产业高质量发展专项资金', 'Q1-Q2', '¥30-300万', '⭐⭐⭐⭐⭐', 'P1'],
    ['四川省AI产业发展专项', 'Q2-Q3', '¥100-1000万', '⭐⭐⭐⭐⭐', 'P1'],
    ['四川省数字经济专项', 'Q2-Q3', '¥100-500万', '⭐⭐⭐⭐⭐', 'P1'],
    ['四川省专精特新中小企业培育', '全年', '¥50-200万', '⭐⭐⭐⭐', 'P1'],
    ['四川省中小企业发展专项', '全年', '¥30-200万', '⭐⭐⭐⭐', 'P1'],
]
t_sc1 = Table(table_sc1, colWidths=[5.5*cm, 2*cm, 2.5*cm, 1.5*cm, 1.5*cm])
t_sc1.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), ACCENT),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 7),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#fff5f5')),
]))
story.append(t_sc1)
story.append(Spacer(1, 6))

story.append(Paragraph("3.2 成都市政策 (最优先)", styles['SubSection']))
table_sc2 = [
    ['政策名称', '申报时间', '支持方式', '匹配度', '优先级'],
    ['成都市科技计划项目', '4-5月', '¥20-200万', '⭐⭐⭐⭐⭐', 'P1'],
    ['成都市文旅专项', 'Q1-Q2', '¥30-200万', '⭐⭐⭐⭐⭐', 'P1'],
    ['成都市AI产业专项', 'Q2-Q3', '¥50-500万', '⭐⭐⭐⭐⭐', 'P1'],
    ['成都市新经济企业认定', '全年', '政策支持', '⭐⭐⭐⭐⭐', 'P1'],
    ['成都高新区AI专项', 'Q2-Q3', '¥100-1000万', '⭐⭐⭐⭐⭐', 'P1'],
    ['天府新区产业扶持', '全年', '场地+资金', '⭐⭐⭐⭐⭐', 'P1'],
]
t_sc2 = Table(table_sc2, colWidths=[5.5*cm, 2*cm, 2.5*cm, 1.5*cm, 1.5*cm])
t_sc2.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), RED),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 7),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#fff5f5')),
]))
story.append(t_sc2)
story.append(PageBreak())

# 全国省级政策汇总
story.append(Paragraph("四、全国省级政策汇总 (能报尽报)", styles['Section']))

story.append(Paragraph("4.1 西南地区", styles['SubSection']))
table_西南 = [
    ['省份', '科技政策', '文旅政策', '特色政策', '匹配度'],
    ['四川省', '省科技计划', '文旅专项', '成都AI专项/高新区', '⭐⭐⭐⭐⭐'],
    ['云南省', '省科技计划', '文旅专项', '丽江文旅数字化', '⭐⭐⭐⭐'],
    ['贵州省', '省科技专项', '文旅专项', '大数据专项', '⭐⭐⭐⭐'],
    ['重庆市', '市科技计划', '文旅专项', '两江新区数字经济', '⭐⭐⭐⭐'],
]
t_西南 = Table(table_西南, colWidths=[1.8*cm, 2.5*cm, 2.5*cm, 3*cm, 1.5*cm])
t_西南.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 7),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ffffff')),
]))
story.append(t_西南)
story.append(Spacer(1, 5))

story.append(Paragraph("4.2 华东地区 (政策力度最强)", styles['SubSection']))
table_华东 = [
    ['省份', '科技政策', '文旅政策', '特色政策', '匹配度'],
    ['江苏省', '省科技计划', '文旅专项', '苏州市AI专项', '⭐⭐⭐⭐⭐'],
    ['浙江省', '省科技计划', '文旅专项', '数字经济专项', '⭐⭐⭐⭐⭐'],
    ['上海市', '市科技计划', '文旅专项', '张江科学城专项', '⭐⭐⭐⭐⭐'],
    ['安徽省', '省科技计划', '文旅专项', '-', '⭐⭐⭐⭐'],
    ['福建省', '省科技计划', '文旅专项', '福州市数字经济', '⭐⭐⭐⭐'],
    ['山东省', '省科技计划', '文旅专项', '-', '⭐⭐⭐⭐'],
]
t_华东 = Table(table_华东, colWidths=[1.8*cm, 2.5*cm, 2.5*cm, 3*cm, 1.5*cm])
t_华东.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), LIGHT_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 7),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ffffff')),
]))
story.append(t_华东)
story.append(Spacer(1, 5))

story.append(Paragraph("4.3 华北/华南地区", styles['SubSection']))
table_other = [
    ['省份', '科技政策', '文旅政策', '特色政策', '匹配度'],
    ['北京市', '市科委计划', '文旅专项', '中关村创新专项', '⭐⭐⭐⭐⭐'],
    ['广东省', '省科技计划', '文旅专项', '深圳AI专项/大湾区', '⭐⭐⭐⭐⭐'],
    ['海南省', '省科技计划', '文旅专项', '自贸港专项', '⭐⭐⭐⭐⭐'],
    ['天津市', '市科技计划', '文旅专项', '滨海新区专项', '⭐⭐⭐⭐'],
    ['河北省', '省科技计划', '文旅专项', '雄安新区专项', '⭐⭐⭐⭐⭐'],
]
t_other = Table(table_other, colWidths=[1.8*cm, 2.5*cm, 2.5*cm, 3*cm, 1.5*cm])
t_other.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), GREEN),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 7),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f0fff4')),
]))
story.append(t_other)
story.append(PageBreak())

# 能报尽报清单
story.append(Paragraph("五、能报尽报清单 (按优先级排序)", styles['Section']))

story.append(Paragraph("5.1 P0级别 - 立即申报 (入场资质)", styles['SubSection']))
table_p0 = [
    ['政策名称', '申报方式', '理由'],
    ['科技型中小企业认定', '国家系统', '入门资质，长期有效'],
    ['高新技术企业认定', '国家系统 (4月第一批)', '税收优惠，门槛必备'],
    ['软件企业认证', '工信部', '增值税即征即退'],
]
t_p0 = Table(table_p0, colWidths=[5*cm, 3.5*cm, 4*cm])
t_p0.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), RED),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#fff5f5')),
]))
story.append(t_p0)
story.append(Spacer(1, 6))

story.append(Paragraph("5.2 P1级别 - 重点申报 (本月集中)", styles['SubSection']))
table_p1 = [
    ['政策名称', '申报渠道', '时间', '预估金额'],
    ['成都市科技计划', 'http://cdstbg.gov.cn', '4-5月', '¥20-200万'],
    ['四川省AI产业专项', 'https://kjt.sc.gov.cn', 'Q2-Q3', '¥100-1000万'],
    ['四川省文旅专项', 'https://wlt.sc.gov.cn', 'Q1-Q2', '¥30-300万'],
    ['成都高新区AI专项', 'https://www.cdht.gov.cn', 'Q2-Q3', '¥100-1000万'],
    ['天府新区产业扶持', 'https://www.cdtf.gov.cn', '全年', '场地+资金'],
    ['文旅部科技创新工程', 'http://zwgk.mct.gov.cn', '3-4月', '¥100-500万'],
]
t_p1 = Table(table_p1, colWidths=[4.5*cm, 4*cm, 2*cm, 2*cm])
t_p1.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), ORANGE),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 7),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#fffaf0')),
]))
story.append(t_p1)
story.append(Spacer(1, 6))

story.append(Paragraph("5.3 P2级别 - 积极申报 (3个月内)", styles['SubSection']))
table_p2 = [
    ['政策名称', '申报渠道', '时间', '预估金额'],
    ['科技型中小企业技术创新基金', 'https://fuwu.most.gov.cn', '全年', '¥10-100万'],
    ['专精特新中小企业', 'https://zjtx.miit.gov.cn', '全年', '¥50-200万'],
    ['工信部AI大模型专项', '省级工信厅推荐', 'Q2-Q3', '算力+¥500万+'],
    ['数字化转型专项行动', '省级经信厅', 'Q2-Q3', '¥100-500万'],
    ['国家文化和旅游科技创新项目', 'http://zwgk.mct.gov.cn', '9-10月', '¥50-300万'],
]
t_p2 = Table(table_p2, colWidths=[4.5*cm, 4*cm, 2*cm, 2*cm])
t_p2.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), YELLOW),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 7),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#fffff0')),
]))
story.append(t_p2)
story.append(PageBreak())

# 行动时间表
story.append(Paragraph("六、行动时间表", styles['Section']))

story.append(Paragraph("6.1 本周行动 (3月24日-3月31日)", styles['SubSection']))
table_action1 = [
    ['日期', '行动', '负责'],
    ['本周', '开始四川公司注册', '张实'],
    ['本周', '准备科技型中小企业申报材料', '张实'],
    ['本周', '联系成都高新区咨询', '张实'],
    ['本周', '联系天府新区咨询入驻', '张实'],
]
t_action1 = Table(table_action1, colWidths=[2*cm, 6*cm, 2.5*cm])
t_action1.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ffffff')),
]))
story.append(t_action1)
story.append(Spacer(1, 6))

story.append(Paragraph("6.2 4月行动", styles['SubSection']))
table_action2 = [
    ['日期', '行动', '负责'],
    ['4月初', '完成科技型中小企业认定', '张实'],
    ['4月初', '申报成都市科技计划', '张实'],
    ['4月中旬', '跟进高新企业第一批申报', '张实'],
    ['4月底', '准备四川省AI专项申报材料', '张实'],
]
t_action2 = Table(table_action2, colWidths=[2*cm, 6*cm, 2.5*cm])
t_action2.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), LIGHT_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ffffff')),
]))
story.append(t_action2)
story.append(Spacer(1, 10))

# 联系方式
story.append(Paragraph("七、核心联系方式", styles['Section']))
table_contact = [
    ['部门/地区', '电话', '网址'],
    ['科技部火炬中心', '010-88656262', 'https://fuwu.most.gov.cn'],
    ['文旅部科技教育司', '010-59882171', 'http://zwgk.mct.gov.cn'],
    ['工信部科技司', '010-68207730', 'https://www.miit.gov.cn'],
    ['四川省科技厅', '028-86729925', 'https://kjt.sc.gov.cn'],
    ['四川省文旅厅', '028-86948967', 'https://wlt.sc.gov.cn'],
    ['成都市科技局', '028-61881744', 'http://cdstbg.gov.cn'],
    ['成都高新区', '028-65877000', 'https://www.cdht.gov.cn'],
    ['天府新区', '028-68772522', 'https://www.cdtf.gov.cn'],
]
t_contact = Table(table_contact, colWidths=[3.5*cm, 3*cm, 5*cm])
t_contact.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 7),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ffffff')),
]))
story.append(t_contact)
story.append(Spacer(1, 15))

# Footer
story.append(Paragraph("声明: 以上政策信息基于公开资料整理，各省政策时有调整，请申报前务必访问官方网址或电话确认。", styles['Small']))
story.append(Paragraph("编制人: B166ER AI助手 | 编制日期: 2026年3月24日 | V3.0 (全景申报版)", styles['Small']))

doc.build(story)
print(f"PDF generated: {output_path}")
