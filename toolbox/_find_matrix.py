# -*- coding: utf-8 -*-
"""检索信源矩阵与行业数据维度分析（输出落文件，避免控制台编码问题）"""
import io as _io
import sys, os, re, glob

_buf = _io.StringIO()
_stdout = sys.stdout
sys.stdout = _buf

KB = r'D:\B166ER-openclaw\workspace\anyi-ops-kb'
OUT = r'D:\B166ER-openclaw\workspace\tmp\_matrix_out.txt'

print('=== 1. 检索：数据维度 / 维度分析 / 信源矩阵 / 全景图 ===')
for md in glob.glob(os.path.join(KB, '**', '*.md'), recursive=True):
    b = os.path.basename(md)
    if any(k in b for k in ('数据维度', '维度分析', '信源矩阵', '全景图', '全景拓扑', '指标体系', '数据体系')):
        print('  ' + os.path.relpath(md, KB)[:112])

print('')
print('=== 2. 抓取核心文件结构 ===')
FILES = [
 ('信源矩阵', ('00_全域商业市场认知', '01_酒店行业', '信源矩阵_酒店行业复苏判断排查总表_v1.0_2026-11-10.md')),
 ('行业复苏含西南', ('00_全域商业市场认知', '01_酒店行业', '酒店行业复苏时点判断_v4.1_含西南维度_2026-11-10.md')),
 ('STR对标法竞对', ('02_项目', '国堰宾馆文创改造', '深度抓取_2026-08-08', 'v1.4_STR对标法专业竞对分析.md')),
 ('STR体系内化', ('04_方法论', '方法论书籍内化', '《STR全球酒店指数体系》核心内化笔记_v1.0_2026-10-11.md')),
]
for tag, parts in FILES:
    p = os.path.join(KB, *parts)
    print('')
    print('-' * 88)
    print('【%s】%s' % (tag, os.path.basename(p)))
    if not os.path.exists(p):
        print('  !! 缺失')
        continue
    t = open(p, encoding='utf-8', errors='replace').read()
    print('  长度 %d 字符' % len(t))
    hs = [l.strip() for l in t.split('\n') if l.strip().startswith('#')]
    for h in hs[:26]:
        print('   ' + h[:104])
    tb = [l.strip() for l in t.split('\n') if l.strip().startswith('|')]
    if tb:
        print('   --- 表格首 10 行 ---')
        for l in tb[:10]:
            print('    ' + l[:185])

print('')
print('=== 3. 全库中「维度」相关的成套件清单（文件大小）===')
for md in sorted(glob.glob(os.path.join(KB, '00_全域商业市场认知', '**', '*.md'), recursive=True)):
    print('  %8d B  %s' % (os.path.getsize(md), os.path.relpath(md, KB)[:100]))

sys.stdout = _stdout
open(OUT, 'w', encoding='utf-8').write(_buf.getvalue())
print('已写入: ' + OUT + '  (' + str(os.path.getsize(OUT)) + ' B)')
