import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
content = open('anyi-ops-kb/garden-hotel-26-eval-20260804.md', encoding='utf-8').read()
print('Total chars:', len(content))
keys = ['9 类客源', '门散', '新媒体团队', '开放式卫生间', '亚朵 3.0', 'Eric 部长订正', '年龄段', '1.5 【Eric', '同档对标', 'v2 订正']
print('=== v2 verification ===')
for k in keys:
    print(f'  {k!r:25s}: {content.count(k)}')

# Check section structure
import re
sections = re.findall(r'^(## |### )(.+?)$', content, re.MULTILINE)
print(f'\n=== Section count: {len(sections)} ===')
for prefix, title in sections[:30]:
    print(f'  {prefix} {title}')