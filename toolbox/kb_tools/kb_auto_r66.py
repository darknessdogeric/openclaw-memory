# -*- coding: utf-8 -*-
"""
tool4: KB Auto R66 Revision — 自动批量修订 R66 遗留
检测虚构内容(阿联酋/UAE/本奥米尔/Benoemir/350亿/中国银行四川省分行)
不在 R66 修订日志中的 → 替换为 [R66已清理]
"""
import os, sys, json, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from collections import defaultdict

WORKSPACE = Path(r'D:\B166ER-OpenClaw\workspace')
SCAN_REPORT = WORKSPACE / 'toolbox' / 'kb_tools' / 'scan_report.json'

# 关键词:R66 已清理的虚构内容(部分列表)
FICTIONAL_KEYWORDS = [
    '阿联酋', 'UAE', '本奥米尔', 'Benoemir',
    '350 亿授信', '350亿授信', '350 亿',
    '中国银行四川省分行',
    # Eric 之前提及的
]

# 修订标记:这一行/段如果包含 R66 修订相关词汇,说明是历史日志,保留
REVISION_NOTE_PATTERNS = [
    r'R66修订',
    r'已清理',
    r'作废',
    r'虚构',
    r'修订原则',
]


def is_revision_note(line_or_context):
    """判断这一行是否是 R66 修订日志(应该保留)"""
    return any(re.search(p, line_or_context) for p in REVISION_NOTE_PATTERNS)


def check_file(filepath):
    """检查单个文件的虚构残留"""
    if not filepath.exists():
        return None
    try:
        content = filepath.read_text(encoding='utf-8', errors='replace')
    except Exception:
        return None

    lines = content.split('\n')
    issues = []

    for i, line in enumerate(lines):
        if not any(kw in line for kw in FICTIONAL_KEYWORDS):
            continue

        # 检查是否是 R66 修订日志(保留)
        # 取上下文:本行 + 前后 1 行
        prev_line = lines[i-1] if i > 0 else ''
        next_line = lines[i+1] if i < len(lines) - 1 else ''
        context = f'{prev_line} {line} {next_line}'
        if is_revision_note(context):
            continue

        issues.append({
            'line_num': i + 1,
            'line': line.rstrip(),
            'context_before': prev_line.rstrip()[:80],
            'context_after': next_line.rstrip()[:80],
        })

    return issues


def scan_all(apply=False):
    """扫描所有 KB 文件(从 scan_report 中读取冲突列表)"""
    if not SCAN_REPORT.exists():
        print(f'❌ 扫描报告不存在: {SCAN_REPORT}')
        print('   请先运行 kb_scanner.py')
        return None

    report = json.loads(SCAN_REPORT.read_text(encoding='utf-8'))
    conflicts = report['issues'].get('conflict_keywords', [])

    # 去重(同一文件可能多个关键词冲突)
    file_set = set()
    for c in conflicts:
        file_set.add(c['file'])

    print(f'扫描 {len(file_set)} 个文件(含虚构关键词冲突)...')
    print(f'  模式: {"APPLY" if apply else "DRY-RUN"}')
    print()

    stats = defaultdict(int)
    all_results = []

    for rel_path in sorted(file_set):
        full = WORKSPACE / rel_path
        issues = check_file(full)
        if not issues:
            continue

        stats[rel_path] = len(issues)
        all_results.append({
            'file': rel_path,
            'issues': issues,
        })

    # 输出
    total = sum(stats.values())
    print(f'找到 {len(all_results)} 个文件含虚构残留,共 {total} 处')
    print()

    if not apply:
        # DRY-RUN:只报告
        print('=' * 60)
        print('DRY-RUN 报告(未修改任何文件)')
        print('=' * 60)
        for r in all_results[:30]:
            print(f"\n[{r['file']}] ({len(r['issues'])} 处)")
            for issue in r['issues'][:3]:
                print(f"  L{issue['line_num']}: {issue['line'][:120]}")
        if len(all_results) > 30:
            print(f'\n... 还有 {len(all_results) - 30} 个文件')
        print(f'\n合计: {total} 处需要修订')
        print('运行 `python kb_auto_r66.py apply` 实际修订')

    else:
        # APPLY:实际修改
        print('=' * 60)
        print('APPLY 修订中...')
        print('=' * 60)
        modified_count = 0
        for r in all_results:
            full = WORKSPACE / r['file']
            content = full.read_text(encoding='utf-8', errors='replace')
            lines = content.split('\n')
            changes = 0
            # 从后向前处理,避免行号偏移
            for issue in reversed(r['issues']):
                line_num = issue['line_num']
                if line_num > 0 and line_num <= len(lines):
                    old = lines[line_num - 1]
                    # 替换策略:
                    # 1. 整行删除(如果是表格行)
                    # 2. 整行替换为 [R66已清理]
                    if old.strip().startswith('|') and old.strip().endswith('|'):
                        # 表格行:替换关键词为 [R66已清理]
                        new = old
                        for kw in FICTIONAL_KEYWORDS:
                            if kw in new:
                                # 保留表格结构
                                new = re.sub(re.escape(kw), '[R66已清理]', new)
                        lines[line_num - 1] = new
                    else:
                        # 段落行:整行替换为 [R66已清理]
                        # 但保留行首的格式符(如 > 或 # 或 -)
                        prefix = re.match(r'^([\s>\-\*#]*)', old).group(1)
                        lines[line_num - 1] = f'{prefix}[R66已清理]'
                    changes += 1

            new_content = '\n'.join(lines)
            full.write_text(new_content, encoding='utf-8')
            modified_count += 1
            print(f'  ✓ {r["file"]} ({changes} 处)')

        print(f'\n✅ 已修订 {modified_count} 个文件')

    return all_results, stats


if __name__ == '__main__':
    apply = len(sys.argv) > 1 and sys.argv[1] == 'apply'
    result = scan_all(apply=apply)
    if result:
        # 保存修订报告
        out = WORKSPACE / 'toolbox' / 'kb_tools' / 'r66_revision_report.json'
        out.write_text(json.dumps(result[1], ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'\n报告: {out}')