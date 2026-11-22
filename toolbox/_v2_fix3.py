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
CONV = os.path.join(WS, 'skills', 'gongwen-docx-cn', 'scripts', 'md2docx_gongwen.py')
DESK = 'C:\\Users\\ericz\\Desktop\\产业发展部\\重要文件'
V2_MD = os.path.join(KB, '2026-11-15_安逸主赛道与存量改造范式_深度再研究_v2.0.md')
V2_DX = os.path.join(KB, '2026-11-15_安逸主赛道与存量改造范式_深度再研究_v2.0.docx')

t = open(V2_MD, encoding='utf-8').read()
lines = t.split('\n')
bad = [(i, l) for i, l in enumerate(lines) if re.match(r'^#{1,6}\s', l)]
print('MD 中残留 markdown 标题行 %d 行:' % len(bad))
for i, l in bad[:12]:
    print('   L%d: %s' % (i, l[:96]))
# 找表格行中的 # 号
tb = [(i, l) for i, l in enumerate(lines) if l.strip().startswith('|') and '#' in l]
print('表格行含 # 号 %d 行:' % len(tb))
for i, l in enumerate(tb[:8]):
    print('   L%d: %s' % (i, l[:110]))

# 清理：行首 markdown 记号、行内孤立 # 号、分隔线
out = []
for l in lines:
    s = re.sub(r'^#{1,6}\s*', '', l)
    s = s.replace('| # |', '| 序号 |')
    s = re.sub(r'\|\s*#\s*\|', '| 序号 |', s)
    if re.match(r'^\s*-{3,}\s*$', s):
        continue
    out.append(s)
t = '\n'.join(out)

# 补正式落款
TAIL = '\n安逸酒店产业发展部\n2026 年 11 月 15 日\n'
if '安逸酒店产业发展部\n2026 年 11 月 15 日' not in t:
    # 去掉末尾的斜体署名行，改用正式落款
    t = re.sub(r'\n\*编制：B166ER[^\n]*\n', '\n', t)
    t = re.sub(r'\n\*信源时间戳[^\n]*\n', '\n', t)
    t = re.sub(r'\n<!--.*?-->\s*', '\n', t, flags=re.S)
    t = t.rstrip() + '\n' + TAIL
open(V2_MD, 'w', encoding='utf-8').write(t)
print('MD 清理完成 %d 字符' % len(t))

r = subprocess.run([sys.executable, CONV, V2_MD, V2_DX], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('转换:', (r.stdout or '').strip(), (r.stderr or '').strip()[:120])


def set_font(run, ea, pt):
    run.font.size = Pt(pt)
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = rpr.makeelement(qn('w:rFonts'), {})
        rpr.append(rf)
    for a in ('w:ascii', 'w:hAnsi', 'w:eastAsia'):
        rf.set(qn(a), ea)


HEAD1 = re.compile(r'^[零一二三四五六七八九十]+、')
HEAD2 = re.compile(r'^\d+\.\d+')
d = Document(V2_DX)
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
    if HEAD1.match(tx):
        for run in p.runs:
            set_font(run, '黑体', 16)
        h1 += 1
        continue
    if HEAD2.match(tx):
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
d.save(V2_DX)

d = Document(V2_DX)
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
print('DOCX %.1f KB  段落 %d  表格 %d' % (os.path.getsize(V2_DX) / 1024, len(d.paragraphs), len(d.tables)))
print('字体: ' + ' | '.join('%s/%s x%d' % (k[0], k[1], v) for k, v in c.most_common(8)))
print('标题 %d / 一级黑体 %d / 二级楷体 %d / 小字升16pt %d / 落款右对齐 %d' % (t1, h1, h2, fz, sg))
print('粗体残留: ' + ('有' if '**' in ft else '无'))
print('残留 markdown 记号: ' + ('有' if re.search(r'(?m)^#{1,6}\s', ft) else '无'))
print('页边距 上%.2f 下%.2f 左%.2f 右%.2f cm' % (s.top_margin.cm, s.bottom_margin.cm, s.left_margin.cm, s.right_margin.cm))
print('首段: ' + d.paragraphs[0].text[:44])
print('末三段: ' + ' / '.join(p.text[:30] for p in d.paragraphs[-4:] if p.text.strip()))
CK = ['在地文化生活方式酒店', '逸·精选', '双层改造法', '九步标准流程', '停业期刚性支出', '7,541',
      '15.4%', '柏曼', '145 元', 'GM 95%', '合规四道闸', '零、本次修正的四件事', '一、主赛道',
      '二、存量改造范式', '三、落地路线', '四、数据缺口', '五、与 2026-11-13', '2026 年 11 月 15 日']
miss = [k for k in CK if k not in ft]
print('关键内容缺失: ' + (', '.join(miss) if miss else '无'))
shutil.copy2(V2_DX, os.path.join(DESK, '2026-11-15_安逸主赛道与存量改造范式_深度再研究（修正v2.0）.docx'))
print('桌面已同步')
