#!/usr/bin/env python3
"""
B166ER 混合检索引擎 (Hybrid RAG Knowledge Base)
================================================
FTS5 关键词 + model2vec 语义向量 → 混合检索 → 重排序 → DeepSeek RAG

依赖: pip install model2vec chromadb
零依赖降级: 仅 SQLite FTS5 (无需安装任何包)

用法:
  python kb_rag.py index                    # 增量索引 (FTS5 + 向量)
  python kb_rag.py index --rebuild          # 重建索引
  python kb_rag.py search "查询内容"         # 混合搜索
  python kb_rag.py ask "你的问题"            # RAG 问答
  python kb_rag.py stats                    # 统计信息
"""

import os
import sys
import json
import re
import sqlite3
import hashlib
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

# === 配置 ===
WORKSPACE = Path(os.environ.get("WORKSPACE", r"C:\Users\Administrator\.openclaw\workspace"))
DB_PATH = WORKSPACE / ".kb_rag.db"
CHROMA_DIR = WORKSPACE / ".chroma_db"
INDEX_EXTS = {".md", ".txt", ".py", ".json", ".yaml", ".yml", ".html", ".css", ".js", ".ts", ".csv"}
SKIP_DIRS = {".git", ".chroma_db", "node_modules", "__pycache__", ".venv", "archive_versions", "archive_hotel", "skills"}
MAX_FILE_SIZE = 500 * 1024
CHUNK_SIZE = 500
TOP_K = 10

# LLM
LLM_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
LLM_BASE_URL = "https://api.deepseek.com/v1"
LLM_MODEL = "deepseek-chat"

# === 向量模型 (延迟加载) ===
MODEL_NAME = "minishlab/potion-base-8M"  # 8MB, 256维, CPU
_model = None
_chroma_client = None
_collection = None

def _load_model():
    global _model
    if _model is None:
        from model2vec import StaticModel
        _model = StaticModel.from_pretrained(MODEL_NAME)
    return _model

def _load_chroma():
    global _chroma_client, _collection
    if _chroma_client is None:
        import chromadb
        CHROMA_DIR.mkdir(exist_ok=True)
        _chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        try:
            _collection = _chroma_client.create_collection(
                name="kb_rag_chunks",
                metadata={"description": "B166ER 知识库分块"}
            )
        except Exception:
            _collection = _chroma_client.get_collection(name="kb_rag_chunks")
    return _collection

def has_vector():
    try:
        import model2vec
        import chromadb
        return True
    except ImportError:
        return False

