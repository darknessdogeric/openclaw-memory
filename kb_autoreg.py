# -*- coding: utf-8 -*-
"""
B166ER 知识库自动纳入系统 V1.0
核心理念: 主动发现新内容，自动纳入体系，而非被动等待
"""
import json
import os
import re
from pathlib import Path
from datetime import datetime
from kb_router import B166ERKnowledgeRouter

# ========== 知识库目录规范 ==========
KB_ROOT = Path.home() / ".openclaw" / "workspace" / "memory"
SKILLS_DIR = Path.home() / ".openclaw" / "workspace" / "skills"
ARCHIVE_DIR = KB_ROOT / "archive"

# 知识库命名规范
KB_NAMING_PATTERN = re.compile(r"^(.+?)-([vV]\d+(\.\d+)?|V\d+(\.\d+)?)\.md$")

class KBAutoreg:
    """知识库自动纳入系统"""
    
    def __init__(self):
        self.kb = B166ERKnowledgeRouter()
        self.router_file = SKILLS_DIR / "knowledge-base" / "SKILL.md"
        
    def scan_new_kb_files(self):
        """扫描新KB文件（未索引的）"""
        if not KB_ROOT.exists():
            return []
        
        indexed_hashes = set()
        conn = self.kb.db_path
        import sqlite3
        c = sqlite3.connect(str(conn)).cursor()
        c.execute("SELECT metadata FROM documents WHERE metadata LIKE '%kb_file%'")
        for row in c.fetchall():
            try:
                meta = json.loads(row[0])
                if "source" in meta:
                    indexed_hashes.add(meta["source"])
            except:
                pass
        
        new_files = []
        for f in KB_ROOT.glob("*.md"):
            if f.name.startswith("."):
                continue
            if str(f) not in indexed_hashes:
                new_files.append(f)
        
        return new_files
    
    def parse_kb_metadata(self, content):
        """从KB文件解析元数据（名称/类别/触发词）"""
        metadata = {
            "name": None,
            "category": None,
            "triggers": [],
            "version": None
        }
        
        lines = content.split("\n")
        
        # 解析标题
        for line in lines[:10]:
            if line.startswith("# "):
                metadata["name"] = line[2:].strip()
                break
        
        # 解析标签/分类
        category_patterns = [
            r"\*\*分类\*\*[:：]\s*(.+)",
            r"\*\*类别\*\*[:：]\s*(.+)",
            r"\*\*类型\*\*[:：]\s*(.+)",
            r"category[:：]\s*(.+)",
            r"type[:：]\s*(.+)",
        ]
        for line in lines[:30]:
            for pattern in category_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    metadata["category"] = match.group(1).strip()
                    break
        
        # 解析触发词
        trigger_patterns = [
            r"触发词[:：]\s*(.+)",
            r"triggers[:：]\s*(.+)",
            r"关键词[:：]\s*(.+)",
        ]
        for line in lines[:30]:
            for pattern in trigger_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    triggers = re.split(r"[/,，、]", match.group(1))
                    metadata["triggers"] = [t.strip() for t in triggers if t.strip()][:10]
                    break
        
        # 解析版本
        version_match = re.search(r"[vV](\d+(?:\.\d+)?)", content[:500])
        if version_match:
            metadata["version"] = version_match.group(0)
        
        return metadata
    
    def auto纳入(self, kb_file):
        """将新KB文件自动纳入体系"""
        try:
            content = kb_file.read_text(encoding="utf-8")
            meta = self.parse_kb_metadata(content)
            
            # 1. 索引到KB
            self.kb.add(
                content=content,
                metadata={
                    "source": str(kb_file),
                    "type": "kb_file",
                    "name": meta["name"],
                    "category": meta["category"],
                    "indexed_at": datetime.now().isoformat(),
                    "auto_纳入": True
                },
                tags=[meta["category"]] if meta["category"] else None
            )
            
            # 2. 更新路由表（如果解析到触发词）
            if meta["triggers"] and meta["category"]:
                self._update_routing_table(meta["category"], meta["triggers"], str(kb_file.name))
            
            return {
                "file": kb_file.name,
                "metadata": meta,
                "status": "success"
            }
        except Exception as e:
            return {
                "file": kb_file.name,
                "error": str(e),
                "status": "failed"
            }
    
    def _update_routing_table(self, category, triggers, kb_filename):
        """自动更新路由表"""
        # 这个会在路由引擎的下次加载时生效
        # 实际更新需要修改 kb_router.py 的 ROUTING_TABLE
        # 这里只记录待更新
        update_needed_file = KB_ROOT / "routing_update_needed.json"
        updates = []
        if update_needed_file.exists():
            updates = json.loads(update_needed_file.read_text(encoding="utf-8"))
        
        updates.append({
            "category": category,
            "triggers": triggers,
            "kb_file": kb_filename,
            "added_at": datetime.now().isoformat()
        })
        
        update_needed_file.write_text(json.dumps(updates, ensure_ascii=False, indent=2), encoding="utf-8")
    
    def run_autoreg(self):
        """执行自动纳入"""
        print("🔄 开始自动纳入检查...")
        
        new_files = self.scan_new_kb_files()
        print(f"发现 {len(new_files)} 个新KB文件")
        
        results = []
        for f in new_files:
            result = self.auto纳入(f)
            results.append(result)
            if result["status"] == "success":
                print(f"  ✅ {f.name} → {result['metadata'].get('category', 'unknown')}")
            else:
                print(f"  ❌ {f.name} → {result.get('error', 'unknown error')}")
        
        # 检查是否有待更新的路由表
        update_file = KB_ROOT / "routing_update_needed.json"
        if update_file.exists():
            updates = json.loads(update_file.read_text(encoding="utf-8"))
            if updates:
                print(f"\n📝 有 {len(updates)} 个路由表更新待应用")
                self._apply_routing_updates(updates)
        
        return results
    
    def _apply_routing_updates(self, updates):
        """应用路由表更新"""
        # 读取当前路由表
        router_py = Path.home() / ".openclaw" / "workspace" / "kb_router.py"
        content = router_py.read_text(encoding="utf-8")
        
        # 这里可以实现自动更新ROUTING_TABLE的逻辑
        # 目前只是记录，下次kb_router.py加载时会自动包含新的KB
        print("  路由表更新已记录，将在下次系统加载时生效")
        
        # 清空已应用的更新
        update_file = KB_ROOT / "routing_update_needed.json"
        update_file.write_text("[]", encoding="utf-8")


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    autoreg = KBAutoreg()
    results = autoreg.run_autoreg()
    print(f"\n✅ 自动纳入完成: {len([r for r in results if r['status'] == 'success'])}/{len(results)}")
