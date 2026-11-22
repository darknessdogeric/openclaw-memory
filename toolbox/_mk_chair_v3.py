# -*- coding: utf-8 -*-
"""给董事长的一页纸 v3：四板块，资源型折进业态，改造按步骤，含悦榕样板与数字化"""
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
LEAD = ('一句话结论：赛道收敛为三类业态，各自瞄准一类资源；资源型不另立一条线，是旅游度假型的打法；'
        '存量改造改为按步骤推进，先把首批房间做出产品、再分批放量。')

H1 = '一、三类业态，各自瞄准一类资源'
T1_HEAD = ['业态', '定位', '瞄准资源', '关键经营指标']
T1 = [
 ['城市商旅生活方式', '中高端有限精选，可拓展功能模块', '城市更新片区',
  '每间可售房收入、功能模块坪效、会员直销占比'],
 ['城市及度假地政商旅', '中高端全服务，面向培训级会议与宴会', '各地市州存量物业，与国堰高度相似，尽可能服务这一类',
  '团队间夜数、会议厅坪效、营业利润率'],
 ['旅游度假型', '中高端及以上，自创品牌加外部品牌联营', '大四川承接的旅游度假型项目，可与外部品牌联合做',
  '平均房价溢价率、淡旺季比、二次消费占比'],
]
T1_NOTE = ('资源不是第四个业态，是三类业态各自瞄准的资源来源。三类资源的获取方式、决策层级与回报周期不同，'
           '混在一个体系里考核必然出现用度假逻辑做城市店、用商务逻辑做度假店。业态维度是分类，资源维度是打法。'
           '五项不做：自建高端奢华度假品牌、重资产新建（除已过会）、经济型与中端标准化连锁、非必要全服务会议型产品、'
           '以拓展带改造的对冲。')

H2 = '二、旅游度假型：资源进入方式与悦榕庄样板'
T2_HEAD = ['案例', '事实', '对安逸的启示']
T2 = [
 ['峨眉山悦榕庄', '2026 年 8 月 1 日开业，世界自然与文化双遗产地峨眉山麓，130 间客房全部配私享温泉泡池',
  '康养资源可做成全房型产品的标准配置，对应国堰 11 个汤池的改造方向；与安逸都江堰、峨眉山点位重叠，是竞争也是联动基础'],
 ['广州九龙湖悦榕庄', '147 间客房及套房，全客房配室内汤泉泡池',
  '汤池进客房是度假产品的差异化门槛，可作为旅游度假型的产品底线'],
 ['悦榕集团整体路径', '在华 38 家，2025 年入华二十周年；2026 年新开及将开峨眉山、广州九龙湖、仙居；'
  '2026 年 3 月完成品牌整合为 14 个品牌，推进向轻资产转型',
  '从自营度假村转为品牌与住宅分成输出给业主，与安逸"自有品牌加委托管理"方向一致而路径相反，可作对照'],
]
P2 = [
 '进入方式：保留自有品牌、只做委托管理，不挂牌外部品牌。挂牌要付品牌授权费与管理费，会员计入对方，品牌溢价归对方，等于永久让出该赛道。',
 '首期用零改造先托管：外部品牌方派驻团队、输出管理标准、开放会员与渠道，不动硬装，集团现金投入接近零，管理费与经营结果挂钩。这是抵押受限、经营利润薄、程序未定时唯一能立即启动的方式。',
 '合同必须写入五项：品牌归属、会员与数据归属、员工保留、退出与过渡期、排他与优先权。',
 '指标三条写入协议阶段目标，不写入运营团队考核表：资产市场估值、经营性利润与财务费用的距离、债转股审批进度。',
 '须同时提示：集团内部分析认为九寨沟悦榕庄经营不佳，国际品牌叠加优质目的地并不必然成功，借鉴其产品结构与标准，不简单对标。',
]

