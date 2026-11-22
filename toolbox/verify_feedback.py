import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
content = open('anyi-ops-kb/garden-hotel-26-feedback-letter-20260804.md', encoding='utf-8').read()
print('Total chars:', len(content))
print()
keys = [
    '反馈意见函', '整改要求', '原则同意',
    '5 家', '不低于 5 家', '同定位竞对',
    '中高端精选有限服务', '中高端精选',
    'STR', 'MPI', 'ARI', 'RGI',
    '品牌化起点', '分级分类',
    '9 类客群', '5 个年龄段', '年龄段',
    '不替子公司做方案', '改造方案设计',
    '必答', '建议级',
    '整改意见'
]
print('=== 反馈函验证 ===')
for k in keys:
    cnt = content.count(k)
    print(f'  {k!r:25s}: {cnt}')

import re
sections = re.findall(r'^(## |### )(.*?)$', content, re.MULTILINE)
print(f'\n=== 章节数: {len(sections)} ===')
for prefix, title in sections[:40]:
    print(f'  {prefix} {title}')