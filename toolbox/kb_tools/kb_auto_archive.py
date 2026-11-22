# -*- coding: utf-8 -*-
"""
tool5: KB Auto Archive — 自动归档旧版本
按主题保留最新版本, 其余移到 _归档_/ 子目录
"""
import os, sys, json, shutil, re
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
from collections import defaultdict

WORKSPACE = Path(r'D:\B166ER-OpenClaw\workspace')
SCAN_REPORT = WORKSPACE / 'toolbox' / 'kb_tools' / 'scan_report.json'


def version_key(p):
    """提取版本号作为排序键"""
    m = re.search(r'_v(\d+\.\d+)_', p.name)
    if m:
        try:
            return tuple(int(x) for x in m.group(1).split('.'))
        except Exception:
            return (0, 0)
    return (0, 0)


def archive_old_versions(apply=False):
    if not SCAN_REPORT.exists():
        print('❌ 扫描报告不存在')
        return None

    report = json.loads(SCAN_REPORT.read_text(encoding='utf-8'))
    mv_list = report['issues'].get('multi_versions', [])

    print(f'扫描到 {len(mv_list)} 个多版本主题')
    print(f'  模式: {"APPLY" if apply else "DRY-RUN"}')
    print()

    actions = []

    for m in mv_list:
        versions = m['versions']
        # 按版本号排序(新 → 旧)
        versions.sort(key=lambda x: version_key(Path(x[1])), reverse=True)
        newest = versions[0]
        olders = versions[1:]

        for v, p in olders:
            if '_归档_' in p:
                continue  # 已归档,跳过
            full_path = WORKSPACE / p
            # 在同一目录下创建 _归档_/ 子目录
            archive_dir = full_path.parent / '_归档_'
            new_path = archive_dir / full_path.name
            actions.append({
                'from': p,
                'to': str(new_path.relative_to(WORKSPACE)),
            })

    print('=' * 60)
    print(f'计划归档: {len(actions)} 个文件')
    print('=' * 60)

    if not apply:
        for a in actions:
            print(f"  {a['from']}")
            print(f"    → {a['to']}")
        print()
        print('运行 `python kb_auto_archive.py apply` 实际归档')
    else:
        moved = 0
        for a in actions:
            src = WORKSPACE / a['from']
            dst = WORKSPACE / a['to']
            if not src.exists():
                continue
            dst.parent.mkdir(parents=True, exist_ok=True)
            # 如果目标已存在,加时间戳后缀
            if dst.exists():
                ts = datetime.datetime.now().strftime('%H%M%S')
                dst = dst.parent / f'{dst.stem}_{ts}{dst.suffix}'
            shutil.move(str(src), str(dst))
            moved += 1
            print(f'  ✓ {a["from"]}')
            print(f'    → {dst.relative_to(WORKSPACE)}')
        print(f'\n✅ 已归档 {moved} 个文件')

    return actions


if __name__ == '__main__':
    import datetime
    apply = len(sys.argv) > 1 and sys.argv[1] == 'apply'
    archive_old_versions(apply=apply)