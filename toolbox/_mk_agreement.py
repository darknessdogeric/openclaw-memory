# -*- coding: utf-8 -*-
import io, sys, os, re, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_LINE_SPACING
from docx.oxml.ns import qn

MD  = r'D:\B166ER-openclaw\workspace\tmp\_mt_agreement.md'
OUT = r'C:\Users\ericz\Desktop\美团与安逸酒店集团有限责任公司战略合作框架协议（起草稿）20261029.docx'
KBD = r'D:\B166ER-openclaw\workspace\anyi-ops-kb\02_项目\美团充电宝会员跳转合作'
KBM = os.path.join(KBD, '美团与安逸酒店集团有限责任公司战略合作框架协议（起草稿）20261029.md')
CONV = r'D:\B166ER-openclaw\workspace\skills\gongwen-docx-cn\scripts\md2docx_gongwen.py'

t = open(MD, encoding='utf-8').read()
t = re.sub(r'(?m)^(\d+)\.(\S)', r'\1．\2', t)
open(MD, 'w', encoding='utf-8').write(t)
print('编号已规范为全角点')

r = subprocess.run([sys.executable, CONV, MD, OUT], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('转换:', (r.stdout or '').strip(), (r.stderr or '').strip()[:200])

d = Document(OUT)
n = 0
for p in d.paragraphs:
    txt = p.text.strip()
    pf = p.paragraph_format
    if p.alignment is not None and str(p.alignment).endswith('CENTER'):
        continue
    pf.line_spacing = Pt(28)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    n += 1
    if re.match(r'^(甲方|乙方|统一社会信用代码|地址|授权代表|日期)', txt):
        pf.first_line_indent = None
        pf.left_indent = None
    elif txt.startswith('附件一') or txt.startswith('附件二'):
        for run in p.runs:
            rpr = run._element.get_or_add_rPr()
            rf = rpr.find(qn('w:rFonts'))
            if rf is None:
                rf = rpr.makeelement(qn('w:rFonts'), {}); rpr.append(rf)
            rf.set(qn('w:eastAsia'), '黑体'); rf.set(qn('w:ascii'), '黑体'); rf.set(qn('w:hAnsi'), '黑体')
d.save(OUT)
print('行距校准段落', n)

os.makedirs(KBD, exist_ok=True)
open(KBM, 'w', encoding='utf-8').write(open(MD, encoding='utf-8').read())

d2 = Document(OUT)
f = ''.join(x.text for x in d2.paragraphs) + chr(10) + ''.join(cl.text for tb in d2.tables for rr in tb.rows for cl in rr.cells)
print()
print('SIZE %.1f KB  段落 %d  表格 %d  总字数 %d' % (os.path.getsize(OUT)/1024, len(d2.paragraphs), len(d2.tables), len(f)))
from collections import Counter
c = Counter()
for p in d2.paragraphs:
    for run in p.runs:
        if not run.text.strip(): continue
        rpr = run._element.find(qn('w:rPr'))
        ea = None; sz = None
        if rpr is not None:
            fo = rpr.find(qn('w:rFonts'))
            if fo is not None: ea = fo.get(qn('w:eastAsia'))
            s = rpr.find(qn('w:sz'))
            if s is not None: sz = int(s.get(qn('w:val')))/2.0
        c[(ea, sz)] += 1
print('字体统计: ' + ' | '.join('%s/%s x%d' % (k[0], k[1], v) for k, v in c.most_common(6)))
print()
for k in ['战略合作框架协议','两级签约','1小时、2小时','路径一','路径二','1至3个月','业务合作方管理','合作酒店清单','约60家','不约定具体业务的价格、佣金、分成','个人信息保护法','排他性','三年','争议解决','附件一','附件二']:
    print('  %-22s %s' % (k, 'OK' if k in f else 'MISSING'))