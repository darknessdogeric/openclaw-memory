# -*- coding: utf-8 -*-
"""公文范式 v3：二级标题短语与正文同段（楷体+仿宋）"""
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


def set_font(run, ea, pt, bold=False):
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = rpr.makeelement(qn('w:rFonts'), {})
        rpr.insert(0, rf)
    for a in ('w:ascii', 'w:hAnsi', 'w:eastAsia'):
        rf.set(qn(a), ea)
    run.font.size = Pt(pt)
    run.font.bold = bold


H1 = re.compile(r'^[一二三四五六七八九十]+、')
WIDTHS = [[2.6, 4.6, 3.7, 4.7], [2.5, 13.1], [2.8, 4.5, 3.2, 5.1]]


def clear_runs(p):
    for r in list(p.runs):
        r._element.getparent().remove(r._element)


def calibrate(path, tbl_pt=10.5, tbl_ls=13.0):
    d = Document(path)
    n = t1 = h1 = body = sg = 0
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
            continue
        if H1.match(tx):
            for r in p.runs:
                set_font(r, '黑体', 16)
            pf.first_line_indent = Pt(32)
            pf.space_before = Pt(8)
            pf.space_after = Pt(2)
            h1 += 1
            continue
        if tx.startswith('安逸酒店集团产业发展部') or re.match(r'^2026\s*年\s*11\s*月\s*21\s*日$', tx):
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            pf.first_line_indent = None
            for r in p.runs:
                set_font(r, '仿宋', 16)
            sg += 1
            continue
        # 二级标题短语（楷体）＋正文（仿宋）同段 —— 幂等：按文本模式判定
        if '‖' in tx:
            head, tail = tx.split('‖', 1)
            clear_runs(p)
            set_font(p.add_run(head), '楷体', 16)
            set_font(p.add_run(tail), '仿宋', 16)
        else:
            rs = [r for r in p.runs if r.text.strip()]
            is_sub = bool(re.match(r'^（[一二三四五六七八九十]+）', tx)) and len(rs) >= 2
            if is_sub:
                first = rs[0].text.strip()
                if first.endswith('。') and len(first) <= 40:
                    set_font(rs[0], '楷体', 16)
                    for r in rs[1:]:
                        set_font(r, '仿宋', 16)
                else:
                    for r in rs:
                        set_font(r, '仿宋', 16)
            else:
                for r in rs:
                    set_font(r, '仿宋', 16)
        pf.first_line_indent = Pt(32)
        body += 1
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
                    for r in p.runs:
                        set_font(r, '黑体' if ri == 0 else '仿宋', tbl_pt, ri == 0)
    d.save(path)
    return n, t1, h1, body, sg


def pages():
    outdir = os.path.join(WS, 'tmp', '_pg8')
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
print('公文转换:', (r.stdout or '').strip(), (r.stderr or '').strip()[:120])
best = None
for tp, tls in ((10.5, 13.0), (10.0, 12.0), (9.5, 11.5)):
    n, t1, h1, body, sg = calibrate(DX, tp, tls)
    pg = pages()
    print('表%.1fpt/%.1f -> 段落%d 标题%d 一级%d 正文%d 落款%d | 实测 %d 页' % (tp, tls, n, t1, h1, body, sg, pg))
    if best is None or pg < best[0]:
        best = (pg, tp, tls)
    if pg <= 2:
        break
pg, tp, tls = best
if (tp, tls) != (10.5, 13.0):
    calibrate(DX, tp, tls)
    pg = pages()
print('>>> 采用 表%.1fpt/行距%.1f，实测 %d 页' % (tp, tls, pg))

d = Document(DX)
s = d.sections[0]
print('')
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
print('字体: ' + ' | '.join('%s/%s x%d' % (k[0], k[1], v) for k, v in c.most_common(6)))
print('大小 %.1f KB' % (os.path.getsize(DX) / 1024))

# 归档旧版一页纸
old = os.path.join(DIR, '2026-11-21_发展赛道与存量改造路径_汇报要点一页纸.docx')
if os.path.exists(old):
    arc = os.path.join(DIR, '_归档_被取代版本')
    os.makedirs(arc, exist_ok=True)
    shutil.move(old, os.path.join(arc, os.path.basename(old)))
    print('旧版一页纸已归档 -> _归档_被取代版本')
old2 = os.path.join(DESK, '2026-11-21_发展赛道与存量改造路径_汇报要点一页纸.docx')
if os.path.exists(old2):
    shutil.move(old2, os.path.join(DESK, '2026-11-21_发展赛道与存量改造路径_汇报要点一页纸.docx'))
shutil.copy2(DX, os.path.join(DESK, NAME + '.docx'))
print('桌面副本已同步')
print('')
print('=== 目录最终状态 ===')
for f in sorted(os.listdir(DIR)):
    p = os.path.join(DIR, f)
    if os.path.isfile(p):
        print('  %-62s %5d KB  %s' % (f[:62], os.path.getsize(p) // 1024, time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(p)))))
