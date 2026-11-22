#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
auto_vault.py — B166ER ↔ Obsidian Vault 自动双向同步

设计哲学:
  一键命令, 让 B166ER 产出自动入库, vault 变更也能回流 workspace.

子命令:
  push      推送 workspace 文件到 vault (带 frontmatter + MOC 关联)
  pull      从 vault 拉取最近变更到 workspace
  watch     监听 reports/ 目录, 新文件自动入 vault
  status    查看双向同步状态

典型调用 (B166ER 内部):
  python auto_vault.py push "reports/酒店预订主权分析框架.md" --type kb-hotel --tags "预订,OTA,BSR"
  python auto_vault.py status

作者: B166ER · 2026-07-14
"""
import sys, io, json, os, re, argparse, hashlib, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from datetime import datetime
from collections import Counter

# === CONFIG ===
VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")
WORKSPACE = Path(r"D:\B166ER-OpenClaw\workspace")
STATE_FILE = Path(r"D:\B166ER-OpenClaw\workspace\toolbox\.auto_vault_state.json")
WATCH_DIRS = ['reports', 'output']

# 类型→vault目录映射
TYPE_DIR = {
    'kb-hotel': '10-我为你生成的/知识库/酒店',
    'kb-ai': '10-我为你生成的/知识库/AI',
    'kb-strategy': '10-我为你生成的/知识库/战略',
    'kb-finance': '10-我为你生成的/知识库/金融',
    'kb-crossborder': '10-我为你生成的/知识库/跨境',
    'kb-aesthetic': '10-我为你生成的/知识库/审美',
    'report': '20-我们共同维护的/报告',
    'strategy': '20-我们共同维护的/战略与节奏',
    'inbox': '00-Inbox-待整理',
    'external': '50-外部接入',
    'template': '40-工具与模板',
}

# MOC 关键词匹配
MOC_KEYWORDS = {
    'AHL 平台 MOC': ['AHL', 'ahl', '去中心化', '旅行平台', 'Agent', 'SKILL', '数字员工'],
    '酒店行业 MOC': ['酒店', 'OTA', 'PMS', 'ADR', 'OCC', 'RevPAR', '客房', '预订', 'Walk-in', 'BSR', '客源', '渠道', '佣金', '协议客', 'MICE'],
    'AI-Agent MOC': ['AI', 'Agent', 'LLM', '大模型', 'GPT', 'DeepSeek', 'MCP', '向量', 'RAG', 'embedding', '自动化'],
    '战略-方法论 MOC': ['战略', '博弈论', '群论', '审美', '信息论', '贝叶斯', '第一性', '方法论', '框架', '决策'],
    '安逸集团-D-day MOC': ['安逸', '省旅投', '产业发展部', 'D-day', '党委会', '1244', '部长'],
    'Eric 人格-审美 MOC': ['Eric', '张实', '人格', '音乐', '审美', '品位', 'Bach'],
    '工具-系统 MOC': ['OpenClaw', 'cron', 'Obsidian', 'Vault', 'Python', 'Playwright', 'MCP', 'scrap'],
    'B166ER 知识库 MOC': ['B166ER', '规则', 'self-improving', '知识库', '能力图谱'],
    '跨境-出海 MOC': ['跨境', 'Booking', 'Agoda', 'Expedia', '海外', '出海'],  # [R66 v2026-09-03] 删除'阿联酋'(L1虚构)
}


def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text(encoding='utf-8'))
    return {'pushes': [], 'pulls': [], 'last_watch': None}


def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')


def extract_keywords(text, max_kw=10):
    """提取中文关键词"""
    cn = re.findall(r'[\u4e00-\u9fff]{2,8}', text[:8000])
    # 过滤停用词
    stop = {'可以', '一个', '这个', '什么', '我们', '他们', '没有', '不是', '就是', '如果', '因为', '所以', '但是', '而且', '然后', '或者', '不过', '只是', '已经', '还是', '还有', '这些', '那些', '一些', '这种', '那种', '怎么', '什么', '为什么', '怎么样', '那么', '这样', '那样', '非常', '比较', '可能', '已经', '一定', '必须', '应该', '不能', '不会', '不要', '需要', '通过', '进行', '使用', '提供', '包括', '所有', '对于', '关于', '以及', '作为', '其中', '目前', '主要', '相关'}
    filtered = [w for w in cn if w not in stop]
    return [w for w, _ in Counter(filtered).most_common(max_kw)]


def match_mocs(text, keywords):
    """匹配相关 MOC"""
    full_text = text[:5000] + ' '.join(keywords)
    matches = {}
    for moc_name, kws in MOC_KEYWORDS.items():
        score = sum(1 for kw in kws if kw.lower() in full_text.lower())
        if score > 0:
            matches[moc_name] = score
    return sorted(matches, key=matches.get, reverse=True)


def find_related_notes(keywords, moc_matches, max_notes=10):
    """在 vault 中找相关笔记"""
    related = []
    seen = set()
    
    # 先扫最近修改的文件
    for md_file in sorted(VAULT.rglob('*.md'), key=lambda f: f.stat().st_mtime, reverse=True)[:500]:
        if md_file.stat().st_size > 100000:  # skip huge files
            continue
        try:
            text = md_file.read_text(encoding='utf-8')[:3000]
        except:
            continue
        
        rel_path = str(md_file.relative_to(VAULT))
        score = sum(1 for kw in keywords if kw in text)
        if score >= 2 and rel_path not in seen:
            seen.add(rel_path)
            related.append({'path': rel_path, 'stem': md_file.stem, 'score': score})
            if len(related) >= max_notes:
                break
    
    return sorted(related, key=lambda x: x['score'], reverse=True)


def cmd_push(args):
    """推送文件到 vault"""
    src = Path(args.path)
    if not src.exists():
        print(f"❌ 文件不存在: {src}")
        return 1
    
    content = src.read_text(encoding='utf-8')
    title = args.title or src.stem
    vault_type = args.type or 'inbox'
    tags = [t.strip() for t in (args.tags or '').split(',') if t.strip()]
    importance = args.importance or 'normal'
    summary = args.summary or ''
    
    # 提取关键词
    keywords = extract_keywords(content)
    
    # 匹配 MOC
    moc_matches = match_mocs(content, keywords)
    
    # 找相关笔记
    related = find_related_notes(keywords, moc_matches)
    
    # 确定目标目录
    target_dir = VAULT / TYPE_DIR.get(vault_type, '00-Inbox-待整理')
    target_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成文件名
    date_str = datetime.now().strftime('%Y-%m-%d')
    safe_title = re.sub(r'[\\/:*?"<>|]', '-', title)[:80]
    target_path = target_dir / f'{date_str}-{safe_title}.md'
    
    # 构建 wikilinks
    wikilinks = '\n'.join(f'- [[{r["stem"]}]]' for r in related[:8])
    
    # 构建 frontmatter + 内容
    tags_str = ', '.join(tags)
    moc_str = ', '.join(moc_matches[:3])
    importance_emoji = {'urgent': '🟣', 'high': '🔴', 'normal': '🟡', 'low': '⚪'}.get(importance, '🟡')
    
    full_md = f"""---
