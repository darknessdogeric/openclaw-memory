# -*- coding: utf-8 -*-
"""关于西藏航空《战略合作框架协议》的补充建议（安逸酒店集团产业发展部）· 简洁公文稿"""
import os
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.ns import qn

OUT = r"C:\Users\ericz\Desktop\关于西藏航空战略合作框架协议的合作意见（建议稿）_安逸酒店集团产业发展部_2026-11-03.docx"

doc = Document()
st = doc.styles['Normal']
st.font.name = '仿宋_GB2312'
st.font.size = Pt(16)
st.element.rPr.rFonts.set(qn('w:eastAsia'), '仿宋_GB2312')
st.paragraph_format.space_after = Pt(0)
st.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
st.paragraph_format.line_spacing = Pt(32)
for sec in doc.sections:
    sec.top_margin = Cm(3.4); sec.bottom_margin = Cm(3.2)
    sec.left_margin = Cm(2.8); sec.right_margin = Cm(2.6)


def F(run, name='仿宋_GB2312', size=16, bold=False):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    run._element.rPr.rFonts.set(qn('w:eastAsia'), name)


def p(text, font='仿宋_GB2312', size=16, bold=False, indent=0, align=None,
      before=0, after=0, spacing=32):
    par = doc.add_paragraph()
    par.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    par.paragraph_format.line_spacing = Pt(spacing)
    par.paragraph_format.space_before = Pt(before)
    par.paragraph_format.space_after = Pt(after)
    if align is not None:
        par.alignment = align
    if indent:
        par.paragraph_format.first_line_indent = Pt(size * indent)
    F(par.add_run(text), font, size, bold)
    return par


def gap(pts=14):
    par = doc.add_paragraph()
    par.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    par.paragraph_format.line_spacing = Pt(pts)


def title(t):
    p(t, font='方正小标宋简体', size=20, align=WD_ALIGN_PARAGRAPH.CENTER, spacing=32, after=4)


def item(head, text):
    """条目：1、+ 标题（黑体）+ 正文（仿宋），连续排"""
    par = doc.add_paragraph()
    par.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    par.paragraph_format.line_spacing = Pt(32)
    par.paragraph_format.first_line_indent = Pt(32)
    F(par.add_run(head), '黑体', 16, False)
    F(par.add_run(text), '仿宋_GB2312', 16, False)


# ======================== 标题 ========================
gap()
title('关于《西藏航空有限公司与四川省旅游投资集团有限责任公司')
title('战略合作框架协议》的补充建议')
gap()

# ======================== 主送 ========================
p('四川省旅游投资集团产业发展部：', after=2)

# ======================== 开头 ========================
p('贵部牵头与西藏航空签订的《战略合作框架协议》，已就航空客运业务、酒店业务、'
  '航空旅游、金融投资及其他领域合作达成框架共识。我部结合酒店板块及新零售业务实际，'
  '就协议未尽事项提出以下补充建议。', indent=2)

# ======================== 四条 ========================
item('1、酒店板块合作内容。',
     '协议第二条已明确西藏航空在同等市场条件下优先选择乙方酒店成为其签约酒店。'
     '建议补充明确承接主体与落地方式，由安逸品牌酒店承接藏航员工差旅、会议会务及机组运行保障住宿，'
     '在成都、重庆、西安三个基地城市形成协议价与签约酒店安排，并将机组保障条款单列。')

item('2、新零售合作内容。',
     '协议第三条已明列机票加酒店、机票加景点及航空广告。建议在该项下增加商品维度，'
     '由安逸新零售在机上零售与航线渠道上架安逸甄选、川茶及川货产品，'
     '试点川货进藏、藏货出川双向商品通道，并在藏航机场、办公及员工服务场景推广联合货架与联合点位。')

item('3、会员与品牌渠道合作内容。',
     '建议推进西藏航空常旅客会员与安逸会会员在积分累积、权益互享及会员数据互通上的合作，'
     '与安逸会积分方案一并提交审议；并就航空广告、航线主题营销与联合推广形成打包方案。')

item('4、资产合作与配套安排。',
     '建议依托协议第四条金融投资合作方向，推动西藏航空参与东部新区天府山庄（三岔湖）联合开发，'
     '我部提供产业策划与品牌方案。同时建议明确安逸品牌在协议项下的认定口径与授权路径，'
     '并在协议合作推进联合工作组中为我部产发部及相关子企业明确席位。')

# ======================== 结语 ========================
gap()
p('以上补充建议，供贵部完善协议及后续签订具体业务合作协议时参考。', indent=2)

# ======================== 落款 ========================
gap()
gap()
p('安逸酒店集团产业发展部', align=WD_ALIGN_PARAGRAPH.RIGHT, after=2)
p('2026 年 11 月 3 日', align=WD_ALIGN_PARAGRAPH.RIGHT)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
doc.save(OUT)
print('SAVED:', OUT)
print('SIZE:', os.path.getsize(OUT))
