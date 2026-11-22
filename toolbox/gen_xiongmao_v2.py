# -*- coding: utf-8 -*-
"""关于与成都大熊猫基地合作项目的报送建议 · 公文 Word（v2 集团全方位视角）"""
import os
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = r"C:\Users\ericz\Desktop\关于与成都大熊猫基地合作项目的报送建议_集团视角_2026-11-18.docx"

doc = Document()
st = doc.styles['Normal']
st.font.name = '仿宋_GB2312'
st.font.size = Pt(16)
st.element.rPr.rFonts.set(qn('w:eastAsia'), '仿宋_GB2312')
st.paragraph_format.space_after = Pt(0)
st.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
st.paragraph_format.line_spacing = Pt(30)
for sec in doc.sections:
    sec.top_margin = Cm(3.7); sec.bottom_margin = Cm(3.5)
    sec.left_margin = Cm(2.8); sec.right_margin = Cm(2.6)


def F(run, name='仿宋_GB2312', size=16, bold=False):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    run._element.rPr.rFonts.set(qn('w:eastAsia'), name)


def p(t, font='仿宋_GB2312', size=16, bold=False, indent=2, align=None,
      before=0, after=0, spacing=30):
    par = doc.add_paragraph()
    par.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    par.paragraph_format.line_spacing = Pt(spacing)
    par.paragraph_format.space_before = Pt(before)
    par.paragraph_format.space_after = Pt(after)
    if align is not None:
        par.alignment = align
    if indent:
        par.paragraph_format.first_line_indent = Pt(size * indent)
    F(par.add_run(t), font, size, bold)
    return par


def h1(t):
    p(t, font='黑体', size=16, before=10, after=2)


def h2(t):
    p(t, font='楷体_GB2312', size=16, bold=True, before=6, after=2)


def item(t):
    par = doc.add_paragraph()
    par.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    par.paragraph_format.line_spacing = Pt(30)
    par.paragraph_format.first_line_indent = Pt(32)
    F(par.add_run(t), '仿宋_GB2312', 16, False)
    return par


def item3(head, sub, body):
    """条目：黑体标题 + 楷体小标题 + 仿宋正文"""
    par = doc.add_paragraph()
    par.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    par.paragraph_format.line_spacing = Pt(30)
    par.paragraph_format.first_line_indent = Pt(32)
    F(par.add_run(head), '黑体', 16, False)
    q = doc.add_paragraph()
    q.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    q.paragraph_format.line_spacing = Pt(30)
    q.paragraph_format.left_indent = Pt(32)
    q.paragraph_format.first_line_indent = Pt(0)
    F(q.add_run(sub), '楷体_GB2312', 16, True)
    F(q.add_run(body), '仿宋_GB2312', 16, False)


def shade(cell, hexc):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement('w:shd'); sh.set(qn('w:val'), 'clear'); sh.set(qn('w:fill'), hexc)
    tcPr.append(sh)


