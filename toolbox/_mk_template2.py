# -*- coding: utf-8 -*-
import io, sys, os, re, copy, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.shared import Pt, Cm, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.text import WD_BREAK
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SRC = r'C:\Users\ericz\Desktop\产业发展部\项目\美团本地生活\安逸集团&美团充电宝战略合作框架协议_20261106.docx'
DESK_IND = r'C:\Users\ericz\Desktop\产业发展部'
PROJ = r'C:\Users\ericz\Desktop\产业发展部\项目\美团本地生活'
KB_LIB = r'D:\B166ER-openclaw\workspace\anyi\anyi-ops-kb\11_合作资源库'
OUT_NAME = '战略合作框架协议_通用模板_v1.1_20261106.docx'

FONT_BODY = '仿宋_GB2312'
FONT_H = '黑体'
FONT_TITLE = '方正小标宋简体'
IND = Emu(406400)
SB1 = Emu(127000)

# ---------- 步骤1：清洗 Word 列表残渣 ----------
d = Document(SRC)
print('=== 清洗前 ===')
junk = 0
for p in d.paragraphs:
    t = p.text
    if re.match(r'^\s*B\s+\S', t) or re.match(r'^\s*\d+\s+[一二三四五六七八九十]+、', t):
        junk += 1
print('  带残渣段落数:', junk)

for p in d.paragraphs:
    for r in p.runs:
        t = r.text
        nt = re.sub(r'^(\s*)B\s+', r'\1', t)
        nt = re.sub(r'^(\s*)\d+\s+(?=[一二三四五六七八九十]+、)', r'\1', nt)
        if nt != t:
            r.text = nt

print('=== 清洗后残留 ===')
left = 0
for i, p in enumerate(d.paragraphs):
    t = p.text
    if re.match(r'^\s*B\s+\S', t) or re.match(r'^\s*\d+\s+[一二三四五六七八九十]+、', t):
        left += 1
        print('  p%d: %s' % (i, t[:70]))
print('  残留:', left)

# ---------- 步骤2：Eric 的 90:10 条款 → 通用占位符 ----------
SHARE_OLD = ('4. 收益分配比例。双方确认，乙方与甲方旗下酒店合作的本项目充电宝租赁业务税前净营收按照酒店方90%、乙方10%的比例进行分配，'
              '该比例为通行最终结算比例，无特殊情形不得变更。')
SHARE_NEW = ('4．收益分配比例。双方确认，乙方与甲方旗下酒店合作的本项目充电宝租赁业务税前净营收按照酒店方【甲方分成比例】、'
             '乙方【乙方分成比例】的比例进行分配，该比例为通行最终结算比例，无特殊情形不得变更。')
swap = 0
for p in d.paragraphs:
    if p.text.strip().replace(' ', '') == SHARE_OLD.replace(' ', ''):
        for r in list(p.runs)[1:]:
            r._element.getparent().remove(r._element)
        p.runs[0].text = SHARE_NEW
        swap += 1
print()
print('收益分配条款转占位符:', swap, '处')

# ---------- 步骤3：去品牌化 ----------
REPL = [
    ('安逸酒店集团有限责任公司与天津三快信息技术有限公司', '【甲方全称】与【乙方全称】'),
    ('安逸酒店集团有限责任公司', '【甲方全称】'),
    ('天津三快信息技术有限公司', '【乙方全称】'),
    ('91510100MA7DERN160', '【甲方统一社会信用代码】'),
    ('四川省成都市锦江区横丁字街15号', '【甲方地址】'),
    ('四川省旅游投资集团旗下酒店板块专业运营主体', '【集团名称】旗下【业务板块】专业运营主体'),
    ('美团旗下本地生活服务平台运营主体', '【平台名称】旗下【业务条线】运营主体'),
    ('“安逸会”会员体系', '“【会员体系名称】”会员体系'),
    ('安逸会', '【会员体系名称】'),
    ('美团', '【平台名称】'),
    ('三快', '【乙方全称】'),
]
for p in d.paragraphs:
    for r in p.runs:
        t = r.text
        nt = t
        for a, b in REPL:
            nt = nt.replace(a, b)
        if nt != t:
            r.text = nt
    full = p.text
    if any(a in full for a, b in REPL):
        nt = full
        for a, b in REPL:
            nt = nt.replace(a, b)
        for r in list(p.runs)[1:]:
            r._element.getparent().remove(r._element)
        p.runs[0].text = nt

