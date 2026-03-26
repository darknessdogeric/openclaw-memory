# -*- coding: utf-8 -*-
"""
Generate AHL Government Support Channel List PDF
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
import os

# Register Chinese fonts
font_path = "C:/Windows/Fonts/simhei.ttf"
pdfmetrics.registerFont(TTFont('SimHei', font_path))

# Colors
DARK_BLUE = HexColor('#1a365d')
LIGHT_BLUE = HexColor('#3182ce')
ACCENT = HexColor('#e53e3e')
GRAY = HexColor('#718096')
LIGHT_GRAY = HexColor('#edf2f7')

# Create PDF
output_path = r"C:\Users\ericz\.openclaw\workspace\ppt_output\AHL-Tech\AHL-政府扶持渠道清单.pdf"
doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    rightMargin=2*cm,
    leftMargin=2*cm,
    topMargin=2*cm,
    bottomMargin=2*cm
)

# Styles
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name='MainTitle',
    fontName='SimHei',
    fontSize=24,
    leading=30,
    textColor=DARK_BLUE,
    alignment=TA_CENTER,
    spaceAfter=20
))
styles.add(ParagraphStyle(
    name='SubTitle',
    fontName='SimHei',
    fontSize=12,
    leading=16,
    textColor=GRAY,
    alignment=TA_CENTER,
    spaceAfter=30
))
styles.add(ParagraphStyle(
    name='Section',
    fontName='SimHei',
    fontSize=16,
    leading=20,
    textColor=DARK_BLUE,
    spaceBefore=20,
    spaceAfter=10
))
styles.add(ParagraphStyle(
    name='SubSection',
    fontName='SimHei',
    fontSize=13,
    leading=16,
    textColor=LIGHT_BLUE,
    spaceBefore=12,
    spaceAfter=6
))
styles.add(ParagraphStyle(
    name='Body',
    fontName='SimHei',
    fontSize=10,
    leading=14,
    textColor='#2d3748',
    spaceAfter=6
))
styles.add(ParagraphStyle(
    name='BodySmall',
    fontName='SimHei',
    fontSize=9,
    leading=12,
    textColor='#4a5568',
    spaceAfter=4
))
styles.add(ParagraphStyle(
    name='BulletPoint',
    fontName='SimHei',
    fontSize=10,
    leading=14,
    textColor='#2d3748',
    leftIndent=15,
    bulletIndent=5,
    spaceAfter=3
))

story = []

# Title
story.append(Paragraph("AHL项目政府扶持渠道清单", styles['MainTitle']))
story.append(Paragraph("AI赋能文旅产业创业项目申报指南", styles['SubTitle']))
story.append(Paragraph("编制日期: 2026年3月24日", styles['SubTitle']))
story.append(Spacer(1, 20))

# Section 1
story.append(Paragraph("一、政府扶持体系概览", styles['Section']))
story.append(Paragraph("1.1 扶持类型", styles['SubSection']))

table_data = [
    ['类型', '说明', '金额范围'],
    ['无偿资助', '不需要归还', '¥10万-¥3000万'],
    ['贷款贴息', '利息补贴', '最高100%贴息'],
    ['股权投资', '政府基金入股', '视项目评估'],
    ['税收优惠', '减免/抵扣', '15%税率等'],
    ['场地支持', '免租/补贴', '最高100%免租3年'],
]
t = Table(table_data, colWidths=[4*cm, 5*cm, 4*cm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), LIGHT_GRAY),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#ffffff'), LIGHT_GRAY]),
]))
story.append(t)
story.append(Spacer(1, 15))

# Section 2
story.append(Paragraph("二、国家级申报渠道", styles['Section']))

# 2.1 文旅部
story.append(Paragraph("2.1 文化和旅游部", styles['SubSection']))
story.append(Paragraph("渠道1: 文旅部科技教育司", styles['Body']))
table_data2 = [
    ['项目', '说明'],
    ['主管司局', '科技教育司'],
    ['申报方式', '每年定期发文通知'],
    ['申报时间', '通常3-4月/9-10月'],
    ['联系电话', '010-59882171'],
]
t2 = Table(table_data2, colWidths=[4*cm, 10*cm])
t2.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), LIGHT_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ffffff')),
]))
story.append(t2)
story.append(Spacer(1, 10))

story.append(Paragraph("相关政策:", styles['Body']))
story.append(Paragraph("• 文化和旅游科技创新工程", styles['BulletPoint']))
story.append(Paragraph("• 文化和旅游部重点实验室申报", styles['BulletPoint']))
story.append(Paragraph("• 国家文化和旅游科技创新项目", styles['BulletPoint']))
story.append(Spacer(1, 10))

# 2.2 科技部
story.append(Paragraph("2.2 科学技术部", styles['SubSection']))
story.append(Paragraph("渠道1: 火炬中心（国家级科技计划）", styles['Body']))
table_data3 = [
    ['项目', '说明'],
    ['主管单位', '科学技术部火炬高技术产业开发中心'],
    ['申报方式', '在线申报系统: https://fuwu.most.gov.cn'],
    ['申报时间', '全年受理，分批评审'],
    ['联系方式', '010-88656262'],
]
t3 = Table(table_data3, colWidths=[4*cm, 10*cm])
t3.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), LIGHT_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ffffff')),
]))
story.append(t3)
story.append(Spacer(1, 10))

story.append(Paragraph("相关计划:", styles['Body']))
story.append(Paragraph("• 国家重点研发计划: 信息技术/现代服务业", styles['BulletPoint']))
story.append(Paragraph("• 科技型中小企业技术创新基金", styles['BulletPoint']))
story.append(Paragraph("• AHL适配度: ⭐⭐⭐⭐⭐", styles['BulletPoint']))

story.append(PageBreak())

# 2.3 高新技术企业
story.append(Paragraph("2.3 国家高新技术企业认定", styles['SubSection']))
table_data4 = [
    ['项目', '说明'],
    ['申报网址', 'https://www.innocom.gov.cn'],
    ['申报时间', '每年3批 (4月/7月/10月)'],
    ['有效期', '3年'],
    ['税收优惠', '企业所得税15% (vs 标准25%)'],
    ['其他优惠', '研发加计扣除、落户加分等'],
    ['AHL适配度', '⭐⭐⭐⭐⭐'],
]
t4 = Table(table_data4, colWidths=[4*cm, 10*cm])
t4.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), ACCENT),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#fff5f5')),
]))
story.append(t4)
story.append(Spacer(1, 15))

# 2.4 工信部
story.append(Paragraph("2.4 工业和信息化部", styles['SubSection']))
story.append(Paragraph("渠道1: AI大模型专项（最匹配AHL）", styles['Body']))
table_data5 = [
    ['项目', '说明'],
    ['主管司局', '科技司/信息化推进司'],
    ['申报方式', '省级工信厅推荐'],
    ['重点方向', '行业大模型、垂直应用'],
    ['支持方式', '算力补贴+场景开放+资金支持'],
    ['AHL适配度', '⭐⭐⭐⭐⭐'],
]
t5 = Table(table_data5, colWidths=[4*cm, 10*cm])
t5.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#38a169')),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f0fff4')),
]))
story.append(t5)
story.append(Spacer(1, 15))

# Section 3
story.append(Paragraph("三、省级申报渠道", styles['Section']))

story.append(Paragraph("3.1 湖北省（张实所在地）", styles['SubSection']))
table_data6 = [
    ['部门', '政策名称', '申报方式', '联系方式'],
    ['湖北省科技厅', '湖北省科技计划项目', '在线申报', '027-87135826'],
    ['湖北省文旅厅', '湖北省文旅产业高质量发展专项资金', '地方文旅局推荐', '027-68892352'],
    ['湖北省经信厅', '湖北省专精特新中小企业培育', '在线申报', '027-87236586'],
    ['襄阳市科技局', '襄阳市科技计划项目', '在线+纸质', '0710-3511277'],
]
t6 = Table(table_data6, colWidths=[4*cm, 5*cm, 3*cm, 2.5*cm])
t6.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ffffff')),
]))
story.append(t6)
story.append(Spacer(1, 15))

story.append(Paragraph("3.2 云南省（文旅资源丰富）", styles['SubSection']))
table_data7 = [
    ['部门', '政策名称', '支持方向'],
    ['云南省文旅厅', '云南省文旅产业发展专项资金', '智慧旅游目的地建设'],
    ['云南省科技厅', '云南省科技计划项目', '数字云南建设'],
    ['云南省发改委', '云南省数字经济专项', '智慧旅游，数字小镇'],
]
t7 = Table(table_data7, colWidths=[4*cm, 5*cm, 5*cm])
t7.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), LIGHT_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ffffff')),
]))
story.append(t7)

story.append(PageBreak())

# Section 4
story.append(Paragraph("四、申报渠道优先级汇总", styles['Section']))

# Priority table
table_data8 = [
    ['优先级', '渠道', '申报时间', '适配度'],
    ['P0', '高新技术企业认定', '4月/7月/10月', '⭐⭐⭐⭐⭐'],
    ['P0', '科技型中小企业认定', '全年受理', '⭐⭐⭐⭐⭐'],
    ['P1', '襄阳市科技计划项目', '通常4-5月', '⭐⭐⭐⭐'],
    ['P1', '湖北省文旅发展资金', '通常Q1-Q2', '⭐⭐⭐⭐'],
    ['P2', '工信部AI大模型专项', '通常Q2-Q3', '⭐⭐⭐⭐⭐'],
    ['P2', '文旅部科技教育司项目', '3-4月/9-10月', '⭐⭐⭐⭐⭐'],
    ['P3', '国家重点研发计划', '通常Q2-Q3', '⭐⭐⭐'],
    ['P3', '省级文旅发展资金', '通常Q1-Q2', '⭐⭐⭐⭐'],
]
t8 = Table(table_data8, colWidths=[2*cm, 5*cm, 4*cm, 2.5*cm])
t8.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (0, 2), HexColor('#feb2b2')),
    ('BACKGROUND', (0, 3), (0, 4), HexColor('#fbd38d')),
    ('BACKGROUND', (0, 5), (0, 6), HexColor('#90cdf4')),
    ('BACKGROUND', (0, 7), (0, 8), HexColor('#c6f6d5')),
]))
story.append(t8)
story.append(Spacer(1, 15))

# Section 5
story.append(Paragraph("五、AHL项目申报建议", styles['Section']))

story.append(Paragraph("5.1 立即可申报", styles['SubSection']))
table_data9 = [
    ['项目', '理由', '预计时间'],
    ['高新技术企业认定', '税收优惠+门槛', '6-9个月'],
    ['科技型中小企业认定', '入门资质', '1-3个月'],
]
t9 = Table(table_data9, colWidths=[5*cm, 5*cm, 4*cm])
t9.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), ACCENT),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#fff5f5')),
]))
story.append(t9)
story.append(Spacer(1, 10))

story.append(Paragraph("5.2 短期目标(3个月内)", styles['SubSection']))
table_data10 = [
    ['项目', '理由', '预计时间'],
    ['襄阳市科技计划', '地方便利+快速启动', '3-6个月'],
    ['湖北省科技型中小企业技术创新基金', '匹配度高', '3-6个月'],
]
t10 = Table(table_data10, colWidths=[5*cm, 5*cm, 4*cm])
t10.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), HexColor('#dd6b20')),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#fffaf0')),
]))
story.append(t10)
story.append(Spacer(1, 15))

# Section 6
story.append(Paragraph("六、联系方式汇总", styles['Section']))

story.append(Paragraph("6.1 国家级", styles['SubSection']))
table_data11 = [
    ['部门', '电话', '邮箱/网址'],
    ['文旅部科技教育司', '010-59882171', 'kjjsc@mct.gov.cn'],
    ['科技部火炬中心', '010-88656262', 'zhangsq@ctp.gov.cn'],
    ['工信部科技司', '010-68207730', '-'],
]
t11 = Table(table_data11, colWidths=[4*cm, 3.5*cm, 6*cm])
t11.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ffffff')),
]))
story.append(t11)
story.append(Spacer(1, 10))

story.append(Paragraph("6.2 湖北省", styles['SubSection']))
table_data12 = [
    ['部门', '电话', '网址'],
    ['湖北省科技厅', '027-87135826', 'http://kjt.hubei.gov.cn'],
    ['湖北省文旅厅', '027-68892352', 'http://whly.hubei.gov.cn'],
    ['湖北省经信厅', '027-87236586', 'http://jxyt.hubei.gov.cn'],
    ['襄阳市科技局', '0710-3511277', 'http://kjj.xf.gov.cn'],
]
t12 = Table(table_data12, colWidths=[4*cm, 3.5*cm, 6*cm])
t12.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), LIGHT_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ffffff')),
]))
story.append(t12)
story.append(Spacer(1, 20))

# Footer
story.append(Paragraph("声明: 以上信息基于公开政策整理，具体申报要求以官方最新通知为准。", styles['BodySmall']))
story.append(Spacer(1, 10))
story.append(Paragraph("编制人: B166ER AI助手 | 编制日期: 2026年3月24日", styles['BodySmall']))

# Build PDF
doc.build(story)
print(f"PDF generated: {output_path}")
