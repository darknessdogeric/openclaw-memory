# -*- coding: utf-8 -*-
import io, sys, os, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document
from docx.oxml.ns import qn

D = r'C:\Users\ericz\Desktop\产业发展部\重要文件\重要项目情况'
OUT = r'D:\B166ER-openclaw\workspace\tmp\_proj_txt'

# ---------- 1. docx 全量抽取 ----------
f1 = glob.glob(os.path.join(D, '*.docx'))[0]
d = Document(f1)
lines = []
for ch in d.element.body.iterchildren():
    if ch.tag == qn('w:p'):
        p = None
        for x in d.paragraphs:
            if x._element is ch:
                p = x
                break
        if p is not None and p.text.strip():
            st = p.style.name if p.style is not None else ''
            lines.append(('[%s] ' % st if st and st != 'Normal' else '') + p.text.strip())
    elif ch.tag == qn('w:tbl'):
        t = None
        for x in d.tables:
            if x._tbl is ch:
                t = x
                break
        if t is not None:
            lines.append('--- 表格 ---')
            for r in t.rows:
                lines.append(' | '.join(c.text.strip().replace('\n', ' / ')[:70] for c in r.cells))
            lines.append('--- /表格 ---')
txt = '\n'.join(lines)
open(os.path.join(OUT, 'chain.txt'), 'w', encoding='utf-8').write(txt)
print('=== 安逸连锁 docx：段落 %d 表格 %d 抽取 %d 字符 -> chain.txt ===' % (len(d.paragraphs), len(d.tables), len(txt)))
print(txt[:5000])

# ---------- 2. .doc 签名探测 ----------
f2 = glob.glob(os.path.join(D, '*.doc'))
if f2:
    p = f2[0]
    head = open(p, 'rb').read(8)
    sig = head.hex()
    print()
    print('=== 古尔沟 .doc ===')
    print('文件: %s  %.1f MB' % (os.path.basename(p), os.path.getsize(p) / 1024 / 1024))
    print('前 8 字节: %s' % sig)
    kind = 'OLE2 复合文档(真 .doc)' if head[:4] == b'\xd0\xcf\x11\xe0' else ('RTF' if head[:5] == b'{\\rtf' else ('HTML/纯文本' if head[:5].lower()[:5] == b'<html' or head[:1] == b'<' else '未知'))
    print('判定: %s' % kind)
else:
    print('未找到 .doc')

# ---------- 3. KB 来源台账 ----------
print()
print('=== KB 来源台账 ===')
for c in glob.glob(r'D:\B166ER-openclaw\workspace\anyi-ops-kb\**\00_来源台账*.md', recursive=True):
    print('路径: %s  %.1f KB' % (c, os.path.getsize(c) / 1024))
    t = open(c, encoding='utf-8', errors='replace').read()
    print('--- 前 1800 字 ---')
    print(t[:1800])