# 标题加"（模板）"
for p in d.paragraphs:
    if p.text.strip().endswith('共享充电宝战略合作框架协议'):
        for r in p.runs:
            r.text = r.text.replace('共享充电宝战略合作框架协议', '共享充电宝战略合作框架协议（模板）')
        break

# ---------- 步骤4：前置使用说明页 ----------
GUIDE = [
    ('T', '战略合作框架协议 · 模板使用说明'),
    ('N', '（本页为内部填写指引，不构成协议内容。定稿签署前请整页删除。）'),
    ('P', ''),
    ('H', '一、模板定位'),
    ('B', '本模板适用于【集团名称】二级公司作为战略合作方，与平台方或其指定的业务统筹方签署顶层战略合作框架协议，适用于共享充电宝等本地生活场景合作。'),
    ('B', '正文条款结构、序号与措辞与集团级共享充电宝战略合作框架协议合并稿（2026-11-06）一致，仅将主体标识替换为占位符，并保留甲方在合并稿上的修订意见。'),
    ('H', '二、填写须知（占位符对照）'),
    ('B', '全文占位符以 Word 查找替换一次性替换即可：'),
    ('TBL', '占位符|填写内容|取数来源'),
    ('TBL', '【甲方全称】|签约主体工商全称|营业执照 / 公司章程'),
    ('TBL', '【甲方统一社会信用代码】|18 位统一社会信用代码|营业执照'),
    ('TBL', '【甲方地址】|营业执照登记住所|营业执照'),
    ('TBL', '【甲方法定代表人】|登记法定代表人|营业执照'),
    ('TBL', '【乙方全称】|签约对方全称（通常为业务实际运营主体）|营业执照'),
    ('TBL', '【乙方统一社会信用代码】/【乙方地址】/【乙方法定代表人】|同上|营业执照'),
    ('TBL', '【集团名称】/【业务板块】/【会员体系名称】/【平台名称】/【业务条线】|集团、板块、会员体系与对方品牌称谓|集团口径与对方主体介绍'),
    ('TBL', '【甲方分成比例】/【乙方分成比例】|收益分配比例（仅在确需于框架层约定时填写）|商务确定'),
    ('H', '三、四条不得突破的底线'),
    ('B', '1．不得写入排他条款。框架协议不得约定甲方不得与其他第三方开展同类合作，不得出现"独家""排他""不再与第三方合作"等表述。对方提出排他诉求一律拒绝，改为对等口径的优先合作表述。'),
    ('B', '2．框架层不写落地细则。设备规格与参数、点位数量与位置、会员权益档位与核销、运维服务等级与响应时限、数据口径与结算周期，全部下沉到第二层《专项执行合同》——由乙方合作商与甲方对应三级子公司一对一签署。框架协议只写"提供哪一类资源"，并在条款末尾注明具体内容由专项执行合同约定。'),
    ('B', '3．收益分配比例与框架性质条款不得打架。模板第一条保留了可选的"收益分配比例"条款，但第一条第 5 款与第五条第 1 款同时声明"框架协议不约定收益分成"。二选一：要么删除第一条第 4 款、把比例下沉到第二层（更稳妥）；要么保留并同步修改上述两处口径。切勿原样照用同一份文本。'),
    ('B', '4．甲方是二级公司，不是酒店本身。各酒店与三级公司为独立法人，框架层甲方只能承担统筹协调、提供品牌与会员体系数据接口授权、品牌视觉确认等集团层义务，不得替下属酒店承诺点位数量、结算金额与收益。'),
    ('H', '四、定稿前自检清单'),
    ('B', '1．全文检索"排他""独家""不再与""不得与其他"，结果必须为零。'),
    ('B', '2．全文检索甲乙双方具体主体名称、信用代码、地址，确认已全部替换为占位符或已填实。'),
    ('B', '3．确认首部乙方为业务实际运营主体（能独立承担义务与履约责任者），而非无独立法人资格的分支机构或业务部门。'),
    ('B', '4．确认协议期限年限与续展机制，并填入起止日期。'),
    ('B', '5．确认合作协议门店清单的确认主体与流程（框架层以甲方确认的清单为准）。'),
    ('B', '6．确认争议解决管辖地为甲方所在地。'),
    ('B', '7．核对第一条第 4 款（收益分配）与第一条第 5 款、第五条第 1 款的口径是否自洽。'),
    ('H', '五、版本'),
    ('B', '模板版本：v1.1 · 2026-11-06 · B166ER 编制。来源：集团级共享充电宝战略合作框架协议合并稿（2026-11-06），含甲方修订意见。'),
]


