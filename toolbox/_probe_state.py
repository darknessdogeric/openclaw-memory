# -*- coding: utf-8 -*-
import io, sys, os, glob, hashlib
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document

W = r'D:\B166ER-openclaw\workspace'
PROJ = r'C:\Users\ericz\Desktop\产业发展部\项目\美团本地生活'
KB = r'D:\B166ER-openclaw\workspace\anyi\anyi-ops-kb\02_项目\安逸×美团本地生活合作'
DESK = r'C:\Users\ericz\Desktop'

print('=== 1. daily memory 文件状态 ===')
d = os.path.join(W, 'memory', '2026-11-06.md')
if os.path.exists(d):
    lines = open(d, encoding='utf-8').read().split('\n')
    print('行数 %d  大小 %d' % (len(lines), os.path.getsize(d)))
    print('--- 前 6 行 ---')
    for l in lines[:6]:
        print('   ', l[:100])
    print('--- 章节标题 ---')
    for l in lines:
        if l.startswith('##'):
            print('   ', l[:100])
else:
    print('缺失')
print()
print('memory 目录全部文件:')
for f in sorted(glob.glob(os.path.join(W, 'memory', '2026-1*.md'))):
    print('   %-16s %8d  %s' % (os.path.basename(f), os.path.getsize(f),
                                os.path.getmtime(f)))

print()
print('=== 2. 项目文件夹里 342KB 的那份是什么 ===')
big = os.path.join(PROJ, '安逸集团&美团充电宝战略合作框架协议_20261106.docx')
orig = os.path.join(KB, '10_乙方原版_安逸集团&美团充电宝战略合作框架协议.docx')
for label, fp in [('项目文件夹(342KB?)', big), ('KB归档对方原件', orig)]:
    if not os.path.exists(fp):
        print(' %s -> 缺失' % label)
        continue
    print(' %s: %d bytes' % (label, os.path.getsize(fp)))
    try:
        doc = Document(fp)
        txt = ''.join(p.text for p in doc.paragraphs)
        print('   段落 %d  表格 %d  正文字数 %d' % (len(doc.paragraphs), len(doc.tables), len(txt)))
        print('   首段: %s' % doc.paragraphs[0].text.strip()[:60])
        # 压缩包内是否有批注/修订
        import zipfile
        z = zipfile.ZipFile(fp)
        names = z.namelist()
        for key in ['word/comments.xml', 'word/people.xml']:
            print('   %s: %s' % (key, 'YES' if key in names else 'no'))
        media = [n for n in names if n.startswith('word/media/')]
        print('   内嵌媒体 %d 个: %s' % (len(media), media[:5]))
        # 修订标记
        xml = z.read('word/document.xml').decode('utf-8', 'ignore')
        print('   修订标记 ins=%d del=%d 批注引用=%d' % (
            xml.count('<w:ins '), xml.count('<w:del '), xml.count('commentReference')))
    except Exception as e:
        print('   读取失败:', e)
    print()

print('=== 3. 桌面根目录 + 锁文件 ===')
for f in sorted(glob.glob(os.path.join(DESK, '*美团*'))):
    if os.path.basename(f).startswith('~$'):
        continue
    print('   %-64s %8d' % (os.path.basename(f), os.path.getsize(f)))
for f in sorted(glob.glob(os.path.join(DESK, '~$*'))):
    print('   [LOCK] %s' % os.path.basename(f))
