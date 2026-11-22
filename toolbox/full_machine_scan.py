#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""全盘扫描: 找出所有可纳入 vault 的内容"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from collections import defaultdict

# 扫描范围
SCAN_ROOTS = [
    Path(r"D:\B166ER-OpenClaw"),  # 整个 B166ER 根
    Path(r"C:\Users\ericz"),         # 用户目录
]

# 排除（系统/虚拟/隐藏）
EXCLUDE = [
    'node_modules', '.git', '.backups', '.openclaw',
    'obsidian-vault',  # 已经是 vault 了
    '.agents', '.clawhub', '.iflow', '.last30days-skill',
    '.playwright-cli', '.self-improving', '.tmp', '.next', '.venv',
    'cache', '__pycache__', '.pytest_cache',
    'Windows', 'Program Files', 'ProgramData', 'Users/Default', '$Recycle.Bin',
    'AppData',  # 用户 AppData 太多噪音
]

# 重点关注目录（这些已知有内容）
PRIORITY_DIRS = [
    'AHL-AGENT-SKILL架构体系', 'AHL项目', 'knowledge', 'MemOS',
    'mempalace-test', 'tencentDB-Agent-Memory', 'career-ops',
    'poster_templates', 'ppt_output', 'redfox-community',
    'Horizon-eric', 'open-design-repo', 'evolver',
    'research', 'output', 'outputs', 'media', 'temp',
    'skills', 'toolbox', 'scripts', 'docs', 'reports', 'memory',
    'my-project', 'CLI-Anything-Project', 'coder', 'design-studio',
    'eval', 'mempalace-test', 'log', 'lottery_history',
    'mempalace-test', 'openhuman-eval', 'ota-scraper', 'ota_scraper',
    'ota-scan', 'ponytail', 'refly-eval', 'search_cache',
    'self_evolution', 'TencentDB-Agent-Memory', 'toolbox',
    'trendradar', 'yunding_remotion', 'ZeusHammer',
]


def should_skip(path: Path) -> bool:
    s = str(path).lower()
    for ex in EXCLUDE:
        if ex.lower() in s:
            return True
    return False


def count_files(root: Path, ext=None) -> dict:
    """统计 root 下文件数 + 总大小"""
    stats = {'files': 0, 'md': 0, 'pdf': 0, 'docx': 0, 'txt': 0,
             'json': 0, 'images': 0, 'other': 0, 'total_size': 0}
    if not root.exists():
        return stats
    for f in root.rglob("*"):
        if f.is_file():
            if should_skip(f):
                continue
            try:
                size = f.stat().st_size
            except Exception:
                continue
            stats['total_size'] += size
            stats['files'] += 1
            if f.suffix.lower() == '.md':
                stats['md'] += 1
            elif f.suffix.lower() == '.pdf':
                stats['pdf'] += 1
            elif f.suffix.lower() in ('.docx', '.doc'):
                stats['docx'] += 1
            elif f.suffix.lower() == '.txt':
                stats['txt'] += 1
            elif f.suffix.lower() == '.json':
                stats['json'] += 1
            elif f.suffix.lower() in ('.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg'):
                stats['images'] += 1
            else:
                stats['other'] += 1
    return stats


def main():
    print("=" * 80)
    print("本机全盘扫描 · 找出所有可纳入 vault 的内容")
    print("=" * 80)

    # 1. 整体统计
    print("\n[1] D:\\B166ER-OpenClaw 全部")
    b166_root = Path(r"D:\B166ER-OpenClaw")
    s = count_files(b166_root)
    print(f"  Total files: {s['files']}")
    print(f"  .md: {s['md']}  .pdf: {s['pdf']}  .docx: {s['docx']}  .json: {s['json']}  .txt: {s['txt']}  images: {s['images']}  other: {s['other']}")
    print(f"  Total size: {s['total_size']/1024/1024/1024:.2f}GB")

    # 2. workspace 子目录
    print("\n[2] D:\\B166ER-OpenClaw\\workspace 子目录 (按 .md 数排序)")
    ws = b166_root / "workspace"
    if ws.exists():
        dirs = []
        for d in ws.iterdir():
            if d.is_dir() and not should_skip(d):
                ds = count_files(d)
                if ds['md'] > 0:
                    dirs.append((d.name, ds['md'], ds['total_size']))
        dirs.sort(key=lambda x: -x[1])
        for name, md_count, size in dirs[:30]:
            print(f"  {name:35s}  {md_count:5d} .md  {size/1024/1024:6.1f}MB")

    # 3. workspace 之外（B166ER 根其他子目录）
    print("\n[3] D:\\B166ER-OpenClaw 其他子目录（workspace 外）")
    for d in b166_root.iterdir():
        if d.is_dir() and d.name != 'workspace' and not should_skip(d):
            ds = count_files(d)
            if ds['md'] > 0 or ds['files'] > 5:
                print(f"  {d.name:40s}  {ds['files']:5d} files  {ds['md']:4d} .md  {ds['total_size']/1024/1024:6.1f}MB")

    # 4. C:\Users\ericz 关键目录
    print("\n[4] C:\\Users\\ericz 关键目录")
    user_root = Path(r"C:\Users\ericz")
    for d in user_root.iterdir():
        if d.is_dir() and not should_skip(d):
            try:
                # 只看顶层
                md_count = sum(1 for f in d.glob("*.md") if f.is_file())
                if md_count > 0:
                    total = sum(f.stat().st_size for f in d.rglob("*") if f.is_file() and not should_skip(f))
                    print(f"  {d.name:40s}  {md_count:4d} .md (top)  {total/1024/1024:6.1f}MB total")
            except Exception:
                pass

    # 5. 全部 .md 数量
    print("\n[5] 全部 .md 统计")
    total_md = s['md']
    print(f"  workspace 全部 .md: {total_md}")


if __name__ == "__main__":
    main()
