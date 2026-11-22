# -*- coding: utf-8 -*-
"""修 set_font 的 rPr 顺序缺陷 + 轻度压缩内容，重建公文版"""
import io, sys, os, re, subprocess, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ---------- 1. 修 set_font（rFonts 必须置于 rPr 最前）----------
B = r'D:\B166ER-openclaw\workspace\toolbox\_mk_chair_gongwen3.py'
t = open(B, encoding='utf-8').read()

OLD = """def set_font(run, ea, pt, bold=False):
    run.font.size = Pt(pt)
    run.font.bold = bold
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = rpr.makeelement(qn('w:rFonts'), {})
        rpr.append(rf)
    for a in ('w:ascii', 'w:hAnsi', 'w:eastAsia'):
        rf.set(qn(a), ea)"""

NEW = """def set_font(run, ea, pt, bold=False):
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = rpr.makeelement(qn('w:rFonts'), {})
        rpr.insert(0, rf)
    for a in ('w:ascii', 'w:hAnsi', 'w:eastAsia'):
        rf.set(qn(a), ea)
    run.font.size = Pt(pt)
    run.font.bold = bold"""

miss = 0
if OLD in t:
    t = t.replace(OLD, NEW, 1)
    print('set_font 已修正：rFonts 插入 rPr 首位')
else:
    print('!! set_font 未命中'); miss += 1
open(B, 'w', encoding='utf-8').write(t)

# ---------- 2. 轻度压缩 MD ----------
M = r'D:\B166ER-openclaw\workspace\tmp\_chair_gongwen.md'
m = open(M, encoding='utf-8').read()
REPL = [
 # 表3 内容列压缩
 ('品牌重塑、策展联营、基础信息化；外立面、结构与消防主体、屋面防水、设备机房与主干管线；首批客房与公共功能区一次做透',
  '品牌重塑、策展联营、基础信息化；外立面、结构与消防主体、屋面防水、设备机房与主干管线；首批客房与公区一次做透'),
 ('咨询量未提升，或数据颗粒度未建成，或首批客房出租率未破百分之四十五，不进第二步',
  '咨询量未提升，或数据颗粒度未建成，或首批客房出租率未破四成五，不进第二步'),
 ('投后十二个月出租率未破百分之四十五，冻结追加，转做运营', '投后十二个月出租率未破四成五，冻结追加，转做运营'),
 # 合并四（二）（三）
 ('（二）同一批空间内，隐蔽工程与饰面必须同批完成，不得先做隐蔽再分批饰体，否则开挖破坏；可独立先行的隐蔽工程，是后续不再进入的空间与部位。\n\n（三）每一步只放大上一步已验证的部分，未通过验证不得进入下一步。',
  '（二）同一批空间内，隐蔽工程与饰面必须同批完成，不得先做隐蔽再分批饰体，否则开挖破坏；可独立先行的隐蔽工程，是后续不再进入的空间与部位。每一步只放大上一步已验证的部分，未通过验证不得进入下一步。'),
 # 表2 数字化能力行并入二（三），表2 减一行
 ('| 数字化能力 | 一个体系筑牢运营护城河，类似华住：底座层统一，模块层按业态装配，输出层对外可售 |\n', ''),
 ('（三）数智化四场景为收益管理、会议与客源、渠道与内容、经营诊断与预警，验收标准一律是业务指标，不是模型指标；四步为先统一口径、不投系统，再单店贯通，再人工智能中台另立项，最后对外输出。',
  '（三）数字化能力是一个体系，筑牢运营护城河，类似华住：底座层统一，模块层按业态装配，输出层对外可售。四场景为收益管理、会议与客源、渠道与内容、经营诊断与预警，验收标准一律是业务指标，不是模型指标；四步为先统一口径、不投系统，再单店贯通，再人工智能中台另立项，最后对外输出。'),
]
for a, b in REPL:
    if a in m:
        m = m.replace(a, b, 1)
    else:
        print('!! MD 未命中: ' + a[:36]); miss += 1
open(M, 'w', encoding='utf-8').write(m)
print('MD 压缩完成，未命中累计 %d 处' % miss)

# ---------- 3. 重建并实测 ----------
r = subprocess.run([sys.executable, B], capture_output=True, text=True, encoding='utf-8', errors='replace')
print(r.stdout)
if r.stderr:
    print('STDERR:', r.stderr[:300])

# ---------- 4. 验证字体与分隔符 ----------
from docx import Document
from docx.oxml.ns import qn
DX = r'C:\Users\ericz\Desktop\产业发展部\给董事长的单独汇报\2026-11-21_发展赛道与存量改造路径_汇报要点.docx'
d = Document(DX)
from collections import Counter
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
print('分隔符 ‖ 残留: %d' % full.count('‖'))
print('段落 %d  表格 %d  大小 %.1f KB' % (len(d.paragraphs), len(d.tables), os.path.getsize(DX) / 1024))
print('')
print('=== 段落抽样 ===')
for i, p in enumerate(d.paragraphs[:14]):
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
        fs.append('%s「%s」' % (ea, rr.text[:16]))
    print('  P%-2d %s' % (i, ' + '.join(fs)[:150]))
