#!/usr/bin/env python3
"""
元认知工具 (Metacognition Tool)
版本: V1.0
创建: 2026-04-03
功能: 递归知识与元认知的实践操作工具
"""

import json
import sys
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

# ============================================================
# 核心数据结构
# ============================================================

@dataclass
class KnowledgePiece:
    """知识碎片"""
    domain: str              # 领域（审美/博弈/酒店/AI...）
    concept: str              # 核心概念
    principle: str            # 核心原则
    application: str          # 应用场景
    source: str               # 来源（经验/学习/教训）
    confidence: float         # 置信度 (0-1)
    last_validated: str       # 最后验证时间
    validation_count: int     # 验证次数
    
@dataclass
class ReflectionEntry:
    """反思条目"""
    timestamp: str
    situation: str            # 情境
    action_taken: str          # 采取的行动
    expected_outcome: str      # 预期结果
    actual_outcome: str         # 实际结果
    gap_analysis: str          # 差距分析
    lesson: str                # 教训/规律
    applicable_to: List[str]   # 可迁移的场景

# ============================================================
# 元认知引擎
# ============================================================

class MetacognitionEngine:
    """元认知引擎"""
    
    def __init__(self):
        self.knowledge_base: List[KnowledgePiece] = []
        self.reflection_log: List[ReflectionEntry] = []
        self.insight_index: Dict[str, List[str]] = {}  # 概念 -> 知识碎片ID
    
    def add_knowledge(self, domain: str, concept: str, principle: str,
                      application: str, source: str = "经验",
                      confidence: float = 0.7) -> KnowledgePiece:
        """添加知识碎片"""
        piece = KnowledgePiece(
            domain=domain,
            concept=concept,
            principle=principle,
            application=application,
            source=source,
            confidence=confidence,
            last_validated=datetime.now().strftime("%Y-%m-%d"),
            validation_count=1 if source == "经验" else 0
        )
        self.knowledge_base.append(piece)
        
        # 更新索引
        key = f"{domain}:{concept}"
        if key not in self.insight_index:
            self.insight_index[key] = []
        self.insight_index[key].append(concept)
        
        return piece
    
    def validate_knowledge(self, concept: str, success: bool) -> None:
        """验证知识碎片"""
        for piece in self.knowledge_base:
            if piece.concept == concept:
                piece.validation_count += 1
                if success and piece.confidence < 0.95:
                    piece.confidence = min(0.95, piece.confidence + 0.05)
                elif not success and piece.confidence > 0.3:
                    piece.confidence = max(0.3, piece.confidence - 0.1)
                piece.last_validated = datetime.now().strftime("%Y-%m-%d")
    
    def add_reflection(self, situation: str, action: str,
                      expected: str, actual: str,
                      lesson: str, applicable: List[str]) -> ReflectionEntry:
        """添加反思条目"""
        entry = ReflectionEntry(
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"),
            situation=situation,
            action_taken=action,
            expected_outcome=expected,
            actual_outcome=actual,
            gap_analysis=self._analyze_gap(expected, actual),
            lesson=lesson,
            applicable_to=applicable
        )
        self.reflection_log.append(entry)
        return entry
    
    def _analyze_gap(self, expected: str, actual: str) -> str:
        """分析预期与实际的差距"""
        if expected == actual:
            return "完全符合预期"
        
        # 简单分析
        if len(actual) > len(expected) * 1.5:
            return "实际结果超出预期（好或过度）"
        elif len(actual) < len(expected) * 0.5:
            return "实际结果低于预期"
        else:
            return "实际结果与预期有偏差"
    
    def query_knowledge(self, domain: str = None, 
                       concept: str = None) -> List[KnowledgePiece]:
        """查询知识库"""
        results = self.knowledge_base
        
        if domain:
            results = [k for k in results if k.domain == domain]
        if concept:
            results = [k for k in results if concept.lower() in k.concept.lower()]
        
        # 按置信度排序
        return sorted(results, key=lambda x: x.confidence, reverse=True)
    
    def get_insights(self, situation: str) -> List[str]:
        """从知识库中获取与情境相关的洞见"""
        insights = []
        situation_lower = situation.lower()
        
        for piece in self.knowledge_base:
            # 检查领域关键词
            if piece.domain.lower() in situation_lower:
                insights.append(f"[{piece.domain}] {piece.concept}: {piece.principle}")
            # 检查概念
            if piece.concept.lower() in situation_lower:
                insights.append(f"[{piece.concept}] {piece.principle}")
        
        return list(set(insights))  # 去重
    
    def daily_review_prompt(self) -> str:
        """生成每日复盘提示"""
        prompt = f"""
╔══════════════════════════════════════════════════════════════╗
║                    每日元认知复盘                           ║
║                    {datetime.now().strftime('%Y-%m-%d')}                            ║
╚══════════════════════════════════════════════════════════════╝

【今日最高点】
  今天最有成就感的一件事是什么？
  为什么它成功了？
  背后的规律是什么？

  ____________________________________________________________

【今日最低点】
  今天最困难或最遗憾的一件事是什么？
  预期和实际的差距在哪里？
  根本原因是什么？

  ____________________________________________________________

【认知升级】
  今天学到了什么新认知？
  它如何改变了我对某件事的理解？
  这个认知可以迁移到哪些场景？

  ____________________________________________________________

【明日行动】
  基于今天的认知，明日我要：
  1. 开始做：_______________
  2. 停止做：_______________
  3. 继续做：_______________

  ____________________________________________________________

【知识验证】
  之前学到的哪个认知今天得到了验证？
  之前学到的哪个认知今天被推翻或修正了？

"""
        return prompt
    
    def decision_checklist(self, situation: str) -> str:
        """决策前检查清单"""
        
        # 获取相关洞见
        insights = self.get_insights(situation)
        
        checklist = f"""
╔══════════════════════════════════════════════════════════════╗
║                    决策前元认知检查                          ║
╚══════════════════════════════════════════════════════════════╝

情境: {situation}

【历史经验检索】
相关洞见:
"""
        for i, insight in enumerate(insights[:5], 1):
            checklist += f"\n  {i}. {insight}"
        
        checklist += """

【决策检查清单】
□ 我是否理解了这件事的底层逻辑？
□ 我的判断是基于事实还是情绪？
□ 我在重复过去的成功经验吗？
□ 我在避免重蹈覆辙吗？
□ 如果失败了，我能承受吗？
□ 有没有我遗漏的关键变量？

【逆向归纳检查】
□ 我从终局倒推了吗？
□ 如果对方是我，他会怎么行动？
□ 三年后回看，这个决策还正确吗？

"""
        return checklist
    
    def knowledge_decay_report(self) -> Dict:
        """知识失效检测报告"""
        today = datetime.now()
        stale_knowledge = []
        
        for piece in self.knowledge_base:
            if piece.source == "学习" and piece.confidence < 0.6:
                stale_knowledge.append({
                    "concept": piece.concept,
                    "domain": piece.domain,
                    "confidence": piece.confidence,
                    "issue": "低置信度，需要实践验证"
                })
            elif piece.validation_count > 0 and piece.confidence < 0.5:
                stale_knowledge.append({
                    "concept": piece.concept,
                    "domain": piece.domain,
                    "confidence": piece.confidence,
                    "issue": "验证次数多但置信度低，可能需要修正"
                })
        
        return {
            "stale_count": len(stale_knowledge),
            "stale_items": stale_knowledge,
            "total_knowledge": len(self.knowledge_base),
            "healthy_count": len(self.knowledge_base) - len(stale_knowledge)
        }

