#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
vault_search.py — MOC 优先网状检索

设计理念:
  不是 flat keyword search，而是:
  1. 先找匹配的 MOC 主题枢纽
  2. 读 MOC → 获取所有关联笔记清单
  3. 沿 [[wikilink]] 链遍历相关笔记
  4. 返回结构化结果 (MOC 上下文 + 笔记内容)

对比 memory_search:
  memory_search: 扁平语义搜索 → 返回碎片片段
  vault_search:    MOC 优先 → 返回结构化+网状内容

用法:
  python vault_search.py "AHL 技术架构"
  python vault_search.py --json "五一复盘 酒店行业"
  from vault_search import smart_search
  results = smart_search("AHL 酒店智能升级")

作者: B166ER · 2026-07-12
"""
import sys, io, json, re, argparse
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from collections import Counter

VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")
HUB_DIR = VAULT / "emergence" / "hubs"

# 快速索引: MOC → 标签词
MOC_INDEX = {
    'AHL 平台 MOC': ['AHL', 'ahl', '去中心化', '旅行平台', 'Agent', 'SKILL', '乐山', '锦江', '苏州酒管', '数字员工', '酒店智能升级'],
    '酒店行业 MOC': ['酒店', 'OTA', 'PMS', 'ADR', 'OCC', 'RevPAR', '客房', '前台', '餐饮', 'SOP', '维景', '收益管理', '服务', '品质', '清洁', '安保', '工程', '房务'],
    'AI-Agent MOC': ['AI', 'Agent', 'LLM', '大模型', 'GPT', 'DeepSeek', 'Claude', 'MCP', '向量', 'RAG', 'embedding', 'SKILL', '自动化', '智能'],
    '战略-方法论 MOC': ['战略', '博弈论', '群论', '审美', '信息论', '贝叶斯', '第一性', '奥卡姆', '元认知', '复盘', '预测', '方法论', '决策'],
    '安逸集团-D-day MOC': ['安逸', '省旅投', '产业发展部', 'D-day', '党委会', '公示', '入职', '1244', '350亿', '阿联酋', '本奥米尔', '部长'],
    'Eric 人格-审美 MOC': ['张实', 'Eric', '人格', '音乐', '手风琴', '俄罗斯', '昭和', '维吾尔', 'Bach', '审美', '品味', '侧写'],
    '工具-系统 MOC': ['OpenClaw', 'cron', 'Obsidian', 'Vault', 'Python', 'PowerShell', 'scrap', 'Playwright', '工具', 'MCP', 'Tavily'],
    'B166ER 知识库 MOC': ['B166ER', 'R 规则', 'self-improving', '能力图谱', '知识库', '技能'],
    '跨境-出海 MOC': ['跨境', '亚马逊', '阿联酋', '本奥米尔', '出海', '境外', 'Booking', 'Agoda', 'Expedia', '海外'],
}


def find_matching_mocs(query: str, top_n: int = 3) -> list:
    """匹配 MOC"""
    scores = {}
    ql = query.lower()
    for moc_name, keywords in MOC_INDEX.items():
        score = sum(1 for kw in keywords if kw.lower() in ql)
        if score > 0:
            scores[moc_name] = score
    return sorted(scores, key=scores.get, reverse=True)[:top_n]


def read_moc_links(moc_name: str) -> list:
    """读 MOC 笔记，提取所有 [[wikilinks]]"""
    moc_path = HUB_DIR / f"{moc_name}.md"
    if not moc_path.exists():
        return []

    content = moc_path.read_text(encoding="utf-8")
    links = re.findall(r'\[\[([^\]]+)\]\]', content)
    # 解析: [[path|label]] or [[path#section]]
    parsed = []
    for link in links:
        path = link.split('|')[0].split('#')[0].strip()
        parsed.append({
            'raw': link,
            'path': path,
            'name': Path(path).name,
        })
    return parsed


def find_note_by_name(name: str) -> Path:
    """根据名称找 vault 中的实际文件"""
    # 先按精确匹配
    for f in VAULT.rglob("*.md"):
        if f.stem == name:
            return f
    # 模糊匹配
    for f in VAULT.rglob("*.md"):
        if name.lower() in f.stem.lower():
            return f
    return None


def read_note(path: Path, max_chars: int = 3000) -> dict:
    """读笔记内容 + frontmatter"""
    if not path or not path.exists():
        return None

    content = path.read_text(encoding="utf-8")
    fm = {}
    fm_match = re.match(r'^---\n(.*?)\n---\n(.*)$', content, re.DOTALL)
    if fm_match:
        for line in fm_match.group(1).split('\n'):
            if ':' in line:
                k, v = line.split(':', 1)
                fm[k.strip()] = v.strip()
        body = fm_match.group(2)[:max_chars]
    else:
        body = content[:max_chars]

    return {
        'path': str(path.relative_to(VAULT)).replace('\\', '/'),
        'name': path.stem,
        'frontmatter': fm,
        'body_preview': body[:500],
        'size': path.stat().st_size,
        'tags': [t.strip() for t in fm.get('tags', '').strip('[]').split(',') if t.strip()],
        'type': fm.get('type', 'unknown'),
    }


def keyword_search(query: str, max_results: int = 15) -> list:
    """fallback: 关键词搜索 vault（不扫外部接入 50/03 大型目录）"""
    ql = query.lower()
    results = []

    for f in VAULT.rglob("*.md"):
        rel = str(f.relative_to(VAULT))
        if any(x in rel for x in ['50-外部接入/03-维景', '.obsidian', 'emergence/graph.jsonl']):
            continue

        try:
            content = f.read_text(encoding="utf-8")[:5000]
        except Exception:
            continue

        # 评分
        score = 0
        words = re.findall(r'[\u4e00-\u9fff]+|[a-zA-Z]+', ql)
        for w in words:
            score += content.lower().count(w.lower())
        if score > 0:
            results.append({
                'path': rel,
                'name': f.stem,
                'score': score,
                'size': f.stat().st_size,
            })

    results.sort(key=lambda x: -x['score'])
    return results[:max_results]


def smart_search(query: str, max_results: int = 20) -> dict:
    """
    核心检索函数 — 可被 Python 代码调用

    Returns:
      {
        'query': str,
        'mocs': [...],           # 匹配的 MOC
        'moc_notes': [...],      # MOC 关联的笔记
        'keyword_results': [...], # 关键词搜索结果
        'top_notes': [...],      # 综合排名 top
      }
    """
    result = {
        'query': query,
        'mocs': [],
        'moc_notes': [],
        'keyword_results': [],
        'top_notes': [],
    }

    # 1. MOC 匹配
    mocs = find_matching_mocs(query)
    result['mocs'] = mocs

    # 2. 从 MOC 展开
    moc_notes_set = set()
    for moc in mocs[:2]:
        links = read_moc_links(moc)
        for link in links:
            note_path = find_note_by_name(link['name'])
            if note_path:
                note = read_note(note_path)
                if note:
                    key = note['path']
                    if key not in moc_notes_set:
                        moc_notes_set.add(key)
                        result['moc_notes'].append(note)

    # 3. 关键词搜索 fallback
    result['keyword_results'] = keyword_search(query, max_results=15)

    # 4. 综合排序: MOC 笔记优先
    moc_paths = {n['path'] for n in result['moc_notes']}
    top = list(result['moc_notes'])

    # MOC 笔记不够 → 补关键词结果
    for kw in result['keyword_results']:
        if kw['path'] not in moc_paths:
            note = read_note(find_note_by_name(kw['name']))
            if note:
                top.append(note)
                moc_paths.add(kw['path'])
        if len(top) >= max_results:
            break

    result['top_notes'] = top
    result['total_found'] = len(top)

    return result


def search_for_agent(query: str) -> str:
    """
    给 B166ER 用的高层接口: 返回 Markdown 格式的检索结果
    可直接作为对话上下文注入
    """
    r = smart_search(query, max_results=10)

    md = f"## vault 检索: {query}\n\n"

    if r['mocs']:
        md += f"### 匹配的 MOC: {', '.join(r['mocs'])}\n\n"

    if r['top_notes']:
        md += f"### Top {len(r['top_notes'])} 相关笔记\n\n"
        for i, note in enumerate(r['top_notes'][:8], 1):
            md += f"**{i}. {note['name']}** ({note['type']})\n"
            md += f"   📄 `{note['path']}` ({note['size']/1024:.1f}KB)\n"
            preview = note['body_preview'][:200].replace('\n', ' ')
            md += f"   📝 {preview}...\n\n"
    else:
        md += "> 无匹配结果\n"

    return md


def main():
    parser = argparse.ArgumentParser(description="vault_search — MOC 优先检索")
    parser.add_argument("query", help="搜索查询")
    parser.add_argument("--json", action="store_true", help="JSON 输出")
    parser.add_argument("--max", type=int, default=15, help="最大结果数")
    parser.add_argument("--for-agent", action="store_true", help="Markdown 格式 (给 B166ER)")

    args = parser.parse_args()

    if args.for_agent:
        print(search_for_agent(args.query))
    else:
        r = smart_search(args.query, max_results=args.max)
        if args.json:
            print(json.dumps(r, ensure_ascii=False, indent=2))
        else:
            print(f"MOCs: {r['mocs']}")
            print(f"MOC notes: {len(r['moc_notes'])}")
            print(f"Keyword: {len(r['keyword_results'])}")
            print(f"Top: {len(r['top_notes'])}")
            for n in r['top_notes'][:5]:
                print(f"  {n['name']} ({n['type']})")


if __name__ == "__main__":
    main()
