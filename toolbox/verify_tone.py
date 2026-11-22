import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
content = open('anyi-ops-kb/garden-hotel-26-feedback-letter-20260804.md', encoding='utf-8').read()
print('Total chars:', len(content))
print()
# 检查口吻:本部门 vs 我部 vs 个人引用
checks = [
    ('本部门', '+', '应该出现'),
    ('本部门', '+', '正确'),
    ('我部', '-', '不应该出现'),
    ('我', '-', '不应该出现'),
    ('我们', '-', '不应该出现'),
    ('Eric', '-', '不应该出现'),
    ('张实', '-', '落款已经修改'),
    ('贵公司', '+', '应该出现'),
    ('请贵公司', '+', '应该出现'),
    ('本函', '+', '应该出现'),
    ('特此函达', '+', '公文结束语'),
    ('安产业函〔2026〕21号', '+', '发文字号'),
    ('主送', '+', '主送单位'),
    ('抄送', '+', '抄送'),
]
print('=== 口吻校验 ===')
for kw, sign, note in checks:
    cnt = content.count(kw)
    print(f'  {sign} {kw!r:25s}: {cnt}  ({note})')

# 验证段落数
import re
sections = re.findall(r'^(## |### )(.*?)$', content, re.MULTILINE)
print(f'\n=== 章节数: {len(sections)} ===')