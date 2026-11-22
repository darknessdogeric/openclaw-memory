"""
通用 Markdown → Word（非公文场景）
适合日常报告、PPT 演讲稿、技术文档、研究报告等。
不带 GB/T 9704 公文规范（那种用 gongwen-docx-cn）。

特点：
  - 中英文字体绑定（关键：eastAsia）
  - 支持代码块、表格、引用、列表
  - 段前段后间距合理
  - 无 emoji / 无装饰
  - 页边距 Word 默认
"""
import sys, io, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from docx import Document
from docx.shared import Pt, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BODY_FONT   = '等线'      # 正文
H1_FONT     = '等线'      # 一级
H2_FONT     = '等线'      # 二级
TITLE_FONT  = '等线'      # 标题
IND = Emu(403225)

def set_font(run, name, size):
    run.font.size = Pt(size)
    run.font.name = name
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts')
        rpr.append(rf)
    rf.set(qn('w:eastAsia'), name)
    rf.set(qn('w:ascii'), name)
    rf.set(qn('w:hAnsi'), name)

def add_para(doc, text, font=BODY_FONT, size=11,
             align=None, indent=True, sa=None, sb=None, bold=False):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    if align is not None:
        p.alignment = align
    if indent:
        pf.first_line_indent = IND
    if sa is not None:
        pf.space_after = sa
    if sb is not None:
        pf.space_before = sb
    run = p.add_run(text)
    run.bold = bold
    set_font(run, font, size)
    return p

def add_table(doc, rows, size=10):
    if not rows:
        return None
    ncol = max(len(r) for r in rows)
    t = doc.add_table(rows=0, cols=ncol)
    t.style = 'Table Grid'
    for ri, row in enumerate(rows):
        cells = t.add_row().cells
        for i, val in enumerate(row):
            if i < len(cells):
                cells[i].text = ''
                run = cells[i].paragraphs[0].add_run(str(val))
                run.bold = (ri == 0)
                set_font(run, BODY_FONT, size)
    add_para(doc, '')

def add_code_block(doc, lines, size=9):
    for b in lines:
        if not b.strip():
            continue
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.left_indent = IND
        pf.space_after = Emu(12700)
        pf.line_spacing = 1.15
        run = p.add_run(b)
        set_font(run, BODY_FONT, size)

RE_H1 = re.compile(r'^#{1}\s+(.+)$')
RE_H2 = re.compile(r'^##\s+(.+)$')
RE_H3 = re.compile(r'^###\s+(.+)$')
RE_H4 = re.compile(r'^####\s+(.+)$')
RE_HR = '---'
RE_TABLE = re.compile(r'^\|.*\|$')
RE_CODE = re.compile(r'^```')
RE_OL   = re.compile(r'^(\d+)[.)]\s+(.*)$')   # 编号列表（2026-11-18 并入）
RE_PB   = re.compile(r'^<!--\s*pagebreak\s*-->$', re.I)  # 分页标记（2026-11-18 并入）

def md_to_docx(src_md, dst_docx):
    with open(src_md, encoding='utf-8') as f:
        lines = [l.rstrip() for l in f.read().splitlines()]
    lines = [l for l in lines if l.strip()]
    doc = Document()
    i = 0
    n = len(lines)
    is_first = True
    while i < n:
        line = lines[i]
        s = line.strip()
        # 代码块
        if RE_CODE.match(s):
            i += 1
            buf = []
            while i < n and not RE_CODE.match(lines[i].strip()):
                buf.append(lines[i])
                i += 1
            i += 1
            add_code_block(doc, buf)
            add_para(doc, '')
            is_first = False
            continue
        # 表格
        if RE_TABLE.match(s):
            rows = []
            while i < n and RE_TABLE.match(lines[i].strip()):
                row = lines[i].strip()
                if re.match(r'^\|[\s\-:|]+\|$', row):
                    i += 1
                    continue
                rows.append([c.strip() for c in row.strip('|').split('|')])
                i += 1
            add_table(doc, rows)
            is_first = False
            continue
        # 分隔线
        if s == RE_HR:
            add_para(doc, '')
            i += 1
            is_first = False
            continue
        # 标题
        if is_first:
            add_para(doc, s, font=TITLE_FONT, size=20,
                     align=WD_ALIGN_PARAGRAPH.CENTER, indent=False, sa=Emu(101600))
            is_first = False
            i += 1
            continue
        m4 = RE_H4.match(s)
        if m4:
            add_para(doc, m4.group(1), font=BODY_FONT, size=11, bold=True)
            i += 1
            continue
        m3 = RE_H3.match(s)
        if m3:
            add_para(doc, m3.group(1), font=H2_FONT, size=12, bold=True)
            i += 1
            continue
        m2 = RE_H2.match(s)
        if m2:
            add_para(doc, m2.group(1), font=H1_FONT, size=14, bold=True)
            i += 1
            continue
        m1 = RE_H1.match(s)
        if m1:
            add_para(doc, m1.group(1), font=TITLE_FONT, size=16, bold=True)
            i += 1
            continue
        if s.startswith('>'):
            p = doc.add_paragraph()
            pf = p.paragraph_format
            pf.left_indent = IND
            run = p.add_run(s.lstrip('> ').strip())
            set_font(run, BODY_FONT, 10)
            i += 1
            continue
        m = re.match(r'^[-*]\s+(.*)', s)
        if m:
            add_para(doc, '• ' + m.group(1), font=BODY_FONT, size=11)
            i += 1
            continue
        txt = re.sub(r'\*\*(.+?)\*\*', r'\1', s)
        txt = re.sub(r'(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)', r'\1', txt)
        txt = re.sub(r'`(.+?)`', r'\1', txt)
        add_para(doc, txt, font=BODY_FONT, size=11)
        i += 1
    doc.save(dst_docx)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('用法: python md_to_docx.py <src.md> <dst.docx>')
        sys.exit(1)
    md_to_docx(sys.argv[1], sys.argv[2])
    print('OK', os.path.getsize(sys.argv[2]), 'bytes')
