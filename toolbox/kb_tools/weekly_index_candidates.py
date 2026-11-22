# -*- coding: utf-8 -*-
"""
weekly_index_candidates.py — 每周知识库索引更新:候选文件扫描 + 索引核验

用法:
  python weekly_index_candidates.py --scan          # 只列候选(不索引)
  python weekly_index_candidates.py --scan --json    # JSON 输出
  python weekly_index_candidates.py --verify         # 候选文件是否已在索引中
"""
import os
import sys
import json
import time
import pickle
import argparse
import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

WORKSPACE = Path(r'D:\B166ER-OpenClaw\workspace')
INDEX_FILE = WORKSPACE / 'toolbox' / 'kb_tools' / 'index' / 'documents.pkl'

# 扫描根:1) memory/*.md  2) skills/*/SKILL.md  3) data-acquisition/**/*.md
SCAN_ROOTS = [
    WORKSPACE / 'memory',
    WORKSPACE / 'skills' / 'data-acquisition',
]
SKILL_GLOB = WORKSPACE / 'skills' / '*' / 'SKILL.md'
DAYS = 7

# 临时文件 / 日志 / 归档 / 备份 —— 不索引
SKIP_PATTERNS = (
    '.tmp', '.bak', '.pre-c-backup', '_archive_', '归档_',
    'backup', 'backups', '.log', 'debug_', 'test_',
    'round9-append', 'scratch', 'node_modules', '__pycache__',
)
SKIP_PREFIX = ('_', '~$')


def is_skippable(name: str) -> bool:
    low = name.lower()
    if any(p in low for p in SKIP_PATTERNS):
        return True
    if any(name.startswith(p) for p in SKIP_PREFIX):
        return True
    return False


def collect():
    cutoff = time.time() - DAYS * 86400
    out = []
    seen = set()

    def add(fp: Path, kind: str):
        if not fp.is_file():
            return
        if str(fp) in seen:
            return
        seen.add(str(fp))
        st = fp.stat()
        if st.st_mtime < cutoff:
            return
        if is_skippable(fp.name):
            return
        out.append({
            'path': str(fp.relative_to(WORKSPACE)),
            'kind': kind,
            'size': st.st_size,
            'mtime': datetime.datetime.fromtimestamp(st.st_mtime).strftime('%Y-%m-%d %H:%M'),
            # 是否落在 KB 索引范围内(universal-kb / anyi-ops-kb / memory)
            'in_kb_scope': str(fp.relative_to(WORKSPACE)).startswith(
                ('memory\\', 'anyi-ops-kb\\', 'universal-kb\\')),
        })

    for md in sorted((WORKSPACE / 'memory').glob('*.md')):
        add(md, 'memory')
    for md in sorted(WORKSPACE.glob('skills/*/SKILL.md')):
        add(md, 'skill')
    for md in sorted((WORKSPACE / 'skills' / 'data-acquisition').rglob('*.md')):
        add(md, 'data-acquisition')
    return out


def indexed_paths():
    if not INDEX_FILE.exists():
        return set()
    try:
        with open(INDEX_FILE, 'rb') as f:
            docs = pickle.load(f)
        return set(d['path'] for d in docs)
    except Exception:
        return set()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scan', action='store_true')
    ap.add_argument('--verify', action='store_true')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()

    cands = collect()
    idx = indexed_paths() if args.verify else set()
    for c in cands:
        c['indexed'] = (c['path'] in idx) if args.verify else None

    if args.json:
        print(json.dumps(cands, ensure_ascii=False, indent=2))
        return

    print('=== 过去 {} 天新增/修改的候选文件 ({}) ==='.format(DAYS, len(cands)))
    for c in cands:
        flag = 'KB范围内' if c['in_kb_scope'] else 'KB范围外'
        mark = ''
        if args.verify:
            mark = ' [已索引]' if c['indexed'] else ' [未索引]'
        print('  {:<12} {:<16} {:>8}B  {}{}'.format(
            c['kind'], c['mtime'], c['size'], flag, mark))
    if args.verify:
        miss = [c for c in cands if not c['indexed']]
        print('\n未索引: {} / {}'.format(len(miss), len(cands)))


if __name__ == '__main__':
    main()
