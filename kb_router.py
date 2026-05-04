# -*- coding: utf-8 -*-
"""
B166ER 知识库核心引擎 V2.0
功能：语义路由 + KB检索 + 自动索引
"""
import sqlite3
import json
import os
import re
from pathlib import Path
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import hashlib

# ========== 路由决策表 ==========
ROUTING_TABLE = {
    "审美": {"kb": "aesthetic-knowledge-base", "triggers": ["审美", "设计", "品位", "气韵", "意境", "留白", "排版", "海报", "图片"]},
    "博弈": {"kb": "game-theory-decision-knowledge-base", "triggers": ["博弈", "谈判", "策略", "博弈论", "纳什均衡", "对手", "投资人", "合作"]},
    "酒店": {"kb": "hotel-industry-knowledge-base", "triggers": ["酒店", "民宿", "ADR", "OCC", "入住率", "洲际", "希尔顿", "万豪", "品牌", "连锁"]},
    "AI技术": {"kb": "ai-llm-knowledge-base-v2", "triggers": ["AI", "LLM", "AGENT", "Prompt", "RAG", "大模型", "Kimi", "DeepSeek", "代码", "架构"]},
    "创业融资": {"kb": "startup-fundraising-knowledge-base-v2", "triggers": ["融资", "股权", "YC", "路演", "BP", "VC", "投资", "IPO"]},
    "大乐透": {"kb": "lottery-knowledge-base-v2", "triggers": ["大乐透", "彩票", "预测", "开奖", "体彩"]},
    "金融": {"kb": "finance-securities-knowledge-base-v2", "triggers": ["金融", "证券", "投资", "股票", "债券", "REITs", "量化"]},
    "跨境": {"kb": "cross-border-trade-v1", "triggers": ["跨境", "选品", "亚马逊", "Amazon", "出海", "外贸", "集装箱"]},
    "收益管理": {"kb": "hotel-revenue-management-knowledge-base", "triggers": ["收益管理", "动态定价", "预测", "GOP", "RevPAR"]},
    "私域": {"kb": "hotel-private-domain-membership-knowledge-base", "triggers": ["私域", "会员", "RFM", "复购", "积分"]},
    "新媒体": {"kb": "hotel-new-media-marketing-knowledge-base", "triggers": ["新媒体", "抖音", "小红书", "微信", "社群", "内容营销"]},
    "智能化": {"kb": "hotel-ai-applications-knowledge-base", "triggers": ["智能化", "AI获客", "PMS", "数字化", "智慧酒店"]},
    "跨境资金": {"kb": "cross-border-payment-knowledge", "triggers": ["支付", "结算", "美元", "人民币", "汇率", "结汇"]},
}

# 知识库文件路径
KB_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
KB_EXTENSIONS = [".md", ".txt", ".json"]

