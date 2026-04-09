#!/usr/bin/env python3
"""
博弈论决策工具 (Game Theory Decision Tool)
版本: V1.0
创建: 2026-04-03
功能: 博弈论框架的可执行决策工具
"""

import json
import sys
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict
from enum import Enum

# ============================================================
# 核心数据结构
# ============================================================

class InterestLevel(Enum):
    HIGH = "high"
    MEDIUM = "medium"  
    LOW = "low"
    NONE = "none"

@dataclass
class Player:
    name: str
    explicit_interests: List[str]  # 显性利益（钱/权/名）
    implicit_interests: List[str]   # 隐性利益（安全/面子/关系）
    baseline: str                   # 底线利益（必须保住的）
    strength: InterestLevel          # 博弈实力
    urgency: InterestLevel            # 行动紧迫性

@dataclass
class Strategy:
    name: str
    description: str
    for_player: str
    payoff_high: float   # 高结果（最优）
    payoff_mid: float    # 中结果
    payoff_low: float    # 低结果（最差）
    probability_high: float = 0.3
    probability_mid: float = 0.4

@dataclass
class GameTheoryAnalysis:
    situation: str
    players: List[Player]
    strategies: List[Strategy]
    nash_equilibrium: Optional[str] = None
    recommendation: Optional[str] = None
    risk_assessment: Optional[str] = None

# ============================================================
# 博弈分析引擎
# ============================================================

class GameTheoryEngine:
    """博弈论分析引擎"""
    
    def __init__(self):
        self.analyses = []
    
    def add_player(self, name: str, explicit: List[str], 
                   implicit: List[str], baseline: str,
                   strength: str = "medium", urgency: str = "medium") -> Player:
        """添加博弈方"""
        player = Player(
            name=name,
            explicit_interests=explicit,
            implicit_interests=implicit,
            baseline=baseline,
            strength=InterestLevel(strength),
            urgency=InterestLevel(urgency)
        )
        return player
    
    def analyze_nash_equilibrium(self, players: List[Player], 
                                strategies: List[Strategy]) -> Dict:
        """
        分析纳什均衡
        纳什均衡：给定他人策略，没有玩家愿意单方面改变策略的状态
        """
        results = {
            "equilibrium_found": False,
            "equilibrium_strategies": [],
            "reasoning": [],
            "dominant_strategy": None,
            "risky_strategy": None
        }
        
        # 找出每个玩家的最优策略
        for player in players:
            player_strategies = [s for s in strategies if s.for_player == player.name]
            if not player_strategies:
                continue
            
            # 计算期望收益
            for s in player_strategies:
                s.expected_payoff = (
                    s.payoff_high * s.probability_high +
                    s.payoff_mid * s.probability_mid +
                    s.payoff_low * (1 - s.probability_high - s.probability_mid)
                )
            
            # 找最优
            best = max(player_strategies, key=lambda x: x.expected_payoff)
            worst = min(player_strategies, key=lambda x: x.expected_payoff)
            
            results["reasoning"].append(
                f"{player.name}的最优策略: {best.name} "
                f"(期望收益: {best.expected_payoff:.2f})"
            )
            
            # 检查是否占优策略
            all_dominant = all(
                s.expected_payoff <= best.expected_payoff 
                for s in player_strategies
            )
            if all_dominant and len(player_strategies) > 1:
                results["dominant_strategy"] = best.name
                results["equilibrium_strategies"].append(best.name)
                results["equilibrium_found"] = True
        
        return results
    
    def analyze_incentive_compatibility(self, players: List[Player]) -> Dict:
        """
        分析激励相容性
        核心问题：对方有动机按我希望的行动吗？
        """
        results = {
            "compatible": [],
            "incompatible": [],
            "recommendations": []
        }
        
        for player in players:
            # 简单判断：紧急度高 + 底线清晰 = 激励相容
            if player.urgency == InterestLevel.HIGH:
                results["compatible"].append(player.name)
                results["recommendations"].append(
                    f"{player.name}: 紧迫性高，需立即给出明确激励"
                )
            elif player.urgency == InterestLevel.LOW:
                results["incompatible"].append(player.name)
                results["recommendations"].append(
                    f"{player.name}: 紧迫性低，需创造紧迫性或改变激励结构"
                )
        
        return results
    
    def recommend_strategy(self, players: List[Player],
                           nash_results: Dict) -> str:
        """给出策略建议"""
        recommendations = []
        
        # 原则1：找均衡
        if nash_results.get("equilibrium_found"):
            recommendations.append(
                f"✓ 发现均衡点: {', '.join(nash_results['equilibrium_strategies'])}"
            )
        
        # 原则2：避免劣势策略
        if nash_results.get("dominant_strategy"):
            recommendations.append(
                f"✓ {players[0].name}有占优策略: {nash_results['dominant_strategy']}"
            )
        
        # 原则3：考虑对方激励
        inc_results = self.analyze_incentive_compatibility(players)
        if inc_results["compatible"]:
            recommendations.append(
                f"✓ 激励相容: {', '.join(inc_results['compatible'])}"
            )
        
        # 原则4：建立信誉
        recommendations.append(
            "✓ 信誉是长期博弈的最优策略：一次失信永久损失"
        )
        
        return "\n".join(recommendations)
    
    def run_full_analysis(self, situation: str, 
                          players: List[Player],
                          strategies: List[Strategy]) -> GameTheoryAnalysis:
        """运行完整博弈分析"""
        
        print(f"\n{'='*60}")
        print(f"博弈论分析: {situation}")
        print(f"{'='*60}\n")
        
        # Step 1: 玩家识别
        print("【Step 1: 玩家识别】")
        for p in players:
            print(f"  {p.name}:")
            print(f"    显性利益: {', '.join(p.explicit_interests)}")
            print(f"    隐性利益: {', '.join(p.implicit_interests)}")
            print(f"    底线: {p.baseline}")
            print(f"    实力: {p.strength.value} | 紧迫性: {p.urgency.value}")
        print()
        
        # Step 2: 策略映射
        print("【Step 2: 策略映射】")
        for s in strategies:
            exp_payoff = (
                s.payoff_high * s.probability_high +
                s.payoff_mid * s.probability_mid +
                s.payoff_low * (1 - s.probability_high - s.probability_mid)
            )
            print(f"  [{s.for_player}] {s.name}:")
            print(f"    描述: {s.description}")
            print(f"    期望收益: {exp_payoff:.2f}")
        print()
        
        # Step 3: 均衡分析
        print("【Step 3: 均衡分析】")
        nash_results = self.analyze_nash_equilibrium(players, strategies)
        for r in nash_results["reasoning"]:
            print(f"  {r}")
        print()
        
        # Step 4: 激励相容
        print("【Step 4: 激励相容分析】")
        inc_results = self.analyze_incentive_compatibility(players)
        print(f"  相容: {', '.join(inc_results['compatible'])}")
        print(f"  不相容: {', '.join(inc_results['incompatible'])}")
        for rec in inc_results["recommendations"]:
            print(f"  → {rec}")
        print()
        
        # Step 5: 策略建议
        print("【Step 5: 策略建议】")
        recommendation = self.recommend_strategy(players, nash_results)
        for line in recommendation.split('\n'):
            print(f"  {line}")
        print()
        
        # 风险评估
        print("【风险评估】")
        risk_factors = []
        for p in players:
            if p.strength == InterestLevel.HIGH:
                risk_factors.append(f"{p.name}实力强，需警惕")
            if p.urgency == InterestLevel.HIGH:
                risk_factors.append(f"{p.name}紧迫性高，可能随时行动")
        for r in risk_factors:
            print(f"  ⚠ {r}")
        
        return GameTheoryAnalysis(
            situation=situation,
            players=players,
            strategies=strategies,
            nash_equilibrium=str(nash_results),
            recommendation=recommendation
        )

