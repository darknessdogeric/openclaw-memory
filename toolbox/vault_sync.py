#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
vault_sync.py — Vault 统一操作门面 (R13 重 IO 隔离入口)

设计哲学:
  R13: 涉及 obsidian-vault/ 的重 IO 操作必须隔离到子会话.
  本门面把所有 vault 操作集中在一个入口, 让 B166ER / Eric 只需调用一个工具.

子命令:
  build        全量构建索引 (一次性, 建议走子会话)
  update       增量更新索引 (基于 mtime, 子会话)
  index-info   索引健康度
  search       关键词查询 (毫秒级, 主会话可直调)
  find-moc     按 MOC 主题查
  by-path      按文件名查
  push         调用 cron_to_obsidian.py 推送 (子会话执行)
  sync-workspace  workspace → vault 整体同步 (子会话执行)
  watch        监听 vault 变化, 自动增量更新 (后台)

典型调用:
  python vault_sync.py build                          # 子会话跑
  python vault_sync.py search "AHL 智能升级"            # 主会话毫秒级
  python vault_sync.py push "深度自检" "报告内容..."   # 子会话跑 (自动 enrich)
  python vault_sync.py sync-workspace                  # 子会话跑

R13 推荐调用模式:
  - 子会话: build / update / push / sync-workspace / watch
  - 主会话: search / find-moc / by-path / index-info