# ============================================================
# 预设知识库（核心认知）
# ============================================================

PRESET_KNOWLEDGE = [
    {
        "domain": "审美",
        "concept": "气韵优先原则",
        "principle": "有气韵者，必有意境，有形式，有生命。气韵是审美判断的最高标准。",
        "application": "所有审美判断：设计/艺术/空间/音乐/服装..."
    },
    {
        "domain": "博弈",
        "concept": "信誉是长期博弈的最优策略",
        "principle": "一次失信永久损失。长期重复博弈中，信誉是核心资产。",
        "application": "所有需要信任的场景：商业谈判/合作/承诺..."
    },
    {
        "domain": "博弈",
        "concept": "逆向归纳",
        "principle": "从终局倒推起点。先想结果，再找路径。",
        "application": "所有复杂决策：创业/投资/职业规划..."
    },
    {
        "domain": "认知",
        "concept": "知其然而知其所以然",
        "principle": "理解底层逻辑（历史/原因/未来/原理），不碎片化认知。",
        "application": "所有学习和执行任务"
    },
    {
        "domain": "认知",
        "concept": "格式塔原则",
        "principle": "先看整体，再看细节。整体大于部分之和。",
        "application": "审美判断/问题分析/系统设计..."
    }
]

# ============================================================
# 主程序
# ============================================================

