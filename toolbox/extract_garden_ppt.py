"""读取 PPT 内容到文件"""
content = open(r'D:\B166ER-OpenClaw\workspace\toolbox\garden_ppt.txt', 'r', encoding='utf-8').read()
# 写到 UTF-8 BOM 文件（避免编码问题）
with open(r'D:\B166ER-OpenClaw\workspace\toolbox\garden_ppt_safe.txt', 'w', encoding='utf-8') as f:
    f.write(content)
print(f'OK: {len(content)} 字')