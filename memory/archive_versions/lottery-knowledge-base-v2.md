# 大乐透专业知识库 V2.0 - 深度统计与数学模型

> 版本: V2.0
> 创建: 2026-03-31
> 基于: V1.0 基础规则

---

## 一、高级统计学模型

### 1.1 贝叶斯推断 (Bayesian Inference)

#### 原理
```
P(θ|D) = P(D|θ) × P(θ) / P(D)

其中:
- P(θ|D): 后验概率（给定数据D下θ的概率）
- P(D|θ): 似然函数（参数θ下观察到数据D的概率）
- P(θ): 先验概率（θ的先验信念）
- P(D): 边缘似然（归一化常数）
```

#### 在彩票中的应用

**号码冷热的后验估计**:
```python
# 先验: 每个号码出现概率相等 (1/35)
# 似然: 观察历史频率
# 后验: 更新后的出现概率

class BayesianModel:
    def __init__(self, alpha=1, beta=1):
        # alpha/beta 是先验参数（拉普拉斯平滑）
        self.alpha = alpha
        self.beta = beta

    def posterior(self, successes, trials, n_positions=35):
        """
        successes: 号码出现次数
        trials: 总试验次数
        n_positions: 位置数
        """
        # 后验均值: (alpha + successes) / (alpha + beta + trials)
        # 这里 alpha = beta = 1 (均匀先验)
        posterior_mean = (1 + successes) / (2 + trials)
        return posterior_mean

    def update_with_observation(self, prior_mean, observed_freq, weight=0.3):
        """
        融合先验和观测
        weight: 观测数据的权重
        """
        return (1 - weight) * prior_mean + weight * observed_freq
```

**贝叶斯更新流程**:
1. 初始化每个号码的先验概率 (均匀分布)
2. 每期开奖后更新后验概率
3. 用后验概率作为下期预测的权重

#### 优势
- 可以融合先验知识（号码分布的信念）
- 不需要大量历史数据也能给出估计
- 可以量化不确定性

---

### 1.2 蒙特卡洛模拟 (Monte Carlo Simulation)

#### 原理
通过大量随机采样来估计复杂系统的行为。

```python
import random
import numpy as np
from collections import Counter

class MonteCarloSimulator:
    """蒙特卡洛模拟器"""

    def __init__(self, n_simulations=100000):
        self.n_simulations = n_simulations
        self.front_range = range(1, 36)
        self.back_range = range(1, 13)

    def simulate_random(self):
        """纯随机模拟（作为基准）"""
        results = []
        for _ in range(self.n_simulations):
            front = sorted(random.sample(self.front_range, 5))
            back = sorted(random.sample(self.back_range, 2))
            results.append({'front': front, 'back': back})
        return results

    def simulate_with_constraints(self, constraints):
        """
        带约束的模拟
        constraints: dict 包含和值/奇偶/区间等约束
        """
        results = []
        for _ in range(self.n_simulations):
            front = self._generate_constrained_front(constraints)
            back = sorted(random.sample(self.back_range, 2))
            results.append({'front': front, 'back': back})
        return results

    def _generate_constrained_front(self, constraints):
        """生成满足约束的前区号码"""
        max_attempts = 1000
        for _ in range(max_attempts):
            front = sorted(random.sample(self.front_range, 5))

            # 检查和值约束
            if 'sum_range' in constraints:
                lo, hi = constraints['sum_range']
                if not (lo <= sum(front) <= hi):
                    continue

            # 检查奇偶约束
            if 'odd_ratio' in constraints:
                odd_count = sum(1 for n in front if n % 2 == 1)
                if odd_count not in constraints['odd_ratio']:
                    continue

            # 检查跨度约束
            if 'span_range' in constraints:
                lo, hi = constraints['span_range']
                span = max(front) - min(front)
                if not (lo <= span <= hi):
                    continue

            return front

        return sorted(random.sample(self.front_range, 5))

    def analyze_patterns(self, simulations):
        """分析模拟结果的模式分布"""
        sum_dist = Counter(sum(s['front']) for s in simulations)
        odd_dist = Counter(sum(1 for n in s['front'] if n % 2 == 1) for s in simulations)
        zone_dist = Counter()
        for s in simulations:
            zones = set((n-1)//7 for n in s['front'])
            zone_dist[len(zones)] += 1

        return {
            'sum_distribution': dict(sum_dist.most_common(10)),
            'odd_distribution': dict(odd_dist),
            'zone_coverage_distribution': dict(zone_dist)
        }

    def run_frequency_test(self, historical_data, simulated_data):
        """
        卡方检验: 历史数据 vs 模拟数据的频率分布
        H0: 历史数据符合均匀分布
        """
        # 统计历史频率
        historical_freq = Counter()
        for draw in historical_data:
            for num in draw['front']:
                historical_freq[num] += 1

        # 期望频率（均匀分布）
        n_draws = len(historical_data)
        expected = n_draws * 5 / 35  # 每个号码期望出现次数

        # 计算卡方统计量
        chi_square = 0
        for num in range(1, 36):
            observed = historical_freq.get(num, 0)
            chi_square += (observed - expected) ** 2 / expected

        # 自由度 = 35 - 1 = 34
        # 若 chi_square > 50.73 (α=0.05), 拒绝H0
        return chi_square
```

