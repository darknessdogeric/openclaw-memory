#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
build_link_graph.py — vault 关联性建立器

输入: obsidian-vault 全部 .md
输出:
  1. emergence/graph.jsonl (节点 + 边)
  2. emergence/graph-summary.md (图谱统计)
  3. 给关键笔记加 related: frontmatter

设计理念: vault = 节点群, 关联 = 群运算, MOC = 子群结构
"""
import os, re, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from collections import defaultdict, Counter
from datetime import datetime

VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")
EMERGENCE = VAULT / "emergence"
GRAPH_JSONL = EMERGENCE / "graph.jsonl"
GRAPH_SUMMARY = EMERGENCE / "graph-summary.md"

# ===== 1. 扫所有笔记 =====
def scan_vault():
    """扫 vault, 解析每篇笔记的元数据"""
    nodes = {}
    for f in VAULT.rglob("*.md"):
        # 包含 emergence/hubs/ (MOC 枢纽)
        if "emergence" in f.parts and "hubs" not in f.parts:
            continue
        if f.name == "RECOVERY-LOG.md":
            continue
        rel = f.relative_to(VAULT)
        try:
            content = f.read_text(encoding="utf-8")
        except Exception:
            continue

        # 解析 frontmatter
        fm = {}
        fm_match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
        if fm_match:
            fm_text = fm_match.group(1)
            body = fm_match.group(2)
            for line in fm_text.split('\n'):
                if ':' in line:
                    k, v = line.split(':', 1)
                    fm[k.strip()] = v.strip()
        else:
            body = content

        # 提取 [[双链]]
        wikilinks = re.findall(r'\[\[([^\]]+)\]\]', body)
        wikilinks = [w.split('|')[0].split('#')[0] for w in wikilinks]

        # 提取 # 标签
        tags_inline = re.findall(r'(?<!\w)#([\w/-]+)', body)

        # 提取 title (第一行 #)
        title_match = re.match(r'^#\s+(.+?)$', body, re.MULTILINE)
        title = title_match.group(1).strip() if title_match else f.stem

        # 关键词提取（粗略，4+ 字中文或 2+ 字符英文）
        cn_words = re.findall(r'[\u4e00-\u9fff]{4,}', body[:5000])
        en_words = re.findall(r'\b[A-Z][a-zA-Z]{2,}\b', body[:5000])

        nodes[str(rel).replace('\\', '/')] = {
            'path': str(rel).replace('\\', '/'),
            'name': f.stem,
            'title': title,
            'type': fm.get('type', 'leaf'),
            'author': fm.get('author', 'unknown'),
            'audience': fm.get('audience', 'both'),
            'tags': [t.strip() for t in fm.get('tags', '').strip('[]').split(',') if t.strip()],
            'tags_inline': list(set(tags_inline))[:10],
            'wikilinks': list(set(wikilinks)),
            'keywords_cn': [w for w, _ in Counter(cn_words).most_common(10)],
            'keywords_en': [w for w, _ in Counter(en_words).most_common(10)],
            'size': f.stat().st_size,
            'category': str(rel.parent) if rel.parent != Path('.') else 'root',
        }
    return nodes


# ===== 2. 主题分类 =====
THEME_PATTERNS = {
    'AHL 平台': ['AHL', 'ahl', '去中心化', '旅行平台', '双 Agent', '87 SKILL', 'CTO', '陈思序', '李源', '乐山', '锦江嘉州', '苏州酒管', '产品目录', '组织架构', '营销 Agent'],
    '安逸集团/D-day': ['安逸', '省旅投', '四川省旅游', '产业发展部', 'D-day', '党委会', '1234', '1244', '入职', '报到', '公示'],
    '酒店行业': ['酒店', 'OTA', '收益管理', 'PMS', 'ADR', 'OCC', 'RevPAR', '入住率', '客房', '前台', '餐饮', '客房', '客房部', '康养', '民宿'],
    'AI/Agent': ['AI', 'Agent', 'MCP', 'SKILL', 'LLM', '大模型', 'GPT', 'DeepSeek', 'Claude', '向量', 'embed', 'RAG'],
    '战略/方法论': ['战略', '博弈论', '群论', '审美', '信息论', '贝叶斯', '第一性', '奥卡姆', '元认知', '复盘', 'MOC'],
    '产品/营销': ['产品', '营销', '新媒体', '小红书', '抖音', '朋友圈', '流量', '私域', '供应链', '数据资产'],
    'B166ER 自身': ['B166ER', 'R13', 'R14', 'R15', 'R16', 'R17', 'R18', 'R19', 'R20', 'R 规则', 'self-improving'],
    'Eric 人格': ['张实', 'Eric', '人格', '音乐', '手风琴', '俄罗斯', '昭和', '维吾尔', 'Bach', '审美味道', '侧写'],
    '工具/系统': ['OpenClaw', 'cron', 'Obsidian', 'Vault', 'Python', 'PowerShell', 'scrap', 'Playwright', 'MCP'],
    '金融/经济': ['金融', '量化', '美股', 'A股', '美债', 'REITs', '美元', 'CNY', 'Fed', '央行', 'BIS'],
    '跨境/出海': ['跨境', '亚马逊', '阿联酋', '本奥米尔', '出海', '境外', 'Booking', 'Agoda'],
}


def classify_theme(node):
    """根据内容给节点打主题标签"""
    text_parts = [
        node.get('name', ''),
        node.get('title', ''),
        ' '.join(node.get('keywords_cn', [])),
        ' '.join(node.get('keywords_en', [])),
        ' '.join(node.get('wikilinks', [])),
        ' '.join(node.get('tags', [])),
    ]
    text = ' '.join(text_parts).lower()

    themes = []
    for theme, keywords in THEME_PATTERNS.items():
        for kw in keywords:
            if kw.lower() in text:
                themes.append(theme)
                break
    return themes or ['其他']


# ===== 3. 构建关联矩阵 =====
def build_links(nodes):
    """基于 wikilinks 解析关联"""
    edges = []
    for path, node in nodes.items():
        for link in node.get('wikilinks', []):
            # 尝试找匹配的笔记
            for target_path, target_node in nodes.items():
                if (link == target_node['name']
                    or link == target_node['title']
                    or link in target_path):
                    edges.append({
                        'source': path,
                        'target': target_path,
                        'type': 'wikilink',
                    })
                    break
    return edges


def build_tag_links(nodes):
    """基于 tag 聚合关联"""
    tag_groups = defaultdict(list)
    for path, node in nodes.items():
        for tag in node.get('tags', []):
            tag_groups[tag].append(path)
        for tag in node.get('tags_inline', []):
            tag_groups[tag].append(path)

    edges = []
    for tag, paths in tag_groups.items():
        if len(paths) > 1 and len(paths) < 50:  # 避免太大
            for i, p1 in enumerate(paths):
                for p2 in paths[i+1:]:
                    edges.append({
                        'source': p1,
                        'target': p2,
                        'type': f'tag:{tag}',
                    })
    return edges


# ===== 4. 输出 =====
def main():
    print("=" * 60)
    print("vault 关联性建立")
    print("=" * 60)

    # 1. 扫
    print("\n[1/5] 扫描 vault ...")
    nodes = scan_vault()
    print(f"  找到 {len(nodes)} 个节点")

    # 2. 主题分类
    print("\n[2/5] 主题分类 ...")
    for path, node in nodes.items():
        node['themes'] = classify_theme(node)
    theme_count = Counter()
    for n in nodes.values():
        for t in n['themes']:
            theme_count[t] += 1
    print("  主题分布:")
    for theme, count in theme_count.most_common():
        print(f"    {theme}: {count}")

    # 3. 构建关联
    print("\n[3/5] 构建关联边 ...")
    wikilink_edges = build_links(nodes)
    print(f"  wikilink 边: {len(wikilink_edges)}")
    tag_edges = build_tag_links(nodes)
    print(f"  tag 边: {len(tag_edges)}")
    all_edges = wikilink_edges + tag_edges

    # 4. 写 graph.jsonl
    print("\n[4/5] 写 graph.jsonl ...")
    EMERGENCE.mkdir(parents=True, exist_ok=True)
    with open(GRAPH_JSONL, 'w', encoding='utf-8') as f:
        for path, node in nodes.items():
            f.write(json.dumps({
                'node': path,
                'type': node['type'],
                'themes': node['themes'],
                'tags': node.get('tags', []),
                'wikilinks': node.get('wikilinks', []),
                'size': node['size'],
            }, ensure_ascii=False) + '\n')
        for edge in all_edges:
            f.write(json.dumps({
                'edge': [edge['source'], edge['target']],
                'type': edge['type'],
            }, ensure_ascii=False) + '\n')
    print(f"  [OK] {GRAPH_JSONL}")

    # 5. 写 graph-summary.md
    print("\n[5/5] 写 graph-summary.md ...")
    isolated = [p for p, n in nodes.items() if not n.get('wikilinks') and len(n.get('themes', [])) == 1]
    highly_connected = sorted(
        [(p, len([e for e in all_edges if e['source'] == p or e['target'] == p]))
         for p in nodes.keys()],
        key=lambda x: -x[1]
    )[:20]

    summary = f"""---
