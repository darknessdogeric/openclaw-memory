# -*- coding: utf-8 -*-
"""给董事长的一页纸 v4：资源为先；一个体系（数智化）+三个方向+四大能力；Mandai 样板"""
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
LEAD = ('核心思想：资源为先。方式只是载体，资源才具备不可复制性。集团按抢什么资源分三个方向，'
        '以一个数智化体系筑牢运营护城河，存量改造按步骤推进、先出产品再放量。')

H1 = '一、总体判断：资源比位置更靠前'
P1 = [
 '位置不是充分条件：同样位置、同样房量，产品做对了是首，做错了是尾；位置决定被谁看到，产品决定被记住多少、付多少。',
 '但资源比位置更靠前。位置可以被复制，同一街区可以开出多家；业态可以被复制，品牌与打法可以学；资源不可以复制——山川湖泊、野生动物保护区、城市核心区位、不可再生的存量物业，一个地方只有一份。',
 '所以集团不按业态分类，按抢什么资源分类。业态是分类，资源是打法，方式是载体，资源是目的。',
 '同时明确五项不做：自建高端奢华度假品牌、重资产新建（除已履行决策程序的项目外）、经济型与中端标准化连锁、'
 '非必要全服务会议型产品、以拓展带改造的对冲。',
]

H2 = '二、一个体系、三个方向、四大能力'
T2_HEAD = ['方向', '瞄准资源', '产品形态', '关键经营指标']
T2 = [
 ['城市生活方式', '各城市核心区位物业，主要瞄准城市更新', '中高端有限精选，可拓展功能模块',
  '每间可售房收入、功能模块坪效、会员直销占比'],
 ['全服务政商培训', '各地市州培训会议型存量改造项目，既有存量资源，又部分占据城市核心区位',
  '中高端全服务，会议与培训产品包', '团队间夜数、会议厅坪效、营业利润率'],
 ['度假', '四川省内核心优质景点资源，山川湖泊、森林', '中高端及以上，自创品牌加外部品牌联营',
  '平均房价溢价率、淡旺季比、二次消费占比'],
]
T3_HEAD = ['能力', '建法']
T3 = [
 ['在地文化能力', '策展空间、展陈与线上矩阵，构成当地文化展示窗口；借展、艺术家驻店与手作客座常态化'],
 ['资源能力', '以占资源为首要目的，轻资产拿运营权而非自购产权；用旅投信用与地方政府、景区谈资源'],
 ['产品能力', '模块化配置，按客源支付能力装配；形成品牌、产品、服务、运营与筹开的标准产品包'],
 ['数字化能力', '一个体系筑牢运营护城河，类似华住：底座层全域统一，系统模块层按业态装配，输出层对外可售并绑定三类合同模板'],
]
P2 = [
 '数智化四场景：收益管理、会议与客源、渠道与内容、经营诊断与预警。验收标准一律是业务指标，不是模型指标。',
 '数智化四步：先统一口径，不投系统，此步不花钱，不做则后面全部无效；再单店基础信息化与贯通；再集团级人工智能中台另立项，私有化部署与数据治理；最后对外输出。',
]

H3 = '三、样板：Mandai Rainforest Resort by Banyan Tree（悦榕集团新加坡样本）'
P3 = [
 '位置：坐落于新加坡 Mandai 野生动物保护区，直连 Singapore Zoo、Night Safari、River Wonders、Bird Paradise、Rainforest Wild Adventure 五大园区。',
 '产品：338 间客房全部为树冠与岸线栖居，最顶级房型是独栋树屋；房费含园区门票，早餐在动物园内与饲养员同场，夜游、熊猫馆、亚洲象馆都是住店动线。',
 '机制：酒店是载体，生态资源不可复制；在地文化就是保育本身，不靠造景；把门票与住宿打成一个产品卖。',
 '对安逸：四川的山川湖泊森林是同一种资源，可做同样的资源即产品；城市更新片区与地市州存量物业同理，占住资源比选哪种打法更要紧。',
]

