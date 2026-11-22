# -*- coding: utf-8 -*-
"""重做一页纸：按集团本部/饭店管理公司/资产运营中心三方分工协作口径，不以产业发展部为中心"""
import io, sys, os, re, subprocess, shutil, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_LINE_SPACING, WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

DESK = 'C:\\Users\\ericz\\Desktop'
ARCH = 'C:\\Users\\ericz\\Desktop\\产业发展部\\重要文件'
WS = 'D:\\B166ER-openclaw\\workspace'
NAME = '2026-11-21_对大运营体系建设实施方案草案的意见建议_一页纸'
DX = os.path.join(DESK, NAME + '.docx')
SOFFICE = 'C:\\Program Files\\LibreOffice\\program\\soffice.com'

LEAD = '建议按集团本部、饭店管理公司、资产运营中心三方的分工协作关系表述如下。'

BLOCKS = [
 ('一、集团本部与饭店管理公司的分工', [
  '建议集团本部保留品牌、标准、IT架构、产品模型四项工作，不参与具体经营与执行行为；饭店管理公司承接全部酒店项目的经营、管理与拓展，包括旗下自营酒店。',
  '建议品牌标准与品牌管理放在集团本部，饭店管理公司负责品牌开发、产品建设与拓展。',
  '建议AI体系建设与架构放在集团本部，饭店管理公司负责应用层的开发与拓展，并纳入管道费体系。',
  '建议集团本部以标准输出、产品模型输出、IT架构与数据服务、品牌授权与对外合作四项服务，对饭店管理公司及门店提供支撑，建立服务目录、响应时限与验收方式，避免只出文件不落地。',
  '建议大运营中心虽为饭店管理公司内设机构，其承接的品牌标准落地、IT架构应用与产品模型落地，仍由集团本部归口部门负责版本管理与验收，形成本部定、中心落、门店用的闭环。',
 ]),
 ('二、资产运营中心与饭店管理公司的分工', [
  '建议在轻重分离方案中同步明确资产运营中心、饭店管理公司、门店三层的租赁定价、委托管理费、考核与亏损分担规则；自营酒店资产在资产运营中心、经营在饭店管理公司，两者之间须有明确协议，避免权责与考核落空。',
  '建议明确品牌授权收入与管道费收入在上述三层中的归属与确认口径。',
 ]),
 ('三、跨主体的定价机制：管道费体系', [
  '建议在集团本部明确管道费归口部门，归口各类费用的定价、归集与收缴，建立管道费体系。包括但不限于品牌费、管理费、服务费、系统费、会员及中央预订订单抽佣、外部合作渠道佣金、体系化营销服务费等。饭店管理公司对外合作项目统一出口，打包赋能单店后从中扣点。',
  '建议管道费的定价权与执行权分离：凡涉及集团品牌、标准、系统、会员的项目，由集团本部统一出具授权意见、统一费率与合同范本；饭店管理公司可独立开展业务，但不得自行对外授权集团品牌与系统。',
  '建议中央集采板块的集采服务费模式与节约额归属口径，纳入统一管道费口径与分账规则。',
 ]),
 ('四、饭店管理公司的内部建制', [
  '建议饭店管理公司在其大运营中心内，将收益管理从营销板块独立，按"集团标准与系统、区域与单店执行"两层设置。收益管理除盯市场与价格外，还需制定市场细分维度、价格体系、价格代码与预订管理标准化制度流程，并定期召开收益管理分析会，对经营与市场全面分析复盘与预测。饭店管理公司设有预订中心的，收益管理领衔预订中心；若通过系统实现自动分单分账，则收益管理单立，整体层级高于营销板块。集团本部负责输出价格体系与价格代码标准。',
  '建议将业主关系维护单列，管理费回款率与合同续约率纳入板块及岗位考核。',
  '建议开发拓展岗后端增列筹开岗位，覆盖工程审图、开业筹备、系统接入与开业相关事务对接。',
 ]),
]


def set_font(run, ea, pt, bold=False):
    run.font.size = Pt(pt)
    run.font.bold = bold
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = rpr.makeelement(qn('w:rFonts'), {})
        rpr.append(rf)
    for a in ('w:ascii', 'w:hAnsi', 'w:eastAsia'):
        rf.set(qn(a), ea)


def build(fs=11.5, ls=17, top=2.0, bot=1.8, left=2.4, right=2.2):
    doc = Document()
    s = doc.sections[0]
    s.page_width = Cm(21.0)
    s.page_height = Cm(29.7)
    s.top_margin = Cm(top)
    s.bottom_margin = Cm(bot)
    s.left_margin = Cm(left)
    s.right_margin = Cm(right)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = Pt(24)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    p.paragraph_format.space_after = Pt(3)
    set_font(p.add_run('对《安逸酒店集团大运营体系建设实施方案（草案）》的意见建议'), '方正小标宋简体', 15)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = Pt(16)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    p.paragraph_format.space_after = Pt(7)
    set_font(p.add_run('安逸酒店集团产业发展部　2026 年 11 月 21 日'), '楷体', 10.5)

    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = Pt(ls)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    p.paragraph_format.first_line_indent = Pt(fs * 2)
    p.paragraph_format.space_after = Pt(2)
    set_font(p.add_run(LEAD), '仿宋', fs)

    idx = 1
    for head, items in BLOCKS:
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.line_spacing = Pt(ls)
        pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        pf.space_before = Pt(3)
        pf.space_after = Pt(1)
        set_font(p.add_run(head), '黑体', fs, bold=True)
        for it in items:
            p = doc.add_paragraph()
            pf = p.paragraph_format
            pf.line_spacing = Pt(ls)
            pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
            pf.first_line_indent = Pt(fs * 2)
            pf.space_after = Pt(2)
            set_font(p.add_run(str(idx) + '.'), '黑体', fs, bold=True)
            set_font(p.add_run(it), '仿宋', fs)
            idx += 1

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p.paragraph_format.line_spacing = Pt(ls)
    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    p.paragraph_format.space_before = Pt(6)
    set_font(p.add_run('安逸酒店集团产业发展部　2026 年 11 月 21 日'), '仿宋', fs)

    doc.save(DX)
    return idx - 1


def pages():
    outdir = os.path.join(WS, 'tmp', '_pg')
    if os.path.isdir(outdir):
        for f in os.listdir(outdir):
            os.remove(os.path.join(outdir, f))
    else:
        os.makedirs(outdir)
    subprocess.run([SOFFICE, '--headless', '--convert-to', 'pdf', '--outdir', outdir, DX],
                   capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=240)
    pdf = os.path.join(outdir, NAME + '.pdf')
    if os.path.exists(pdf):
        import pypdf
        return len(pypdf.PdfReader(pdf).pages)
    return -1


for fs, ls, tp, bt, lf, rt in [(11.5, 17, 2.0, 1.8, 2.4, 2.2), (11.0, 16, 1.8, 1.6, 2.2, 2.0), (10.5, 15, 1.6, 1.5, 2.0, 1.8)]:
    n = build(fs, ls, tp, bt, lf, rt)
    pg = pages()
    print('字号%.1f 行距%d 边距%.1f/%.1f/%.1f/%.1f -> %d 条, 实测 %d 页' % (fs, ls, tp, bt, lf, rt, n, pg))
    if pg == 1:
        shutil.copy2(DX, os.path.join(ARCH, NAME + '.docx'))
        print('  >>> 采用该版，%.1f KB' % (os.path.getsize(DX) / 1024))
        break
