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

# ---- 1. MD 结构改造：去 markdown 标记，建公文抬头 ----
t = open(V2_MD, encoding='utf-8').read()
t = t.replace('**', '')
lines = t.split('\n')
# 收集所有 markdown 标题的正文
title = ''
h1 = []
h2 = []
body = []
for l in lines:
    s = l.rstrip()
    if s.startswith('# '):
        if not title:
            title = s[2:].strip()
    elif s.startswith('## '):
        h1.append(s[3:].strip())
    elif s.startswith('### '):
        h2.append(s[4:].strip())
    else:
        body.append(s)
note = ''
for i, l in enumerate(body):
    if l.strip().startswith('（本件为'):
        note = l.strip()
        body.pop(i)
        break
out = []
out.append(title)
out.append('')
out.append('呈：集团领导')
out.append('拟：产业发展部')
out.append('时间：2026 年 11 月 15 日')
out.append('')
if note:
    out.append(note)
    out.append('')
out.append('编制：B166ER　　编制时间：2026-11-15')
out.append('性质：对 2026-11-13《发展赛道与存量改造路径报告》的修正与深化，该报告第二章与第五章以本件为准')
out.append('信源：集团 KB 既有调研成果八份、2025 年度述职报告、五份原始名录、全网检索')
out.append('数据引用格式：《文件名》（成文日期，数据截止日期）')
out.append('')
ti = 0
bi = 0
for l in body:
    s = l.strip()
    if not s:
        out.append('')
        continue
    if ti < len(h1) and s == h1[ti]:
        out.append(h1[ti]); ti += 1; bi = 0
        continue
    if bi < len(h2) and s == h2[bi]:
        out.append(h2[bi]); bi += 1
        continue
    out.append(l)
# 兜底：把未消费掉的标题追加到末尾
for x in h1[ti:]:
    out.append(''); out.append(x)
for x in h2[bi:]:
    out.append(''); out.append(x)
final = '\n'.join(out)
# 去掉残留的 markdown 记号
final = re.sub(r'^#{1,6}\s*', '', final, flags=re.M)
final = re.sub(r'^>\s*', '', final, flags=re.M)
final = final.replace('| ', '| ')
open(V2_MD, 'w', encoding='utf-8').write(final)
print('MD 重构：标题=%s / 一级 %d / 二级 %d / 总 %d 字符' % (title[:26], len(h1), len(h2), len(final)))

r = subprocess.run([sys.executable, CONV, V2_MD, V2_DX], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('转换:', (r.stdout or '').strip(), (r.stderr or '').strip()[:120])

# ---- 2. 正则校准（与 v1.0 同一套规则） ----
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

# ---- 3. 校验 ----
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
print('次段: ' + (d.paragraphs[1].text[:30] if len(d.paragraphs) > 1 else ''))
CK = ['在地文化生活方式酒店', '逸·精选', '双层改造法', '九步标准流程', '停业期刚性支出', '7,541',
      '15.4%', '柏曼', '145 元', 'GM 95%', '合规四道闸', '零、本次修正的四件事', '一、主赛道',
      '二、存量改造范式', '三、落地路线', '四、数据缺口', '五、与 2026-11-13']
miss = [k for k in CK if k not in ft]
print('关键内容缺失: ' + (', '.join(miss) if miss else '无'))
shutil.copy2(V2_DX, os.path.join(DESK, '2026-11-15_安逸主赛道与存量改造范式_深度再研究（修正v2.0）.docx'))
print('桌面已同步')