# === 数据库 ===
def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT UNIQUE NOT NULL,
            hash TEXT NOT NULL,
            size INTEGER,
            indexed_at TEXT DEFAULT (datetime('now','localtime'))
        );
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_id INTEGER REFERENCES files(id) ON DELETE CASCADE,
            chunk_index INTEGER,
            content TEXT NOT NULL,
            tokens TEXT NOT NULL
        );
        CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
            content, tokens,
            content='chunks',
            content_rowid='id'
        );
        CREATE INDEX IF NOT EXISTS idx_chunks_file ON chunks(file_id);
        CREATE INDEX IF NOT EXISTS idx_files_path ON files(path);
        -- FTS 同步触发器
        CREATE TRIGGER IF NOT EXISTS chunks_ai AFTER INSERT ON chunks BEGIN
            INSERT INTO chunks_fts(rowid, content, tokens) VALUES (new.id, new.content, new.tokens);
        END;
        CREATE TRIGGER IF NOT EXISTS chunks_ad AFTER DELETE ON chunks BEGIN
            INSERT INTO chunks_fts(chunks_fts, rowid, content, tokens) VALUES ('delete', old.id, old.content, old.tokens);
        END;
        CREATE TRIGGER IF NOT EXISTS chunks_au AFTER UPDATE ON chunks BEGIN
            INSERT INTO chunks_fts(chunks_fts, rowid, content, tokens) VALUES ('delete', old.id, old.content, old.tokens);
            INSERT INTO chunks_fts(rowid, content, tokens) VALUES (new.id, new.content, new.tokens);
        END;
    """)
    conn.commit()
    conn.close()

# === 分词 ===
def tokenize(text):
    tokens = []
    chinese = re.findall(r'[\u4e00-\u9fff]+', text.lower())
    for phrase in chinese:
        for i in range(len(phrase)):
            tokens.append(phrase[i])
            if i + 1 < len(phrase):
                tokens.append(phrase[i:i+2])
    english = re.findall(r'[a-zA-Z][a-zA-Z0-9_-]+', text.lower())
    tokens.extend(english)
    return ' '.join(tokens)

def file_hash(filepath):
    h = hashlib.md5()
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

# === 索引 ===
def index_file(conn, filepath, use_vector=True):
    path = str(filepath.relative_to(WORKSPACE))
    try:
        stat = filepath.stat()
        if stat.st_size > MAX_FILE_SIZE:
            return None
        fhash = file_hash(filepath)

        cur = conn.execute("SELECT id, hash FROM files WHERE path=?", (path,))
        row = cur.fetchone()
        if row and row["hash"] == fhash:
            return {"id": row["id"], "chunks": 0}  # 未变，跳过

        if row:
            conn.execute("DELETE FROM files WHERE id=?", (row["id"],))

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()

        conn.execute(
            "INSERT INTO files (path, hash, size) VALUES (?, ?, ?)",
            (path, fhash, stat.st_size)
        )
        file_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

        # 分块
        paragraphs = re.split(r'\n\n+', text)
        chunk_batch = []
        chunk_idx = 0
        for para in paragraphs:
            para = para.strip()
            if len(para) < 20:
                continue
            for i in range(0, len(para), CHUNK_SIZE):
                chunk_text = para[i:i+CHUNK_SIZE].strip()
                if len(chunk_text) < 20:
                    continue
                tokens = tokenize(chunk_text)
                conn.execute(
                    "INSERT INTO chunks (file_id, chunk_index, content, tokens) VALUES (?, ?, ?, ?)",
                    (file_id, chunk_idx, chunk_text, tokens)
                )
                chunk_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
                chunk_batch.append({"id": chunk_id, "content": chunk_text})
                chunk_idx += 1

        return {"id": file_id, "chunks": chunk_idx, "batch": chunk_batch}
    except Exception:
        return None

def index_all(rebuild=False, use_vector=True):
    print(f"[索引] 工作目录: {WORKSPACE}")
    if rebuild:
        print("[索引] 重建模式")
        conn = get_db()
        conn.execute("DELETE FROM chunks_fts")
        conn.execute("DELETE FROM chunks")
        conn.execute("DELETE FROM files")
        conn.commit()
        conn.close()

    # 向量模式初始化
    collection = None
    vector_ready = False
    if use_vector and has_vector():
        try:
            collection = _load_chroma()
            if rebuild:
                try:
                    _chroma_client.delete_collection("kb_rag_chunks")
                    collection = _chroma_client.create_collection(
                        name="kb_rag_chunks",
                        metadata={"description": "B166ER 知识库分块"}
                    )
                except Exception:
                    pass
            vector_ready = True
            print(f"[索引] 向量引擎: model2vec (256维) + Chromadb")
        except Exception as e:
            print(f"[索引] 向量引擎初始化失败: {e}，回退到纯FTS5")
    else:
        print(f"[索引] 纯 FTS5 模式 (pip install model2vec chromadb 启用向量)")

    conn = get_db()
    model = _load_model() if vector_ready else None
    total, new, skipped, vec_count = 0, 0, 0, 0
    batch_count = 0

    for root, dirs, files in os.walk(WORKSPACE):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        for fname in files:
            filepath = Path(root) / fname
            if filepath.suffix.lower() not in INDEX_EXTS:
                continue
            total += 1
            result = index_file(conn, filepath, use_vector=vector_ready)
            if result and result.get("chunks", 0) > 0:
                new += 1
                # 向量化
                if vector_ready and "batch" in result and result["batch"]:
                    batch = result["batch"]
                    ids = [f"chunk_{b['id']}" for b in batch]
                    texts = [b["content"] for b in batch]
                    try:
                        embeddings = model.encode(texts, show_progress_bar=False)
                        collection.add(
                            ids=ids,
                            embeddings=embeddings.tolist() if hasattr(embeddings, 'tolist') else list(embeddings),
                            documents=texts,
                            metadatas=[{"chunk_id": b["id"], "len": len(b["content"])} for b in batch],
                        )
                        vec_count += len(batch)
                    except Exception as e:
                        if 'already exists' not in str(e):
                            print(f"  [WARN] 向量插入失败: {e}")
            else:
                skipped += 1
            # 每100文件提交一次+进度显示
            batch_count += 1
            if batch_count % 100 == 0:
                conn.commit()
                cc = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
                print(f"  进度: {new}/{total} 文件, {cc} 分块, {vec_count} 向量")
    conn.commit()
    file_count = conn.execute("SELECT COUNT(*) FROM files").fetchone()[0]
    chunk_count = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    conn.close()

    print(f"[索引] 完成: {total}扫描, {new}索引, {skipped}跳过")
    print(f"[索引] 数据库: {file_count}文件, {chunk_count}分块", end="")
    if vector_ready:
        print(f", {vec_count}向量")
    else:
        print()

# === 关键词检索 (FTS5) ===
def fts5_search(query, top_k=TOP_K):
    conn = get_db()
    tokens = tokenize(query)
    terms = tokens.split()
    if not terms:
        conn.close()
        return []

    fts_query = ' OR '.join(terms)
    try:
        cur = conn.execute("""
            SELECT c.id, c.content, c.chunk_index, f.path, rank
            FROM chunks_fts
            JOIN chunks c ON chunks_fts.rowid = c.id
            JOIN files f ON c.file_id = f.id
            WHERE chunks_fts MATCH ?
            ORDER BY rank
            LIMIT ?
        """, (fts_query, top_k * 2))
        results = [{"id": r["id"], "content": r["content"], "path": r["path"],
                     "score": -r["rank"], "source": "fts5"} for r in cur.fetchall()]
    except sqlite3.OperationalError:
        like_term = f"%{query}%"
        cur = conn.execute("""
            SELECT c.id, c.content, f.path
            FROM chunks c
            JOIN files f ON c.file_id = f.id
            WHERE c.content LIKE ?
            LIMIT ?
        """, (like_term, top_k * 2))
        results = [{"id": r["id"], "content": r["content"], "path": r["path"],
                     "score": 0.1, "source": "like"} for r in cur.fetchall()]

    conn.close()
    return results

# === 语义检索 (model2vec + Chromadb) ===
def semantic_search(query, top_k=TOP_K):
    if not has_vector():
        return []

    try:
        model = _load_model()
        collection = _load_chroma()
        query_embedding = model.encode([query], show_progress_bar=False)
        results = collection.query(
            query_embeddings=query_embedding.tolist() if hasattr(query_embedding, 'tolist') else list(query_embedding),
            n_results=top_k * 2,
            include=["documents", "metadatas", "distances"]
        )

        items = []
        if results["ids"] and results["ids"][0]:
            for i, chunk_id in enumerate(results["ids"][0]):
                doc = results["documents"][0][i] if results["documents"] else ""
                dist = results["distances"][0][i] if results["distances"] else 1.0
                meta = results["metadatas"][0][i] if results["metadatas"] else {}
                chunk_db_id = meta.get("chunk_id", 0)

                # 查文件路径
                conn = get_db()
                cur = conn.execute("""
                    SELECT f.path FROM chunks c
                    JOIN files f ON c.file_id = f.id
                    WHERE c.id = ?
                """, (chunk_db_id,))
                row = cur.fetchone()
                conn.close()

                items.append({
                    "id": chunk_db_id,
                    "content": doc,
                    "path": row["path"] if row else "?",
                    "score": 1.0 - dist,  # 距离→相似度
                    "source": "semantic"
                })
        return sorted(items, key=lambda x: x["score"], reverse=True)[:top_k]
    except Exception as e:
        print(f"  [WARN] 语义搜索失败: {e}")
        return []

# === 混合检索 ===
def hybrid_search(query, top_k=TOP_K):
    """FTS5 + 语义 → RRF 融合去重 → 重排序"""
    fts5_results = fts5_search(query, top_k)
    sem_results = semantic_search(query, top_k)

    if not sem_results:
        return fts5_results[:top_k]  # 纯FTS5

    # RRF (Reciprocal Rank Fusion): 不同来源分数归一化
    K = 60
    seen = {}
    merged = []

    for rank, r in enumerate(sem_results, 1):
        rrf_score = 1.0 / (K + rank)
        merged.append({**r, "rrf_score": rrf_score})
        seen[r["id"]] = len(merged) - 1

    for rank, r in enumerate(fts5_results, 1):
        rrf_score = 1.0 / (K + rank)
        if r["id"] in seen:
            merged[seen[r["id"]]]["rrf_score"] += rrf_score
        else:
            merged.append({**r, "rrf_score": rrf_score})
            seen[r["id"]] = len(merged) - 1

    merged.sort(key=lambda x: x["rrf_score"], reverse=True)
    return merged[:top_k]

# === RAG 问答 ===
def ask_rag(question, top_k=TOP_K):
    """混合检索 + DeepSeek 生成"""
    results = hybrid_search(question, top_k)

    if not results:
        return "未找到相关知识。请先运行 `python kb_rag.py index`。"

    # 构建上下文
    context_parts = []
    for i, r in enumerate(results, 1):
        source_tag = f"[{'🔍' if r['source']=='fts5' else '🧠'} 语义]" if r['source'] == 'semantic' else ""
        context_parts.append(
            f"[来源{i}] {r['path']} {source_tag}\n{r['content'][:800]}"
        )

    context = "\n\n---\n\n".join(context_parts)

    if not LLM_API_KEY:
        return f"[离线模式] 找到 {len(results)} 个相关片段:\n\n{context}"

    system_prompt = """你是 B166ER 的知识库助手。基于提供的文档片段回答问题。
