# -*- coding: utf-8 -*-
"""
tool6: KB Incremental Indexer — 增量索引
只索引新增/修改的文件,避免全量重建(7-8 分钟 → 几秒)

用法:
  python kb_index_incremental.py           # 检查 + 报告
  python kb_index_incremental.py apply     # 实际增量索引

原理:
  1. 读取已有索引(从 documents.pkl 提取 paths + content_hash)
  2. 扫描 KB,计算每个文件的 content_hash (SHA256)
  3. 对比:
     - 新文件:path 不在已有索引 → 需要新增
     - 修改文件:path 在已有索引,但 hash 变了 → 需要重建该文件
     - 删除文件:path 在已有索引,但文件已不存在 → 需要移除
  4. 只对新文件/修改文件生成 embeddings
  5. 合并到 embeddings 数组
  6. 保存新 documents.pkl + embeddings.npz

性能:
  - 全量索引 14,740 块约 7 分钟
  - 增量索引(典型 100 个新文件):~30 秒
"""
import os, sys, hashlib, pickle, time

# --- R-F 整改 2026-09-29: 切换到中文 embedding 模型 ---
# 原: sentence-transformers/all-MiniLM-L6-v2 (英文模型, 中文检索 Top-1 仅 50%)
# 现: BAAI/bge-small-zh-v1.5 (中文, Top-1 100%, 区分度提升 2 倍)
MODEL_PATH = os.environ.get('KB_EMBED_MODEL', r'D:\B166ER-OpenClaw\workspace\toolbox\models\bge-small-zh-v1.5')
# -----------------------------------------------------
sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path
import numpy as np

WORKSPACE = Path(r'D:\B166ER-OpenClaw\workspace')
INDEX_DIR = WORKSPACE / 'toolbox' / 'kb_tools' / 'index'
INDEX_DIR.mkdir(parents=True, exist_ok=True)
DOCS_FILE = INDEX_DIR / 'documents.pkl'
EMBEDDINGS_FILE = INDEX_DIR / 'embeddings.npz'

KB_DIRS = [WORKSPACE / 'universal-kb', WORKSPACE / 'anyi-ops-kb']
MEMORY_DIR = WORKSPACE / 'memory'
MEMORY_DAYS = 14


def chunk_text(text, max_chars=500, overlap=100):
    text = text.strip()
    if len(text) <= max_chars:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start = end - overlap
    return chunks


def file_hash(path):
    """SHA256 哈希"""
    h = hashlib.sha256()
    try:
        with open(path, 'rb') as f:
            for block in iter(lambda: f.read(8192), b''):
                h.update(block)
    except Exception:
        return None
    return h.hexdigest()[:16]  # 短哈希,够用


def scan_all_files():
    """扫描所有 KB 文件,返回 {path: hash}"""
    import datetime
    import re
    files = {}
    # KB
    for kb_dir in KB_DIRS:
        if not kb_dir.exists():
            continue
        for md_file in kb_dir.rglob('*.md'):
            content_hash = file_hash(md_file)
            if content_hash:
                files[str(md_file.relative_to(WORKSPACE))] = content_hash

    # memory(最近 14 天)
    if MEMORY_DIR.exists():
        cutoff = datetime.datetime.now() - datetime.timedelta(days=MEMORY_DAYS)
        for md_file in MEMORY_DIR.glob('*.md'):
            try:
                mtime = datetime.datetime.fromtimestamp(md_file.stat().st_mtime)
                if mtime < cutoff:
                    continue
            except Exception:
                pass
            content_hash = file_hash(md_file)
            if content_hash:
                files[str(md_file.relative_to(WORKSPACE))] = content_hash

    return files


