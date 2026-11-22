# -*- coding: utf-8 -*-
import io, sys, os, re, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_LINE_SPACING, WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from collections import Counter

WS = 'D:\\B166ER-openclaw\\workspace'
KB = os.path.join(WS, 'anyi-ops-kb', '07_战略与改革')
CONV = os.path.join(WS, 'skills', 'gongwen-docx-cn', 'scripts', 'md2docx_gongwen.py')
DESK = 'C:\\Users\\ericz\\Desktop\\产业发展部\\重要文件'

V2_MD = os.path.join(KB, '2026-11-15_安逸主赛道与存量改造范式_深度再研究_v2.0.md')
V2_DX = os.path.join(KB, '2026-11-15_安逸主赛道与存量改造范式_深度再研究_v2.0.docx')
V1_MD = os.path.join(KB, '2026-11-13_关于安逸酒店集团发展赛道与存量改造路径的指导意见的报告_v1.0.md')
V1_DX = os.path.join(KB, '2026-11-13_关于安逸酒店集团发展赛道与存量改造路径的指导意见的报告_v1.0.docx')

# ---- 0. 诊断 v2.0 现有段落 ----
d = Document(V2_DX)
print('=== v2.0 诊断：前 18 个非空段落 ===')
for i, p in enumerate(d.paragraphs):
    tx = p.text.strip()
    if not tx:
        continue
    ea = None
    sz = None
    for run in p.runs:
        if not run.text.strip():
            continue
        rpr = run._element.find(qn('w:rPr'))
        if rpr is not None:
            f2 = rpr.find(qn('w:rFonts'))
            if f2 is not None:
                ea = f2.get(qn('w:eastAsia'))
            s2 = rpr.find(qn('w:sz'))
            if s2 is not None:
                sz = int(s2.get(qn('w:val'))) / 2.0
        break
    al = str(p.alignment)
    print('  P%-3d %-30s font=%s/%s align=%s' % (i, tx[:28], ea, sz, al[-12:]))
    if i > 20:
        break

# ---- 1. v2.0 去掉 YAML frontmatter ----
t = open(V2_MD, encoding='utf-8').read()
if t.lstrip().startswith('---'):
    parts = t.split('\n---', 1)
    rest = parts[1].split('\n', 1)[1] if len(parts) > 1 else t
    head = '（本件为 2026-11-13《发展赛道与存量改造路径报告》的修正版，取代其第二章与第五章）\n\n'
    t = head + rest.lstrip('\n')
    open(V2_MD, 'w', encoding='utf-8').write(t)
    print('\nv2.0 已去 frontmatter，现 %d 字符' % len(t))

# ---- 2. v1.0 去粗体残留 ----
v1 = open(V1_MD, encoding='utf-8').read()
c = v1.count('**')
if c:
    v1 = v1.replace('**', '')
    open(V1_MD, 'w', encoding='utf-8').write(v1)
    print('v1.0 清除粗体标记 %d 处' % c)

# ---- 3. 重新转换 ----
for src, dst in ((V2_MD, V2_DX), (V1_MD, V1_DX)):
    r = subprocess.run([sys.executable, CONV, src, dst], capture_output=True, text=True, encoding='utf-8', errors='replace')
    print('转换 ' + os.path.basename(dst) + ': ' + (r.stdout or '').strip() + (r.stderr or '').strip()[:120])

# ---- 4. 版式校准（按字体判定层级，不靠正则） ----
def set_font(run, ea, pt):
    run.font.size = Pt(pt)
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = rpr.makeelement(qn('w:rFonts'), {})
        rpr.append(rf)
    for a in ('w:ascii', 'w:hAnsi', 'w:eastAsia'):
        rf.set(qn(a), ea)

def first_font(p):
    for run in p.runs:
        if not run.text.strip():
            continue
        rpr = run._element.find(qn('w:rPr'))
        ea = sz = None
        if rpr is not None:
            f2 = rpr.find(qn('w:rFonts'))
            if f2 is not None:
                ea = f2.get(qn('w:eastAsia'))
            s2 = rpr.find(qn('w:sz'))
            if s2 is not None:
                sz = int(s2.get(qn('w:val'))) / 2.0
        return ea, sz
    return None, None

def calibrate(path):
    d = Document(path)
    n = 0; title = 0; h1 = 0; h2 = 0; fz = 0; sg = 0
    seen_first = False
    for p in d.paragraphs:
        tx = p.text.strip()
        if not tx:
            continue
        pf = p.paragraph_format
        pf.line_spacing = Pt(28)
        pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        n += 1
        ea, sz = first_font(p)
        if not seen_first:
            seen_first = True
            for run in p.runs:
                set_font(run, '方正小标宋简体', 22)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            pf.first_line_indent = None
            title += 1
            continue
        if ea == '黑体':
            for run in p.runs:
                set_font(run, '黑体', 16)
            h1 += 1
            continue
        if ea == '楷体':
            for run in p.runs:
                set_font(run, '楷体', 16)
            h2 += 1
            continue
        if tx.startswith('安逸酒店产业发展部') or re.match(r'^\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日$', tx):
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            pf.first_line_indent = None
            for run in p.runs:
                set_font(run, '仿宋', 16)
            sg += 1
            continue
        for run in p.runs:
            if run.font.size and run.font.size.pt < 15.5:
                set_font(run, '仿宋', 16); fz += 1
    d.save(path)
    return n, title, h1, h2, fz, sg

for p in (V2_DX, V1_DX):
    n, title, h1, h2, fz, sg = calibrate(p)
    d = Document(p)
    s = d.sections[0]
    ft = ''.join(x.text for x in d.paragraphs) + '\n' + '\n'.join(cl.text for t in d.tables for rr in t.rows for cl in rr.cells)
    c = Counter()
    for x in d.paragraphs:
        for run in x.runs:
            if not run.text.strip():
                continue
            rpr = run._element.find(qn('w:rPr'))
            ea = sz = None
            if rpr is not None:
                f2 = rpr.find(qn('w:rFonts'))
                if f2 is not None:
                    ea = f2.get(qn('w:eastAsia'))
                s2 = rpr.find(qn('w:sz'))
                if s2 is not None:
                    sz = int(s2.get(qn('w:val'))) / 2.0
            c[(ea, sz)] += 1
    print('')
    print('== ' + os.path.basename(p))
    print('   %.1f KB  段落 %d  表格 %d' % (os.path.getsize(p) / 1024, len(d.paragraphs), len(d.tables)))
    print('   字体: ' + ' | '.join('%s/%s x%d' % (k[0], k[1], v) for k, v in c.most_common(7)))
    print('   标题 %d / 一级黑体 %d / 二级楷体 %d / 小字升16pt %d / 落款右对齐 %d' % (title, h1, h2, fz, sg))
    print('   粗体残留: ' + ('有' if '**' in ft else '无'))
    print('   页边距 上%.2f 下%.2f 左%.2f 右%.2f cm' % (s.top_margin.cm, s.bottom_margin.cm, s.left_margin.cm, s.right_margin.cm))
    print('   首段: ' + d.paragraphs[0].text[:44])

import shutil
shutil.copy2(V2_DX, os.path.join(DESK, '2026-11-15_安逸主赛道与存量改造范式_深度再研究（修正v2.0）.docx'))
print('')
print('桌面已同步')