#### 蒙特卡洛应用场景
1. **验证策略有效性**: 对比约束选号 vs 随机选号的期望回报
2. **模式分布分析**: 了解"正常"范围，避免选极端组合
3. **风险评估**: 模拟极端情况下的资金需求

---

### 1.3 泊松分布 (Poisson Distribution)

#### 原理
泊松分布描述单位时间内随机事件发生次数的概率分布:
```
P(X=k) = (λ^k × e^(-λ)) / k!

其中 λ 是单位时间内事件发生的平均次数
```

#### 在彩票分析中的应用

**号码出现次数的泊松建模**:
```python
from scipy import stats
import numpy as np

class PoissonAnalyzer:
    """泊松分布分析器"""

    def __init__(self, historical_draws):
        self.historical = historical_draws
        self.n_periods = len(historical_draws)
        self.n_numbers = 35

    def calculate_lambda(self, number):
        """计算某号码的λ值（平均出现次数/期）"""
        count = sum(1 for draw in self.historical if number in draw['front'])
        return count / self.n_periods

    def probability_reappear(self, number, periods=1):
        """预测某号码在接下来N期内出现的概率"""
        lam = self.calculate_lambda(number) * periods
        # P(X >= 1) = 1 - P(X = 0)
        prob = 1 - stats.poisson.pmf(0, lam)
        return prob

    def expected_appearances(self, number, periods):
        """期望出现次数"""
        lam = self.calculate_lambda(number) * periods
        return lam

    def gap_probability(self, number, gap):
        """
        某号码连续gap期不出现后，在下一期出现的概率
        基于几何分布（泊松的离散版本）
        """
        lam = self.calculate_lambda(number)
        # 几何分布: P(X=k) = (1-p)^k × p
        # 这里 p ≈ λ（当λ很小时）
        p = 1 - np.exp(-lam)  # 一期内出现的概率
        prob_geometric = (1 - p) ** gap * p
        return prob_geometric

    def recommend_by_poisson(self, top_n=10):
        """基于泊松模型推荐号码"""
        recommendations = []
        for num in range(1, 36):
            lam = self.calculate_lambda(num)
            # 综合评分: λ越高越值得选，但也要考虑遗漏
            gap = self._get_current_gap(num)
            score = lam * 10 + gap * 0.5  # 可调整权重
            recommendations.append((num, lam, score))

        recommendations.sort(key=lambda x: x[2], reverse=True)
        return recommendations[:top_n]

    def _get_current_gap(self, number):
        """获取某号码当前遗漏期数"""
        for i, draw in enumerate(reversed(self.historical)):
            if number in draw['front']:
                return i
        return len(self.historical)
```

#### 泊松分布的关键洞察
- 泊松假设事件是独立发生的
- 彩票开奖满足这个假设（每次开奖是独立的）
- 可用于计算"某号码N期不出现在数学上应该出现"的概率

---

### 1.4 卡方检验 (Chi-Square Test)

#### 原理
用于检验观察频率与期望频率之间是否存在显著差异。

