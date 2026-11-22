# -*- coding: utf-8 -*-
import io, sys, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
p = r'C:\Users\ericz\Desktop\安逸酒店集团与美团合作框架协议_起草稿_20261029.docx'
d = Document(p)
f = ''.join(x.text for x in d.paragraphs)
print('=== 第一条 各项标题 ===')
for x in d.paragraphs:
    t = x.text.strip()
    if t and t[0].isdigit() and len(t) > 3 and t[1] == chr(0xFF0E):
        print('  ' + t[:36])
print()
print('=== 新增条目全文 ===')
for x in d.paragraphs:
    t = x.text.strip()
    if t.startswith('3' + chr(0xFF0E) + '充电宝箱体'):
        print(t)
print()
for k in ['标识纹样','设计图案','箱体定制','书面确认','户外场地','另行业务合同约定','享有知识产权','不得用于其他客户','终止时','清理或更换']:
    print('  %-22s %s' % (k, 'OK' if k in f else 'MISSING'))
print()
print('段落 %d  表格 %d  字数 %d  大小 %.1f KB' % (len(d.paragraphs), len(d.tables), len(f), os.path.getsize(p)/1024))