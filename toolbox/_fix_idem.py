# -*- coding: utf-8 -*-
"""修 calibrate 幂等性：楷体判定改为基于文本模式，不依赖 ‖ 标记"""
import io, sys, os, re, subprocess, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.shared import Pt, Cm
from docx.enum.text import WD_LINE_SPACING, WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from collections import Counter

B = r'D:\B166ER-openclaw\workspace\toolbox\_mk_chair_gongwen3.py'
t = open(B, encoding='utf-8').read()

OLD = """        # 二级标题短语（楷体）＋正文（仿宋）同段
        if '‖' in tx:
            head, tail = tx.split('‖', 1)
            clear_runs(p)
            set_font(p.add_run(head), '楷体', 16)
            set_font(p.add_run(tail), '仿宋', 16)
        else:
            for r in p.runs:
                set_font(r, '仿宋', 16)"""

NEW = """        # 二级标题短语（楷体）＋正文（仿宋）同段 —— 幂等：按文本模式判定
        if '‖' in tx:
            head, tail = tx.split('‖', 1)
            clear_runs(p)
            set_font(p.add_run(head), '楷体', 16)
            set_font(p.add_run(tail), '仿宋', 16)
        else:
            rs = [r for r in p.runs if r.text.strip()]
            is_sub = bool(re.match(r'^（[一二三四五六七八九十]+）', tx)) and len(rs) >= 2
            if is_sub:
                first = rs[0].text.strip()
                if first.endswith('。') and len(first) <= 40:
                    set_font(rs[0], '楷体', 16)
                    for r in rs[1:]:
                        set_font(r, '仿宋', 16)
                else:
                    for r in rs:
                        set_font(r, '仿宋', 16)
            else:
                for r in rs:
                    set_font(r, '仿宋', 16)"""

if OLD in t:
    t = t.replace(OLD, NEW, 1)
    print('calibrate 已改为幂等（按文本模式判定楷体）')
else:
    print('!! 未命中，脚本未改')
    sys.exit(1)
open(B, 'w', encoding='utf-8').write(t)

r = subprocess.run([sys.executable, B], capture_output=True, text=True, encoding='utf-8', errors='replace')
print(r.stdout)
if r.stderr:
    print('STDERR:', r.stderr[:300])

DX = r'C:\Users\ericz\Desktop\产业发展部\给董事长的单独汇报\2026-11-21_发展赛道与存量改造路径_汇报要点.docx'
d = Document(DX)
c = Counter()
for p in d.paragraphs:
    for rr in p.runs:
        if not rr.text.strip():
            continue
        rpr = rr._element.find(qn('w:rPr'))
        ea = sz = None
        if rpr is not None:
            f = rpr.find(qn('w:rFonts'))
            if f is not None:
                ea = f.get(qn('w:eastAsia'))
            s2 = rpr.find(qn('w:sz'))
            if s2 is not None:
                sz = int(s2.get(qn('w:val'))) / 2.0
        c[(ea, sz)] += 1
print('')
print('字体统计: ' + ' | '.join('%s/%s x%d' % (k[0], k[1], v) for k, v in c.most_common(8)))
full = '\n'.join(p.text for p in d.paragraphs)
print('‖ 残留: %d' % full.count('‖'))
print('段落 %d  表格 %d  大小 %.1f KB' % (len(d.paragraphs), len(d.tables), os.path.getsize(DX) / 1024))
print('')
print('=== 段落抽样 ===')
for i, p in enumerate(d.paragraphs[:13]):
    tx = p.text.strip()
    if not tx:
        continue
    fs = []
    for rr in p.runs:
        if not rr.text.strip():
            continue
        rpr = rr._element.find(qn('w:rPr'))
        ea = None
        if rpr is not None:
            f = rpr.find(qn('w:rFonts'))
            if f is not None:
                ea = f.get(qn('w:eastAsia'))
        fs.append('%s「%s」' % (ea, rr.text[:18]))
    print('  P%-2d %s' % (i, ' + '.join(fs)[:150]))
shutil.copy2(DX, os.path.join(r'C:\Users\ericz\Desktop', os.path.basename(DX)))
print('')
print('桌面副本已同步')
