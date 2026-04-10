#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

"""
B166ER 本地语义搜索工具
- Embedding: model2vec (minishlab/potion-base-8M) — 8MB, CPU, 500×快
- Vector DB: Chromadb (本地持久化)
- 完全免费、无API依赖、离线可用
"""
import os, sys, glob
from pathlib import Path
from model2vec import StaticModel
import chromadb
from chromadb import PersistentClient

# ===== 配置 =====
MEMORY_DIR = Path("C:/Users/ericz/.openclaw/workspace/memory")
CHROMA_DIR = Path("C:/Users/ericz/.openclaw/workspace/.chroma_db")
MODEL_NAME = "minishlab/potion-base-8M"
COLLECTION_NAME = "b166er_memory"

# ===== 初始化 =====
print(" 初始化本地语义搜索...")
print(f"   Model: {MODEL_NAME}")
print(f"   Chroma: {CHROMA_DIR}")
print(f"   Memory: {MEMORY_DIR}")

# 加载 embedding 模型
model = StaticModel.from_pretrained(MODEL_NAME)
print(f"   Embedding维度: {len(model.encode(['test'])[0])}")

# 初始化 Chromadb
CHROMA_DIR.mkdir(exist_ok=True)
chroma_client = PersistentClient(path=str(CHROMA_DIR))

# 获取或创建 collection
try:
    collection = chroma_client.create_collection(
        name=COLLECTION_NAME,
        metadata={"description": "B166ER记忆库"}
    )
    print(f"   [OK] 新建 collection: {COLLECTION_NAME}")
except Exception:
    collection = chroma_client.get_collection(name=COLLECTION_NAME)
    print(f"    已有 collection: {COLLECTION_NAME}")

def index_memory_files():
    """索引 memory 目录下所有 .md 文件"""
    files = []
    for ext in ["*.md", "*.txt"]:
        files.extend(MEMORY_DIR.glob(f"**/{ext}"))
    
    # 过滤日志文件
    files = [f for f in files if not f.stem.startswith("2026-")]
    
    print(f"\n 找到 {len(files)} 个文件待索引...")
    
    ids, documents, metadatas = [], [], []
    
    for i, f in enumerate(files):
        try:
            with open(f, "r", encoding="utf-8", errors="ignore") as fh:
                content = fh.read()
            
            # 截取前2000字符（避免超长）
            content = content[:2000]
            
            rel_path = str(f.relative_to(MEMORY_DIR))
            
            ids.append(f"doc_{i}")
            documents.append(content)
            metadatas.append({"source": rel_path, "size": len(content)})
            
            if (i + 1) % 50 == 0:
                print(f"   进度: {i+1}/{len(files)}")
        except Exception as e:
            print(f"   [WARN]️ 跳过 {f.name}: {e}")
    
    if ids:
        # 生成 embeddings
        print(f"\n 生成 embeddings ({len(ids)} 个)...")
        embeddings = model.encode(documents)
        
        # 存入 Chromadb
        print(f" 存入 Chromadb...")
        collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings.tolist(),
            metadatas=metadatas
        )
        print(f"   [OK] 索引完成: {len(ids)} 个文档")
    else:
        print("   [WARN]️ 没有文件可索引")

def search(query, n=5):
    """语义搜索"""
    emb = model.encode([query])
    results = collection.query(
        query_embeddings=emb.tolist(),
        n_results=n
    )
    
    print(f"\n 搜索: {query}")
    print("=" * 60)
    
    for i, (doc, meta, dist) in enumerate(zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    )):
        print(f"\n[Result {i+1}]: {meta['source']}")
        print(f"   Score: {1 - dist:.4f}")
        preview = doc[:150].encode('utf-8', errors='replace').decode('utf-8')
        print(f"   Preview: {preview}...")
    
    return results

def count():
    """统计"""
    count = collection.count()
    print(f"\n Collection 统计: {count} 个文档")
    return count

# ===== 主命令 =====
if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "count"
    
    if cmd == "index":
        index_memory_files()
    elif cmd == "count":
        count()
    elif cmd == "search":
        query = sys.argv[2] if len(sys.argv) > 2 else "AHL"
        search(query)
    elif cmd == "full":
        count()
        index_memory_files()
        count()
    else:
        print(f"用法: python local_semantic_search.py [index|count|search|full]")
        print(f"  index  — 重建索引")
        print(f"  count  — 查看统计")
        print(f"  search <query> — 搜索")
        print(f"  full   — 完整重建")