# ============================================================
# 快速决策卡（预设场景）
# ============================================================

QUICK_DECISION_CARDS = {
    "price_war": {
        "name": "价格战决策",
        "description": "竞争对手大幅降价，我该怎么办？",
        "players": [
            {"name": "我方", "explicit": ["市场份额", "利润"], "implicit": ["品牌定位"], "baseline": "保住市场份额"},
            {"name": "竞品", "explicit": ["市场份额", "打压对手"], "implicit": ["行业地位"], "baseline": "不亏本"}
        ],
        "strategies": [
            {"name": "跟进降价", "payoff": [6, 5, 2], "reason": "保住份额但利润下降"},
            {"name": "维持价格，强化非价格竞争", "payoff": [7, 6, 4], "reason": "保护利润但份额可能下滑"},
            {"name": "差异化高端", "payoff": [8, 7, 3], "reason": "高风险高回报"}
        ],
        "recommendation": "不参与价格战，选择差异化竞争"
    },
    
    "investment": {
        "name": "投资决策",
        "description": "大额投资机会，回报不确定",
        "players": [
            {"name": "我方", "explicit": ["资本回报"], "implicit": ["团队信心"], "baseline": "不亏本"},
            {"name": "市场", "explicit": ["趋势"], "implicit": ["周期"], "baseline": "不确定"}
        ],
        "strategies": [
            {"name": "全投", "payoff": [9, 6, 1], "reason": "高风险高回报"},
            {"name": "部分投入", "payoff": [7, 6, 4], "reason": "稳健"},
            {"name": "观望", "payoff": [5, 5, 5], "reason": "零风险但可能错过机会"}
        ],
        "recommendation": "逆向归纳：从终局倒推，部分投入验证假设"
    },
    
    "negotiation": {
        "name": "谈判决策",
        "description": "关键合作谈判，条件分歧大",
        "players": [
            {"name": "我方", "explicit": ["利益最大化"], "implicit": ["关系维护"], "baseline": "保住底线"},
            {"name": "对方", "explicit": ["利益最大化"], "implicit": ["面子"], "baseline": "不失面子"}
        ],
        "strategies": [
            {"name": "强硬", "payoff": [8, 4, 2], "reason": "可能破裂"},
            {"name": "让步", "payoff": [6, 7, 5], "reason": "关系好但利益受损"},
            {"name": "创造新方案", "payoff": [8, 8, 6], "reason": "扩大饼的方案"}
        ],
        "recommendation": "先想'做大蛋糕'的方案，再谈分配"
    }
}