- 只基于提供的文档内容回答，不编造
- 如果文档中没有相关信息，明确说"文档中未找到相关信息"
- 引用时标注来源文件
- 回答简洁、有条理
- 如果来源标记了[语义]，说明是语义匹配结果，相关性更高"""

    user_prompt = f"""## 问题
{question}

## 知识库检索结果 (混合: 关键词+语义)
{context}

请基于以上知识库内容回答问题。"""

    try:
        data = json.dumps({
            "model": LLM_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 2048
        }).encode('utf-8')

        req = urllib.request.Request(
            f"{LLM_BASE_URL}/chat/completions",
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {LLM_API_KEY}"
            }
        )

        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode('utf-8'))
            return result["choices"][0]["message"]["content"]

    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8') if e.fp else str(e)
        return f"[API错误] HTTP {e.code}: {body[:500]}"
    except Exception as e:
        return f"[错误] {e}"

# === 统计 ===
def stats():
    conn = get_db()
    fc = conn.execute("SELECT COUNT(*) FROM files").fetchone()[0]
    cc = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    ts = conn.execute("SELECT COALESCE(SUM(size), 0) FROM files").fetchone()[0]
    li = conn.execute("SELECT MAX(indexed_at) FROM files").fetchone()[0]
    conn.close()

    db_sz = DB_PATH.stat().st_size if DB_PATH.exists() else 0
    chroma_sz = sum(f.stat().st_size for f in CHROMA_DIR.rglob("*") if f.is_file()) if CHROMA_DIR.exists() else 0
    vec_ok = has_vector()

    print(f"=== B166ER 混合知识库 ===")
    print(f"FTS5  数据库:  {DB_PATH} ({db_sz/1024:.0f}KB)")
    print(f"向量  数据库:  {CHROMA_DIR} ({chroma_sz/1024:.0f}KB)")
    print(f"向量  引擎:    {'✅ model2vec 256维' if vec_ok else '❌ 未安装 (pip install model2vec chromadb)'}")
    print(f"索引  文件数:  {fc}")
    print(f"分块  总数:    {cc}")
    print(f"索引  总大小:  {ts/1024:.0f}KB")
    print(f"最后  索引:    {li or '无'}")

# === 格式化输出 ===
def format_results(results, show_source=True):
    if not results:
        print("无匹配结果。")
        return
    for i, r in enumerate(results, 1):
        content_preview = r['content'][:200].replace('\n', ' ')
        source_badge = ""
        if show_source:
            icon = "🧠" if r.get('source') == 'semantic' else "🔍"
            source_badge = f" [{icon} {r['source']}]"
        print(f"[{i}] 📄 {r['path']}{source_badge}")
        print(f"    {content_preview}...")
        print()

# === CLI ===
def main():
    init_db()

    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1].lower()
    rebuild = "--rebuild" in sys.argv

    if cmd == "index":
        index_all(rebuild=rebuild)
    elif cmd == "stats":
        stats()
    elif cmd == "search":
        if len(sys.argv) < 3:
            print("用法: python kb_rag.py search \"查询内容\"")
            return
        query = sys.argv[2]
        print(f"\n🔍 混合搜索: {query}")
        results = hybrid_search(query)
        print(f"找到 {len(results)} 个结果 (关键词+语义):\n")
        format_results(results)
    elif cmd == "ask":
        if len(sys.argv) < 3:
            print("用法: python kb_rag.py ask \"你的问题\"")
            return
        question = sys.argv[2]
        print(f"\n🤔 问题: {question}")
        print(f"📚 混合检索中 (FTS5 + model2vec)...")
        answer = ask_rag(question)
        print(f"\n✨ 回答:\n{answer}")
    else:
        print(f"未知命令: {cmd}")
        print("可用: index [--rebuild], search, ask, stats")

if __name__ == "__main__":
    main()
