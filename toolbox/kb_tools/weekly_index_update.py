# -*- coding: utf-8 -*-
"""
weekly_index_update.py — 每周知识库索引更新主程序 (2026-10-26)

严格按 cron 任务定义执行:
  1. 扫描 memory/*.md、skills/*/SKILL.md、data-acquisition/**/*.md (过去 7 天)
  2. 对新文件调用 kb.index_file(filepath, tags=['auto-updated'])
  3. 核验索引结果 + 写日志

用法: python weekly_index_update.py
"""
import os
import sys
import json
import time
import pickle
import datetime
import argparse
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from weekly_index_candidates import collect, indexed_paths, WORKSPACE, INDEX_FILE

LOG_PATH = WORKSPACE / 'toolbox' / 'kb_tools' / 'weekly_index_last.json'


def kb_api():
    """按任务指定方式导入:from knowledge_base import B166ERKnowledgeBase"""
    from knowledge_base import B166ERKnowledgeBase
    return B166ERKnowledgeBase()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    t0 = time.time()
    cands = collect()
    kb_scope = [c for c in cands if c['in_kb_scope']]
    out_scope = [c for c in cands if not c['in_kb_scope']]
    print('[1/4] 候选扫描: {} 个(索引范围内 {} / 范围外 {})'.format(
        len(cands), len(kb_scope), len(out_scope)), flush=True)

    results = []
    if not args.dry_run:
        kb = kb_api()
        # 逐个调用任务指定的 API;首次调用触发全局增量索引,后续为幂等空跑
        for i, c in enumerate(kb_scope, 1):
            r = kb.index_file(c['path'], tags=['auto-updated'])
            results.append({'path': c['path'], **r})
            if i == 1:
                print('   首次 index_file → 增量索引完成: {}'.format(r), flush=True)
            elif not r.get('ok'):
                print('   [warn] {} → {}'.format(c['path'], r.get('error')), flush=True)
    print('[2/4] index_file 调用完成 ({} 个文件, {:.1f}s)'.format(
        len(results), time.time() - t0), flush=True)

    # 核验
    idx = indexed_paths()
    in_idx = [c for c in cands if c['path'] in idx]
    missing = [c for c in cands if c['path'] not in idx]
    print('[3/4] 核验: 已索引 {}/{} | 未索引 {} (KB 范围外: {})'.format(
        len(in_idx), len(cands), len(missing), len(out_scope)), flush=True)

    meta = {}
    try:
        meta = json.loads((WORKSPACE / 'toolbox' / 'kb_tools' / 'index' /
                           'index_meta.json').read_text(encoding='utf-8'))
    except Exception:
        pass

    payload = {
        'ts': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'candidates_total': len(cands),
        'candidates_in_scope': len(kb_scope),
        'candidates_out_scope': len(out_scope),
        'indexed_ok': len(in_idx),
        'missing': [c['path'] for c in missing],
        'out_of_scope': [c['path'] for c in out_scope],
        'index_meta': meta,
        'elapsed_sec': round(time.time() - t0, 1),
    }
    LOG_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    print('[4/4] 日志写入 {}'.format(LOG_PATH), flush=True)
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