def tbl(headers, rows, widths=None, fs=10.5):
    t = doc.add_table(rows=1, cols=len(headers)); t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hc = t.rows[0].cells
    for i, h in enumerate(headers):
        hc[i].text = ''
        pp = hc[i].paragraphs[0]; pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pp.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        pp.paragraph_format.line_spacing = Pt(18)
        F(pp.add_run(h), '黑体', fs, False); shade(hc[i], 'D9D9D9')
    for ri, row in enumerate(rows):
        cs = t.add_row().cells
        for ci, v in enumerate(row):
            cs[ci].text = ''
            pp = cs[ci].paragraphs[0]
            pp.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
            pp.paragraph_format.line_spacing = Pt(18)
            F(pp.add_run(str(v)), '仿宋_GB2312', fs, False)
    if widths:
        for r in t.rows:
            for i, w in enumerate(widths):
                r.cells[i].width = Cm(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    return t


# ==================== 文头 ====================
p('四川省旅游投资集团有限责任公司', font='仿宋_GB2312', size=15, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
p('关于与成都大熊猫繁育研究基地合作项目的报送建议', font='方正小标宋简体', size=20,
  align=WD_ALIGN_PARAGRAPH.CENTER, spacing=34, after=4)
p('报送对象：集团产业发展部（陈天科部长、蔡思捷）　　编制：安逸酒店集团产业发展部　　2026 年 11 月 18 日',
  font='仿宋_GB2312', size=12, align=WD_ALIGN_PARAGRAPH.CENTER, after=14)

# ==================== 一 ====================
h1('一、合作对象基本情况与合作前提')
item('成都大熊猫繁育研究基地（熊猫基地）位于成都市成华区熊猫大道 1375 号，距市中心天府广场约 10 公里，'
     '距双流机场约 30 公里，核心区总面积 3570 亩，2006 年评为国家 AAAA 级旅游景区；'
     '系副局级公益二类事业单位，内设党群综合部、动物保护研究部、动物饲养管理部、动物疫病防控部、'
     '文旅发展部、都江堰野放繁育研究中心六个机构；截至 2024 年末圈养大熊猫 260 只，为全球最大圈养繁殖种群；'
     '2000 年设科普教育专职部门，2021 年建成全球首家大熊猫主题互动体验专题博物馆，'
     '近十年开展各类科普教育活动 3600 余场次，获评全国科普教育基地、全国青少年科技教育基地、'
     '国家青少年自然教育绿色营地等资质。')
item('需特别区分三个熊猫主题园区的隶属关系，避免口径混淆：'
     '熊猫基地（成华区）内设文旅发展部；都江堰野放繁育研究中心（熊猫谷）为熊猫基地内设部门，'
     '占地 2004 亩，坐落都江堰市玉堂镇，毗邻都江堰千年水利工程与青城山，'
     '距都江堰市区约 3 公里、距成都约 50 公里，2015 年 4 月开放，主营野化训练放归、自然教育与生态旅游；'
     '都江堰中华大熊猫苑（原熊猫乐园）属中国大熊猫保护研究中心，与熊猫基地非同一机构，本次不宜混用。')
item('基于上述，本次合作报请按集团全方位口径组织，覆盖酒店、景区、文旅服务、物业、党建培训、康养六大板块，'
     '并由产业发展部牵引轻资产与新零售、数字化、专列等增量合作事项。'
     '对接窗口建议明确为基地内设的文旅发展部。')

# ==================== 二 ====================
h1('二、集团各板块可对接的合作事项')

h2('（一）酒店板块')
item3('1. 基地及研学团队的城市接待住宿',
      '锦江宾馆、金牛宾馆、四川宾馆、花园宾馆等市区核心酒店距天府广场均在 10 公里圈内，'
      '距双流机场约 30 公里。',
      '建议为基地接待团队、科普研学团队、志愿者与后勤团队建立协议价与 VIP 接待标准，'
      '并承接基地科普教育、志愿者培训的会务与住宿。需基地明确：年度接待团队规模、'
      '入住标准与结算方式、是否纳入单位差旅采购目录。')
item3('2. 熊猫谷—青城山—都江堰联线产品（国堰宾馆）',
      '国堰宾馆与熊猫谷同处都江堰，距熊猫谷约 3 公里，'
      '其改造项目已明确定位政务文化交流基地、本土康养产业基地、熊猫文化研学基地三大文化定位，'
      '空间规划含熊猫亲子文创、九重文化空间，非房收入占比目标由 25% 提升至 65%。',
      '建议以基地科普教育为前段、国堰为承接，'
      '推出熊猫谷—青城山—灌县古城两日一夜联线，住宿由国堰承接、餐饮与非房由国堰运营。'
      '需基地明确：联线线路与时间窗、联合售票与分账机制、研学课程内容与师资对接。')
item3('3. 熊猫主题的产品标准与轻资产输出',
      '安逸 6 大品牌体系含安逸·熊猫；集团先锋国潮新潮赛道的大熊猫国潮 IP 对应酒店为新良酒店。',
      '建议以熊猫基地的科普教育内容为内核，把熊猫主题做成可授权、可托管、可复制的产品包，'
      '为集团轻资产拓展提供主题化样本，避免仅以门店命名承载熊猫。'
      '需基地明确：熊猫主题形象与名称在商业场景的使用边界。')

h2('（二）景区板块')
item3('4. 熊猫谷生态旅游与集团景区的联线互导',
      '熊猫谷为基地内设部门，主营野化放归、自然教育与生态旅游；'
      '集团在都江堰另有国堰宾馆、天府山庄、三岔湖天府山庄等资产。',
      '建议形成以熊猫谷为熊猫主题入口、集团都江堰资产为承接的熊猫经济带，'
      '统一线路、导流与分账。需明确：双方线路的排他条款与运营主体分工。')
item3('5. 科普研学线路与集团景区的联合课程',
      '基地近十年开展科普教育活动 3600 余场次，具备全国科普教育基地、'
      '国家青少年自然教育绿色营地等资质。',
      '建议由基地出科普课程与师资，集团出场景与运营，联合开发研学线路产品。'
      '需明确：课程知识产权归属、师资派遣与安全责任、联合产品的定价与分成。')

h2('（三）文旅服务板块')
item3('6. 熊猫专列·锦绣天府号与基地的客流组织',
      '熊猫专列（安逸号／锦绣天府号）由心已远国际旅行社操盘运营，'
      '采用铁路方出车、旅投购买运营权、运营方全流程操盘模式，锦绣天府号 8 万／10 万两档，以入境客为主；'
      '当前 Q2 款项已按期到账，三方协议 11 月 15 日签署、运营方 11 月 30 日确定。',
      '建议将基地作为专列线路与班期上的重点目的地产品，'
      '打通“行＋住＋购”闭环，并借专列入境客为基地与川内景区导流。'
      '需明确：基地与专列的线路衔接、联合售票与分账、班期与客流承诺。')

h2('（四）物业板块')
item3('7. 基地及熊猫谷的物业与设施运维',
      '集团物业板块（锦宾物业、玉沙物业、总府物业）具备酒店业态的设施运维、'
      '能耗管控与服务标准体系。',
      '建议以酒店物业经验外溢，承接基地及熊猫谷的公共区域、场馆、商业街区与园区的设施运维、'
      '能耗管理与服务标准化输出。需明确：服务边界、资质与准入要求、结算方式。')

h2('（五）党建培训板块')
item3('8. 党建共建与干部培训',
      '基地设党群综合部，具备“学习强国”科普基地等资质；'
      '集团有党校与旅投英才等培训资源。',
      '建议在基地科普教育与党建培训之间建立联合课程与现场教学点，'
      '把基地的科普课程纳入集团干部培训与青少年自然教育体系。'
      '需明确：联合办学的组织形式、课程标准与师资互派。')

h2('（六）康养板块')
item3('9. 自然教育与生态康养产品',
      '熊猫谷主打自然教育与生态旅游；集团康养板块有古尔沟温泉、三岔湖等载体。',
      '建议以熊猫谷的自然教育客群为前端，与集团康养载体组合成中长期度假产品。'
      '需明确：产品边界与分账、客源互导机制。')

h2('（七）产业发展部牵引的增量合作')
item3('10. 安逸新零售与熊猫主题商品开发',
      '安逸新零售（安逸甄选／安逸集市）具备私域商城、线上外贸体系与外部运营商；'
      '基地 2021 年建成全球首家大熊猫主题互动体验专题博物馆，文创开发与销售场景现成。',
      '建议由茶业公司与甄选平台承接熊猫主题文创与伴手礼开发，'
      '形成“基地场景内开发—线上商城与专列渠道销售”的闭环，并延伸至外贸出口。'
      '需明确：文创 IP 开发授权、商品品控与召回、渠道费用与分成。')
item3('11. 品牌与新媒体传播',
      '集团新媒体矩阵含抖音 35 个、小红书 35 个账号；'
      '熊猫专列 4 班期现成熊猫 IP 素材（雪山＋列车＋熊猫）可复用。',
      '建议做“熊猫基地—熊猫专列—安逸酒店”的城市级内容 campaign，'
      '小红书侧主打亲子出行攻略，抖音侧主打专列加住宿线路内容。'
      '需明确：官方账号联合发布、素材与拍摄准入、舆情口径。')
item3('12. 数字化与网络信息安全',
      '集团具备岭博网关与公安网监审计一体化能力、AI 风险预警与 AI 与数据中台建设能力。',
      '建议以“安全管理＋网安保险＋风险防控服务”模式，为基地及合作单位提供公共上网、'
      '安全生产、食品安全与极端天气的风险减损服务，落地载体为集团智能弱电与 AI 预警。'
      '需明确：是否有对应采购或合作需求，可由集团与保险方共同提案。')

# ==================== 三 ====================
h1('三、需请集团与基地明确的事项')
item('一、对接口径与主体。基地为副局级公益二类事业单位，熊猫谷为其内设部门，'
     '建议明确由基地文旅发展部作为统一窗口，并区分公益合作与市场化经营两条路径。')
item('二、IP 授权边界。熊猫形象、名称及文创开发的商业化授权权属上级保护主管部门与基地，'
     '建议由集团层面统一提出，集团侧先不自行商用。')
item('三、场景分工。城北基地承担科普教育、研学与城市接待，熊猫谷承担生态旅游与野化放归，'
     '建议由同一窗口统一口径，避免两个园区各自对接造成客源分散。')
item('四、落地载体指定。建议明确研学团队的城市住宿由市区酒店板块承接、'
     '熊猫谷线路由国堰宾馆承接，党建培训由集团培训板块承接，避免同一客源多板块分散承接。')
item('五、报送重点。按集团近期“聚焦赛道、跟地方政府和国资谈”的部署要求，'
     '本次建议以熊猫专列、熊猫谷联线、国堰研学基地三条作为主推项目先行落地，'
     '其余板块作配套跟进。')

# ==================== 四 ====================
h1('四、下一步')
item('一、2026 年 11 月 20 日前，由产业发展部牵头，'
     '与酒店、景区、文旅服务、物业、党建培训、康养六个板块分别确认对接人与可落地的具体事项。')
item('二、2026 年 11 月底前，完成与基地文旅发展部的首轮对接，'
     '明确对接口径、IP 授权边界与场景分工三项前提。')
item('三、2026 年 12 月底前，形成熊猫专列与熊猫谷联线两条主推项目的实施方案，'
     '连同熊猫谷—青城山—都江堰联线的投资与运营测算一并提交集团决策。')

gap = doc.add_paragraph()
gap.paragraph_format.line_spacing = Pt(16)
p('说明：本稿按集团全方位口径组织，按各板块分列，每条写明我方做什么、需要基地给什么、预期效果，不写方案书。'
  '基地三个熊猫主题园区的隶属关系已作区分，避免口径混淆。',
  font='仿宋_GB2312', size=12, after=10)

doc.add_paragraph()
p('安逸酒店集团产业发展部', align=WD_ALIGN_PARAGRAPH.RIGHT, after=2)
p('2026 年 11 月 18 日', align=WD_ALIGN_PARAGRAPH.RIGHT)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
doc.save(OUT)
print('SAVED:', OUT)
print('SIZE:', os.path.getsize(OUT))

