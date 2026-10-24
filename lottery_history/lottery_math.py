"""
B166ER 博彩数学武器库 V1.0
═══════════════════════════════════════════
凯利公式 / 泊松分布 / Elo评级 / 破产定理 / 反谬误护栏

参考: Kelly(1956), Poisson(1837), Elo(1960)
用途: 资金管理 / 概率建模 / 风险控制 / 认知纠偏
═══════════════════════════════════════════
"""
import math
import json
import os
import csv
from typing import Tuple, Optional
from dataclasses import dataclass, field

# ═══════════════════════════════════════════
#  一、凯利公式 (Kelly Criterion)
# ═══════════════════════════════════════════

@dataclass
class KellyResult:
    """凯利公式计算结果"""
    f_star: float          # 理论最优下注比例
    f_half: float          # 半凯利 (Half-Kelly)
    f_quarter: float       # 四分之一凯利
    is_positive_ev: bool   # 是否正期望值
    expected_value: float  # 期望收益
    recommendation: str    # 建议


def kelly_criterion(p: float, b: float, mode: str = 'half') -> KellyResult:
    """
    凯利公式: 计算最优下注比例

    参数:
        p: 预估胜率 (0~1)
        b: 净赔率 (投1元赢b元，即总回报=1+b)
           例: 赔率2.5 → b=1.5, 赔率5.0 → b=4.0
        mode: 'full' | 'half' | 'quarter' (默认半凯利，风险缓冲)

    公式: f* = (bp - q) / b = (p(b+1) - 1) / b

    返回: KellyResult

    ⚠️ 前提: p必须尽可能精准。高估p会导致资金快速缩水。
    """
    if not 0 < p < 1:
        raise ValueError(f'胜率p必须在(0,1)之间，收到: {p}')
    if b <= 0:
        raise ValueError(f'净赔率b必须>0，收到: {b}')

    q = 1 - p
    f_star = (b * p - q) / b

    # 期望值
    ev = p * b - q * 1

    # 凯利公式关键判定
    if f_star <= 0:
        return KellyResult(
            f_star=0.0,
            f_half=0.0,
            f_quarter=0.0,
            is_positive_ev=False,
            expected_value=round(ev, 4),
            recommendation='❌ 无价值投注 — 期望值为负，不下注',
        )

    # 实际应用中采用分数凯利
    f_half = f_star / 2
    f_quarter = f_star / 4
    final_f = {'full': f_star, 'half': f_half, 'quarter': f_quarter}[mode]

    # 建议文案
    if final_f <= 0.01:
        rec = f'🟢 小注 (下注 {final_f*100:.1f}% 资金)'
    elif final_f <= 0.05:
        rec = f'🟡 中注 (下注 {final_f*100:.1f}% 资金)'
    elif final_f <= 0.10:
        rec = f'🟠 重注 (下注 {final_f*100:.1f}% 资金) — 谨慎'
    else:
        rec = f'🔴 极重注 ({final_f*100:.1f}%) — 建议降为半凯利 {f_half*100:.1f}%'

    return KellyResult(
        f_star=round(f_star, 6),
        f_half=round(f_half, 6),
        f_quarter=round(f_quarter, 6),
        is_positive_ev=True,
        expected_value=round(ev, 4),
        recommendation=rec,
    )


def kelly_bet_size(bankroll: float, p: float, odds: float, mode: str = 'half') -> Tuple[float, KellyResult]:
    """
    计算具体下注金额

    参数:
        bankroll: 总资金
        p: 预估胜率
        odds: 欧洲赔率 (如 2.5 表示投1中2.5)

    返回: (下注金额, KellyResult)
    """
    b = odds - 1.0  # 转换为净赔率
    result = kelly_criterion(p, b, mode)
    final_f = {'full': result.f_star, 'half': result.f_half, 'quarter': result.f_quarter}[mode]
    return round(bankroll * final_f, 2), result


# ═══════════════════════════════════════════
#  二、泊松分布 (Poisson Distribution)
# ═══════════════════════════════════════════

