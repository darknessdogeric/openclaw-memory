# -*- coding: utf-8 -*-
"""
tool1: KB Scanner — 扫描所有 .md,提取元数据,发现问题
"""
import os, re, json, sys
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from collections import defaultdict

WORKSPACE = Path(r'D:\B166ER-OpenClaw\workspace')
KB_DIRS = [
    WORKSPACE / 'universal-kb',
    WORKSPACE / 'anyi-ops-kb',
]
# 只扫描最近 N 天的 memory(避免太久)
MEMORY_DIR = WORKSPACE / 'memory'
MEMORY_DAYS = 30  # 最近 30 天的 memory

def extract_metadata(filepath):
    """提取单个 .md 文件的元数据"""
    try:
        size = filepath.stat().st_size
        content = filepath.read_text(encoding='utf-8', errors='replace')
    except Exception as e:
        return None

    md = {
        'path': str(filepath.relative_to(WORKSPACE)),
        'size': size,
        'title': '',
        'h1_count': 0,
        'word_count': len(content),
        'r66_marks': [],
        'version_in_name': '',
        'has_todo': False,
        'has_archived': False,
        'is_empty': size < 100,
        'links_to_other_kb': [],
    }

    # 提取 H1 (取第一个)
    h1_match = re.search(r'^# (.+?)$', content, re.MULTILINE)
    if h1_match:
        md['title'] = h1_match.group(1).strip()

    # 提取 H1 数量
    md['h1_count'] = len(re.findall(r'^# ', content, re.MULTILINE))

    # 提取 R66 标记
    md['r66_marks'] = re.findall(r'\[R66[^\]]+\]', content)

    # 提取版本号
    version_match = re.search(r'_v(\d+\.\d+)[_\s]', filepath.name)
    if version_match:
        md['version_in_name'] = version_match.group(1)

    # 检测 TODO
    md['has_todo'] = bool(re.search(r'\bTODO\b|\bFIXME\b|\bXXX\b', content))

    # 检测归档标记
    md['has_archived'] = '_归档_' in filepath.name or '_archive_' in filepath.name

    # 跨 KB 引用
    if 'anyi-ops-kb' in content:
        md['links_to_other_kb'].append('anyi-ops-kb')
    if 'universal-kb' in content:
        md['links_to_other_kb'].append('universal-kb')

    return md


def scan_kbs():
    """扫描所有 KB,生成报告"""
    all_files = []
    for kb_dir in KB_DIRS:
        if not kb_dir.exists():
            continue
        for md_file in kb_dir.rglob('*.md'):
            meta = extract_metadata(md_file)
            if meta:
                all_files.append(meta)

    # Memory 单独扫描(最近 30 天)
    if MEMORY_DIR.exists():
        import datetime
        cutoff = datetime.datetime.now() - datetime.timedelta(days=MEMORY_DAYS)
        for md_file in MEMORY_DIR.glob('*.md'):
            try:
                mtime = datetime.datetime.fromtimestamp(md_file.stat().st_mtime)
                if mtime < cutoff:
                    continue
            except Exception:
                pass
            meta = extract_metadata(md_file)
            if meta:
                meta['is_memory'] = True
                all_files.append(meta)

    return all_files


