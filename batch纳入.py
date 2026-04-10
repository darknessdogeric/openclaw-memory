# -*- coding: utf-8 -*-
"""
B166ER 批量纳入引擎 V1.0
批量将文件纳入知识库体系
"""
import json
import os
from pathlib import Path
from datetime import datetime
from kb_router import B166ERKnowledgeRouter

class BatchIndexer:
    """批量纳入引擎"""
    
    def __init__(self):
        self.kb = B166ERKnowledgeRouter()
        self.inventory_file = Path.home() / ".openclaw" / "workspace" / "memory" / "file_inventory.json"
        self.processed_file = Path.home() / ".openclaw" / "workspace" / "memory" / "纳入_history.json"
        
    def load_inventory(self):
        """加载文件清单"""
        if self.inventory_file.exists():
            return json.loads(self.inventory_file.read_text(encoding="utf-8"))
        return []
    
    def load_processed(self):
        """加载已处理记录"""
        if self.processed_file.exists():
            return json.loads(self.processed_file.read_text(encoding="utf-8"))
        return {}
    
    def save_processed(self, processed):
        """保存处理记录"""
        self.processed_file.write_text(json.dumps(processed, ensure_ascii=False, indent=2), encoding="utf-8")
    
    def extract_text_md(self, file_path):
        """提取.md文件文本"""
        try:
            return file_path.read_text(encoding="utf-8", errors="ignore")
        except:
            return None
    
    def extract_text_docx(self, file_path):
        """提取.docx文件文本"""
        try:
            from docx import Document
            doc = Document(str(file_path))
            return "\n".join([p.text for p in doc.paragraphs])
        except:
            return None
    
    def extract_text_pdf(self, file_path):
        """提取.pdf文件文本"""
        try:
            import pdfplumber
            with pdfplumber.open(str(file_path)) as pdf:
                text = "\n".join([page.extract_text() or "" for page in pdf.pages])
            return text if text.strip() else None
        except:
            return None
    
    def determine_kb_category(self, file_path, content):
        """判断KB分类"""
        path_str = str(file_path).lower()
        content_lower = content[:1000].lower() if content else ""
        
        # 按路径判断
        if "ahl" in path_str or "去中心化" in path_str:
            return "AHL项目"
        if "自我革命" in path_str:
            return "自我革命"
        if "收益" in path_str or "revenue" in path_str:
            return "酒店收益管理"
        if "酒店" in path_str or "hotel" in path_str:
            return "酒店行业"
        if "融资" in path_str or "bp" in path_str or "商业" in path_str:
            return "创业融资"
        
        # 按内容判断
        if any(k in content_lower for k in ["酒店", "民宿", "收益", "ADR", "OCC"]):
            return "酒店行业"
        if any(k in content_lower for k in ["融资", "VC", "投资", "股权"]):
            return "创业融资"
        if any(k in content_lower for k in ["AI", "LLM", "AGENT", "大模型"]):
            return "AI技术"
        
        return "未分类"
    
    def should_index(self, file_info, processed):
        """判断是否应该纳入"""
        path = file_info["path"]
        
        # 已在processed中，跳过
        if path in processed:
            return False
        
        # workspace/memory 中的 .md 文件（已索引过）
        if path.startswith(str(Path.home() / ".openclaw" / "workspace" / "memory")) and file_info["ext"] == ".md":
            return True  # 重新检查
        
        # 非常大的文件 (>50MB)，跳过
        if file_info["size_kb"] > 50000:
            return False
        
        # 非常小的文件 (<1KB)，跳过
        if file_info["size_kb"] < 1:
            return False
        
        return True
    
    def index_file(self, file_info):
        """索引单个文件"""
        path = Path(file_info["path"])
        
        # 提取文本
        if file_info["ext"] == ".md":
            content = self.extract_text_md(path)
        elif file_info["ext"] == ".docx":
            content = self.extract_text_docx(path)
        elif file_info["ext"] == ".pdf":
            content = self.extract_text_pdf(path)
        else:
            content = None
        
        if not content or len(content.strip()) < 100:
            return {"path": path.name, "status": "failed", "reason": "内容过少或提取失败"}
        
        # 判断分类
        category = self.determine_kb_category(path, content)
        
        # 截断过长内容
        if len(content) > 50000:
            content = content[:50000]
        
        # 纳入KB
        doc_id = self.kb.add(
            content=content,
            metadata={
                "source": str(path),
                "type": file_info["ext"],
                "category": category,
                "size_kb": file_info["size_kb"],
                "indexed_at": datetime.now().isoformat(),
                "batch_indexed": True
            },
            tags=[category]
        )
        
        return {"path": path.name, "category": category, "doc_id": doc_id, "content_len": len(content), "status": "success"}
    
    def run_batch(self, limit=100, priority_classes=None):
        """批量纳入"""
        print(f"开始批量纳入 (限制: {limit})...")
        
        files = self.load_inventory()
        processed = self.load_processed()
        
        # 按优先级排序
        priority_files = [f for f in files if self.should_index(f, processed)]
        priority_files.sort(key=lambda x: x["priority"])
        
        if priority_classes:
            priority_files = [f for f in priority_files if self.determine_kb_category(f["path"], "") in priority_classes]
        
        results = {"success": 0, "failed": 0, "skipped": 0, "details": []}
        
        for i, f in enumerate(priority_files[:limit]):
            if f["priority"] > 4:  # 只处理 md, txt, json, docx
                continue
                
            result = self.index_file(f)
            processed[f["path"]] = result
            
            if result["status"] == "success":
                results["success"] += 1
                print(f"  ✅ [{i+1}] {result['category']}: {result['path'][:60]}...")
            else:
                results["failed"] += 1
                print(f"  ❌ {result['path']}: {result.get('reason', 'unknown')}")
            
            results["details"].append(result)
        
        self.save_processed(processed)
        
        print(f"\n批量纳入完成:")
        print(f"  成功: {results['success']}")
        print(f"  失败: {results['failed']}")
        
        return results

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    
    indexer = BatchIndexer()
    
    # 批量纳入Top文件
    results = indexer.run_batch(limit=200)
    
    # 保存结果
    result_file = Path.home() / ".openclaw" / "workspace" / "memory" / "batch_index_result.json"
    result_file.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n结果已保存: {result_file}")
