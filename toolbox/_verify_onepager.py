# -*- coding: utf-8 -*-
import io, sys, os, subprocess, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.shared import Pt
from docx.oxml.ns import qn
from collections import Counter
DESK = 'C:\\Users\\ericz\\Desktop'
WS = 'D:\\B166ER-openclaw\\workspace'
NAME = '2026-11-21_对大运营体系建设实施方案草案的意见建议_一页纸'
DX = os.path.join(DESK, NAME + '.docx')
print('文件存在:', os.path.exists(DX), ' 大小:', os.path.getsize(DX) // 1024 if os.path.exists(DX) else 0, 'KB')
print('修改时间:', __import__('time').strftime('%Y-%m-%d %H:%M:%S', __import__('time').localtime(os.path.getmtime(DX))))
d = Document(DX)
c = Counter()
for p in d.paragraphs:
    for r in p.runs:
        if not r.text.strip():
            continue
        rpr = r._element.find(qn('w:rPr'))
        ea = sz = None
        if rpr is not None:
            f = rpr.find(qn('w:rFonts'))
            if f is not None: ea = f.get(qn('w:eastAsia'))
            s2 = rpr.find(qn('w:sz'))
            if s2 is not None: sz = int(s2.get(qn('w:val'))) / 2.0
        c[(ea, sz)] += 1
print('字体: ' + ' | '.join('%s/%s x%d' % (k[0], k[1], v) for k, v in c.most_common(5)))
print('段落数:', len(d.paragraphs))
s = d.sections[0]
print('页边距 上%.1f 下%.1f 左%.1f 右%.1f cm' % (s.top_margin.cm, s.bottom_margin.cm, s.left_margin.cm, s.right_margin.cm))
ls = Counter(str(p.paragraph_format.line_spacing) for p in d.paragraphs if p.text.strip())
print('行距: ' + ' | '.join('%s x%d' % (k, v) for k, v in ls.most_common(3)))
print('')
SOFFICE = 'C:\\Program Files\\LibreOffice\\program\\soffice.com'
outdir = os.path.join(WS, 'tmp', '_pdfchk3')
os.makedirs(outdir, exist_ok=True)
for f in os.listdir(outdir):
    os.remove(os.path.join(outdir, f))
r = subprocess.run([SOFFICE, '--headless', '--convert-to', 'pdf', '--outdir', outdir, DX],
                   capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=240)
pdf = os.path.join(outdir, NAME + '.pdf')
if os.path.exists(pdf):
    import pypdf
    n = len(pypdf.PdfReader(pdf).pages)
    print('>>> 实测页数: %d  %s' % (n, '【1 页，达标】' if n == 1 else '【超页，需重新生成】'))
else:
    print('PDF 未生成:', (r.stdout or r.stderr or '')[:150])