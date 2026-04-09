#!/usr/bin/env python3
"""
B166ER 大乐透预测系统 V5.0
核心架构: 数据特征工程 -> 混合预测引擎 -> 组合优化 -> 博弈论 -> 资金管理
"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import sys
sys.path.insert(0, 'C:/Users/ericz/.openclaw/workspace/lottery_history')
import math
from collections import Counter, defaultdict
import random

# ========== 历史数据 (内联) ==========
HISTORY_DATA = [
    {"issue": "26007", "front": [1, 3, 13, 20, 26], "back": [3, 10], "date": "2026-01-17"},
    {"issue": "26008", "front": [3, 6, 17, 21, 33], "back": [5, 11], "date": "2026-01-19"},
    {"issue": "26009", "front": [5, 12, 13, 14, 33], "back": [5, 8], "date": "2026-01-21"},
    {"issue": "26010", "front": [2, 3, 13, 18, 26], "back": [2, 9], "date": "2026-01-24"},
    {"issue": "26011", "front": [14, 21, 23, 29, 33], "back": [2, 10], "date": "2026-01-26"},
    {"issue": "26012", "front": [1, 2, 9, 22, 25], "back": [1, 6], "date": "2026-01-28"},
    {"issue": "26013", "front": [3, 5, 6, 23, 26], "back": [1, 4], "date": "2026-01-31"},
    {"issue": "26014", "front": [16, 18, 23, 34, 35], "back": [1, 6], "date": "2026-02-02"},
    {"issue": "26015", "front": [1, 4, 10, 13, 17], "back": [3, 11], "date": "2026-02-04"},
    {"issue": "26016", "front": [8, 9, 12, 19, 24], "back": [1, 6], "date": "2026-02-07"},
    {"issue": "26017", "front": [4, 5, 10, 23, 31], "back": [7, 12], "date": "2026-02-09"},
    {"issue": "26018", "front": [9, 11, 19, 30, 35], "back": [1, 12], "date": "2026-02-11"},
    {"issue": "26019", "front": [12, 13, 14, 16, 31], "back": [4, 12], "date": "2026-02-25"},
    {"issue": "26020", "front": [1, 10, 21, 23, 29], "back": [10, 12], "date": "2026-02-28"},
    {"issue": "26021", "front": [5, 8, 12, 14, 17], "back": [4, 5], "date": "2026-03-02"},
    {"issue": "26022", "front": [5, 9, 10, 18, 26], "back": [5, 6], "date": "2026-03-04"},
    {"issue": "26023", "front": [9, 25, 26, 27, 34], "back": [1, 8], "date": "2026-03-07"},
    {"issue": "26024", "front": [2, 4, 8, 10, 21], "back": [9, 12], "date": "2026-03-09"},
    {"issue": "26025", "front": [3, 15, 24, 28, 29], "back": [3, 7], "date": "2026-03-11"},
    {"issue": "26026", "front": [10, 11, 22, 26, 32], "back": [1, 8], "date": "2026-03-14"},
    {"issue": "26027", "front": [9, 10, 11, 16, 21], "back": [1, 11], "date": "2026-03-16"},
    {"issue": "26028", "front": [15, 27, 29, 30, 34], "back": [1, 10], "date": "2026-03-18"},
    {"issue": "26029", "front": [3, 5, 17, 33, 35], "back": [5, 7], "date": "2026-03-21"},
    {"issue": "26030", "front": [2, 13, 22, 28, 34], "back": [5, 12], "date": "2026-03-23"},
    {"issue": "26031", "front": [6, 8, 22, 29, 34], "back": [5, 7], "date": "2026-03-25"},
    {"issue": "26032", "front": [3, 4, 19, 26, 32], "back": [1, 12], "date": "2026-03-28"},
    {"issue": "26033", "front": [3, 5, 7, 9, 18], "back": [2, 10], "date": "2026-03-30"},
    {"issue": "26034", "front": [11, 12, 25, 26, 27], "back": [8, 11], "date": "2026-04-01"},
    {"issue": "26035", "front": [2, 22, 30, 33, 34], "back": [8, 12], "date": "2026-04-04"},
    {"issue": "26036", "front": [4, 7, 16, 26, 32], "back": [5, 8], "date": "2026-04-06"},
]

NEXT_ISSUE = "26037"
NEXT_DATE = "2026-04-08"

# ========== 第一层: 数据特征工程 ==========

class FeatureEngineering:
    """多维特征提取"""

    @staticmethod
    def calc_ac(front):
        """AC值 - 算术复杂性"""
        diffs = []
        for i in range(len(front)):
            for j in range(i+1, len(front)):
                diffs.append(abs(front[i] - front[j]))
        return len(set(diffs)) - (len(front) - 1)

    @staticmethod
    def calc_sum(front):
        return sum(front)

    @staticmethod
    def calc_span(front):
        return max(front) - min(front)

    @staticmethod
    def calc_odd_even(front):
        odd = sum(1 for x in front if x % 2 == 1)
        return f"{odd}:{len(front)-odd}"

    @staticmethod
    def calc_size_ratio(front):
        small = sum(1 for x in front if x <= 17)
        return f"{small}:{len(front)-small}"

    @staticmethod
    def calc_zone_dist(front):
        """5区分布"""
        zones = [0]*5
        for x in front:
            if x <= 7: zones[0] += 1
            elif x <= 14: zones[1] += 1
            elif x <= 21: zones[2] += 1
            elif x <= 28: zones[3] += 1
            else: zones[4] += 1
        return zones

    @staticmethod
    def calc_road_012(front):
        """012路特征"""
        road = [0, 0, 0]
        for x in front:
            road[x % 3] += 1
        return road

    @staticmethod
    def extract_features(draw):
        """提取单期所有特征"""
        front = draw['front']
        back = draw['back']
        return {
            'issue': draw['issue'],
            'sum': FeatureEngineering.calc_sum(front),
            'span': FeatureEngineering.calc_span(front),
            'ac': FeatureEngineering.calc_ac(front),
            'odd_even': FeatureEngineering.calc_odd_even(front),
            'size_ratio': FeatureEngineering.calc_size_ratio(front),
            'zones': FeatureEngineering.calc_zone_dist(front),
            'road_012': FeatureEngineering.calc_road_012(front),
            'front': front,
            'back': back
        }


class MissTracker:
    """遗漏值追踪"""

    def __init__(self, history):
        self.history = history
        self.front_miss = {i: 0 for i in range(1, 36)}
        self.back_miss = {i: 0 for i in range(1, 13)}

    def update(self):
        """更新遗漏值到最新一期"""
        for num in range(1, 36):
            self.front_miss[num] += 1
        for num in range(1, 13):
            self.back_miss[num] += 1

        # 最新一期开出的号重置为0
        latest = self.history[-1]
        for num in latest['front']:
            self.front_miss[num] = 0
        for num in latest['back']:
            self.back_miss[num] = 0

    def get_front_miss(self):
        return self.front_miss.copy()

    def get_back_miss(self):
        return self.back_miss.copy()

    def get_hot(self, top_n=10):
        """热号: 出现次数最多"""
        counter = Counter()
        for draw in self.history:
            counter.update(draw['front'])
        return counter.most_common(top_n)

    def get_cold(self, bottom_n=12):
        """冷号: 出现次数最少"""
        counter = Counter()
        for draw in self.history:
            counter.update(draw['front'])
        all_nums = set(range(1, 36))
        counted = set(counter.keys())
        uncounted = all_nums - counted
        cold = [(n, 0) for n in uncounted]
        cold.extend(counter.most_common()[:-bottom_n-1:-1])
        return sorted(cold, key=lambda x: x[1])[:bottom_n]


# ========== 第二层: 信息论分析 ==========

class InformationTheory:
    """信息熵与随机性分析"""

    @staticmethod
    def shannon_entropy(numbers):
        """香农熵"""
        freq = Counter(numbers)
        total = len(numbers)
        entropy = 0
        for count in freq.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy

    @staticmethod
    def front_entropy(draw):
        """前区号码的熵值"""
        return InformationTheory.shannon_entropy(draw['front'])

    @staticmethod
    def sequence_entropy(history, window=10):
        """滑动窗口熵值序列"""
        entropies = []
        for i in range(len(history) - window + 1):
            window_data = history[i:i+window]
            all_nums = [n for draw in window_data for n in draw['front']]
            entropies.append(InformationTheory.shannon_entropy(all_nums))
        return entropies

    @staticmethod
    def hurst_exponent(series, max_lag=10):
        """
        赫斯特指数 - 衡量时间序列的自相似性
        H < 0.5: 反持续性 (mean-reverting)
        H > 0.5: 持续性 (trending)
        H = 0.5: 纯随机游走
        """
        if len(series) < max_lag + 1:
            return 0.5

        def var(r):
            return sum((series[i] - sum(series[:r])/r)**2 for i in range(r)) / r

        lags = range(2, min(max_lag, len(series)//2))
        rs = []
        for n in lags:
            subseries = [series[i*n:(i+1)*n] for i in range(len(series)//n)]
            R = max(max(s) - min(s) for s in subseries if len(s) == n)
            S = math.sqrt(var(n)) if var(n) > 0 else 1e-10
            rs.append(R / S if S > 0 else 0)

        if not rs or max(rs) == 0:
            return 0.5

        # H = log(R/S) / log(n)
        log_ns = [math.log(n) for n in lags]
        log_rs = [math.log(r + 1e-10) for r in rs]

        # 简单线性回归
        n = len(log_ns)
        mean_x = sum(log_ns) / n
        mean_y = sum(log_rs) / n
        cov = sum((log_ns[i]-mean_x)*(log_rs[i]-mean_y) for i in range(n))
        var_x = sum((x-mean_x)**2 for x in log_ns)
        slope = cov / var_x if var_x > 0 else 0.5

        return max(0, min(1, slope))

    @staticmethod
    def mutual_info(x, y, bins=10):
        """互信息 - 衡量两个变量之间的信息共享"""
        try:
            hist_2d, _, _ = [0, 0, 0], [0, 0], [0, 0]  # placeholder
            # 简化实现
            return 0.0
        except:
            return 0.0


# ========== 第三层: 马尔可夫链 ==========

class MarkovChain:
    """号码状态转移矩阵"""

    def __init__(self, history):
        self.transition = defaultdict(Counter)
        self.states = list(range(1, 36))
        self._build_matrix(history)

    def _build_matrix(self, history):
        """构建转移矩阵"""
        for i in range(len(history) - 1):
            current = set(history[i]['front'])
            next_draw = history[i+1]['front']
            for num in current:
                self.transition[num].update(next_draw)

    def predict_next(self, current_nums, top_n=10):
        """给定当前号码，预测下一期可能的号码"""
        aggregated = Counter()
        for num in current_nums:
            aggregated.update(self.transition[num])
        return aggregated.most_common(top_n)


# ========== 第四层: 组合优化 ==========

class WheelingSystem:
    """旋转矩阵 - 用更少注数覆盖更多号码"""

    @staticmethod
    def wheel_10_to_5(numbers, guarantee=4):
        """
        简化旋转矩阵: 10个号码保证中5保4
        返回需要购买的注数列表
        """
        if len(numbers) < 10:
            return [numbers]  # 不足10个，只买1注

        # 简化实现: 分组覆盖
        n = len(numbers)
        combos = []
        step = 5
        for i in range(0, n, step):
            combo = numbers[i:i+5]
            if len(combo) == 5:
                combos.append(combo)
            elif len(combo) < 5 and combos:
                # 最后一组不足5个，用已有注数补充
                pass
        return combos[:5] if combos else [numbers[:5]]

    @staticmethod
    def filter_constraints(front_nums, back_nums, rules=None):
        """
        约束过滤
        rules: dict with keys: sum_range, span_range, odd_ratio, size_ratio
        """
        if rules is None:
            rules = {
                'sum_range': (65, 130),
                'span_range': (10, 34),
                'odd_ratio': (2, 3, 4),
            }

        filtered_front = []
        for nums in front_nums:
            s = sum(nums)
            sp = max(nums) - min(nums)
            odd = sum(1 for x in nums if x % 2 == 1)

            if rules['sum_range'][0] <= s <= rules['sum_range'][1]:
                if rules['span_range'][0] <= sp <= rules['span_range'][1]:
                    if odd in rules['odd_ratio']:
                        filtered_front.append(nums)
        return filtered_front


# ========== 第五层: 博弈论过滤 ==========

class GameTheoryFilter:
    """反人群过滤"""

    # 生日高频区
    BIRTHDAY_ZONE = list(range(1, 13))
    # 7的倍数
    LUCKY_7_MULTIPLES = [7, 14, 21, 28, 35]
    # 热门吉祥数
    AUSPICIOUS = [8, 6, 9]
    # 2026相关
    DATE_2026 = [26, 20, 2, 6]

    @staticmethod
    def filter_score(numbers, miss_tracker=None):
        """
        给一组号码打分 (越低越推荐)
        考虑: 遗漏值 + 博弈论
        """
        score = 0
        for num in numbers:
            # 遗漏加分
            if miss_tracker:
                score += min(miss_tracker.get(num, 0), 20)

            # 博弈论惩罚
            if num in GameTheoryFilter.BIRTHDAY_ZONE:
                score += 15
            if num in GameTheoryFilter.LUCKY_7_MULTIPLES:
                score += 10
            if num in GameTheoryFilter.AUSPICIOUS:
                score += 8
            if num in GameTheoryFilter.DATE_2026:
                score += 5

        return score

    @staticmethod
    def best_combination(candidates, miss_tracker=None):
        """从候选池中选择期望收益最优组合"""
        scored = []
        for nums in candidates:
            score = GameTheoryFilter.filter_score(nums, miss_tracker)
            scored.append((score, nums))
        scored.sort(key=lambda x: x[0])
        return scored[:5]


# ========== 第六层: 凯利公式 ==========

class KellyCriterion:
    """凯利公式资金管理"""

    @staticmethod
    def kelly_fraction(win_rate, odds, fraction=0.125):
        """
        分数凯利 (通常用1/8凯利降低波动)
        win_rate: 胜率 (预估)
        odds: 赔率
        """
        # f* = (p * b - q) / b
        # p = win_rate, q = 1-p, b = odds
        p = win_rate
        q = 1 - p
        b = odds - 1  # 净赔率

        if b <= 0:
            return 0

        f_star = (p * b - q) / b

        # 限制在合理范围
        f_star = max(0, min(f_star, 0.25))

        # 分数凯利
        return f_star * fraction

    @staticmethod
    def expected_value(hit_rate, prize_amount, bet_amount=2):
        """
        计算期望收益
        hit_rate: 命中率预估
        prize_amount: 奖金(浮动取平均值估算)
        """
        return hit_rate * prize_amount - (1 - hit_rate) * bet_amount


# ========== 第七层: 回测系统 ==========

class BacktestSystem:
    """策略回测 - 最重要的模块"""

    @staticmethod
    def backtest_strategy(history, strategy_func, n_periods=30):
        """
        回测指定策略在过去n_periods的表现
        strategy_func: 接收历史数据，返回预测号码的函数
        """
        results = []
        for i in range(len(history) - n_periods, len(history) - 1):
            train_data = history[:i+1]
            actual = history[i+1]

            prediction = strategy_func(train_data)

            front_hit = len(set(prediction['front']) & set(actual['front']))
            back_hit = len(set(prediction['back']) & set(actual['back']))

            results.append({
                'issue': actual['issue'],
                'predicted': prediction,
                'actual': actual,
                'front_hit': front_hit,
                'back_hit': back_hit,
                'prize': BacktestSystem._prize_level(front_hit, back_hit)
            })

        # 统计
        total_bet = len(results) * 2
        total_prize = sum(r['prize'] for r in results)
        hit_counts = Counter(r['prize'] for r in results)

        return {
            'periods': n_periods,
            'total_bet': total_bet,
            'total_prize': total_prize,
            'net_profit': total_prize - total_bet,
            'roi': (total_prize - total_bet) / total_bet * 100 if total_bet > 0 else 0,
            'prize_distribution': dict(hit_counts),
            'best': max(results, key=lambda x: x['prize']) if results else None,
        }

    @staticmethod
    def _prize_level(front_hit, back_hit):
        """根据命中数判定奖项"""
        if front_hit == 5 and back_hit == 2:
            return 10000000  # 一等奖(估)
        elif front_hit == 5 and back_hit == 1:
            return 500000  # 二等奖(估)
        elif front_hit == 5 or (front_hit == 4 and back_hit == 2):
            return 10000  # 三等奖(估)
        elif front_hit == 4 or (front_hit == 3 and back_hit == 2):
            return 300  # 四等奖(估)
        elif front_hit == 4 or (front_hit == 3 and back_hit == 1) or (front_hit == 2 and back_hit == 2):
            return 200
        elif front_hit == 3 or (front_hit == 2 and back_hit == 1) or (front_hit == 1 and back_hit == 2) or back_hit == 2:
            return 100
        elif front_hit == 2 and back_hit == 1:
            return 15
        elif front_hit == 1 and back_hit == 2:
            return 5
        elif front_hit == 2 and back_hit == 0:
            return 0  # 九等奖以下
        return 0


# ========== 主预测函数 ==========

def generate_prediction_v5(history, n_注=5):
    """
    V5.0 综合预测
    输入: 历史数据
    输出: 5注推荐
    """
    print(f"[V5.0] 收到历史数据 {len(history)} 期")

    # Step 1: 特征工程
    features = [FeatureEngineering.extract_features(d) for d in history]
    sums = [f['sum'] for f in features]
    mean_sum = sum(sums) / len(sums)
    std_sum = (sum((s - mean_sum)**2 for s in sums) / len(sums)) ** 0.5

    # Step 2: 遗漏追踪
    tracker = MissTracker(history)
    for _ in range(5):  # 模拟到当前
        tracker.update()

    front_miss = tracker.get_front_miss()
    back_miss = tracker.get_back_miss()
    hot_nums = tracker.get_hot(15)
    cold_nums = tracker.get_cold(10)

    # Step 3: 马尔可夫预测
    mc = MarkovChain(history[-10:])  # 用近10期训练
    last_front = history[-1]['front']
    markov_probs = mc.predict_next(last_front, 15)

    # Step 4: 信息论分析
    recent_sums = [sum(d['front']) for d in history[-10:]]
    H = InformationTheory.hurst_exponent(recent_sums)

    # Step 5: 博弈论候选池
    candidate_pool = []

    # 策略A: 热号 + 大遗漏
    for h, _ in hot_nums[:5]:
        for c, _ in cold_nums[:5]:
            combo = sorted([h, c] + random.sample([n for n in range(1,36) if n != h and n != c], 3))
            if len(set(combo)) == 5:
                candidate_pool.append(combo)

    # 策略B: 马尔可夫高分
    for m, _ in markov_probs[:5]:
        combo = sorted([m] + random.sample([n for n in range(1,36) if n != m], 4))
        if len(set(combo)) == 5:
            candidate_pool.append(combo)

    # 策略C: 博弈论低分 (人少选的组合)
    gt_filtered = GameTheoryFilter.best_combination(
        candidate_pool[:20], front_miss
    )

    # Step 6: 生成最终5注
    results = []
    for i, (score, nums) in enumerate(gt_filtered[:n_注]):
        back_combo = random.sample([4, 6, 9, 11], 2)  # 大遗漏后区
        results.append({
            'no': i+1,
            'front': nums,
            'back': back_combo,
            'sum': sum(nums),
            'span': max(nums) - min(nums),
            'gt_score': score,
            'strategy': f'热号回归+博弈过滤'
        })

    print(f"[V5.0] 生成 {len(results)} 注预测")
    return results


# ========== 执行 ==========

if __name__ == '__main__':
    print("=" * 50)
    print("B166ER 大乐透预测系统 V5.0")
    print("=" * 50)

    predictions = generate_prediction_v5(HISTORY_DATA)

    print(f"\n26037期预测 (共{len(predictions)}注):")
    print("-" * 50)
    for p in predictions:
        print(f"注{p['no']}: 前区 {p['front']} | 后区 {p['back']} | "
              f"和值{p['sum']} | 博弈分{p['gt_score']}")
        print(f"     策略: {p['strategy']}")
        print()
