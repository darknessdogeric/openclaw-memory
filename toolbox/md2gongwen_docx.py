# -*- coding: utf-8 -*-
"""md -> 公文范式 docx (GB/T 9704-2012 风格)
参照 toolbox/_mk_mt_docx.py 排版参数：
  标题 方正小标宋简体 二号 居中；一级标题 黑体 三号；二级 楷体_GB2312 三号；
  正文 仿宋_GB2312 三号 首行缩进2字符 行距1.5；表格 Table Grid 仿宋 小四 表头加粗；
  页边距 上3.7 下3.5 左2.8 右2.6 cm
"""
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.shared import Pt, Cm, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

SRC = sys.argv[1]
OUT = sys.argv[2]
BT = chr(96)
DATE_DEFAULT = '2026年10月30日'
DOC_DATE = sys.argv[3] if len(sys.argv) > 3 else DATE_DEFAULT

IND = Emu(406400)
SB1 = Emu(127000)
F_TITLE = '方正小标宋简体'
F_H1 = '黑体'
F_H2 = '楷体_GB2312'
F_BODY = '仿宋_GB2312'

def setfont(run, name, size, bold=None):
    run.font.size = Pt(size)
    run.font.name = name
    if bold is not None:
        run.bold = bold
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts'); rpr.append(rf)
    rf.set(qn('w:eastAsia'), name)
    rf.set(qn('w:ascii'), 'Times New Roman')
    rf.set(qn('w:hAnsi'), 'Times New Roman')

def clean(s):
    s = re.sub(r'\*\*(.+?)\*\*', r'\1', s)
    s = re.sub(BT + r'(.+?)' + BT, r'\1', s)
    s = s.replace('**', '').replace('~~', '')
    s = s.strip().strip('*').strip()
    return s

raw = open(SRC, encoding='utf-8').read()
lines = raw.split('\n')

title = ''
for i, ln in enumerate(lines):
    if ln.strip():
        cand = ln.strip()
        if cand.startswith('# '):
            cand = cand[2:]
        title = clean(cand)
        lines[i] = ''
        break

items = []
i = 0
n = len(lines)
while i < n:
    ln = lines[i].rstrip()
    s = ln.strip()
    if not s:
        i += 1; continue
    if s.startswith('|'):
        rows = []
        while i < n and lines[i].strip().startswith('|'):
            cells = [c.strip() for c in lines[i].strip().strip('|').split('|')]
            if not all(re.fullmatch(r':?-{2,}:?', c or '') for c in cells):
                rows.append([clean(c) for c in cells])
            i += 1
        items.append(('TBL', rows))
        continue
    if re.fullmatch(r'-{3,}', s):
        i += 1; continue
    if s.startswith('>'):
        buf = []
        while i < n and lines[i].strip().startswith('>'):
            buf.append(clean(lines[i].strip().lstrip('>')))
            i += 1
        items.append(('QUOTE', ' '.join(x for x in buf if x)))
        continue
    if s.startswith('### '):
        items.append(('H3', clean(s[4:]))); i += 1; continue
    if s.startswith('## '):
        items.append(('H2', clean(s[3:]))); i += 1; continue
    if s.startswith('# '):
        items.append(('H1', clean(s[2:]))); i += 1; continue
    if re.match(r'^\*\*(用途|编制|时间|配套)\*\*', s):
        i += 1; continue
    items.append(('P', clean(s)))
    i += 1

d = Document()
s = d.sections[0]
s.top_margin = Cm(3.7); s.bottom_margin = Cm(3.5)
s.left_margin = Cm(2.8); s.right_margin = Cm(2.6)

def add(text, font=F_BODY, size=16, bold=False, align=None, indent=True, sb=None, spacing=1.5):
    p = d.add_paragraph()
    pf = p.paragraph_format
    if align is not None:
        p.alignment = align
    if indent:
        pf.first_line_indent = IND
    if sb is not None:
        pf.space_before = sb
    pf.line_spacing = spacing
    r = p.add_run(text)
    setfont(r, font, size, bold)
    return p

def add_table(rows):
    if not rows: return
    n = max(len(r) for r in rows)
    t = d.add_table(rows=0, cols=n)
    t.style = 'Table Grid'
    for ri, row in enumerate(rows):
        cells = t.add_row().cells
        for i2 in range(n):
            v = row[i2] if i2 < len(row) else ''
            cells[i2].text = ''
            r = cells[i2].paragraphs[0].add_run(v)
            r.bold = (ri == 0)
            setfont(r, F_BODY, 11)
            cells[i2].paragraphs[0].paragraph_format.line_spacing = 1.0
    d.add_paragraph()

# 标题
add(title, font=F_TITLE, size=22, align=WD_ALIGN_PARAGRAPH.CENTER, indent=False, spacing=1.5)
add('', font=F_BODY, size=8, indent=False)
# 抬头（右对齐）
for h in ['呈：安逸酒店集团产业发展部与四川蒙顶山茶业有限公司二销业务对接机制',
          '拟：安逸酒店集团产业发展部',
          '时间：' + DOC_DATE]:
    add(h, font=F_BODY, size=16, align=WD_ALIGN_PARAGRAPH.RIGHT, indent=False)
add('', font=F_BODY, size=16, indent=False)
# 正文
for kind, val in items:
    if kind == 'TBL':
        add_table(val)
    elif kind == 'QUOTE':
        add(val, font=F_H2, size=14, indent=True)
    elif kind == 'H1':
        add(val, font=F_H1, size=16, bold=True, indent=True, sb=SB1)
    elif kind == 'H2':
        add(val, font=F_H2, size=16, bold=True, indent=True, sb=SB1)
    elif kind == 'H3':
        add(val, font=F_BODY, size=16, bold=True, indent=True, sb=SB1)
    else:
        add(val, font=F_BODY, size=16, indent=True)
# 落款（右对齐）
add('', font=F_BODY, size=16, indent=False)
for h in ['安逸酒店集团有限责任公司产业发展部', DOC_DATE]:
    add(h, font=F_BODY, size=16, align=WD_ALIGN_PARAGRAPH.RIGHT, indent=False)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
d.save(OUT)
print('OK %d bytes -> %s' % (os.path.getsize(OUT), OUT))
d2 = Document(OUT)
f = ''.join(x.text for x in d2.paragraphs) + chr(10) + ''.join(cl.text for tb in d2.tables for rr in tb.rows for cl in rr.cells)
print('段落 %d  表格 %d  字数 %d' % (len(d2.paragraphs), len(d2.tables), len(f)))
print('首段:', d2.paragraphs[0].text[:44])
print('末3段:', [x.text[:26] for x in d2.paragraphs[-3:]])
for k in ['董事长','郭涛','刘维','邹士勇','专班','存量改造','# ']:
    print('  %-8s %s' % (k, 'HIT' if k in f else 'clean'))
