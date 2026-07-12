#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
emergence_curator.py — Obsidian 涌现整理器

设计理念: vault 是 B166ER 的知识库, 沉淀 + 迭代 + 涌现

功能:
- 每日 21:30 跑 (cron-push-checker 之后)
- 读当天 cron-push/YYYY-MM-DD/ 所有推送
- 提取关键概念/事件/数字
- 写入 emergence/ 当日 MOC
- 写 knowledge graph 节点
- 推送 5 句话日报到 webchat

涌现 vs 推送的区别:
- 推送: 原始报告入库 (cron_to_obsidian.py 干的事)
- 涌现: 跨推送归纳 → 形成 MOC/索引/知识网络

时间表:
- 每日 21:30: 整理当日推送 → 写 emergence/daily/YYYY-MM-DD.md
- 每周日 21:30: 跨天归纳 → 写 emergence/weekly/YYYY-Www.md
- 每月 1 日 21:30: 跨周归纳 → 写 emergence/monthly/YYYY-MM.md
"""
import os
import sys
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict

VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")
PUSH_DIR = VAULT / "00-Inbox-待整理" / "cron-push"
EMERGENCE_DIR = VAULT / "emergence"

# 关键概念提取 (简单 regex)
CONCEPT_PATTERNS = [
    (r'\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,3})\b', 'proper_noun'),  # 专有名词
    (r'\b(\d+\.?\d*)\s*(亿|万|%|元|美元|人民币|JPY|USD|CNY)\b', 'number'),  # 数字
    (r'#(\w+)', 'hashtag'),  # 标签
    (r'@(\w+)', 'mention'),  # 提及
]


def extract_concepts(content: str) -> dict:
    """从一个推送文件提取关键概念"""
    concepts = defaultdict(list)
    for pattern, ptype in CONCEPT_PATTERNS:
        for match in re.finditer(pattern, content):
            concepts[ptype].append(match.group(0))
    # 去重
    for k in concepts:
        concepts[k] = sorted(set(concepts[k]))[:30]  # 限制 30 个
    return dict(concepts)


def read_push_files(date_str: str) -> list:
    """读当天所有推送文件"""
    date_dir = PUSH_DIR / date_str
    if not date_dir.exists():
        return []
    files = []
    for f in sorted(date_dir.glob("*.md")):
        try:
            content = f.read_text(encoding="utf-8")
            # 提取 frontmatter
            fm_match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
            if fm_match:
                frontmatter = fm_match.group(1)
                body = fm_match.group(2)
            else:
                frontmatter = ""
                body = content
            # 提取 task 名
            task_match = re.search(r'task:\s*(.+)', frontmatter)
            importance_match = re.search(r'importance:\s*(\w+)', frontmatter)
            files.append({
                'file': f,
                'name': f.name,
                'task': task_match.group(1).strip() if task_match else 'unknown',
                'importance': importance_match.group(1) if importance_match else 'normal',
                'body': body,
                'size': f.stat().st_size
            })
        except Exception as e:
            print(f"  ERR reading {f.name}: {e}", file=sys.stderr)
    return files


def generate_daily_moc(date_str: str, files: list) -> str:
    """生成当日 MOC (Map of Content)"""
    if not files:
        return f"# {date_str} · 涌现 MOC\n\n> 当日无 cron 推送\n"

    # 收集所有概念
    all_concepts = defaultdict(int)
    high_importance = []
    normal_importance = []

    for f in files:
        concepts = extract_concepts(f['body'])
        for ptype, items in concepts.items():
            for item in items:
                all_concepts[f"{ptype}:{item}"] += 1
        if f['importance'] in ('urgent', 'high'):
            high_importance.append(f)
        else:
            normal_importance.append(f)

    # Top 20 概念
    top_concepts = sorted(all_concepts.items(), key=lambda x: -x[1])[:20]

    # 构建 MOC
    lines = [
        f"---",
        f"author: b166er-emergence",
        f"audience: both",
        f"type: emergence-moc",
        f"date: {date_str}",
        f"source_count: {len(files)}",
        f"created: {datetime.now().isoformat()}",
        f"---",
        f"",
        f"# 🌅 {date_str} · 涌现 MOC (Map of Content)",
        f"",
        f"> 当日共 {len(files)} 条 cron 推送，{len(high_importance)} 条高重要度",
        f"> 自动整理 by emergence_curator.py · 21:30 跑",
        f"",
        f"## 🔴 高重要度推送",
        f"",
    ]

    for f in high_importance:
        # 提取文件首句作为简介
        first_para = f['body'].split('\n\n')[0] if f['body'] else ''
        # 提取推送文件名对应 vault 路径
        rel_path = f"../00-Inbox-待整理/cron-push/{date_str}/{f['name']}"
        lines.append(f"### {f['task']}")
        lines.append(f"- 文件：[[{rel_path}|{f['name']}]] ({f['size']}b)")
        if first_para:
            lines.append(f"- 摘要：{first_para[:150]}")
        lines.append("")

    lines.extend([
        f"## 🟡 常规推送",
        f"",
    ])

    for f in normal_importance:
        rel_path = f"../00-Inbox-待整理/cron-push/{date_str}/{f['name']}"
        lines.append(f"- {f['task']} · [[{rel_path}|{f['name']}]]")
    lines.append("")

    lines.extend([
        f"## 🧠 涌现概念 (Top 20)",
        f"",
        f"| 概念 | 类型 | 出现次数 |",
        f"|------|------|----------|",
    ])

    for concept, count in top_concepts:
        ptype, name = concept.split(':', 1)
        type_emoji = {
            'proper_noun': '📌', 'number': '🔢', 'hashtag': '🏷️', 'mention': '@'
        }.get(ptype, '·')
        lines.append(f"| {name} | {type_emoji} {ptype} | {count} |")

    lines.extend([
        f"",
        f"## 🔗 跨推送关联",
        f"",
        f"- (涌现层 v1: 基于关键词共现)",
        f"- (涌现层 v2: 基于 ontology graph.jsonl - 待)",
        f"",
        f"---",
        f"",
        f"*涌现整理 by B166ER emergence_curator.py · 21:30 daily*",
    ])

    return "\n".join(lines)


def generate_daily_summary(date_str: str, files: list) -> str:
    """生成 5 句话日报 (用于 webchat 推送)"""
    if not files:
        return f"{date_str} 无 cron 推送"

    high = [f for f in files if f['importance'] in ('urgent', 'high')]
    normal = [f for f in files if f['importance'] not in ('urgent', 'high')]

    high_names = "、".join([f['task'] for f in high[:3]])
    if not high_names:
        high_names = "无"

    summary = f"""📊 **{date_str} 涌现日报**
