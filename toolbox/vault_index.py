#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
vault_index.py — Obsidian vault 预计算索引

为什么需要这个工具?
  R13 (重IO隔离规则): 任何涉及 obsidian-vault/ 大体量操作的 IO, 必须隔离到子会话.
  本工具把"扫描全库"从"每次调用时执行"提升为"一次性预计算 + 后续查询", 让主会话
  和子会话都达到毫秒级响应.

设计哲学:
  - 一次扫描, 持久化为 JSON
  - 子会话负责 build/update (重 IO 隔离)
  - 主会话只查 JSON (轻 IO)
  - 自动增量更新: mtime 变化才重建

索引结构:
  {
    "version": "1.0",
    "built_at": "2026-07-13T12:25:00+08:00",
    "vault_root": "...",
    "total_files": 1762,
    "files": {
      "相对路径": {
        "path": ...,
        "title": ...,
        "stem": ...,
        "size": int,
        "mtime": float,
        "keywords": [str, ...],
        "tags": [str, ...],
        "frontmatter": {...},
        "type": "inbox|k|cron-push|diary|hub|external|...",
        "moc_matches": [moc_name, ...],
        "preview": "前 300 字",
        "wikilinks": [stem, ...]
      }
    }
  }

用法:
  python vault_index.py build          # 全量重建
  python vault_index.py update         # 增量更新 (基于 mtime)
  python vault_index.py query "关键词"   # 关键词查询
  python vault_index.py find-moc "AHL 平台 MOC"  # 找某 MOC 下所有笔记
  python vault_index.py stats          # 索引健康度
  python vault_index.py path "0-快速捕捉"  # 按文件名查