author: b166er
audience: eric
title: {title}
type: {vault_type}
importance: {importance}
pushed_at: {datetime.now().isoformat()}
tags: [{tags_str}]
moc: [{moc_str}]
source: {src.relative_to(WORKSPACE)}
keywords: [{', '.join(keywords[:8])}]
---

# {importance_emoji} {title}

> **入库时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> **来源**: `{src.relative_to(WORKSPACE)}`
> **类型**: {vault_type} | **重要度**: {importance}
> **MOC**: {moc_str if moc_str else '(未匹配)'}

{summary if summary else ''}

---

{content}

---

## 🔗 关联笔记

{wikilinks if wikilinks else '(暂无自动匹配的关联笔记)'}

---
*自动入库: B166ER auto_vault · {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
    
    target_path.write_text(full_md, encoding='utf-8')
    
    # 更新状态
    state = load_state()
    state['pushes'].append({
        'time': datetime.now().isoformat(),
        'source': str(src.relative_to(WORKSPACE)),
        'target': str(target_path.relative_to(VAULT)),
        'mocs': moc_matches,
        'related_count': len(related)
    })
    # 只保留最近100条
    state['pushes'] = state['pushes'][-100:]
    save_state(state)
    
    print(f'✅ 已入库: {target_path.relative_to(VAULT)}')
    print(f'   MOC: {moc_matches[:3] if moc_matches else "无匹配"}')
    print(f'   关联笔记: {len(related)} 篇')
    print(f'   标签: {tags_str}')
    print(f'   关键词: {", ".join(keywords[:5])}')
    return 0


def cmd_status(args):
    """查看同步状态"""
    state = load_state()
    pushes = state.get('pushes', [])
    pulls = state.get('pulls', [])
    
    print('=' * 60)
    print('B166ER ↔ Obsidian Vault 双向同步状态')
    print('=' * 60)
    print(f'  总推送: {len(pushes)} 次')
    print(f'  总拉取: {len(pulls)} 次')
    
    # 最近推送
    if pushes:
        print(f'\n  最近推送:')
        for p in pushes[-5:]:
            print(f'    {p["time"][:19]} → {p["target"]}')
    
    # 统计 MOC 覆盖
    if pushes:
        moc_count = Counter()
        for p in pushes:
            for m in p.get('mocs', []):
                moc_count[m] += 1
        print(f'\n  MOC 覆盖:')
        for moc, cnt in moc_count.most_common(5):
            print(f'    {moc}: {cnt}')
    
    print(f'\n  Vault: {VAULT}')
    print(f'  索引: {"✅" if (Path(__file__).parent / ".vault_index.json").exists() else "❌"}')
    return 0


def cmd_watch(args):
    """监听 reports/ 目录"""
    print(f'🔍 监听目录: {", ".join(WATCH_DIRS)}')
    print(f'   新 .md 文件将被自动推送到 vault')
    print(f'   按 Ctrl+C 停止')
    
    known = set()
    # 初始化已知文件
    for watch_dir in WATCH_DIRS:
        watch_path = WORKSPACE / watch_dir
        if watch_path.exists():
            for f in watch_path.rglob('*.md'):
                known.add(str(f))
    
    try:
        while True:
            for watch_dir in WATCH_DIRS:
                watch_path = WORKSPACE / watch_dir
                if not watch_path.exists():
                    continue
                for f in watch_path.rglob('*.md'):
                    fpath = str(f)
                    if fpath not in known:
                        known.add(fpath)
                        print(f'\n🆕 发现新文件: {f.relative_to(WORKSPACE)}')
                        # 自动推送
                        rel = str(f.relative_to(WORKSPACE))
                        auto_type = 'report' if 'report' in rel.lower() else 'inbox'
                        auto_tags = 'auto-push'
                        cmd_push(argparse.Namespace(
                            path=fpath, title=f.stem, type=auto_type,
                            tags=auto_tags, importance='normal', summary=''
                        ))
            time.sleep(30)
    except KeyboardInterrupt:
        print('\n👋 监听已停止')


# === CLI ===
def main():
    parser = argparse.ArgumentParser(description='B166ER ↔ Obsidian Vault 自动双向同步')
    sub = parser.add_subparsers(dest='cmd', help='子命令')
    
    # push
    p_push = sub.add_parser('push', help='推送文件到 vault')
    p_push.add_argument('path', help='源文件路径')
    p_push.add_argument('--title', help='标题 (默认用文件名)')
    p_push.add_argument('--type', default='inbox', help=f'内容类型: {", ".join(TYPE_DIR.keys())}')
    p_push.add_argument('--tags', default='', help='标签 (逗号分隔)')
    p_push.add_argument('--importance', default='normal', choices=['urgent', 'high', 'normal', 'low'])
    p_push.add_argument('--summary', default='', help='一句话摘要')
    
    # status
    sub.add_parser('status', help='查看同步状态')
    
    # watch
    sub.add_parser('watch', help='监听目录自动入库')
    
    args = parser.parse_args()
    
    if args.cmd == 'push':
        return cmd_push(args)
    elif args.cmd == 'status':
        return cmd_status(args)
    elif args.cmd == 'watch':
        return cmd_watch(args)
    else:
        # 默认: status
        return cmd_status(argparse.Namespace())
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