author: b166er-emergence
audience: both
type: graph-summary
created: {datetime.now().isoformat()}
---

# 🌐 vault 知识图谱 · 总览

> 自动构建 by build_link_graph.py
> 节点 = 笔记, 边 = 关联 (wikilink + tag)
> **群论视角**: vault = 节点群, MOC = 子群结构, 涌现 = 网络效应

## 📊 统计

| 指标 | 数值 |
|------|------|
| 节点数 | {len(nodes)} |
| wikilink 边 | {len(wikilink_edges)} |
| tag 边 | {len(tag_edges)} |
| 总边数 | {len(all_edges)} |
| 孤岛节点 | {len(isolated)} ({len(isolated)/len(nodes)*100:.1f}%) |
| 高连接节点 (top 20) | 见下 |

## 🎨 主题分布

"""
    for theme, count in theme_count.most_common():
        summary += f"- **{theme}**: {count} 节点\n"

    summary += f"""

## 🏆 高连接节点 (Top 20)

| 排名 | 节点 | 关联数 |
|------|------|--------|
"""
    for i, (p, c) in enumerate(highly_connected, 1):
        name = Path(p).name[:50]
        summary += f"| {i} | {name} | {c} |\n"

    summary += f"""

## 🏝️ 孤岛节点 (无 wikilink + 单主题): {len(isolated)}

