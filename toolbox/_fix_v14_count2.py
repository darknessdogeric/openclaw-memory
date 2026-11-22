# -*- coding: utf-8 -*-
"""从 Word 表格直接读数，回写 v1.4 汇总标题，并打印附缺口表尾部核对"""
import io, sys, os, re, subprocess, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document

IMP = r'C:\Users\ericz\Desktop\产业发展部\重要文件'
KB7 = r'D:\B166ER-openclaw\workspace\anyi-ops-kb\07_战略与改革'
MD = os.path.join(IMP, '2026-11-09_近期重点工作量化清单_v1.4.md')
MD_KB = os.path.join(KB7, '2026-11-09_近期重点工作量化清单_v1.4.md')
DX = os.path.join(IMP, '2026-11-09_近期重点工作量化清单_v1.4.docx')
CONV = r'D:\B166ER-openclaw\workspace\skills\docx-md-bridge\scripts\md_to_docx.py'


def conv(src, dst):
    r = subprocess.run([sys.executable, CONV, src, dst], capture_output=True, text=True, encoding='utf-8', errors='replace')
    return (r.stdout or '').strip(), (r.stderr or '').strip()[:160]


def count_by_docx(path):
    d = Document(path)
    res = {}
    for tb in d.tables:
        hdr = [c.text.strip() for c in tb.rows[0].cells]
        if len(hdr) > 1:
            k = hdr[1]
            if k in ('日期', '工作项', '缺口', '动作') and k not in res:
                res[k] = len(tb.rows) - 1
    return res, d


# 第 1 遍：转临时 docx 读数
TMP = r'D:\B166ER-openclaw\workspace\tmp\_v14_tmp.docx'
print(conv(MD, TMP)[0])
cnt, _ = count_by_docx(TMP)
print('Word 实测: 工作项 %s 项 / 关键节点 %s 个 / 缺口 %s 处 / 管理动作 %s 条'
      % (cnt.get('工作项'), cnt.get('日期'), cnt.get('缺口'), cnt.get('动作')))

n_wi = cnt.get('工作项', 0)
n_kn = cnt.get('日期', 0)
n_gap = cnt.get('缺口', 0)
n_act = cnt.get('动作', 0)

t = open(MD, encoding='utf-8').read()
t = re.sub(r'(?m)^## 〇.*$',
            '## 〇　汇总：%d 项工作 · %d 个关键节点 · %d 处待补数据' % (n_wi, n_kn, n_gap), t, count=1)
t = re.sub(r'(?m)^## 附：需补齐的 .*? 处量化缺口$',
            '## 附：需补齐的 %d 处量化缺口' % n_gap, t, count=1)
open(MD, 'w', encoding='utf-8').write(t)
shutil.copy2(MD, MD_KB)
print('标题已回写')

# 第 2 遍：最终 docx
print(conv(MD, DX)[0])
shutil.copy2(DX, os.path.join(KB7, os.path.basename(DX)))

# 校验
cnt2, d2 = count_by_docx(DX)
paras = [x.text.strip() for x in d2.paragraphs]
cells = set()
for tb in d2.tables:
    for rr in tb.rows:
        for c in rr.cells:
            cells.add(c.text.strip())
print()
print('DOCX %.1f KB  段落 %d  表格 %d' % (os.path.getsize(DX) / 1024, len(d2.paragraphs), len(d2.tables)))
print('表格实测: ' + ' | '.join('%s=%d' % (k, v) for k, v in cnt2.items()))
print('--- 标题 ---')
for x in paras:
    if x.startswith('〇') or x.startswith('附：') or x.startswith('5.3') or x.startswith('6.5'):
        print('  ' + x)
print('--- 关键内容 ---')
allc = chr(10).join(cells) + chr(10) + chr(10).join(paras)
for k in ['5.11', '5.12', '5.13', '5.14', '5.15', '4.5', '5.3　已闭环事项',
          '穿透式监管举措', '议题合规性审查', '十五五意见核销', '三项认领', '招采与合作合规自查',
          '5-2 至 5-5', '第15/20次总经会决议原文', '成熟一个、上报一个']:
    print('  %-24s %s' % (k, 'OK' if k in allc else 'MISSING'))
print('--- 附缺口表最后 4 行 ---')
for tb in d2.tables:
    hdr = [c.text.strip() for c in tb.rows[0].cells]
    if len(hdr) > 1 and hdr[1] == '缺口':
        for rr in list(tb.rows)[-4:]:
            print('  | ' + ' | '.join(c.text.strip()[:46] for c in rr.cells))
