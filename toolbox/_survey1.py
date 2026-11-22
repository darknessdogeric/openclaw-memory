# -*- coding: utf-8 -*-
import io, sys, os, re, glob, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
WS = r'D:\B166ER-openclaw\workspace'
KB = os.path.join(WS, 'anyi-ops-kb')
DESK = r'C:\Users\ericz\Desktop\产业发展部'

print('=== A. 桌面产业发展部 目录树（2层）===')
for root, dirs, files in os.walk(DESK):
    lvl = root[len(DESK):].count(os.sep)
    if lvl > 2:
        dirs[:] = []
        continue
    rel = root[len(DESK):] or '产业发展部'
    print('  ' * lvl + '[' + os.path.basename(root) + ']  files=' + str(len(files)))

print()
print('=== B. 新媒体采集目录（酒店账号名单）===')
nm = os.path.join(DESK, '新媒体业务', '下属酒店新媒体现状采集')
if os.path.isdir(nm):
    for f in sorted(os.listdir(nm))[:40]:
        print('  ' + f[:90])
else:
    print('  未找到', nm)

print()
print('=== C. KB 中所有 md 文件名（找台账/名单）===')
mds = glob.glob(os.path.join(KB, '**', '*.md'), recursive=True)
print('  共 %d 个' % len(mds))
KEY = ['台账', '名单', '清单', '一企一策', '酒店', '项目', '摸排', '资产', '委管', '自营', '一览']
for m in sorted(mds):
    b = os.path.basename(m)
    if any(k in b for k in KEY):
        print('  ' + os.path.relpath(m, KB)[:110])
