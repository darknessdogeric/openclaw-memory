# -*- coding: utf-8 -*-
"""
tool3: KB Maintenance — 基于 Scanner 输出执行维护
功能:
  1. 删除 0 字节 / 空文件
  2. 检测并报告多版本冲突(自动跳过已有 _归档_ 标记的)
  3. 关键词冲突清理建议
  4. 生成 KB 总览索引(MOC)
"""
import os, re, json, sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from collections import defaultdict
import datetime

WORKSPACE = Path(r'D:\B166ER-OpenClaw\workspace')
SCAN_REPORT = WORKSPACE / 'toolbox' / 'kb_tools' / 'scan_report.json'

def load_scan_report():
    if not SCAN_REPORT.exists():
        print(f'❌ 扫描报告不存在: {SCAN_REPORT}')
        print('   请先运行 kb_scanner.py')
        return None
    return json.loads(SCAN_REPORT.read_text(encoding='utf-8'))


def fix_empty_files(issues):
    """删除 0 字节文件"""
    print('\n=== 修复: 0 字节文件 ===')
    for path in issues.get('empty_files', []):
        full = WORKSPACE / path
        if full.exists():
            size = full.stat().st_size
            print(f'   删除: {path} ({size} bytes)')
            full.unlink()
        else:
            print(f'   已不存在: {path}')


def analyze_multi_versions(issues):
    """分析多版本冲突,生成合并建议"""
    print('\n=== 多版本冲突分析 ===')
    merge_plan = []
    for m in issues.get('multi_versions', []):
        base = m['base']
        versions = m['versions']
        # 找出最新版本(根据 vX.Y 数字)
        def v_key(item):
            v = item[0]
            if v == '无版本':
                return (0, 0)
            try:
                parts = v.split('.')
                return tuple(int(p) for p in parts)
            except Exception:
                return (0, 0)
        versions.sort(key=v_key, reverse=True)
        newest = versions[0]
        olders = versions[1:]
        print(f'\n   主题: {base}')
        print(f'   最新: v{newest[0]} → {newest[1]}')
        for v, p in olders:
            if '_归档_' in p:
                print(f'   归档: v{v} → {p} (OK,保留)')
            else:
                print(f'   ⚠️ 未归档: v{v} → {p} (建议移到 _归档_/)')
                merge_plan.append({
                    'theme': base,
                    'newest': newest[1],
                    'old_to_archive': p,
                })
    return merge_plan


def analyze_keyword_conflicts(issues):
    """分析关键词冲突,标记需要 R66 修订的文件"""
    print('\n=== 关键词冲突(R66 修订遗留)===')
    r66_needed = defaultdict(list)
    for c in issues.get('conflict_keywords', []):
        file_path = c['file']
        conflict_type = c['type']
        r66_needed[conflict_type].append(file_path)

    for ctype, files in r66_needed.items():
        print(f'\n   类型: {ctype} ({len(files)} 个文件)')
        for f in files[:5]:
            print(f'      - {f}')
        if len(files) > 5:
            print(f'      ... +{len(files) - 5} 个')


def generate_kb_moc():
    """生成 KB 总览索引(MOC)"""
    print('\n=== 生成 KB 总览索引(MOC)===')
    moc = []
    moc.append('# KB 总览索引(MOC)')
    moc.append('')
    moc.append(f'> 自动生成于 {datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}')
    moc.append('> 工具: kb_maintenance.py')
    moc.append('')

    # 按顶级目录分组
    kb_dirs = {
        'universal-kb': WORKSPACE / 'universal-kb',
        'anyi-ops-kb': WORKSPACE / 'anyi-ops-kb',
    }
    for kb_name, kb_path in kb_dirs.items():
        if not kb_path.exists():
            continue
        moc.append(f'## {kb_name}')
        moc.append('')
        # 顶级目录
        for sub in sorted(kb_path.iterdir()):
            if not sub.is_dir():
                continue
            md_files = list(sub.rglob('*.md'))
            current = [f for f in md_files if '_归档_' not in f.name]
            archived = [f for f in md_files if '_归档_' in f.name]
            moc.append(f'### {sub.name} ({len(current)} 当前 + {len(archived)} 归档)')
            moc.append('')
            # 当前权威版(取每个基础名的最新版本)
            by_base = defaultdict(list)
            for f in current:
                base = re.sub(r'_v\d+\.\d+_\d{4}-\d{2}-\d{2}', '', f.name)
                base = re.sub(r'_\d{4}-\d{2}-\d{2}', '', base)
                by_base[base].append(f)
            for base, group in sorted(by_base.items()):
                # 最新版
                def v_key(p):
                    m = re.search(r'_v(\d+\.\d+)_', p.name)
                    if m:
                        try:
                            return tuple(int(x) for x in m.group(1).split('.'))
                        except Exception:
                            return (0, 0)
                    return (0, 0)
                group.sort(key=v_key, reverse=True)
                latest = group[0]
                rel = latest.relative_to(WORKSPACE)
                moc.append(f'- **{base.replace(".md", "")}** ({len(group)} 个版本) → `{rel}`')
            if not current:
                moc.append('  *(无当前文件)*')
            moc.append('')

    # memory
    moc.append('## memory/')
    moc.append('')
    memory_dir = WORKSPACE / 'memory'
    if memory_dir.exists():
        md_files = sorted(memory_dir.glob('*.md'), key=lambda p: p.name, reverse=True)
        moc.append(f'- 总文件数: {len(md_files)}')
        moc.append(f'- 最近: {md_files[0].name if md_files else "无"}')
    moc.append('')

    # 保存
    moc_path = WORKSPACE / 'toolbox' / 'kb_tools' / 'KB_MOC.md'
    moc_path.write_text('\n'.join(moc), encoding='utf-8')
    print(f'   ✓ MOC 已生成: {moc_path}')


def main():
    data = load_scan_report()
    if not data:
        return
    issues = data['issues']
    files = data['files']

    print('=' * 60)
    print(f'KB 维护报告 - 总文件数: {len(files)}')
    print('=' * 60)

    # 1. 修复 0 字节
    fix_empty_files(issues)

    # 2. 分析多版本
    merge_plan = analyze_multi_versions(issues)

    # 3. 关键词冲突分析
    analyze_keyword_conflicts(issues)

    # 4. 生成 MOC
    generate_kb_moc()

    print('\n' + '=' * 60)
    print('✅ 维护完成')
    print('=' * 60)


if __name__ == '__main__':
    main()