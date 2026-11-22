# -*- coding: utf-8 -*-
"""在《2026年度经营情况及》第八条下补充第5条：集团赋能型平台合作（含数据支撑）"""
import os, shutil
from docx import Document
from docx.shared import Pt, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

SRC = r"C:\Users\ericz\Desktop\关于安逸酒店集团2026年度经营情况及.docx"
BAK = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\07_战略与改革\关于安逸酒店集团2026年度经营情况及_含产发部4条_备份_2026-11-03.docx"

doc = Document(SRC)
os.makedirs(os.path.dirname(BAK), exist_ok=True)
shutil.copy2(SRC, BAK)

paras = doc.paragraphs
idx = None
for i, p in enumerate(paras):
    if p.text.strip().startswith('4.推进存量改造策划'):
        idx = i
        break
assert idx is not None, "未找到第4条"
anchor = paras[idx + 1]
print("锚点 P%d 之后 = %r" % (idx, anchor.text[:20]))

IND = Emu(443865)


def mk_item(anchor, num, head, body):
    par = anchor.insert_paragraph_before('')
    par.style = doc.styles['Heading 1']
    par.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    par.paragraph_format.first_line_indent = IND
    par.paragraph_format.left_indent = Emu(0)
    for text, bold, size, font in [
        (num, True, 18, 'Times New Roman'),
        (head, True, 16, '仿宋_GB2312'),
        (body, False, 16, '仿宋_GB2312'),
    ]:
        r = par.add_run(text)
        r.bold = bold
        r.font.size = Pt(size)
        r.font.name = font
        r._element.rPr.rFonts.set(qn('w:eastAsia'), font)
    return par


HEAD = '深化平台渠道合作，提升集团渠道赋能与直销质效。'

BODY = (
    '集团已与小红书、抖音、美团等平台建立合作基础：抖音集团账号后台授权已完成，'
    '可获取委托管理项目与执行项目全量抖音数据；小红书已与2家服务商对接，酒店类目专属费率7.5%、餐饮3.5%，'
    '较美团酒店8%-10%、抖音8%低6至25个百分点；美团合作将酒店充电宝统一接入安逸会会员入口，'
    '入会赠送免费充电时间、单店分润提高1成，框架协议已通过对方法务。'
    '行业层面，2025年国内酒店OTA渠道订单占比达63%、渠道成本同比上涨27%，'
    '携程佣金率已升至15%-20%、叠加流量推广后综合获客成本达15%-25%，'
    '而华住自有渠道间夜占比已突破75%、锦江中央预订率超75%，渠道结构分化正在加快。'
    '集团现有在营酒店56家、2026年目标103家，以在营酒店经营数据为参照测算，'
    'OTA渠道与会员直订每间夜获客成本相差约24元，'
    '2027年计划将OTA渠道间夜占比压降5个百分点，对应约38万间夜转为会员直订，折合减少渠道成本约900万元。'
    '2027年同时计划开通集团平台矩阵号5个以上、建成抖音数据看板、打通1个新零售商品通道，'
    '推动会员与直销渠道贯通，将三方渠道佣金支出压降15%。'
)

mk_item(anchor, '5.', HEAD, BODY)

doc.save(SRC)
print('SAVED:', SRC, os.path.getsize(SRC))
print('BACKUP:', BAK)