```python
from scipy import stats

class ChiSquareTest:
    """卡方检验器"""

    def __init__(self, historical_data):
        self.data = historical_data

    def test_uniformity(self):
        """
        检验每个号码出现频率是否符合均匀分布
        H0: 35个号码出现频率均匀
        """
        # 统计观察频率
        observed = [0] * 35
        for draw in self.data:
            for num in draw['front']:
                observed[num - 1] += 1

        # 期望频率（均匀）
        n_draws = len(self.data)
        expected = [n_draws * 5 / 35] * 35

        # 卡方检验
        chi2, p_value = stats.chisquare(observed, expected)

        return {
            'chi_square': chi2,
            'p_value': p_value,
            'significant': p_value < 0.05,
            'interpretation': '拒绝均匀分布假设' if p_value < 0.05 else '无法拒绝均匀分布假设'
        }

    def test_odd_even_ratio(self):
        """
        检验奇偶比是否符合理论分布
        理论上5个号码中奇数个数的分布:
        P(0奇)=C(17,5)/C(35,5) ≈ 0.001
        P(1奇)=C(17,4)×C(18,1)/C(35,5) ≈ 0.014
        ...
        """
        # 统计实际奇偶比分布
        observed = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        for draw in self.data:
            odd_count = sum(1 for n in draw['front'] if n % 2 == 1)
            observed[odd_count] += 1

        # 理论分布（可计算或查表）
        # 这里用近似: 奇偶比接近1:1 (3:2或2:3)
        expected = {}
        total = len(self.data)

        return {
            'observed': observed,
            'expected_approx': {i: total/7 for i in range(7)}
        }

    def test_zone_distribution(self):
        """
        检验区间分布是否均匀
        5个区间各应出现约1个号码/期
        """
        zone_counts = [{i: 0 for i in range(5)} for _ in range(5)]

        for draw in self.data:
            for num in draw['front']:
                zone = (num - 1) // 7
                zone_counts[zone][zone] += 1

        return zone_counts
```

---

### 1.5 时间序列分析 (ARIMA)

#### 原理
ARIMA (AutoRegressive Integrated Moving Average) 用于分析时间序列数据的自相关性。

```python
from statsmodels.tsa.arima.model import ARIMA
import pandas as pd
import numpy as np

class TimeSeriesAnalyzer:
    """时间序列分析器"""

    def __init__(self, historical_data):
        self.data = historical_data
        self._prepare_time_series()

    def _prepare_time_series(self):
        """将历史数据转换为时间序列"""
        # 为每个号码创建出现/未出现的二元序列
        self.series = {}
        for num in range(1, 36):
            series = []
            for draw in self.data:
                series.append(1 if num in draw['front'] else 0)
            self.series[num] = series

    def fit_arima(self, number, order=(1, 0, 1)):
        """
        对指定号码拟合ARIMA模型
        order: (p, d, q) - 自回归阶数, 差分阶数, 移动平均阶数
        """
        series = np.array(self.series[number])

        try:
            model = ARIMA(series, order=order)
            fitted = model.fit()
            return fitted
        except:
            return None

    def forecast(self, number, steps=1):
        """预测接下来N期的出现概率"""
        fitted = self.fit_arima(number)
        if fitted is None:
            return 0.5  # 默认50%

        forecast = fitted.forecast(steps=steps)
        # 预测值 > 0.5 表示更可能出现的信号
        prob = min(forecast[0], 0.5)  # 限制在合理范围

        return max(prob, 0.1)  # 至少10%

    def find_best_lags(self, number, max_lag=10):
        """寻找最佳自回归阶数"""
        series = np.array(self.series[number])
        correlations = []

        for lag in range(1, max_lag + 1):
            corr = np.corrcoef(series[:-lag], series[lag:])[0, 1]
            correlations.append((lag, corr))

        correlations.sort(key=lambda x: abs(x[1]), reverse=True)
        return correlations[:3]  # 返回最佳3个滞后阶数

    def detect_periodicity(self, number):
        """
        检测号码是否存在周期性
        返回周期长度（如果存在）
        """
        series = np.array(self.series[number])
        n = len(series)

        # 计算自相关函数
        lags = range(1, min(20, n // 2))
        autocorr = []
        for lag in lags:
            corr = np.corrcoef(series[:-lag], series[lag:])[0, 1]
            autocorr.append((lag, corr))

        # 找到显著正相关的滞后
        significant = [(lag, corr) for lag, corr in autocorr if corr > 0.1]

        if significant:
            return significant[0][0]  # 返回可能的周期长度
        return None
```

#### 时间序列分析的价值
- 发现号码出现的周期性（如果存在）
- ARIMA预测可以作为辅助参考
- 但要注意：独立随机事件通常没有自相关

---

## 二、数学模型

### 2.1 组合数学基础

