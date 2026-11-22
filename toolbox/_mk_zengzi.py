# -*- coding: utf-8 -*-
import io, sys, os, re, subprocess, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_LINE_SPACING, WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from collections import Counter

WS = 'D:\\B166ER-openclaw\\workspace'
KB = os.path.join(WS, 'anyi-ops-kb', '07_战略与改革')
OUT_DIR = 'C:\\Users\\ericz\\Desktop\\产业发展部\\重要文件'
os.makedirs(OUT_DIR, exist_ok=True)
CONV = os.path.join(WS, 'skills', 'gongwen-docx-cn', 'scripts', 'md2docx_gongwen.py')
SRC = os.path.join(WS, 'tmp', '_zengzi_yijian.md')
NAME = '2026-11-19_对《四川省旅游投资集团有限责任公司增资实施细则（试行）》的意见建议'
DX = os.path.join(OUT_DIR, NAME + '.docx')
MD = os.path.join(KB, NAME + '.md')

t = open(SRC, encoding='utf-8').read()
t = t.replace('**', '')
lines = []
for l in t.split('\n'):
    s = l.rstrip()
    if re.match(r'^\s*-{3,}\s*$', s):
        continue
    s = re.sub(r'^\*(.+)\*$', r'\1', s.strip())
    s = s.replace('*', '')
    lines.append(s)
t = '\n'.join(lines)
open(SRC, 'w', encoding='utf-8').write(t)
open(MD, 'w', encoding='utf-8').write(t)
print('源文件清洗 %d 字符' % len(t))

r = subprocess.run([sys.executable, CONV, SRC, DX], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('公文转换:', (r.stdout or '').strip(), (r.stderr or '').strip()[:150])


def set_font(run, ea, pt):
    run.font.size = Pt(pt)
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = rpr.makeelement(qn('w:rFonts'), {})
        rpr.append(rf)
    for a in ('w:ascii', 'w:hAnsi', 'w:eastAsia'):
        rf.set(qn(a), ea)


H1 = re.compile(r'^[一二三四五六七八九十]+、')
H2 = re.compile(r'^（[一二三四五六七八九十]+）')
d = Document(DX)
n = 0; t1 = 0; h1 = 0; h2 = 0; fz = 0; sg = 0; first = True
for p in d.paragraphs:
    tx = p.text.strip()
    if not tx:
        continue
    pf = p.paragraph_format
    pf.line_spacing = Pt(28)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    n += 1
    if first:
        first = False
        for run in p.runs:
            set_font(run, '方正小标宋简体', 22)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        pf.first_line_indent = None
        t1 += 1
        continue
    if H1.match(tx):
        for run in p.runs:
            set_font(run, '黑体', 16)
        h1 += 1
        continue
    if H2.match(tx):
        for run in p.runs:
            set_font(run, '楷体', 16)
        h2 += 1
        continue
    if tx.startswith('安逸酒店集团产业发展部') or re.match(r'^2026\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日$', tx):
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        pf.first_line_indent = None
        for run in p.runs:
            set_font(run, '仿宋', 16)
        sg += 1
        continue
    for run in p.runs:
        if run.font.size and run.font.size.pt < 15.5:
            set_font(run, '仿宋', 16); fz += 1
d.save(DX)

d = Document(DX)
s = d.sections[0]
ft = ''.join(x.text for x in d.paragraphs) + '\n' + '\n'.join(cl.text for tb in d.tables for rr in tb.rows for cl in rr.cells)
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
print('DOCX %.1f KB  段落 %d  表格 %d' % (os.path.getsize(DX) / 1024, len(d.paragraphs), len(d.tables)))
print('字体: ' + ' | '.join('%s/%s x%d' % (k[0], k[1], v) for k, v in c.most_common(6)))
print('标题 %d / 一级黑体 %d / 二级楷体 %d / 小字升16pt %d / 落款右对齐 %d' % (t1, h1, h2, fz, sg))
print('粗体残留: ' + ('有' if '**' in ft else '无'))
print('页边距 上%.2f 下%.2f 左%.2f 右%.2f cm' % (s.top_margin.cm, s.bottom_margin.cm, s.left_margin.cm, s.right_margin.cm))
print('首段: ' + d.paragraphs[0].text[:44])
print('末三段: ' + ' / '.join(p.text[:30] for p in d.paragraphs[-4:] if p.text.strip()))
CK = ['集团战略投资部', '一、关于总体意见的补充建议', '二、关于具体条款的意见', '三、其他建议',
      '第二十三条', '第二十六条', '第三十四条', '第二十条', '第三十条', '第十五条', '第六十条',
      '第五十六条', '第五十八条', '第十九条', '第四十四条', '附件一', '2026 年 11 月 19 日',
      '6,605.49', '184.16%', '古尔沟', '安逸连锁', '国堰', 'LPR', '90%', '3,000 万元']
print('')
miss = [k for k in CK if k not in ft]
for k in CK:
    print('  %-28s %s' % (k, 'OK' if k in ft else 'MISSING'))
print('')
print('缺项 %d' % len(miss))
print('KB: ' + MD)
print('交付: ' + DX)
