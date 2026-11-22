# -*- coding: utf-8 -*-
"""《大干一百天 冲刺四季度》公众号稿 · 可增加亮点与引进项目清单"""
import os
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = r"C:\Users\ericz\Desktop\大干100天公众号稿_可增加亮点与引进项目清单_2026-11-18.docx"

doc = Document()
st = doc.styles['Normal']
st.font.name = '仿宋_GB2312'
st.font.size = Pt(12)
st.element.rPr.rFonts.set(qn('w:eastAsia'), '仿宋_GB2312')
st.paragraph_format.space_after = Pt(0)
st.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
st.paragraph_format.line_spacing = Pt(22)
for sec in doc.sections:
    sec.top_margin = Cm(2.6); sec.bottom_margin = Cm(2.4)
    sec.left_margin = Cm(2.4); sec.right_margin = Cm(2.2)


def F(run, name='仿宋_GB2312', size=12, bold=False):
    run.font.name = name; run.font.size = Pt(size); run.bold = bold
    run._element.rPr.rFonts.set(qn('w:eastAsia'), name)


def p(t, font='仿宋_GB2312', size=12, bold=False, indent=2, align=None,
      before=0, after=0, spacing=22):
    par = doc.add_paragraph()
    par.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    par.paragraph_format.line_spacing = Pt(spacing)
    par.paragraph_format.space_before = Pt(before); par.paragraph_format.space_after = Pt(after)
    if align is not None:
        par.alignment = align
    if indent:
        par.paragraph_format.first_line_indent = Pt(size * indent)
    F(par.add_run(t), font, size, bold)
    return par


def h1(t):
    p(t, font='黑体', size=13, before=10, after=2)


def h2(t):
    p(t, font='楷体_GB2312', size=12, bold=True, before=6, after=2)


def item(t):
    par = doc.add_paragraph()
    par.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    par.paragraph_format.line_spacing = Pt(22)
    par.paragraph_format.first_line_indent = Pt(24)
    F(par.add_run(t), '仿宋_GB2312', 12, False)
    return par


def quote(t):
    par = doc.add_paragraph()
    par.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    par.paragraph_format.line_spacing = Pt(22)
    par.paragraph_format.left_indent = Pt(24)
    par.paragraph_format.first_line_indent = Pt(0)
    F(par.add_run(t), '楷体_GB2312', 11.5, False)
    return par


def shade(cell, hexc):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement('w:shd'); sh.set(qn('w:val'), 'clear'); sh.set(qn('w:fill'), hexc)
    tcPr.append(sh)