def setfont(run, name, size, bold=None):
    run.font.size = Pt(size)
    run.font.name = name
    if bold is not None:
        run.bold = bold
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts')
        rpr.append(rf)
    rf.set(qn('w:eastAsia'), name)
    rf.set(qn('w:ascii'), 'Times New Roman')
    rf.set(qn('w:hAnsi'), 'Times New Roman')


guide_els = []
tbl_rows = []


def mk_guide(text, font=FONT_BODY, size=16, bold=False, align=None, indent=True, sb=None):
    p = d.add_paragraph()
    pf = p.paragraph_format
    if align is not None:
        p.alignment = align
    if indent:
        pf.first_line_indent = IND
    if sb is not None:
        pf.space_before = sb
    pf.line_spacing = 1.5
    r = p.add_run(text)
    setfont(r, font, size, bold)
    guide_els.append(p._p)
    return p


for tag, text in GUIDE:
    if tag == 'P':
        mk_guide('')
    elif tag == 'T':
        mk_guide(text, font=FONT_TITLE, size=22, align=WD_ALIGN_PARAGRAPH.CENTER, indent=False)
    elif tag == 'H':
        mk_guide(text, font=FONT_H, size=16, bold=True, sb=SB1)
    elif tag == 'B':
        mk_guide(text)
    elif tag == 'N':
        mk_guide(text, indent=False)
    elif tag == 'TBL':
        tbl_rows.append(text)

t = d.add_table(rows=0, cols=3)
t.style = 'Table Grid'
for ri, row in enumerate(tbl_rows):
    cells = t.add_row().cells
    for ci, v in enumerate(row.split('|')):
        cells[ci].text = ''
        r = cells[ci].paragraphs[0].add_run(v.strip())
        r.bold = (ri == 0)
        setfont(r, FONT_BODY, 11)
guide_els.append(t._tbl)

pb = d.add_paragraph()
pb.add_run().add_break(WD_BREAK.PAGE)
guide_els.append(pb._p)

body = d.element.body
for el in reversed(guide_els):
    body.remove(el)
    body.insert(0, el)

STAGE = r'D:\B166ER-openclaw\workspace\tmp\_tpl2_stage.docx'
os.makedirs(os.path.dirname(STAGE), exist_ok=True)
d.save(STAGE)
print()
print('saved %d bytes' % os.path.getsize(STAGE))

for o in [os.path.join(DESK_IND, OUT_NAME), os.path.join(PROJ, OUT_NAME), os.path.join(KB_LIB, OUT_NAME)]:
    os.makedirs(os.path.dirname(o), exist_ok=True)
    try:
        shutil.copy2(STAGE, o)
        print('copied -> %s' % o)
    except PermissionError as e:
        print('LOCKED -> %s (%s)' % (o, e))

# ---------- 校验 ----------
d2 = Document(STAGE)
f = ''.join(x.text for x in d2.paragraphs)
f += ''.join(c.text for tb in d2.tables for rr in tb.rows for c in rr.cells)
print()
print('段落 %d  表格 %d  字数 %d' % (len(d2.paragraphs), len(d2.tables), len(f)))
bad = 0
for w in ['美团', '三快', '安逸', '91510100MA7DERN160', '横丁字街', '锦江区',
          '四川省旅游投资集团', '天津', '90%', '10%', '唯一实际执行主体',
          '无正当理由不得无故终止']:
    if w in f:
        bad += 1
        print('  [应无] %-24s *** 仍存在 ***' % w)
for k in ['【甲方全称】', '【乙方全称】', '【甲方分成比例】', '【乙方分成比例】',
          '【平台名称】', '【业务条线】', '【集团名称】', '【业务板块】', '【会员体系名称】',
          '模板使用说明', '不得写入排他条款', '框架层不写落地细则',
          '收益分配比例与框架性质条款不得打架', '甲方是二级公司，不是酒店本身',
          '积分兑换权益', '甲方授权并提供用于充电宝箱体的标识纹样',
          '品牌授权，会员体系数据接口授权', '本框架协议合作期限：3年',
          '第四条 数据与会员', '提交甲方所在地人民法院诉讼解决']:
    if k not in f:
        bad += 1
        print('  [应有] %-24s *** 缺失 ***' % k)
# 残渣
for k in ['B 甲方', 'B 乙方', 'B 统一', 'B 地址', 'B 联系', 'B 法定', 'B 日期', '2 一、', '2 二、']:
    if k in f:
        bad += 1
        print('  [残渣] %-24s *** 仍存在 ***' % k)
print('  FAIL COUNT =', bad)