H4 = '四、存量改造：按步骤推进，每一步先出产品再放量'
T4_HEAD = ['步骤', '内容', '验证什么', '止损条件']
T4 = [
 ['第一步\n品牌文化先行\n＋可独立先行的隐蔽工程\n＋首批房间做透',
  '品牌重塑、文创与策展联营、基础信息化；外立面、结构与消防主体、屋面防水、设备机房与主干管线；'
  '首批客房与公共功能区域一次做透，含隐蔽与饰面',
  '品牌市场接受度、主题商品与联营营收、数据颗粒度是否建成、首批客房爬坡斜率',
  '六个月品牌咨询量未提升，或联营无营收，或数据颗粒度未建成，或首批客房出租率未突破 45%，不进第二步'],
 ['第二步\n拓展客房与园林', '第二批客房、公共区域深化、园林与庭院',
  '平均房价与出租率爬坡斜率、营业利润率改善幅度', '投后十二个月出租率未突破 45%，冻结追加，转做运营'],
 ['第三步\n剩余区域与运营深化', '餐饮、会议、康养场景与全店运营深化',
  '整体投资回报与回收期', '回收期超三年或五年红线，降档或退出'],
]
P4 = [
 '同一批空间内，隐蔽工程与饰面必须同批完成，不得先做隐蔽再分批饰面，否则开挖破坏；隐蔽工程可独立先行的，是后续不再进入的空间与部位。',
 '样板先行列为强制动作：先做样板客房并封样确认，再按样板验证过的做法与单价放量，单店不少于二十间，验证一个完整经营周期；每一步只放大上一步已验证的部分。',
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


def build(fs=9.0, ls=11.8, top=1.2, bot=1.0, left=1.6, right=1.4, tf=8.0, tls=10.0):
    doc = Document()
    s = doc.sections[0]
    s.page_width = Cm(21.0)
    s.page_height = Cm(29.7)
    s.top_margin = Cm(top)
    s.bottom_margin = Cm(bot)
    s.left_margin = Cm(left)
    s.right_margin = Cm(right)

    para(doc, TITLE, 14.5, 20, '方正小标宋简体', False, False, 1, WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, SUB, 9.5, 14, '楷体', False, False, 4, WD_ALIGN_PARAGRAPH.CENTER)
    para(doc, LEAD, fs, ls, '仿宋', False, True, 3)

    para(doc, H1, fs, ls, '黑体', True, False, 1, before=2)
    for x in P1:
        para(doc, x, fs, ls, '仿宋', False, True, 1)

    para(doc, H2, fs, ls, '黑体', True, False, 1, before=2)
    mktable(doc, T2_HEAD, T2, tf, tls, [2.7, 4.7, 3.9, 4.6])
    mktable(doc, T3_HEAD, T3, tf, tls, [2.7, 13.2])
    for x in P2:
        para(doc, x, fs, ls, '仿宋', False, True, 1)

    para(doc, H3, fs, ls, '黑体', True, False, 1, before=2)
    for x in P3:
        para(doc, x, fs, ls, '仿宋', False, True, 1)

    para(doc, H4, fs, ls, '黑体', True, False, 1, before=2)
    mktable(doc, T4_HEAD, T4, tf, tls, [2.5, 4.5, 3.6, 4.6])
    for x in P4:
        para(doc, x, fs, ls, '仿宋', False, True, 1)

    doc.save(DX)


def pages():
    outdir = os.path.join(WS, 'tmp', '_pg5')
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


for cfg in [(9.5, 12.5, 1.3, 1.1, 1.7, 1.5, 8.5, 10.5),
            (9.0, 11.8, 1.2, 1.0, 1.6, 1.4, 8.0, 10.0),
            (8.5, 11.0, 1.1, 0.9, 1.5, 1.3, 7.5, 9.5),
            (8.0, 10.5, 1.0, 0.8, 1.4, 1.2, 7.0, 9.0)]:
    build(*cfg)
    pg = pages()
    print('正文%.1f/行距%.1f/表%.1f/%.1f -> 实测 %d 页' % (cfg[0], cfg[1], cfg[6], cfg[7], pg))
    if pg == 1:
        shutil.copy2(DX, os.path.join(DESK, NAME + '.docx'))
        print('  >>> 采用该版，%.1f KB' % (os.path.getsize(DX) / 1024))
        break
