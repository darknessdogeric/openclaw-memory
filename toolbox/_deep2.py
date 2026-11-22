# -*- coding: utf-8 -*-
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
KB = 'D:\\B166ER-openclaw\\workspace\\anyi-ops-kb'

def show(path, tag, hmax=40, tmax=60, tbl_start=None, tbl_end=None, only_tables=False):
    print('=' * 96)
    print('【' + tag + '】')
    if not os.path.exists(path):
        print('  !! 缺失:', path); return
    t = open(path, encoding='utf-8', errors='replace').read()
    lines = t.split(chr(10))
    print('  长度 %d 字符 / %d 行' % (len(t), len(lines)))
    print('  --- 结构 ---')
    for h in [l for l in lines if l.strip().startswith('#')][:hmax]:
        print('   ' + h.strip()[:100])
    print('  --- 表格 ---')
    n = 0
    for i, l in enumerate(lines):
        s = l.strip()
        if not s.startswith('|'):
            continue
        if tbl_start is not None and i < tbl_start:
            continue
        if tbl_end is not None and i > tbl_end:
            continue
        print('   ' + s[:185])
        n += 1
        if n >= tmax:
            break
    print()

# 1) 董事长命题主文档
show(os.path.join(KB, '07_战略与改革', '十五五战略定位研究',
      '07_董事长要求_生活方式酒店具体模型_前台后台双层架构_v1.0.md'),
     '董事长要求_在地文化生活方式酒店_前台后台双层架构 v1.3',
     hmax=44, tmax=72)

# 2) 7家酒店周报（数据层）
show(os.path.join(KB, '07_战略与改革', '十五五战略定位研究',
      '06_7家酒店周报调研纪要与集团认知_v0.6_2026-08-14.md'),
     '7家酒店周报调研纪要与集团认知 v0.6',
     hmax=16, tmax=60)