"""
import sys, io, json, argparse, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from datetime import datetime

VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")
INDEX_PATH = Path(r"D:\B166ER-OpenClaw\workspace\toolbox\.vault_index.json")
TOOLBOX = Path(r"D:\B166ER-OpenClaw\workspace\toolbox")


def run_subprocess(cmd: list, label: str = "") -> int:
    """在子进程跑命令 (模拟子会话执行, 适用于 CLI 工具)"""
    print(f"[{label or 'subprocess'}] {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode


def cmd_build(args):
    """全量构建索引"""
    return run_subprocess(
        [sys.executable, str(TOOLBOX / 'vault_index.py'), 'build', '--force'],
        'build-index'
    )


def cmd_update(args):
    """增量更新索引"""
    return run_subprocess(
        [sys.executable, str(TOOLBOX / 'vault_index.py'), 'update'],
        'update-index'
    )


def cmd_index_info(args):
    """索引健康度"""
    return run_subprocess(
        [sys.executable, str(TOOLBOX / 'vault_index.py'), 'stats'],
        'index-info'
    )


def cmd_search(args):
    """关键词查询 (毫秒级, 主会话安全)"""
    extra = []
    if args.top:
        extra += ['--top', str(args.top)]
    if args.type:
        extra += ['--type', args.type]
    if args.json:
        extra += ['--json']
    return run_subprocess(
        [sys.executable, str(TOOLBOX / 'vault_index.py'), 'query', args.query] + extra,
        'search'
    )


def cmd_find_moc(args):
    """按 MOC 查"""
    return run_subprocess(
        [sys.executable, str(TOOLBOX / 'vault_index.py'), 'find-moc', args.moc_name],
        'find-moc'
    )


def cmd_by_path(args):
    """按文件名查"""
    return run_subprocess(
        [sys.executable, str(TOOLBOX / 'vault_index.py'), 'path', args.stem],
        'by-path'
    )


def cmd_push(args):
    """推送 cron 输出到 vault (子会话执行, 自动 enrich)"""
    cmd = [sys.executable, str(TOOLBOX / 'cron_to_obsidian.py'),
           '--task', args.task,
           '--content', args.content,
           '--importance', args.importance]
    if args.summary:
        cmd += ['--summary', args.summary]
    if args.append_daily:
        cmd += ['--append-daily']
    return run_subprocess(cmd, 'push-cron')


def cmd_sync_workspace(args):
    """workspace → vault 整体同步 (子会话执行)"""
    return run_subprocess(
        [sys.executable, str(TOOLBOX / 'sync_all_to_vault.py')],
        'sync-workspace'
    )


def cmd_health(args):
    """vault 整体健康度 (文件数 / 索引状态 / MOC 覆盖)"""
    print("=" * 60)
    print("Vault 整体健康度")
    print("=" * 60)

    # 1. 文件统计
    md_files = list(VAULT.rglob('*.md'))
    md_count = len(md_files)
    total_size = sum(f.stat().st_size for f in md_files)
    print(f"  .md 文件: {md_count}")
    print(f"  总文本: {total_size / 1024 / 1024:.2f} MB")

    # 2. 索引状态
    if INDEX_PATH.exists():
        idx_mtime = datetime.fromtimestamp(INDEX_PATH.stat().st_mtime)
        idx_age = (datetime.now() - idx_mtime).total_seconds() / 60
        idx_size = INDEX_PATH.stat().st_size / 1024 / 1024
        print(f"  索引状态: ✅ 已构建 ({idx_age:.1f} 分钟前, {idx_size:.2f} MB)")
        try:
            idx = json.loads(INDEX_PATH.read_text(encoding='utf-8'))
            print(f"  索引覆盖: {idx.get('total_files')}/{md_count} 文件")
            if idx.get('total_files') < md_count:
                print(f"  ⚠️  索引滞后 {md_count - idx.get('total_files')} 个文件, 建议 update")
        except Exception:
            print(f"  ⚠️  索引文件损坏, 建议 build --force")
    else:
        print(f"  索引状态: ❌ 未构建, 请运行 `vault_sync.py build`")

    # 3. 子目录分布
    print()
    print("  子目录 .md 分布:")
    sub_counts = {}
    for f in md_files:
        try:
            rel = f.relative_to(VAULT)
            top_dir = rel.parts[0] if len(rel.parts) > 1 else 'root'
            sub_counts[top_dir] = sub_counts.get(top_dir, 0) + 1
        except Exception:
            pass
    for d, n in sorted(sub_counts.items(), key=lambda x: -x[1])[:10]:
        print(f"    {d}: {n}")

    return 0


def main():
    parser = argparse.ArgumentParser(description='vault_sync — Vault 统一操作门面 (R13)')
    sub = parser.add_subparsers(dest='cmd', required=True)

    # build / update / index-info
    sub.add_parser('build', help='全量构建索引')
    sub.add_parser('update', help='增量更新索引')
    sub.add_parser('index-info', help='索引健康度')

    # search
    p_search = sub.add_parser('search', help='关键词查询 (毫秒级)')
    p_search.add_argument('query', help='查询关键词')
    p_search.add_argument('--top', type=int, default=15, help='返回 top N')
    p_search.add_argument('--type', help='按 type 过滤')
    p_search.add_argument('--json', action='store_true', help='JSON 输出')

    # find-moc
    p_moc = sub.add_parser('find-moc', help='按 MOC 主题查')
    p_moc.add_argument('moc_name', help='MOC 名称')

    # by-path
    p_path = sub.add_parser('by-path', help='按文件名查')
    p_path.add_argument('stem', help='文件名或部分名')

    # push
    p_push = sub.add_parser('push', help='推送 cron 输出 (子会话执行)')
    p_push.add_argument('--task', required=True, help='任务名')
    p_push.add_argument('--content', required=True, help='内容')
    p_push.add_argument('--importance', default='normal', choices=['urgent','high','normal','low'])
    p_push.add_argument('--summary', help='一句话摘要')
    p_push.add_argument('--append-daily', action='store_true', help='追加到日记')

    # sync-workspace
    sub.add_parser('sync-workspace', help='workspace → vault 整体同步')

    # health
    sub.add_parser('health', help='vault 整体健康度')

    args = parser.parse_args()

    handlers = {
        'build': cmd_build,
        'update': cmd_update,
        'index-info': cmd_index_info,
        'search': cmd_search,
        'find-moc': cmd_find_moc,
        'by-path': cmd_by_path,
        'push': cmd_push,
        'sync-workspace': cmd_sync_workspace,
        'health': cmd_health,
    }

    return handlers[args.cmd](args)


if __name__ == '__main__':
    sys.exit(main())