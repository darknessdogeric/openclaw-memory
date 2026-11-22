# -*- coding: utf-8 -*-
import io, sys, os, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn
KB = r'D:\B166ER-openclaw\workspace\anyi-ops-kb'

print('===== 1. 三份任职通知 =====')
for f in glob.glob(os.path.join(KB, '**', '*任职*.txt'), recursive=True):
    print('--- ' + os.path.basename(f) + ' ---')
    t = open(f, encoding='utf-8', errors='replace').read()
    print(t[:900])
    print()

print('===== 2. 第44周工作例会会议纪要.pdf =====')
try:
    import fitz
    p = glob.glob(r'C:\Users\ericz\Desktop\产业发展部\重要文件\*44周*')
    if not p:
        p = glob.glob(r'C:\Users\ericz\Desktop\产业发展部\重要文件\*.pdf')
    doc = fitz.open(p[0])
    txt = chr(10).join(pg.get_text() for pg in doc)
    print('文件:', os.path.basename(p[0]), ' 页数', doc.page_count, ' 字数', len(txt))
    import re
    for kw in ['试用', '转正', '新入职', '人才', '招聘', '干部']:
        for m in re.finditer(kw, txt):
            print('  [' + kw + '] ' + txt[max(0,m.start()-120):m.start()+180].replace(chr(10),' '))
            break
    print('--- 前 2500 字 ---')
    print(txt[:2500])
except Exception as e:
    print('PDF 读取失败:', e)

print()
print('===== 3. 新质生产力时代.docx =====')
try:
    d2 = Document(r'C:\Users\ericz\Desktop\新质生产力时代.docx')
    print('段落 %d 表格 %d' % (len(d2.paragraphs), len(d2.tables)))
    for x in d2.paragraphs[:60]:
        if x.text.strip():
            print('  ' + x.text.strip()[:160])
    for ti, tb in enumerate(d2.tables[:3], 1):
        print('--- 表 %d (%d x %d) ---' % (ti, len(tb.rows), len(tb.columns)))
        for r in tb.rows[:8]:
            print('  | ' + ' | '.join(c.text.strip().replace(chr(10),' / ')[:70] for c in r.cells))
except Exception as e:
    print('DOCX 读取失败:', e)