# -*- coding: utf-8 -*-
import io, sys, os, glob, shutil, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DESK = r'C:\Users\ericz\Desktop'
cands = [x for x in glob.glob(os.path.join(DESK, '*战略合作框架协议*'))
         if not os.path.basename(x).startswith('~$')]
for c in sorted(cands):
    print('%-12s %10d  %s' % ('FILE' if c.endswith('.docx') else 'LOCK', os.path.getsize(c), c))

lock = [x for x in glob.glob(os.path.join(DESK, '~$*'))]
print()
print('锁文件:', lock if lock else '无')

# 尝试写入测试
target = [x for x in cands if x.endswith('_合并稿_20261106.docx')]
if target:
    t = target[0]
    try:
        with open(t, 'r+b') as fh:
            fh.seek(0, 2)
        print('目标可写(R+W):', t)
    except Exception as e:
        print('目标被占用:', type(e).__name__, e)
