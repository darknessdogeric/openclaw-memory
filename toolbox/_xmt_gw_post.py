# -*- coding: utf-8 -*-
import io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import docx
from docx.shared import Pt, Cm, Emu
from docx.enum.text import WD_LINE_SPACING
from docx.oxml.ns import qn
D = r'C:\Users\ericz\Desktop\2026-10-27_安逸集团新媒体业务诊断报告_公文版.docx'
d = docx.Document(D)
n = 0
for p in d.paragraphs:
    pf = p.paragraph_format
    if p.alignment is not None and str(p.alignment).endswith('CENTER'):
        continue
    pf.line_spacing = Pt(28)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    n += 1
d.save(D)
print('行距校准段落数: %d' % n)

d = docx.Document(D)
s = d.sections[0]
print('页边距 上%.1f 下%.1f 左%.1f 右%.1f cm' % (s.top_margin.cm, s.bottom_margin.cm, s.left_margin.cm, s.right_margin.cm))
print('段落 %d  表格 %d  大小 %.1f KB' % (len(d.paragraphs), len(d.tables), os.path.getsize(D)/1024))
print()
print('--- 字体应用统计（按 eastAsia）---')
from collections import Counter
c = Counter()
for p in d.paragraphs:
    for r in p.runs:
        if not r.text.strip(): continue
        rf = r._element.find(qn('w:rPr'))
        ea = ''
        if rf is not None:
            f = rf.find(qn('w:rFonts'))
            if f is not None: ea = f.get(qn('w:eastAsia')) or ''
        sz = r.font.size.pt if r.font.size else 0
        c[(ea, sz)] += 1
for (ea, sz), v in c.most_common(10):
    print('  %-16s %-5s x%d' % (ea or '(未设)', str(sz)+'pt', v))
print()
print('--- 首行缩进抽查 ---')
k = 0
for p in d.paragraphs:
    if p.text.strip() and len(p.text) > 20:
        fi = p.paragraph_format.first_line_indent
        print('  %s %s' % (str(fi), p.text[:26]))
        k += 1
    if k >= 4: break
print()
print('--- 内容完整性 ---')
full = ''.join(x.text for x in d.paragraphs) + ''.join(cl.text for t in d.tables for r in t.rows for cl in r.cells)
for kw in ['关于安逸集团新媒体业务现状的诊断报告','呈：集团领导','产业发展部','一、基本情况','十、数据说明','附件一','附件二']:
    print('  %-28s %s' % (kw, 'OK' if kw in full else 'MISSING'))
bad = [e for e in ['🟢','🟡','🟠','🔴','✅','☑','★'] if e in full]
print('  符号残留: %s' % (','.join(bad) if bad else '无'))
print('  表格行列: ' + ' / '.join('%d×%d' % (len(t.rows), len(t.columns)) for t in d.tables))