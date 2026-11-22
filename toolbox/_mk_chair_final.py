# -*- coding: utf-8 -*-
"""最终版：公文范式汇报要点 —— 单次校准、状态干净、幂等"""
import io, sys, os, re, subprocess, shutil, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_LINE_SPACING, WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from collections import Counter

WS = r'D:\B166ER-openclaw\workspace'
DIR = r'C:\Users\ericz\Desktop\产业发展部\给董事长的单独汇报'
DESK = r'C:\Users\ericz\Desktop'
NAME = '2026-11-21_发展赛道与存量改造路径_汇报要点'
SRC = os.path.join(WS, 'tmp', '_chair_gongwen.md')
DX = os.path.join(DIR, NAME + '.docx')
CONV = os.path.join(WS, 'skills', 'gongwen-docx-cn', 'scripts', 'md2docx_gongwen.py')
SOFFICE = r'C:\Program Files\LibreOffice\program\soffice.com'

H1 = re.compile(r'^[一二三四五六七八九十]+、')
WIDTHS = [[2.6, 4.6, 3.7, 4.7], [2.5, 13.1], [2.8, 4.5, 3.2, 5.1]]


def set_font(run, ea, pt):
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = rpr.makeelement(qn('w:rFonts'), {})
        rpr.insert(0, rf)
    for a in ('w:ascii', 'w:hAnsi', 'w:eastAsia'):
        rf.set(qn(a), ea)
    run.font.size = Pt(pt)


def clear_runs(p):
    for r in list(p.runs):
        r._element.getparent().remove(r._element)


def build_once(tbl_pt=10.5, tbl_ls=13.0):
    """从 MD 重新转换并一次性校准 —— 无跨次状态"""
    r = subprocess.run([sys.executable, CONV, SRC, DX], capture_output=True, text=True, encoding='utf-8', errors='replace')
    d = Document(DX)
    title_done = False
    for p in d.paragraphs:
        tx = p.text.strip()
        if not tx:
            continue
        pf = p.paragraph_format
        pf.line_spacing = Pt(28)
        pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        pf.space_after = Pt(0)
        pf.space_before = Pt(0)
        if not title_done:
            title_done = True
            for rr in p.runs:
                set_font(rr, '方正小标宋简体', 22)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            pf.first_line_indent = None
            pf.space_after = Pt(6)
            continue
        if tx in ('呈：集团董事长', '拟：产业发展部', '时间：2026 年 11 月 21 日'):
            for rr in p.runs:
                set_font(rr, '仿宋', 16)
            pf.first_line_indent = None
            continue
        if H1.match(tx):
            for rr in p.runs:
                set_font(rr, '黑体', 16)
            pf.first_line_indent = Pt(32)
            pf.space_before = Pt(8)
            pf.space_after = Pt(2)
            continue
        if tx.startswith('安逸酒店集团产业发展部') or re.match(r'^2026\s*年\s*11\s*月\s*21\s*日$', tx):
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            pf.first_line_indent = None
            for rr in p.runs:
                set_font(rr, '仿宋', 16)
            continue
        if '‖' in tx:
            head, tail = tx.split('‖', 1)
            clear_runs(p)
            set_font(p.add_run(head), '楷体', 16)
            set_font(p.add_run(tail), '仿宋', 16)
        else:
            for rr in p.runs:
                set_font(rr, '仿宋', 16)
        pf.first_line_indent = Pt(32)
    for ti, tb in enumerate(d.tables):
        for ri, row in enumerate(tb.rows):
            for ci, cell in enumerate(row.cells):
                if ci < len(WIDTHS[ti]):
                    cell.width = Cm(WIDTHS[ti][ci])
                for p in cell.paragraphs:
                    p.paragraph_format.line_spacing = Pt(tbl_ls)
                    p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.EXACTLY
                    p.paragraph_format.space_after = Pt(0)
                    p.paragraph_format.first_line_indent = None
                    for rr in p.runs:
                        set_font(rr, '黑体' if ri == 0 else '仿宋', tbl_pt)
    d.save(DX)


def pages():
    outdir = os.path.join(WS, 'tmp', '_pgf')
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


for tp, tls in ((10.5, 13.0), (10.0, 12.0)):
    build_once(tp, tls)
    pg = pages()
    print('表%.1fpt/%.1f -> 实测 %d 页' % (tp, tls, pg))
    if pg <= 3:
        break

d = Document(DX)
c = Counter()
for p in d.paragraphs:
    for rr in p.runs:
        if not rr.text.strip():
            continue
        rpr = rr._element.find(qn('w:rPr'))
        ea = sz = None
        if rpr is not None:
            f = rpr.find(qn('w:rFonts'))
            if f is not None:
                ea = f.get(qn('w:eastAsia'))
            s2 = rpr.find(qn('w:sz'))
            if s2 is not None:
                sz = int(s2.get(qn('w:val'))) / 2.0
        c[(ea, sz)] += 1
s = d.sections[0]
print('')
print('页边距 上%.2f 下%.2f 左%.2f 右%.2f cm' % (s.top_margin.cm, s.bottom_margin.cm, s.left_margin.cm, s.right_margin.cm))
print('字体: ' + ' | '.join('%s/%s x%d' % (k[0], k[1], v) for k, v in c.most_common(8)))
full = '\n'.join(p.text for p in d.paragraphs)
print('‖ 残留: %d   段落 %d  表格 %d  大小 %.1f KB' % (full.count('‖'), len(d.paragraphs), len(d.tables), os.path.getsize(DX) / 1024))
print('')
print('=== 段落字体核对 ===')
for i, p in enumerate(d.paragraphs[:16]):
    tx = p.text.strip()
    if not tx:
        continue
    fs = []
    for rr in p.runs:
        if not rr.text.strip():
            continue
        rpr = rr._element.find(qn('w:rPr'))
        ea = None
        if rpr is not None:
            f = rpr.find(qn('w:rFonts'))
            if f is not None:
                ea = f.get(qn('w:eastAsia'))
        fs.append('%s「%s」' % (ea, rr.text[:16]))
    print('  P%-2d %s' % (i, ' + '.join(fs)[:140]))
shutil.copy2(DX, os.path.join(DESK, NAME + '.docx'))
print('')
print('桌面副本已同步')
