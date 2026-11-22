# -*- coding: utf-8 -*-
"""2026 H1 中国酒店业八大角色多视角分析专题 v6.0 PDF"""
import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle
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
sty_t = ParagraphStyle('T', parent=styles['Title'], fontName='NotoSC-Bold', fontSize=22, leading=30, alignment=TA_CENTER, textColor=C_ASH, spaceAfter=10)
sty_h1 = ParagraphStyle('H1', parent=styles['Heading1'], fontName='NotoSC-Bold', fontSize=16, leading=23, textColor=C_CRIMSON, spaceBefore=14, spaceAfter=8)
sty_h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontName='NotoSC-Bold', fontSize=13, leading=19, textColor=C_INDIGO, spaceBefore=10, spaceAfter=5)
sty_b = ParagraphStyle('B', parent=styles['Normal'], fontName='NotoSC', fontSize=9, leading=13, alignment=TA_JUSTIFY, textColor=C_ASH, spaceBefore=2, spaceAfter=4)
sty_bl = ParagraphStyle('BL', parent=styles['Normal'], fontName='NotoSC', fontSize=8.5, leading=12, leftIndent=14, bulletIndent=2, textColor=C_ASH)
sty_m = ParagraphStyle('M', parent=styles['Normal'], fontName='NotoSC', fontSize=10, leading=15, alignment=TA_CENTER, textColor=C_ASH, spaceAfter=5)
sty_q = ParagraphStyle('Q', parent=styles['Normal'], fontName='NotoSC', fontSize=10, leading=15, alignment=TA_LEFT, textColor=C_CRIMSON, leftIndent=18, rightIndent=18, spaceBefore=6, spaceAfter=6)

def hf(canvas, doc):
    canvas.saveState()
    canvas.setFont('NotoSC', 8)
    canvas.setFillColor(C_ASH)
    canvas.drawString(2*cm, 27.5*cm, '2026 H1 中国酒店业八大角色多视角分析专题 v6.0')
    canvas.drawRightString(18*cm, 27.5*cm, 'B166ER | 2026-07-27')
    canvas.line(2*cm, 27.3*cm, 18*cm, 27.3*cm)
    canvas.setFont('NotoSC', 8)
    canvas.setFillColor(colors.gray)
    canvas.drawCentredString(10*cm, 1.5*cm, f'— 第 {doc.page} 页 —')
    canvas.restoreState()

