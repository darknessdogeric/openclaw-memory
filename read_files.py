import glob
import sys
sys.path.insert(0, 'C:\\Users\\Administrator\\.openclaw\\workspace\\skills\\doc-reader\\scripts')
from extract_doc import extract_pdf, extract_docx

output = []

# 1. 读取HAL相关PDF
files = glob.glob('C:\\Users\\Administrator\\Desktop\\自我革命\\下一代AI+去中心化旅游发展平台\\*.pdf')
for f in files:
    if 'FAQ' in f.upper():
        output.append('=== HAL 商业计划书 FAQ ===')
        output.append(extract_pdf(f))
        output.append('\n' + '='*50 + '\n')
        break

# 2. 读取温泉酒店
files = glob.glob('C:\\Users\\Administrator\\Desktop\\自我革命\\温泉酒店专题\\*.pdf')
for f in files[:1]:
    output.append('=== 温泉酒店协议客户AI方案 ===')
    output.append(extract_pdf(f))
    output.append('\n' + '='*50 + '\n')
    break

# 3. 读取导师提示词
files = glob.glob('C:\\Users\\Administrator\\Desktop\\自我革命\\导师项目提示词\\*.pdf')
for f in files[:1]:
    output.append('=== 导师端 Prompt ===')
    output.append(extract_pdf(f))
    output.append('\n' + '='*50 + '\n')
    break

# 写入输出文件
with open('C:\\Users\\Administrator\\.openclaw\\workspace\\temp_output.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print('输出完成')
