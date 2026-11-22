import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
content = open('anyi-ops-kb/garden-hotel-26-eval-20260804.md', encoding='utf-8').read()
chinese = sum(1 for c in content if '\u4e00' <= c <= '\u9fff')
print('Total chars:', len(content))
print('Chinese chars:', chinese)
print('ASCII ratio:', (len(content) - chinese) / len(content) * 100, '%')
# Check for v2 markers
print('Has "9 类客源":', '9 类客源' in content)
print('Has "门散":', '门散' in content)
print('Has "新媒体团队":', '新媒体团队' in content)
print('Has "开放式卫生间":', '开放式卫生间' in content)
print('Has "亚朵 3.0":', '亚朵 3.0' in content)
print('Has "Eric 部长订正":', 'Eric 部长订正' in content)
# Show end
print('=== Last 500 chars ===')
print(content[-500:])