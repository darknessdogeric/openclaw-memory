# -*- coding: utf-8 -*-
"""在《关于安逸酒店集团2026年度经营情况及2027年工作举措的汇报》的第八条下补充产发部2027年工作目标"""
import os, shutil
from docx import Document
from docx.shared import Pt, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

SRC = r"C:\Users\ericz\Desktop\关于安逸酒店集团2026年度经营情况及.docx"
BAK = r"D:\B166ER-openclaw\workspace\anyi-ops-kb\07_战略与改革\关于安逸酒店集团2026年度经营情况及_原件_2026-11-03.docx"

doc = Document(SRC)

# ---------- 备份原件 ----------
os.makedirs(os.path.dirname(BAK), exist_ok=True)
shutil.copy2(SRC, BAK)

# ---------- 定位第八条 ----------
paras = doc.paragraphs
idx = None
for i, p in enumerate(paras):
    if p.text.strip().startswith('八是轻资产拓展'):
        idx = i
        break
assert idx is not None, "未找到第八条"
anchor = paras[idx + 1]
print("锚点段落 index=%d: %r" % (idx, paras[idx].text[:40]))
print("插入位置: 之后 = %r" % anchor.text[:30])

IND = Emu(443865)   # 与 2027 部分各条一致
SZ_HEAD = 18
SZ_BODY = 16


def mk_para(anchor, parts):
    """parts = [(text, bold, size, font)]"""
    par = anchor.insert_paragraph_before('')
    par.style = doc.styles['Heading 1']
    par.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    par.paragraph_format.first_line_indent = IND
    par.paragraph_format.left_indent = Emu(0)
    for text, bold, size, font in parts:
        r = par.add_run(text)
        r.bold = bold
        r.font.size = Pt(size)
        r.font.name = font
        r._element.rPr.rFonts.set(qn('w:eastAsia'), font if font != 'Times New Roman' else 'Times New Roman')
    return par


def mk_body(anchor, text):
    return mk_para(anchor, [(text, False, SZ_BODY, '仿宋_GB2312')])


def mk_item(anchor, num, head, body):
    return mk_para(anchor, [
        (num, True, SZ_HEAD, 'Times New Roman'),
        (head, True, SZ_BODY, '仿宋_GB2312'),
        (body, False, SZ_BODY, '仿宋_GB2312'),
    ])


# ---------- 总述 ----------
mk_body(anchor,
    '2027年，产业发展部将围绕品牌赋能与产业增量孵化，推动前期已形成的框架协议、资源通道和策划成果转化为落地项目。')

# ---------- 四条举措 ----------
mk_item(anchor, '1.', '完善品牌标准与轻资产授权体系。',
    '统一品牌定位、视觉识别、产品服务配置与筹建改造要求，配套投资模型和软加盟、硬加盟、管理合同三类授权文本'
    '及合作方准入评审机制，形成可交付、可复制的轻资产输出工具，为承接划转酒店、拓展品牌授权提供支撑。')

mk_item(anchor, '2.', '做强安逸新零售，形成第二增长曲线。',
    '由蒙顶山茶业公司承接二销业务，商投集团作为主要货源供应链，已完成总府皇冠、双流机场两处卖场点位互换。'
    '2027年计划拓展线下点位10个以上、首期上架产品50个以上、接入运营商3家以上，建成私域商城并单开外贸体系，'
    '落地销售数据周报；同步推动与商投集团战略合作框架协议签订，拓展航司等外部渠道商品合作。')

mk_item(anchor, '3.', '以数字化提升产业运营效能。',
    '推进AI与数据中台建设，形成业务智能体、客户需求洞察、政策资金跟踪三类应用，与集团数字化中台二期建设衔接，'
    '深化数据治理和业务链路贯通，推动人工智能在收益管理、需求预测、新零售运营等场景落地；'
    '打通新零售私域平台与会员体系的数据桥接，降低对三方渠道依赖。')

mk_item(anchor, '4.', '推进存量改造策划与增量项目转化。',
    '承担存量酒店改造的定位研判、改造标准制定与品牌落地跟踪，向投资资产条线提供品牌定位、溢价空间、目标客群等'
    '策划参数；推动熊猫专列三方协议签署与常态化开行，深化与悦榕集团、西藏航空等外部品牌的联合品牌及联合开发合作，'
    '探索轻重分离下的高端度假品牌输出路径。')

doc.save(SRC)
print('SAVED:', SRC, os.path.getsize(SRC))
print('BACKUP:', BAK)
