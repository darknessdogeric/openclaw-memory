# -*- coding: utf-8 -*-
"""给董事长的一页纸：发展赛道与存量改造路径 汇报要点"""
import io, sys, os, re, subprocess, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_LINE_SPACING, WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.enum.table import WD_TABLE_ALIGNMENT

DESK = r'C:\Users\ericz\Desktop'
DIR = os.path.join(DESK, '产业发展部', '给董事长的单独汇报')
WS = r'D:\B166ER-openclaw\workspace'
NAME = '2026-11-21_发展赛道与存量改造路径_汇报要点一页纸'
DX = os.path.join(DIR, NAME + '.docx')
SOFFICE = r'C:\Program Files\LibreOffice\program\soffice.com'

TITLE = '安逸酒店集团发展赛道与存量改造路径 · 汇报要点'
SUB = '呈：集团董事长　　拟：产业发展部　　2026 年 11 月 21 日'
LEAD = ('一句话结论：赛道不再全面开花，改为三业态加一条资源轴；改造先花小钱买判断依据再谈大钱；'
        '资源型项目零改造先托管、不挂牌外部品牌；数字化先统一口径、不投系统。')

H1 = '一、赛道：从单一主赛道改为三业态加一条资源轴'
T1_HEAD = ['业态', '定位', '获客逻辑', '关键经营指标']
T1 = [
 ['城市商旅生活方式', '中高端有限精选，可拓展功能模块', '地理位置加功能模块', '每间可售房收入、功能模块坪效、会员直销占比'],
 ['城市及度假地政商旅', '中高端全服务，面向培训级会议与宴会', '会议与培训需求加目的地资源', '团队间夜数、会议厅坪效、营业利润率'],
 ['旅游度假型', '中高端及以上，自创品牌加外部品牌联营', '景区与湖泊山林资源加品牌背书', '平均房价溢价率、淡旺季比、二次消费占比'],
]
T1_NOTE = ('资源型品牌不是第四个品牌，是贯穿三类业态的第二条轴，以"安逸"为母品牌收口。五项不做：自建高端奢华度假品牌、'
           '重资产新建（除已过会）、经济型与中端标准化连锁、非必要全服务会议型产品、以拓展带改造的对冲。'
           '分类错位修正一处：都江堰青城山为资源型度假地载体，成都核心街区为城市更新片区生活方式。')

H2 = '二、改造：三级下探，每一级一条止损线'
T2_HEAD = ['级别', '动作', '预算', '验证什么', '止损条件']
T2 = [
 ['第一级\n品牌与文化先行', '品牌重塑 44 万、文创与策展联营 50 万、基础信息化 80 万', '约 174 万',
  '品牌市场接受度、联营营收、数据颗粒度是否建成', '六个月品牌咨询量未提升，或联营无营收，或数据颗粒度未建成，不进第二级'],
 ['第二级\n可见界面与运营提升', '公区场景、园林、餐厅、宴会会议；客房按间改造', '约 3000 万',
  '平均房价与出租率爬坡斜率、营业利润率改善幅度', '投后十二个月出租率未突破 45%，冻结追加，转做运营'],
 ['第三级\n结构性改造', '隐蔽工程：管线、机电、空调、消防、外立面', '约 800 至 1500 万',
  '仅在第二级已验证改造能带动价格时启动', '前两级任一止损触发，第三级不启动'],
]
T2_NOTE = ('三级的用意不是省钱，是把"投不投、投多少、什么时候停"从一次性变成三次。样板先行强制，单店不少于二十间并验证一个完整经营周期；'
           '改造强度分 L0 至 L2，回收期红线三年与五年，超红线降档或退出。')

H3 = '三、资源型项目：自有品牌加委托管理，首期零改造先托管'
P3 = [
 '集团现金投入接近零，管理费与经营结果挂钩，是抵押受限、经营利润薄、程序未定时唯一能立即启动的方式。',
 '不挂牌外部品牌：品牌费、管理费、会员计入对方、溢价归对方，等于永久让出该赛道。',
 '合同必须写入五项：品牌归属、会员与数据归属、员工保留、退出与过渡期、排他与优先权。',
 '指标三条写入协议阶段目标，不写入运营团队考核表。',
]

H4 = '四、数字化：三层体系、四个场景、四步实施'
P4 = [
 '三层：底座层全域统一，系统模块层按业态装配，输出层对外可售并绑定三类合同模板。',
 '四场景：收益管理、会议与客源、渠道与内容、经营诊断与预警；验收标准均为业务指标而非模型指标。',
 '四步：先统一口径（不花钱，不做则后面全部无效）→ 单店样板贯通 → 人工智能中台另立项 → 对外输出。',
]

H5 = '五、请集团决策六项'
DEC = [
 '是否以"位置加在地文化加产品形态"作为战略表述，以三业态落位替代单一主赛道表述；建议确认，并授权形成业态、资源、产品、指标四列表。',
 '改造第一级约一百七十四万元是否立即启动；建议启动，作为改造路径能否收敛的第一道闸门。',
 '古尔沟走盘活还是处置；建议明确走盘活，同步启动债转股审批协调。',
 '古尔沟是否按自有品牌加委托管理结构启动谈判；建议按此结构，首期零改造先托管。',
 '是否授权产业发展部统一归口对外品牌合作谈判；建议授权，全产业链四方向与合作条款作为同一套文件的两个附件提交。',
 '数字化穿透是否按四步立项；建议按四步，第四步并入轻资产输出合同模板。',
]

