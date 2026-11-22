# -*- coding: utf-8 -*-
"""修正第5条：重算间夜与渠道成本口径（原版漏乘入住率，数字虚高约2.6倍）"""
import os
from docx import Document
from docx.shared import Pt, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

SRC = r"C:\Users\ericz\Desktop\关于安逸酒店集团2026年度经营情况及.docx"
doc = Document(SRC)

# ---------- 重算校验 ----------
N_HOTEL, N_ROOM, OCC, ADR, OTA_SHARE, CUT, DIFF = 103, 200, 0.385, 266.80, 0.50, 0.10, 24
nights = N_HOTEL * N_ROOM * 365 * OCC
rev = nights * ADR
commission = rev * OTA_SHARE * 0.08
shift = nights * CUT
saving = shift * DIFF
print("总间夜 %.0f万  间夜收入 %.2f亿  OTA佣金 %.0f万  转换间夜 %.1f万  节省 %.0f万"
      % (nights / 1e4, rev / 1e8, commission / 1e4, shift / 1e4, saving / 1e4))
print("OTA每间夜成本 %.1f元 vs 直购约5元，差 %.0f元"
      % (ADR * 0.08 + 8, (ADR * 0.08 + 8) - 5))

# ---------- 删除旧的第5条 ----------
paras = doc.paragraphs
old = None
for i, p in enumerate(paras):
    if p.text.strip().startswith('5.深化平台渠道合作'):
        old = p
        break
assert old is not None, "未找到旧第5条"
old._element.getparent().remove(old._element)
print("已删除旧第5条")

# ---------- 重新插入修正版 ----------
paras = doc.paragraphs
idx = None
for i, p in enumerate(paras):
    if p.text.strip().startswith('4.推进存量改造策划'):
        idx = i
        break
anchor = paras[idx + 1]

IND = Emu(443865)
HEAD = '深化平台渠道合作，提升集团渠道赋能与直销质效。'
BODY = (
    '集团已与小红书、抖音、美团等平台建立合作基础：抖音集团账号后台授权已完成，'
    '可获取委托管理项目与执行项目全量抖音数据；小红书已与2家服务商对接，酒店类目专属费率7.5%、餐饮3.5%，'
    '较美团酒店8%-10%、抖音8%低6至25个百分点；美团合作将酒店充电宝统一接入安逸会会员入口，'
    '入会赠送免费充电时间、单店分润提高1成，框架协议已通过对方法务。'
    '行业层面，2025年国内酒店OTA渠道订单占比达63%、渠道成本同比上涨27%，'
    '携程佣金率已升至15%-20%、叠加流量推广后综合获客成本达15%-25%，'
    '而华住自有渠道间夜占比已突破75%、锦江中央预订率超75%，渠道结构分化正在加快。'
    '按2026年目标103家酒店、平均每家200间房、入住率38.5%测算，全年约289万间夜、间夜收入约7.7亿元；'
    '按OTA渠道间夜占比50%估算，年佣金支出规模约3,100万元。'
    'OTA渠道每间夜佣金及推广成本约29元、会员直购约5元，相差约24元，'
    '2027年计划将OTA渠道间夜占比压降10个百分点，对应约29万间夜转为会员直购，'
    '折合减少渠道成本约700万元，并实现三方渠道佣金支出压降15%。'
    '2027年同时计划开通集团平台矩阵号5个以上、建成抖音数据看板、打通1个新零售商品通道。'
)

par = anchor.insert_paragraph_before('')
par.style = doc.styles['Heading 1']
par.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
par.paragraph_format.first_line_indent = IND
par.paragraph_format.left_indent = Emu(0)
for text, bold, size, font in [
    ('5.', True, 18, 'Times New Roman'),
    (HEAD, True, 16, '仿宋_GB2312'),
    (BODY, False, 16, '仿宋_GB2312'),
]:
    r = par.add_run(text)
    r.bold = bold
    r.font.size = Pt(size)
    r.font.name = font
    r._element.rPr.rFonts.set(qn('w:eastAsia'), font)

doc.save(SRC)
print('SAVED:', SRC, os.path.getsize(SRC))
