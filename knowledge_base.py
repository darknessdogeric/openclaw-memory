"""
B166ER 知识库系统 v1.0
基于 scikit-learn + SQLite 的轻量级向量检索
零API成本，本地运行
"""

import sqlite3
import json
import numpy as np
from pathlib import Path
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import hashlib

class B166ERKnowledgeBase:
    """轻量级知识库: TF-IDF + SQLite"""
    
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = Path.home() / ".openclaw" / "knowledge.db"
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
        
    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                metadata TEXT,
                chunk_index INTEGER DEFAULT 0,
                doc_hash TEXT UNIQUE,
                created_at TEXT,
                updated_at TEXT,
                access_count INTEGER DEFAULT 0,
                last_accessed TEXT
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id INTEGER,
                tag TEXT,
                FOREIGN KEY (document_id) REFERENCES documents(id)
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_hash ON documents(doc_hash)")
        conn.commit()
        conn.close()
        
    def add(self, content, metadata=None, tags=None):
        """添加文档"""
        doc_hash = hashlib.md5(content.encode()).hexdigest()
        now = datetime.now().isoformat()
        
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        
        # 检查是否已存在
        c.execute("SELECT id FROM documents WHERE doc_hash = ?", (doc_hash,))
        existing = c.fetchone()
        
        if existing:
            c.execute("""
                UPDATE documents SET updated_at = ?, access_count = access_count + 1, last_accessed = ?
                WHERE doc_hash = ?
            """, (now, now, doc_hash))
            doc_id = existing[0]
        else:
            metadata_json = json.dumps(metadata or {}, ensure_ascii=False)
            c.execute("""
                INSERT INTO documents (content, metadata, doc_hash, created_at, updated_at, last_accessed, access_count)
                VALUES (?, ?, ?, ?, ?, ?, 1)
            """, (content, metadata_json, doc_hash, now, now, now))
            doc_id = c.lastrowid
            
            if tags:
                for tag in tags:
                    c.execute("INSERT INTO tags (document_id, tag) VALUES (?, ?)", (doc_id, tag))
        
        conn.commit()
        conn.close()
        return doc_id
    
    def search(self, query, top_k=5, tags=None):
        """搜索文档"""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        
        if tags:
            placeholders = ','.join('?' * len(tags))
            c.execute(f"""
                SELECT d.id, d.content, d.metadata, d.access_count
                FROM documents d
                LEFT JOIN tags t ON d.id = t.document_id
                WHERE t.tag IN ({placeholders})
                GROUP BY d.id
            """, tags)
        else:
            c.execute("SELECT id, content, metadata, access_count FROM documents")
        
        rows = c.fetchall()
        if not rows:
            return []
        
        contents = [row[1] for row in rows]
        vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        try:
            tfidf_matrix = vectorizer.fit_transform(contents + [query])
            query_vec = tfidf_matrix[-1]
            doc_vecs = tfidf_matrix[:-1]
            
            similarities = cosine_similarity(query_vec, doc_vecs)[0]
            
            results = []
            for i, row in enumerate(rows):
                results.append({
                    'id': row[0],
                    'content': row[1],
                    'metadata': json.loads(row[2]) if row[2] else {},
                    'access_count': row[3],
                    'score': float(similarities[i])
                })
            
            results.sort(key=lambda x: (x['score'], x['access_count']), reverse=True)
            return results[:top_k]
        except:
            return [{'id': row[0], 'content': row[1], 'metadata': {}, 'access_count': row[3], 'score': 1.0} for row in rows[:top_k]]
        finally:
            conn.close()
    
    def get(self, doc_id):
        """获取单个文档"""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("SELECT id, content, metadata, access_count FROM documents WHERE id = ?", (doc_id,))
        row = c.fetchone()
        
        if row:
            c.execute("UPDATE documents SET last_accessed = ?, access_count = access_count + 1 WHERE id = ?",
                      (datetime.now().isoformat(), doc_id))
            conn.commit()
        
        conn.close()
        if row:
            return {'id': row[0], 'content': row[1], 'metadata': json.loads(row[2]) if row[2] else {}, 'access_count': row[3]}
        return None
    
    def stats(self):
        """获取统计信息"""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("SELECT COUNT(*), SUM(access_count) FROM documents")
        count, total_access = c.fetchone()
        c.execute("SELECT COUNT(DISTINCT tag) FROM tags")
        tag_count = c.fetchone()[0]
        conn.close()
        return {'documents': count or 0, 'total_access': total_access or 0, 'unique_tags': tag_count or 0}
    
    def list_tags(self):
        """列出所有标签"""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("SELECT tag, COUNT(*) FROM tags GROUP BY tag ORDER BY COUNT(*) DESC")
        tags = [{'tag': row[0], 'count': row[1]} for row in c.fetchall()]
        conn.close()
        return tags
    
    def index_file(self, file_path, tags=None):
        """索引文件内容"""
        path = Path(file_path)
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            return self.add(content, metadata={'source': str(path), 'type': path.suffix}, tags=tags)
        return None


# CLI 测试
if __name__ == "__main__":
    import sys
    
    kb = B166ERKnowledgeBase()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "add":
            content = sys.argv[2] if len(sys.argv) > 2 else input("Content: ")
            kb.add(content, tags=['manual'])
            print("Added!")
            
        elif cmd == "search":
            query = sys.argv[2] if len(sys.argv) > 2 else input("Query: ")
            results = kb.search(query)
            for r in results:
                print(f"[{r['score']:.3f}] {r['content'][:80]}")
                
        elif cmd == "stats":
            print(kb.stats())
            
        elif cmd == "tags":
            print(kb.list_tags())
    else:
        print("Usage: python knowledge_base.py [add|search|stats|tags]")
