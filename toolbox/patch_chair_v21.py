# -*- coding: utf-8 -*-
import os, shutil
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

DOCX = r"C:\Users\ericz\Desktop\产业发展部\给董事长的单独汇报\关于安逸酒店集团发展赛道与存量改造路径的指导意见的报告_修订版_v2.0_2026-11-20.docx"
NAVY = RGBColor(0x1F, 0x38, 0x64); RED = RGBColor(0xC0, 0x00, 0x00)
doc = Document(DOCX)

def F(run, name='仿宋_GB2312', size=11, bold=False, color=None):
    run.font.name = name; run.font.size = Pt(size); run.bold = bold
    run._element.rPr.rFonts.set(qn('w:eastAsia'), name)
    if color is not None:
        run.font.color.rgb = color

def P(t, font='仿宋_GB2312', size=11, bold=False, indent=2, align=None, color=None,
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

def h1(t):
    return P(t, font='黑体', size=12.5, before=10, after=2, color=NAVY)

def h2(t):
    return P(t, font='楷体_GB2312', size=11, bold=True, before=6, after=2)

def item(t):
    par = doc.add_paragraph()
    par.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    par.paragraph_format.line_spacing = Pt(21)
    par.paragraph_format.first_line_indent = Pt(22)
    F(par.add_run(t), '仿宋_GB2312', 11, False)
    return par

def note(t):
    par = doc.add_paragraph()
    par.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    par.paragraph_format.line_spacing = Pt(21)
    par.paragraph_format.left_indent = Pt(22); par.paragraph_format.first_line_indent = Pt(0)
    F(par.add_run(t), '楷体_GB2312', 10.5, False, RED)
    return par

def shade(cell, hexc):
    tcPr = cell._tc.get_or_add_tcPr()
    sh = OxmlElement('w:shd'); sh.set(qn('w:val'), 'clear'); sh.set(qn('w:fill'), hexc)
    tcPr.append(sh)

def tbl(headers, rows, widths=None, fs=9):
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
    tail = doc.add_paragraph()
    tail.paragraph_format.space_after = Pt(3)
    made.append(t._tbl); made.append(tail._p)
    return t

# ===== 构造新增内容（先建在文末，再整体移到"一、总体判断"之前）=====
made = []
def keep(par):
    el = par._p if hasattr(par, '_p') else par._tbl
    made.append(el); return par
keep(h1('指示承接关系与口径统一'))
keep(item('集团主要负责同志就发展赛道与存量改造的指示，自 11 月 13 日以来持续深化，'
          '产业发展部已多次应答。为避免多轮应答之间出现口径不一，'
          '本件先将承接关系交代清楚，再进入落实内容。'))
tbl(['时间', '指示形态', '产发部应答', '本件关系'],
    [
        ['11-13', '①主赛道选择；②存量改造路径与范式',
         '响应稿；正式报告 v1.0（七章：总体判断／赛道选择／赛道产品模型／'
         '赛道商业模型／管道费体系／存量改造范式／组织保障）',
         '**本件为 v1.0 的修订版**，v1.0 原件同目录留存'],
        ['11-15', '同上，要求深化', '深度再研究 v2.0', 'v1.0 已吸收其结论'],
        ['11-18', '四品牌构想：国堰＝高端全服四星、花园＝城市中高端生活方式、'
         '锦著＝中端快捷、度假品牌＝温泉山川湖泊、临水',
         '应答案：**认同 80%，两处要改，一处要补**',
         '**本件承接其三项结论，见下**'],
        ['11-20', '三业态落位；位置＝资源；存量改造如何高效', '**本件**', '最新一轮落实稿'],
    ],
    widths=[1.4, 5.0, 5.6, 4.8])
keep(h2('（一）"一塔一轴"与"三业态"是两个维度，不冲突'))
keep(item('11-18 应答已判定：**度假品牌不是第四个品牌，是第二条轴**；'
          '前三个品牌都在城市里做酒店，竞争维度是产品与运营；'
          '资源型品牌竞争的是资源占有，一旦占住即形成不可复制壁垒，'
          '且它是轻资产输出与区域资源合作的谈判筹码。'))
keep(item('本次指示以三业态表述，与之不矛盾：**业态维度是分类，'
          '品牌维度是架构。**'
          '对外统一说"三业态"，对内按"一塔一轴"管品牌：'
          '一塔＝城市生活方式、政商旅全服务、城市有限服务三类城市产品；'
          '一轴＝资源型品牌，贯穿三类业态，以"安逸"为母品牌收口。'))
keep(note('★ 建议集团正式确认这一表述：'
          '"三业态"是业务分类，"一塔一轴"是品牌架构，'
          '两者分别用于对外沟通与对内管理，不必二选一。'))
keep(h2('（二）母品牌收口'))
keep(item('11-18 已明确：四个品牌平铺会让人误以为要养四个品牌，'
          '而集团现状（自营口径不一、委管口径不一）撑不起多个平行对外品牌，'
          '须以"安逸"为母品牌收口。**本件沿用该结论，'
          '并据此明确资源型品牌的名称应落在母品牌之下（如"安逸·锦秀"），'
          '不另起独立品牌。**'))
keep(h2('（三）旅投接口'))
keep(item('11-18 已补：资源型品牌是旅投与安逸的接口，'
          '**旅投能给的是信用与资源协调，不是钱**；'
          '集团资产负债率 75.78%、古尔沟 184.16%，不具备替业主垫资改造的能力。'
          '本件第四章据此把接口拆为两个面：'
          '**资产端靠债转股审批，资源端靠景区与地方政府协调。**'))
keep(h2('（四）国堰经营数据口径'))
keep(item('11-18 应答已明确国堰数据取自集团数据分析平台实际数据'
          '（2026 年 1 月 1 日至 10 月 24 日，297 天）：'
          '平均房价 266.80 元、出租率 38.47%、RevPAR 102.63 元、'
          '非房收入占比 44.66%，'
          '并据此判定"11 个汤池仍未做出 RevPAR，'
          '说明是产品未被重新定义，不是位置不行"。'
          '**本件统一采用该口径。**'))
keep(note('★ 另一组数据（平均房价 216.99 元、出租率 37.05%、RevPAR 80.4 元）'
          '来源与期间尚未标注，须补注后确认是否同一口径，'
          '**在确认前不作为对外承诺依据**。'))
keep(note('★ 11-18 的上述判断与本件第二章的完整式表述同源：'
          '"位置（不可复制）＋在地文化（不可替代）＋产品形态（可交付）'
          '＝可定价的收益结构"。'
          '**同一结论在两轮应答中相互印证，可作为向集团说明的第一条依据。**'))

# ===== 移动到"一、总体判断"之前 =====
anchor = None
for p in doc.paragraphs:
    if p.text.strip().startswith('一、总体判断'):
        anchor = p
        break
if anchor is None:
    raise SystemExit('ANCHOR NOT FOUND')
for el in made:
    anchor._p.addprevious(el)

# ===== 更正修订说明表中的"更正一"行 =====
for t in doc.tables:
    for row in t.rows:
        c0 = row.cells[0].text.strip()
        if c0 == '更正一':
            cell = row.cells[2]
            cell.text = ''
            pp = cell.paragraphs[0]
            pp.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
            pp.paragraph_format.line_spacing = Pt(15)
            F(pp.add_run('国堰宾馆经营数据的期间与来源须补注。'
                         '本件统一采用 11 月 18 日应答案已锁定的口径'
                         '（集团数据分析平台实际数据，2026 年 1 月 1 日至 10 月 24 日，297 天）；'
                         '另一组数据在补注确认前不作对外承诺依据（详见第六章第一节）'), '仿宋_GB2312', 9, False)
    # 第六章口径表第1项
    for row in t.rows:
        c0 = row.cells[0].text.strip()
        if c0 == '1' and '国堰宾馆经营数据' in row.cells[1].text:
            cell = row.cells[2]
            cell.text = ''
            pp = cell.paragraphs[0]
            pp.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
            pp.paragraph_format.line_spacing = Pt(15)
            F(pp.add_run('**本件统一采用 2026 年 1 月 1 日至 10 月 24 日实际数据口径**：'
                         '平均房价 266.80 元、出租率 38.47%、RevPAR 102.63 元、'
                         '非房收入占比 44.66%；'
                         '另一组（216.99 元／37.05%／80.4 元）来源与期间待补注'),
              '仿宋_GB2312', 9, False)

doc.save(DOCX)
print('PATCHED', os.path.getsize(DOCX))