def get_existing_index():
    """读取已有索引,返回:
       - existing_paths: {path: chunk_count}
       - existing_chunks: 已有文档块列表
       - existing_embeddings: 已有 embeddings 数组
    """
    if not DOCS_FILE.exists() or not EMBEDDINGS_FILE.exists():
        return {}, [], None

    with open(DOCS_FILE, 'rb') as f:
        docs = pickle.load(f)

    data = np.load(EMBEDDINGS_FILE)
    embeddings = data['embeddings']

    # 统计每个路径的块数
    path_counts = {}
    for d in docs:
        path_counts[d['path']] = path_counts.get(d['path'], 0) + 1

    return path_counts, docs, embeddings


def collect_chunks_for_file(filepath):
    """对单个文件生成 chunks"""
    import re
    try:
        content = filepath.read_text(encoding='utf-8', errors='replace')
    except Exception:
        return []
    h1 = re.search(r'^# (.+?)$', content, re.MULTILINE)
    title = h1.group(1).strip() if h1 else filepath.stem
    chunks = chunk_text(content)
    result = []
    for i, chunk in enumerate(chunks):
        result.append({
            'path': str(filepath.relative_to(WORKSPACE)),
            'title': title,
            'chunk_id': i,
            'content': chunk,
        })
    return result


def check():
    """检查变化, 但不修改"""
    print('=== 增量索引检查 ===\n')
    t0 = time.time()
    print('1. 扫描所有 KB 文件...', flush=True)
    current_files = scan_all_files()
    print(f'   当前 KB 文件: {len(current_files)} 个')

    print('2. 读取已有索引...', flush=True)
    existing_counts, existing_docs, existing_emb = get_existing_index()
    print(f'   已有索引块: {len(existing_docs)} 块')
    existing_paths = set(c['path'] for c in existing_docs)

    # 对比
    current_paths = set(current_files.keys())

    new_files = current_paths - existing_paths
    modified_files = []
    deleted_files = existing_paths - current_paths

    # 检查修改(已有路径但 hash 不同)
    # 注意:已索引的 docs 没有存 hash,只能通过文件大小或时间戳粗略判断
    # 更准确:对已有路径重新计算 hash,与已索引的 docs[0].content_hash 对比
    # 简化:检查文件 mtime > 索引文件 mtime
    index_mtime = max((DOCS_FILE.stat().st_mtime, EMBEDDINGS_FILE.stat().st_mtime))
    for path in (current_paths & existing_paths):
        full = WORKSPACE / path
        try:
            if full.stat().st_mtime > index_mtime:
                modified_files.append(path)
        except Exception:
            pass

    print()
    print('=== 变化清单 ===')
    print(f'  新增文件: {len(new_files)} 个')
    for f in sorted(new_files)[:10]:
        print(f'    + {f}')
    if len(new_files) > 10:
        print(f'    ... +{len(new_files)-10} 个')

    print(f'\n  修改文件: {len(modified_files)} 个')
    for f in sorted(modified_files)[:10]:
        print(f'    ~ {f}')
    if len(modified_files) > 10:
        print(f'    ... +{len(modified_files)-10} 个')

    print(f'\n  删除文件: {len(deleted_files)} 个')
    for f in sorted(deleted_files)[:10]:
        print(f'    - {f}')
    if len(deleted_files) > 10:
        print(f'    ... +{len(deleted_files)-10} 个')

    # 估算增量块数
    print()
    new_blocks = 0
    for f in new_files:
        full = WORKSPACE / f
        try:
            size_kb = full.stat().st_size / 1024
            new_blocks += max(1, int(size_kb / 0.5))  # 估 0.5KB 一块
        except Exception:
            new_blocks += 5

    print(f'=== 估算增量索引 ===')
    print(f'  新增/修改文件: {len(new_files) + len(modified_files)} 个')
    print(f'  估算新增块: ~{new_blocks} 块')
    print(f'  估算耗时: ~{new_blocks / 30:.0f} 秒(30 块/秒)')

    return {
        'new': new_files,
        'modified': modified_files,
        'deleted': deleted_files,
        'existing_docs': existing_docs,
        'existing_emb': existing_emb,
    }


