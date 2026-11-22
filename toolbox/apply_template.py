"""
应用模板字体样式到 v5.5 文件上：
- 模板字体：方正小标宋简体（标题 22pt）+ 仿宋_GB2312（正文 18pt）
- 目标文件：邹士勇发言稿_2026高参圆桌国资酒店_2026-08-29_v5.5_基于十五五规划复盘版.docx
- 内容：Eric 调整后的 v5.5 完整内容
"""
import shutil
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os

# ============= 1. 复制模板到目标路径（保留模板的 styles.xml）============
TEMPLATE = r'C:\Users\ericz\Desktop\邹士勇总发言稿（2026酒店品牌展暨酒店投资峰会）.docx'
TARGET = r'C:\Users\ericz\Desktop\邹士勇发言稿_2026高参圆桌国资酒店_2026-08-29_v5.5_基于十五五规划复盘版.docx'

# 用模板复制为目标文件（这样 styles.xml 是模板的）
shutil.copyfile(TEMPLATE, TARGET)
print(f'已复制模板到目标文件：{TARGET}')

# ============= 2. 打开复制的文档（带模板样式）============
doc = Document(TARGET)

# ============= 3. 清空所有现有段落 =============
# 删除所有 paragraphs（但保留 styles）
# python-docx 没有直接的"清空段落"方法，需要遍历删除
body = doc.element.body
# 保存所有 sectPr（节属性）
sectPr_elements = body.findall('.//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}sectPr')
# 删除所有子元素（除了 sectPr）
for child in list(body):
    if child.tag.endswith('}sectPr'):
        continue
    body.remove(child)
# 重新插入 sectPr
for sectPr in sectPr_elements:
    body.append(sectPr)

print('已清空文档内容（保留样式）')

# ============= 4. 工具函数：设置中文 + ASCII 字体 =============
def set_run_font(run, font_name_eastasia, font_name_ascii='Times New Roman', size_pt=18, bold=False):
    """设置 run 的字体（同时设置 eastAsia 和 ascii）"""
    run.font.name = font_name_ascii
    run.font.size = Pt(size_pt)
    run.font.bold = bold
    # 设置 eastAsia 字体（中文）
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rFonts')
    if rfonts is None:
        from docx.oxml import OxmlElement
        rfonts = OxmlElement('w:rFonts')
        rpr.append(rfonts)
    rfonts.set('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}eastAsia', font_name_eastasia)
    rfonts.set('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}ascii', font_name_ascii)
    rfonts.set('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}hAnsi', font_name_ascii)

# ============= 5. 工具函数：添加段落 =============
def add_para(text, font_eastasia='仿宋_GB2312', size_pt=18, bold=False, center=False, indent=False):
    """添加段落（使用模板字体）"""
    p = doc.add_paragraph()
    if text:
        run = p.add_run(text)
        set_run_font(run, font_eastasia, size_pt=size_pt, bold=bold)
    if center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if indent:
        p.paragraph_format.first_line_indent = Cm(0.74)
    return p

def add_blank():
    """添加空行"""
    doc.add_paragraph()

# ============= 6. 重建 Eric 调整后的 v5.5 完整内容 =============

# === 封面（标题用方正小标宋简体 22pt 加粗）===
add_para('邹士勇总发言稿', font_eastasia='方正小标宋简体', size_pt=22, bold=True, center=True)
add_para('（2026 酒店品牌展暨酒店投资峰会）', font_eastasia='方正小标宋简体', size_pt=22, bold=True, center=True)
add_blank()
add_para('会议：2026 酒店品牌展暨酒店投资峰会', center=True)
add_para('环节：高参圆桌——国资酒店的资产盘活与资本破局之道', center=True)
add_para('时间：2026 年 9 月 1 日（周二）上午 11:20-12:10', center=True)
add_para('地点：上海金茂君悦大酒店', center=True)
add_para('发言时长：15 分钟', center=True)
add_blank()

# === 自我介绍（一级标题，方正小标宋简体 18-20pt 加粗）===
def add_h1(text):
    """一级标题"""
    p = doc.add_paragraph()
    run = p.add_run(text)
    set_run_font(run, '方正小标宋简体', size_pt=18, bold=True)