def tbl(headers, rows, widths=None, fs=9.5):
    t = doc.add_table(rows=1, cols=len(headers)); t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hc = t.rows[0].cells
    for i, h in enumerate(headers):
        hc[i].text = ''
        pp = hc[i].paragraphs[0]; pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pp.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        pp.paragraph_format.line_spacing = Pt(15)
        F(pp.add_run(h), '黑体', fs, False); shade(hc[i], 'D9D9D9')
    for ri, row in enumerate(rows):
        cs = t.add_row().cells
        for ci, v in enumerate(row):
            cs[ci].text = ''
            pp = cs[ci].paragraphs[0]
            pp.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
            pp.paragraph_format.line_spacing = Pt(15)
            F(pp.add_run(str(v)), '仿宋_GB2312', fs, False)
            if ri % 2 == 1:
                shade(cs[ci], 'F2F2F2')
    if widths:
        for r in t.rows:
            for i, w in enumerate(widths):
                r.cells[i].width = Cm(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(3)
    return t


# ==================== 文头 ====================
p('安逸酒店集团产业发展部', font='仿宋_GB2312', size=12, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
p('《大干一百天  冲刺四季度》公众号稿', font='方正小标宋简体', size=16,
  align=WD_ALIGN_PARAGRAPH.CENTER, spacing=28, after=2)
p('可增加亮点与引进项目清单', font='方正小标宋简体', size=16,
  align=WD_ALIGN_PARAGRAPH.CENTER, spacing=28, after=4)
p('2026 年 11 月 18 日', font='仿宋_GB2312', size=11, align=WD_ALIGN_PARAGRAPH.CENTER, after=12)

# ==================== 〇 ====================
h1('〇、总体判断')
item('现稿六条举措的亮点集中在自身成绩：茶山补贴、川渝会员互通、专列运营、改革体系、存量改造、新零售。'
     '但集团近两个月最重要的一批引进项目——上海锦江合资、悦榕集团联合品牌、西藏航空战略合作、'
     '成都体育学院三方共建、人保财险合作——稿中均未体现。'
     '这些是外部品牌、国有资本、行业协会与政企协同层面的合作，对公众号读者而言，'
     '“和谁一起做、做到什么程度”比“自己做了什么”更能说明集团的分量。')
item('建议按三档补：'
     '第一档五项建议必加（对外价值最高、事实已固化）；'
     '第二档五项建议加（补充完整）；'
     '第三档四项建议加（补“数智赋能”形象）。'
     '每项均附可直接插入现稿的段落文字，第三档为可选。')

# ==================== 一 ====================
h1('一、第一档：建议必加的五项')

h2('1. 与上海锦江国际成立合资公司')
item('现状：双方各确定两名董事，董事长待定；已开展业务方向研讨与首批合作项目研判，'
     '工商注册与章程修改流程推进中，集团已明确今年内加快完成。'
     '这是省属国资与上海市属国资的国有酒店集团合资，对外分量与信号意义突出，现稿完全未提。')
quote('建议插入段落（置于第五条之后）：')
quote('深化跨区域国有资本协同。与上海锦江国际集团推进合资公司设立，双方已确定董事会席位安排，'
      '就业务方向、首批合作项目与注册流程完成专项研讨，正在加快组建落地。'
      '合资公司聚焦区域国有酒店资源整合与品牌协同，标志着成渝地区国有酒店集团合作由资源层面进入资本层面，'
      '为集团轻资产规模化拓展打开新的通道。')

h2('2. 与悦榕集团推进联合品牌与全产业链合作')
item('现状：集团级会谈，旅投集团副总经理带队、集团一把手与分管资产投资副总共同出席，'
     '双方建立日常对接渠道并约定实地考察，围绕联合品牌模式与四个延伸方向深入交流：'
     '文旅人才培训、康养养修体系、旅行社产品链路打通、物业服务标准引入。'
     '现稿仅在第五条末以“深化与丽呈、悦榕、中旅等头部机构合作”一句带过，无任何内容。')
quote('建议插入段落：')
quote('牵手国际头部品牌，放大存量价值。集团与悦榕集团就联合品牌模式及文旅人才培训、'
      '康养养修、旅行社产品链路、物业服务标准四个方向开展深入交流并建立常态化沟通机制。'
      '联合品牌以组合命名方式实现双品牌露出，在不增加资本投入的前提下提升存量物业品牌溢价与运营品质，'
      '为集团轻资产输出积累可复制的合作范式。')

h2('3. 与西藏航空签署战略合作框架协议')
item('现状：11 月 5 日完成框架协议签署，就航线开辟、市场开发、品牌推广、商业模式构建，'
     '以及酒店业务合作、航空旅游产品共创、金融投资合作等达成框架共识。'
     '这是最近两周最重要的引进项目，稿中完全空白，读者会明显感到缺口。')
quote('建议插入段落：')
quote('拓展航空文旅合作版图。集团与西藏航空签署战略合作框架协议，围绕航线市场开发、'
      '品牌联合推广、酒店业务合作与金融投资等方向建立长期合作机制。'
      '协议明确航空与酒店资源协同路径，将为川内酒店产品注入新的客源通道，'
      '进一步丰富“行＋住＋游”一体化产品供给。')

h2('4. 与成都体育学院、东部集团共建水上运动产业基地')
item('现状：三方共建战略合作方案已成型，框架协议完成签署，载体为天府山庄三岛，'
     '紧邻世运会赛场，与成都体育学院相距约 2 公里，'
     '分近中远三阶段推进，远期形成国际户外运动康养产业园区愿景，'
     '并可打造国家级体教融合示范基地。这是校地企共建、体教融合的省级示范项目，'
     '政治价值与示范效应都强，现稿未提。')
quote('建议插入段落：')
quote('推进校地企共建，打造体教融合新样板。集团联合成都体育学院、成都东部集团，'
      '共同推进天府山庄水上运动产业基地建设，依托载体紧邻世运会赛场的区位优势，'
      '按近中远三阶段推进体育赛事、水上运动、研学康养与园区运营，'
      '并积极创建国家级体教融合示范基地，为集团康养与运动休闲产品线落下关键一子。')

h2('5. 市场化职业经理人实现“零到一”引进')
item('现状：本部成功引入市场化职业经理人 1 名，并配套建立《职业经理人聘用管理办法》'
     '《职业经理人薪酬管理办法》《职业经理人绩效管理办法》《职业经理人退出管理办法》'
     '四项制度与全套契约文书体系。现稿第四条写了制度体系，'
     '但没有点出“成功引入 1 名职业经理人”这一最具说服力的成果，'
     '国企读者最看重的正是这个“引进来了”。')
quote('建议插入段落（置于第四条前段）：')
quote('市场化机制实现实质突破。本部成功引入市场化职业经理人 1 名，'
      '同步建立职业经理人聘用、薪酬、绩效、退出四项管理办法，'
      '将经营指标、权责边界、激励约束刚性纳入契约文书，'
      '经理层“能上能下、能进能出”的市场化用人机制初步形成，'
      '为集团推进市场化改革提供了制度与实践的双重支撑。')

# ==================== 二 ====================
h1('二、第二档：建议补充的五项')
tbl(['引进项目', '可写入的事实', '建议放的位置'],
    [
        ['商投集团战略合作与“安逸甄选”品牌',
         '商投作为主要货源供应链，已完成双方战略合作意向，框架协议由旅投产业发展部牵头签订；'
         '共同打造“安逸甄选”新零售品牌，已完成总府皇冠酒店、双流机场两处点位互换；'
         '元宇宙场景与“安逸集市”会员互通亦在推进',
         '第六条（新零售）扩写'],
        ['中国旅游集团西南分公司多渠道合作',
         '爱达邮轮产品上架、中免含税店铺入场、境外签证中心点位试点、'
         '“中旅银发好时光”项目接入集团线路酒店与景区酒店、联合党建与出境列车项目共创',
         '第六条或新设渠道合作条目'],
        ['人保财险战略合作',
         '已与人保财险四川省分公司就酒店板块达成合作框架，涉及责任险、'
         '安全与网络风险减损、会员权益增值、零售与助农采购、员工保障等方向',
         '可并入第六条或新设'],
        ['大熊猫基地合作',
         '与成都大熊猫繁育研究基地就酒店、研学、文创零售、传播等方向对接；'
         '熊猫谷为该基地内设部门，国堰宾馆与熊猫谷同处都江堰，'
         '研学与生态旅游线路具备联线开发条件',
         '可并入第三条或新设'],
        ['平台方深度合作',
         '抖音集团账号后台授权已完成，可获取全量项目数据；'
         '小红书本地生活专属费率（餐饮 3.5%、酒店 7.5%）；'
         '美团充电宝统一接入安逸会会员入口，入会赠免费充电时间、单店分润提升',
         '第六条或新设“平台合作”条目'],
    ],
    widths=[3.6, 9.4, 3.0])

# ==================== 三 ====================
h1('三、第三档：建议补充的“数智赋能”形象（可选）')
tbl(['方向', '可写入的事实', '价值'],
    [
        ['智能弱电与公安网监合规',
         '引入岭博科技宽带智能云网关与公安网监审计一体化方案，'
         '实现酒店公共上网实名认证、日志留存与网监数据自动上报，'
         '并将风险查勘与防灾减损服务引入安全管理',
         '回应“数据安全与网络合规”监管关切，体现国企的合规能力'],
        ['人工智能与数据中台',
         '推进人工智能与数据中台建设，在收益管理、需求预测、新零售运营等场景推动智能应用落地；'
         '同步引入外部智库、算法专家与专业团队',
         '行业关注度最高，也是集团数智转型对外的主标识'],
        ['客房数字化与新零售入口',
         '推进客房智能电视交互与客房电商合作，以自有渠道承接住店客人流量与非房收入',
         '“存量变流量”的具体载体，与第五条轻资产输出相互印证'],
    ],
    widths=[3.2, 9.0, 3.8])

# ==================== 四 ====================
h1('四、写作提示')
item('一、对外表述的分寸把握。'
     '上海锦江合资可写“加快推进组建”，不宜写“已成立”；'
     '悦榕合作目前为交流洽谈阶段，宜写“开展深入交流、建立常态化机制”，不宜写“达成合作”；'
     '大熊猫基地与大熊猫谷分属不同主体，表述时须统一口径，避免被理解为两家机构。')
item('二、建议把引进项目集中成组。现稿六条是“做了什么”，'
     '建议在第五条与第六条之间增设一段“对外开放与协同”，'
     '把上海锦江、悦榕、藏航、体院、熊猫基地五项归入，'
     '形成“内部改革 + 对外协同”的双线结构，格局更完整，也便于办公室统一把口径。')
item('三、数据使用请与办公室核对。'
     '涉及费率、补贴金额、班次、会员规模等可公开数据，'
     '建议由办公室统一核对发布版本，确保各条线对外口径一致。')

gap = doc.add_paragraph()
gap.paragraph_format.line_spacing = Pt(12)
p('以上清单与段落文字，供修改稿时取用。编制：安逸酒店集团产业发展部。',
  font='仿宋_GB2312', size=11, after=8)

doc.add_paragraph()
p('安逸酒店集团产业发展部', align=WD_ALIGN_PARAGRAPH.RIGHT, after=2)
p('2026 年 11 月 18 日', align=WD_ALIGN_PARAGRAPH.RIGHT)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
doc.save(OUT)
print('SAVED:', OUT)
print('SIZE:', os.path.getsize(OUT))
