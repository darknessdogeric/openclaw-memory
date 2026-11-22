# -*- coding: utf-8 -*-
"""《大干一百天 冲刺四季度》公众号发布稿 · 审核意见（安逸酒店集团产业发展部）"""
import os
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = r"C:\Users\ericz\Desktop\大干一百天冲刺四季度_公众号发布稿审核意见_安逸酒店集团产业发展部_2026-11-18.docx"

doc = Document()
st = doc.styles['Normal']
st.font.name = '仿宋_GB2312'
st.font.size = Pt(14)
st.element.rPr.rFonts.set(qn('w:eastAsia'), '仿宋_GB2312')
st.paragraph_format.space_after = Pt(0)
st.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
st.paragraph_format.line_spacing = Pt(26)
for sec in doc.sections:
    sec.top_margin = Cm(3.0); sec.bottom_margin = Cm(2.8)
    sec.left_margin = Cm(2.6); sec.right_margin = Cm(2.4)


def F(run, name='仿宋_GB2312', size=14, bold=False):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    run._element.rPr.rFonts.set(qn('w:eastAsia'), name)


def p(t, font='仿宋_GB2312', size=14, bold=False, indent=2, align=None,
      before=0, after=0, spacing=26):
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
    p(t, font='黑体', size=14, before=10, after=2)


def h2(t):
    p(t, font='楷体_GB2312', size=14, bold=True, before=6, after=2)


def item(t):
    par = doc.add_paragraph()
    par.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    par.paragraph_format.line_spacing = Pt(26)
    par.paragraph_format.first_line_indent = Pt(28)
    F(par.add_run(t), '仿宋_GB2312', 14, False)
    return par


def cite(t):
    """原文引述"""
    par = doc.add_paragraph()
    par.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    par.paragraph_format.line_spacing = Pt(26)
    par.paragraph_format.left_indent = Pt(28)
    par.paragraph_format.first_line_indent = Pt(0)
    F(par.add_run('原文：'), '楷体_GB2312', 13, True)
    F(par.add_run(t), '仿宋_GB2312', 13, False)
    return par


def shade(cell, hexc):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement('w:shd'); sh.set(qn('w:val'), 'clear'); sh.set(qn('w:fill'), hexc)
    tcPr.append(sh)