#### 核心公式
```python
import math
from itertools import combinations

class CombinatoricsCalculator:
    """组合数学计算器"""

    @staticmethod
    def total_combinations():
        """总组合数"""
        front = math.comb(35, 5)  # C(35,5)
        back = math.comb(12, 2)    # C(12,2)
        return front * back

    @staticmethod
    def probability(hits_front, hits_back):
        """
        计算中奖概率
        hits_front: 前区命中个数 (0-5)
        hits_back: 后区命中个数 (0-2)
        """
        # P(命中k个前区) = C(5,k) × C(30,5-k) / C(35,5)
        # P(命中l个后区) = C(2,l) × C(10,2-l) / C(12,2)

        prob_front = (
            math.comb(5, hits_front) *
            math.comb(30, 5 - hits_front) /
            math.comb(35, 5)
        )

        prob_back = (
            math.comb(2, hits_back) *
            math.comb(10, 2 - hits_back) /
            math.comb(12, 2)
        )

        return prob_front * prob_back

    @staticmethod
    def expected_value(prize_pool, hits_front, hits_back):
        """
        计算期望回报
        prize_pool: 奖池金额
        """
        prob = CombinatoricsCalculator.probability(hits_front, hits_back)

        # 各奖级理论奖金（简化计算）
        prize_table = {
            (5, 2): prize_pool * 0.15,  # 一等奖
            (5, 1): prize_pool * 0.08,  # 二等奖
            (5, 0): 5000,
            (4, 2): 5000,
            (4, 1): 300,
            (4, 0): 150,
            (3, 2): 150,
            (3, 1): 15,
            (2, 2): 15,
            (1, 2): 5,
            (0, 2): 5,
        }

        prize = prize_table.get((hits_front, hits_back), 0)
        return prob * prize

    @staticmethod
    def all_probabilities():
        """计算所有奖级的中奖概率"""
        results = []
        for hf in range(6):
            for hb in range(3):
                prob = CombinatoricsCalculator.probability(hf, hb)
                if prob > 0:
                    results.append({
                        'hits_front': hf,
                        'hits_back': hb,
                        'probability': prob,
                        'odds': 1/prob if prob > 0 else float('inf')
                    })

        results.sort(key=lambda x: x['probability'], reverse=True)
        return results
```

#### 概率表
```python
# 完整中奖概率表
prob_table = [
    (5, 2): 1/2142280472,   # 一等奖
    (5, 1): 1/10614207,     # 二等奖
    (5, 0): 1/535431,       # 三等奖
    (4, 2): 1/535431,       # 三等奖
    (4, 1): 1/10377,        # 四等奖
    (3, 2): 1/10377,        # 四等奖
    (4, 0): 1/732,          # 五等奖
    (3, 1): 1/207,          # 六等奖
    (2, 2): 1/207,          # 六等奖
    (3, 0): 1/29,           # 七等奖
    (1, 2): 1/29,           # 七等奖
    (2, 1): 1/29,           # 七等奖
    (0, 2): 1/29,           # 七等奖
]
```

---

### 2.2 信息熵 (Information Theory)

#### 香农熵
```python
import math
from collections import Counter

class InformationEntropy:
    """信息熵分析器"""

    @staticmethod
    def shannon_entropy(numbers):
        """
        计算熵值
        H = -Σ p(x) × log2(p(x))

        熵越高表示不确定性越大
        """
        n = len(numbers)
        freq = Counter(numbers)
        entropy = 0

        for count in freq.values():
            p = count / n
            if p > 0:
                entropy -= p * math.log2(p)

        return entropy

    @staticmethod
    def information_gain(before, after):
        """
        信息增益
        表示分类/分割带来的不确定性减少
        """
        return InformationEntropy.shannon_entropy(before) - \
               InformationEntropy.shannon_entropy(after)

    @staticmethod
    def joint_entropy(sequences):
        """
        计算联合熵
        用于衡量多个号码组合的不确定性
        """
        # 简化: 将前区5个号码视为一个组合
        combined = [tuple(s['front']) for s in sequences]
        return InformationEntropy.shannon_entropy(combined)

    @staticmethod
    def mutual_information(seq1, seq2, window=1):
        """
        互信息
        衡量两个序列之间的依赖程度
        I(X;Y) = H(X) + H(Y) - H(X,Y)
        """
        # 简化实现
        h_x = InformationEntropy.shannon_entropy(seq1)
        h_y = InformationEntropy.shannon_entropy(seq2)

        # 联合分布（滑动窗口）
        n = min(len(seq1), len(seq2))
        joint = list(zip(seq1[:n], seq2[:n]))
        h_xy = InformationEntropy.shannon_entropy(joint)

        return h_x + h_y - h_xy

    @staticmethod
    def complexity_score(numbers):
        """
        复杂度评分
        基于多种熵指标的综合评分
        """
        n = len(numbers)
        if n == 0:
            return 0

        # 1. 基本频率熵
        freq = Counter(numbers)
        p = [c/n for c in freq.values()]
        entropy = -sum(pp * math.log2(pp) for pp in p if pp > 0)

        # 2. 间隔熵（考虑号码间间隔）
        sorted_nums = sorted(numbers)
        gaps = [sorted_nums[i+1] - sorted_nums[i] for i in range(len(sorted_nums)-1)]
        gap_entropy = InformationEntropy.shannon_entropy(gaps) if gaps else 0

        # 3. 区间分布熵
        zones = [(num-1)//7 for num in numbers]
        zone_entropy = InformationEntropy.shannon_entropy(zones)

        # 综合评分（加权平均）
        score = entropy * 0.5 + gap_entropy * 0.3 + zone_entropy * 0.2

        return score
```

