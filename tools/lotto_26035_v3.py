# -*- coding: utf-8 -*-
"""
B166ER 大乐透预测 V3.0 - 整合版
基于专业知识库的多模型融合预测

更新日志:
- V3.0: 整合知识库，增加多模型融合
- V2.0: 热号多注覆盖 + 后区遗漏追踪 + 冷转热预警
- V1.1: 基础统计模型
"""
import random
import json
from datetime import datetime
from collections import Counter

# ============================================================================
# 知识库：历史开奖数据（来自17500.cn官方数据）
# ============================================================================
RECENT_DRAWS = [
    # 26030期 - 2026年3月17日(周一)
    {'front': [7, 14, 22, 28, 35], 'back': [2, 8], 'date': '2026-03-17', 'issue': '26030'},
    # 26031期 - 2026年3月25日(周三)
    {'front': [6, 8, 22, 29, 34], 'back': [5, 7], 'date': '2026-03-25', 'issue': '26031'},
    # 26032期 - 2026年3月28日(周六)
    {'front': [3, 4, 19, 26, 32], 'back': [1, 12], 'date': '2026-03-28', 'issue': '26032'},
    # 26033期 - 2026年3月30日(周一) - 官方开奖结果
    {'front': [3, 5, 7, 9, 18], 'back': [2, 10], 'date': '2026-03-30', 'issue': '26033'},
]

# ============================================================================
# 知识库：已知的预测理论
# ============================================================================
KNOWLEDGE_BASE = """
=== 大乐透预测知识库 V1.0 ===

【基础规则】
- 前区: 01-35 选5个 (C(35,5)=32,428,492种)
- 后区: 01-12 选2个 (C(12,2)=66种)
- 总组合: 约21亿种
- 返奖率: 约50-55%
- 一等奖概率: 约1/21亿

【历史统计规律】
1. 频率分析: 前区热号07、22、03出现频率较高
2. 遗漏追踪: 后区02遗漏较长，02在近4期出现2次
3. 区间分布: Zone 0 (01-07) 近4期出现较多
4. 奇偶比例: 3:2或2:3最常见
5. 和值范围: 80-110高频区间

【重要结论】
- 彩票是独立随机事件
- 历史频率不影响未来结果
- 任何预测模型都不能提高中奖概率
- 预测仅供娱乐，不能作为投注依据
"""