def poisson_probability(k: int, lam: float) -> float:
    """
    泊松分布: P(X=k) = (λ^k * e^(-λ)) / k!

    参数:
        k: 事件发生次数 (如进球数)
        lam: 期望发生率 (λ = 预期进球数)

    返回: 恰好发生k次的概率
    """
    if lam < 0:
        raise ValueError(f'λ不能为负: {lam}')
    if k < 0:
        return 0.0
    if lam == 0:
        return 1.0 if k == 0 else 0.0

    return (lam ** k * math.exp(-lam)) / math.factorial(k)


@dataclass
class MatchPrediction:
    """比赛预测结果"""
    home_goals_lambda: float
    away_goals_lambda: float
    home_win_prob: float
    draw_prob: float
    away_win_prob: float
    score_probs: list[dict]  # 各比分的概率
    most_likely_score: str
    over_under_25: dict     # 大小球2.5概率


def predict_match(home_lambda: float, away_lambda: float,
                  max_goals: int = 6) -> MatchPrediction:
    """
    基于泊松分布预测足球比赛

    参数:
        home_lambda: 主队预期进球数
        away_lambda: 客队预期进球数
        max_goals: 单队最大进球数限制

    计算流程:
    1. 对所有可能的比分(i:j)计算联合概率 P(i)*P(j)
    2. 汇总胜/平/负概率
    3. 找最大概率比分
    """
    score_probs = []
    home_win = draw = away_win = 0.0
    over = under = 0.0

    for i in range(max_goals + 1):
        p_home = poisson_probability(i, home_lambda)
        if p_home < 1e-8:
            continue
        for j in range(max_goals + 1):
            p_away = poisson_probability(j, away_lambda)
            if p_away < 1e-8:
                continue
            joint = p_home * p_away
            if joint < 1e-8:
                continue

            score_probs.append({
                'score': f'{i}:{j}',
                'probability': round(joint * 100, 4),
            })

            if i > j:
                home_win += joint
            elif i == j:
                draw += joint
            else:
                away_win += joint

            if i + j > 2.5:
                over += joint
            else:
                under += joint

    # 排序
    score_probs.sort(key=lambda x: -x['probability'])

    return MatchPrediction(
        home_goals_lambda=round(home_lambda, 2),
        away_goals_lambda=round(away_lambda, 2),
        home_win_prob=round(home_win * 100, 2),
        draw_prob=round(draw * 100, 2),
        away_win_prob=round(away_win * 100, 2),
        score_probs=score_probs[:10],
        most_likely_score=score_probs[0]['score'] if score_probs else 'N/A',
        over_under_25={
            'over': round(over * 100, 2),
            'under': round(under * 100, 2),
        },
    )


def find_value_bet(match: MatchPrediction, home_odds: float,
                   draw_odds: float, away_odds: float) -> dict:
    """
    对比泊松模型概率与博彩公司赔率，寻找价值投注

    返回: {'home': KellyResult, 'draw': KellyResult, 'away': KellyResult}
    """
    # 赔率隐含概率 (含抽水)
    implied = {
        'home': 1.0 / home_odds,
        'draw': 1.0 / draw_odds,
        'away': 1.0 / away_odds,
    }

    # 去抽水 (假设均匀分布)
    overround = sum(implied.values())
    fair_implied = {k: v / overround for k, v in implied.items()}

    # 模型概率
    model_prob = {
        'home': match.home_win_prob / 100,
        'draw': match.draw_prob / 100,
        'away': match.away_win_prob / 100,
    }

    results = {}
    for outcome in ['home', 'draw', 'away']:
        odds = {'home': home_odds, 'draw': draw_odds, 'away': away_odds}[outcome]
        b = odds - 1.0
        p = model_prob[outcome]

        try:
            kr = kelly_criterion(p, b, 'half')
        except ValueError:
            kr = KellyResult(0, 0, 0, False, 0, '无效')

        results[outcome] = {
            'model_prob': round(p * 100, 2),
            'implied_prob': round(fair_implied[outcome] * 100, 2),
            'odds': odds,
            'edge': round((p - fair_implied[outcome]) * 100, 2),
            'kelly': kr,
        }

    return results


