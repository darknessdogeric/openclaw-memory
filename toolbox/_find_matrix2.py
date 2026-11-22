# -*- coding: utf-8 -*-
import io as _io
import sys, os, re, glob

_buf = _io.StringIO()
_stdout = sys.stdout
sys.stdout = _buf

KB = r'D:\B166ER-openclaw\workspace\anyi-ops-kb'
OUT = r'D:\B166ER-openclaw\workspace\tmp\_matrix2.txt'

FILES = [
 ('区域市场数据维度体系', ('04_方法论', '区域市场数据维度体系_v1.0_2026-10-11.md')),
 ('全部信源矩阵信息图1119', ('05_方法论', 'B166ER_全部信源矩阵信息图_v1.0_2026-11-19.md')),
 ('B166ER信源矩阵v1.1', ('00_安逸集团知识库总览', 'B166ER信源矩阵_v1.1_2026-10-11.md')),
 ('二销业务数据维度框架v1.2', ('02_项目', '安逸甄选', '安逸甄选二销业务数据维度框架_v1.2_2026-11-02.md')),
]
for tag, parts in FILES:
    p = os.path.join(KB, *parts)
    print('=' * 90)
    print('【%s】%s' % (tag, os.path.basename(p)))
    if not os.path.exists(p):
        print('  !! 缺失')
        continue
    t = open(p, encoding='utf-8', errors='replace').read()
    print('  长度 %d 字符' % len(t))
    for l in t.split('\n'):
        s = l.strip()
        if s.startswith('#'):
            print('   ' + s[:110])
        elif s.startswith('|') and 10 < len(s) < 230:
            print('    ' + s[:185])
        elif s.startswith('- ') and 12 < len(s) < 190:
            print('     ' + s[:180])
    print()

sys.stdout = _stdout
open(OUT, 'w', encoding='utf-8').write(_buf.getvalue())
print('已写入: ' + OUT + ' (' + str(os.path.getsize(OUT)) + ' B)')