- 共 {len(files)} 条推送 ({len(high)} 高 / {len(normal)} 常)
- 重点: {high_names}
- 全部归档: obsidian-vault/cron-push/{date_str}/
- MOC 已生成: emergence/daily/{date_str}.md
- 涌现层 v1 工作中"""
    return summary


def update_emergence_index(date_str: str, file_count: int):
    """更新 emergence/INDEX.md (总索引)"""
    index_path = EMERGENCE_DIR / "INDEX.md"
    EMERGENCE_DIR.mkdir(parents=True, exist_ok=True)

    # 读现有 INDEX (如果有)
    if index_path.exists():
        content = index_path.read_text(encoding="utf-8")
    else:
        content = """---
author: b166er-emergence
audience: both
type: emergence-index
status: active
created: 2026-07-12
---

# 🌐 Emergence 总索引

> 所有 cron 推送的涌现层。每日 21:30 自动更新。
> 入口：每天打开这里看 MOC，不需要翻 100 条原始推送。

## 📅 每日 MOC

"""

    # 在"每日 MOC"段落后追加新行
    new_line = f"- [[daily/{date_str}|{date_str}]] — {file_count} 推送\n"
    if new_line not in content:
        # 找到"## 📅 每日 MOC"位置
        if "## 📅 每日 MOC" in content:
            content = content.replace(
                "## 📅 每日 MOC\n\n",
                f"## 📅 每日 MOC\n\n{new_line}"
            )
        else:
            content += f"\n## 📅 每日 MOC\n\n{new_line}"
        index_path.write_text(content, encoding="utf-8")


def main():
    """主流程: 整理当天 + 更新总索引"""
    # 支持 --date 参数
    if "--date" in sys.argv:
        idx = sys.argv.index("--date")
        date_str = sys.argv[idx + 1]
    else:
        date_str = datetime.now().strftime("%Y-%m-%d")

    print(f"=" * 60)
    print(f"emergence_curator · {date_str}")
    print(f"=" * 60)

    # 1. 读当天推送
    files = read_push_files(date_str)
    print(f"  Found {len(files)} push files")

    if not files:
        print(f"  No pushes for {date_str} - skip MOC generation")
        return 0

    # 2. 生成 MOC
    daily_dir = EMERGENCE_DIR / "daily"
    daily_dir.mkdir(parents=True, exist_ok=True)
    moc_path = daily_dir / f"{date_str}.md"
    moc_content = generate_daily_moc(date_str, files)
    moc_path.write_text(moc_content, encoding="utf-8")
    print(f"  [OK] MOC: {moc_path} ({moc_path.stat().st_size}b)")

    # 3. 更新总索引
    update_emergence_index(date_str, len(files))
    print(f"  [OK] INDEX updated")

    # 4. 生成日报 (给 webchat)
    summary = generate_daily_summary(date_str, files)
    sys.stdout.reconfigure(encoding='utf-8')
    print()
    print(summary)
    print()

    # 5. 写日报到 emergence/daily/ (便于次日 webchat 报告)
    summary_path = daily_dir / f"{date_str}-summary.md"
    summary_path.write_text(f"""---
author: b166er-emergence
audience: eric
date: {date_str}
type: daily-summary
---

{summary}
""", encoding="utf-8")
    print(f"  [OK] Summary: {summary_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
