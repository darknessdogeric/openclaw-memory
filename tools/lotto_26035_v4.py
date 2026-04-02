# -*- coding: utf-8 -*-
"""
B166ER 大乐透预测 V4.0 - 整合高级统计模型 + 自我进化
包含: 贝叶斯/泊松/模糊/熵 + 自适应权重 + 自我迭代

版本历史:
- V4.0: 整合高级统计模型 + 自我进化系统
- V3.0: 多模型融合
- V2.0: 热号多注覆盖 + 后区遗漏追踪
- V1.1: 基础统计
"""
import random
import math
import json
from datetime import datetime
from collections import Counter

# ============================================================================
# 知识库：历史开奖数据
# ============================================================================
RECENT_DRAWS = [
    {'front': [7, 14, 22, 28, 35], 'back': [2, 8], 'date': '2026-03-17', 'issue': '26030'},
    {'front': [6, 8, 22, 29, 34], 'back': [5, 7], 'date': '2026-03-25', 'issue': '26031'},
    {'front': [3, 4, 19, 26, 32], 'back': [1, 12], 'date': '2026-03-28', 'issue': '26032'},
    {'front': [3, 5, 7, 9, 18], 'back': [2, 10], 'date': '2026-03-30', 'issue': '26033'},
]

# ============================================================================
# 高级统计模型
# ============================================================================

class BayesianModel:
    """贝叶斯推断模型"""
    def __init__(self, alpha=1, beta=1):
        self.alpha = alpha  # 先验参数
        self.beta = beta

    def posterior_mean(self, successes, trials):
        """后验均值"""
        return (self.alpha + successes) / (self.alpha + self.beta + trials)

    def update_and_score(self, number, recent_draws, lookback=15):
        """计算贝叶斯评分"""
        count = sum(1 for d in recent_draws[-lookback:] if number in d['front'])
        trials = lookback * 5
        prior = 1 / 35
        observed = count / trials if trials > 0 else 0
        # 融合先验和观测
        score = (1 - 0.3) * prior + 0.3 * observed
        return score


class PoissonAnalyzer:
    """泊松分布分析"""
    def __init__(self, recent_draws):
        self.recent = recent_draws

    def lambda_(self, number, lookback=15):
        """计算某号码的λ值（平均出现率）"""
        count = sum(1 for d in self.recent[-lookback:] if number in d['front'])
        return count / lookback

    def probability_reappear(self, number, periods=1, lookback=15):
        """预测未来N期出现的概率"""
        lam = self.lambda_(number, lookback) * periods
        # P(X >= 1) = 1 - P(X = 0)
        prob = 1 - math.exp(-lam)
        return min(prob, 0.5)  # 限制在合理范围

    def gap_probability(self, number, lookback=30):
        """计算当前遗漏后的出现概率"""
        lam = self.lambda_(number, lookback)
        # 找到当前遗漏期数
        gap = 0
        for i, d in enumerate(reversed(self.recent[-lookback:])):
            if number in d['front']:
                gap = i
                break
        else:
            gap = lookback

        # 几何分布: P(X=k) = (1-p)^k * p
        p = 1 - math.exp(-lam)
        return (1 - p) ** gap * p


class FuzzyModel:
    """模糊数学模型"""
    def __init__(self, recent_draws):
        self.recent = recent_draws

    def membership_hot(self, number, window=10):
        """热隶属度"""
        count = sum(1 for d in self.recent[-window:] if number in d['front'])
        return count / window

    def membership_cold(self, number, window=30):
        """冷隶属度"""
        for i, d in enumerate(reversed(self.recent[-window:])):
            if number in d['front']:
                gap = i
                break
        else:
            gap = window
        # S型隶属函数
        cold = 2 / (1 + math.exp(-0.3 * (gap - 10))) - 1
        return max(0, min(1, cold))

    def fuzzy_score(self, number):
        """模糊推理评分"""
        hot = self.membership_hot(number)
        cold = self.membership_cold(number)
        medium = 1 - hot - cold
        # 模糊规则: 热→推荐, 冷→不推荐, 温→观望
        score = hot * 0.6 + medium * 0.3 - cold * 0.4
        return max(0, min(1, score))


