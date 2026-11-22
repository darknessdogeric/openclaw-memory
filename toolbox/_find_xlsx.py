# -*- coding: utf-8 -*-
import io, sys, os, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
KB = r'D:\B166ER-openclaw\workspace\anyi-ops-kb'
DESK = r'C:\Users\ericz\Desktop\产业发展部'

print('=== 1. 找原始 xlsx 名录（最权威）===')
pats = ['*在营酒店*', '*直营酒店*', '*轻资产在管*', '*酒店名录*']
hits = []
for p in pats:
    hits += glob.glob(os.path.join(DESK, '**', p), recursive=True)
    hits += glob.glob(os.path.join(KB, '**', p), recursive=True)
for h in sorted(set(hits))[:20]:
    print('  ' + os.path.relpath(h, DESK)[:120] + '   [' + str(os.path.getsize(h)//1024) + ' KB]')

print()
print('=== 2. 重要文件目录 xlsx 清单 ===')
imp = os.path.join(DESK, '重要文件')
for f in sorted(os.listdir(imp))[:45]:
    p = os.path.join(imp, f)
    print('  %-70s %s' % (f[:70], ('DIR' if os.path.isdir(p) else str(os.path.getsize(p)//1024)+'KB')))

print()
print('=== 3. KB _原始文件 归档 ===')
raw = os.path.join(KB, '01_集团文件', '_原始文件')
if os.path.isdir(raw):
    for f in sorted(os.listdir(raw)):
        print('  ' + f[:100])
else:
    print('  目录不存在')