def tbl(headers, rows, widths=None, fs=10):
    t = doc.add_table(rows=1, cols=len(headers)); t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hc = t.rows[0].cells
    for i, h in enumerate(headers):
        hc[i].text = ''
        pp = hc[i].paragraphs[0]; pp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pp.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        pp.paragraph_format.line_spacing = Pt(16)
        F(pp.add_run(h), '黑体', fs, False); shade(hc[i], 'D9D9D9')
    for ri, row in enumerate(rows):
        cs = t.add_row().cells
        for ci, v in enumerate(row):
            cs[ci].text = ''
            pp = cs[ci].paragraphs[0]
            pp.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
            pp.paragraph_format.line_spacing = Pt(16)
            F(pp.add_run(str(v)), '仿宋_GB2312', fs, False)
            if ri % 2 == 1:
                shade(cs[ci], 'F2F2F2')
    if widths:
        for r in t.rows:
            for i, w in enumerate(widths):
                r.cells[i].width = Cm(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    return t


# ==================== 文头 ====================
p('安逸酒店集团产业发展部', font='仿宋_GB2312', size=13, align=WD_ALIGN_PARAGRAPH.CENTER, after=2)
p('《大干一百天  冲刺四季度——安逸酒店集团改革破题、稳步推进推动年度目标落地》',
  font='方正小标宋简体', size=17, align=WD_ALIGN_PARAGRAPH.CENTER, spacing=30, after=2)
p('公众号发布稿审核意见', font='方正小标宋简体', size=17,
  align=WD_ALIGN_PARAGRAPH.CENTER, spacing=30, after=4)
p('审核对象：11.18 V2 版　　审核单位：安逸酒店集团产业发展部　　2026 年 11 月 18 日',
  font='仿宋_GB2312', size=11, align=WD_ALIGN_PARAGRAPH.CENTER, after=12)

# ==================== 〇 ====================
h1('〇、审核结论')
item('稿件整体质量较高，六条举措逻辑清晰、事实充分，"文旅融合业态升级""川渝会员互通""旅游列车"三条具备对外发布的实力与亮点。'
     '但按集团公众号对外发布口径，尚有 3 处须处理、4 处建议改写、5 个亮点建议补充。'
     '其中第一处涉及公开点名单一经营困难企业，建议发布前必须删除或改写。')

# ==================== 一 ====================
h1('一、发布前必须处理的三处')
h2('（一）不得点名古尔沟公司【高】')
cite('已在锦著空港、安逸美舍、乐山嘉州宾馆、古尔沟公司4家直营店试点店长负责制')
item('古尔沟为公司资不抵债、累计亏损较大且正在推进破产重整与关停处置的主体。'
     '将其与其他三家直营店并列写入"市场化改革破题"的正面表述，等于在公众号公开点名单一经营困难企业，'
     '且与集团正在推进的关停并转、两资两非处置工作口径相冲突，易被外部解读为"安逸改革阵痛"。')
item('处理建议：改为"已在锦著空港、安逸美舍、乐山嘉州宾馆等 4 家直营店试点店长负责制"，'
     '或改述为"已在部分直营门店试点店长负责制"。如确需体现覆盖面，可另补同批试点门店数量而不点名。')

h2('（二）不宜对外表述"争取酒店资产划转"【高】')
cite('主动对接集团内外各类资源，争取更多优质国有酒店资产划转至安逸运营平台')
item('一、资产划转属集团决策事项，"争取"二字对外发布等于以公告形式提出资产划转诉求，不宜由企业公众号先行发声；'
     '二、若后续未落地，将形成对外承诺与实际不符的落差。')
item('处理建议：改为"主动对接集团内外各类资源，持续提升优质国有酒店资产的运营承接能力，'
     '推动更多存量资产在安逸平台实现价值提升"。落点在"承接运营能力"，不在"划转诉求"。')

h2('（三）结尾段的攻坚表述建议中性化【中高】')
cite('统筹推进利润攻坚、资产盘活、资金清收与风险防控')
item('"利润攻坚""资金清收""风险防控"三词并置，读者容易读成"亏损、欠款、出险"，'
     '与前文六条正向举措的基调不匹配，建议改为正面结果导向的表述。')
item('处理建议：改为"统筹推进经营质效提升、存量资产盘活、资金效率优化与发展风险防控，'
     '同步完善治理体系，推动经营质效稳步提升，确保全年各项工作圆满收官"。')

# ==================== 二 ====================
h1('二、建议改写的四处表述')
tbl(['原文表述', '问题', '建议改法'],
    [
        ['"明确由茶业公司作为二销业务承载主体，敲定品牌二次授权运营模式"',
         '"二销"为内部简称，公众号读者无从理解；"敲定"属内部语态',
         '统一改为"安逸新零售"，全篇"二销拓展板块"改为"新零售板块"，"敲定"改为"明确"'],
        ['"梳理形成 300 余款产品清单初稿"',
         '"初稿"对外发布会被读成尚未完成',
         '改为"形成 300 余款产品清单"'],
        ['"积极打通华夏邮轮川货展销、成都及三亚中免免税店入场等销售渠道"',
         '"打通""入场"均为未落地状态，公众号慎用推进式动词',
         '改为"积极拓展华夏邮轮川货展销、成都及三亚中免免税店等销售渠道"'],
        ['"打造区域省级国资酒店协同发展样板"',
         '重庆两江假日酒店管理公司为市属国资平台，"省级国资"表述与事实不符',
         '核实后改为"打造区域国资酒店协同发展样板"，或删去"省级"'],
    ],
    widths=[6.0, 4.4, 5.6])

# ==================== 三 ====================
h1('三、建议补充的五个亮点')
item('一、补充政治站位。稿子目前从企业自身工作写起，缺少上位依据。'
     '建议在导语段增加一句：集团落实省委十二届七次全会关于推进文化和旅游深度融合发展的决策部署，'
     '贯彻省旅投集团"一体两翼"战略，锚定成为文旅产业整合平台。'
     '这一句放在开头，整篇的格局与分量立刻不同。')
item('二、把"锦绣天府·安逸四川"立为全文主线。稿中仅在专列一条末尾出现一次，'
     '建议提升为导语中的品牌主线，并让六条举措都与之呼应，形成统一的对外品牌声量。')
item('三、把入境游单列为一条亮点。240 小时过境免签、联动 10 余国 20 余家头部组团社、入境游客占比超九成、'
     '获新华社与省文旅厅省国资委集中报道、入选四川省文旅领域改革创新典型案例——'
     '这一组内容对外价值很高，目前被埋在专列条内，建议独立成条。'
     '如内部有带动入境游客人次、带动消费额等数据，建议补入。')
item('四、补充数智化与人工智能应用。当前稿子第四、五条已写中央预订、会员互通与商旅平台接入，'
     '但集团在人工智能与数据中台方向的工作未体现。建议在第四条中补一句，'
     '说明正推进人工智能与数据中台建设、在收益管理、需求预测、新零售运营等场景落地应用，'
     '这既是集团"数智赋能"的对外形象，也是行业关注点。')
item('五、会员与直销要给数字。稿中"对OTA渠道的依赖和渠道成本持续下降"是有力表述，'
     '但无数字支撑，公众号读者最关心这个变化幅度。'
     '建议补入安逸会会员规模、中央预订率提升幅度或渠道成本下降幅度中的任一可公开指标。')

# ==================== 四 ====================
h1('四、两处可选强化的表述')
item('一、第 3 条专列的数据可再补一层。稿中"累计开行 9 趟、累计收客 784 席、上座率 94.69%"数字准确，'
     '但 9 趟的体量在公众号语境下容易被追问规模。'
     '建议补入后续计划开行班期、覆盖城市或线路数量，以及"一期一主题"的迭代节奏（如已规划的蜀锦宋韵等主题），'
     '把"体量小"转成"节奏密、单产品打磨深"。')
item('二、第 6 条文创活动可升格。帆书与乐山嘉州酒店的合作，'
     '是"文化内容赋能酒店闲置空间"的典型样本，与集团轻资产输出、文化主题酒店的逻辑是一体的。'
     '建议从"文创活动板块"提升为独立表述，与第五条的存量改造、文化主题旗舰店形成"空间改造 + 内容运营"的组合。')

# ==================== 五 ====================
h1('五、需办公室统一把关的两项')
item('一、组织与人事相关表述。第四条"机构精简、职能集约、运行高效"，涉及集团组织架构调整，'
     '且集团层面正推进大运营中心机制，建议由办公室会同组织人事部门确认对外口径，'
     '避免与内部调整节奏不一致。')
item('二、对外数据的统一口径。本篇涉及的补贴金额、开行班次、会员互通对象等数据，'
     '建议由办公室统一核对发布版本，确保与各条线对外口径一致。')

gap = doc.add_paragraph()
gap.paragraph_format.line_spacing = Pt(14)
p('以上意见，供办公室修改时参考。审核人：安逸酒店集团产业发展部。',
  font='仿宋_GB2312', size=12, after=10)

doc.add_paragraph()
p('安逸酒店集团产业发展部', align=WD_ALIGN_PARAGRAPH.RIGHT, after=2)
p('2026 年 11 月 18 日', align=WD_ALIGN_PARAGRAPH.RIGHT)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
doc.save(OUT)
print('SAVED:', OUT)
print('SIZE:', os.path.getsize(OUT))
