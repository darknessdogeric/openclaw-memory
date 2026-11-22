# -*- coding: utf-8 -*-
import io, sys, os, re, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
KB = 'D:\\B166ER-openclaw\\workspace\\anyi-ops-kb'

NAMES = ['安逸合并', '安逸本部', '古尔沟', '总府皇冠', '深圳四川', '乐山锦江嘉州', '新良',
         '花园宾馆', '金桥', '华龙', '雁江', '茶庄', '广州烜逸', '广州逸琪', '蜀汉路',
         '国堰宾馆', '天府山庄', '亚丁宾馆', '安逸美舍', '鹧鸪', '旅居', '锦宾国际',
         '洲际丽景', '安逸茶山', '百丈湖', '青青园', '锦弘', '三岔湖', '锦城', '锦森',
         '天豪', '梦栖', '汇都', '梦']

print('=== 1. KB 命中公司名（确认主体对应）===')
found = {}
for md in glob.glob(os.path.join(KB, '**', '*.md'), recursive=True):
    if '培训手册' in md or '00_全域商业市场认知' in md:
        continue
    try:
        t = open(md, encoding='utf-8', errors='replace').read()
    except Exception:
        continue
    for nm in NAMES:
        if nm in t:
            found.setdefault(nm, []).append((os.path.relpath(md, KB), t.count(nm)))
for nm in NAMES:
    lst = found.get(nm, [])
    lst.sort(key=lambda x: -x[1])
    if lst:
        print('  %-10s %2d 文件  top: %s' % (nm, len(lst), lst[0][0][:78]))

print('')
print('=== 2. 一店一策 / 一企一策 相关文件 ===')
for md in glob.glob(os.path.join(KB, '**', '*.md'), recursive=True):
    b = os.path.basename(md)
    if any(k in b for k in ('一企一策', '一店一策', 'S01', 'S12', '策略词典')):
        print('  ' + os.path.relpath(md, KB)[:110])

print('')
print('=== 3. 一企一策范式 v1.0：策略词典 S01-S12 ===')
p = os.path.join(KB, '04_方法论', '一企一策分析范式_v1.0_2026-11-11.md')
if os.path.exists(p):
    t = open(p, encoding='utf-8', errors='replace').read()
    for l in t.split('\n'):
        s = l.strip()
        if s.startswith('|') and re.search(r'\bS\d\d\b', s):
            print('   ' + s[:190])
    print('')
    print('   --- 八条底线/关键段落 ---')
    n = 0
    for l in t.split('\n'):
        s = l.strip()
        if len(s) > 14 and not s.startswith('|') and not s.startswith('#') and not s.startswith('```'):
            if any(k in s for k in ('红线', '必须', '底线', '牵头', '节点', '动作', '顺序')):
                print('   * ' + s[:190]); n += 1
                if n >= 12:
                    break