#### 熵分析应用
- **选号策略**: 优先选择高熵（不确定性大）的组合
- **模式识别**: 检测号码分布的规律性
- **异常检测**: 识别"太规律"的号码组合

---

### 2.3 模糊数学模型

#### 模糊集合与隶属度
```python
class FuzzyLotteryModel:
    """模糊数学模型"""

    def __init__(self, historical_data):
        self.data = historical_data
        self.numbers = range(1, 36)

    def membership_hot(self, number, window=10):
        """
        计算某号码"热"的隶属度
        使用近N期的出现频率作为隶属度
        """
        recent = self.data[-window:]
        count = sum(1 for draw in recent if number in draw['front'])
        return count / window  # 0-1之间的值

    def membership_cold(self, number, window=30):
        """
        计算某号码"冷"的隶属度
        基于长期未出现的程度
        """
        for i, draw in enumerate(reversed(self.data)):
            if number in draw['front']:
                missing_periods = i
                break
        else:
            missing_periods = len(self.data)

        # 使用S型隶属函数
        # missing_periods越大，cold隶属度越高（上限为1）
        cold = 2 / (1 + math.exp(-0.3 * (missing_periods - 10))) - 1
        return max(0, min(1, cold))

    def membership_medium(self, number):
        """
        计算"温"的隶属度
        """
        hot = self.membership_hot(number)
        cold = self.membership_cold(number)
        return 1 - hot - cold

    def fuzzy_inference(self, number):
        """
        模糊推理
        综合热/冷/温隶属度给出推荐度
        """
        hot = self.membership_hot(number)
        cold = self.membership_cold(number)
        medium = self.membership_medium(number)

        # 模糊规则:
        # IF 热 THEN 推荐
        # IF 冷 THEN 不推荐
        # IF 温 THEN 观望

        # 计算推荐度 (0-1)
        recommendation = hot * 0.6 + medium * 0.3 - cold * 0.4

        return {
            'hot': hot,
            'cold': cold,
            'medium': medium,
            'recommendation': max(0, min(1, recommendation))
        }

    def generate_fuzzy_set(self, top_n=10):
        """
        生成模糊推荐集合
        返回推荐度最高的N个号码
        """
        scores = []
        for num in self.numbers:
            result = self.fuzzy_inference(num)
            scores.append((num, result['recommendation']))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_n]
```

#### 模糊模式识别
```python
class FuzzyPatternRecognition:
    """模糊模式识别"""

    # 定义模糊模式类型
    PATTERNS = {
        'hot_dominant': {'description': '热号主导型', 'hot_weight': 0.7},
        'cold_transition': {'description': '冷转热型', 'cold_weight': 0.6},
        'balanced': {'description': '均衡型', 'balance_weight': 0.5},
        'zone_concentrated': {'description': '区间集中型', 'zone_weight': 0.6},
        'spread_out': {'description': '分散型', 'spread_weight': 0.5},
    }

    @staticmethod
    def classify_pattern(numbers):
        """将号码组合分类到已知模式"""
        n = len(numbers)

        # 计算热号比例
        # (需要历史数据，这里简化)
        hot_count = len([n for n in numbers if n in [3, 7, 22, 35]])  # 简化假设

        # 计算区间集中度
        zones = set((num-1)//7 for num in numbers)
        zone_concentration = len(zones) / 5

        # 模式匹配
        if hot_count >= 3:
            return 'hot_dominant'
        elif zone_concentration <= 0.4:
            return 'zone_concentrated'
        elif zone_concentration >= 0.8:
            return 'spread_out'
        else:
            return 'balanced'
```