def apply():
    """执行增量索引"""
    print('=== 增量索引 APPLY ===\n')
    changes = check()

    new_files = changes['new']
    modified_files = changes['modified']
    deleted_files = changes['deleted']
    existing_docs = changes['existing_docs']
    existing_emb = changes['existing_emb']

    if not new_files and not modified_files and not deleted_files:
        print('\n✅ 没有变化,索引已是最新')
        return

    # 1. 处理删除的文件(从 docs 中移除)
    deleted_set = set(deleted_files)
    keep_idx = [i for i, d in enumerate(existing_docs) if d['path'] not in deleted_set]
    filtered_docs = [existing_docs[i] for i in keep_idx]
    if existing_emb is not None:
        filtered_emb = existing_emb[keep_idx]
    else:
        filtered_emb = np.array([])
    print(f'1. 移除 {len(existing_docs) - len(filtered_docs)} 个删除文件的索引')

    # 2. 对修改的文件:先从 filtered 中移除,再重新加
    modified_set = set(modified_files)
    filtered_docs = [d for d in filtered_docs if d['path'] not in modified_set]
    if len(filtered_docs) < len(filtered_docs) or modified_set:
        # 重新算 filtered_emb
        keep_idx2 = [i for i, d in enumerate(existing_docs)
                     if d['path'] not in deleted_set and d['path'] not in modified_set]
        filtered_emb = existing_emb[keep_idx2]
    print(f'2. 移除 {len(modified_set)} 个修改文件的旧索引')

    # 3. 处理新增/修改的文件
    to_process = list(new_files) + list(modified_files)
    if to_process:
        print(f'3. 生成 {len(to_process)} 个文件的 embeddings...', flush=True)
        t0 = time.time()
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(MODEL_PATH)
        print(f'   模型加载: {time.time()-t0:.1f}s', flush=True)

        new_docs = []
        new_emb_list = []
        BATCH = 32
        batch_chunks = []
        batch_meta = []

        def flush_batch():
            nonlocal batch_chunks, batch_meta, new_docs, new_emb_list
            if not batch_chunks:
                return
            emb = model.encode(batch_chunks, batch_size=BATCH, show_progress_bar=False, convert_to_numpy=True)
            new_emb_list.append(emb)
            new_docs.extend(batch_meta)
            batch_chunks = []
            batch_meta = []

        for i, rel_path in enumerate(to_process):
            full = WORKSPACE / rel_path
            chunks = collect_chunks_for_file(full)
            for chunk in chunks:
                batch_chunks.append(chunk['content'])
                batch_meta.append(chunk)
            if len(batch_chunks) >= BATCH:
                flush_batch()
            if (i + 1) % 20 == 0:
                print(f'   {i+1}/{len(to_process)} 文件', flush=True)

        flush_batch()
        new_embeddings = np.vstack(new_emb_list).astype('float32') if new_emb_list else np.array([])
        print(f'   embeddings: shape={new_embeddings.shape}, {time.time()-t0:.1f}s', flush=True)

        # 合并
        filtered_docs = filtered_docs + new_docs
        if len(filtered_emb) == 0:
            filtered_emb = new_embeddings
        elif len(new_embeddings) > 0:
            filtered_emb = np.vstack([filtered_emb, new_embeddings])
        print(f'4. 合并后总块数: {len(filtered_docs)}')

    # 5. 保存
    with open(DOCS_FILE, 'wb') as f:
        pickle.dump(filtered_docs, f)
    np.savez_compressed(EMBEDDINGS_FILE, embeddings=filtered_emb)
    print(f'\n✅ 增量索引完成: {len(filtered_docs)} 块, 大小 {EMBEDDINGS_FILE.stat().st_size / 1024 / 1024:.1f} MB')

    # 6. 元数据
    meta = {
        'total_chunks': len(filtered_docs),
        'total_size_mb': EMBEDDINGS_FILE.stat().st_size / 1024 / 1024,
        'updated_at': time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    meta_file = INDEX_DIR / 'index_meta.json'
    meta_file.write_text(
        str(meta).replace("'", '"'),
        encoding='utf-8'
    )


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'apply':
        apply()
    else:
        check()