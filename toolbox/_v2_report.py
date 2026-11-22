# -*- coding: utf-8 -*-
import io, sys, os, re, shutil, subprocess
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

# ---------- 1. v2.0 清洗 ----------
t = open(V2_MD, encoding='utf-8').read()
t = re.sub(r'<!--.*?-->', '', t, flags=re.S)
t = t.replace('**', '')
t = t.rstrip() + '\n'
open(V2_MD, 'w', encoding='utf-8').write(t)
print('v2.0 源文件清洗后 %d 字符' % len(t))

r = subprocess.run([sys.executable, CONV, V2_MD, V2_DX], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('转换 v2.0:', (r.stdout or '').strip(), (r.stderr or '').strip()[:150])

# ---------- 2. v1.0 加作废标注 ----------
BANNER = ('> **【本件已部分作废 · 2026-11-15】**\n'
          '> 本件第三章（赛道产品模型）与第五章（存量改造范式）已被《2026-11-15_安逸主赛道与存量改造范式_深度再研究_v2.0》取代；\n'
          '> **本件第二章"主赛道＝成德绵乐与川西北两集群的中高端有限服务型，内核为政务接待＋区域康养度假"的表述不成立**，\n'
          '> 修正后主赛道为"在地文化生活方式酒店（有限服务为主体）"，依据见 v2.0 第一章。\n'
          '> 本件第一章、第四章、第六章、第七章、第八章继续有效。请勿单独引用本件第二章。\n\n')
v1 = open(V1_MD, encoding='utf-8').read()
if '本件已部分作废' not in v1:
    lines = v1.split('\n')
    # 插到 frontmatter 之后
    ins = 0
    for i, l in enumerate(lines):
        if l.strip() == '---':
            if ins == 0:
                ins = i + 1
                break
            else:
                break
    if ins == 0:
        ins = 1
    v1 = '\n'.join(lines[:ins]) + '\n' + BANNER + '\n'.join(lines[ins:])
    open(V1_MD, 'w', encoding='utf-8').write(v1)
    print('v1.0 已加作废标注')
r = subprocess.run([sys.executable, CONV, V1_MD, V1_DX], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('转换 v1.0:', (r.stdout or '').strip(), (r.stderr or '').strip()[:150])

# ---------- 3. 版式校准 ----------
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

def calibrate(path):
    d = Document(path)
    n = 0; h1 = 0; h2 = 0; fz = 0
    for p in d.paragraphs:
        tx = p.text.strip()
        if not tx:
            continue
        pf = p.paragraph_format
        pf.line_spacing = Pt(28)
        pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        n += 1
        if p.alignment is not None and str(p.alignment).endswith('CENTER'):
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
            continue
        for run in p.runs:
            if run.font.size and run.font.size.pt < 15.5:
                set_font(run, '仿宋', 16); fz += 1
    d.save(path)
    return n, h1, h2, fz

for p in (V2_DX, V1_DX):
    n, h1, h2, fz = calibrate(p)
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
    print('   字体: ' + ' | '.join('%s/%s x%d' % (k[0], k[1], v) for k, v in c.most_common(6)))
    print('   行距 %d 段 / 一级黑体 %d / 二级楷体 %d / 小字升16pt %d' % (n, h1, h2, fz))
    print('   粗体残留: ' + ('有' if '**' in ft else '无'))
    print('   页边距 上%.2f 下%.2f 左%.2f 右%.2f cm' % (s.top_margin.cm, s.bottom_margin.cm, s.left_margin.cm, s.right_margin.cm))

# ---------- 4. 桌面同步 ----------
os.makedirs(DESK, exist_ok=True)
shutil.copy2(V2_DX, os.path.join(DESK, '2026-11-15_安逸主赛道与存量改造范式_深度再研究（修正v2.0）.docx'))
print('')
print('桌面已同步: ' + os.path.join(DESK, '2026-11-15_安逸主赛道与存量改造范式_深度再研究（修正v2.0）.docx'))

# ---------- 5. 内容校验 ----------
d = Document(V2_DX)
ft = ''.join(x.text for x in d.paragraphs) + '\n' + '\n'.join(cl.text for t in d.tables for rr in t.rows for cl in rr.cells)
CK = ['在地文化生活方式酒店', '逸·精选', '逸·精品', '逸·度假', '双层改造法', '九步标准流程',
      '停业期刚性支出', '7,541', '4.05 亿', '15.4%', '非房', '420.42', '410.68', '269.14',
      '本次修正的四件事', '不能什么都做', '柏曼', '45 天', '145 元', 'GM 95%',
      '合规四道闸', '议题合规审查', '川旅投发〔2026〕147 号', '穿透式监管',
      '一企一策', '3 方向决策框架', '翻牌改造流程', '分级分类基准参数体系',
      '在地市井', '巴蜀深度', '标准范式', '在地文化', '80 间', '零、本次修正的四件事']
print('')
miss = 0
for k in CK:
    ok = k in ft
    if not ok:
        miss += 1
    print('  %-30s %s' % (k, 'OK' if ok else 'MISSING'))
print('')
print('缺项 %d' % miss)