---

### 2.4 混沌理论初步

#### 彩票中的混沌现象
```python
class ChaosAnalyzer:
    """混沌分析器（简化版）"""

    @staticmethod
    def poincare_section(data, threshold=17.5):
        """
        庞加莱截面分析
        将连续数据转换为离散状态
        threshold: 分割点（这里用17.5将号码分为大小两组）
        """
        section = []
        for draw in data:
            # 统计大于阈值的号码个数
            count = sum(1 for num in draw['front'] if num > threshold)
            section.append(count)
        return section

    @staticmethod
    def lyapunov_exponent_estimate(data, window=5):
        """
        李雅普诺夫指数估计（简化）
        正值表示混沌（对初始条件敏感）
        注意: 彩票数据太短，无法可靠估计
        """
        if len(data) < window * 2:
            return None

        # 简化: 计算相邻状态的变化率
        section = ChaosAnalyzer.poincare_section(data)
        lyapunov = 0

        for i in range(len(section) - 1):
            if section[i] > 0:
                change = abs(section[i+1] - section[i]) / section[i]
                lyapunov += math.log(change + 0.01)  # 加小量避免log(0)

        lyapunov /= (len(section) - 1)
        return lyapunov

    @staticmethod
    def correlation_dimension(data, max_embedding=10):
        """
        关联维数估计（Grass-Procaccia算法简化）
        用于检测数据中的自由度数量
        注意: 这是一个示意实现
        """
        # 简化: 使用前区平均值作为简化特征
        features = [sum(draw['front'])/5 for draw in data]

        # 计算不同嵌入维数下的关联积分
        dimensions = []
        for m in range(2, max_embedding + 1):
            # 简化的关联积分计算
            correlations = []
            for i in range(len(features) - m):
                window = features[i:i+m]
                variance = sum((x - sum(window)/m)**2 for x in window) / m
                correlations.append(variance)

            if correlations:
                # 关联维数近似
                dim = sum(math.log(max(c, 0.01)) for c in correlations) / (len(correlations) * math.log(0.01))
                dimensions.append(dim)

        return dimensions[-1] if dimensions else None
```

#### 混沌视角的彩票认知
1. **短期不可预测**: 混沌系统对初始条件敏感，长期不可预测
2. **存在吸引子**: 号码分布可能在统计上趋向某些"吸引子"
3. **分形结构**: 号码分布可能具有自相似性

---

## 三、自我迭代进化系统

### 3.1 自我评估机制

