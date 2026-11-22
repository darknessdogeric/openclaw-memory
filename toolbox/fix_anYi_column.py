"""精确修正 3 个调研模板的"安逸集团有无"列"""
import re
from pathlib import Path

WORKSPACE = Path(r'D:\B166ER-OpenClaw\workspace\anyi-ops-kb\06_调研')

TEMPLATES = [
    WORKSPACE / '调研模板_01_上级单位_2026-08-01.md',
    WORKSPACE / '调研模板_02_集团_2026-08-01.md',
    WORKSPACE / '调研模板_03_旗下酒店_2026-08-01.md',
]

# 已知有问题的模式:
# 1. | 1.9 | 集团 SWOT 分析 | Gap Analysis | SWOT 表 | 必备 |
#    → 期望: | 1.9 | 集团 SWOT 分析 | Gap Analysis | ⚪ 待调研 | | SWOT 表 | 必备 |
#
# 2. | 2.1 | 集团 2023-2025 年总营收 / 净利润 | 集团 2023-2025 年总营收 / 净利润 | 集团财务部 | ? 待调研 | 三年数据 |
#    应该是: | 2.1 | 集团 2023-2025 年总营收 / 净利润 | 集团财务部 | ⚪ 待调研 | | 三年数据 |
# 注意"集团 2023-2025 年总营收 / 净利润" 重复了一次

# 解决思路:
# 1. 读全文
# 2. 找所有 5-6 列的数据行 (不重复列内容)
# 3. 重新规范化

for template_path in TEMPLATES:
    print(f"\n=== {template_path.name} ===")
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_size = len(content)

    # 步骤 1: 修复重复列内容 (例如 "| description | description |" 模式)
    # 这种模式: | 1.1 | 集团 X | 集团 X | 集团财务部 | ⚪ 待调研 |
    # 应该: | 1.1 | 集团 X | 集团财务部 | ⚪ 待调研 | |

    # 用正则找到重复模式
    # 模式: | 数字 | 文本 | 文本 | 文本 | 文本 | 文本 |
    # 其中第 2 个和第 3 个文本相同
    lines = content.split('\n')
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # 检查是否是 5-7 列的数据行
        # 模式: | 数字 | 文本1 | 文本2 | 文本3 | 文本4 | 文本5 | 文本6 | 文本7 |
        # 文本可能包含中文或英文
        match = re.match(r'^\| (\d+(?:\.\d+)?) \| ((?:[^|\n]|\|[^|\n][^|\n]*?)+?) \| ((?:[^|\n]|\|[^|\n][^|\n]*?)+?) \| ((?:[^|\n]|\|[^|\n][^|\n]*?)+?) \| ((?:[^|\n]|\|[^|\n][^|\n]*?)+?) \| ((?:[^|\n]|\|[^|\n][^|\n]*?)+?) \| ((?:[^|\n]|\|[^|\n][^|\n]*?)+?) \|$', line)
        if match and len(match.groups()) == 7:
            num = match.group(1)
            col1 = match.group(2).strip()
            col2 = match.group(3).strip()
            col3 = match.group(4).strip()
            col4 = match.group(5).strip()
            col5 = match.group(6).strip()
            col6 = match.group(7).strip()

            # 检查 col1 == col2 (重复)
            if col1 == col2:
                # 删除 col2, 同时也要看 col5 是否带 "⚪ 待调研"
                print(f"  修复行 {num}: 检测到 col1==col2 '{col1}', 应用修复")
                # 新的 7 列: | 数字 | 调研项 | 数据来源 | 输出形式 | 安逸集团有无 | 现有程度 | 备注 |
                new_line = f'| {num} | {col1} | {col3} | ⚪ 待调研 | | {col4} | {col5} | {col6} |'
                new_lines.append(new_line)
            else:
                new_lines.append(line)
        else:
            new_lines.append(line)
        i += 1

    content = '\n'.join(new_lines)

    with open(template_path, 'w', encoding='utf-8') as f:
        f.write(content)

    new_size = len(content)
    print(f"  大小: {original_size} → {new_size}")

print("\n=== 完成 ===")