def analyze(files):
    """分析问题"""
    issues = defaultdict(list)

    # 1. 0 字节 / 空文件
    for f in files:
        if f['is_empty']:
            issues['empty_files'].append(f['path'])

    # 2. 版本号冲突(同主题多版本)
    # 用文件名前缀(去版本和日期)
    base_names = defaultdict(list)
    for f in files:
        # 提取基础名(去 _vX.Y_YYYY-MM-DD)
        base = re.sub(r'_v\d+\.\d+_\d{4}-\d{2}-\d{2}', '', f['path'])
        base = re.sub(r'_\d{4}-\d{2}-\d{2}', '', base)
        base_names[base].append(f)

    for base, group in base_names.items():
        if len(group) > 1:
            # 检查是不是同一主题多版本
            if any('_归档_' not in g['path'] for g in group):
                # 至少有一个非归档版本 + 多个版本
                versions = [(g['version_in_name'] or '无版本', g['path']) for g in group]
                versions.sort()
                issues['multi_versions'].append({
                    'base': base,
                    'count': len(group),
                    'versions': versions,
                })

    # 3. 数据冲突关键词检测
    CONFLICTS = {
        '1234 vs 1244': {
            'old': '1234',
            'new': '1244',
            'note': '战略编号修正',
        },
        # 2026-10-26 分级修正：原规则把「本奥米尔」（R66 虚构地名）与「UAE/阿联酋」
        #   （**真实地名**，如迪拜棕榈岛项目本就该提）混为一谈 → 实测 38 处「冲突」里
        #   36 处是误报，噪音淹没真问题（真含虚构残留的只有 2 个文件）。
        #   拆分：虚构残留 = error 级（conflict_keywords）；真实地名提及 = info 级（advisory_terms）
        'R66虚构地名残留': {
            'old': ['本奥米尔'],
            'note': 'R66 已清理的虚构地名，应保持不出现',
        },
        '真实地名提及(非冲突)': {
            'old': ['UAE', '阿联酋'],
            'note': '真实地名，属正常表述，非 R66 虚构残留',
            'advisory': True,
        },
    }

    for f in files:
        try:
            content = (WORKSPACE / f['path']).read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        # 检查 1234 在标题但 1244 在文末(矛盾)
        for conflict_name, info in CONFLICTS.items():
            if isinstance(info['old'], list):
                # 多关键词:分级收集（advisory → advisory_terms，只提示不判冲突）
                bucket = 'advisory_terms' if info.get('advisory') else 'conflict_keywords'
                for kw in info['old']:
                    if kw in content:
                        issues[bucket].append({
                            'file': f['path'],
                            'type': conflict_name,
                            'term': kw,
                            'note': info.get('note', ''),
                        })
                        break
            else:
                # 单一关键词(只在标题层)
                if info['old'] in f['title'] and info['new'] in content:
                    issues['conflict_keywords'].append({
                        'file': f['path'],
                        'type': conflict_name,
                        'note': info.get('note', ''),
                    })

    # 4. TODO/FIXME
    for f in files:
        if f['has_todo']:
            issues['todos'].append(f['path'])

    # 5. 无 R66 校准标记但应该有
    for f in files:
        if not f['has_archived'] and not f['r66_marks'] and f['size'] > 2048:
            # 大文件但无 R66 标记(可能漏)
            pass  # 太多 false positive,先不报告

    return dict(issues)


def main():
    print('🔍 扫描 KB...')
    files = scan_kbs()
    print(f'   总文件数: {len(files)}')

    print('\n🔎 分析问题...')
    issues = analyze(files)

    # 输出报告
    print('\n' + '=' * 60)
    print('📊 扫描结果')
    print('=' * 60)

    print(f"\n📁 0 字节/空文件: {len(issues.get('empty_files', []))}")
    for f in issues.get('empty_files', [])[:10]:
        print(f"   - {f}")

    print(f"\n🔀 多版本冲突: {len(issues.get('multi_versions', []))}")
    for m in issues.get('multi_versions', [])[:10]:
        print(f"   - {m['base']} ({m['count']} 个版本)")
        for v, p in m['versions']:
            print(f"      v{v}: {p}")

    print(f"\n⚠️ 关键词冲突(R66虚构残留): {len(issues.get('conflict_keywords', []))}")
    print(f"ℹ️ 真实地名提及(非冲突): {len(issues.get('advisory_terms', []))}")
    for c in issues.get('conflict_keywords', [])[:10]:
        print(f"   - {c['file']}: {c['type']} ({c['note']})")

    print(f"\n📝 TODO/FIXME: {len(issues.get('todos', []))}")
    for f in issues.get('todos', [])[:5]:
        print(f"   - {f}")

    # 保存 JSON 报告
    report_path = WORKSPACE / 'toolbox' / 'kb_tools' / 'scan_report.json'
    report_path.write_text(
        json.dumps({
            'files': files,
            'issues': issues,
        }, ensure_ascii=False, indent=2),
        encoding='utf-8'
    )
    print(f"\n✅ 详细报告已保存: {report_path}")

    return issues, files


if __name__ == '__main__':
    main()