```python
class SelfEvolution:
    """预测模型自我迭代进化系统"""

    def __init__(self, history_file='lottery_history/index.json'):
        self.history_file = history_file
        self.load_history()
        self.model_weights = {
            'frequency': 0.25,
            'missing': 0.25,
            'recent': 0.25,
            'zone': 0.25
        }
        self.performance_history = []

    def load_history(self):
        """加载预测历史"""
        import json
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                self.history = json.load(f)
        except:
            self.history = {'predictions': []}

    def record_prediction(self, issue, predictions, actual=None):
        """记录预测结果"""
        prediction_record = {
            'issue': issue,
            'predictions': predictions,
            'actual': actual,
            'weights_used': self.model_weights.copy()
        }
        self.history['predictions'].append(prediction_record)
        self.save_history()

    def evaluate_accuracy(self, lookback=10):
        """
        评估近期预测准确度
        返回各模型的命中率
        """
        if len(self.history['predictions']) < 3:
            return self.model_weights.copy()

        recent = self.history['predictions'][-lookback:]

        # 统计各模型命中的前区/后区个数
        model_hits = {model: {'front': 0, 'back': 0, 'total': 0}
                     for model in ['frequency', 'missing', 'recent', 'zone']}

        for record in recent:
            if not record.get('actual'):
                continue

            actual_front = set(record['actual'].get('front', []))
            actual_back = set(record['actual'].get('back', []))

            for pred in record['predictions']:
                model = pred.get('model', 'frequency')
                front_hit = len(set(pred['front']) & actual_front)
                back_hit = len(set(pred['back']) & actual_back)

                model_hits[model]['front'] += front_hit
                model_hits[model]['back'] += back_hit
                model_hits[model]['total'] += front_hit + back_hit

        # 计算各模型命中率
        total_predictions = len(recent) * 5 * 7  # 前区5个 + 后区2个
        hit_rates = {}
        for model, hits in model_hits.items():
            hit_rates[model] = hits['total'] / total_predictions if total_predictions > 0 else 0

        return hit_rates

    def adjust_weights(self, learning_rate=0.1):
        """
        基于近期表现调整模型权重
        使用强化学习思想：奖励好模型，惩罚差模型
        """
        hit_rates = self.evaluate_accuracy()

        # 归一化命中率作为新的权重基础
        total_rate = sum(hit_rates.values())
        if total_rate == 0:
            return self.model_weights

        raw_weights = {model: rate / total_rate for model, rate in hit_rates.items()}

        # 混合: 保留历史权重 + 吸收新信息
        new_weights = {}
        for model in self.model_weights:
            new_weights[model] = (1 - learning_rate) * self.model_weights[model] + \
                               learning_rate * raw_weights.get(model, 0.25)

        # 再次归一化
        total = sum(new_weights.values())
        self.model_weights = {k: v/total for k, v in new_weights.items()}

        return self.model_weights

    def evolve(self, generations=10):
        """
        进化算法: 通过多代迭代找到最优参数组合
        简化版: 网格搜索 + 交叉验证
        """
        best_weights = self.model_weights.copy()
        best_score = self._evaluate_weights(best_weights)

        for gen in range(generations):
            # 生成候选权重
            candidates = []
            for _ in range(5):
                # 随机扰动
                candidate = {}
                for model, weight in best_weights.items():
                    noise = random.uniform(-0.1, 0.1)
                    candidate[model] = max(0.05, min(0.5, weight + noise))

                # 归一化
                total = sum(candidate.values())
                candidate = {k: v/total for k, v in candidate.items()}
                candidates.append(candidate)

            # 评估候选
            for candidate in candidates:
                score = self._evaluate_weights(candidate)
                if score > best_score:
                    best_score = score
                    best_weights = candidate

        self.model_weights = best_weights
        return best_weights, best_score

    def _evaluate_weights(self, weights):
        """
        评估一组权重的得分
        使用历史数据进行交叉验证
        """
        if len(self.history['predictions']) < 5:
            return 0

        # 简化: 计算加权命中率
        hit_rates = self.evaluate_accuracy()
        score = sum(weights.get(model, 0.25) * rate
                   for model, rate in hit_rates.items())

        return score
```

### 3.2 自适应参数调整

```python
class AdaptiveParameters:
    """自适应参数调整系统"""

    def __init__(self):
        # 可调参数及其当前值
        self.parameters = {
            'hot_threshold': 3,           # 热号阈值（出现次数）
            'cold_threshold': 8,        # 冷号阈值（遗漏期数）
            'recent_window': 3,          # 近期窗口期数
            'zone_weight': 0.2,          # 区间策略权重
            'sum_target': 95,            # 目标和值
            'sum_tolerance': 30,        # 和值容差
        }

        # 参数历史（用于趋势分析）
        self.param_history = []

    def update_with_feedback(self, prediction, actual, score):
        """
        根据预测结果更新参数
        prediction: 预测时的参数组合
        actual: 实际开奖
        score: 综合得分 (0-1)
        """
        self.param_history.append({
            'params': prediction,
            'actual': actual,
            'score': score
        })

        # 如果得分低，触发参数调整
        if score < 0.3:
            self._adjust_parameters(prediction, actual, score)

    def _adjust_parameters(self, prediction, actual, score):
        """
        根据失败案例调整参数
        这里实现一个简化的反向传播逻辑
        """
        # 分析失败原因
        front_miss = set(prediction['front']) - set(actual.get('front', []))
        back_miss = set(prediction['back']) - set(actual.get('back', []))

        # 如果后区全错，增加遗漏号权重
        if len(back_miss) == 2:
            self.parameters['cold_threshold'] = min(15,
                self.parameters['cold_threshold'] + 1)

        # 如果前区遗漏多，考虑增加近期号权重
        if len(front_miss) >= 3:
            self.parameters['recent_window'] = min(5,
                self.parameters['recent_window'] + 1)

    def get_parameters(self):
        """获取当前最优参数"""
        return self.parameters.copy()
```

### 3.3 知识蒸馏系统

