# -*- coding: utf-8 -*-
"""
B166ER 知识库自动迭代系统
功能：
1. 定期检查KB质量
2. 自动清理/归档过期内容
3. 更新索引
4. 自我反思日志
"""
import os
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from kb_router import B166ERKnowledgeRouter

# 路径配置
KB_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
ARCHIVE_DIR = Path.home() / ".openclaw" / "workspace" / "memory" / "archive"
SELF_IMPROVING_DIR = Path.home() / ".openclaw" / "self-improving"

class B166ERIteration:
    """自动迭代维护"""
    
    def __init__(self):
        self.kb = B166ERKnowledgeRouter()
        self.today = datetime.now().strftime("%Y-%m-%d")
        
    def weekly_maintenance(self):
        """每周维护任务"""
        report = {
            "date": self.today,
            "tasks": [],
            "kb_stats": {},
            "corrections": [],
            "action_items": []
        }
        
        # 1. KB统计
        report["kb_stats"] = self.kb.get_stats()
        
        # 2. 检查过期的自反思内容
        corrections = self._check_corrections()
        report["corrections"] = corrections
        
        # 3. 检查需要归档的文件
        to_archive = self._check_archive_candidates()
        report["to_archive"] = to_archive
        
        # 4. 重新索引KB
        result = self.kb.auto_index_kb_files()
        report["indexing"] = result
        
        # 5. 生成行动项
        report["action_items"] = self._generate_action_items(report)
        
        return report
    
    def _check_corrections(self):
        """检查corrections文件"""
        corrections_file = SELF_IMPROVING_DIR / "corrections.md"
        if not corrections_file.exists():
            return []
        
        content = corrections_file.read_text(encoding="utf-8")
        lines = content.split("\n")
        
        # 统计最近7天的corrections
        recent = []
        for line in lines:
            if self.today in line:
                recent.append(line.strip())
        
        return recent
    
    def _check_archive_candidates(self):
        """检查需要归档的文件"""
        if not KB_DIR.exists():
            return []
        
        candidates = []
        for f in KB_DIR.glob("*.md"):
            # 检查最后修改时间
            mtime = datetime.fromtimestamp(f.stat().st_mtime)
            if (datetime.now() - mtime).days > 90:  # 90天未修改
                candidates.append({"file": f.name, "last_modified": mtime.strftime("%Y-%m-%d")})
        
        return candidates[:10]  # 最多返回10个
    
    def _generate_action_items(self, report):
        """生成行动项"""
        items = []
        
        if report["kb_stats"]["documents"] == 0:
            items.append("⚠️ KB为空，执行首次索引")
        
        if len(report["corrections"]) > 5:
            items.append(f"📝 最近有{len(report['corrections'])}条corrections，检查是否有规律可固化")
        
        if len(report["to_archive"]) > 0:
            items.append(f"📦 {len(report['to_archive'])}个文件待归档")
        
        if report.get("indexing", {}).get("errors"):
            items.append(f"❌ 索引有{len(report['indexing']['errors'])}个错误")
        
        return items
    
    def log_iteration(self, report):
        """记录迭代日志"""
        log_file = SELF_IMPROVING_DIR / "iterations" / f"{self.today}.json"
        log_file.parent.mkdir(parents=True, exist_ok=True)
        log_file.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        return str(log_file)
    
    def run(self):
        """执行完整迭代"""
        print(f"🔄 开始 {self.today} 周常维护...")
        
        report = self.weekly_maintenance()
        
        # 记录日志
        log_path = self.log_iteration(report)
        print(f"📝 报告已保存: {log_path}")
        
        # 输出摘要
        print("\n📊 KB状态:")
        print(f"   文档数: {report['kb_stats'].get('documents', 0)}")
        print(f"   总访问: {report['kb_stats'].get('total_access', 0)}")
        
        if report["action_items"]:
            print("\n📋 行动项:")
            for item in report["action_items"]:
                print(f"   {item}")
        
        return report


if __name__ == "__main__":
    iteration = B166ERIteration()
    iteration.run()