add_h1('自我介绍')
add_para('各位嘉宾、各位同仁：')
add_para('大家好，我是邹士勇，来自安逸酒店集团。')
add_para('我们集团是四川省的一家省属国资酒店集团，于 2021 年 12 月揭牌成立。集团现有自营酒店 17 家、受托管理酒店 39 家，合计管理 56 家酒店、78,752 间管理房间。覆盖宜宾、乐山、都江堰等省内 17 个地市州。我们集团曾上榜"中国饭店集团 60 强"，并荣登"中国旅游饭店业协会 2023 年全服务饭店"第 7 位。今天讨论的主题是"国资酒店的资产盘活与资本破局之道"，我围绕主持人提出的五个命题，结合集团"十五五"高质量发展规划，从安逸现状出发，逐一分享我们的观察与思考。')
add_blank()

# === 第一部分：安逸现状全面复盘 ===
add_h1('第一部分：安逸现状全面复盘')
add_para('在进入五个话题之前，我先快速复盘一下安逸的现状——这既是问题起点，也是所有思考的底座。')
add_para('从规模看：集团目前管理 56 家酒店、78,752 间客房。但  自我诊断揭示了三个根本性矛盾：第一，资产与战略要求不匹配——资产总额仅 35.51 亿元，2025 年酒店板块利润 -6,843 万元，亏损面接近 50%；第二，产品与资产价值不匹配——硬件老化、文化缺失，RevPAR 与同地段竞品差距 30% 以上，400 余个注册商标"有注册无应用"；第三，机制与市场竞争不匹配——薪酬与市场脱节、决策链条长、会员运营未精准分层。')
add_para('从财务看：2025 年集团营收 15.65 亿元（含旅行社），其中酒店板块 5.63 亿元、同比 +4.5%；资产负债率 56.76%、同比优化 17 个百分点。2026 H1 营收 1.49 亿元、利润 -3,675 万元，但同比减亏 24.29%——减亏是真实的，但"未扭亏"也是真实的。')
add_para('从对标看：我们重点学习了两个案例。一个是浙江雷迪森——省属国资轻重分离标杆，2020 年启动全域整合，2023 年完成重资产与轻资产平台物理拆分，3 年管理门店突破 230 家。另一个是君亭酒店——中高端文化主题酒店差异化标杆，聚焦"住宿+文化艺术+服务" BAS 体系、高溢价、高辨识度品牌。这两个案例给我们的启示：国资改革必须"重资产做优、轻资产做强"+ 文化赋能是商业模式核心。', bold=True)
add_para('基于以上复盘，集团"十五五"规划明确了"1244 战略"——一条高质量发展主线（聚焦中高端）、两大品牌价值内核（巴蜀生活美学 + 安逸生活方式）、三大核心赛道（城市商务 + 文化主题 + 文旅度假）、四步实施路径（轻重分离 → 打造标杆 → 品牌运营 → 标准输出）。2030 年目标是轻资产管理酒店 200 家、管理客房 30,000 间、利润总额 >5,000 万、亏损面 <10%。')
add_para('这是我们发言的底色。接下来 5 个话题，都从这个现状出发。')
add_blank()

# === 第二部分：五个话题 ===
add_h1('第二部分：五个话题——基于现状的思考与回复')

def add_h2(text):
    """二级标题（话题标题）"""
    p = doc.add_paragraph()
    run = p.add_run(text)
    set_run_font(run, '黑体', size_pt=16, bold=True)

