# -*- coding: utf-8 -*-
"""
B166ER 架构迭代进化系统 V1.0
科学迭代 = 数据驱动 + 反馈闭环 + 定期评估 + 跨领域发现
"""
import json
import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from kb_router import B166ERKnowledgeRouter

class B166EREvolution:
    """架构迭代进化"""
    
    def __init__(self):
        self.kb = B166ERKnowledgeRouter()
        self.self_improving_dir = Path.home() / ".openclaw" / "self-improving"
        self.iterations_dir = self.self_improving_dir / "iterations"
        
    def log_feedback(self, query, routed_kb, actual_kb, correct):
        """记录路由反馈，用于评估准确率"""
        conn = sqlite3.connect(str(self.kb.db_path))
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS routing_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT,
                routed_kb TEXT,
                actual_kb TEXT,
                correct INTEGER,
                timestamp TEXT
            )
        """)
        c.execute("""
            INSERT INTO routing_feedback (query, routed_kb, actual_kb, correct, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (query[:200], routed_kb or "", actual_kb or "", 1 if correct else 0, datetime.now().isoformat()))
        conn.commit()
        conn.close()
    
    def evaluate_routing_accuracy(self, days=7):
        """评估路由准确率"""
        conn = sqlite3.connect(str(self.kb.db_path))
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS routing_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT,
                routed_kb TEXT,
                actual_kb TEXT,
                correct INTEGER,
                timestamp TEXT
            )
        """)
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        
        c.execute("""
            SELECT routed_kb, actual_kb, correct, COUNT(*) as cnt
            FROM routing_feedback
            WHERE timestamp > ?
            GROUP BY routed_kb, actual_kb, correct
        """, (cutoff,))
        
        rows = c.fetchall()
        conn.close()
        
        if not rows:
            return {"accuracy": None, "total": 0, "message": "暂无反馈数据"}
        
        total = sum(r[3] for r in rows)
        correct = sum(r[3] for r in rows if r[2] == 1)
        
        # 按KB分类统计
        by_kb = {}
        for routed, actual, correct_flag, cnt in rows:
            kb = routed or "unknown"
            if kb not in by_kb:
                by_kb[kb] = {"total": 0, "correct": 0}
            by_kb[kb]["total"] += cnt
            if correct_flag:
                by_kb[kb]["correct"] += cnt
        
        # 计算各KB准确率
        kb_accuracy = {}
        for kb, stats in by_kb.items():
            kb_accuracy[kb] = {
                "accuracy": stats["correct"] / stats["total"] if stats["total"] > 0 else 0,
                "total": stats["total"]
            }
        
        return {
            "accuracy": correct / total if total > 0 else 0,
            "total": total,
            "correct": correct,
            "by_kb": kb_accuracy,
            "period_days": days
        }
    
    def discover_patterns(self):
        """发现跨领域规律"""
        # 读取最近的自反思日志
        iteration_files = sorted(self.iterations_dir.glob("*.json"))
        recent_logs = iteration_files[-5:]  # 最近5次
        
        patterns = []
        
        for log_file in recent_logs:
            try:
                log = json.loads(log_file.read_text(encoding="utf-8"))
                corrections = log.get("corrections", [])
                patterns.extend(corrections)
            except:
                pass
        
        return patterns[:20]  # 返回最近20条
    
    def suggest_improvements(self):
        """基于数据生成改进建议"""
        suggestions = []
        
        # 1. 评估路由准确率
        accuracy = self.evaluate_routing_accuracy(days=7)
        
        if accuracy["total"] > 0:
            if accuracy["accuracy"] < 0.7:
                suggestions.append({
                    "type": "routing",
                    "priority": "high",
                    "issue": f"路由准确率仅{accuracy['accuracy']:.0%}",
                    "action": "检查路由决策表，补充遗漏的触发词"
                })
            
            # 找出准确率最低的KB
            low_accuracy_kbs = [(kb, stats) for kb, stats in accuracy["by_kb"].items() 
                               if stats["accuracy"] < 0.6 and stats["total"] >= 3]
            if low_accuracy_kbs:
                suggestions.append({
                    "type": "routing",
                    "priority": "medium",
                    "issue": f"以下KB路由准确率低: {[kb for kb, _ in low_accuracy_kbs]}",
                    "action": "优化触发词，或用户反馈时手动记录正确答案"
                })
        
        # 2. 检查corrections趋势
        corrections = self.discover_patterns()
        if len(corrections) > 10:
            suggestions.append({
                "type": "pattern",
                "priority": "medium",
                "issue": f"最近有{len(corrections)}条corrections",
                "action": "检查是否有规律可固化到MEMORY.md"
            })
        
        return suggestions
    
    def run_evolution_cycle(self):
        """执行一个完整的迭代周期"""
        print("🧬 开始架构迭代评估...")
        
        # 1. 评估路由准确率
        accuracy = self.evaluate_routing_accuracy()
        print(f"\n📊 路由准确率评估 (最近7天):")
        if accuracy["total"] > 0:
            print(f"   准确率: {accuracy['accuracy']:.1%}")
            print(f"   总反馈: {accuracy['total']}条")
        else:
            print("   暂无反馈数据")
        
        # 2. 生成改进建议
        suggestions = self.suggest_improvements()
        print(f"\n💡 改进建议 ({len(suggestions)}条):")
        for s in suggestions:
            print(f"   [{s['priority']}] {s['issue']}")
            print(f"   → {s['action']}")
        
        # 3. 记录到迭代日志
        evolution_log = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "accuracy": accuracy,
            "suggestions": suggestions,
            "patterns": self.discover_patterns()[:10]
        }
        
        log_file = self.iterations_dir / f"evolution_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
        log_file.parent.mkdir(parents=True, exist_ok=True)
        log_file.write_text(json.dumps(evolution_log, ensure_ascii=False, indent=2), encoding="utf-8")
        
        print(f"\n✅ 迭代报告已保存: {log_file.name}")
        
        return evolution_log


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    
    evo = B166EREvolution()
    
    if len(sys.argv) > 1 and sys.argv[1] == "feedback":
        # 记录反馈
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        routed = sys.argv[3] if len(sys.argv) > 3 else ""
        actual = sys.argv[4] if len(sys.argv) > 4 else ""
        correct = sys.argv[5] == "1" if len(sys.argv) > 5 else False
        evo.log_feedback(query, routed, actual, correct)
        print("反馈已记录")
    else:
        # 执行迭代评估
        evo.run_evolution_cycle()
