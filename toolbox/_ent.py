# -*- coding: utf-8 -*-
import io, sys, os, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
KB = 'D:\\B166ER-openclaw\\workspace\\anyi-ops-kb'

TARGETS = ['金桥两座', '金桥', '雁江', '普照山', '茶庄', '广川逸境', '广州逸境', '广州烜逸',
           '广州逸琪', '川汇实业', '蜀汉路', '天豪', '旅居锦都', '锦都悦宾', '洲际丽景',
           '安逸逸山', '逸山', '安逸汇', '锦城悦都', '锦森天成', '梦栖集', '安逸会管',
           '蒙顶山', '银星村', '三岔湖', '青白江', '彭祖湾']

FILES = []
for md in glob.glob(os.path.join(KB, '**', '*.md'), recursive=True):
    if '培训手册' in md or '00_全域商业市场认知' in md or '01_集团文件' in md:
        continue
    try:
        t = open(md, encoding='utf-8', errors='replace').read()
    except Exception:
        continue
    for nm in TARGETS:
        if nm in t:
            FILES.append((nm, md, t))

from collections import defaultdict
g = defaultdict(list)
for nm, md, t in FILES:
    g[nm].append((md, t))

for nm in TARGETS:
    lst = g.get(nm, [])
    if not lst:
        print('=== ' + nm + ' : KB 无命中 ===')
        continue
    print('=== ' + nm + '  (' + str(len(lst)) + ' 文件) ===')
    shown = 0
    for md, t in lst:
        lines = t.split('\n')
        for i, l in enumerate(lines):
            s = l.strip()
            if nm in s and len(s) > 10:
                ctx = ' / '.join(x.strip()[:60] for x in lines[max(0, i-1):i+2] if x.strip())[:180]
                print('   ' + os.path.basename(md)[:34] + ' | ' + ctx)
                shown += 1
                break
        if shown >= 3:
            break
    print('')
