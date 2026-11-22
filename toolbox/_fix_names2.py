# -*- coding: utf-8 -*-
import io, sys, os, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

JX = glob.glob(r'D:\B166ER-openclaw\workspace\anyi-ops-kb\08_*\2026-10-26_*要点吸收*.md')[0]
t = open(JX, encoding='utf-8').read()

pairs = [
    # 校准表"转录稿写法"列必须保留转录时的错误写法
    ('| 1 | 丽呈集团 | **丽呈集团** |', '| 1 | 历程集团 | **丽呈集团** |'),
    ('| 2 | 岷山集团 | **岷山集团** |', '| 2 | 闽山集团 | **岷山集团** |'),
    # 第一节表格
    ('| 1 | **国宴（国堰）宾馆文化主题改造** |',
     '| 1 | **国堰宾馆**文化主题改造（转录稿误作国宴） |'),
    # 第四节净影响表
    ('历程本周交方案', '丽呈本周交方案'),
]
n = 0
for old, new in pairs:
    c = t.count(old)
    if c:
        t = t.replace(old, new); n += c
    else:
        print('   [未命中] ' + old[:44])
open(JX, 'w', encoding='utf-8').write(t)
print('纪要吸收: 修正 ' + str(n) + ' 处')

print()
print('=== 校准表最终形态 ===')
for i, l in enumerate(t.split('\n')):
    if l.startswith('| 1 | 历程') or l.startswith('| 2 | 闽山') or l.startswith('| 3 | 国宴'):
        print('  ' + l[:118])
print()
print('=== 第一节/第四节相关行 ===')
for l in t.split('\n'):
    if '国堰宾馆**文化主题改造' in l or '丽呈本周交方案' in l or '丽呈集团存量经营升级' in l:
        print('  ' + l[:130])