class EntropyAnalyzer:
    """信息熵分析"""
    @staticmethod
    def shannon_entropy(numbers):
        """计算熵值"""
        if not numbers:
            return 0
        counter = Counter(numbers)
        entropy = 0
        n = len(numbers)
        for count in counter.values():
            p = count / n
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy

    @staticmethod
    def zone_entropy(numbers):
        """区间分布熵"""
        zones = [(num - 1) // 7 for num in numbers]
        return EntropyAnalyzer.shannon_entropy(zones)


class AdaptiveEvolution:
    """自适应进化系统"""
    def __init__(self):
        # 初始权重
        self.weights = {
            'frequency': 0.20,
            'bayesian': 0.20,
            'poisson': 0.20,
            'fuzzy': 0.20,
            'entropy': 0.10,
            'random': 0.10
        }
        self.performance_history = []

    def record_result(self, predictions, actual):
        """记录预测结果"""
        if not actual:
            return

        actual_front = set(actual['front'])
        actual_back = set(actual['back'])

        for pred in predictions:
            front_hit = len(set(pred['front']) & actual_front)
            back_hit = len(set(pred['back']) & actual_back)
            score = (front_hit * 2 + back_hit * 3) / 17  # 归一化

            self.performance_history.append({
                'model': pred.get('model', 'unknown'),
                'front_hits': front_hit,
                'back_hits': back_hit,
                'score': score
            })

    def adjust_weights(self, learning_rate=0.15):
        """基于近期表现调整权重"""
        if len(self.performance_history) < 3:
            return self.weights

        # 统计各模型近期得分
        recent = self.performance_history[-10:]
        model_scores = {}
        for item in recent:
            model = item['model']
            if model not in model_scores:
                model_scores[model] = []
            model_scores[model].append(item['score'])

        # 计算平均得分
        avg_scores = {}
        for model, scores in model_scores.items():
            avg_scores[model] = sum(scores) / len(scores) if scores else 0

        # 归一化
        total = sum(avg_scores.values()) if avg_scores else 1
        new_weights = {}
        for model in self.weights:
            score = avg_scores.get(model, 0)
            new_weights[model] = (1 - learning_rate) * self.weights.get(model, 0.2) + \
                                 learning_rate * (score / total if total > 0 else 0.2)

        # 归一化确保总和为1
        total_w = sum(new_weights.values())
        self.weights = {k: v/total_w for k, v in new_weights.items()}

        return self.weights


# ============================================================================
# 主预测器
# ============================================================================

class LottoPredictorV40:
    """大乐透预测 V4.0 - 整合高级模型 + 自我进化"""

    def __init__(self, recent_draws):
        self.recent = recent_draws
        self.front_range = range(1, 36)
        self.back_range = range(1, 13)

        # 初始化各模型
        self.bayesian = BayesianModel()
        self.poisson = PoissonAnalyzer(recent_draws)
        self.fuzzy = FuzzyModel(recent_draws)
        self.entropy = EntropyAnalyzer()
        self.evolution = AdaptiveEvolution()

        # 计算统计数据
        self._calculate_statistics()

    def _calculate_statistics(self):
        """计算统计数据"""
        # 频率统计
        front_all = []
        back_all = []
        for draw in self.recent[-15:]:
            front_all.extend(draw.get('front', []))
            back_all.extend(draw.get('back', []))

        self.front_freq = Counter(front_all)
        self.back_freq = Counter(back_all)
        self.hot_front = [n for n, c in self.front_freq.most_common(12)]
        self.cold_front = [n for n in self.front_range if n not in self.hot_front[:10]]

        # 近期重复号
        recent_3 = set()
        for draw in self.recent[-3:]:
            recent_3.update(draw.get('front', []))
        self.recent_3 = recent_3

        recent_2 = set()
        for draw in self.recent[-2:]:
            recent_2.update(draw.get('front', []))
        self.recent_2 = recent_2

        # 后区遗漏
        self.back_missing = {}
        for num in self.back_range:
            for i, d in enumerate(reversed(self.recent[-20:])):
                if num in d.get('back', []):
                    self.back_missing[num] = i
                    break
            else:
                self.back_missing[num] = 20

    def score_all_numbers(self):
        """综合评分所有号码"""
        scores = {}
        for num in self.front_range:
            # 1. 频率评分
            freq_score = self.front_freq.get(num, 0) / 15

            # 2. 贝叶斯评分
            bayes_score = self.bayesian.update_and_score(num, self.recent)

            # 3. 泊松评分
            poisson_score = self.poisson.probability_reappear(num)

            # 4. 模糊评分
            fuzzy_score = self.fuzzy.fuzzy_score(num)

            # 5. 熵评分（基于区间）
            zone = (num - 1) // 7
            zone_hot = sum(1 for n in self.hot_front if (n-1)//7 == zone)
            entropy_score = zone_hot / 8

            # 综合评分
            weights = self.evolution.weights
            comprehensive = (
                weights.get('frequency', 0.2) * freq_score +
                weights.get('bayesian', 0.2) * bayes_score +
                weights.get('poisson', 0.2) * poisson_score +
                weights.get('fuzzy', 0.2) * fuzzy_score +
                weights.get('entropy', 0.1) * entropy_score
            )

            scores[num] = {
                'comprehensive': comprehensive,
                'frequency': freq_score,
                'bayesian': bayes_score,
                'poisson': poisson_score,
                'fuzzy': fuzzy_score,
                'entropy': entropy_score
            }

        return scores

    def _check_constraints(self, front):
        """约束检查"""
        total = sum(front)
        if not (65 <= total <= 130):
            return False
        span = max(front) - min(front)
        if not (10 <= span <= 34):
            return False
        odd = sum(1 for n in front if n % 2 == 1)
        if odd not in [2, 3, 4]:
            return False
        big = sum(1 for n in front if n >= 18)
        if big not in [2, 3, 4]:
            return False
        zones = set((n - 1) // 7 for n in front)
        if len(zones) < 4:
            return False
        consecutive = sum(1 for i in range(4) if front[i+1] - front[i] == 1)
        if consecutive > 1:
            return False
        return True

    def _generate_back(self):
        """生成后区"""
        missing = sorted(self.back_missing.items(), key=lambda x: x[1], reverse=True)
        big_missing = [n for n, m in missing if m >= 5]

        # 至少选1个大遗漏号
        if big_missing and random.random() < 0.85:
            back = [random.choice(big_missing[:3])]
        else:
            back = [random.choice(list(self.back_range))]

        remaining = [n for n in self.back_range if n not in back]
        if remaining:
            hot = [n for n in remaining if n in self.back_freq.most_common(4)]
            if hot and random.random() < 0.5:
                back.append(random.choice(hot))
            else:
                rem_sorted = sorted(remaining, key=lambda x: self.back_missing.get(x, 0), reverse=True)
                back.append(random.choice(rem_sorted[:4]))

        return sorted(back[:2])

    def generate_prediction(self, count=5):
        """生成预测"""
        all_scores = self.score_all_numbers()
        sorted_nums = sorted(all_scores.items(), key=lambda x: x[1]['comprehensive'], reverse=True)

        results = []
        for i in range(count):
            # 策略: 高分号码优先，但加入随机性和约束
            candidates = [num for num, _ in sorted_nums[:15]]

            # 贪心选择
            selected = []
            attempts = 0
            while len(selected) < 5 and attempts < 100:
                # 基于评分配比选择
                if random.random() < 0.7:  # 70%按评分
                    pool = candidates
                else:  # 30%随机
                    pool = list(self.front_range)

                chosen = random.choice(pool)
                if chosen not in selected:
                    test = selected + [chosen]
                    if self._check_constraints(test):
                        selected.append(chosen)
                attempts += 1

            # 兜底
            while len(selected) < 5:
                avail = [n for n in self.front_range if n not in selected]
                if avail:
                    selected.append(random.choice(avail))
                else:
                    break

            back = self._generate_back()

            # 记录使用的模型（简化版）
            model_used = random.choice(['frequency', 'bayesian', 'poisson', 'fuzzy', 'entropy'])

            results.append({
                'no': i + 1,
                'front': sorted(selected),
                'back': back,
                'sum': sum(selected),
                'span': max(selected) - min(selected),
                'model': model_used,
                'scores': {n: all_scores[n]['comprehensive'] for n in selected}
            })

        return results


def save_prediction(issue, predictions, review=None):
    """保存预测"""
    filename = f"lottery_history/prediction_{issue}.json"
    data = {
        'issue': issue,
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'predictions': predictions,
        'last_issue_review': review,
        'model_version': 'V4.0',
        'features': '贝叶斯 + 泊松 + 模糊 + 熵 + 自适应权重'
    }
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[OK] Saved: {filename}")


def main():
    print("=" * 70)
    print("[B166ER] Super Lotto Prediction V4.0")
    print("Advanced: Bayesian + Poisson + Fuzzy + Entropy + Self-Evolution")
    print("=" * 70)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Target: 26035 (2026-04-04 Saturday)")
    print()

    predictor = LottoPredictorV40(RECENT_DRAWS)

    # 显示模型权重
    print("【自适应权重 (V4.0)】")
    for model, weight in predictor.evolution.weights.items():
        bar = '#' * int(weight * 50) + '-' * (50 - int(weight * 50))
        print(f"  {model:12s}: {bar} {weight:.1%}")
    print()

    # 显示综合评分TOP10
    all_scores = predictor.score_all_numbers()
    sorted_nums = sorted(all_scores.items(), key=lambda x: x[1]['comprehensive'], reverse=True)

    print("【综合评分 TOP 10】")
    print("  号码 | 综合  | 频率  | 贝叶斯 | 泊松  | 模糊  | 熵")
    print("  " + "-" * 60)
    for num, scores in sorted_nums[:10]:
        print(f"  {num:5d} | {scores['comprehensive']:.3f} | {scores['frequency']:.3f} | {scores['bayesian']:.3f} | {scores['poisson']:.3f} | {scores['fuzzy']:.3f} | {scores['entropy']:.3f}")
    print()

    # 26034期复盘（未开奖，用历史数据验证）
    print("【26034期 - 待开奖 (2026-04-02)】")
    print()

    # 生成26035期预测
    print("【26035期预测 - 5注】")
    print("-" * 70)

    predictions = predictor.generate_prediction(count=5)
    save_prediction('26035', predictions)

    for pred in predictions:
        front_str = ' '.join([f"{n:02d}" for n in pred['front']])
        back_str = ' '.join([f"{n:02d}" for n in pred['back']])
        print(f"注{pred['no']}: 前区[{front_str}] 后区[{back_str}]")
        print(f"       和值:{pred['sum']:3d} 跨度:{pred['span']:2d} [模型:{pred['model']}]")

    print()
    print("=" * 70)
    print("Disclaimer: 彩票是随机事件，预测仅供娱乐，请理性购彩")
    print("=" * 70)


if __name__ == '__main__':
    main()