```python
class KnowledgeDistillation:
    """
    知识蒸馏: 将多个模型的知识压缩到单一高效模型
    基于"教师-学生"框架
    """

    def __init__(self, teacher_models):
        """
        teacher_models: 多个已训练模型的预测结果
        """
        self.teacher_models = teacher_models
        self.student_knowledge = {}

    def distill(self, historical_data):
        """
        从教师模型中提取知识
        生成"软标签"代替硬标签
        """
        # 对每个号码计算教师模型的平均预测概率
        number_probs = {n: [] for n in range(1, 36)}

        for model in self.teacher_models:
            for num in range(1, 36):
                prob = model.predict_number_probability(num)
                number_probs[num].append(prob)

        # 计算软标签（加权平均）
        self.student_knowledge = {}
        for num, probs in number_probs.items():
            self.student_knowledge[num] = sum(probs) / len(probs)

        return self.student_knowledge

    def generate_student_prediction(self):
        """
        基于蒸馏知识生成预测
        """
        # 按概率排序
        sorted_numbers = sorted(
            self.student_knowledge.items(),
            key=lambda x: x[1],
            reverse=True
        )

        # 选择概率最高的组合
        # （考虑约束条件后）
        front = [num for num, _ in sorted_numbers[:15]]  # 前15个候选
        # 加入一些随机性和约束检查...

        return front
```

---

## 四、整合预测系统

### 4.1 综合评分模型

```python
class IntegratedPredictor:
    """整合所有模型的综合预测器"""

    def __init__(self, historical_data):
        self.data = historical_data
        self.bayesian = BayesianModel()
        self.poisson = PoissonAnalyzer(historical_data)
        self.fuzzy = FuzzyLotteryModel(historical_data)
        self.entropy = InformationEntropy()
        self.evolution = SelfEvolution()
        self.adaptive = AdaptiveParameters()

    def calculate_comprehensive_score(self, number):
        """
        计算某号码的综合评分
        综合贝叶斯 + 泊松 + 模糊 + 熵
        """
        scores = {}

        # 1. 贝叶斯评分
        recent = self.data[-15:]
        count = sum(1 for d in recent if number in d['front'])
        scores['bayesian'] = self.bayesian.update_with_observation(
            1/35, count/15, weight=0.3
        )

        # 2. 泊松评分
        scores['poisson'] = self.poisson.probability_reappear(number, periods=1)

        # 3. 模糊评分
        fuzzy_result = self.fuzzy.fuzzy_inference(number)
        scores['fuzzy'] = fuzzy_result['recommendation']

        # 4. 熵评分（基于近期缺失的信息增益）
        # ...

        # 综合评分（可调整权重）
        comprehensive = (
            scores['bayesian'] * 0.3 +
            scores['poisson'] * 0.3 +
            scores['fuzzy'] * 0.4
        )

        return comprehensive

    def generate_recommendation(self, count=5):
        """
        生成推荐号码组合
        """
        # 计算所有号码的综合评分
        all_scores = []
        for num in range(1, 36):
            score = self.calculate_comprehensive_score(num)
            all_scores.append((num, score))

        # 排序
        all_scores.sort(key=lambda x: x[1], reverse=True)

        # 选择候选
        candidates = [num for num, _ in all_scores[:20]]

        # 应用约束条件筛选
        selected = self._apply_constraints(candidates, all_scores)

        return selected

    def _apply_constraints(self, candidates, all_scores, target_count=5):
        """应用约束条件"""
        # 这里实现一个简化的贪心算法
        selected = []

        # 优先选择评分最高的
        for num, score in sorted(all_scores, key=lambda x: x[1], reverse=True):
            if len(selected) >= target_count:
                break
            if num in candidates:
                selected.append(num)

        return selected
```

---

## 五、使用指南

### 5.1 模型选择建议

| 场景 | 推荐模型 |
|------|----------|
| 短期娱乐 | 随机选号 |
| 分析学习 | 综合评分模型 |
| 避免极端 | 蒙特卡洛模拟约束 |
| 历史研究 | 贝叶斯 + 泊松 |

### 5.2 重要警告

1. **所有预测模型期望值为负**
2. **历史规律不能预测未来**
3. **理性购彩，娱乐为主**

---

**版本历史**:
- V1.0: 基础规则 + 历史数据 + 预测理论
- V2.0: 高级统计模型（贝叶斯/蒙特卡洛/泊松/卡方/时间序列）+ 数学模型（组合/熵/模糊/混沌）+ 自我迭代进化系统

**更新日期**: 2026-03-31