class B166ERKnowledgeRouter:
    """语义路由 + KB检索引擎"""
    
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = Path.home() / ".openclaw" / "knowledge.db"
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
        
    def _init_db(self):
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                metadata TEXT,
                doc_hash TEXT UNIQUE,
                created_at TEXT,
                updated_at TEXT,
                access_count INTEGER DEFAULT 0,
                last_accessed TEXT
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS routing_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT,
                route_target TEXT,
                kb_used TEXT,
                timestamp TEXT
            )
        """)
        c.execute("CREATE INDEX IF NOT EXISTS idx_hash ON documents(doc_hash)")
        conn.commit()
        conn.close()
        
    def route(self, query):
        """语义路由：判断应该用哪个知识库"""
        query_lower = query.lower()
        scores = {}
        
        for category, info in ROUTING_TABLE.items():
            score = 0
            for trigger in info["triggers"]:
                if trigger.lower() in query_lower:
                    score += 1
            if score > 0:
                scores[category] = {"score": score, "kb": info["kb"]}
        
        if not scores:
            return {"category": "通用", "kb": None, "confidence": 0}
        
        best = max(scores.items(), key=lambda x: x[1]["score"])
        return {
            "category": best[0],
            "kb": best[1]["kb"],
            "confidence": best[1]["score"]
        }
    
    def add(self, content, metadata=None, tags=None):
        """添加文档到KB"""
        doc_hash = hashlib.md5(content[:5000].encode()).hexdigest()
        now = datetime.now().isoformat()
        
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        
        c.execute("SELECT id FROM documents WHERE doc_hash = ?", (doc_hash,))
        existing = c.fetchone()
        
        if existing:
            c.execute("UPDATE documents SET access_count = access_count + 1, last_accessed = ? WHERE doc_hash = ?",
                     (now, doc_hash))
            doc_id = existing[0]
        else:
            metadata_json = json.dumps(metadata or {}, ensure_ascii=False)
            c.execute("""
                INSERT INTO documents (content, metadata, doc_hash, created_at, updated_at, last_accessed, access_count)
                VALUES (?, ?, ?, ?, ?, ?, 1)
            """, (content[:50000], metadata_json, doc_hash, now, now, now))
            doc_id = c.lastrowid
            
            if tags:
                for tag in tags:
                    c.execute("INSERT INTO tags (document_id, tag) VALUES (?, ?)", (doc_id, tag))
        
        conn.commit()
        conn.close()
        return doc_id
    
    def search(self, query, top_k=5, kb_filter=None):
        """搜索KB"""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        
        if kb_filter:
            c.execute("SELECT id, content, metadata, access_count FROM documents")
        else:
            c.execute("SELECT id, content, metadata, access_count FROM documents")
        
        rows = c.fetchall()
        if not rows:
            return []
        
        contents = [row[1] for row in rows]
        try:
            vectorizer = TfidfVectorizer(max_features=1000)
            tfidf_matrix = vectorizer.fit_transform(contents + [query])
            query_vec = tfidf_matrix[-1]
            doc_vecs = tfidf_matrix[:-1]
            similarities = cosine_similarity(query_vec, doc_vecs)[0]
            
            results = []
            for i, row in enumerate(rows):
                results.append({
                    "id": row[0],
                    "content": row[1][:500] + "..." if len(row[1]) > 500 else row[1],
                    "metadata": json.loads(row[2]) if row[2] else {},
                    "access_count": row[3],
                    "score": float(similarities[i])
                })
            
            results.sort(key=lambda x: (x["score"], x["access_count"]), reverse=True)
            conn.close()
            return results[:top_k]
        except Exception as e:
            conn.close()
            return [{"id": row[0], "content": row[1][:200], "score": 1.0} for row in rows[:top_k]]
    
    def log_route(self, query, route_target, kb_used):
        """记录路由日志"""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("""
            INSERT INTO routing_log (query, route_target, kb_used, timestamp)
            VALUES (?, ?, ?, ?)
        """, (query[:200], route_target, kb_used or "", datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def get_stats(self):
        """获取统计"""
        conn = sqlite3.connect(str(self.db_path))
        c = conn.cursor()
        c.execute("SELECT COUNT(*), SUM(access_count) FROM documents")
        count, total = c.fetchone()
        c.execute("SELECT COUNT(*), route_target FROM routing_log GROUP BY route_target ORDER BY COUNT(*) DESC LIMIT 10")
        routes = [{"target": r[1] or "未分类", "count": r[0]} for r in c.fetchall()]
        conn.close()
        return {
            "documents": count or 0,
            "total_access": total or 0,
            "top_routes": routes
        }
    
    def auto_index_kb_files(self):
        """自动索引KB目录中的文件"""
        if not KB_DIR.exists():
            return {"indexed": 0, "errors": []}
        
        indexed = 0
        errors = []
        
        for kb_file in KB_DIR.glob("*.md"):
            if kb_file.name.startswith("."):
                continue
            try:
                content = kb_file.read_text(encoding="utf-8")
                tags = self._extract_tags(content)
                self.add(
                    content=content,
                    metadata={"source": str(kb_file), "type": "kb_file", "indexed_at": datetime.now().isoformat()},
                    tags=tags
                )
                indexed += 1
            except Exception as e:
                errors.append(f"{kb_file.name}: {str(e)}")
        
        return {"indexed": indexed, "errors": errors}
    
    def _extract_tags(self, content):
        """从内容中提取标签"""
        tags = []
        # 提取 # 标题作为标签
        for line in content.split("\n")[:20]:
            if line.startswith("# ") and len(line) > 2:
                tag = line[2:].strip()[:30]
                if tag:
                    tags.append(tag)
        return tags[:5]


# ========== CLI 入口 ==========
if __name__ == "__main__":
    import sys
    
    kb = B166ERKnowledgeRouter()
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "route":
            query = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
            result = kb.route(query)
            print(f"路由结果: {result}")
            
        elif cmd == "index":
            result = kb.auto_index_kb_files()
            print(f"索引完成: {result}")
            
        elif cmd == "stats":
            print(kb.get_stats())
            
        elif cmd == "search":
            query = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""
            results = kb.search(query)
            for r in results:
                print(f"[{r['score']:.3f}] {r['content'][:80]}")
    else:
        print("用法: python kb_router.py [route|index|stats|search] [args...]")
