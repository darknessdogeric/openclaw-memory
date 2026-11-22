# -*- coding: utf-8 -*-
import io, sys, os, re, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn

KB = r'D:\B166ER-openclaw\workspace\anyi-ops-kb'
DOCX = os.path.join(KB, '04_情报', 'STR成都研讨会数据吸收与工作校准_v1.0_2026-11-20.docx')
TXT = os.path.join(KB, '04_情报', '2026-11-19_STR成都研讨会_全文抽取.txt')

print('=== A. 11-20 工作校准 DOCX ===')
d = Document(DOCX)
print('段落 %d  表格 %d' % (len(d.paragraphs), len(d.tables)))
print('')
print('--- 结构 ---')
for p in d.paragraphs:
    t = p.text.strip()
    st = p.style.name if p.style is not None else ''
    if t and ('Head' in st or '标题' in st or 'Title' in st):
        print('  ' + t[:110])
print('')
print('--- 表格 ---')
for ti, tb in enumerate(d.tables):
    print('  [表 %d] %d 行 x %d 列' % (ti + 1, len(tb.rows), len(tb.columns)))
    for row in tb.rows[:14]:
        cells = [c.text.strip().replace('\n', ' ')[:36] for c in row.cells]
        line = ' | '.join([c for c in cells if c])
        if line:
            print('      ' + line[:200])
print('')
print('--- 正文要点 ---')
n = 0
for p in d.paragraphs:
    t = p.text.strip()
    if len(t) > 24 and not t.startswith('|'):
        print('  · ' + t[:240])
        n += 1
        if n >= 22:
            break

print('')
print('=== B. 11-19 seminar 全文抽取（章节与关键维度）===')
if os.path.exists(TXT):
    t = open(TXT, encoding='utf-8', errors='replace').read()
    print('长度 %d 字符' % len(t))
    heads = re.findall(r'(?m)^[^\n]{0,80}(?:Part |PART |Chapter |第[一二三四五六七八九十]+[章节部分]|\d+\.\d+|\d+、)[^\n]{0,90}$', t)
    print('--- 识别到的章节标题 %d 条 ---' % len(heads))
    for h in heads[:40]:
        s = h.strip()
        if s:
            print('  ' + s[:110])
    print('')
    print('--- 维度关键词频次 ---')
    KW = ['RevPAR', 'ADR', 'OCC', '入住率', '房价', '出租率', '可售房', '间夜', '同店', '可比',
          '市场码', '档次', '连锁', '单店', '集团', '样本', '渗透率', '供给', '需求', '库存',
          '淡季', '旺季', '月', '周', '预测', '曼哈顿', '加权平均', '排名', '分层']
    for k in KW:
        c = t.count(k)
        if c:
            print('  %-10s %d' % (k, c))
else:
    print('  !! 缺失')
