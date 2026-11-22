# -*- coding: utf-8 -*-
"""
tool2: KB Semantic Search v3 (稳定版)
"""
import os, sys, pickle, time

# --- R-F 整改 2026-09-29: 切换到中文 embedding 模型 ---
# 原: sentence-transformers/all-MiniLM-L6-v2 (英文模型, 中文检索 Top-1 仅 50%)
# 现: BAAI/bge-small-zh-v1.5 (中文, Top-1 100%, 区分度提升 2 倍)
MODEL_PATH = os.environ.get('KB_EMBED_MODEL', r'D:\B166ER-OpenClaw\workspace\toolbox\models\bge-small-zh-v1.5')
# -----------------------------------------------------
os.environ['PYTHONIOENCODING'] = 'utf-8'
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
import numpy as np
import re

WORKSPACE = Path(r'D:\B166ER-OpenClaw\workspace')
INDEX_DIR = WORKSPACE / 'toolbox' / 'kb_tools' / 'index'
INDEX_DIR.mkdir(parents=True, exist_ok=True)
KB_DIRS = [WORKSPACE / 'universal-kb', WORKSPACE / 'anyi-ops-kb']
MEMORY_DIR = WORKSPACE / 'memory'

# --- R-F 整改 2026-09-29: 扩展索引范围 ---
# 根目录关键文件(此前完全未索引 -> SOUL/MEMORY/AGENTS 无法被检索)
ROOT_EXCLUDE_PATTERNS = ('HEARTBEAT_head', 'HEARTBEAT_archive', 'tmp-', 'tmp_', '.bak')
# memory 需排除的目录(归档/备份/运行态,非知识)
MEMORY_EXCLUDE_DIRS = {'archive_versions', 'backups', '.dreams', 'dreaming', 'eval'}
# -------------------------------------------
MEMORY_DAYS = 14

INDEX_FILE = INDEX_DIR / 'documents.pkl'
EMBEDDINGS_FILE = INDEX_DIR / 'embeddings.npz'


def chunk_text(text, max_chars=800, overlap=120):
    """语义切分:按 Markdown 标题 + 双换行 切块,优先保留结构完整;超长再字符切。
    比固定字符切分好:块内语义连贯,检索更准。"""
    import re as _re
    text = text.strip()
    if not text:
        return []
    if len(text) <= max_chars:
        return [text]
    raw_chunks = _re.split(r'(?<=\n)(?=\n#{1,6} )|(?<=\n\n)', text)
    chunks = []
    for seg in raw_chunks:
        seg = seg.strip()
        if not seg:
            continue
        if len(seg) <= max_chars:
            chunks.append(seg)
            continue
        while len(seg) > max_chars:
            chunks.append(seg[:max_chars])
            seg = seg[max_chars - overlap:]
        if seg:
            chunks.append(seg)
    return chunks


def collect_documents():
    docs = []
    for kb_dir in KB_DIRS:
        if not kb_dir.exists():
            continue
        for md_file in kb_dir.rglob('*.md'):
            try:
                content = md_file.read_text(encoding='utf-8', errors='replace')
            except Exception:
                continue
            h1 = re.search(r'^# (.+?)$', content, re.MULTILINE)
            title = h1.group(1).strip() if h1 else md_file.stem
            for i, chunk in enumerate(chunk_text(content)):
                docs.append({
                    'path': str(md_file.relative_to(WORKSPACE)),
                    'title': title,
                    'chunk_id': i,
                    'content': chunk,
                })

    # --- 根目录关键文件 ---
    for md_file in sorted(WORKSPACE.glob('*.md')):
        if any(pat in md_file.name for pat in ROOT_EXCLUDE_PATTERNS):
            continue
        try:
            content = md_file.read_text(encoding='utf-8', errors='replace')
        except Exception:
            continue
        h1 = re.search(r'^# (.+?)$', content, re.MULTILINE)
        title = h1.group(1).strip() if h1 else md_file.stem
        for i, chunk in enumerate(chunk_text(content)):
            docs.append({
                'path': str(md_file.relative_to(WORKSPACE)),
                'title': title,
                'chunk_id': i,
                'content': chunk,
            })

    if MEMORY_DIR.exists():
        import datetime
        cutoff = datetime.datetime.now() - datetime.timedelta(days=MEMORY_DAYS)
        for md_file in MEMORY_DIR.rglob('*.md'):
            if any(part in MEMORY_EXCLUDE_DIRS for part in md_file.parts):
                continue
            try:
                mtime = datetime.datetime.fromtimestamp(md_file.stat().st_mtime)
                if mtime < cutoff:
                    continue
                content = md_file.read_text(encoding='utf-8', errors='replace')
                for i, chunk in enumerate(chunk_text(content)):
                    docs.append({
                        'path': str(md_file.relative_to(WORKSPACE)),
                        'title': md_file.stem,
                        'chunk_id': i,
                        'content': chunk,
                    })
            except Exception:
                pass

    return docs


