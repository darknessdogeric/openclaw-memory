# -*- coding: utf-8 -*-
import io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.shared import Pt, Cm, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SRC = r'D:\B166ER-openclaw\workspace\tmp\_mt_proto.txt'
OUT = r'C:\Users\ericz\Desktop\安逸酒店集团与美团合作框架协议_起草稿_20261029.docx'
KBD = r'D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\美团充电宝会员跳转合作'

IND = Emu(406400)
SB1 = Emu(127000)
FONT_BODY = '仿宋_GB2312'
FONT_H = '黑体'

def setfont(run, name, size, bold=None):
    run.font.size = Pt(size)
    run.font.name = name
    if bold is not None:
        run.bold = bold
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts'); rpr.append(rf)
    rf.set(qn('w:eastAsia'), name); rf.set(qn('w:ascii'), 'Times New Roman'); rf.set(qn('w:hAnsi'), 'Times New Roman')

d = Document()
s = d.sections[0]
s.top_margin = Cm(3.7); s.bottom_margin = Cm(3.5); s.left_margin = Cm(2.8); s.right_margin = Cm(2.6)

def add(text, font=FONT_BODY, size=16, bold=False, align=None, indent=True, sb=None):
    p = d.add_paragraph()
    pf = p.paragraph_format
    if align is not None:
        p.alignment = align
    if indent:
        pf.first_line_indent = IND
    if sb is not None:
        pf.space_before = sb
    pf.line_spacing = 1.5
    r = p.add_run(text); setfont(r, font, size, bold)
    return p

def table(rows):
    n = max(len(x.split('|')) for x in rows)
    t = d.add_table(rows=0, cols=n); t.style = 'Table Grid'
    for ri, row in enumerate(rows):
        cells = t.add_row().cells
        for i, v in enumerate(row.split('|')):
            if i < len(cells):
                cells[i].text = ''
                r = cells[i].paragraphs[0].add_run(v.strip())
                r.bold = (ri == 0)
                setfont(r, FONT_BODY, 11)
    return t

lines = open(SRC, encoding='utf-8').read().split(chr(10))
i = 0; n = len(lines)
while i < n:
    ln = lines[i].rstrip()
    if not ln.strip():
        i += 1; continue
    body = ln[1:] if ln.startswith('^') else ln
    if body.startswith('TR'):
        rows = [body[2:]]
        i += 1
        while i < n and lines[i].startswith('^TR'):
            rows.append(lines[i][3:]); i += 1
        table(rows)
        continue
    if body.startswith('TB'):
        rows = [body[2:]]
        i += 1
        while i < n and lines[i].startswith('^TR'):
            rows.append(lines[i][3:]); i += 1
        table(rows)
        continue
    tag = body[0]
    rest = body[1:]
    if tag == 'T':
        add(rest, font=FONT_H, size=22, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, indent=False)
    elif tag == 'H':
        add(rest, font=FONT_H, size=16, bold=True, sb=SB1)
    elif tag == 'B':
        add(rest)
    elif tag == 'N':
        add(rest, indent=False)
    else:
        add(rest, indent=False)
    i += 1

os.makedirs(KBD, exist_ok=True)
d.save(OUT)
print('OK %d bytes -> %s' % (os.path.getsize(OUT), OUT))

d2 = Document(OUT)
f = ''.join(x.text for x in d2.paragraphs) + chr(10) + ''.join(cl.text for tb in d2.tables for rr in tb.rows for cl in rr.cells)
print('段落 %d  表格 %d  字数 %d' % (len(d2.paragraphs), len(d2.tables), len(f)))
for k in ['合作框架协议','91510100MA7DERN160','一、拟合作内容','二、商业秘密','三、数据与会员','四、协议期限','五、收费','六、联合工作小组与争议解决','七、其他','以下无正文','附件一','1小时、2小时','1至3个月','业务合作方授权与责任','约60家','原告所在地人民法院']:
    print('  %-24s %s' % (k, 'OK' if k in f else 'MISSING'))