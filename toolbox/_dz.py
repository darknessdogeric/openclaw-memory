# -*- coding: utf-8 -*-
import io, sys, os, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
WS = 'D:\\B166ER-openclaw\\workspace'
KB = os.path.join(WS, 'anyi-ops-kb')
DESK = 'C:\\Users\\ericz\\Desktop\\产业发展部'

print('=== 1. 桌面 数智化目录 ===')
dz = os.path.join(DESK, '数智化')
if os.path.isdir(dz):
    for f in sorted(os.listdir(dz)):
        p = os.path.join(dz, f)
        if os.path.isdir(p):
            tag = 'DIR'
        else:
            tag = str(os.path.getsize(p) // 1024) + 'KB'
        print('  ' + f[:70] + '  ' + tag)
else:
    print('  无')

print('')
print('=== 2. 桌面 数智化相关 全部命中 ===')
for p in glob.glob(os.path.join(DESK, '**', '*数智*'), recursive=True):
    print('  ' + os.path.relpath(p, DESK)[:110])

print('')
print('=== 3. KB 智能网关项目目录 ===')
gw = os.path.join(KB, '02_项目', '酒店智能网关项目')
if os.path.isdir(gw):
    for f in sorted(os.listdir(gw)):
        p = os.path.join(gw, f)
        if os.path.isdir(p):
            print('  [DIR] ' + f)
        else:
            print('  ' + f[:60] + '  ' + str(os.path.getsize(p) // 1024) + 'KB')

print('')
print('=== 4. KB 检索：数字化一期/二期、中台、CRS ===')
PAT = re.compile(r'数字化二期|二期立项|中台|CRS')
HITS = []
for md in glob.glob(os.path.join(KB, '**', '*.md'), recursive=True):
    if '培训手册' in md or '00_全域商业市场认知' in md:
        continue
    try:
        t = open(md, encoding='utf-8', errors='replace').read()
    except Exception:
        continue
    if not PAT.search(t):
        continue
    score = sum(1 for k in ('数字化二期', '二期立项', '中台', 'CRS') if k in t)
    HITS.append((score, md, t))
HITS.sort(key=lambda x: -x[0])
for score, md, t in HITS[:14]:
    print('  [' + str(score) + '] ' + os.path.relpath(md, KB)[:100])

print('')
print('=== 5. 关键段落 ===')
KEY = ('数字化二期', '二期立项', '中台', 'CRS', '立项', '一期')
for score, md, t in HITS[:9]:
    print('-' * 92)
    print('【' + os.path.relpath(md, KB)[:98] + '】')
    n = 0
    for l in t.split('\n'):
        s = l.strip()
        if len(s) < 12 or s.startswith('|') or s.startswith('```'):
            continue
        if any(k in s for k in KEY):
            print('   * ' + s[:200])
            n += 1
            if n >= 8:
                break