H3 = '三、存量改造：按步骤推进，每一步先出产品再放量'
T3_HEAD = ['步骤', '内容', '验证什么', '止损条件']
T3 = [
 ['第一步\n品牌文化先行\n＋可独立先行的隐蔽工程\n＋首批房间做透',
  '品牌重塑、文创与策展联营、基础信息化；外立面、结构与消防主体、屋面防水、设备机房与主干管线；'
  '首批客房与公共功能区域一次做透，含隐蔽与饰面',
  '品牌市场接受度、主题商品与联营营收、数据颗粒度是否建成、首批客房爬坡斜率',
  '六个月品牌咨询量未提升，或联营无营收，或数据颗粒度未建成，或首批客房出租率未突破 45%，不进第二步'],
 ['第二步\n拓展客房与园林',
  '第二批客房、公共区域深化、园林与庭院',
  '平均房价与出租率爬坡斜率、营业利润率改善幅度',
  '投后十二个月出租率未突破 45%，冻结追加，转做运营'],
 ['第三步\n剩余区域与运营深化',
  '餐饮、会议、康养场景与全店运营深化',
  '整体投资回报与回收期',
  '回收期超三年或五年红线，降档或退出'],
]
P3 = [
 '同一批空间内，隐蔽工程与饰面必须同批完成，不得先做隐蔽再分批饰面，否则开挖破坏；隐蔽工程可独立先行的，是后续不再进入的空间与部位。',
 '样板先行列为强制动作：先做样板客房并封样确认，再按样板验证过的做法与单价放量，单店不少于二十间，验证一个完整经营周期。',
 '每一步只放大上一步已验证的部分，未通过验证不得进入下一步。',
]

H4 = '四、数字化：三层体系、四个场景、四步实施'
P4 = [
 '三层：底座层全域统一、不随业态变化；系统模块层按业态选择装配，不做全量一套；输出层对外可售，把品牌标准、系统接口、会员体系与数据标准打包为轻资产交付物，与品牌授权、委托管理、输出管理三类合同模板绑定。',
 '四场景：收益管理、会议与客源、渠道与内容、经营诊断与预警。验收标准一律是业务指标，不是模型指标——收益管理看建议采纳率与实际房价提升，会议与客源看分账准确率与协议客户新增，渠道看内容产出效率与直销转化，诊断看预警命中与处置闭环率。',
 '四步：第一步统一口径，先不投系统（编制集团数据字典、统一市场细分码与主数据规则、政务科目单列；此步不花钱，不做则后面全部无效）；第二步单店基础信息化与贯通，上 PMS 单店版、直销与小程序、会员接口、中央预订、财务共享与业财一体；第三步集团级人工智能中台另立项，私有化部署与数据治理，四个场景按收益管理优先逐项上线；第四步对外输出，系统与标准打包为轻资产交付物。',
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


def build(fs=9.5, ls=12.5, top=1.3, bot=1.1, left=1.7, right=1.5, tf=8.5, tls=10.5):
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
    mktable(doc, T1_HEAD, T1, tf, tls, [2.8, 4.2, 4.6, 4.6])
    para(doc, T1_NOTE, fs, ls, '仿宋', False, True, 3)

    para(doc, H2, fs, ls, '黑体', True, False, 1, before=2)
    mktable(doc, T2_HEAD, T2, tf, tls, [2.9, 6.3, 7.0])
    for x in P2:
        para(doc, x, fs, ls, '仿宋', False, True, 1)

    para(doc, H3, fs, ls, '黑体', True, False, 1, before=2)
    mktable(doc, T3_HEAD, T3, tf, tls, [2.5, 4.5, 3.6, 4.6])
    for x in P3:
        para(doc, x, fs, ls, '仿宋', False, True, 1)

    para(doc, H4, fs, ls, '黑体', True, False, 1, before=2)
    for x in P4:
        para(doc, x, fs, ls, '仿宋', False, True, 1)

    doc.save(DX)


def pages():
    outdir = os.path.join(WS, 'tmp', '_pg4')
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


for cfg in [(10.0, 13.0, 1.4, 1.2, 1.8, 1.6, 9.0, 11),
            (9.5, 12.5, 1.3, 1.1, 1.7, 1.5, 8.5, 10.5),
            (9.0, 11.8, 1.2, 1.0, 1.6, 1.4, 8.0, 10),
            (8.5, 11.0, 1.1, 0.9, 1.5, 1.3, 7.5, 9.5)]:
    build(*cfg)
    pg = pages()
    print('正文%.1f/行距%.1f/表%.1f/%.1f -> 实测 %d 页' % (cfg[0], cfg[1], cfg[6], cfg[7], pg))
    if pg == 1:
        shutil.copy2(DX, os.path.join(DESK, NAME + '.docx'))
        print('  >>> 采用该版，%.1f KB' % (os.path.getsize(DX) / 1024))
        break
