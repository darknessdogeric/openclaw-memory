# -*- coding: utf-8 -*-
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

NAVY = RGBColor(0x1F, 0x38, 0x64); RED = RGBColor(0xC0, 0x00, 0x00)

def F(run, name='仿宋_GB2312', size=11, bold=False, color=None):
    run.font.name = name; run.font.size = Pt(size); run.bold = bold
    run._element.rPr.rFonts.set(qn('w:eastAsia'), name)
    if color is not None:
        run.font.color.rgb = color

def P(doc, t, font='仿宋_GB2312', size=11, bold=False, indent=2, align=None, color=None,
      before=0, after=0, spacing=21):
    par = doc.add_paragraph()
    par.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    par.paragraph_format.line_spacing = Pt(spacing)
    par.paragraph_format.space_before = Pt(before); par.paragraph_format.space_after = Pt(after)
    if align is not None:
        par.alignment = align
    if indent:
        par.paragraph_format.first_line_indent = Pt(size * indent)
    F(par.add_run(t), font, size, bold, color)
    return par

# ============ 任务1：给上一版件追加修订说明 v1.1 ============
OLD = r"C:\Users\ericz\Desktop\景区度假型业态_外部品牌托管模式分析_v1.0_2026-11-20.docx"
d = Document(OLD)
d.add_page_break()
P(d, '修订说明（v1.1 · 2026 年 11 月 20 日）', font='黑体', size=13, align=WD_ALIGN_PARAGRAPH.CENTER,
  color=NAVY, after=6)
P(d, '安逸酒店集团产业发展部', font='仿宋_GB2312', size=11, align=WD_ALIGN_PARAGRAPH.CENTER, after=8)

P(d, '一、第七节"三项目落地排序"结论有误，现更正', font='黑体', size=11.5, before=6, after=2)
P(d, '更正一：原建议"三岔湖天府山庄作首个试点"不成立。', font='楷体_GB2312', size=11, bold=True, after=2)
P(d, '三岔湖相关资产实际为两项，且均不属安逸集团可自主处置范围：'
    '一、"成都东部新区天府山庄"为省旅投 100% 持有，三钻 73 间，已停业，'
    '列入"停业评估备案、联系意向方"与"天府山庄资产转让"；'
    '二、"三岔湖岛屿项目"（88.8 亩、3 个独立岛屿、原四川省人大培训中心、'
    '完整国有商业建设用地、无品牌）同为省旅投资产，'
    '安逸仅有"引入合作方共同开发"的诉求。'
    '原件将二者混同，并推荐了一个集团无资金来源、无处置权限的项目。', after=4)

P(d, '更正二：古尔沟不宜作首个托管试点这一判断不成立。', font='楷体_GB2312', size=11, bold=True, after=2)
P(d, '经核对集团《古尔沟公司系统性改革盘活实施方案》与相关台账，'
    '古尔沟是三个候选中唯一同时具备四个条件的载体：'
    '一、安逸酒店集团控股 52%（理县城投 30%、大九旅 18%）；'
    '二、集团已在改革方案中明确"安逸·锦秀：温泉康养主题度假酒店（依托古尔沟）"，'
    '子品牌与载体均已定；'
    '三、悦榕已同意赴现场考察；'
    '四、华美达品牌授权即将到期，形成天然时间窗口。'
    '且古尔沟正处在系统性改革盘活的关口，'
    '引入外部品牌运营方正是该方案"运营市场化"与"业态扩容"两项的直接抓手。'
    '**首个试点改为古尔沟。**', after=4)

P(d, '更正三：本件第四节将"保留集团品牌 + 外部托管"归入轨道 B（付品牌费），属归类错误。',
  font='楷体_GB2312', size=11, bold=True, after=2)
P(d, '保留集团品牌、外部方只做管理的结构，经济性质是"自有品牌 + 委托管理"，'
    '即轨道 A 的变体，不含品牌授权费；'
    '与轨道 B（挂外部品牌、付品牌费与品牌管理费）的根本区别在于品牌资产归属。'
    '古尔沟项目按前者设计，方能在合同中把品牌资产与会员数据留在安逸一侧。', after=4)

P(d, '二、本件其余结论不受影响', font='黑体', size=11.5, before=6, after=2)
P(d, '第一节的模式确认（Mandai 先例与命名法）、第二节的三条反向证据'
    '（九寨沟悦榕庄经营不佳、悦榕已在四川、托管的真实价值在学运营与建品牌资产）、'
    '第三节"保留集团品牌"的三种含义、第五节准入五问、'
    '第七节的其余排序与节点提醒，均继续有效。', after=4)

P(d, '三、后续处理', font='黑体', size=11.5, before=6, after=2)
P(d, '已另行出具《古尔沟 × 悦榕集团 合作方案要点与条款清单 v1.0》，'
    '作为古尔沟方向的具体落地方案，本件与之配套使用。', after=4)

d.add_paragraph()
P(d, '安逸酒店集团产业发展部', font='仿宋_GB2312', size=11, align=WD_ALIGN_PARAGRAPH.RIGHT, after=2)
P(d, '2026 年 11 月 20 日', font='仿宋_GB2312', size=11, align=WD_ALIGN_PARAGRAPH.RIGHT)
d.save(OLD)
print('PATCHED:', OLD, os.path.getsize(OLD))
