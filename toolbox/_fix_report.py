# -*- coding: utf-8 -*-
import io, sys, os, re, subprocess, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_LINE_SPACING, WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

WS = r'D:\B166ER-openclaw\workspace'
KB = os.path.join(WS, 'anyi-ops-kb', '07_战略与改革')
NAME = '2026-11-13_关于安逸酒店集团发展赛道与存量改造路径的指导意见的报告_v1.0'
MD_OUT = os.path.join(KB, NAME + '.md')
MD_DESK = r'C:\Users\ericz\Desktop\关于安逸酒店集团发展赛道与存量改造路径的指导意见的报告_20261113.md'
DX_OUT = r'C:\Users\ericz\Desktop\关于安逸酒店集团发展赛道与存量改造路径的指导意见的报告_20261113.docx'
CONV = os.path.join(WS, 'skills', 'gongwen-docx-cn', 'scripts', 'md2docx_gongwen.py')

md = open(MD_OUT, encoding='utf-8').read()
before = md.count('**')
md = md.replace('**', '')
open(MD_OUT, 'w', encoding='utf-8').write(md)
shutil.copy2(MD_OUT, MD_DESK)
print('源文件清除粗体标记 %d 处 -> 剩余 %d' % (before, md.count('**')))

r = subprocess.run([sys.executable, CONV, MD_OUT, DX_OUT], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('公文转换:', (r.stdout or '').strip(), (r.stderr or '').strip()[:160])

d = Document(DX_OUT)
n = 0; sg = 0
for p in d.paragraphs:
    t = p.text.strip()
    if p.alignment is not None and str(p.alignment).endswith('CENTER'):
        continue
    pf = p.paragraph_format
    pf.line_spacing = Pt(28)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    n += 1
    if t == '安逸酒店集团产业发展部' or re.match(r'^\d{4}\s*年\s*\d{1,2}\s*月\s*\d{1,2}\s*日$', t):
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        pf.first_line_indent = None
        sg += 1
d.save(DX_OUT)
shutil.copy2(DX_OUT, os.path.join(KB, NAME + '.docx'))
print('行距校准 %d 段，落款右对齐 %d 处' % (n, sg))

d2 = Document(DX_OUT)
full = ''.join(p.text for p in d2.paragraphs) + chr(10) + ''.join(cl.text for t in d2.tables for rr in t.rows for cl in rr.cells)
print()
print('DOCX %.1f KB  段落 %d  表格 %d' % (os.path.getsize(DX_OUT)/1024, len(d2.paragraphs), len(d2.tables)))
print('粗体标记残留: %s' % ('有' if '**' in full else '无'))
SYM = ['\u2605','\u2192','\u2190','\uff0b','\u26a0','\u2610','\u2611','\u221a','\u2713','\u203b','\u3010','\u3011','\u3014','\u3015','\u2022','\u00b7','\uff0a','\uff0d']
hit = [x for x in SYM if x in full]
print('装饰符号残留: %s' % (','.join(hit) if hit else '无'))
print()
for k in ['会员人均年贡献', '约 21 元', '仅占集团考核口径收入 2.3%', '160 万会员几乎未产生消费']:
    print('  %-30s %s' % (k, 'OK' if k in full else 'MISSING'))
print()
print('末三段: ' + ' / '.join(p.text[:30] for p in d2.paragraphs[-4:] if p.text.strip()))
print('落款段: ' + ' / '.join(p.text[:26] for p in d2.paragraphs[-2:]))