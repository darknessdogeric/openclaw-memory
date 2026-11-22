# -*- coding: utf-8 -*-
"""与成都大熊猫基地合作项目 · 报送口径建议稿（Word 公文版）"""
import os
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = r"C:\Users\ericz\Desktop\与成都大熊猫基地合作项目_报送口径建议稿_安逸酒店集团产业发展部_2026-11-18.docx"

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
    p(t, font='楷体_GB2312', size=16, bold=True, before=4, after=2)


def item(t):
    """条目：标题加粗，正文常规，同段"""
    par = doc.add_paragraph()
    par.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    par.paragraph_format.line_spacing = Pt(30)
    par.paragraph_format.first_line_indent = Pt(32)
    F(par.add_run(t), '仿宋_GB2312', 16, False)
    return par


def item2(head, body):
    """条目：黑体小标题 + 楷体正文，三行结构"""
    par = doc.add_paragraph()
    par.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    par.paragraph_format.line_spacing = Pt(30)
    par.paragraph_format.first_line_indent = Pt(32)
    F(par.add_run(head), '黑体', 16, False)
    for lab, txt in body:
        q = doc.add_paragraph()
        q.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        q.paragraph_format.line_spacing = Pt(30)
        q.paragraph_format.left_indent = Pt(32)
        q.paragraph_format.first_line_indent = Pt(0)
        F(q.add_run(lab), '楷体_GB2312', 16, True)
        F(q.add_run(txt), '仿宋_GB2312', 16, False)


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
p('安逸酒店集团产业发展部', font='仿宋_GB2312', size=15, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
p('关于与成都大熊猫基地合作项目的报送口径建议稿', font='方正小标宋简体', size=20,
  align=WD_ALIGN_PARAGRAPH.CENTER, spacing=34, after=4)
p('报送对象：集团产业发展部（陈天科部长、蔡思捷）　　编制日期：2026 年 11 月 18 日',
  font='仿宋_GB2312', size=12, align=WD_ALIGN_PARAGRAPH.CENTER, after=14)

# ==================== 〇 ====================
h1('〇、三条纪律（写报材料前必须守住）')
item('一、不提“熊猫主题酒店”。集团已明确批评“熊猫”品牌空心化与低端化。'
     '安逸·熊猫是安逸连锁旗下低档门店（追马卡拉、大邑、熊猫、星光、天香仁和、藏雅），'
     '本次只报熊猫文化的深度运营，载体是国堰宾馆，不新开熊猫酒店。')
item('二、只报“把基地客流变成安逸产品”的事，不报“想进基地做文创”的空话。'
     '落点是住宿、研学、零售、传播四类。')
item('三、IP 授权边界先留白。成都大熊猫繁育研究基地的形象、名称、文创开发授权属对方商业化权限，'
     '我方只承诺提供场景与运营能力，授权条款请基地方面明确后再落协议。')

# ==================== 一 ====================
h1('一、存量项目：与基地可直接对接的（四条）')

item2('1. 熊猫专列·锦绣天府号——“行”侧引流入口',
      [('我方：', '旅投系“熊猫专列”（安逸号／锦绣天府号）已由心已远国际旅行社操盘运营，'
                 '采用“铁路方出车＋旅投购买运营权＋运营方全流程操盘”模式，锦绣天府号 8 万／10 万两档，以入境客为主；'
                 '与集团酒店可形成“行＋住”闭环。'),
       ('需基地：', '基地园区或成都市域内的上车点接驳、专列线路与班期上的基地产品植入、联合售票口径。'),
       ('预期：', '以专列为入口把基地客流导入四川沿线（含都江堰）住宿与非房消费，专列每班次形成住宿与餐饮溢出。')])

item2('2. 国堰宾馆“熊猫文化研学基地”——“住”侧承接载体（最实）',
      [('我方：', '都江堰国堰宾馆与成都大熊猫繁育研究基地同处都江堰，基地至酒店车程约 20 分钟。'
                 '国堰改造项目已明确定位“政务文化交流基地＋本土康养产业基地＋熊猫文化研学基地”三大文化定位，'
                 '空间规划含 AR 大屏、治水文化水井坊、谚语堂、“一菜一故事”、熊猫亲子文创等九重文化空间；'
                 '非房收入占比目标由 25% 提升至 65%。'),
       ('需基地：', '研学课程内容与师资对接、亲子文创联名开发、基地客人 VIP 通道与接待标准。'),
       ('预期：', '基地研学团队与散客的餐宿由国堰承接，研学与非房收入成为国堰改造后的主力收益结构。')])

item2('3. 安逸·熊猫与“大熊猫国潮 IP”——品牌与轻资产输出的对象',
      [('我方：', '安逸 6 大品牌体系含“安逸·熊猫”；集团“先锋国潮新潮”赛道的大熊猫国潮 IP 对应酒店为新良酒店，'
                 '可承接熊猫主题的轻资产授权与品牌输出。'),
       ('需基地：', '熊猫主题 IP 的品牌授权路径与使用边界、联名产品的开发与分成机制。'),
       ('预期：', '形成“基地 IP＋安逸品牌＋轻资产托管”的可复制产品包，为集团轻资产超 200 家提供主题化样本。')])

item2('4. 熊猫主题文创与零售——非房收入与川货出川',
      [('我方：', '安逸新零售（安逸甄选／安逸集市）承接熊猫主题文创、亲子伴手礼上架；'
                 '专列机上与沿线零售渠道同步；安逸 7 大子品牌中的非遗与农庄品牌可做熊猫场景下的组合礼盒。'),
       ('需基地：', '文创选品与联名开发通道、专列及园区渠道的货品准入。'),
       ('预期：', '形成“到站即购”的熊猫场景商品线，纳入新零售年度点位与 SKU 计划。')])

# ==================== 二 ====================
h1('二、未来想合作的项目（六条）')

item2('5. “熊猫＋青城山＋都江堰”联线产品',
      [('内容：', '基地（都江堰）—国堰—青城山道观—灌县古城，两日一夜联线，住宿由国堰承接、餐饮与非房由国堰运营，专列或直通车串联。'),
       ('需基地：', '联线线路与时间窗、联合售票与分账机制。')])

item2('6. 熊猫生态研学营地（青少年＋企业团建）',
      [('内容：', '依托国堰会议与研学空间，做熊猫生态研学、非遗手作、中医药 SPA（藏羌医药）、茶与农庄的组合课程。'),
       ('需基地：', '研学导师或课程内容支持、公益与研学资质背书。')])

item2('7. 熊猫文化主题展陈与文创落地',
      [('内容：', '在国堰设熊猫文化主题展陈与零售区（与九重文化空间一体），按“IP 授权＋内容运营＋商品分成”模式落地。'),
       ('需基地：', '展览与文创的内容授权、联名品牌与产品开发的对接部门。')])

item2('8. 主人与员工服务：基地员工与家属的差旅住宿',
      [('内容：', '以安逸会员体系承接基地及其合作单位的员工差旅、接待与家属探亲住宿，形成稳定协议价与会员权益。'),
       ('需基地：', '职工差旅标准与采购口径、是否可纳入单位福利采购目录。')])

item2('9. 熊猫主题短视频与城市传播',
      [('内容：', '依托集团新媒体矩阵（抖音 35 个＋小红书 35 个账号）与专列 4 班期现成熊猫 IP 素材，'
                 '做熊猫基地×安逸酒店×熊猫专列的城市级内容 campaign；小红书侧主打“亲子出行攻略”，抖音侧主打“专列＋住宿＋基地”线路内容。'),
       ('需基地：', '官方账号联合发布、素材与拍摄准入、舆情口径。')])

item2('10. 安全与风险防控服务（保险合作延伸）',
      [('内容：', '以人保财险“安全管理＋网安保险＋风险防控服务”模式，为基地及合作单位的公共上网、安全生产、'
                  '食品安全与极端天气提供风险减损服务，落地载体为集团智能弱电与 AI 风险预警能力。'),
       ('需基地：', '是否有对应采购或合作需求；可由集团与保险方共同提案。')])

# ==================== 三 ====================
h1('三、需要集团与基地明确支持的四件事')
item('一、对接口径：本次主要领导到基地对接，是就基地侧的合作需求（接待、研学、文创），还是就 IP 商业化授权？'
     '两者对应的我方方案完全不同，建议先明确。')
item('二、IP 授权边界：熊猫形象、名称、文创开发的授权范围与分成机制。')
item('三、客流动线：基地团队与散客的接驳、时间窗、团队规模（研学与团队分批量）。')
item('四、落地载体指定：建议明确由国堰宾馆作为“熊猫文化研学基地”唯一承接载体，避免同一客源被多个板块分散承接。')

# ==================== 四 ====================
h1('四、我方可即时提供的能力清单（供谈判调用）')
tbl(['能力', '说明'],
    [
        ['研学住宿与餐饮承载', '国堰 236 间客房＋会议空间＋餐饮，可承接团队研学与散客'],
        ['专列运营', '熊猫专列／锦绣天府号已运营，铁路＋运营＋客源三角模式成熟'],
        ['主题内容方法论', '成都院子“5 朵金花贯穿全业态＋五大产品串联”的可复制方法'
                        '（OCC 约 80%、RevPAR 近 800、OTA 仅占 48%—50%），用于把熊猫主题做成真主题而非贴标'],
        ['零售与文创通道', '安逸新零售私域商城＋安逸甄选＋外部运营商（川茶、非遗、农产品）'],
        ['传播能力', '新媒体 70 个账号＋专列 4 班期熊猫 IP 素材＋品牌 VI 与内容团队'],
        ['数字化', '岭博网关与网监审计一体化、AI 风险预警、AI 与数据中台（业务智能体／客户需求洞察／产业资源衔接）'],
    ],
    widths=[3.6, 13.4])

gap = doc.add_paragraph()
gap.paragraph_format.line_spacing = Pt(16)
p('说明：本稿按“存量可直接对接的项目”与“未来想合作的项目”两段式填写，每条一句话讲清我方做什么、需要基地给什么、预期效果，不写方案书。',
  font='仿宋_GB2312', size=12, after=10)

doc.add_paragraph()
p('安逸酒店集团产业发展部', align=WD_ALIGN_PARAGRAPH.RIGHT, after=2)
p('2026 年 11 月 18 日', align=WD_ALIGN_PARAGRAPH.RIGHT)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
doc.save(OUT)
print('SAVED:', OUT)
print('SIZE:', os.path.getsize(OUT))
