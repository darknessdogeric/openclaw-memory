# -*- coding: utf-8 -*-
"""公文范式：转换 + 版式校准 + 页数实测"""
import io, sys, os, re, subprocess, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_LINE_SPACING, WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from collections import Counter

WS = r'D:\B166ER-openclaw\workspace'
DIR = r'C:\Users\ericz\Desktop\产业发展部\给董事长的单独汇报'
NAME = '2026-11-21_发展赛道与存量改造路径_汇报要点'
SRC = os.path.join(WS, 'tmp', '_chair_gongwen.md')
DX = os.path.join(DIR, NAME + '.docx')
CONV = os.path.join(WS, 'skills', 'gongwen-docx-cn', 'scripts', 'md2docx_gongwen.py')
SOFFICE = r'C:\Program Files\LibreOffice\program\soffice.com'


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


H1 = re.compile(r'^[一二三四五六七八九十]+、')
H2 = re.compile(r'^（[一二三四五六七八九十]+）')


def calibrate(path):
    d = Document(path)
    n = t1 = h1 = h2 = fz = sg = 0
    first = True
    for p in d.paragraphs:
        tx = p.text.strip()
        if not tx:
            continue
        pf = p.paragraph_format
        pf.line_spacing = Pt(28)
        pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        pf.space_after = Pt(0)
        n += 1
        if first:
            first = False
            for r in p.runs:
                set_font(r, '方正小标宋简体', 22)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            pf.first_line_indent = None
            pf.space_after = Pt(6)
            t1 += 1
            continue
        if tx in ('呈：集团董事长', '拟：产业发展部', '时间：2026 年 11 月 21 日'):
            for r in p.runs:
                set_font(r, '仿宋', 16)
            pf.first_line_indent = None
            pf.space_after = Pt(0)
            continue
        if H1.match(tx):
            for r in p.runs:
                set_font(r, '黑体', 16)
            pf.first_line_indent = Pt(32)
            pf.space_before = Pt(6)
            h1 += 1
            continue
        if H2.match(tx):
            for r in p.runs:
                set_font(r, '楷体', 16)
            pf.first_line_indent = Pt(32)
            h2 += 1
            continue
        if tx.startswith('安逸酒店集团产业发展部') or re.match(r'^2026\s*年\s*11\s*月\s*21\s*日$', tx):
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            pf.first_line_indent = None
            for r in p.runs:
                set_font(r, '仿宋', 16)
            sg += 1
            continue
        for r in p.runs:
            set_font(r, '仿宋', 16)
        pf.first_line_indent = Pt(32)
        fz += 1
    # 表格：小四
    for tb in d.tables:
        for ri, row in enumerate(tb.rows):
            for cell in row.cells:
                for p in cell.paragraphs:
                    p.paragraph_format.line_spacing = Pt(16)
                    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
                    p.paragraph_format.space_after = Pt(0)
                    for r in p.runs:
                        set_font(r, '黑体' if ri == 0 else '仿宋', 12, ri == 0)
    d.save(path)
    return n, t1, h1, h2, fz, sg


def pages():
    outdir = os.path.join(WS, 'tmp', '_pg6')
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


r = subprocess.run([sys.executable, CONV, SRC, DX], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('公文转换:', (r.stdout or '').strip(), (r.stderr or '').strip()[:150])
n, t1, h1, h2, fz, sg = calibrate(DX)
print('段落 %d / 标题 %d / 一级黑体 %d / 二级楷体 %d / 正文 %d / 落款 %d' % (n, t1, h1, h2, fz, sg))
pg = pages()
print('实测页数: %d' % pg)

d = Document(DX)
s = d.sections[0]
print('页边距 上%.2f 下%.2f 左%.2f 右%.2f cm' % (s.top_margin.cm, s.bottom_margin.cm, s.left_margin.cm, s.right_margin.cm))
c = Counter()
for p in d.paragraphs:
    for r in p.runs:
        if not r.text.strip():
            continue
        rpr = r._element.find(qn('w:rPr'))
        ea = sz = None
        if rpr is not None:
            f = rpr.find(qn('w:rFonts'))
            if f is not None:
                ea = f.get(qn('w:eastAsia'))
            s2 = rpr.find(qn('w:sz'))
            if s2 is not None:
                sz = int(s2.get(qn('w:val'))) / 2.0
        c[(ea, sz)] += 1
print('字体: ' + ' | '.join('%s/%s x%d' % (k[0], k[1], v) for k, v in c.most_common(8)))
print('大小 %.1f KB' % (os.path.getsize(DX) / 1024))
shutil.copy2(DX, os.path.join(r'C:\Users\ericz\Desktop', NAME + '.docx'))
print('桌面副本已同步')
