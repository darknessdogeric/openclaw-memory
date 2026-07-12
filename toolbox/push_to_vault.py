#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
push_to_vault.py — 对话产出实时入 vault + 自动关联

设计理念:
  每次 B166ER 产生"重要产出"时调用此脚本
  → 写入 vault 对应目录
  → 自动 frontmatter (tags/type/related)
  → 关键词匹配找已有笔记 → 生成 [[wikilink]]
  → 可选: 追加到对应 MOC

用法:
  python push_to_vault.py --title "标题" --content "内容" --type kb --tags "酒店,收益" --importance high
  python push_to_vault.py --title "标题" --content-file /tmp/output.md --type report --tags "五一,复盘"
  python push_to_vault.py --title "标题" --content -  (stdin)

作者: B166ER · 2026-07-12
"""
import sys, io, json, re, argparse
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from datetime import datetime
from collections import Counter

VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")

# 类型 → 目录映射
TYPE_DIR_MAP = {
    'kb': '10-我为你生成的/知识库',
    'kb-hotel': '10-我为你生成的/知识库/酒店',
    'kb-ai': '10-我为你生成的/知识库/AI',
    'kb-crossborder': '10-我为你生成的/知识库/跨境',
    'kb-finance': '10-我为你生成的/知识库/金融',
    'kb-strategy': '10-我为你生成的/知识库/战略',
    'kb-aesthetic': '10-我为你生成的/知识库/审美',
    'report': '20-我们共同维护的/报告',
    'strategy': '20-我们共同维护的/战略与节奏',
    'diary': '01-日记',
    'inbox': '00-Inbox-待整理',
    'external': '50-外部接入',
}

# MOC 主题关键词
MOC_THEMES = {
    'AHL 平台 MOC': ['AHL', 'ahl', '去中心化', 'Agent', 'SKILL', '乐山', '苏州酒管', '酒店智能'],
    '酒店行业 MOC': ['酒店', 'OTA', 'PMS', 'ADR', 'OCC', 'RevPAR', '客房', '前台', '餐饮', 'SOP', '维景', '入住率'],
    'AI-Agent MOC': ['AI', 'Agent', 'LLM', '大模型', 'GPT', 'DeepSeek', 'Claude', 'MCP', '向量', 'RAG', 'embedding'],
    '战略-方法论 MOC': ['战略', '博弈论', '群论', '审美', '信息论', '贝叶斯', '第一性', '奥卡姆', '元认知', '复盘'],
    '安逸集团-D-day MOC': ['安逸', '省旅投', '产业发展部', 'D-day', '党委会', '公示', '入职', '1244'],
    'Eric 人格-审美 MOC': ['张实', 'Eric', '人格', '音乐', '手风琴', '俄罗斯', '昭和', '维吾尔', 'Bach', '审美'],
    '工具-系统 MOC': ['OpenClaw', 'cron', 'Obsidian', 'Vault', 'Python', 'PowerShell', 'scrap', 'Playwright'],
    'B166ER 知识库 MOC': ['B166ER', 'R 规则', 'self-improving', '能力图谱'],
    '跨境-出海 MOC': ['跨境', '亚马逊', '阿联酋', '本奥米尔', '出海', '境外', 'Booking', 'Agoda'],
}


def extract_keywords(text: str, max_kw: int = 10) -> list:
    """从文本提取中文关键词 (4+ 字) + 英文专有名词"""
    cn = [w for w, _ in Counter(re.findall(r'[\u4e00-\u9fff]{4,}', text[:10000])).most_common(max_kw)]
    en = [w for w, _ in Counter(re.findall(r'\b[A-Z][a-zA-Z]{2,}\b', text[:10000])).most_common(max_kw)]
    return cn + en


def find_related_notes(keywords: list, top_n: int = 10) -> list:
    """基于关键词在 vault 中找相关笔记 (不扫外部接入/emergence)"""
    scores = {}
    for f in VAULT.rglob("*.md"):
        # 跳过大型目录
        rel = str(f.relative_to(VAULT))
        if any(x in rel for x in ['50-外部接入/03-维景', 'emergence/graph', '.obsidian']):
            continue
        try:
            content = f.read_text(encoding="utf-8")[:8000]
        except Exception:
            continue
        score = 0
        for kw in keywords:
            if kw.lower() in content.lower():
                score += 1
        if score >= 2:
            scores[f] = score

    # 返回 top_n
    ranked = sorted(scores.items(), key=lambda x: -x[1])[:top_n]
    results = []
    for f, s in ranked:
        rel = str(f.relative_to(VAULT)).replace('\\', '/')
        results.append({'path': rel, 'name': f.stem, 'score': s, 'size': f.stat().st_size})
    return results


def find_best_moc(keywords: list) -> list:
    """找匹配的 MOC"""
    matches = []
    for moc_name, moc_kws in MOC_THEMES.items():
        score = sum(1 for kw in keywords if any(mk.lower() in kw.lower() for mk in moc_kws))
        if score >= 1:
            matches.append((moc_name, score))
    return [m[0] for m in sorted(matches, key=lambda x: -x[1])[:3]]


def determine_tags(keywords: list, content_type: str) -> str:
    """自动生成 tags"""
    tags = [content_type]
    # 从关键词提取 tag
    key_tag_map = {
        '酒店': '酒店', 'AHL': 'AHL', 'AI': 'AI', 'Agent': 'Agent',
        '博弈论': '博弈论', '群论': '群论', '审美': '审美',
        '安逸': '安逸', 'cron': 'cron', 'report': '报告',
        'B166ER': 'B166ER', 'Eric': 'Eric',
    }
    for kw in keywords[:5]:
        for key, tag in key_tag_map.items():
            if key.lower() in kw.lower() and tag not in tags:
                tags.append(tag)
    return ', '.join(tags[:5])


def update_moc(moc_name: str, new_note_path: str, note_title: str):
    """向 MOC 追加新笔记引用"""
    moc_path = VAULT / "emergence" / "hubs" / f"{moc_name}.md"
    if not moc_path.exists():
        return

    content = moc_path.read_text(encoding="utf-8")
    link = f"[[{new_note_path}|{note_title}]]"

    # 避免重复
    if link not in content:
        # 找到 "## 🔗 关联" 或 "## 🔗 关联 MOC" 前插入
        if "## 🔗 关联 MOC" in content:
            content = content.replace(
                "## 🔗 关联 MOC",
                f"- {link}\n\n## 🔗 关联 MOC"
            )
        elif "## 🔗 关联" in content:
            content = content.replace(
                "## 🔗 关联",
                f"- {link}\n\n## 🔗 关联"
            )
        elif "## 📂 核心笔记" in content:
            content = content.replace(
                "## 📂 核心笔记",
                f"## 📂 核心笔记\n\n- {link}"
            )
        moc_path.write_text(content, encoding="utf-8")


def push(title: str, content: str, content_type: str = 'inbox',
         tags: str = "", importance: str = 'normal',
         update_mocs: bool = True) -> dict:
    """
    核心 push 函数 — 可被 Python 代码调用

    Returns:
      {
        'success': True,
        'path': '10-我为你生成的/知识库/xxx.md',
        'full_path': 'D:\\...\\xxx.md',
        'related_notes': [...],
        'matched_mocs': [...],
        'frontmatter': {...}
      }
    """
    # 1. 确定目录
    target_dir_name = TYPE_DIR_MAP.get(content_type, TYPE_DIR_MAP['inbox'])
    target_dir = VAULT / target_dir_name
    target_dir.mkdir(parents=True, exist_ok=True)

    # 2. 生成文件名
    now = datetime.now()
    safe_title = re.sub(r'[\\/:*?"<>|]', '-', title)[:50]
    filename = f"{now.strftime('%Y-%m-%d')}-{safe_title}.md"
    filepath = target_dir / filename
    rel_path = f"{target_dir_name}/{filename}".replace('\\', '/')

    # 3. 提取关键词
    keywords = extract_keywords(f"# {title}\n\n{content}")

    # 4. 自动 determine tags
    if not tags:
        tags = determine_tags(keywords, content_type)

    # 5. 找关联笔记
    related = find_related_notes(keywords)

    # 6. 找 MOC
    matched_mocs = find_best_moc(keywords)

    # 7. 生成 wikilinks
    wikilinks = [f"[[{r['path']}|{r['name']}]]" for r in related[:8]]

    # 8. 生成 MOC references
    moc_refs = [f"[[emergence/hubs/{m}|{m}]]" for m in matched_mocs]

    # 9. 构建 frontmatter + body
    frontmatter = f"""---