# ============================================================================
# 多模型预测类
# ============================================================================
class LottoPredictorV30:
    """大乐透预测模型 V3.0 - 多模型融合"""

    def __init__(self, recent_draws):
        self.recent = recent_draws
        self.front_range = range(1, 36)
        self.back_range = range(1, 13)
        self._calculate_all_stats()

    def _calculate_all_stats(self):
        """计算所有统计数据"""
        # 前区频率统计（近15期）
        front_all = []
        back_all = []
        for draw in self.recent[-15:]:
            front_all.extend(draw.get('front', []))
            back_all.extend(draw.get('back', []))

        self.front_freq = Counter(front_all)
        self.back_freq = Counter(back_all)

        # 热号（前区）
        self.hot_front = [n for n, c in self.front_freq.most_common(12)]
        # 冷号（前区）
        self.cold_front = [n for n in self.front_range if n not in self.hot_front[:10]]

        # 近期出现过的号
        recent_3_front = []
        for draw in self.recent[-3:]:
            recent_3_front.extend(draw.get('front', []))
        self.recent_3_front = set(recent_3_front)

        recent_2_front = []
        for draw in self.recent[-2:]:
            recent_2_front.extend(draw.get('front', []))
        self.recent_2_front = set(recent_2_front)

        # 后区遗漏追踪
        self.back_missing = {}
        for num in self.back_range:
            last_appear = None
            for i, draw in enumerate(reversed(self.recent[-20:])):
                if num in draw.get('back', []):
                    last_appear = i
                    break
            self.back_missing[num] = last_appear if last_appear is not None else 20

        # 前区遗漏追踪
        self.front_missing = {}
        for num in self.front_range:
            last_appear = None
            for i, draw in enumerate(reversed(self.recent[-15:])):
                if num in draw.get('front', []):
                    last_appear = i
                    break
            self.front_missing[num] = last_appear if last_appear is not None else 15

        # 和值统计
        self.sum_values = [sum(d['front']) for d in self.recent[-10:]]
        self.avg_sum = sum(self.sum_values) / len(self.sum_values) if self.sum_values else 95

        # 跨度统计
        self.span_values = [max(d['front']) - min(d['front']) for d in self.recent[-10:]]
        self.avg_span = sum(self.span_values) / len(self.span_values) if self.span_values else 28

    def model_frequency(self):
        """模型1: 频率分析模型"""
        # 基于历史频率选择
        selected = []
        # 选3个热号
        selected.extend(random.sample(self.hot_front[:8], 3))
        # 选1个温号
        mid_freq = [n for n in self.front_range if n not in self.hot_front[:8] and n not in self.cold_front[:5]]
        if mid_freq:
            selected.append(random.choice(mid_freq))
        # 选1个冷号
        if self.cold_front and len(selected) < 5:
            selected.append(random.choice(self.cold_front[:5]))
        return sorted(selected[:5])

    def model_missing(self):
        """模型2: 遗漏追踪模型"""
        selected = []
        # 选择遗漏值较大的号
        sorted_by_missing = sorted(self.front_missing.items(), key=lambda x: x[1], reverse=True)
        top_missing = [n for n, m in sorted_by_missing[:10] if n in self.hot_front[:10] or m > 5]

        if len(top_missing) >= 3:
            selected.extend(random.sample(top_missing[:6], 3))
        else:
            selected.extend(random.sample(self.hot_front[:5], 3))

        # 补齐5个
        while len(selected) < 5:
            avail = [n for n in self.front_range if n not in selected]
            if avail:
                selected.append(random.choice(avail))
        return sorted(selected[:5])

    def model_recent(self):
        """模型3: 近期规律模型"""
        selected = []
        # 策略: 近3期重复号权重高
        recent_candidates = list(self.recent_3_front)

        # 选择2-3个近期号
        if len(recent_candidates) >= 3:
            selected.extend(random.sample(recent_candidates[:8], 2))

        # 补齐（选择遗漏5-10期的号）
        mid_missing = [n for n in self.front_range
                       if 5 <= self.front_missing.get(n, 10) <= 10
                       and n not in selected]
        while len(selected) < 5:
            if mid_missing and random.random() < 0.5:
                selected.append(random.choice(mid_missing))
                mid_missing.remove(selected[-1])
            else:
                avail = [n for n in self.front_range if n not in selected]
                if avail:
                    selected.append(random.choice(avail))
        return sorted(selected[:5])

    def model_zones(self):
        """模型4: 区间分布模型"""
        zones = {
            0: list(range(1, 8)),
            1: list(range(8, 15)),
            2: list(range(15, 22)),
            3: list(range(22, 29)),
            4: list(range(29, 36))
        }

        # 统计近10期各区出现次数
        zone_counts = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0}
        for draw in self.recent[-10:]:
            for num in draw['front']:
                zone_counts[(num - 1) // 7] += 1

        # 选择较热的区（但避免全热）
        selected = []
        for zone_idx, count in sorted(zone_counts.items(), key=lambda x: x[1], reverse=True):
            if len(selected) >= 5:
                break
            zone_nums = zones[zone_idx]
            # 每区选1个，优先选热号
            hot_in_zone = [n for n in zone_nums if n in self.hot_front[:8] and n not in selected]
            if hot_in_zone:
                selected.append(random.choice(hot_in_zone))
            else:
                avail = [n for n in zone_nums if n not in selected]
                if avail:
                    selected.append(random.choice(avail))

        return sorted(selected[:5])

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
        zones_covered = set()
        for n in front:
            zones_covered.add((n - 1) // 7)
        if len(zones_covered) < 4:
            return False
        consecutive = sum(1 for i in range(4) if front[i + 1] - front[i] == 1)
        if consecutive > 1:
            return False
        return True

    def _generate_back(self):
        """后区生成 - 多策略融合"""
        missing_sorted = sorted(self.back_missing.items(), key=lambda x: x[1], reverse=True)
        big_missing = [n for n, m in missing_sorted if m >= 5]

        # 策略: 至少选1个大遗漏号
        if big_missing and random.random() < 0.85:
            back = [random.choice(big_missing[:3])]
        else:
            back = [random.choice(list(self.back_range))]

        remaining = [n for n in self.back_range if n not in back]
        if remaining:
            # 混合: 50%热号，50%遗漏号
            if random.random() < 0.5:
                hot = [n for n in remaining if n in self.back_freq.most_common(4)]
                back.append(random.choice(hot if hot else remaining[:4]))
            else:
                rem_sorted = sorted(remaining, key=lambda x: self.back_missing.get(x, 0), reverse=True)
                back.append(random.choice(rem_sorted[:4]))

        return sorted(back[:2])

    def generate_ensemble(self, count=5):
        """融合多模型生成预测"""
        results = []

        for i in range(count):
            # 轮询使用不同模型
            model_id = i % 4

            if model_id == 0:
                front = self.model_frequency()
            elif model_id == 1:
                front = self.model_missing()
            elif model_id == 2:
                front = self.model_recent()
            else:
                front = self.model_zones()

            # 检查约束
            attempts = 0
            while not self._check_constraints(front) and attempts < 50:
                # 修复约束问题
                if sum(front) > 130:
                    # 替换最小的几个
                    front = sorted(random.sample(list(self.front_range), 5))
                else:
                    break
                attempts += 1

            back = self._generate_back()

            # 检查是否与最近2期完全重复
            recent_front = [set(d.get('front', [])) for d in self.recent[-2:]]
            recent_back = [set(d.get('back', [])) for d in self.recent[-2:]]
            if set(front) in recent_front and set(back) in recent_back:
                # 换一个后区
                back = self._generate_back()

            results.append({
                'no': i + 1,
                'front': sorted(front),
                'back': sorted(back),
                'sum': sum(front),
                'span': max(front) - min(front),
                'odd_even': (sum(1 for n in front if n % 2 == 1), sum(1 for n in front if n % 2 == 0)),
                'big_small': (sum(1 for n in front if n >= 18), sum(1 for n in front if n < 18)),
                'model': ['频率', '遗漏', '近期', '区间'][model_id]
            })

        return results

def save_prediction(issue, predictions, review=None):
    """保存预测结果"""
    filename = f"lottery_history/prediction_{issue}.json"
    data = {
        'issue': issue,
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'predictions': predictions,
        'last_issue_review': review,
        'model_version': 'V3.0',
        'knowledge_base_version': 'V1.0',
        'strategy': '多模型融合: 频率+遗漏+近期+区间'
    }
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[OK] Saved: {filename}")

def main():
    print("=" * 70)
    print("[B166ER] Super Lotto Prediction V3.0 - Multi-Model Ensemble")
    print("=" * 70)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Target: 26035 (2026-04-04 Saturday)")
    print()

    predictor = LottoPredictorV30(RECENT_DRAWS)

    # 显示统计信息
    print("【知识库统计 (近15期)】")
    print(f"前区热号: {' '.join([f'{n:02d}' for n in predictor.hot_front[:8]])}")
    print(f"近3期重复号: {' '.join([f'{n:02d}' for n in predictor.recent_3_front])}")
    print(f"平均和值: {predictor.avg_sum:.1f}")
    print(f"平均跨度: {predictor.avg_span:.1f}")
    print()

    print("【后区遗漏追踪】")
    for num in range(1, 13):
        m = predictor.back_missing.get(num, 20)
        bar = '#' * min(m, 10) + '-' * (10 - min(m, 10))
        print(f"  {num:02d}: {bar} ({m}期未出)")
    print()

    # 26034期复盘
    print("=" * 70)
    print("【26034期复盘 - 待开奖】")
    print("=" * 70)
    print("注: 26034期(2026-04-02)尚未开奖，将基于26030-26033数据分析")
    print()

    # 生成26035期预测
    print("【26035期预测 - 5注 (多模型融合)】")
    print("-" * 70)

    predictions = predictor.generate_ensemble(count=5)
    save_prediction('26035', predictions)

    for pred in predictions:
        front_str = ' '.join([f"{n:02d}" for n in pred['front']])
        back_str = ' '.join([f"{n:02d}" for n in pred['back']])
        print(f"注{pred['no']} [{pred['model']}]: 前区[{front_str}] 后区[{back_str}]")
        print(f"       和值:{pred['sum']:3d} 跨度:{pred['span']:2d} 奇偶:{pred['odd_even'][0]}:{pred['odd_even'][1]} 大小:{pred['big_small'][0]}:{pred['big_small'][1]}")

    print()
    print("=" * 70)
    print("Disclaimer: 彩票是随机事件，预测仅供娱乐，请理性购彩")
    print("=" * 70)

if __name__ == '__main__':
    main()