# -*- coding: utf-8 -*-
import io, sys, os, re, subprocess, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_LINE_SPACING, WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from collections import Counter

WS = r'D:\B166ER-openclaw\workspace'
KB = os.path.join(WS, 'anyi-ops-kb', '07_战略与改革')
BODY = os.path.join(WS, 'tmp', '_report_gaidao.md')
ATT = os.path.join(WS, 'tmp', '_report_att.md')
NAME = '2026-11-13_关于安逸酒店集团发展赛道与存量改造路径的指导意见的报告_v1.0'
MD_OUT = os.path.join(KB, NAME + '.md')
MD_DESK = r'C:\Users\ericz\Desktop\关于安逸酒店集团发展赛道与存量改造路径的指导意见的报告_20261113.md'
DX_OUT = r'C:\Users\ericz\Desktop\关于安逸酒店集团发展赛道与存量改造路径的指导意见的报告_20261113.docx'
CONV = os.path.join(WS, 'skills', 'gongwen-docx-cn', 'scripts', 'md2docx_gongwen.py')

md = open(BODY, encoding='utf-8').read().rstrip() + chr(10) + open(ATT, encoding='utf-8').read()
open(MD_OUT, 'w', encoding='utf-8').write(md)
shutil.copy2(MD_OUT, MD_DESK)
print('报告 MD %d 字符 -> KB + 桌面' % len(md))

r = subprocess.run([sys.executable, CONV, MD_OUT, DX_OUT], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('公文转换:', (r.stdout or '').strip(), (r.stderr or '').strip()[:180])

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
s = d2.sections[0]
print()
print('DOCX %.1f KB  段落 %d  表格 %d' % (os.path.getsize(DX_OUT)/1024, len(d2.paragraphs), len(d2.tables)))
print('页边距 上%.2f 下%.2f 左%.2f 右%.2f cm' % (s.top_margin.cm, s.bottom_margin.cm, s.left_margin.cm, s.right_margin.cm))
c = Counter(); ind = Counter(); ls = Counter()
for p in d2.paragraphs:
    if p.text.strip():
        ind[str(p.paragraph_format.first_line_indent)] += 1
        ls[str(p.paragraph_format.line_spacing)] += 1
    for run in p.runs:
        if not run.text.strip():
            continue
        rpr = run._element.find(qn('w:rPr'))
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
print('缩进: ' + ' | '.join('%s x%d' % (k, v) for k, v in ind.most_common(3)))
print('行距: ' + ' | '.join('%s x%d' % (k, v) for k, v in ls.most_common(3)))
full = ''.join(p.text for p in d2.paragraphs) + chr(10) + ''.join(cl.text for t in d2.tables for rr in t.rows for cl in rr.cells)
print()
SYM = ['\u2605', '\u2192', '\u2190', '\uff0b', '\u26a0', '\u2610', '\u2611', '\u221a', '\u2713', '\u203b', '\u3010', '\u3011', '\u3014', '\u3015', '\u2022', '\u00b7', '\uff0a', '\uff0d']
hit = [x for x in SYM if x in full]
print('装饰符号残留: %s' % (','.join(hit) if hit else '无'))
print('粗体标记残留: %s' % ('有' if '**' in full else '无'))
print()
CK = ['关于安逸酒店集团发展赛道与存量改造路径的指导意见的报告', '呈：集团领导', '拟：产业发展部',
 '一、总体判断', '二、赛道选择', '三、赛道产品模型', '四、赛道商业模型', '五、存量改造路径与范式',
 '六、组织与机制保障', '七、需集团决策事项', '八、风险提示', '附件一', '附件二',
 'P1 政务型有限服务', 'P4 轻资产输出', '三段式收入结构', '轻资产输出的商业条款设计',
 '会员与直销商业模型', '二销与供应链商业模型', '三年经营路线图', 'L1 产品轻改', '分级审批与合规管控',
 '国堰宾馆量化示范', '试点与推进安排', '147,629', '100,203', '6,892', '266.80', '102.63',
 '160 万', '约 21 元', '2026 年 11 月 13 日']
miss = 0
for k in CK:
    ok = k in full
    if not ok:
        miss += 1
    print('  %-32s %s' % (k, 'OK' if ok else 'MISSING'))
print()
print('缺项 %d' % miss)
print('首段: ' + d2.paragraphs[0].text[:46])
print('末三段: ' + ' / '.join(p.text[:26] for p in d2.paragraphs[-4:] if p.text.strip()))