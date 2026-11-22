# -*- coding: utf-8 -*-
"""生成使用说明（含 71 张表清单）并转 Word"""
import io, sys, os, re, subprocess, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import openpyxl

XLSX = r'C:\Users\ericz\Desktop\附件5. 酒店经营预算模板-汇总版（空白模板）v1.0.xlsx'
MD_IN = r'D:\B166ER-openclaw\workspace\tmp\_cw_use_manual.md'
MD_OUT = r'C:\Users\ericz\Desktop\附件5. 酒店经营预算模板（空白模板）v1.0_使用说明.md'
DX_OUT = r'C:\Users\ericz\Desktop\附件5. 酒店经营预算模板（空白模板）v1.0_使用说明.docx'
KB = r'D:\B166ER-openclaw\workspace\anyi-ops-kb\04_方法论\酒店经营预算模板'
CONV = r'D:\B166ER-openclaw\workspace\skills\docx-md-bridge\scripts\md_to_docx.py'

# 序号 -> (类别, 填数说明)
CAT = {}
INPUT_IDX = {3, 4, 5, 14, 18, 19, 21}
SUM_IDX = {1, 2, 7, 8, 9, 10, 11, 12}
FIN_IDX = {65, 66, 67}
ALLOC_IDX = {34, 61, 62, 63, 64, 68, 69, 71}

wb = openpyxl.load_workbook(XLSX, data_only=False)
rows = ['| 序号 | 工作表 | 类别 | 填数说明 |', '|---|---|---|---|']
cnt = {}
for i, ws in enumerate(wb.worksheets, 1):
    if i in INPUT_IDX:
        cat, tip = '市场细分输入', '填各细分市场/分档的月度数据，为全表源头'
    elif i in FIN_IDX:
        if i in (66, 67):
            cat, tip = '财务三表', 'C/D/E 为上年口径；**F 列起按月填本年**，行次与科目行需补'
        else:
            cat, tip = '财务三表', '期初、期末、科目行次需补（D–K 列）'
    elif i in SUM_IDX:
        cat, tip = '汇总／报表', '**全自动，勿手改**'
    elif i in ALLOC_IDX:
        cat, tip = '分摊／人工', '填分摊基数与人数，其余由公式分摊'
    else:
        cat, tip = '部门损益表', '填 B–M（1–12 月）收入、成本、人工行'
    cnt[cat] = cnt.get(cat, 0) + 1
    rows.append('| %d | %s | %s | %s |' % (i, ws.title.replace('|', '／'), cat, tip))
table = '\n'.join(rows)

md = open(MD_IN, encoding='utf-8').read()
assert '<!--TABLE-->' in md
md = md.replace('<!--TABLE-->', table)
open(MD_OUT, 'w', encoding='utf-8').write(md)
print('说明 MD: %d 字符，表清单 %d 行' % (len(md), len(rows) - 2))
for k, v in sorted(cnt.items()):
    print('   %-12s %d 张' % (k, v))

r = subprocess.run([sys.executable, CONV, MD_OUT, DX_OUT], capture_output=True, text=True, encoding='utf-8', errors='replace')
print('转换:', (r.stdout or '').strip(), (r.stderr or '').strip()[:200])
os.makedirs(KB, exist_ok=True)
shutil.copy2(MD_OUT, os.path.join(KB, os.path.basename(MD_OUT)))
shutil.copy2(DX_OUT, os.path.join(KB, os.path.basename(DX_OUT)))
print('KB 已同步')

# ---------- 验证 ----------
import docx
d = docx.Document(DX_OUT)
full = ''.join(p.text for p in d.paragraphs) + '\n' + ''.join(c.text for t in d.tables for r in t.rows for c in r.cells)
print()
print('DOCX %.1f KB  段落 %d  表格 %d  字数 %d' % (os.path.getsize(DX_OUT) / 1024, len(d.paragraphs), len(d.tables), len(full)))
checks = ['使用说明', 'XXX年', 'XXXX-1年', 'XXXX-4年', '外部链接', 'fullCalcOnLoad',
          '18,618', '40,616', '276 处', 'B – M', 'Full Year', 'Total 酒店汇总表', 'P&L Summary',
          '第 44 周', '序号', '71 张']
for k in checks:
    print('  %-20s %s' % (k, 'OK' if k in full else 'MISSING'))
# 表格清单是否 71 行
hit = [t for t in d.tables if t.rows and '工作表' in t.rows[0].cells[1].text]
print('  表清单行数: %s' % (len(hit[0].rows) - 1 if hit else 'NOT FOUND'))
print('  文件: %s  %.1f KB' % (os.path.basename(DX_OUT), os.path.getsize(DX_OUT) / 1024))
