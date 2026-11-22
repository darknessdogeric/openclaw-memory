# -*- coding: utf-8 -*-
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
KB = r'D:\B166ER-openclaw\workspace\anyi-ops-kb'

FILES = [
 ('酒店名录三表', os.path.join(KB, '01_集团文件', '2026-09-16_安逸集团酒店名录三表内化_v1.0.md')),
 ('在营酒店清单', os.path.join(KB, '01_集团文件', '202609_安逸集团在营酒店清单_自有资产加轻资产_v1.0_2026-09-10.md')),
]

for tag, f in FILES:
    print('=' * 88)
    print('【' + tag + '】' + os.path.basename(f))
    if not os.path.exists(f):
        print('  !! 不存在'); continue
    t = open(f, encoding='utf-8', errors='replace').read()
    print('  长度 %d 字符' % len(t))
    lines = t.split(chr(10))
    tbl = [l for l in lines if l.strip().startswith('|')]
    print('  表格行 %d' % len(tbl))
    for l in tbl[:70]:
        print('   ' + l[:210])
    non = [l for l in lines if l.strip() and not l.strip().startswith('|') and not l.strip().startswith('#')]
    print('  --- 正文要点 ---')
    for l in non[:26]:
        print('   ' + l.strip()[:190])
    print()