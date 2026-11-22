# -*- coding: utf-8 -*-
import io, sys, os, re, shutil, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_LINE_SPACING, WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from collections import Counter

WS = 'D:\\B166ER-openclaw\\workspace'
TMP = os.path.join(WS, 'tmp')
KB = os.path.join(WS, 'anyi-ops-kb', '07_战略与改革')
ROOT = 'C:\\Users\\ericz\\Desktop\\产业发展部\\酒店摸排'
D1 = os.path.join(ROOT, '01_发文件')
D2 = os.path.join(ROOT, '02_摸排底册与口径')
D3 = os.path.join(ROOT, '03_填报与回收')
for d in (D1, D2, D3):
    os.makedirs(d, exist_ok=True)
CONV = os.path.join(WS, 'skills', 'gongwen-docx-cn', 'scripts', 'md2docx_gongwen.py')

def rd(n):
    return open(os.path.join(TMP, n), encoding='utf-8').read().rstrip()

notice = rd('_tijiao_notice.md')
att1 = rd('_att1.md')
att2 = rd('_tijiao_att2.md')
att3 = rd('_tijiao_att3.md')

full = notice + chr(10) + chr(10) + att1 + chr(10) + chr(10) + att2 + chr(10) + chr(10) + att3 + chr(10)
MD_FULL = os.path.join(D1, '关于开展集团旗下酒店全面摸排与基础数据填报工作的通知_20261113.md')
open(MD_FULL, 'w', encoding='utf-8').write(full)
print('合并全文 %d 字符' % len(full))

MD_A1 = os.path.join(D2, '附件一_安逸集团旗下酒店摸排底册_v1.0.md')
open(MD_A1, 'w', encoding='utf-8').write(att1 + chr(10))
MD_A3 = os.path.join(D3, '附件三_填报表（空白模板）_v1.0.md')
open(MD_A3, 'w', encoding='utf-8').write(att3 + chr(10))

DX_FULL = os.path.join(D1, '关于开展集团旗下酒店全面摸排与基础数据填报工作的通知_20261113.docx')
DX_A1 = os.path.join(D2, '附件一_安逸集团旗下酒店摸排底册_v1.0.docx')
DX_A3 = os.path.join(D3, '附件三_填报表（空白模板）_v1.0.docx')
for src, dst in ((MD_FULL, DX_FULL), (MD_A1, DX_A1), (MD_A3, DX_A3)):
    r = subprocess.run([sys.executable, CONV, src, dst], capture_output=True, text=True, encoding='utf-8', errors='replace')
    print('转换 ' + os.path.basename(dst) + ': ' + (r.stdout or '').strip() + (r.stderr or '').strip()[:120])

def calibrate(path):
    d = Document(path)
    n = 0; sg = 0
    for p in d.paragraphs:
        t = p.text.strip()
        if p.alignment is not None and str(p.alignment).endswith('CENTER'):
            continue
        pf = p.paragraph_format
        pf.line_spacing = Pt(28)
        pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
        n += 1
        if t.startswith('安逸酒店集团产业发展部') or re.match(r'^\u4e8c\u96f6\u4e8c\u516d\u5e74\u5341\u4e00\u6708\u5341\u4e09\u65e5$', t) or t == '2026年11月13日':
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            pf.first_line_indent = None
            sg += 1
    d.save(path)
    return n, sg

for f in (DX_FULL, DX_A1, DX_A3):
    n, sg = calibrate(f)
    d = Document(f)
    s = d.sections[0]
    fulltext = ''.join(p.text for p in d.paragraphs) + chr(10) + ''.join(cl.text for t in d.tables for rr in t.rows for cl in rr.cells)
    print('')
    print('== ' + os.path.basename(f))
    print('   %.1f KB  段落 %d  表格 %d' % (os.path.getsize(f)/1024, len(d.paragraphs), len(d.tables)))
    print('   页边距 上%.2f 下%.2f 左%.2f 右%.2f cm' % (s.top_margin.cm, s.bottom_margin.cm, s.left_margin.cm, s.right_margin.cm))
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
    print('   字体: ' + ' | '.join('%s/%s x%d' % (k[0], k[1], v) for k, v in c.most_common(5)))
    print('   行距校准 %d 段  落款右对齐 %d 处' % (n, sg))
    print('   粗体残留: ' + ('有' if '**' in fulltext else '无'))

d = Document(DX_FULL)
ft = ''.join(p.text for p in d.paragraphs) + chr(10) + ''.join(cl.text for t in d.tables for rr in t.rows for cl in rr.cells)
CK = ['关于开展集团旗下酒店全面摸排与基础数据填报工作的通知', '集团所属各酒店、各项目公司及饭店管理公司', '一、摸排目的', '二、摸排范围', '三、填报内容', '四、填报口径', '五、时间安排', '六、工作要求', '特此通知', '附件一', '附件二', '附件三', '附件四', '表一', '表二', '表三', '表四', '表五', '表六', '表七', '表八', '摸排底册', '填报须知与口径定义', '差异说明汇总表', '二〇二六年十一月十三日']
miss = 0
for k in CK:
    ok = k in ft
    if not ok: miss += 1
    print('  %-34s %s' % (k, 'OK' if ok else 'MISSING'))
print('')
print('缺项 %d' % miss)
print('首段: ' + d.paragraphs[0].text[:46])
print('主送: ' + (d.paragraphs[1].text[:44] if len(d.paragraphs) > 1 else ''))
print('末三段: ' + ' / '.join(p.text[:24] for p in d.paragraphs[-4:] if p.text.strip()))