author: b166er
audience: both
type: {content_type}
tags: [{tags}]
importance: {importance}
created: {now.isoformat()}
related: [{', '.join(r['name'] for r in related[:5]) if related else ''}]
mocs: [{', '.join(matched_mocs[:3]) if matched_mocs else ''}]
---

# {title}

> 自动推送 by push_to_vault.py · {now.strftime('%Y-%m-%d %H:%M')}
"""
    body = f"{frontmatter}\n{content}\n"

    # 10. 追加关联
    if wikilinks:
        body += f"\n## 🔗 关联笔记\n\n" + "\n".join(f"- {w}" for w in wikilinks) + "\n"

    if moc_refs:
        body += f"\n## 📂 所属 MOC\n\n" + "\n".join(f"- {r}" for r in moc_refs) + "\n"

    body += f"\n---\n*by B166ER push_to_vault.py · {now.strftime('%Y-%m-%d %H:%M')}*\n"

    # 11. 写入
    filepath.write_text(body, encoding="utf-8")

    # 12. 更新 MOC（可选）
    if update_mocs and matched_mocs:
        for moc in matched_mocs[:1]:  # 只更新排名第一的 MOC
            try:
                update_moc(moc, rel_path, title)
            except Exception as e:
                print(f"  MOC update warning: {e}", file=sys.stderr)

    return {
        'success': True,
        'path': rel_path,
        'full_path': str(filepath),
        'related_notes': related,
        'matched_mocs': matched_mocs,
        'keywords': keywords,
        'tags': tags,
        'file_size': filepath.stat().st_size,
    }


def main():
    parser = argparse.ArgumentParser(description="push_to_vault — 实时推送")
    parser.add_argument("--title", required=True, help="标题")
    parser.add_argument("--content", default="", help="内容")
    parser.add_argument("--content-file", help="从文件读取内容")
    parser.add_argument("--type", default="inbox", choices=list(TYPE_DIR_MAP.keys()), help="内容类型")
    parser.add_argument("--tags", default="", help="标签 (逗号分隔)")
    parser.add_argument("--importance", default="normal", choices=['normal', 'high', 'urgent'])
    parser.add_argument("--no-moc-update", action="store_true", help="不更新 MOC")
    parser.add_argument("--json", action="store_true", help="JSON 输出")

    args = parser.parse_args()

    # 读取内容
    content = args.content
    if args.content_file and args.content_file == '-':
        content = sys.stdin.read()
    elif args.content_file:
        content = Path(args.content_file).read_text(encoding="utf-8")

    if not content:
        print("ERROR: no content", file=sys.stderr)
        sys.exit(1)

    # 执行 push
    result = push(
        title=args.title,
        content=content,
        content_type=args.type,
        tags=args.tags,
        importance=args.importance,
        update_mocs=not args.no_moc_update,
    )

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"[OK] {result['path']} ({result['file_size']}b)")
        print(f"     MOC: {result['matched_mocs']}")
        print(f"     Related: {len(result['related_notes'])} notes")
        print(f"     Tags: {result['tags']}")


if __name__ == "__main__":
    main()
