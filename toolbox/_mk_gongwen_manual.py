# -*- coding: utf-8 -*-
"""使用说明 -> 标准公文格式 Word（GB/T 9704）+ 符号终检"""
import io, sys, os, re, subprocess, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import openpyxl
from docx import Document
from docx.shared import Pt
from docx.enum.text import WD_LINE_SPACING, WD_ALIGN_PARAGRAPH

XLSX = r'C:\Users\ericz\Desktop\附件5. 酒店经营预算模板-汇总版（空白模板）v1.0.xlsx'
MD_IN = r'D:\B166ER-openclaw\workspace\tmp\_cw_use_manual2.md'
MD_OUT = r'C:\Users\ericz\Desktop\附件5. 酒店经营预算模板（空白模板）v1.0_使用说明.md'
DX_OUT = r'C:\Users\ericz\Desktop\附件5. 酒店经营预算模板（空白模板）v1.0_使用说明.docx'
KB = r'D:\B166ER-openclaw\workspace\anyi-ops-kb\04_方法论\酒店经营预算模板'
CONV = r'D:\B166ER-openclaw\workspace\skills\gongwen-docx-cn\scripts\md2docx_gongwen.py'

INPUT_IDX = {3, 4, 5, 14, 18, 19, 21}
SUM_IDX = {1, 2, 7, 8, 9, 10, 11, 12}
FIN_IDX = {65, 66, 67}
ALLOC_IDX = {34, 61, 62, 63, 64, 68, 69, 71}

wb = openpyxl.load_workbook(XLSX, data_only=False)
rows = ['| 序号 | 工作表名称 | 层级 | 填数说明 |', '|---|---|---|---|']
cnt = {}
for i, ws in enumerate(wb.worksheets, 1):
    if i in INPUT_IDX:
        cat, tip = '输入层', '填各细分市场及档位的月度数据，为全表源头'
    elif i in FIN_IDX:
        if i in (66, 67):
            cat, tip = '财务三表', '上年三列为既定口径，自一月份起按月填写本年数据'
        else:
            cat, tip = '财务三表', '填写期初、期末余额及科目行次'
    elif i in SUM_IDX:
        cat, tip = '汇总层', '系统自动生成，不得手工修改'
    elif i in ALLOC_IDX:
        cat, tip = '分摊层', '填分摊基数与人数，其余由公式分摊'
    else:
        cat, tip = '部门层', '填一月至十二月的收入、成本、人工行'
    cnt[cat] = cnt.get(cat, 0) + 1
    rows.append('| %d | %s | %s | %s |' % (i, ws.title.replace('|', '／'), cat, tip))
table = '\n'.join(rows)

md = open(MD_IN, encoding='utf-8').read()
assert '<!--TABLE-->' in md
md = md.replace('<!--TABLE-->', table)
open(MD_OUT, 'w', encoding='utf-8').write(md)
print('公文正文 %d 字符，附表 %d 行' % (len(md), len(rows) - 2))
for k, v in sorted(cnt.items()):
    print('   %-6s %d 张' % (k, v))

r = subprocess.run([sys.executable, CONV, MD_OUT, DX_OUT], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('公文转换:', (r.stdout or '').strip(), (r.stderr or '').strip()[:200])

# ---------- 版式校准：28 磅固定行距 + 落款右对齐 ----------
d = Document(DX_OUT)
n = 0
for p in d.paragraphs:
    t = p.text.strip()
    if p.alignment is not None and str(p.alignment).endswith('CENTER'):
        continue
    pf = p.paragraph_format
    pf.line_spacing = Pt(28)
    pf.line_spacing_rule = WD_LINE_SPACING.EXACTLY
    n += 1
    if re.fullmatch(r'\d{4}\s*年\s*\d{1,2}\s*月', t):
        p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        pf.first_line_indent = None
d.save(DX_OUT)
print('行距校准段落 %d，落款日期已右对齐' % n)

os.makedirs(KB, exist_ok=True)
shutil.copy2(MD_OUT, os.path.join(KB, os.path.basename(MD_OUT)))
shutil.copy2(DX_OUT, os.path.join(KB, os.path.basename(DX_OUT)))
print('KB 已同步')

# ---------- 验证 ----------
d2 = Document(DX_OUT)
s = d2.sections[0]
print()
print('DOCX %.1f KB  段落 %d  表格 %d' % (os.path.getsize(DX_OUT) / 1024, len(d2.paragraphs), len(d2.tables)))
print('页边距 上%.2f 下%.2f 左%.2f 右%.2f cm' % (s.top_margin.cm, s.bottom_margin.cm, s.left_margin.cm, s.right_margin.cm))
from collections import Counter
from docx.oxml.ns import qn
c = Counter(); inds = Counter(); ls = Counter()
for p in d2.paragraphs:
    if p.text.strip():
        inds[str(p.paragraph_format.first_line_indent)] += 1
        ls[str(p.paragraph_format.line_spacing)] += 1
    for r in p.runs:
        if not r.text.strip():
            continue
        rpr = r._element.find(qn('w:rPr'))
        ea = sz = None
        if rpr is not None:
            f = rpr.find(qn('w:rFonts'))
            if f is not None:
                ea = f.get(qn('w:eastAsia'))
            s2 = rpr.find(qn('w:sz'))
            if s2 is not None:
                sz = int(s2.get(qn('w:val'))) / 2.0
        c[(ea, sz)] += 1
print('字体: ' + ' | '.join('%s/%s x%d' % (k[0], k[1], v) for k, v in c.most_common(6)))
print('首行缩进: ' + ' | '.join('%s x%d' % (k, v) for k, v in inds.most_common(3)))
print('行距: ' + ' | '.join('%s x%d' % (k, v) for k, v in ls.most_common(3)))

full = ''.join(p.text for p in d2.paragraphs) + '\n' + ''.join(cl.text for t in d2.tables for rr in t.rows for cl in rr.cells)
print()
print('--- 符号终检 ---')
SYM = ['★', '→', '←', '＋', '⚠', '☐', '☑', '√', '✓', '※', '－', '〔', '〕', '【', '】', '•', '·']
hit = [x for x in SYM if x in full]
print('  装饰符号残留: %s' % (','.join(hit) if hit else '无'))
print('  粗体标记残留: %s' % ('有' if '**' in full else '无'))
print('  竖线残留: %s' % ('有' if '|' in full else '无'))
print()
print('--- 内容完整性 ---')
for k in ['酒店经营预算模板（空白模板）使用说明', '一、模板基本情况', '二、模板结构', '三、标准部门损益表列结构',
          '四、填写顺序', '五、各表读法要点', '六、年度参数规则', '七、外部链接处理', '八、数据清洗情况',
          '九、使用注意事项', '十、常见问题', '附件', '工作表一览', '产业发展部', '2026 年 11 月',
          '18618', '40616', 'XXXX-4 年', 'B 至 M']:
    print('  %-28s %s' % (k, 'OK' if k in full else 'MISSING'))
tb = [t for t in d2.tables if t.rows and '工作表名称' in t.rows[0].cells[1].text]
print('  附表行数: %s' % (len(tb[0].rows) - 1 if tb else 'NOT FOUND'))
print('  首段: %s' % d2.paragraphs[0].text[:44])
print('  末段: %s' % d2.paragraphs[-1].text[:44])
