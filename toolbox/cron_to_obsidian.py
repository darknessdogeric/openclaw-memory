#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
cron_to_obsidian.py — Cron 任务输出 → Obsidian vault 推送器

Usage:
  python cron_to_obsidian.py --task "任务名" --content "内容" [--importance high] [--summary "一句话摘要"]
  python cron_to_obsidian.py --task "深度自检晚间" --content-file "/path/to/file.md" --importance high
  python cron_to_obsidian.py --json '{"task": "...", "content": "..."}'

效果:
  - 写入 obsidian-vault/00-Inbox-待整理/cron-push/YYYY-MM-DD/HH-MM-{task}.md
  - 自动加 frontmatter (author/audience/task/importance/pushed_at)
  - 可选 --append-daily 把摘要追加到 01-日记/YYYY-MM-DD.md
"""
import os, sys, json, argparse
from datetime import datetime

VAULT = r'D:\B166ER-OpenClaw\workspace\obsidian-vault'
PUSH_BASE = os.path.join(VAULT, '00-Inbox-待整理', 'cron-push')

# 重要度映射
IMPORTANCE_EMOJI = {
    'urgent': '🟣',
    'high': '🔴',
    'normal': '🟡',
    'low': '⚪',
}

def safe_filename(name):
    """清理文件名，只保留字母数字和-_"""
    return ''.join(c if c.isalnum() or c in '-_' else '-' for c in name)[:80]

def push_to_obsidian(task_name, content, importance='normal', summary=None, tags=None):
    """推送一条 cron 输出到 Obsidian"""
    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H-%M')
    
    # 创建日期文件夹
    date_dir = os.path.join(PUSH_BASE, date_str)
    os.makedirs(date_dir, exist_ok=True)
    
    # 文件名（避免重复）
    base_name = safe_filename(task_name)
    file_path = os.path.join(date_dir, f'{time_str}-{base_name}.md')
    counter = 1
    while os.path.exists(file_path):
        file_path = os.path.join(date_dir, f'{time_str}-{base_name}-{counter}.md')
        counter += 1
    
    # Frontmatter
    tags_list = tags or ['cron-push']
    tags_str = ' '.join(tags_list)
    emoji = IMPORTANCE_EMOJI.get(importance, '🟡')
    
    # 完整 markdown
    md_parts = [
        '---',
        'author: b166er',
        'audience: eric',
        f'task: {task_name}',
        f'importance: {importance}',
        f'pushed_at: {now.isoformat()}',
        'source: cron',
        'status: active',
        f'tags: [{tags_str}]',
        '---',
        '',
        f'# {emoji} {task_name}',
        '',
        f'> **推送时间**: {now.strftime("%Y-%m-%d %H:%M:%S")}',
        f'> **来源**: Cron 任务自动推送',
        f'> **重要度**: {importance}',
        '',
    ]
    
    if summary:
        md_parts.extend(['## 📋 摘要', '', summary, ''])
    
    md_parts.extend(['## 📄 内容', '', content, '', '---', ''])
    md_parts.extend([
        '## 🔗 相关',
        '',
        '- [[../../../../20-我们共同维护的/00-Dashboard]]',
        '- [[../../../../20-我们共同维护的/00-今日重点]]',
        '',
        '*由 `cron_to_obsidian.py` 自动推送*',
    ])
    
    md = '\n'.join(md_parts)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(md)
    
    # === R25 hook: 增强关联 + MOC 追加 ===
    try:
        enrich_with_links(file_path, task_name, content, importance)
    except Exception as e:
        # 失败不阻塞推送（避免 cron 失败）
        print(f'enrich_with_links warning: {e}', file=sys.stderr)
    
    return file_path


def enrich_with_links(file_path, task_name, content, importance='normal'):
    """
    R25 hook: 推送后自动增强关联
    - 找 vault 中相关笔记 → 加 [[wikilink]]
    - 找匹配 MOC → 追加新笔记引用
    - 高 importance 额外处理
    """
    import re
    from pathlib import Path
    
    # 只对 high / urgent 处理 (避免噪音)
    if importance not in ('high', 'urgent'):
        return
    
    fp = Path(file_path)
    if not fp.exists():
        return
    
    # 提取关键词
    text = f"{task_name}\n{content[:5000]}"
    cn_kws = re.findall(r'[\u4e00-\u9fff]{4,}', text)
    en_kws = re.findall(r'\b[A-Z][a-zA-Z]{2,}\b', text)
    keywords = list(set(cn_kws + en_kws))[:15]
    
    # 在 vault 中找相关笔记 (不扫 50-外部接入/03-维景 大目录)
    VAULT_ROOT = Path(r'D:\B166ER-OpenClaw\workspace\obsidian-vault')
    related_scores = {}
    for f in VAULT_ROOT.rglob('*.md'):
        rel = str(f.relative_to(VAULT_ROOT))
        if any(x in rel for x in ['50-外部接入/03-维景', '.obsidian', 'cron-push/']):
            continue
        try:
            c = f.read_text(encoding='utf-8')[:5000]
        except Exception:
            continue
        score = sum(1 for kw in keywords if kw.lower() in c.lower())
        if score >= 2:
            related_scores[f] = score
    
    related_top = sorted(related_scores.items(), key=lambda x: -x[1])[:5]
    
    if not related_top:
        return
    
    # 在推送文件底部追加相关链接 + 相关 MOC
    md_text = fp.read_text(encoding='utf-8')
    extra_lines = ['\n## 🔗 自动关联 (R25)', '']
    for f, s in related_top:
        rel = str(f.relative_to(VAULT_ROOT)).replace('\\', '/')
        extra_lines.append(f'- [[{rel}|{f.stem}]] (匹配 {s})')
    
    # 检查 MOC 匹配
    MOC_THEMES = {
        'AHL 平台 MOC': ['AHL', 'ahl', 'Agent', 'SKILL', '乐山', '锦江'],
        '酒店行业 MOC': ['酒店', 'OTA', '收益', '客房', '维景', 'SOP'],
        'AI-Agent MOC': ['AI', 'Agent', 'LLM', 'MCP', '向量'],
        '战略-方法论 MOC': ['战略', '博弈', '群论', '审美', '复盘'],
        '安逸集团-D-day MOC': ['安逸', '省旅投', 'D-day', '党委会', '产业', '入职'],
        'Eric 人格-审美 MOC': ['Eric', '张实', '音乐', '人格', '审美'],
        '工具-系统 MOC': ['OpenClaw', 'cron', 'Obsidian', 'Python', 'scrap'],
        '跨境-出海 MOC': ['跨境', '亚马逊', '阿联酋', 'Booking', 'Agoda'],
    }
    matched_mocs = []
    for moc_name, kws in MOC_THEMES.items():
        if any(kw.lower() in text.lower() for kw in kws):
            matched_mocs.append(moc_name)
    
    if matched_mocs:
        extra_lines.append('')
        extra_lines.append('**📂 相关 MOC**:')
        for m in matched_mocs[:3]:
            extra_lines.append(f'- [[emergence/hubs/{m}|{m}]]')
    
    md_text += '\n' + '\n'.join(extra_lines) + '\n'
    fp.write_text(md_text, encoding='utf-8')

def append_to_daily(summary, task_name):
    """追加一条摘要到今日日记"""
    import re as _re
    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    daily_path = os.path.join(VAULT, '01-日记', f'{date_str}.md')
    
    if not os.path.exists(daily_path):
        return False
    
    with open(daily_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    timestamp = now.strftime('%H:%M')
    push_link = f'../00-Inbox-待整理/cron-push/{date_str}/{timestamp.replace(":","-")}-{safe_filename(task_name)}'
    line = f'- {timestamp} · [[{push_link}|{task_name}]] · {summary}'
    
    # 找 B166ER 输出物 section（regex 灵活匹配）
    match = _re.search(r'^## B166ER 输出物.*$', content, _re.MULTILINE)
    if match:
        # 在匹配的 heading 后插入
        insert_pos = match.end()
        # 找到下一行
        next_newline = content.find('\n', insert_pos)
        content = content[:next_newline+1] + line + '\n' + content[next_newline+1:]
    else:
        # 追加到末尾
        content += f'\n## B166ER 输出物\n\n{line}\n'
    
    with open(daily_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Cron → Obsidian vault 推送')
    parser.add_argument('--task', help='Cron 任务名（--json 模式下可省略）')
    parser.add_argument('--content', help='推送内容（字符串）')
    parser.add_argument('--content-file', help='从文件读取内容')
    parser.add_argument('--importance', default='normal', choices=['urgent','high','normal','low'])
    parser.add_argument('--summary', help='一句话摘要')
    parser.add_argument('--tags', help='逗号分隔的标签')
    parser.add_argument('--append-daily', action='store_true', help='追加摘要到今日日记')
    parser.add_argument('--json', help='JSON 字符串输入（覆盖其他参数）')
    
    args = parser.parse_args()
    
    # JSON 模式
    if args.json:
        data = json.loads(args.json)
        task = data['task']
        content = data.get('content', '')
        if 'content_file' in data:
            with open(data['content_file'], 'r', encoding='utf-8') as f:
                content = f.read()
        importance = data.get('importance', 'normal')
        summary = data.get('summary')
        tags = data.get('tags')
    else:
        task = args.task
        content = args.content or ''
        if args.content_file:
            with open(args.content_file, 'r', encoding='utf-8') as f:
                content = f.read()
        importance = args.importance
        summary = args.summary
        tags = args.tags.split(',') if args.tags else None
    
    # 推送
    file_path = push_to_obsidian(task, content, importance, summary, tags)
    
    # 追加到日记
    daily_ok = False
    if args.append_daily and summary:
        daily_ok = append_to_daily(summary, task)
    
    # 输出结果（供 cron 任务读取）
    result = {
        'success': True,
        'task': task,
        'file': file_path,
        'importance': importance,
        'appended_to_daily': daily_ok,
        'pushed_at': datetime.now().isoformat(),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    return 0

if __name__ == '__main__':
    sys.exit(main())