doc = SimpleDocTemplate(
    'D:/B166ER-OpenClaw/workspace/reports/2026H1中国酒店业八大角色多视角分析专题-v6.0.pdf',
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
S.append(Paragraph('中国酒店业八大角色', sty_t))
S.append(Paragraph('多视角分析专题', sty_t))
S.append(Spacer(1, 0.4*cm))
S.append(Paragraph('v6.0 · 从业者/经营者/投资人/业主/品牌方/单店/集团/轻资产酒管', sty_m))
S.append(Spacer(1, 0.3*cm))
S.append(Paragraph('编制：B166ER  |  时间：2026-07-27 08:03 GMT+8', sty_m))
S.append(Paragraph('依据：v4.0 七维度 + v5.0 三层纵深 + Eric 7/27 多视角指令', sty_m))
S.append(Spacer(1, 1.2*cm))

S.append(Paragraph('⚠️ v6.0 vs v4.0/v5.0 关键差异', sty_h2))
S.append(Paragraph('v4.0 = <b>横切</b>（八维度全景盘点）', sty_b))
S.append(Paragraph('v5.0 = <b>纵深</b>（历史+现状+未来+大陆专属）', sty_b))
S.append(Paragraph('v6.0 = <b>角色化</b>（八大视角立体扫描）', sty_b))
S.append(Spacer(1, 0.2*cm))
S.append(Paragraph('v4.0 回答"是什么"，v5.0 回答"从哪里来、现在哪里、未来去哪里"，v6.0 回答"<b>对我意味着什么、我该怎么做</b>"', sty_q))
S.append(PageBreak())

# ========== 执行摘要 ==========
S.append(Paragraph('执行摘要', sty_h1))

S.append(Paragraph('1. 八大角色全景', sty_h2))
role_overview = [
    ['角色', '关键指标', 'H1 2026 处境', '核心机会'],
    ['从业者', '工资/职业发展', '中端化+AI 替代双重压力', '银发康养/AI 培训师'],
    ['经营者', 'OCC/ADR/RevPAR/餐饮毛利', '五一高基数承压', 'AI RM 降本'],
    ['投资人', 'ROE/Cap Rate/退出', '资产 Cap Rate 下行', 'REITs 化退出通道'],
    ['业主', '物业估值/翻牌收益', '出清与翻牌双重机会', '第三方资管'],
    ['品牌方', '会员/中央预订/品牌矩阵', '加盟翻牌井喷', '主题细分品牌'],
    ['单店', 'OCC/私域占比/获客成本', '连锁挤压 + 翻牌窗口', '翻牌加盟/精品化'],
    ['集团', '翻牌门店数/REITs 池/AI 自研', 'REITs 化集中爆发', '翻牌+REITs+资管三轨'],
    ['轻资产酒管', '加盟费/翻牌速度/坪效', '翻牌井喷 → 服务能力跟不上', '海外扩张/AI 工具'],
]
S.append(make_table(role_overview, [2.5*cm, 3.5*cm, 4.5*cm, 5*cm], head_bg=C_INDIGO))
S.append(Spacer(1, 0.3*cm))

S.append(Paragraph('2. 三大跨角色洞察', sty_h2))

S.append(Paragraph('洞察 1：角色冲突矩阵', sty_h2))
conflicts = [
    ['关系', '冲突点', '本质', '解决路径'],
    ['投资人 vs 业主', 'Cap Rate vs 物业升值', '接盘方 vs 出货方', 'REITs 化平衡'],
    ['集团 vs 业主', '翻牌加速 vs 业主收益', '规模扩张 vs 单店利益', '第三方资管'],
    ['品牌方 vs 单店', '中央预订 vs 私域', '中央化 vs 地方化', '平衡点'],
    ['集团 vs 从业者', 'AI 替代 vs 职业发展', '效率 vs 稳定', '培训转型'],
    ['品牌方 vs OTA', '会员 vs 渠道', '独立 vs 借力', '平衡+反垄断'],
]
S.append(make_table(conflicts, [3.5*cm, 3.5*cm, 4.5*cm, 4*cm], head_bg=C_CRIMSON))
S.append(Spacer(1, 0.2*cm))

S.append(Paragraph('洞察 2：AI 时代的赢家与输家', sty_h2))
ai_win = [
    ['角色', '赢家画像', '输家画像'],
    ['从业者', 'AI 培训师/银发康养管家', '传统前台/客服'],
    ['经营者', 'AI RM 深度使用者', '拒绝 AI 工具'],
    ['投资人', 'REITs 配置/AI 资管', '重资产持有'],
    ['业主', '翻牌收购/REITs 化', '不做决策'],
    ['品牌方', 'AI Agent 协议层', '单一中央化'],
    ['单店', '精品化/AHL 接入', '拒绝数字化'],
    ['集团', '翻牌+REITs+AI 三轨', '单一扩张'],
    ['轻资产酒管', 'AI 赋能+协议化', '传统加盟'],
]
S.append(make_table(ai_win, [3*cm, 6.5*cm, 6*cm], head_bg=C_JADE))
S.append(Spacer(1, 0.2*cm))

S.append(Paragraph('洞察 3：8 大角色的共同方向', sty_h2))
S.append(Paragraph('1. <b>数据资产化</b>：每个角色都需要"数据→决策"闭环', sty_b))
S.append(Paragraph('2. <b>轻资产化</b>：从"持有"转向"运营"', sty_b))
S.append(Paragraph('3. <b>专业化分工</b>：每个角色做自己最擅长的部分', sty_b))
S.append(PageBreak())

S.append(Paragraph('3. Eric 个人 4 重角色定位', sty_h2))
S.append(Paragraph('Eric 同时承担 4 重角色，建议按优先级排序：', sty_b))
S.append(Paragraph('1. <b>AHL 创始人（投资人 + 品牌方 + 轻资产酒管）</b> — 最关键 🔴', sty_b))
S.append(Paragraph('2. <b>安逸集团产业发展部部长（集团 + 业主）</b> — 战略级 🟠', sty_b))
S.append(Paragraph('3. <b>酒店业老兵（经营者 + 从业者）</b> — 基础级 🟡', sty_b))
S.append(Paragraph('4. <b>个人品牌（品牌方 + 投资人）</b> — 长期级 🟢', sty_b))
S.append(PageBreak())

# ========== 第一章 从业者 ==========
S.append(Paragraph('第一章  从业者视角（Practitioners）', sty_h1))

S.append(Paragraph('1.1 角色定义', sty_h2))
S.append(Paragraph('酒店业从业者 = 直接服务客人的前线员工 + 后台运营人员 + 中高层管理者', sty_b))

S.append(Paragraph('1.2 核心关注点', sty_h2))
S.append(Paragraph('1. 工资水平  2. 职业发展  3. 工作稳定性  4. 技能升级  5. 工作强度', sty_b))

S.append(Paragraph('1.3 H1 2026 现状', sty_h2))
S.append(Paragraph('岗位薪资基准（v6.0 综合）：', sty_b))
salary = [
    ['岗位', '一线城市 (¥/月)', '二线城市 (¥/月)', '三四线城市 (¥/月)'],
    ['前台/礼宾', '6,000-9,000', '4,500-7,000', '3,500-5,500'],
    ['客房/餐饮', '5,000-7,500', '4,000-6,000', '3,000-4,500'],
    ['销售经理', '10,000-18,000', '8,000-13,000', '6,000-10,000'],
    ['店长（150 间）', '15,000-25,000', '12,000-18,000', '9,000-15,000'],
    ['区域经理', '25,000-40,000', '20,000-30,000', '15,000-22,000'],
    ['集团高管', '50,000-150,000+', '35,000-80,000', '25,000-50,000'],
]
S.append(make_table(salary, [3*cm, 4*cm, 4*cm, 4.5*cm]))
S.append(Spacer(1, 0.2*cm))

S.append(Paragraph('职业发展路径：前台 → 领班 → 主管 → 店长 → 区域经理 → 集团高管（7-10 年）', sty_b))

S.append(Paragraph('1.4 核心挑战', sty_h2))
S.append(Paragraph('🔴 <b>AI 替代风险</b>：5-7 年内 30-40% 前台/客服岗位将被 AI 替代', sty_b))
S.append(Paragraph('🟠 <b>工资上行空间收窄</b>：AI 降本压力下基础工资受压', sty_b))
S.append(Paragraph('🟡 <b>行业吸引力下降</b>：35 岁危机 + Z 世代不愿从事高强度服务', sty_b))

S.append(Paragraph('1.5 5 条战略路径', sty_h2))
paths = [
    ['路径', '适合人群', '关键动作', '预期收益'],
    ['A: AI 复合技能升级', '25-40 岁技术敏感型', '1 年内掌握 AI RM/数据分析', '工资 +30-50%'],
    ['B: 银发康养转型', '30-45 岁服务型', '考取健康管理师/老年照护师', '行业转型期红利'],
    ['C: 海外派遣/出海', '25-35 岁愿意闯荡', '学习外语+申请国际品牌海外岗', '工资 ×2-3'],
    ['D: 数字化营销', '25-35 岁内容创作型', '私域运营/小红书/抖音', '收入多元化'],
    ['E: 创业单店/民宿', '30-45 岁有资本', '收购翻牌/精品民宿', '长期资产积累'],
]
S.append(make_table(paths, [3*cm, 3.5*cm, 4.5*cm, 4.5*cm], head_bg=C_JADE))
S.append(Spacer(1, 0.2*cm))

S.append(Paragraph('1.6 短/中/长期行动建议', sty_h2))
S.append(Paragraph('<b>短期（2026 H2 - 2027）</b>：盘点技能缺口，优先补 AI 工具；申请集团管培生项目；开始运营个人 IP', sty_b))
S.append(Paragraph('<b>中期（2027-2030）</b>：转型银发康养/医养管家/精品民宿；完成"酒店员工→生活方式服务商"升级', sty_b))
S.append(Paragraph('<b>长期（2028-2040）</b>：成为 AI+康养+跨境复合型高端人才或创业', sty_b))

S.append(Paragraph('1.7 风险预警', sty_h2))
S.append(Paragraph('🔴 35 岁危机  🔴 AI 替代（5-7 年内 30-40%）  🟠 行业收缩风险', sty_b))
S.append(PageBreak())

# ========== 第二章 经营者 ==========
S.append(Paragraph('第二章  经营者视角（Operators/Managers）', sty_h1))

S.append(Paragraph('2.1 角色定义', sty_h2))
S.append(Paragraph('酒店经营者 = 直接负责单店或区域运营的中高层管理者（店长/驻店经理/餐饮总监/收益经理）', sty_b))

S.append(Paragraph('2.2 核心关注点', sty_h2))
S.append(Paragraph('1. 运营效率  2. 成本控制  3. 服务质量  4. 营收结构  5. 团队稳定', sty_b))

S.append(Paragraph('2.3 H1 2026 现状 - 核心 KPI', sty_h2))
kpi_ops = [
    ['指标', '经济型', '中端', '高端', '奢华'],
    ['OCC', '55-65%', '60-70%', '65-75%', '70-80%'],
    ['ADR (¥)', '150-250', '250-400', '400-800', '800-1,500+'],
    ['RevPAR (¥)', '85-160', '160-280', '280-560', '600-1,200+'],
    ['客房毛利', '50-60%', '60-70%', '65-75%', '70-80%'],
    ['餐饮毛利', '45-55%', '48-58%', '50-60%', '52-62%'],
    ['整体毛利', '48-58%', '52-62%', '55-65%', '58-68%'],
    ['EBITDA 率', '10-20%', '15-25%', '22-32%', '28-38%'],
    ['人效（万/人/年）', '10-16', '16-24', '22-32', '28-40'],
]
S.append(make_table(kpi_ops, [3*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2.5*cm], head_bg=C_INDIGO))
S.append(Spacer(1, 0.2*cm))

S.append(Paragraph('2.4 核心挑战', sty_h2))
S.append(Paragraph('🔴 <b>五一高基数效应</b>：OCC 63.5%（vs 71.42%，-7.92pp）/ ADR ¥295.98（vs ¥448.58，-34%）', sty_b))
S.append(Paragraph('🟠 <b>餐饮毛利低</b>：46-56% vs 客房 66-76% → 人力成本高 + 食材损耗大', sty_b))
S.append(Paragraph('🟠 <b>能耗成本上行</b>：7/31 国内成品油或上调 0.7 元/升 + 美伊冲突', sty_b))
S.append(Paragraph('🟡 <b>AI 工具应用门槛</b>：需要 1-2 个月学习曲线', sty_b))

S.append(Paragraph('2.5 5 个战略杠杆', sty_h2))
levers = [
    ['杠杆', '关键动作', '预期收益'],
    ['杠杆 1: AI RM', '部署美团"既白"/华住 AI/Lighthouse', 'RevPAR +5-10%'],
    ['杠杆 2: 餐饮外包', '团餐外包/预制菜/智能厨电', '餐饮毛利 +5-8pp'],
    ['杠杆 3: 私域运营', '微信小程序+会员体系+社群', 'OTA 佣金节省 10-15%'],
    ['杠杆 4: 能耗优化', '智能空调/热回收/LED', '能耗 -15-20%'],
    ['杠杆 5: 场景化产品', '影音房/电竞房/赛事房/亲子房', 'ADR +20-40%'],
]
S.append(make_table(levers, [3.5*cm, 7*cm, 5*cm], head_bg=C_JADE))
S.append(Spacer(1, 0.2*cm))

S.append(Paragraph('2.6 短/中/长期行动建议', sty_h2))
S.append(Paragraph('<b>短期（2026 H2 - 2027）</b>：Q3 必须部署 AI RM；餐饮外包试点；建立私域社群；旺季前能耗预算锁定', sty_b))
S.append(Paragraph('<b>中期（2027-2030）</b>：全面 AI 化运营；培育场景化产品；建立数据中台；探索机器人+人工协同', sty_b))
S.append(Paragraph('<b>长期（2028-2040）</b>：转型为"AI 驱动的生活方式运营专家"；跨业态运营', sty_b))

S.append(Paragraph('2.7 风险预警', sty_h2))
S.append(Paragraph('🔴 AI 工具选型错误（损失 6-12 个月学习曲线）  🟠 高基数效应持续  🟡 餐饮毛利持续走低', sty_b))
S.append(PageBreak())

# ========== 第三章 投资人 ==========
S.append(Paragraph('第三章  投资人视角（Investors）', sty_h1))

S.append(Paragraph('3.1 角色定义', sty_h2))
S.append(Paragraph('酒店业投资人 = 持有酒店物业或酒店相关金融资产的投资者（财务/战略/个人）', sty_b))

S.append(Paragraph('3.2 核心关注点', sty_h2))
S.append(Paragraph('1. 投资回报率  2. 退出路径  3. 风险/收益比  4. 资产配置  5. 现金流稳定性', sty_b))

S.append(Paragraph('3.3 H1 2026 现状 - 核心资产指标', sty_h2))
inv_assets = [
    ['资产类型', 'Cap Rate', '净现金流分派率', '流动性'],
    ['一线城市高奢酒店', '4.0-5.0%', '5-6%', '中'],
    ['一线城市中端酒店', '5.0-6.0%', '5-7%', '中'],
    ['二线城市中端酒店', '5.5-6.5%', '6-8%', '低-中'],
    ['三线城市经济型', '6.5-7.5%', '8-10%', '低'],
    ['酒店 REITs（国内）', '—', '5.05%（华安锦江标杆）', '高'],
    ['酒店 REITs（国际）', '—', '5.5-7%（雅诗阁）/7-8%（HPT）', '高'],
]
S.append(make_table(inv_assets, [4.5*cm, 3*cm, 4*cm, 4*cm], head_bg=C_INDIGO))
S.append(Spacer(1, 0.2*cm))

S.append(Paragraph('3.4 核心挑战', sty_h2))
S.append(Paragraph('🔴 <b>Cap Rate 持续走低 + 利率风险</b>：5.0-6.0% → 2027-2028 预计 4.5-5.5%；美联储 9 月加息 53.5%', sty_b))
S.append(Paragraph('🔴 <b>REITs 化时的资产质量挑战</b>：3 年稳定现金流 + 资产打包 + 资管能力', sty_b))
S.append(Paragraph('🟠 <b>跨境投资门槛</b>：日本 BOJ 加息 + 中东地缘风险 + 东南亚是主战场', sty_b))

S.append(Paragraph('3.5 5 类资产配置建议', sty_h2))
inv_config = [
    ['配置类型', '风险等级', '预期 ROE', '适合人群'],
    ['A: 一线城市核心物业', '中', '8-12%', '长期机构（险资/银行/社保）'],
    ['B: 酒店 REITs 池', '中低', '5-7%（分派率）', '稳健型（家族办公室/公募）'],
    ['C: 第三方资管服务', '低', '6-10%（管理费率 1-3%）', '轻资产玩家'],
    ['D: 海外酒店资产', '高', '12-20%', '高净值/专业 PE'],
    ['E: AHL 等协议平台股权', '高', '待估（潜在 50%+）', '高风险偏好的战略投资人'],
]
S.append(make_table(inv_config, [4*cm, 2*cm, 3*cm, 6.5*cm], head_bg=C_JADE))
S.append(Spacer(1, 0.2*cm))

S.append(Paragraph('3.6 短/中/长期行动建议', sty_h2))
S.append(Paragraph('<b>短期（2026 H2 - 2027）</b>：Q3 优先配置一线城市核心物业；关注华住/锦江/海珠公募 REIT 套利机会；海外资产日韩/东南亚', sty_b))
S.append(Paragraph('<b>中期（2027-2030）</b>：投资第三方酒店资管公司；跨境资产配置日韩 + 中东（沙特 2030 愿景）', sty_b))
S.append(Paragraph('<b>长期（2028-2040）</b>：酒店 REITs 化率对标成熟市场 25-30%；险资/银行/社保标配资产；中国投资人出海', sty_b))

S.append(Paragraph('3.7 风险预警', sty_h2))
S.append(Paragraph('🔴 地产周期持续  🔴 REITs 估值波动（加息环境）  🟠 地缘风险  🟡 跨境政策风险', sty_b))
S.append(PageBreak())

# ========== 第四章 业主 ==========
S.append(Paragraph('第四章  业主视角（Owners）', sty_h1))

S.append(Paragraph('4.1 角色定义', sty_h2))
S.append(Paragraph('酒店业主 = 拥有酒店物业产权的所有者（私人/中型/国企/地产开发商）', sty_b))

S.append(Paragraph('4.2 核心关注点', sty_h2))
S.append(Paragraph('1. 物业估值  2. 租金收益  3. REITs 化退出  4. 翻牌决策  5. 管理方博弈', sty_b))

S.append(Paragraph('4.3 H1 2026 现状', sty_h2))
S.append(Paragraph('<b>业主类型分布</b>：单体（25 万家）/ 中型（1 万家）/ 国企（50 家）/ 地产开发商（200 家）', sty_b))
S.append(Paragraph('<b>业主最大压力</b>：富力/万达/海航 系酒店 2026.04 拍卖 58 家；地产出清期持续到 2027-2028', sty_b))

S.append(Paragraph('4.4 核心挑战', sty_h2))
S.append(Paragraph('🔴 <b>翻牌决策的两难</b>：加入连锁（让渡权益）vs 维持独立（被挤压）vs 转售（估值低）', sty_b))
S.append(Paragraph('🔴 <b>REITs 化时点判断</b>：太早（估值低）vs 太晚（错过窗口）', sty_b))
S.append(Paragraph('🟠 <b>管理方博弈</b>：业主方（自主+收益）vs 管理方（标准+集团利益）vs 第三方资管', sty_b))

S.append(Paragraph('4.5 5 条路径', sty_h2))
owner_paths = [
    ['路径', '适合业主类型', '关键动作', '预期收益'],
    ['A: 翻牌加盟连锁', '单体/小型', '加入华住/锦江/首旅', 'OCC +10-15pp'],
    ['B: 精品化转型', '中高端物业', '主题酒店/民宿化', 'ADR +50-100%'],
    ['C: 打包 REITs 化', '中大型（5+ 家）', '申报 REIT 退出', '资产流动性溢价'],
    ['D: 卖给集团', '出清期业主', '卖给华住/锦江', '一次性退出'],
    ['E: 第三方资管托管', '不愿加盟', '委托 JLL/仲量联行', '专业管理 + 自主决策'],
]
S.append(make_table(owner_paths, [3.5*cm, 3*cm, 4*cm, 5*cm], head_bg=C_CRIMSON))
S.append(Spacer(1, 0.2*cm))

S.append(Paragraph('4.6 短/中/长期行动建议', sty_h2))
S.append(Paragraph('<b>短期（2026 H2 - 2027）</b>：Q3 决策窗口（翻牌/REITs/卖出三选一）；启动资产清单梳理；接触第三方资管', sty_b))
S.append(Paragraph('<b>中期（2027-2030）</b>：完成 REITs 化或翻牌决策；进入"专业资管+轻资产持有"模式', sty_b))
S.append(Paragraph('<b>长期（2028-2040）</b>：业主角色转向"长期资产持有者"；通过 REITs 实现流动性', sty_b))

S.append(Paragraph('4.7 Eric 特别提示（安逸集团 167 家酒店）', sty_h2))
S.append(Paragraph('⚠️ Eric 作为安逸集团产业发展部部长，处于"国企业主"角色', sty_b))
S.append(Paragraph('167 家酒店 = <b>潜在的 REITs 资产池</b>（¥80-150 亿市值）', sty_b))
S.append(Paragraph('<b>路径建议</b>：Q3 内部资产清单梳理 → Q4 接触 REITs 团队 → 2027-2028 是窗口期 → 第三方资管必需', sty_b))

S.append(Paragraph('4.8 风险预警', sty_h2))
S.append(Paragraph('🔴 翻牌决策错误  🔴 REITs 化失败  🟠 管理方控制过强  🟡 地产周期未结束', sty_b))
S.append(PageBreak())

# ========== 第五章 品牌方 ==========
S.append(Paragraph('第五章  品牌方视角（Brand Owners）', sty_h1))

S.append(Paragraph('5.1 角色定义', sty_h2))
S.append(Paragraph('酒店品牌方 = 拥有酒店品牌+商标+会员体系+中央预订系统的酒店集团', sty_b))

S.append(Paragraph('5.2 核心关注点', sty_h2))
S.append(Paragraph('1. 品牌力  2. 加盟模式  3. 会员体系  4. 中央预订贡献率  5. 品牌矩阵', sty_b))

S.append(Paragraph('5.3 H1 2026 现状 - 头部品牌矩阵', sty_h2))
brand_matrix = [
    ['集团', '主力品牌', '客房间数', '会员数', '中央预订贡献率'],
    ['华住', '汉庭/全季/桔子/禧玥/花间堂', '100+ 万', '2.3 亿', '~60%'],
    ['锦江', '锦江之星/维也纳/麗枫/喆啡/康铂', '110+ 万', '1.5 亿+', '~55%'],
    ['首旅', '如家/和颐/莫泰/首旅建国', '50+ 万', '1.5 亿+', '~50%'],
    ['亚朵', '亚朵/亚朵 S/亚朵 X', '6+ 万', '4,000 万+', '~70%'],
    ['万豪', '万豪/万怡/万枫/喜来登/瑞吉', '60+ 万（中国）', '2 亿+（全球）', '~40%'],
    ['洲际', '洲际/皇冠假日/假日/智选假日', '30+ 万（中国）', '1 亿+（全球）', '~40%'],
]
S.append(make_table(brand_matrix, [2*cm, 5.5*cm, 3*cm, 3*cm, 3*cm], head_bg=C_INDIGO))
S.append(Spacer(1, 0.2*cm))

S.append(Paragraph('5.4 核心挑战', sty_h2))
S.append(Paragraph('🔴 <b>OTA 反垄断 + AI Agent</b>：携程被反垄断立案 + 美团"既白"/微信 AI Agent 接入', sty_b))
S.append(Paragraph('🟠 <b>会员体系增长瓶颈</b>：4-5 亿活跃用户已接近天花板', sty_b))
S.append(Paragraph('🟡 <b>品牌矩阵同质化</b>：中端品牌竞争白热化', sty_b))

S.append(Paragraph('5.5 5 个战略方向', sty_h2))
brand_strats = [
    ['战略', '关键动作', '预期收益'],
    ['战略 1: 主题品牌矩阵', '推出银发康养/电竞/影音等主题品牌', '差异化溢价'],
    ['战略 2: AI Agent 协议', '接入 MCP/A2A/AHL 协议', '跨平台获客'],
    ['战略 3: 会员深度运营', '私域+短视频+直播', '复购率+10pp'],
    ['战略 4: 跨境扩张', '出海东南亚/中东/欧洲', '增量市场'],
    ['战略 5: REITs 化协同', '旗下资产打包 REIT', '资产估值修复'],
]
S.append(make_table(brand_strats, [3.5*cm, 7*cm, 5*cm], head_bg=C_JADE))
S.append(Spacer(1, 0.2*cm))

S.append(Paragraph('5.6 短/中/长期行动建议', sty_h2))
S.append(Paragraph('<b>短期（2026 H2 - 2027）</b>：推出主题品牌矩阵；接入 MCP/A2A 标准；中央预订+私域+短视频 三合一', sty_b))
S.append(Paragraph('<b>中期（2027-2030）</b>：主题品牌孵化（3-5 个）；跨境扩张（东南亚）；旗下资产打包 REITs 化', sty_b))
S.append(Paragraph('<b>长期（2028-2040）</b>：全球化品牌集团；AI Agent 协议层联盟；主题酒店第一品牌', sty_b))

S.append(Paragraph('5.7 风险预警', sty_h2))
S.append(Paragraph('🔴 OTA 反垄断反转  🟠 会员获取成本  🟡 主题品牌失败', sty_b))
S.append(PageBreak())

# ========== 第六章 单店 ==========
S.append(Paragraph('第六章  单店视角（Single Stores）', sty_h1))

S.append(Paragraph('6.1 角色定义', sty_h2))
S.append(Paragraph('酒店单店 = 独立运营的非连锁酒店物业（75% 的中国大陆酒店是单体）', sty_b))

S.append(Paragraph('6.2 核心关注点', sty_h2))
S.append(Paragraph('1. 生存能力  2. 翻牌决策  3. AI 工具使用  4. 客源结构  5. 退出路径', sty_b))

S.append(Paragraph('6.3 H1 2026 现状', sty_h2))
S.append(Paragraph('单体酒店总数：约 <b>25 万家</b>（占酒店总数 75%）', sty_b))
S.append(Paragraph('<b>核心痛点</b>：OTA 抽佣 12-18% + 推广费综合成本近 40%；AI RM 渗透率低；会员体系缺位；翻牌成本 ¥200-500 万', sty_b))

S.append(Paragraph('6.4 核心挑战', sty_h2))
S.append(Paragraph('🔴 <b>连锁挤压</b>：连锁化率 41.80% + TOP10 集中度 59.38% 持续上升', sty_b))
S.append(Paragraph('🔴 <b>AI 工具差距</b>：单店没有资源/能力/动机使用', sty_b))
S.append(Paragraph('🟠 <b>翻牌决策两难</b>：让渡 5-8% 管理费 + 部分决策权 + 装修投入 ¥200-500 万', sty_b))

S.append(Paragraph('6.5 5 条路径', sty_h2))
single_paths = [
    ['路径', '适合单店类型', '关键动作', '预期收益'],
    ['A: 翻牌加盟', '城市核心区中小物业', '加入华住/锦江/首旅', 'OCC +10-15pp'],
    ['B: 精品化转型', '区位独特+有调性', '主题酒店/民宿化', 'ADR +50-100%'],
    ['C: 卖给连锁', '不愿加盟的业主', '卖给华住/锦江/海珠', '一次性退出'],
    ['D: AHL 等协议平台', '中小单体 + 渴望独立', '接入 AHL 协议', 'AI RM + 私域'],
    ['E: 维持独立 + 数字化自救', '强品牌力/老客户', '私域+会员+小红书', '中度提升'],
]
S.append(make_table(single_paths, [3.5*cm, 3*cm, 4.5*cm, 4.5*cm], head_bg=C_JADE))
S.append(Spacer(1, 0.2*cm))

S.append(Paragraph('6.6 短/中/长期行动建议', sty_h2))
S.append(Paragraph('<b>短期（2026 H2 - 2027）</b>：Q3 决策窗口；数字化自救；接触连锁集团/第三方资管', sty_b))
S.append(Paragraph('<b>中期（2027-2030）</b>：完成路径选择；进入"专业玩家"角色；接入 AHL 等协议平台', sty_b))
S.append(Paragraph('<b>长期（2028-2040）</b>：单店角色减少；精品化是最后蓝海；资产通过 REITs/出售/家族办公室退出', sty_b))

S.append(Paragraph('6.7 风险预警', sty_h2))
S.append(Paragraph('🔴 不做决策就是最差决策  🔴 翻牌选错品牌  🟠 AI 工具差距持续扩大', sty_b))
S.append(PageBreak())

# ========== 第七章 集团 ==========
S.append(Paragraph('第七章  集团视角（Groups）', sty_h1))

S.append(Paragraph('7.1 角色定义', sty_h2))
S.append(Paragraph('酒店集团 = 拥有 5+ 家酒店的多品牌酒店组织（华住/锦江/万豪/华侨城等）', sty_b))

S.append(Paragraph('7.2 核心关注点', sty_h2))
S.append(Paragraph('1. 市占率  2. 收购整合  3. 翻牌扩张  4. REITs 化  5. AI 自研', sty_b))

S.append(Paragraph('7.3 H1 2026 现状 - 集团格局', sty_h2))
group_data = [
    ['集团', '客房数', '翻牌/年', 'AI 自研', 'REITs 化进度'],
    ['华住', '100+ 万', '500+', '易客房 4.0', '待申报'],
    ['锦江', '110+ 万', '400+', '锦江 AI', '待申报'],
    ['首旅', '50+ 万', '300+', '首旅如家 AI', '待申报'],
    ['亚朵', '6+ 万', '80+', '亚朵 S 智能', '待申报'],
    ['万豪', '60+ 万（中国）', '20+', 'Marriott AI', '国际 REITs'],
    ['华侨城', '30+ 万', '—', '—', '拟申报'],
]
S.append(make_table(group_data, [2.5*cm, 3*cm, 2.5*cm, 3.5*cm, 4*cm], head_bg=C_INDIGO))
S.append(Spacer(1, 0.2*cm))

S.append(Paragraph('7.4 核心挑战', sty_h2))
S.append(Paragraph('🔴 <b>翻牌规模 vs 品质</b>：翻牌加速可能导致服务品质下降', sty_b))
S.append(Paragraph('🟠 <b>AI 自研 vs 接入第三方</b>：自研投入大但控制力强；接入 MCP/A2A 标准成本低但依赖性强', sty_b))
S.append(Paragraph('🟡 <b>REITs 化时点</b>：太早影响集团报表，太晚错过窗口', sty_b))

S.append(Paragraph('7.5 5 个战略方向', sty_h2))
group_strats = [
    ['战略', '关键动作', '预期收益'],
    ['战略 1: 加速翻牌', '2026 H2 - 2027 翻牌 5,000+', '市占率 +5-10pp'],
    ['战略 2: 旗下资产 REITs 化', '申报 REIT，2027-2028 退出', '资产流动性溢价'],
    ['战略 3: AI 自研 + 协议接入', '自研核心 + MCP/A2A 标准', '成本 +20-30%'],
    ['战略 4: 主题品牌矩阵', '银发/电竞/影音/亲子', '差异化溢价'],
    ['战略 5: 跨境扩张', '出海东南亚/中东', '增量市场'],
]
S.append(make_table(group_strats, [3.5*cm, 7*cm, 5*cm], head_bg=C_CRIMSON))
S.append(Spacer(1, 0.2*cm))

S.append(Paragraph('7.6 短/中/长期行动建议', sty_h2))
S.append(Paragraph('<b>短期（2026 H2 - 2027）</b>：Q3 加速翻牌（500-1,000 家/季度）；启动 REITs 申报；AI 工具全栈部署', sty_b))
S.append(Paragraph('<b>中期（2027-2030）</b>：完成 REITs 化集中发行；主题品牌孵化（3-5 个）；跨境扩张启动', sty_b))
S.append(Paragraph('<b>长期（2028-2040）</b>：全球化酒店集团；AI Agent 协议层领导者；多元化（住宿+康养+零售+娱乐）', sty_b))

S.append(Paragraph('7.7 Eric 特别提示（安逸集团集团视角）', sty_h2))
S.append(Paragraph('⚠️ Eric 作为安逸集团产业发展部部长，处于"国企集团"角色', sty_b))
S.append(Paragraph('<b>路径建议</b>：167 家酒店 = 潜在的 REITs 资产池；第三方资管是必需；合作首选华住/锦江的轻资产管理输出模式；特色路径 与安逸集团"医养/康养"基因结合', sty_b))

S.append(Paragraph('7.8 风险预警', sty_h2))
S.append(Paragraph('🔴 翻牌过快导致品质稀释  🟠 REITs 化失败  🟡 AI 自研投入大', sty_b))
S.append(PageBreak())

# ========== 第八章 轻资产酒管 ==========
S.append(Paragraph('第八章  轻资产酒管公司视角', sty_h1))

S.append(Paragraph('8.1 角色定义', sty_h2))
S.append(Paragraph('轻资产酒管公司 = 以管理输出为主要模式的酒店运营专业服务公司（AHL/华住轻资产/万豪特许经营）', sty_b))

S.append(Paragraph('8.2 核心关注点', sty_h2))
S.append(Paragraph('1. 翻牌速度  2. 单店坪效  3. 加盟费率  4. 集团总部 vs 单店决策权  5. 跨境扩张', sty_b))

S.append(Paragraph('8.3 H1 2026 现状 - 核心玩家', sty_h2))
light_assets = [
    ['玩家', '模式', '单店数', '加盟费率', '重点赛道'],
    ['华住（轻资产）', '特许+管理', '60,000+', '5-7%', '国内中端'],
    ['锦江（轻资产）', '特许+管理', '70,000+', '5-7%', '国内中端+经济'],
    ['首旅（轻资产）', '特许+管理', '40,000+', '5-6%', '国内经济+中端'],
    ['万豪（特许）', '特许', '5,000+（中国）', '4-6%', '国内中高端'],
    ['雅高（特许）', '特许', '2,000+（中国）', '4-6%', '国内中端'],
    ['AHL（去中心化协议）', '协议赋能', '待启动', '服务费（待定）', '跨境/中小单体'],
]
S.append(make_table(light_assets, [3*cm, 2.5*cm, 3*cm, 3*cm, 4*cm], head_bg=C_INDIGO))
S.append(Spacer(1, 0.2*cm))

S.append(Paragraph('8.4 核心挑战', sty_h2))
S.append(Paragraph('🔴 <b>翻牌加速 vs 服务能力</b>：2026 H2 - 2027 翻牌井喷，但服务能力跟不上', sty_b))
S.append(Paragraph('🟠 <b>加盟费下行压力</b>：从 7-8% 降到 5-6%', sty_b))
S.append(Paragraph('🟡 <b>跨境扩张能力</b>：东南亚是主战场，人才/合规/支付是难题', sty_b))

S.append(Paragraph('8.5 5 个战略方向', sty_h2))
light_strats = [
    ['战略', '关键动作', '预期收益'],
    ['战略 1: AI 工具赋能', '部署 AI RM/AI 客服/AI 收益', '单店 OCC +5-8pp'],
    ['战略 2: 增值服务', 'AI 工具费+数据服务费+营销服务费', '单店收入 +30%'],
    ['战略 3: 会员体系打通', '与华住/锦江/万豪会员互通', '跨品牌获客'],
    ['战略 4: 跨境扩张', '出海东南亚/中东/欧洲', '增量市场'],
    ['战略 5: AHL 等协议', '接入 MCP/A2A 标准', '协议层联盟'],
]
S.append(make_table(light_strats, [3.5*cm, 7*cm, 5*cm], head_bg=C_JADE))
S.append(Spacer(1, 0.2*cm))

S.append(Paragraph('8.6 短/中/长期行动建议', sty_h2))
S.append(Paragraph('<b>短期（2026 H2 - 2027）</b>：Q3 是翻牌井喷窗口，加速签约；AI 工具全栈部署；与头部集团会员体系打通', sty_b))
S.append(Paragraph('<b>中期（2027-2030）</b>：完成 5,000+ 单店签约；增值服务收入占比 30%+；跨境扩张启动', sty_b))
S.append(Paragraph('<b>长期（2028-2040）</b>：全球化轻资产酒管集团；AI Agent 协议层标准制定者；收入结构 50%+30%+20%', sty_b))

S.append(Paragraph('8.7 Eric 特别提示（AHL 作为轻资产酒管）', sty_h2))
S.append(Paragraph('⚠️ AHL 是 Eric 的核心项目，正好属于"轻资产酒管公司"角色', sty_b))
S.append(Paragraph('<b>AHL 独特优势</b>：去中心化协议比传统轻资产更轻；Multi-Agent 架构是 AI 时代原生优势；跨境协议 MCP/A2A 标准对齐', sty_b))
S.append(Paragraph('<b>AHL 关键动作</b>：Q3-Q4 完成 MVP 测试 → 2027 正式上线（与服务 5-10 家中小酒管）→ 2028 接入 MCP/A2A → 2029-2030 跨境扩张', sty_b))

S.append(Paragraph('8.8 风险预警', sty_h2))
S.append(Paragraph('🔴 翻牌过快导致服务稀释  🟠 加盟费率下行  🟡 AI 工具替代', sty_b))
S.append(PageBreak())

# ========== 第九章 综合判断 ==========
S.append(Paragraph('第九章  八大角色综合判断（v6.0 核心）', sty_h1))

S.append(Paragraph('9.1 角色冲突矩阵', sty_h2))
S.append(Paragraph('见上文 2 表格：投资人 vs 业主 / 集团 vs 业主 / 品牌方 vs 单店 / 集团 vs 从业者 / 品牌方 vs OTA', sty_b))

S.append(Paragraph('9.2 AI 时代的赢家与输家（八大角色矩阵）', sty_h2))
S.append(Paragraph('见上文 3 表格：每个角色都有明确的赢家画像和输家画像', sty_b))

S.append(Paragraph('9.3 8 大角色的共同方向', sty_h2))
S.append(Paragraph('<b>方向 1：数据资产化</b>——每个角色都需要"数据→决策"闭环', sty_b))
S.append(Paragraph('<b>方向 2：轻资产化</b>——从"持有"转向"运营"', sty_b))
S.append(Paragraph('<b>方向 3：专业化分工</b>——每个角色做自己最擅长的部分', sty_b))

S.append(Paragraph('9.4 跨角色协同机会', sty_h2))
S.append(Paragraph('• <b>安逸集团 + 华住模式</b>：Eric 作为桥梁，国企+民企协同', sty_b))
S.append(Paragraph('• <b>AHL + 头部集团</b>：AHL 协议 + 华住/锦江品牌矩阵 = 下一代酒店生态', sty_b))
S.append(Paragraph('• <b>第三方资管 + 业主</b>：JLL/仲量联行 + 国企业主/地产出清', sty_b))
S.append(Paragraph('• <b>AI 工具 + 全部角色</b>：AI 是赋能所有角色的"基础工具"', sty_b))
S.append(PageBreak())

# ========== 第十章 Eric 个人 ==========
S.append(Paragraph('第十章  Eric 个人行动建议（v6.0 综合 4 重角色）', sty_h1))

S.append(Paragraph('10.1 角色定位与优先级', sty_h2))
eric_roles = [
    ['角色', '优先级', '短期重点', '中期重点', '长期重点'],
    ['AHL 创始人', '🔴 P0', 'MVP 测试', '协议标准对齐', '全球化扩张'],
    ['安逸集团部长', '🟠 P1', '资产清单梳理', 'REITs 化时点', '医养康养主题品牌'],
    ['酒店业老兵', '🟡 P2', '行业观察', '方法论输出', '行业话语权'],
    ['个人品牌', '🟢 P3', '内容输出', '行业报告', 'IP 化品牌'],
]
S.append(make_table(eric_roles, [3*cm, 2*cm, 3*cm, 3*cm, 4*cm], head_bg=C_CRIMSON))
S.append(Spacer(1, 0.2*cm))

S.append(Paragraph('10.2 Q3-Q4 关键动作清单', sty_h2))

S.append(Paragraph('AHL（最关键 P0）：', sty_b))
S.append(Paragraph('□ 跟进 Claude Opus 5 / DeepSeek V4 / Kimi K3 定价', sty_bl))
S.append(Paragraph('□ 完成 MVP 内测（乐山锦江嘉州宾馆基础上）', sty_bl))
S.append(Paragraph('□ 对接 MCP / A2A 标准', sty_bl))
S.append(Paragraph('□ Multi-Agent 架构对齐美团"既白"', sty_bl))
S.append(Paragraph('□ Q3 启动跨境数据通道（为 77 国免签红利）', sty_bl))

S.append(Paragraph('安逸集团 1244 战略（P1）：', sty_b))
S.append(Paragraph('□ Q3 完成 167 家酒店资产清单梳理', sty_bl))
S.append(Paragraph('□ Q3 接触中信/华泰/中金 REITs 团队', sty_bl))
S.append(Paragraph('□ Q4 启动第三方资管接触（JLL/仲量联行）', sty_bl))
S.append(Paragraph('□ 跟踪暑期酒店预订（贵阳/普洱/六盘水/呼和浩特）', sty_bl))

S.append(Paragraph('医养酒店（0 号实验室路径）：', sty_b))
S.append(Paragraph('□ 跟踪 800 元/月失能老人电子服务券落地', sty_bl))
S.append(Paragraph('□ 跟踪视网膜芯片中国市场引进时间线', sty_bl))
S.append(Paragraph('□ 探索"医养+酒店"的轻资产模式', sty_bl))
S.append(Paragraph('□ 与地方民政部门建立沟通渠道', sty_bl))

S.append(Paragraph('个人品牌（"ERIC的B166ER出品"）：', sty_b))
S.append(Paragraph('□ 县域文旅+大理民宿系列案例输出', sty_bl))
S.append(Paragraph('□ 中国大陆酒店 v4.0/v5.0/v6.0 综合报告输出', sty_bl))
S.append(Paragraph('□ 保持"行业研究+方法论可执行"的两大核心价值', sty_bl))
S.append(Paragraph('□ 探索个人 IP + AI Agent 的结合', sty_bl))

S.append(Paragraph('10.3 风险与机会（Eric 4 重角色）', sty_h2))
S.append(Paragraph('<b>风险</b>：', sty_b))
S.append(Paragraph('🔴 安逸集团国企干部身份约束（红黄绿清单必须遵守）', sty_b))
S.append(Paragraph('🔴 AHL 个人项目与国企身份的潜在冲突', sty_b))
S.append(Paragraph('🟠 行业波动风险（中美博弈/地缘风险/AI 替代）', sty_b))
S.append(Paragraph('🟡 个人精力分配（4 重角色如何平衡）', sty_b))

S.append(Paragraph('<b>机会</b>：', sty_b))
S.append(Paragraph('🟢 AHL 作为安逸集团内部试点（个人品牌+国企资源）', sty_b))
S.append(Paragraph('🟢 v4.0/v5.0/v6.0 报告系列成为行业话语权', sty_b))
S.append(Paragraph('🟢 AI Agent 时代红利（AHL 卡位 MCP/A2A 标准）', sty_b))
S.append(Paragraph('🟢 医养康养主题品牌（安逸集团基因 + AHL 协议）', sty_b))

S.append(Paragraph('10.4 长期愿景（v6.0 终极判断）', sty_h2))
S.append(Paragraph('Eric 作为"复合型玩家"，10 年后最可能成为的角色组合：', sty_b))
S.append(Paragraph('1. <b>AHL/MCP/A2A 协议层领导者</b>（个人核心）', sty_b))
S.append(Paragraph('2. <b>安逸集团旗下医养康养主题品牌创始人</b>（国企+个人）', sty_b))
S.append(Paragraph('3. <b>中国大陆酒店行业研究方法论第一人</b>（个人品牌）', sty_b))
S.append(Paragraph('4. <b>AI+康养+酒店+跨境 的复合型独立咨询人</b>（职业化）', sty_b))
S.append(Spacer(1, 0.2*cm))
S.append(Paragraph('这不是"打工者"路径，是"创办者+投资者+研究者"复合路径', sty_q))
S.append(PageBreak())

# ========== 附录 ==========
S.append(Paragraph('附录：v6.0 vs v4.0/v5.0 关系', sty_h1))
S.append(Paragraph('v4.0 (七维度横切)    : 行业总览 (WHAT)', sty_b))
S.append(Paragraph('v5.0 (三层纵深)      : 历史+现状+未来 (WHEN+WHERE+HOW)', sty_b))
S.append(Paragraph('v6.0 (八角色穿透)    : 角色化深度分析 (WHO)', sty_b))
S.append(Spacer(1, 0.2*cm))

S.append(Paragraph('完整逻辑链：', sty_b))
S.append(Paragraph('行业是什么 → 行业从哪里来/去哪里 → 对我意味着什么', sty_q))
S.append(Paragraph('v4.0 全景盘点 → v5.0 纵深穿透 → v6.0 角色化决策', sty_q))

S.append(Paragraph('v6.0 新增清单（vs v4.0/v5.0）', sty_h2))
appendix = [
    ['#', 'v4.0/v5.0 缺失', 'v6.0 新增'],
    ['1', '无角色化分析', '8 大角色完整覆盖'],
    ['2', '无角色冲突矩阵', '第九章 9.1 角色冲突矩阵'],
    ['3', '无 AI 赢家输家画像', '第九章 9.2 AI 时代赢家/输家'],
    ['4', '无跨角色协同', '第九章 9.4 跨角色协同机会'],
    ['5', '无角色行动建议', '第一~八章 每章 行动建议'],
    ['6', '无 Eric 4 重角色定位', '第十章 综合判断'],
    ['7', '无 Q3-Q4 关键动作清单', '第十章 10.2 动作清单'],
]
S.append(make_table(appendix, [1*cm, 5*cm, 10.5*cm], head_bg=C_JADE))
S.append(Spacer(1, 0.3*cm))

S.append(Paragraph('附录：v6.0 数据可信度声明', sty_h1))
credibility = [
    ['数据类型', '来源', '可信度'],
    ['8 大角色核心 KPI', 'v4.0 多源综合', '🟢 高'],
    ['头部集团数据', '上市公司公告', '🟢 高'],
    ['AI RM 渗透率', '行业报告 + 公司披露', '🟡 中'],
    ['单体酒店总数', '行业协会 + OTA 平台', '🟢 高'],
    ['角色冲突判断', 'v6.0 综合分析', '🟡 中'],
    ['角色行动建议', 'v6.0 推断', '🟠 行业判断'],
    ['短期/中期预测', 'v6.0 推演', '🟡 中'],
    ['Eric 长期愿景', 'v6.0 综合', '🟠 需用户验证'],
]
S.append(make_table(credibility, [6*cm, 6*cm, 4.5*cm], head_bg=C_INDIGO))
S.append(Spacer(1, 0.4*cm))

S.append(Paragraph('编制信息', sty_h2))
info = [
    ['版本', 'v6.0 八大角色多视角专题'],
    ['编制', 'B166ER'],
    ['编制时间', '2026-07-27 08:03 GMT+8'],
    ['依据', 'v4.0 七维度 + v5.0 三层纵深 + Eric 7/27 多视角指令'],
    ['AI 模型', 'DeepSeek-V4-Flash + Claude Sonnet'],
    ['PDF 生成', 'reportlab + Noto Sans SC'],
    ['风险偏好', '稳（默认）'],
    ['下一步', 'Q3 跟进 Claude Opus 5 / DeepSeek V4 / Kimi K3 实际定价；Q4 完成 v4.0+v5.0+v6.0 三报告系列综合发布'],
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
size = os.path.getsize('D:/B166ER-OpenClaw/workspace/reports/2026H1中国酒店业八大角色多视角分析专题-v6.0.pdf')
print('[OK] v6.0 PDF generated')
print('  Path: D:/B166ER-OpenClaw/workspace/reports/2026H1中国酒店业八大角色多视角分析专题-v6.0.pdf')
print(f'  Size: {size/1024:.1f} KB ({size:,} bytes)')