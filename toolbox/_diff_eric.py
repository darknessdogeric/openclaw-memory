# -*- coding: utf-8 -*-
import io, sys, os, difflib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document

MINE = r'C:\Users\ericz\Desktop\产业发展部\项目\美团本地生活\安逸集团&美团充电宝战略合作框架协议_合并稿_20261106.docx'
ERIC = r'C:\Users\ericz\Desktop\产业发展部\项目\美团本地生活\安逸集团&美团充电宝战略合作框架协议_20261106.docx'


def paras(fp):
    d = Document(fp)
    return [p.text.strip() for p in d.paragraphs if p.text.strip()]


a = paras(MINE)
b = paras(ERIC)
print('我的合并稿: %d 段   Eric 版: %d 段' % (len(a), len(b)))
print()
print('=== 逐段差异 ===')
sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
changed = 0
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == 'equal':
        continue
    changed += 1
    print('--- [%s] 我的 p%d-%d  →  Eric p%d-%d ---' % (tag, i1, i2, j1, j2))
    for x in a[i1:i2]:
        print('   [我] %s' % x[:190])
    for x in b[j1:j2]:
        print('   [他] %s' % x[:190])
    print()
print('差异块数:', changed)

print()
print('=== 全文级对比（按字符）===')
ta = '\n'.join(a)
tb = '\n'.join(b)
print('我 %d 字 / 他 %d 字' % (len(ta), len(tb)))
if ta == tb:
    print('正文完全一致（差异仅在空段落或格式）')
else:
    sm2 = difflib.SequenceMatcher(None, ta, tb, autojunk=False)
    for tag, i1, i2, j1, j2 in sm2.get_opcodes():
        if tag == 'equal':
            continue
        print('--- [%s] ---' % tag)
        if i1 != i2:
            print('   [我] ...%s...' % ta[max(0, i1-40):i2+40].replace('\n', ' / '))
        if j1 != j2:
            print('   [他] ...%s...' % tb[max(0, j1-40):j2+40].replace('\n', ' / '))