H6 = '六、待核实五项（详见报告第七章）'
P6 = [
 '改造房量口径记载不一致，须与投资资产部锁定，否则单房投入基数与止损线均为浮动。',
 '改造测算经营数据为两组，一组已标注期间、一组未标注期间，补注确认前不作对外承诺依据。',
 '锦秀商标权属原在一家民营企业手中且已有冠名用法，子品牌对外使用前须完成检索与注册。',
 '所引行业基准数据未经授权不得转载或重新发布，仅限内部使用。',
 '人工智能中台投入须与收益管理立项合并报批，避免两条线重复投入。',
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


def para(doc, text, fs, ls, ea='仿宋', bold=False, indent=True, after=2, align=None, before=0):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing = Pt(ls)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    pf.space_after = Pt(after)
    pf.space_before = Pt(before)
    if indent:
        pf.first_line_indent = Pt(fs * 2)
    if align is not None:
        p.alignment = align
    set_font(p.add_run(text), ea, fs, bold)
    return p


def mktable(doc, head, rows, fs, ls, widths):
    t = doc.add_table(rows=1, cols=len(head))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for i, c in enumerate(t.rows[0].cells):
        c.text = ''
        p = c.paragraphs[0]
        p.paragraph_format.line_spacing = Pt(ls)
        p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        set_font(p.add_run(head[i]), '黑体', fs, True)
        shd = c._tc.get_or_add_tcPr().makeelement(qn('w:shd'), {qn('w:val'): 'clear', qn('w:fill'): 'D9E2F3'})
        c._tc.get_or_add_tcPr().append(shd)
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ''
            first = True
            for line in str(v).split('\n'):
                p = cells[i].paragraphs[0] if first else cells[i].add_paragraph()
                first = False
                p.paragraph_format.line_spacing = Pt(ls)
                p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
                set_font(p.add_run(line), '仿宋', fs)
    for r in t.rows:
        for i, c in enumerate(r.cells):
            c.width = Cm(widths[i])
    return t


def build(fs=11.0, ls=15.5, top=1.6, bot=1.4, left=2.0, right=1.8, tf=9.5, tls=13):
    doc = Document()
    s = doc.sections[0]
    s.page_width = Cm(21.0)
    s.page_height = Cm(29.7)
    s.top_margin = Cm(top)
    s.bottom_margin = Cm(bot)
    s.left_margin = Cm(left)
    s.right_margin = Cm(right)

    para(doc, TITLE, 15, 22, '方正小标宋简体', False, False, 2, WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, SUB, 10, 15, '楷体', False, False, 6, WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, LEAD, fs, ls, '仿宋', False, True, 4)

    para(doc, H1, fs, ls, '黑体', True, False, 2, before=2)
    mktable(doc, T1_HEAD, T1, tf, tls, [3.0, 4.4, 3.8, 5.6])
    para(doc, T1_NOTE, fs, ls, '仿宋', False, True, 4)

    para(doc, H2, fs, ls, '黑体', True, False, 2, before=2)
    mktable(doc, T2_HEAD, T2, tf, tls, [2.4, 4.0, 2.0, 4.4, 4.0])
    para(doc, T2_NOTE, fs, ls, '仿宋', False, True, 4)

    para(doc, H3, fs, ls, '黑体', True, False, 2, before=2)
    for x in P3:
        para(doc, x, fs, ls, '仿宋', False, True, 1)

    para(doc, H4, fs, ls, '黑体', True, False, 2, before=2)
    for x in P4:
        para(doc, x, fs, ls, '仿宋', False, True, 1)

    para(doc, H5, fs, ls, '黑体', True, False, 2, before=2)
    for i, x in enumerate(DEC, 1):
        para(doc, '%d. %s' % (i, x), fs, ls, '仿宋', False, True, 1)

    para(doc, H6, fs, ls, '黑体', True, False, 2, before=2)
    for x in P6:
        para(doc, x, fs, ls, '仿宋', False, True, 1)

    doc.save(DX)
    return len(DEC)


def pages():
    outdir = os.path.join(WS, 'tmp', '_pg2')
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


for cfg in [(10.5, 14.5, 1.5, 1.3, 1.8, 1.6, 9.0, 12),
            (10.0, 13.5, 1.4, 1.2, 1.7, 1.5, 8.5, 11),
            (9.5, 12.5, 1.3, 1.1, 1.6, 1.4, 8.5, 10)]:
    n = build(*cfg)
    pg = pages()
    print('正文%.1f/行距%.1f/表%.1f/%.1f -> %d 决策项, 实测 %d 页' % (cfg[0], cfg[1], cfg[6], cfg[7], n, pg))
    if pg == 1:
        shutil.copy2(DX, os.path.join(DESK, NAME + '.docx'))
        print('  >>> 采用该版，%.1f KB' % (os.path.getsize(DX) / 1024))
        break
