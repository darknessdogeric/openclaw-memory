# -*- coding: utf-8 -*-
"""按表头特征重算 v1.4 汇总计数并回写，重出 docx"""
import io, sys, os, re, subprocess, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

IMP = r'C:\\Users\\ericz\\Desktop\\产业发展部\\重要文件'.replace('\\\\', '\\')
KB7 = r'D:\\B166ER-openclaw\\workspace\\anyi-ops-kb\\07_战略与改革'.replace('\\\\', '\\')
MD = os.path.join(IMP, '2026-11-09_近期重点工作量化清单_v1.4.md')
MD_KB = os.path.join(KB7, '2026-11-09_近期重点工作量化清单_v1.4.md')
DX = os.path.join(IMP, '2026-11-09_近期重点工作量化清单_v1.4.docx')
CONV = r'D:\\B166ER-openclaw\\workspace\\skills\\docx-md-bridge\\scripts\\md_to_docx.py'.replace('\\\\', '\\')

L = open(MD, encoding='utf-8').read().split(chr(10))


def md_tables(lines):
    tabs, cur = [], []
    for l in lines:
        if l.startswith('| '):
            cur.append(l)
        else:
            if cur:
                tabs.append(cur)
            cur = []
    if cur:
        tabs.append(cur)
    return tabs


def second_cell(line):
    parts = line.split('|')
    return parts[2].strip() if len(parts) > 2 else ''


tabs = md_tables(L)
print('识别到表格块 %d 个' % len(tabs))


def find_tab(key):
    for t in tabs:
        if len(t) >= 2 and second_cell(t[0]) == key:
            return t
    return None


n_kn = n_wi = n_gap = n_act = 0
t = find_tab('日期')
if t:
    n_kn = len(t) - 2
t = find_tab('工作项')
if t:
    n_wi = len(t) - 2
t = find_tab('缺口')
if t:
    n_gap = len(t) - 2
t = find_tab('动作')
if t:
    n_act = len(t) - 2
print('计数：工作项 %d 项 / 关键节点 %d 个 / 缺口 %d 处 / 管理动作 %d 条' % (n_wi, n_kn, n_gap, n_act))

t2 = chr(10).join(L)
t2 = re.sub(r'(?m)^## 〇.*$',
            '## 〇　汇总：%d 项工作 · %d 个关键节点 · %d 处待补数据' % (n_wi, n_kn, n_gap), t2, count=1)
t2 = re.sub(r'(?m)^## 附：需补齐的 .*? 处量化缺口$',
            '## 附：需补齐的 %d 处量化缺口' % n_gap, t2, count=1)
open(MD, 'w', encoding='utf-8').write(t2)
shutil.copy2(MD, MD_KB)

r = subprocess.run([sys.executable, CONV, MD, DX], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('转换:', (r.stdout or '').strip(), (r.stderr or '').strip()[:160])
shutil.copy2(DX, os.path.join(KB7, os.path.basename(DX)))

from docx import Document
d = Document(DX)
cells, paras = set(), [x.text.strip() for x in d.paragraphs]
for tb in d.tables:
    for rr in tb.rows:
        for c in rr.cells:
            cells.add(c.text.strip())
print('DOCX %.1f KB  段落 %d  表格 %d' % (os.path.getsize(DX) / 1024, len(d.paragraphs), len(d.tables)))
print('--- 标题 ---')
for x in paras:
    if x.startswith('〇') or x.startswith('附：') or x.startswith('五、') or x.startswith('六、') or x.startswith('5.3') or x.startswith('6.5'):
        print('  ' + x)
print('--- 关键内容校验 ---')
for k in ['5.11', '5.12', '5.13', '5.14', '5.15', '4.5', '5.3　已闭环事项',
          '穿透式监管举措', '议题合规性审查', '十五五意见核销', '三项认领', '招采与合作合规自查',
          '5-2 至 5-5 期全文', '第15/20次总经会决议原文']:
    print('  %-24s %s' % (k, 'OK' if (k in cells or any(k in p for p in paras)) else 'MISSING'))
print('--- 附缺口表行数复核 ---')
for tb in d.tables:
    hdr = [c.text.strip() for c in tb.rows[0].cells]
    if len(hdr) > 1 and hdr[1] == '缺口':
        print('  附缺口表: %d 数据行（含表头共 %d）' % (len(tb.rows) - 1, len(tb.rows)))
    if len(hdr) > 1 and hdr[1] == '工作项':
        print('  工作项一览: %d 数据行' % (len(tb.rows) - 1))
    if len(hdr) > 1 and hdr[1] == '日期':
        print('  关键节点总表: %d 数据行' % (len(tb.rows) - 1))