孤岛意味着：没有内链、没有 tag 聚合。
**重点突破对象**——给这些节点加 related: 字段。

"""
    for p in isolated[:30]:
        name = Path(p).name
        themes = nodes[p].get('themes', [])
        summary += f"- `{p}` ({themes})\n"
    if len(isolated) > 30:
        summary += f"- ... 还有 {len(isolated) - 30} 个\n"

    summary += f"""

## 🔗 关联类型分布

| 类型 | 边数 |
|------|------|
| wikilink (双链) | {len(wikilink_edges)} |
| tag (标签聚合) | {len(tag_edges)} |

## 💡 涌现路径建议

1. **写 6-8 个 MOC 主题枢纽**（按主题分布）→ 立即把孤岛节点桥接
2. **关键节点加 related:** 字段 → 让 MOC 节点知道它的子节点
3. **每周跑一次 build_link_graph.py** → 持续涌现
4. **Obsidian graph view** → 可视化涌现层

## 🔗 相关

- [[INDEX|emergence/INDEX]]
- [[../00-Workspace-核心/PROJECT-TRACKING|项目矩阵]]
- [[../00-Dashboard|Dashboard]]

---

*by B166ER build_link_graph.py · {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
    GRAPH_SUMMARY.write_text(summary, encoding="utf-8")
    print(f"  [OK] {GRAPH_SUMMARY}")

    print("\n" + "=" * 60)
    print("完成")
    print("=" * 60)
    print(f"  节点: {len(nodes)}")
    print(f"  边: {len(all_edges)}")
    print(f"  孤岛: {len(isolated)} ({len(isolated)/len(nodes)*100:.1f}%)")
    print(f"  graph.jsonl: {GRAPH_JSONL}")
    print(f"  graph-summary.md: {GRAPH_SUMMARY}")


if __name__ == "__main__":
    main()