# ═══════════════════════════════════════════
#  三、Elo 评级系统
# ═══════════════════════════════════════════

class EloSystem:
    """
    Elo 评级系统
    用于足球/篮球/电竞等对抗性赛事的动态实力评估

    核心逻辑:
    - 初始分: 1500
    - 预期得分: E_A = 1 / (1 + 10^((R_B - R_A) / 400))
    - 更新: R'_A = R_A + K * (S_A - E_A)
    """

    def __init__(self, k_factor: float = 32, initial_rating: float = 1500):
        """
        参数:
            k_factor: K值，决定积分变化速度
                - K=32: 标准 (国际象棋)
                - K=20: 低波动 (成熟联赛)
                - K=40: 高波动 (新队伍/快节奏)
            initial_rating: 初始积分
        """
        self.K = k_factor
        self.initial = initial_rating
        self.ratings: dict[str, float] = {}

    def get_rating(self, team: str) -> float:
        """获取队伍当前积分，不存在则返回初始分"""
        return self.ratings.get(team, self.initial)

    def expected_score(self, team_a: str, team_b: str) -> float:
        """
        计算A对B的预期得分 (0~1)
        E_A = 1 / (1 + 10^((R_B - R_A) / 400))
        """
        ra = self.get_rating(team_a)
        rb = self.get_rating(team_b)
        return 1.0 / (1.0 + 10 ** ((rb - ra) / 400))

    def update(self, team_a: str, team_b: str, score_a: float):
        """
        更新两队积分

        参数:
            score_a: A的实际得分 (1=胜, 0.5=平, 0=负)
        """
        ra = self.get_rating(team_a)
        rb = self.get_rating(team_b)
        ea = self.expected_score(team_a, team_b)

        # 更新
        new_ra = ra + self.K * (score_a - ea)
        new_rb = rb + self.K * ((1 - score_a) - (1 - ea))

        self.ratings[team_a] = round(new_ra, 1)
        self.ratings[team_b] = round(new_rb, 1)

        return {
            'team_a': {'old': ra, 'new': new_ra, 'delta': round(new_ra - ra, 1)},
            'team_b': {'old': rb, 'new': new_rb, 'delta': round(new_rb - rb, 1)},
        }

    def win_probability(self, team_a: str, team_b: str) -> dict:
        """
        基于Elo分差计算胜平负概率

        简化公式 (常用于足彩):
        - 胜率 ≈ E_A * (1 - draw_rate)
        - 平率 ≈ draw_rate
        - 负率 ≈ (1 - E_A) * (1 - draw_rate)

        draw_rate经验公式: DR = 0.28 - 0.02 * |R_A - R_B|/100
        """
        ea = self.expected_score(team_a, team_b)
        diff = abs(self.get_rating(team_a) - self.get_rating(team_b))
        draw_rate = max(0.15, 0.30 - 0.025 * diff / 100)

        return {
            'home_win': round(ea * (1 - draw_rate) * 100, 2),
            'draw': round(draw_rate * 100, 2),
            'away_win': round((1 - ea) * (1 - draw_rate) * 100, 2),
            'rating_diff': round(self.get_rating(team_a) - self.get_rating(team_b), 1),
        }

    def to_dict(self) -> dict:
        return {
            'K': self.K,
            'initial': self.initial,
            'teams': dict(sorted(self.ratings.items(), key=lambda x: -x[1])),
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'EloSystem':
        elo = cls(data.get('K', 32), data.get('initial', 1500))
        elo.ratings = data.get('teams', {})
        return elo


# ═══════════════════════════════════════════
#  四、赌徒破产定理 (Gambler's Ruin)
# ═══════════════════════════════════════════

def gamblers_ruin_probability(bankroll: float, target: float, win_prob: float) -> float:
    """
    赌徒破产概率

    场景: 有限资金 vs 无限资金庄家, 胜率p<0.5
    结论: 长期必破产

    公式 (公平博弈 p=0.5): P_ruin = 1 - bankroll/target
    公式 (偏博弈 p≠0.5): P_ruin = ((q/p)^bankroll - (q/p)^target) / (1 - (q/p)^target)
                         简化: 当 target→∞ 且 p<0.5 时, P_ruin = 1 (100%破产)

    参数:
        bankroll: 当前资金
        target: 目标资金
        win_prob: 单局胜率
    """
    if bankroll <= 0:
        return 1.0
    if bankroll >= target:
        return 0.0

    if abs(win_prob - 0.5) < 1e-10:
        return 1.0 - bankroll / target

    q = 1 - win_prob
    ratio = q / win_prob

    if ratio == 1:
        return 1.0 - bankroll / target

    # 完整公式
    try:
        p_ruin = (ratio ** bankroll - ratio ** target) / (1 - ratio ** target)
        return min(max(p_ruin, 0), 1)
    except OverflowError:
        return 1.0 if win_prob < 0.5 else 0.0


def ruin_simulation(bankroll: float, bet_size: float, win_prob: float,
                    n_sims: int = 10000) -> dict:
    """
    蒙特卡洛模拟破产风险

    返回: 破产概率, 预期存活回合数, 中位最终资金
    """
    import random

    ruins = 0
    final_balances = []

    for _ in range(n_sims):
        bal = bankroll
        rounds = 0
        while bal > 0 and rounds < 10000:
            if random.random() < win_prob:
                bal += bet_size
            else:
                bal -= bet_size
            rounds += 1

        if bal <= 0:
            ruins += 1
        final_balances.append(bal)

    final_balances.sort()
    return {
        'ruin_probability': round(ruins / n_sims * 100, 2),
        'median_final': round(final_balances[n_sims // 2], 2),
        'n_simulations': n_sims,
        'verdict': ('⚠️ 大概率破产' if ruins / n_sims > 0.5
                    else '🟡 有风险' if ruins / n_sims > 0.1
                    else '🟢 相对安全'),
    }


# ═══════════════════════════════════════════
#  五、反谬误护栏 (Anti-Fallacy Guardrails)
# ═══════════════════════════════════════════

class FallacyDetector:
    """
    检测并标记博彩推理中的认知谬误

    ⛔ 检测的谬误类型:
    1. 赌徒谬误: "X很久没出了,下次必出" → 每期独立随机
    2. 热手谬误: "X连出3期了,还会出" → 同上
    3. 马丁格尔倾向: "输了就加注翻本" → 指数爆炸,必破产
    4. 近因偏差: 过度加权最近几期的模式
    """

    @staticmethod
    def is_gamblers_fallacy(reasoning: str) -> bool:
        """检测赌徒谬误关键词"""
        triggers = [
            '该出', '必出', '一定会出', '肯定有',
            '太久没出', '冷号回补', '该出了',
            '连续不开', '概率增加了', '概率更大',
            '已经X期没出', '不可能再不出',
        ]
        return any(t in reasoning for t in triggers)

    @staticmethod
    def is_hot_hand_fallacy(reasoning: str) -> bool:
        """检测热手谬误关键词"""
        triggers = [
            '手气好', '连中', '势头', '旺',
            '继续出', '追热', '趁热',
        ]
        return any(t in reasoning for t in triggers)

    @staticmethod
    def is_martingale(reasoning: str) -> bool:
        """检测马丁格尔/倍投策略"""
        triggers = [
            '倍投', '翻倍', '加倍下注', '输了加注',
            '马丁格尔', 'martingale', '追回来',
            '一把赢回来',
        ]
        return any(t in reasoning.lower() for t in triggers)

    @staticmethod
    def audit_text(text: str) -> list[str]:
        """全面审计一段文本的谬误"""
        warnings = []
        if FallacyDetector.is_gamblers_fallacy(text):
            warnings.append('⚠️ 赌徒谬误: 独立随机事件不受历史影响')
        if FallacyDetector.is_hot_hand_fallacy(text):
            warnings.append('⚠️ 热手谬误: 过去的成功不增加未来的概率')
        if FallacyDetector.is_martingale(text):
            warnings.append('🚫 马丁格尔策略: 必破产, 绝对禁止')
        return warnings

    @staticmethod
    def correction_text() -> str:
        """标准纠偏声明"""
        return (
            '⚠️ 概率声明: 彩票/博彩的每一期/每一局都是独立随机事件。'
            '历史数据可用于识别机械偏倚(如球重不均), 但不能作为'
            '"该出了"的论据。大数定律保证的是长期频率趋近概率, '
            '不是短期必然回归。'
        )


# ═══════════════════════════════════════════
#  六、马尔可夫链状态分析 (Markov Chain)
# ═══════════════════════════════════════════

def markov_steady_state(transition_matrix: list[list[float]],
                        steps: int = 1000) -> list[float]:
    """
    计算马尔可夫链的稳态分布

    用于: 分析球队状态转移 (如 胜→胜, 胜→平, 胜→负 的概率)

    参数:
        transition_matrix: n×n 转移概率矩阵
        steps: 迭代步数
    """
    n = len(transition_matrix)
    # 从均匀分布开始
    state = [1.0 / n] * n

    for _ in range(steps):
        new_state = [0.0] * n
        for i in range(n):
            for j in range(n):
                new_state[j] += state[i] * transition_matrix[i][j]
        state = new_state

    return [round(s, 6) for s in state]


# ═══════════════════════════════════════════
#  七、约束过滤器 (Constraint Filter)
# ═══════════════════════════════════════════

@dataclass
class ConstraintCheck:
    passes: bool
    checks: dict
    violations: list[str]


def validate_combination(numbers: list[int], pool_size: int,
                         count: int, history_sums: list[float] | None = None) -> ConstraintCheck:
    """验证号码组合是否符合统计约束: 和值/奇偶/区间/连号"""
    violations = []
    nums = sorted(numbers)
    total = sum(nums)

    # 和值
    if history_sums and len(history_sums) > 0:
        import statistics
        h_sorted = sorted(history_sums)
        p05 = h_sorted[max(0, int(len(h_sorted) * 0.05))]
        p95 = h_sorted[min(len(h_sorted) - 1, int(len(h_sorted) * 0.95))]
        sum_ok = p05 <= total <= p95
    else:
        sum_ok = True
    if not sum_ok:
        violations.append(f'和值{total}超出范围')

    # 奇偶比
    odds = sum(1 for n in nums if n % 2 == 1)
    oe_ok = odds not in (0, count)
    if not oe_ok:
        violations.append(f'奇偶极端{odds}:{count-odds}')

    # 区间
    zs = pool_size // 3
    zones = [sum(1 for n in nums if n <= zs),
             sum(1 for n in nums if zs < n <= zs * 2),
             sum(1 for n in nums if n > zs * 2)]
    zone_ok = max(zones) < count - 1
    if not zone_ok:
        violations.append(f'区间极端{zones}')

    return ConstraintCheck(
        passes=sum_ok and oe_ok and zone_ok,
        checks={'sum': total, 'odds': odds, 'zones': zones},
        violations=violations,
    )


# ═══════════════════════════════════════════
#  八、轮转覆盖 (Wheeling System)
# ═══════════════════════════════════════════

def generate_wheel(key_numbers: list[int], pick_count: int,
                   guarantee: int = 3) -> list[list[int]]:
    """轮转覆盖: 若key_numbers含guarantee个中奖号, 保证至少一注覆盖"""
    from itertools import combinations

    if len(key_numbers) < pick_count:
        return []

    all_subsets = {frozenset(s) for s in combinations(key_numbers, guarantee)}
    all_combos = list(combinations(key_numbers, pick_count))

    covered = set()
    selected = []
    for _ in range(50):
        best, best_new = None, 0
        for combo in all_combos:
            n = sum(1 for s in combinations(combo, guarantee)
                    if frozenset(s) in all_subsets and frozenset(s) not in covered)
            if n > best_new:
                best_new, best = n, combo
        if best is None or best_new == 0:
            break
        selected.append(list(best))
        for s in combinations(best, guarantee):
            covered.add(frozenset(s))
    return selected


# ═══════════════════════════════════════════
#  九、反共识过滤器 (Anti-Consensus)
# ═══════════════════════════════════════════

BIRTHDAY_RANGE = set(range(1, 32))
BIRTHDAY_HOT = {6, 8, 16, 18, 28}


def consensus_score(numbers: list[int]) -> float:
    """共识度 0~1 (越高越大众, 中奖后分钱越多)"""
    birthday_r = sum(1 for n in numbers if n in BIRTHDAY_RANGE) / len(numbers)
    lucky = min(sum(1 for n in numbers if n in BIRTHDAY_HOT) / len(numbers), 0.5)
    return min(birthday_r * 0.5 + lucky * 0.5, 1.0)


def diversify_anti_consensus(combos: list[tuple[list[int], list[int]]], top_k: int = 5) -> list[list[int]]:
    """选出最反共识的组合 (combos: [(front, back), ...])"""
    scored = []
    for combo in combos:
        if isinstance(combo, tuple):
            front, _ = combo
        else:
            front = combo
        scored.append((combo, consensus_score(front)))
    scored.sort(key=lambda x: x[1])
    return [c for c, _ in scored[:top_k]]


# ═══════════════════════════════════════════
#  十、回测框架
# ═══════════════════════════════════════════

@dataclass
class BacktestResult:
    total_trials: int
    avg_front_hits: float
    avg_back_hits: float
    random_baseline: float
    better_than_random: bool


def backtest_strategy(lottery_type: str, n_trials: int = 20,
                      train_window: int = 50) -> BacktestResult | None:
    """滑动窗口回测: 策略 vs 随机基线"""
    import random

    RULES = {
        'dlt': {'front_pool': 35, 'front_count': 5, 'back_pool': 12, 'back_count': 2},
        'ssq': {'front_pool': 33, 'front_count': 6, 'back_pool': 16, 'back_count': 1},
    }
    rule = RULES[lottery_type]
    csv_path = os.path.join(os.path.dirname(__file__),
                            'dlt_history.csv' if lottery_type == 'dlt' else 'ssq_history.csv')
    if not os.path.exists(csv_path):
        return None

    with open(csv_path, 'r', encoding='utf-8') as f:
        history = list(csv.DictReader(f))

    if len(history) < train_window + n_trials + 5:
        return None

    front_hits_all, back_hits_all = [], []
    total = len(history)

    for i in range(n_trials):
        test_idx = total - n_trials + i
        train = history[:test_idx]
        test = history[test_idx]

        # 提取实际号码
        if lottery_type == 'dlt':
            actual_front = sorted(int(test[f'front_{j}']) for j in range(1, 6))
            actual_back = sorted(int(test[f'back_{j}']) for j in range(1, 3))
        else:
            actual_front = sorted(int(test[f'r{j}']) for j in range(1, 7))
            actual_back = [int(test['b1'])]

        # 从训练集统计热号
        from collections import Counter
        front_cnt = Counter()
        back_cnt = Counter()
        for row in train:
            if lottery_type == 'dlt':
                front_cnt.update(int(row[f'front_{j}']) for j in range(1, 6))
                back_cnt.update(int(row[f'back_{j}']) for j in range(1, 3))
            else:
                front_cnt.update(int(row[f'r{j}']) for j in range(1, 7))
                back_cnt.update([int(row['b1'])])

        hot_f = [n for n, _ in front_cnt.most_common(rule['front_count'] * 3)]
        hot_b = [n for n, _ in back_cnt.most_common(rule['back_count'] * 3)]

        if len(hot_f) >= rule['front_count']:
            pred_f = sorted(random.sample(hot_f, rule['front_count']))
        else:
            pred_f = sorted(random.sample(range(1, rule['front_pool'] + 1), rule['front_count']))

        if len(hot_b) >= rule['back_count']:
            pred_b = sorted(random.sample(hot_b, rule['back_count']))
        else:
            pred_b = sorted(random.sample(range(1, rule['back_pool'] + 1), rule['back_count']))

        front_hits_all.append(len(set(pred_f) & set(actual_front)))
        back_hits_all.append(len(set(pred_b) & set(actual_back)))

    avg_f = sum(front_hits_all) / len(front_hits_all)
    avg_b = sum(back_hits_all) / len(back_hits_all)
    random_f = rule['front_count'] * (rule['front_count'] / rule['front_pool'])

    return BacktestResult(
        total_trials=n_trials,
        avg_front_hits=round(avg_f, 2),
        avg_back_hits=round(avg_b, 2),
        random_baseline=round(random_f, 2),
        better_than_random=avg_f > random_f,
    )
# ═══════════════════════════════════════════

def binomial_test(successes: int, trials: int, expected_p: float) -> dict:
    """
    二项检验: 判断实际胜率是否显著偏离随机

    用于: 验证预测模型是否真的有预测能力
    """
    from math import comb

    if trials == 0:
        return {'p_value': 1.0, 'significant': False}

    observed_p = successes / trials

    # 双尾检验: 计算比观察值更极端的概率
    p_value = 0.0
    for k in range(trials + 1):
        prob = comb(trials, k) * (expected_p ** k) * ((1 - expected_p) ** (trials - k))
        if abs(k / trials - expected_p) >= abs(observed_p - expected_p):
            p_value += prob

    p_value = min(p_value, 1.0)

    return {
        'successes': successes,
        'trials': trials,
        'observed_rate': round(observed_p * 100, 2),
        'expected_rate': round(expected_p * 100, 2),
        'p_value': round(p_value, 4),
        'significant_05': p_value < 0.05,
        'significant_01': p_value < 0.01,
        'verdict': ('✅ 显著偏离随机 — 模型可能有预测能力' if p_value < 0.05
                    else '❌ 不显著 — 不能排除纯随机'),
    }


# ═══════════════════════════════════════════
#  CLI 测试
# ═══════════════════════════════════════════

if __name__ == '__main__':
    print('=' * 60)
    print('  B166ER 博彩数学武器库 V1.0')
    print('=' * 60)

    # 1. 凯利公式
    print('\n── 凯利公式 ──')
    kr = kelly_criterion(p=0.55, b=1.0, mode='half')
    print(f'  胜率55% 赔率2.0 → f*={kr.f_star}, 半凯利={kr.f_half}')
    print(f'  {kr.recommendation}')

    # 边缘情况: 负期望
    kr2 = kelly_criterion(p=0.45, b=1.0)
    print(f'  胜率45% 赔率2.0 → {kr2.recommendation}')

    # 2. 泊松分布
    print('\n── 泊松分布 ──')
    match = predict_match(home_lambda=1.8, away_lambda=1.1)
    print(f'  主{home_lambda} vs 客{away_lambda}:')
    print(f'  胜{match.home_win_prob}% 平{match.draw_prob}% 负{match.away_win_prob}%')
    print(f'  最大概率比分: {match.most_likely_score} ({match.score_probs[0]["probability"]}%)')

    # 3. Elo
    print('\n── Elo ──')
    elo = EloSystem(k_factor=32)
    elo.ratings = {'北京国安': 1650, '上海申花': 1580}
    probs = elo.win_probability('北京国安', '上海申花')
    print(f'  北京国安 vs 上海申花:')
    print(f'  胜{probs["home_win"]}% 平{probs["draw"]}% 负{probs["away_win"]}%')

    # 4. 破产定理
    print('\n── 赌徒破产 ──')
    ruin = gamblers_ruin_probability(bankroll=100, target=200, win_prob=0.49)
    print(f'  资金100 目标200 胜率49% → 破产概率: {ruin*100:.1f}%')

    # 5. 反谬误
    print('\n── 反谬误护栏 ──')
    warnings = FallacyDetector.audit_text('08号已经32期没出了，下一期该出了！')
    for w in warnings:
        print(f'  {w}')

    # 6. 统计检验
    print('\n── 统计显著性 ──')
    bt = binomial_test(successes=6, trials=10, expected_p=0.5)
    print(f'  10次中6次 → p={bt["p_value"]} → {bt["verdict"]}')

    print('\n✅ 所有模块就绪')