"""
import sys, io, json, re, argparse, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from datetime import datetime

VAULT = Path(r"D:\B166ER-OpenClaw\workspace\obsidian-vault")
INDEX_PATH = Path(r"D:\B166ER-OpenClaw\workspace\toolbox\.vault_index.json")

# 与 vault_search.py 保持一致
MOC_INDEX = {
    'AHL 平台 MOC': ['AHL', 'ahl', '去中心化', '旅行平台', 'Agent', 'SKILL', '乐山', '锦江', '苏州酒管', '数字员工', '酒店智能升级'],
    '酒店行业 MOC': ['酒店', 'OTA', 'PMS', 'ADR', 'OCC', 'RevPAR', '客房', '前台', '餐饮', 'SOP', '维景', '收益管理', '服务', '品质', '清洁', '安保', '工程', '房务'],
    'AI-Agent MOC': ['AI', 'Agent', 'LLM', '大模型', 'GPT', 'DeepSeek', 'Claude', 'MCP', '向量', 'RAG', 'embedding', 'SKILL', '自动化', '智能'],
    '战略-方法论 MOC': ['战略', '博弈论', '群论', '审美', '信息论', '贝叶斯', '第一性', '奥卡姆', '元认知', '复盘', '预测', '方法论', '决策'],
    '安逸集团-D-day MOC': ['安逸', '省旅投', '产业发展部', 'D-day', '党委会', '公示', '入职', '1244', '部长'],  # [R66 v2026-09-03] 删除'350亿','阿联酋','本奥米尔'(L1/L2虚构)
    'Eric 人格-审美 MOC': ['张实', 'Eric', '人格', '音乐', '手风琴', '俄罗斯', '昭和', '维吾尔', 'Bach', '审美', '品味', '侧写'],
    '工具-系统 MOC': ['OpenClaw', 'cron', 'Obsidian', 'Vault', 'Python', 'PowerShell', 'scrap', 'Playwright', '工具', 'MCP', 'Tavily'],
    'B166ER 知识库 MOC': ['B166ER', 'R 规则', 'self-improving', '能力图谱', '知识库', '技能'],
    '跨境-出海 MOC': ['跨境', '亚马逊', '出海', '境外', 'Booking', 'Agoda', 'Expedia', '海外'],  # [R66 v2026-09-03] 删除'阿联酋','本奥米尔'(L1虚构)
}

# 文件夹 → 类型映射 (推断 type)
TYPE_BY_DIR = {
    '00-Inbox-待整理/cron-push': 'cron-push',
    '00-Inbox-待整理': 'inbox',
    '01-日记': 'diary',
    '10-我为你生成的': 'kb-generated',
    '20-我们共同维护的': 'kb-joint',
    '30-你写给我的': 'eric-note',
    '40-工具与模板': 'template',
    '50-外部接入': 'external',
    'emergence/hubs': 'moc-hub',
    'emergence/daily': 'emergence-daily',
}

# 排除路径 (不索引)
EXCLUDE_PATTERNS = [
    '.obsidian',
    '.trash',
    '__pycache__',
]


def infer_type(rel_path: str) -> str:
    """根据相对路径推断 type"""
    rel = rel_path.replace('\\', '/')
    for dir_prefix, type_name in TYPE_BY_DIR.items():
        if rel.startswith(dir_prefix + '/') or rel == dir_prefix:
            return type_name
    return 'other'


def parse_frontmatter(text: str) -> tuple:
    """解析 frontmatter, 返回 (fm_dict, body)"""
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n(.*)$', text, re.DOTALL)
    if not fm_match:
        return {}, text

    fm = {}
    for line in fm_match.group(1).split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")

    return fm, fm_match.group(2)


def extract_title(text: str, fm: dict, stem: str) -> str:
    """从 frontmatter / 第一行 / 文件名 提取标题"""
    if 'title' in fm:
        return fm['title']
    if 'name' in fm:
        return fm['name']

    # 从正文找第一个 # 标题
    for line in text.split('\n')[:30]:
        m = re.match(r'^#\s+(.+)$', line.strip())
        if m:
            return m.group(1).strip()

    return stem


def extract_keywords(text: str, top_n: int = 30) -> list:
    """从正文提取关键词 (中文 2-12 字 + 英文 3+ 字母)"""
    cn_kws = re.findall(r'[\u4e00-\u9fff]{2,12}', text)
    en_kws = re.findall(r'\b[A-Za-z]{3,}\b', text)

    # 停用词
    STOPWORDS_CN = {'的', '了', '是', '在', '和', '与', '或', '及', '等', '为', '以', '从', '到', '把', '被',
                    '也', '都', '就', '还', '又', '再', '已', '已', '曾', '将', '可', '能', '会', '要',
                    '这', '那', '此', '该', '其', '他', '她', '它', '我', '你', '您', '我们', '你们',
                    '什么', '怎么', '为什么', '如何', '一个', '一些', '没有', '可以', '应该', '可能',
                    '由于', '因为', '所以', '但是', '然而', '虽然', '即使', '如果', '那么', '因此'}
    STOPWORDS_EN = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'her', 'was', 'one',
                    'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how', 'man', 'new', 'now', 'old',
                    'see', 'two', 'way', 'who', 'boy', 'did', 'its', 'let', 'put', 'say', 'she', 'too',
                    'use', 'this', 'that', 'with', 'have', 'from', 'they', 'their', 'there', 'what',
                    'when', 'where', 'which', 'will', 'would', 'about', 'could', 'should'}

    counter = {}
    for kw in cn_kws:
        if kw not in STOPWORDS_CN and len(kw) >= 2:
            counter[kw] = counter.get(kw, 0) + 1
    for kw in en_kws:
        kw_lower = kw.lower()
        if kw_lower not in STOPWORDS_EN:
            counter[kw] = counter.get(kw, 0) + 1

    return [k for k, _ in sorted(counter.items(), key=lambda x: -x[1])[:top_n]]


def extract_wikilinks(text: str) -> list:
    """提取 [[wikilinks]] 的目标 stem"""
    links = re.findall(r'\[\[([^\]|#]+)', text)
    stems = []
    for link in links:
        # 处理 path|label 和 path#section
        target = link.strip().split('|')[0].split('#')[0].strip()
        if target:
            stem = Path(target).stem if '/' in target or '\\' in target else target
            stems.append(stem)
    return list(set(stems))


def match_moc(keywords: list, text_lower: str) -> list:
    """根据关键词和文本匹配 MOC"""
    matched = []
    kw_set = set(k.lower() for k in keywords)
    for moc_name, moc_kws in MOC_INDEX.items():
        for moc_kw in moc_kws:
            if moc_kw.lower() in kw_set or moc_kw.lower() in text_lower:
                matched.append(moc_name)
                break
    return matched


def should_skip(path: Path) -> bool:
    """是否跳过该文件"""
    rel = str(path).replace('\\', '/')
    for pattern in EXCLUDE_PATTERNS:
        if pattern in rel:
            return True
    return False


def build_index(force: bool = False) -> dict:
    """全量构建索引"""
    start_time = time.time()

    if not force and INDEX_PATH.exists():
        try:
            existing = json.loads(INDEX_PATH.read_text(encoding='utf-8'))
            if existing.get('version') == '1.0':
                # 检查 mtime, 如果 vault 没有新文件, 直接返回
                vault_mtime = VAULT.stat().st_mtime
                if existing.get('vault_mtime', 0) >= vault_mtime:
                    print(f"[skip] 索引已是最新 ({existing.get('built_at')})")
                    return existing
        except Exception:
            pass

    print(f"[build] 扫描 vault: {VAULT}")
    files = {}
    total_size = 0

    for f in VAULT.rglob('*.md'):
        if should_skip(f):
            continue

        try:
            text = f.read_text(encoding='utf-8')
        except Exception:
            continue

        fm, body = parse_frontmatter(text)
        rel = str(f.relative_to(VAULT)).replace('\\', '/')
        stem = f.stem

        title = extract_title(body, fm, stem)
        keywords = extract_keywords(text[:10000])  # 只取前 10K 字符
        wikilinks = extract_wikilinks(text)
        type_name = infer_type(rel)
        text_lower = text[:5000].lower()
        moc_matches = match_moc(keywords, text_lower)

        size = f.stat().st_size
        total_size += size

        # tags from frontmatter
        tags = []
        if 'tags' in fm:
            tags = [t.strip() for t in fm['tags'].strip('[]').split(',') if t.strip()]

        # preview (前 300 字, 去掉 markdown 标记)
        preview_raw = body.strip()[:500]
        preview = re.sub(r'[#*`>\[\]\(\)]', '', preview_raw)[:300]

        files[rel] = {
            'path': rel,
            'title': title,
            'stem': stem,
            'size': size,
            'mtime': f.stat().st_mtime,
            'keywords': keywords,
            'tags': tags,
            'frontmatter': fm,
            'type': type_name,
            'moc_matches': moc_matches,
            'preview': preview,
            'wikilinks': wikilinks[:20],  # 限制数量
        }

    index = {
        'version': '1.0',
        'built_at': datetime.now().isoformat(),
        'vault_root': str(VAULT),
        'vault_mtime': VAULT.stat().st_mtime,
        'total_files': len(files),
        'total_size_mb': round(total_size / 1024 / 1024, 2),
        'files': files,
    }

    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    INDEX_PATH.write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding='utf-8')

    elapsed = time.time() - start_time
    print(f"[build] 完成: {len(files)} 文件 / {index['total_size_mb']} MB / {elapsed:.1f}s")
    print(f"[build] 索引路径: {INDEX_PATH}")

    return index


def update_index() -> dict:
    """增量更新 (基于 mtime)"""
    if not INDEX_PATH.exists():
        return build_index(force=True)

    index = json.loads(INDEX_PATH.read_text(encoding='utf-8'))
    files = index.get('files', {})

    updated = 0
    added = 0
    removed = 0

    # 1. 检查现有文件的 mtime
    for rel, meta in list(files.items()):
        full_path = VAULT / rel
        if not full_path.exists():
            del files[rel]
            removed += 1
            continue

        try:
            current_mtime = full_path.stat().st_mtime
        except Exception:
            continue

        if current_mtime > meta.get('mtime', 0):
            # 需要更新
            try:
                text = full_path.read_text(encoding='utf-8')
                fm, body = parse_frontmatter(text)
                keywords = extract_keywords(text[:10000])
                wikilinks = extract_wikilinks(text)
                type_name = infer_type(rel)
                text_lower = text[:5000].lower()
                moc_matches = match_moc(keywords, text_lower)
                tags = []
                if 'tags' in fm:
                    tags = [t.strip() for t in fm['tags'].strip('[]').split(',') if t.strip()]
                preview = re.sub(r'[#*`>\[\]\(\)]', '', body.strip()[:500])[:300]

                files[rel] = {
                    'path': rel,
                    'title': extract_title(body, fm, full_path.stem),
                    'stem': full_path.stem,
                    'size': full_path.stat().st_size,
                    'mtime': current_mtime,
                    'keywords': keywords,
                    'tags': tags,
                    'frontmatter': fm,
                    'type': type_name,
                    'moc_matches': moc_matches,
                    'preview': preview,
                    'wikilinks': wikilinks[:20],
                }
                updated += 1
            except Exception:
                pass

    # 2. 扫描 vault 中新增的文件
    for f in VAULT.rglob('*.md'):
        if should_skip(f):
            continue
        rel = str(f.relative_to(VAULT)).replace('\\', '/')
        if rel not in files:
            # 新增文件 → 加入索引
            try:
                text = f.read_text(encoding='utf-8')
                fm, body = parse_frontmatter(text)
                keywords = extract_keywords(text[:10000])
                wikilinks = extract_wikilinks(text)
                type_name = infer_type(rel)
                text_lower = text[:5000].lower()
                moc_matches = match_moc(keywords, text_lower)
                tags = []
                if 'tags' in fm:
                    tags = [t.strip() for t in fm['tags'].strip('[]').split(',') if t.strip()]
                preview = re.sub(r'[#*`>\[\]\(\)]', '', body.strip()[:500])[:300]

                files[rel] = {
                    'path': rel,
                    'title': extract_title(body, fm, f.stem),
                    'stem': f.stem,
                    'size': f.stat().st_size,
                    'mtime': f.stat().st_mtime,
                    'keywords': keywords,
                    'tags': tags,
                    'frontmatter': fm,
                    'type': type_name,
                    'moc_matches': moc_matches,
                    'preview': preview,
                    'wikilinks': wikilinks[:20],
                }
                added += 1
            except Exception:
                pass

    index['built_at'] = datetime.now().isoformat()
    index['vault_mtime'] = VAULT.stat().st_mtime
    index['total_files'] = len(files)
    index['total_size_mb'] = round(sum(m['size'] for m in files.values()) / 1024 / 1024, 2)

    INDEX_PATH.write_text(json.dumps(index, ensure_ascii=False, indent=1), encoding='utf-8')

    print(f"[update] +{added} 新增 / ~{updated} 更新 / -{removed} 删除")
    print(f"[update] 总计: {index['total_files']} 文件 / {index['total_size_mb']} MB")
    return index


def query_index(query: str, top_n: int = 15, file_type: str = None) -> list:
    """关键词查询"""
    if not INDEX_PATH.exists():
        build_index(force=True)

    index = json.loads(INDEX_PATH.read_text(encoding='utf-8'))
    files = index.get('files', {})

    # 分词: 中文 2+ 字 / 英文 3+ 字母
    cn_words = re.findall(r'[\u4e00-\u9fff]{2,}', query)
    en_words = re.findall(r'\b[A-Za-z]{3,}\b', query)
    query_words = cn_words + en_words
    query_lower = query.lower()

    if not query_words:
        return []

    results = []
    for rel, meta in files.items():
        if file_type and meta.get('type') != file_type:
            continue

        score = 0
        # 标题命中 +5
        title_lower = meta.get('title', '').lower()
        for w in query_words:
            if w.lower() in title_lower:
                score += 5

        # 关键词命中 +3
        kw_set = set(k.lower() for k in meta.get('keywords', []))
        for w in query_words:
            if w.lower() in kw_set:
                score += 3

        # tags 命中 +3
        tag_set = set(t.lower() for t in meta.get('tags', []))
        for w in query_words:
            if w.lower() in tag_set:
                score += 3

        # wikilinks 命中 +2
        for w in query_words:
            if any(w.lower() in link.lower() for link in meta.get('wikilinks', [])):
                score += 2

        # MOC 命中 +2
        for w in query_words:
            if any(w.lower() in moc.lower() for moc in meta.get('moc_matches', [])):
                score += 2

        # preview 命中 +1
        preview_lower = meta.get('preview', '').lower()
        for w in query_words:
            if w.lower() in preview_lower:
                score += 1

        if score > 0:
            results.append({
                'path': rel,
                'title': meta.get('title', ''),
                'score': score,
                'type': meta.get('type', 'unknown'),
                'moc_matches': meta.get('moc_matches', []),
                'size_kb': round(meta.get('size', 0) / 1024, 1),
            })

    results.sort(key=lambda x: -x['score'])
    return results[:top_n]


def find_by_moc(moc_name: str) -> list:
    """找某 MOC 下所有笔记"""
    if not INDEX_PATH.exists():
        build_index(force=True)

    index = json.loads(INDEX_PATH.read_text(encoding='utf-8'))
    files = index.get('files', {})

    results = []
    for rel, meta in files.items():
        if moc_name in meta.get('moc_matches', []):
            results.append({
                'path': rel,
                'title': meta.get('title', ''),
                'type': meta.get('type', 'unknown'),
                'size_kb': round(meta.get('size', 0) / 1024, 1),
            })

    return results


def find_by_stem(stem: str) -> dict:
    """按文件名查"""
    if not INDEX_PATH.exists():
        build_index(force=True)

    index = json.loads(INDEX_PATH.read_text(encoding='utf-8'))
    files = index.get('files', {})

    for rel, meta in files.items():
        if meta.get('stem') == stem or stem.lower() in meta.get('stem', '').lower():
            return meta

    return None


def show_stats() -> None:
    """显示索引健康度"""
    if not INDEX_PATH.exists():
        print("[stats] 索引不存在, 请先 build")
        return

    index = json.loads(INDEX_PATH.read_text(encoding='utf-8'))
    files = index.get('files', {})

    # 按 type 统计
    type_counter = {}
    for meta in files.values():
        t = meta.get('type', 'unknown')
        type_counter[t] = type_counter.get(t, 0) + 1

    # MOC 分布
    moc_counter = {}
    for meta in files.values():
        for moc in meta.get('moc_matches', []):
            moc_counter[moc] = moc_counter.get(moc, 0) + 1

    print("=" * 60)
    print(f"Vault 索引健康度")
    print("=" * 60)
    print(f"  索引版本: {index.get('version')}")
    print(f"  构建时间: {index.get('built_at')}")
    print(f"  Vault 路径: {index.get('vault_root')}")
    print(f"  总文件数: {index.get('total_files')}")
    print(f"  总大小: {index.get('total_size_mb')} MB")
    print()
    print("  按 type 分布:")
    for t, n in sorted(type_counter.items(), key=lambda x: -x[1]):
        print(f"    {t}: {n}")
    print()
    print("  按 MOC 分布 (top 10):")
    for m, n in sorted(moc_counter.items(), key=lambda x: -x[1])[:10]:
        print(f"    {m}: {n}")
    print()
    print(f"  索引 JSON 大小: {INDEX_PATH.stat().st_size / 1024 / 1024:.2f} MB")


def main():
    parser = argparse.ArgumentParser(description='vault_index — Obsidian vault 预计算索引')
    sub = parser.add_subparsers(dest='cmd', required=True)

    p_build = sub.add_parser('build', help='全量构建索引')
    p_build.add_argument('--force', action='store_true', help='强制重建')

    p_update = sub.add_parser('update', help='增量更新 (基于 mtime)')

    p_query = sub.add_parser('query', help='关键词查询')
    p_query.add_argument('query', help='查询关键词')
    p_query.add_argument('--top', type=int, default=15, help='返回 top N')
    p_query.add_argument('--type', help='按 type 过滤 (e.g. cron-push, kb-generated)')
    p_query.add_argument('--json', action='store_true', help='JSON 输出')

    p_moc = sub.add_parser('find-moc', help='找某 MOC 下所有笔记')
    p_moc.add_argument('moc_name', help='MOC 名称 (e.g. "AHL 平台 MOC")')

    p_path = sub.add_parser('path', help='按文件名查')
    p_path.add_argument('stem', help='文件名或部分名')

    p_stats = sub.add_parser('stats', help='索引健康度')

    args = parser.parse_args()

    if args.cmd == 'build':
        build_index(force=args.force)
    elif args.cmd == 'update':
        update_index()
    elif args.cmd == 'query':
        results = query_index(args.query, args.top, args.type)
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            print(f"Query: {args.query} | Results: {len(results)}")
            for i, r in enumerate(results, 1):
                mocs = ', '.join(r['moc_matches'][:2]) if r['moc_matches'] else '-'
                print(f"  [{i}] {r['title'][:50]:50s} | {r['type']:15s} | score={r['score']:2d} | {r['path']}")
                if r['moc_matches']:
                    print(f"      MOC: {mocs}")
    elif args.cmd == 'find-moc':
        results = find_by_moc(args.moc_name)
        print(f"MOC: {args.moc_name} | Files: {len(results)}")
        for r in results[:20]:
            print(f"  {r['path']} ({r['size_kb']}KB, {r['type']})")
    elif args.cmd == 'path':
        meta = find_by_stem(args.stem)
        if meta:
            print(json.dumps(meta, ensure_ascii=False, indent=2))
        else:
            print(f"未找到: {args.stem}")
    elif args.cmd == 'stats':
        show_stats()


if __name__ == '__main__':
    sys.exit(main())