# ============================================================
# 主程序
# ============================================================

def print_banner():
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                  博弈论决策工具 v1.0                         ║
║                  Game Theory Decision Tool                   ║
╠══════════════════════════════════════════════════════════════╣
║  框架: 玩家识别 → 策略映射 → 均衡分析 → 策略建议            ║
║  原则: 纳什均衡 | 激励相容 | 逆向归纳 | 信誉投资             ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def interactive_mode():
    """交互模式"""
    engine = GameTheoryEngine()
    
    print("\n请输入博弈情境描述（简洁）：")
    situation = input("> ").strip() or "一般博弈情境"
    
    # 添加玩家
    players = []
    print("\n【添加博弈方】")
    print("输入 'done' 结束添加\n")
    
    while True:
        name = input("玩家名称 (done/回车结束): ").strip()
        if name.lower() in ['done', '']:
            break
        
        explicit = input("  显性利益（逗号分隔）: ").strip()
        implicit = input("  隐性利益（逗号分隔）: ").strip()
        baseline = input("  底线利益: ").strip()
        
        player = engine.add_player(
            name=name,
            explicit=[x.strip() for x in explicit.split(',') if x.strip()],
            implicit=[x.strip() for x in implicit.split(',') if x.strip()],
            baseline=baseline
        )
        players.append(player)
        print(f"  ✓ 添加 {name}\n")
    
    if not players:
        print("没有添加玩家，退出")
        return
    
    # 添加策略
    strategies = []
    print("\n【添加策略】")
    print("输入 'done' 结束添加\n")
    
    while True:
        player_name = input("策略所属玩家 (done/回车结束): ").strip()
        if player_name.lower() in ['done', '']:
            break
        
        strategy_name = input("  策略名称: ").strip()
        description = input("  策略描述: ").strip()
        
        try:
            ph = float(input("  高结果(0-10): ").strip() or "6")
            pm = float(input("  中结果(0-10): ").strip() or "5")
            pl = float(input("  低结果(0-10): ").strip() or "3")
            prob_h = float(input("  高概率(0-1): ").strip() or "0.3")
            prob_m = float(input("  中概率(0-1): ").strip() or "0.4")
        except ValueError:
            ph, pm, pl = 6, 5, 3
            prob_h, prob_m = 0.3, 0.4
        
        strategy = Strategy(
            name=strategy_name,
            description=description,
            for_player=player_name,
            payoff_high=ph,
            payoff_mid=pm,
            payoff_low=pl,
            probability_high=prob_h,
            probability_mid=prob_m
        )
        strategies.append(strategy)
        print(f"  ✓ 添加策略 [{player_name}] {strategy_name}\n")
    
    # 运行分析
    engine.run_full_analysis(situation, players, strategies)

def quick_mode(card_name: str):
    """快速决策卡模式"""
    if card_name not in QUICK_DECISION_CARDS:
        print(f"可用快速决策卡: {', '.join(QUICK_DECISION_CARDS.keys())}")
        return
    
    card = QUICK_DECISION_CARDS[card_name]
    
    print(f"\n{'='*60}")
    print(f"快速决策卡: {card['name']}")
    print(f"{'='*60}")
    print(f"\n情境: {card['description']}\n")
    
    print("【博弈方】")
    for p in card["players"]:
        print(f"  {p['name']}:")
        print(f"    显性利益: {', '.join(p['explicit'])}")
        print(f"    底线: {p['baseline']}")
    
    print("\n【可选策略】")
    for i, s in enumerate(card["strategies"], 1):
        print(f"  {i}. {s['name']}")
        print(f"     {s['reason']}")
        print(f"     收益: 高={s['payoff'][0]} 中={s['payoff'][1]} 低={s['payoff'][2]}")
    
    print("\n【建议】")
    print(f"  {card['recommendation']}")

def main():
    print_banner()
    
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "quick":
            card = sys.argv[2] if len(sys.argv) > 2 else "price_war"
            quick_mode(card)
        elif command == "list":
            print("\n可用快速决策卡:")
            for key, card in QUICK_DECISION_CARDS.items():
                print(f"  {key}: {card['name']} - {card['description']}")
        elif command == "help":
            print("""
用法:
  python game_theory_tool.py              # 交互模式
  python game_theory_tool.py quick [卡名] # 快速决策卡
  python game_theory_tool.py list        # 列出所有快速决策卡
  python game_theory_tool.py help        # 显示帮助

快速决策卡:
  price_war   - 价格战决策
  investment  - 投资决策  
  negotiation - 谈判决策
            """)
        else:
            print(f"未知命令: {command}")
            print("使用 'python game_theory_tool.py help' 查看帮助")
    else:
        interactive_mode()

if __name__ == "__main__":
    main()
