# -*- coding: utf-8 -*-
import io, sys, os, re, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_LINE_SPACING, WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from collections import Counter

WS = 'D:\\B166ER-openclaw\\workspace'
TMP = os.path.join(WS, 'tmp')
ROOT = 'C:\\Users\\ericz\\Desktop\\产业发展部\\酒店摸排'
D1 = os.path.join(ROOT, '01_发文件')
D2 = os.path.join(ROOT, '02_摸排底册与口径')
D3 = os.path.join(ROOT, '03_填报与回收')
CONV = os.path.join(WS, 'skills', 'gongwen-docx-cn', 'scripts', 'md2docx_gongwen.py')

def rd(n):
    return open(os.path.join(TMP, n), encoding='utf-8').read().rstrip()

att2 = rd('_tijiao_att2.md')
lvl = []
lvl.append('')
lvl.append('五、改造级别定义（用于表五自评）')
lvl.append('')
lvl.append('| 级别 | 名称 | 内容 | 单房投资参考 | 停业上限 |')
lvl.append('|---|---|---|---|---|')
lvl.append('| L0 | 焕新 | 卫生、软装、标识、照明、窗帘、局部隔音 | 0.5 至 1.5 万元 | 0 天 |')
lvl.append('| L1 | 产品轻改 | 客房硬装局部、卫浴、插座、床垫、隔音、弱电 | 3 至 5 万元 | 7 天以内，分区施工 |')
lvl.append('| L2 | 场景轻改 | 客房、公区、餐饮动线、主题化、非房场景 | 8 至 15 万元 | 15 天以内，分区施工 |')
lvl.append('| L3 | 系统更新 | 机电、空调、电梯、消防升级 | 20 至 50 万元 | 45 天以内 |')
lvl.append('| L4 | 全面重建 | 拆除重做 | 50 万元以上 | 原则上不采用 |')
lvl.append('')
lvl.append('分级依据是这家店该不该改、能改多少，不是形象好不好看。集团将以本级别作为审定改造投资上限与审批权限的依据，超过单房投资参考区间的，须在表五与附件四中单独说明。')
lvl.append('')
lvl.append('六、填报组织要求')
blk = chr(10).join(lvl)
assert '五、填报组织要求' in att2
att2 = att2.replace('五、填报组织要求', blk, 1)
att2 = att2.replace('级别定义见通知第五部分口径', '级别定义见附件二第五部分')
open(os.path.join(TMP, '_tijiao_att2.md'), 'w', encoding='utf-8').write(att2)
print('附件二 已补 L0-L4 定义 -> ' + str(len(att2)) + ' 字符')

notice = rd('_tijiao_notice.md')
att1 = rd('_att1.md')
att3 = rd('_tijiao_att3.md')
full = notice + chr(10) + chr(10) + att1 + chr(10) + chr(10) + att2 + chr(10) + chr(10) + att3 + chr(10)
F_MD = os.path.join(D1, '关于开展集团旗下酒店全面摸排与基础数据填报工作的通知_20261113.md')
A1_MD = os.path.join(D2, '附件一_安逸集团旗下酒店摸排底册_v1.0.md')
A3_MD = os.path.join(D3, '附件三_填报表（空白模板）_v1.0.md')
for path, txt in ((F_MD, full), (A1_MD, att1 + chr(10)), (A3_MD, att3 + chr(10))):
    c = txt.count('**')
    open(path, 'w', encoding='utf-8').write(txt.replace('**', ''))
    print('  清除粗体标记 ' + str(c) + ' 处 -> ' + os.path.basename(path))

JOBS = [(F_MD, os.path.join(D1, '关于开展集团旗下酒店全面摸排与基础数据填报工作的通知_20261113.docx')),
         (A1_MD, os.path.join(D2, '附件一_安逸集团旗下酒店摸排底册_v1.0.docx')),
         (A3_MD, os.path.join(D3, '附件三_填报表（空白模板）_v1.0.docx'))]
for src, dst in JOBS:
    r = subprocess.run([sys.executable, CONV, src, dst], capture_output=True, text=True, encoding='utf-8', errors='replace')
    print('转换 ' + os.path.basename(dst) + ': ' + (r.stdout or '').strip())

def set_font(run, ea, pt):
    run.font.size = Pt(pt)
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = rpr.makeelement(qn('w:rFonts'), {})
        rpr.append(rf)
    for a in ('w:ascii', 'w:hAnsi', 'w:eastAsia'):
        rf.set(qn(a), ea)

ATT_RE = re.compile('^附件[一二三四五六七八九十]')
def fix(path):
    d = Document(path)
    n = 0; sg = 0; fz = 0; hd = 0
    for p in d.paragraphs:
        t = p.text.strip()
        if not t: continue
        pf = p.paragraph_format
        pf.line_spacing = Pt(28)
        pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        n += 1
        if ATT_RE.match(t):
            for run in p.runs: set_font(run, '黑体', 16)
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            pf.first_line_indent = Pt(32)
            hd += 1
            continue
        if p.alignment is not None and str(p.alignment).endswith('CENTER'):
            for run in p.runs:
                if run.font.size and run.font.size.pt < 21:
                    set_font(run, '仿宋', 16); fz += 1
            continue
        if t.startswith('安逸酒店集团产业发展部') or t == '2026年11月13日':
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            pf.first_line_indent = None
            for run in p.runs: set_font(run, '仿宋', 16)
            sg += 1
            continue
        for run in p.runs:
            if run.font.size and run.font.size.pt < 15.5:
                set_font(run, '仿宋', 16); fz += 1
    d.save(path)
    return n, sg, fz, hd

for src, dst in JOBS:
    n, sg, fz, hd = fix(dst)
    d = Document(dst)
    s = d.sections[0]
    ft = ''.join(p.text for p in d.paragraphs) + chr(10) + ''.join(cl.text for t in d.tables for rr in t.rows for cl in rr.cells)
    c = Counter()
    for p in d.paragraphs:
        for run in p.runs:
            if not run.text.strip(): continue
            rpr = run._element.find(qn('w:rPr'))
            ea = sz = None
            if rpr is not None:
                f2 = rpr.find(qn('w:rFonts'))
                if f2 is not None: ea = f2.get(qn('w:eastAsia'))
                s2 = rpr.find(qn('w:sz'))
                if s2 is not None: sz = int(s2.get(qn('w:val')))/2.0
            c[(ea, sz)] += 1
    print('')
    print('== ' + os.path.basename(dst))
    print('   %.1f KB  段落 %d  表格 %d' % (os.path.getsize(dst)/1024, len(d.paragraphs), len(d.tables)))
    print('   字体: ' + ' | '.join('%s/%s x%d' % (k[0], k[1], v) for k, v in c.most_common(6)))
    print('   行距 %d 段 / 落款右对齐 %d / 小字升16pt %d / 附件标题黑体 %d' % (n, sg, fz, hd))
    print('   粗体残留: ' + ('有' if '**' in ft else '无'))
    print('   页边距 上%.2f 下%.2f 左%.2f 右%.2f cm' % (s.top_margin.cm, s.bottom_margin.cm, s.left_margin.cm, s.right_margin.cm))