# 话题 1
add_h2('一、关于"进退之间"——国资酒店的角色定位')
add_para('核心判断："进"不是争一时之地利，而是筑产业之生态；"退"不是消极收缩，而是盘活低效资产、释放沉淀资本。')
add_para('现状与思考：安逸 56 家酒店中，自营仅 17 家、占比 30%，其余 39 家是受托管理。集团下面 4 家代表性子公司——新良（轻重分离）、安逸茶山（提质增效）、古尔沟（资不抵债 181.74% 处置出清）、安逸连锁（2026-6-30 前全部闭店）——没有任何两家是同一种命运。715 自我诊断的"资产与战略要求不匹配"，具体就体现在这里。')
add_para('我们的措施："十五五"规划"1244 战略"的第一步就是"轻重分离"——重资产管理平台 + 轻资产运营平台拆分，人/财/业务权责独立、市场化激励配套。我们的路径是：1+5 业务架构（1 个集团 + 5 大事业部），重资产管物业保增值、轻资产做品牌拓托管。同时与省旅投、巴蜀文化旅游走廊产业联盟协作，把安逸放进更大范围的巴蜀文旅生态。')
add_para('困惑：差异化策略说起来对，但怎么防止"好公司被差公司拖累"？国资委对国资保值增值的要求，与"允许部分子公司出清"的容忍度边界在哪？')
add_blank()

# 话题 2
add_h2('二、关于"REITs 周期"——阶段研判与应对')
add_para('核心判断：酒店 REITs 窗口已全面打开，行业整体处于"试点期"，距离"成熟期"还有较长时间。')
add_para('现状与思考：2025 年集团资负率 56.76%，同比优化 17 个百分点，但经营现金流仍为 -1,137 万元。资产沉淀严重——2025 年全国 764 个酒店拍卖项目、752 亿拍卖金额就是代价。好消息是：2025 年 12 月国家发改委首次将酒店纳入公募 REITs；2025 年 7 月华安锦江商业 REIT 6/23 过审——国内首单纯酒店公募 REIT，底层资产 18 城 21 家"锦江都城"酒店，为我们打了样。')
add_para('我们的措施：集团"十五五"规划对应"1244 战略"第四步"标准输出"——通过投融建管退资本闭环实现资产证券化。我们正在做 6 大酒店改造——4.08 亿投资，预计净利润 1,675 万，IRR 6.6%-24.6%——这是为 REITs 发行做的"资产储备"。同时与锦江合资成立轻资产管理公司（51:49），把"管理能力"证券化。集团 2030 年目标：轻资产管理酒店 200 家、管理客房 30,000 间。')
add_para('困惑：酒店 REITs 的"流动性溢价"到底能不能兑现？酒店 REITs 与写字楼、商业 REITs 的估值逻辑差异在哪？这是国资酒店行业没人回答的问题。')
add_blank()

# 话题 3
add_h2('三、关于"接手之后"——国资酒店的改革实践')
add_para('核心判断：国资酒店普遍面临三个根本性变化——产权关系之变、业务结构之变、资产形态之变。核心是从"行政化"走向"市场化"。')
add_para('现状与思考：2026 H1 营收 1.49 亿、利润 -3,675 万、同比减亏 24.29%——这是"止血期"的真实数据。715 诊断的"产品与资产价值不匹配"+"机制与市场竞争不匹配"两大矛盾，在接手之后体现为：硬件老化导致 RevPAR 落后 30%+；薪酬与市场脱节导致人才流失；决策链条长导致市场反应慢。')
add_para('我们的措施："十五五"规划对应"1244 战略"的第二、三步（打造标杆 + 品牌运营）——通过 6 大旗舰标杆酒店改造，沉淀"安逸"产品标准与运营体系，再通过各赛道品牌独立专业化运营实现品牌矩阵成型。三大改革动作：子公司专业化整合（差异化策略）、品牌矩阵化构建（多品牌覆盖）、数字化转型（集团级中台 + AI 能力沉淀）。集团"十五五"明确三大护城河：数字化护城河、在地文化护城河、自营能力护城河。')
add_para('困惑：怎么防止"减亏"变成"美化报表"？国资委对国资保值增值的要求，与"短期减亏但长期需要持续投入"之间怎么平衡？')
add_blank()

