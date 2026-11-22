# -*- coding: utf-8 -*-
import io, sys, os, re, subprocess, shutil
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

ITEMS = [
 '组织形式建议按“两块牌子、一套人马、分职能运作”设计，企业经营管理、绩效考核与亏损企业治理不整体划出。',
 '建议增设管道费与商业化岗位，归口各类品牌费、管理费、服务费的定价、归集与收缴。',
 '建议增设知识管理与标准产品化岗位，将品牌、产品、服务标准及筹开打包为可交付业主的产品包。',
 '建议收益管理从营销板块独立，按“集团标准与系统、区域与单店执行”两层设置。',
 '建议中央集采板块明确集采服务费模式与节约额归属口径，补充对外收入与分账规则。',
 '建议将业主关系维护单列考核，管理费回款率与合同续约率纳入板块及岗位考核。',
 '建议按四品牌设置品牌经理，明确品牌标准编制、审核与稽核的责任人与授权层级。',
 '建议运营标准板块增列集团级改造技术标准库输出，与六家存量酒店改造标准统一。',
 '建议开发拓展岗后端增列筹开岗位，覆盖工程审图、开业筹备、系统接入与开业营销。',
 '建议明确管理规模 100 家以上的承接机制，与集团 180 家以上管理酒店目标相衔接。',
 '建议第一阶段改为选定三家改造样板店产出标准，品牌标准手册分店分模块形成，取消一次性发布。',
 '建议数字化板块与已立项的人工智能收益管理、人工智能与数据中台项目建立接口并明确考核。',
 '建议明确划出的 AK 替代、数字旅投管理业务的承接主体、交接清单与交接期责任人。',
 '建议补充量化目标：管理费收入、自有渠道占比、会员人均贡献、新增受托家数、人均管理店数。',
 '建议补充投入产出测算：43 人三年人力成本、平台与差旅投入及对应管理费与对外收入。',
 '建议补充风险退出条款与验收主体：两年未达标时的编制调整与退出安排，由战略部与财务金融部共同验收。',
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

doc = Document()
s = doc.sections[0]
s.page_width = Cm(21.0)
s.page_height = Cm(29.7)
s.top_margin = Cm(2.2)
s.bottom_margin = Cm(2.0)
s.left_margin = Cm(2.6)
s.right_margin = Cm(2.4)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.line_spacing = Pt(26)
p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
p.paragraph_format.space_after = Pt(4)
set_font(p.add_run('对《安逸酒店集团大运营体系建设实施方案（草案）》的意见建议'), '方正小标宋简体', 16)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.line_spacing = Pt(17)
p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
p.paragraph_format.space_after = Pt(8)
set_font(p.add_run('安逸酒店集团产业发展部　2026 年 11 月 21 日'), '楷体', 11)

for i, it in enumerate(ITEMS, 1):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing = Pt(18)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.first_line_indent = Pt(24)
    pf.space_after = Pt(2)
    set_font(p.add_run(str(i) + '.'), '黑体', 12, bold=True)
    set_font(p.add_run(it), '仿宋', 12)

doc.save(DX)
shutil.copy2(DX, os.path.join(ARCH, NAME + '.docx'))
print('DOCX: ' + DX + '  (%d KB, %d 条)' % (os.path.getsize(DX) // 1024, len(ITEMS)))

SOFFICE = 'C:\\Program Files\\LibreOffice\\program\\soffice.com'
outdir = os.path.join(WS, 'tmp', '_pdfchk2')
for f in os.listdir(outdir) if os.path.isdir(outdir) else []:
    os.remove(os.path.join(outdir, f))
os.makedirs(outdir, exist_ok=True)
r2 = subprocess.run([SOFFICE, '--headless', '--convert-to', 'pdf', '--outdir', outdir, DX],
                   capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=240)
pdf = os.path.join(outdir, NAME + '.pdf')
if os.path.exists(pdf):
    import pypdf
    n = len(pypdf.PdfReader(pdf).pages)
    print('实测页数: %d  %s' % (n, '一页纸 OK' if n == 1 else '仍超页'))
else:
    print('PDF 未生成:', (r2.stdout or r2.stderr or '')[:150])