# -*- coding: utf-8 -*-
"""
Generate AHL Government Support Channel List PDF V2 - Full National Coverage
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
LIGHT_GRAY = HexColor('#edf2f7')
ORANGE = HexColor('#dd6b20')

output_path = r"C:\Users\ericz\.openclaw\workspace\ppt_output\AHL-Tech\AHL-政府扶持渠道清单-全国版.pdf"
doc = SimpleDocTemplate(
    output_path,
    pagesize=A4,
    rightMargin=1.5*cm,
    leftMargin=1.5*cm,
    topMargin=1.5*cm,
    bottomMargin=1.5*cm
)

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='MainTitle', fontName='SimHei', fontSize=20, leading=26, textColor=DARK_BLUE, alignment=TA_CENTER, spaceAfter=10))
styles.add(ParagraphStyle(name='SubTitle', fontName='SimHei', fontSize=10, leading=14, textColor=GRAY, alignment=TA_CENTER, spaceAfter=20))
styles.add(ParagraphStyle(name='Section', fontName='SimHei', fontSize=14, leading=18, textColor=DARK_BLUE, spaceBefore=15, spaceAfter=8))
styles.add(ParagraphStyle(name='SubSection', fontName='SimHei', fontSize=11, leading=14, textColor=LIGHT_BLUE, spaceBefore=10, spaceAfter=5))
styles.add(ParagraphStyle(name='Body', fontName='SimHei', fontSize=9, leading=12, textColor='#2d3748', spaceAfter=4))
styles.add(ParagraphStyle(name='Small', fontName='SimHei', fontSize=8, leading=10, textColor=GRAY, spaceAfter=3))

story = []

# Title
story.append(Paragraph("AHL项目政府扶持渠道清单 V2.0", styles['MainTitle']))
story.append(Paragraph("全国省级申报渠道 + 在线申报平台 | 当前位置: 四川省成都市", styles['SubTitle']))
story.append(Paragraph("编制日期: 2026年3月24日", styles['SubTitle']))
story.append(Spacer(1, 10))

# 在线申报平台
story.append(Paragraph("一、国家级在线申报平台", styles['Section']))
table_data = [
    ['平台名称', '网址', '用途'],
    ['科技部火炬中心', 'https://fuwu.most.gov.cn', '国家级科技计划申报'],
    ['高新技术企业认定', 'https://www.innocom.gov.cn', '高新企业申报'],
    ['工信部AI专项申报', 'https://jzbp.miit.gov.cn', '专精特新/AI专项'],
    ['文旅部申报系统', 'http://zwgk.mct.gov.cn', '文旅部项目申报'],
    ['发改委重大项目', 'https://tzs.ndrc.gov.cn', '服务业/数字经济专项'],
]
t = Table(table_data, colWidths=[4*cm, 6*cm, 4*cm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ffffff')),
]))
story.append(t)
story.append(Spacer(1, 10))

# 四川省
story.append(Paragraph("二、四川省在线申报平台 (当前位置)", styles['Section']))
table_data2 = [
    ['平台', '网址', '用途'],
    ['四川省科技厅', 'https://kjt.sc.gov.cn', '省级科技计划'],
    ['四川省文旅厅', 'https://wlt.sc.gov.cn', '文旅产业专项资金'],
    ['四川省经信厅', 'http://gxt.sc.gov.cn', '专精特新/AI产业'],
    ['成都市科技局', 'http://cdstbg.gov.cn', '成都市级科技项目'],
    ['成都高新区', 'https://www.cdht.gov.cn', '高新区创新专项'],
    ['天府新区', 'https://www.cdtf.gov.cn', '天府新区产业扶持'],
]
t2 = Table(table_data2, colWidths=[3.5*cm, 6*cm, 4.5*cm])
t2.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), ACCENT),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#fff5f5')),
]))
story.append(t2)
story.append(PageBreak())

# 全国省级渠道汇总
story.append(Paragraph("三、全国省级申报渠道汇总", styles['Section']))

# 西南地区
story.append(Paragraph("3.1 西南地区 (四川/云南/贵州/西藏/重庆)", styles['SubSection']))
table_data3 = [
    ['省份', '科技厅网址', '文旅厅网址', '金额参考'],
    ['四川省', 'https://kjt.sc.gov.cn', 'https://wlt.sc.gov.cn', '¥30-1000万'],
    ['云南省', 'https://kjst.yn.gov.cn', 'http://whly.yn.gov.cn', '¥30-500万'],
    ['贵州省', 'http://kjt.guizhou.gov.cn', 'http://whly.guizhou.gov.cn', '¥30-500万'],
    ['西藏', 'http://sti.xizang.gov.cn', 'http://whly.xizang.gov.cn', '¥20-300万'],
    ['重庆市', 'http://kjj.cq.gov.cn', 'http://whlyw.cq.gov.cn', '¥30-500万'],
]
t3 = Table(table_data3, colWidths=[2*cm, 4.5*cm, 4.5*cm, 2.5*cm])
t3.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 7),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ffffff')),
]))
story.append(t3)
story.append(Spacer(1, 8))

# 华东地区
story.append(Paragraph("3.2 华东地区 (江苏/浙江/安徽/福建/江西/山东/上海)", styles['SubSection']))
table_data4 = [
    ['省份', '科技厅网址', '金额参考'],
    ['江苏省', 'https://kxjst.jiangsu.gov.cn', '¥50-1000万'],
    ['浙江省', 'https://kjt.zj.gov.cn', '¥50-1000万'],
    ['安徽省', 'http://kjt.ah.gov.cn', '¥50-500万'],
    ['福建省', 'http://kjt.fujian.gov.cn', '¥50-500万'],
    ['江西省', 'http://kxj.jiangxi.gov.cn', '¥30-300万'],
    ['山东省', 'http://kjt.shandong.gov.cn', '¥50-1000万'],
    ['上海市', 'http://stcsm.sh.gov.cn', '¥50-1000万'],
]
t4 = Table(table_data4, colWidths=[2*cm, 6*cm, 2.5*cm])
t4.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), LIGHT_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 7),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ffffff')),
]))
story.append(t4)
story.append(Spacer(1, 8))

# 华北/华南
story.append(Paragraph("3.3 华北/华南地区", styles['SubSection']))
table_data5 = [
    ['省份', '科技厅/科委网址', '金额参考'],
    ['北京市', 'http://kw.beijing.gov.cn', '¥50-2000万'],
    ['天津市', 'http://kxjs.tj.gov.cn', '¥50-500万'],
    ['河北省', 'http://kjt.hebei.gov.cn', '¥30-300万'],
    ['广东省', 'http://gdstei.gd.gov.cn', '¥50-1000万'],
    ['深圳市', 'https://stic.sz.gov.cn', '¥50-1000万'],
    ['海南省', 'http://kjt.hainan.gov.cn', '¥50-500万'],
]
t5 = Table(table_data5, colWidths=[2.5*cm, 6*cm, 2.5*cm])
t5.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), GREEN),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 7),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#f0fff4')),
]))
story.append(t5)
story.append(PageBreak())

# 申报优先级
story.append(Paragraph("四、申报优先级建议 (基于当前位置成都)", styles['Section']))

story.append(Paragraph("4.1 立即申报 (本月可操作)", styles['SubSection']))
table_data6 = [
    ['优先级', '项目', '渠道', '申报方式'],
    ['P0', '科技型中小企业认定', '国家', '在线申报'],
    ['P0', '高新技术企业认定', '国家', '在线申报 (4月第一批)'],
    ['P1', '成都市科技计划', '成都', '在线申报'],
    ['P1', '四川省AI产业专项', '四川', '在线申报'],
]
t6 = Table(table_data6, colWidths=[1.5*cm, 4*cm, 2.5*cm, 4*cm])
t6.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), ACCENT),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (0, 2), HexColor('#feb2b2')),
    ('BACKGROUND', (0, 3), (0, 4), HexColor('#fbd38d')),
]))
story.append(t6)
story.append(Spacer(1, 8))

story.append(Paragraph("4.2 短期申报 (3个月内)", styles['SubSection']))
table_data7 = [
    ['优先级', '项目', '渠道', '申报方式'],
    ['P2', '四川省文旅专项', '四川', '地方推荐'],
    ['P2', '成都高新区创新专项', '成都', '在线申报'],
    ['P2', '文旅部科技教育司项目', '国家', '省级推荐'],
]
t7 = Table(table_data7, colWidths=[1.5*cm, 4*cm, 2.5*cm, 4*cm])
t7.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), ORANGE),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#fffaf0')),
]))
story.append(t7)
story.append(Spacer(1, 10))

# 立即行动项
story.append(Paragraph("五、立即行动项", styles['Section']))
table_data8 = [
    ['行动', '负责', '时间'],
    ['在四川注册公司', '张实', '本周'],
    ['完成科技型中小企业认定', '张实', '1个月内'],
    ['申报成都市科技计划', '张实', '4-5月'],
    ['申报四川省AI产业专项', '张实', '本季度'],
    ['跟进文旅部科技教育司项目', '张实', '3-4月'],
]
t8 = Table(table_data8, colWidths=[5*cm, 2.5*cm, 3*cm])
t8.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), HexColor('#ffffff')),
    ('FONTNAME', (0, 0), (-1, -1), 'SimHei'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
    ('BACKGROUND', (0, 1), (-1, -1), HexColor('#ffffff')),
]))
story.append(t8)
story.append(Spacer(1, 15))

# Footer
story.append(Paragraph("声明: 以上信息基于公开政策整理，各省政策时有调整，请申报前务必访问官方网址确认最新要求。", styles['Small']))
story.append(Spacer(1, 5))
story.append(Paragraph("编制人: B166ER AI助手 | 编制日期: 2026年3月24日 | V2.0 (全国版)", styles['Small']))

doc.build(story)
print(f"PDF generated: {output_path}")
