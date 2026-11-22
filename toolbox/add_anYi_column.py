"""给 3 个调研模板加 '安逸集团有无' 列 + '现有程度' 列"""
import re
from pathlib import Path

WORKSPACE = Path(r'D:\B166ER-OpenClaw\workspace\anyi-ops-kb\06_调研')

TEMPLATES = [
    WORKSPACE / '调研模板_01_上级单位_2026-08-01.md',
    WORKSPACE / '调研模板_02_集团_2026-08-01.md',
    WORKSPACE / '调研模板_03_旗下酒店_2026-08-01.md',
]

# 需要替换的 5 列表头, 替换为 7 列表头
# 5 列: | # | 调研项 | 数据来源 | 输出形式 | 备注 |
# 7 列: | # | 调研项 | 数据来源 | 输出形式 | 安逸集团有无 | 现有程度 | 备注 |

OLD_HEADER = '| # | 调研项 | 数据来源 | 输出形式 | 备注 |'
NEW_HEADER = '| # | 调研项 | 数据来源 | 输出形式 | 安逸集团有无 | 现有程度 | 备注 |'

# 同时替换变体（有些表用 --- 而不是 |---|------|---------|------|）
OLD_HEADER_2 = '| # | 调研项 | 数据来源 | 输出形式 | 备注 |---|--------|---------|---------|------|'
NEW_HEADER_2 = '| # | 调研项 | 数据来源 | 输出形式 | 安逸集团有无 | 现有程度 | 备注 |---|--------|---------|---------|------|---------|------|'

# 转换分隔行 (5 列 → 7 列)
# 旧: |---|--------|---------|---------|------|
# 新: |---|--------|---------|---------|---------|------|------|
OLD_SEPARATOR = '|---|--------|---------|---------|------|'
NEW_SEPARATOR = '|---|--------|---------|---------|---------|------|------|'

for template_path in TEMPLATES:
    print(f"\n=== {template_path.name} ===")
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_size = len(content)

    # 替换表头
    content = content.replace(OLD_HEADER, NEW_HEADER)
    # 替换分隔行
    content = content.replace(OLD_SEPARATOR, NEW_SEPARATOR)

    # 替换表格行 - 把列数从 5 增加到 7
    # 模式: | 1.1 | 内容 | 来源 | 输出 | 备注 | → | 1.1 | 内容 | 来源 | 输出 | ⚪ 待调研 | | 备注 |
    # 匹配: | 数字 | 文本 | 文本 | 文本 | 文本 |
    pattern = r'(\| (\d+(?:\.\d+)?) \| (((?:[^|\n]|\|[^|\n])+?)) \|) ((?:[^|\n]|\|[^|\n])+?) \| ((?:[^|\n]|\|[^|\n])+?) \| ((?:[^|\n]|\|[^|\n])+?) \|'
    replacement = r'\1 \4 | \5 | ⚪ 待调研 | \6 |'

    new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
    if new_content != content:
        content = new_content
        print(f"  表格行已扩展")

    # 保存
    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(content)

    new_size = len(content)
    print(f"  大小: {original_size} → {new_size}")
    print(f"  增加: +{new_size - original_size} chars")

print("\n=== 完成 ===")
