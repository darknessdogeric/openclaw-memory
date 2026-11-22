# -*- coding: utf-8 -*-
import io, sys, os, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
KB = r'D:\B166ER-openclaw\workspace\anyi-ops-kb'

P = os.path.join(KB, '10_外部合作', '2026-10-25_悦榕集团前来安逸酒店集团拜访_报告_v1.0.md')
print('=== 悦榕报告 ===')
if os.path.exists(P):
    t = open(P, encoding='utf-8', errors='replace').read()
    print('长度 %d 字符' % len(t))
    for l in t.split('\n'):
        s = l.strip()
        if s.startswith('#') or (len(s) > 20 and any(k in s for k in ('悦榕', '案例', '度假', '改造', '存量', '委托', '管理', '古尔沟', '三岔湖', '皇冠', '合作模式', '轻资产', '品牌'))):
            print('   ' + s[:230])
else:
    print('  !! 缺失')

print('')
print('=== KB 内悦榕相关其他文件 ===')
for md in glob.glob(os.path.join(KB, '**', '*.md'), recursive=True):
    b = os.path.basename(md)
    if '悦榕' in b or 'Banyan' in b:
        print('  ' + os.path.relpath(md, KB)[:110])

print('')
print('=== KB 内 悦榕 提及密集文件（含正文片段）===')
hits = []
for md in glob.glob(os.path.join(KB, '**', '*.md'), recursive=True):
    if '培训手册' in md:
        continue
    try:
        t = open(md, encoding='utf-8', errors='replace').read()
    except Exception:
        continue
    n = t.count('悦榕')
    if n >= 2:
        hits.append((n, md, t))
hits.sort(key=lambda x: -x[0])
for n, md, t in hits[:6]:
    print('  [%d] %s' % (n, os.path.relpath(md, KB)[:100]))
    for l in t.split('\n'):
        s = l.strip()
        if '悦榕' in s and len(s) > 16:
            print('      · ' + s[:200])
            break