def build_index():
    print('Loading model...', flush=True)
    t0 = time.time()
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(MODEL_PATH)
    print(f'  done in {time.time()-t0:.1f}s', flush=True)

    print('Collecting documents...', flush=True)
    docs = collect_documents()
    print(f'  {len(docs)} chunks', flush=True)

    print('Encoding (will take 1-5 min)...', flush=True)
    t0 = time.time()
    contents = [d['content'] for d in docs]
    # 分批 + 进度
    all_emb = []
    BATCH = 32
    for i in range(0, len(contents), BATCH):
        batch = contents[i:i+BATCH]
        emb = model.encode(batch, batch_size=BATCH, show_progress_bar=False, convert_to_numpy=True)
        all_emb.append(emb)
        done = min(i + BATCH, len(contents))
        pct = done / len(contents) * 100
        print(f'  {done}/{len(contents)} ({pct:.0f}%)', flush=True)
    embeddings = np.vstack(all_emb).astype('float32')
    print(f'  done in {time.time()-t0:.1f}s, shape={embeddings.shape}', flush=True)

    with open(INDEX_FILE, 'wb') as f:
        pickle.dump(docs, f)
    np.savez_compressed(EMBEDDINGS_FILE, embeddings=embeddings)
    print(f'Saved to {INDEX_DIR}', flush=True)
    return len(docs)


def search(query, top_k=5):
    if not INDEX_FILE.exists() or not EMBEDDINGS_FILE.exists():
        print('Index missing. Run: python kb_semantic_search.py index', flush=True)
        return []

    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(MODEL_PATH)

    with open(INDEX_FILE, 'rb') as f:
        docs = pickle.load(f)
    data = np.load(EMBEDDINGS_FILE)
    embeddings = data['embeddings']

    query_emb = model.encode([query], convert_to_numpy=True)[0].astype('float32')
    norms = np.linalg.norm(embeddings, axis=1)
    q_norm = np.linalg.norm(query_emb)
    sims = (embeddings @ query_emb) / (norms * q_norm + 1e-9)

    top_idx = np.argsort(sims)[::-1][:top_k]

    results = []
    for i in top_idx:
        results.append({
            'path': docs[i]['path'],
            'title': docs[i]['title'],
            'chunk_id': docs[i]['chunk_id'],
            'content': docs[i]['content'],
            'score': float(sims[i]),
        })
    # === Hybrid: 关键词命中加权(简单 BM25-style) ===
    import re as _re_h
    query_tokens = set(_re_h.findall(r'[\w\u4e00-\u9fff]+', query.lower()))
    if query_tokens:
        for r in results:
            content_tokens = set(_re_h.findall(r'[\w\u4e00-\u9fff]+', r['content'].lower()))
            overlap = len(query_tokens & content_tokens)
            r['_hybrid'] = r['score'] + overlap * 0.02
        results = sorted(results, key=lambda x: x.get('_hybrid', x['score']), reverse=True)
    return results


def stats():
    if not INDEX_FILE.exists():
        print('No index', flush=True)
        return
    with open(INDEX_FILE, 'rb') as f:
        docs = pickle.load(f)
    paths = set()
    for d in docs:
        parts = d['path'].split('\\')
        paths.add(parts[0])
    print(f'Total chunks: {len(docs)}', flush=True)
    print(f'Top dirs: {sorted(paths)}', flush=True)
    print(f'Index size: {EMBEDDINGS_FILE.stat().st_size / 1024 / 1024:.1f} MB', flush=True)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage:', flush=True)
        print('  python kb_semantic_search.py index', flush=True)
        print('  python kb_semantic_search.py search "query"', flush=True)
        print('  python kb_semantic_search.py stats', flush=True)
        sys.exit(0)

    cmd = sys.argv[1]
    if cmd == 'index':
        n = build_index()
        print(f'Index built: {n} chunks', flush=True)
    elif cmd == 'search':
        if len(sys.argv) < 3:
            print('Usage: python kb_semantic_search.py search "query"', flush=True)
            sys.exit(1)
        query = sys.argv[2]
        print(f'Query: {query}', flush=True)
        results = search(query, top_k=5)
        for i, r in enumerate(results, 1):
            print(f'[{i}] {r["path"]} (chunk #{r["chunk_id"]}, score: {r["score"]:.3f})', flush=True)
            print(f'    Title: {r["title"]}', flush=True)
            print(f'    Content: {r["content"][:200]}...', flush=True)
            print(flush=True)
    elif cmd == 'stats':
        stats()
    else:
        print(f'Unknown: {cmd}', flush=True)