def print_banner():
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                  元认知工具 v1.0                              ║
║                  Metacognition Tool                          ║
╠══════════════════════════════════════════════════════════════╣
║  功能: 知识管理 | 反思记录 | 决策检查 | 认知复盘            ║
║  原则: 递归认知 | 验证迭代 | 知行合一                        ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def interactive_review(engine: MetacognitionEngine):
    """交互式每日复盘"""
    print(engine.daily_review_prompt())
    
    print("\n【输入你的复盘】（直接回车跳过该问题）\n")
    
    high = input("今日最高点: ").strip()
    low = input("今日最低点: ").strip()
    new_knowledge = input("认知升级: ").strip()
    
    action_start = input("明日开始做: ").strip()
    action_stop = input("明日停止做: ").strip()
    action_continue = input("明日继续做: ").strip()
    
    # 保存反思
    if high or low or new_knowledge:
        entry = engine.add_reflection(
            situation="每日复盘",
            action_taken=action_continue if action_continue else "待记录",
            expected=high if high else "待定义",
            actual=low if low else "待记录",
            lesson=new_knowledge if new_knowledge else "待提炼",
            applicable=[]
        )
        print(f"\n✓ 反思已保存: {entry.timestamp}")
    
    # 添加新认知
    if new_knowledge:
        domain = input("这个认知属于哪个领域（审美/博弈/认知/酒店/其他）: ").strip() or "认知"
        piece = engine.add_knowledge(
            domain=domain,
            concept=new_knowledge[:50],
            principle=new_knowledge,
            application="待定义",
            source="反思"
        )
        print(f"✓ 知识碎片已添加: {piece.concept}")

def decision_check(engine: MetacognitionEngine):
    """决策前检查"""
    print("\n请描述你面临的情境（回车使用默认）:")
    print("> ", end="")
    situation = input().strip() or "一般决策情境"
    
    print(engine.decision_checklist(situation))
    
    # 记录决策
    decision = input("\n你的决策是: ").strip()
    if decision:
        print(f"\n✓ 决策已记录: {decision}")
        print("  建议后续复盘时验证决策效果")

def knowledge_query(engine: MetacognitionEngine):
    """知识库查询"""
    print("\n查询知识库")
    print("-" * 40)
    
    domain = input("领域（回车显示全部）: ").strip()
    concept = input("关键词（回车跳过）: ").strip()
    
    results = engine.query_knowledge(domain if domain else None,
                                     concept if concept else None)
    
    if not results:
        print("没有找到匹配的知识碎片")
        return
    
    print(f"\n找到 {len(results)} 条知识碎片:\n")
    for i, piece in enumerate(results, 1):
        print(f"{i}. [{piece.domain}] {piece.concept}")
        print(f"   原则: {piece.principle}")
        print(f"   置信度: {piece.confidence:.0%} | 验证: {piece.validation_count}次")
        print(f"   上次验证: {piece.last_validated}")
        print()

def init_preset_knowledge(engine: MetacognitionEngine):
    """初始化预设知识"""
    for k in PRESET_KNOWLEDGE:
        engine.add_knowledge(
            domain=k["domain"],
            concept=k["concept"],
            principle=k["principle"],
            application=k["application"],
            source="内化",
            confidence=0.85
        )
    print(f"✓ 已加载 {len(PRESET_KNOWLEDGE)} 条核心认知")

def main():
    print_banner()
    
    # 创建引擎（带预设知识）
    engine = MetacognitionEngine()
    init_preset_knowledge(engine)
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "review":
            interactive_review(engine)
        elif command == "check":
            decision_check(engine)
        elif command == "query":
            knowledge_query(engine)
        elif command == "list":
            knowledge_query(engine)
        elif command == "report":
            report = engine.knowledge_decay_report()
            print(f"""
╔══════════════════════════════════════════════════════════════╗
║                    知识健康报告                              ║
╚══════════════════════════════════════════════════════════════╝
总知识数: {report['total_knowledge']}
健康知识: {report['healthy_count']}
需关注: {report['stale_count']}
""")
            if report['stale_items']:
                print("需关注项:")
                for item in report['stale_items']:
                    print(f"  - {item['concept']}: {item['issue']}")
        elif command == "help":
            print("""
用法:
  python metacognition_tool.py              # 交互式复盘
  python metacognition_tool.py review       # 每日复盘
  python metacognition_tool.py check        # 决策前检查
  python metacognition_tool.py query        # 查询知识库
  python metacognition_tool.py list         # 列出知识库
  python metacognition_tool.py report       # 知识健康报告
  python metacognition_tool.py help         # 显示帮助
            """)
        else:
            print(f"未知命令: {command}")
    else:
        print("\n请选择操作:")
        print("1. 每日复盘 (review)")
        print("2. 决策前检查 (check)")
        print("3. 查询知识库 (query)")
        print("4. 知识健康报告 (report)")
        print()
        
        choice = input("选择 (1-4): ").strip()
        
        if choice == "1":
            interactive_review(engine)
        elif choice == "2":
            decision_check(engine)
        elif choice == "3":
            knowledge_query(engine)
        elif choice == "4":
            report = engine.knowledge_decay_report()
            print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
