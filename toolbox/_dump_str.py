# -*- coding: utf-8 -*-
import io, sys, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
TXT = r'D:\B166ER-openclaw\workspace\anyi-ops-kb\04_情报\2026-11-19_STR成都研讨会_全文抽取.txt'
t = open(TXT, encoding='utf-8', errors='replace').read()
print('长度 %d 字符' % len(t))
lines = [l.rstrip() for l in t.split('\n')]
print('')
print('=== 结构线索：含"结论/核心/洞察/页/板块/数据解码"等标记的行 ===')
for i, l in enumerate(lines):
    s = l.strip()
    if not s:
        continue
    if len(s) > 150:
        s = s[:150] + '…'
    if re.search(r'(结论|核心|洞察|第\s*\d+\s*页|PART|Part|一、|二、|三、|四、|五、|六、|七、|八、)', s):
        print('  L%-4d %s' % (i, s))
print('')
print('=== 全文前 9000 字（逐行）===')
cnt = 0
for i, l in enumerate(lines):
    s = l.rstrip()
    if len(s) > 200:
        s = s[:200] + '…'
    print('L%-4d %s' % (i, s))
    cnt += len(s)
    if cnt > 9000:
        break