# 话题 4
add_h2('四、关于"区域整合 vs 各自为战"——规模化路径选择')
add_para('核心判断：区域整合有三种典型路径——行政整合（强势集团吞并区域品牌，速度快但文化冲突大）、品牌输出（标准化范式复制扩张，质量可控、品牌一致性高）、资本纽带（REITs+战略投资驱动整合，扩张效率最强，是未来主方向）。')
add_para('现状与思考：集团 2026 目标规模 103 家、2030 目标 200 家轻资产——自营 17 + 受托管理 39 还远不够。区域整合是必由之路。715 诊断的"机制与市场竞争不匹配"决定了：行政整合管得了资产管不了人心——酒店是"人"的服务行业，文化冲突代价大。')
add_para('我们的措施："十五五"规划"1244 战略"第三、四步——文化主题赛道（四川宾馆/花园宾馆/新良酒店/深圳川宾）+ 7 大子品牌（安逸·熊猫、禅茶、锦秀、山屿，星火、非遗、农庄）。今年与锦江合资（51:49、注册资本 1000 万）专做"安逸+锦江"双品牌输出，与省旅投、巴蜀走廊联盟协作，通过央国企差旅对接（平安/铁旅/心已远/重庆文旅）拓展客源基础。')
add_para('困惑：合资公司的治理结构、利益分配、文化磨合比纯自营复杂得多——"先结婚后恋爱"的痛点怎么解决？')
add_blank()

# 话题 5
add_h2('五、关于"从持有到流动"——价值重塑逻辑')
add_para('核心判断：酒店资产价值被重新定义为"四维定价"——资产价值、品牌价值、运营价值、资本价值。四个维度相互增强，形成闭环。')
add_para('现状与思考：2025 年资负率 72.10% → 2026 H1 56.76%，优化 17 个百分点但仍偏高。2025 经营现金流 -1,137 万元。过去"买地→建楼→开 20 年→卖"的逻辑让酒店沉淀资本、无法标准化——这正是"从持有到流动"必须解决的问题。')
add_para('我们的措施："十五五"规划明确——三重价值释放逻辑 = 核心地段资产重估 × 巴蜀文化品牌溢价 × 轻重分离模式升级。对应"1244 战略"中"2"（巴蜀生活美学 + 安逸生活方式）。具体动作：6 大酒店改造（4.08 亿投资）+ 安逸茶山与帆书"书山茶海"文化品牌发布会 + 央国企差旅对接。这 1675 万净利是报表能看到的，"品牌增值"是 3-5 年后会显现的真正价值。')
add_para('困惑：但"品牌 IP 化"很难量化——你跟国资委说"我们做了个茶文化发布会"，他问"这给净资产带来多少增值"，你答不上来。"长期价值"和"短期可量化"在国资体系里怎么平衡？')
add_blank()

# === 第三部分：结语 ===
add_h1('第三部分：结语')
add_para('各位嘉宾、各位同仁：')
add_para('讲到这里，回到集团"十五五"规划的 2030 目标——轻资产管理酒店 200 家、管理客房 30,000 间、利润总额 >5,000 万、亏损面 <10%。从 2026 现状到 2030 目标的距离，正是我们"十五五"需要穿越的四年。')
add_para('国资酒店要承担起三个时代责任：')
add_para('一是产业责任——成为行业基础设施的共建者，推动区域产业协同。')
add_para('二是资本责任——用耐心资本支持行业长期发展，避免短期套利。')
add_para('三是文化责任——把每个城市的在地文化传承下去。')
add_para('最后，用一句话与各位共勉：国资酒店，既要低头做事，也要抬头看路。低头做事，把每个酒店运营好；抬头看路，看清行业趋势，把握资本机遇。')
add_para('谢谢大家！欢迎各位到西部做客！')

# ============= 7. 保存 =============
doc.save(TARGET)
print(f'已保存：{TARGET}')
print(f'文件大小：{os.path.getsize(TARGET) / 1024:.1f} KB')

# 验证字体设置
print()
print('=== 验证字体设置 ===')
verify = Document(TARGET)
for i, p in enumerate(verify.paragraphs[:5]):
    if p.text.strip():
        for run in p.runs[:1]:
            rpr = run._element.rPr
            if rpr is not None:
                rfonts = rpr.find('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rFonts')
                if rfonts is not None:
                    print(f'P{i}: eastAsia={rfonts.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}eastAsia")}, ascii={rfonts.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}ascii")}, size={run.font.size}')
