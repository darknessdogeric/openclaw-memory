# -*- coding: utf-8 -*-
"""
fill_schema.py - 按 schema 模板填充报告（骨架）
历史：methodology/sop-region-analysis.md 引用。v1.0 骨架。
"""
import sys
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parent.parent / 'schema.md'

def fill(raw_data: dict, output_path: str = None) -> str:
    """把 raw_data 填进 10+5 章节框架，输出 markdown。"""
    if not SCHEMA_PATH.exists():
        return '# Error: schema.md not found'

    template = SCHEMA_PATH.read_text(encoding='utf-8')

    # 简单替换占位符
    out = template
    for key, val in raw_data.items():
        placeholder = f'{{{{{key}}}}}'
        if placeholder in out:
            out = out.replace(placeholder, str(val))

    if output_path:
        Path(output_path).write_text(out, encoding='utf-8')

    return out

if __name__ == '__main__':
    print('用法: from fill_schema import fill; fill(raw_data, "out.md")')