# -*- coding: utf-8 -*-
"""B166ER 大乐透预测 V2.0 - 26034期预测
改进版：热号多注覆盖 + 后区遗漏追踪 + 冷转热预警
"""
import random
import json
from datetime import datetime
from collections import Counter

# 历史开奖数据（持续更新）
RECENT_DRAWS = [
    # 26030期 - 2026年3月17日(周一)
    {'front': [7, 14, 22, 28, 35], 'back': [2, 8], 'date': '2026-03-17', 'issue': '26030'},
    # 26031期 - 2026年3月25日(周三)
    {'front': [6, 8, 22, 29, 34], 'back': [5, 7], 'date': '2026-03-25', 'issue': '26031'},
    # 26032期 - 2026年3月28日(周六)
    {'front': [3, 4, 19, 26, 32], 'back': [1, 12], 'date': '2026-03-28', 'issue': '26032'},
    # 26033期 - 2026年3月30日(周一) - 已开奖，用于分析
    {'front': [3, 5, 7, 9, 18], 'back': [2, 11], 'date': '2026-03-30', 'issue': '26033'},
]

class LottoPredictorV20:
    """大乐透预测模型 V2.0 - 改进版"""
    
    def __init__(self, recent_draws):
        self.recent = recent_draws
        self.front_range = range(1, 36)
        self.back_range = range(1, 13)
        self._calculate_statistics()
    
    def _calculate_statistics(self):
        """计算统计数据"""
        front_all = []
        back_all = []
        for draw in self.recent[-15:]:
            front_all.extend(draw.get('front', []))
            back_all.extend(draw.get('back', []))
        
        self.front_freq = Counter(front_all)
        self.back_freq = Counter(back_all)
        
        # 热号：近15期出现次数多的
        self.hot_front = [n for n, c in self.front_freq.most_common(12)]
        # 冷号：近15期出现次数少或未出现的
        self.cold_front = [n for n in self.front_range if n not in self.hot_front[:10]]
        
        # 后区热号
        self.hot_back = [n for n, c in self.back_freq.most_common(6)]
        # 后区遗漏追踪
        self.back_missing = {}
        for num in self.back_range:
            last_appear = None
            for i, draw in enumerate(reversed(self.recent[-15:])):
                if num in draw.get('back', []):
                    last_appear = i
                    break
            self.back_missing[num] = last_appear if last_appear is not None else 15
        
        # 近期重复号（近3期出现过的）
        recent_3_front = []
        for draw in self.recent[-3:]:
            recent_3_front.extend(draw.get('front', []))
        self.recent_3_front = set(recent_3_front)
        
        # 冷转热预警（遗漏>10期的号）
        self.cold_to_hot = []
        for num in self.front_range:
            appearances = [i for i, draw in enumerate(self.recent[-15:]) if num in draw.get('front', [])]
            if appearances and appearances[-1] >= 10:
                self.cold_to_hot.append(num)
    
    def _generate_front_with_hot_multi_cover(self):
        """前区生成 - 热号多注覆盖策略"""
        zones = {
            0: list(range(1, 8)),
            1: list(range(8, 15)),
            2: list(range(15, 22)),
            3: list(range(22, 29)),
            4: list(range(29, 36))
        }
        
        selected = []
        
        # Step 1: 近期重复号（近3期出现过的）- 至少选2个
        recent_hot = [n for n in self.recent_3_front if n in self.hot_front[:8]]
        if len(recent_hot) >= 2:
            selected.extend(random.sample(recent_hot[:6], 2))
        
        # Step 2: 冷转热预警号 - 至少选1个
        if self.cold_to_hot and random.random() < 0.7:
            ctw = random.choice(self.cold_to_hot[:3])
            if ctw not in selected:
                selected.append(ctw)
        
        # Step 3: 补齐前区到5个（区域分散 + 热号优先）
        while len(selected) < 5:
            zone_idx = (len(selected) * 3) % 5  # 分散选区
            zone_nums = zones[zone_idx]
            
            # 区域内优先热号
            hot_in_zone = [n for n in zone_nums if n in self.hot_front[:8] and n not in selected]
            if hot_in_zone and random.random() < 0.6:
                selected.append(random.choice(hot_in_zone))
            else:
                cold_in_zone = [n for n in zone_nums if n not in selected]
                if cold_in_zone:
                    selected.append(random.choice(cold_in_zone))
        
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
        
        # 5区至少覆盖4区
        zones_covered = set()
        for n in front:
            zones_covered.add((n-1) // 7)
        if len(zones_covered) < 4:
            return False
        
        # 连号不超过1组
        consecutive = sum(1 for i in range(4) if front[i+1] - front[i] == 1)
        if consecutive > 1:
            return False
        
        return True
    
    def _generate_back_with_missing_trace(self):
        """后区生成 - 遗漏追踪策略"""
        # 按遗漏次数排序（遗漏越多的权重越高）
        missing_sorted = sorted(self.back_missing.items(), key=lambda x: x[1], reverse=True)
        
        # 确保至少选1个"大遗漏号"（遗漏>5期）
        big_missing = [n for n, m in missing_sorted if m >= 5]
        
        # 另1个选热号或中等遗漏号
        if big_missing and random.random() < 0.8:
            back = [random.choice(big_missing)]
        else:
            back = [random.choice(self.hot_back[:4])]
        
        # 补齐第2个后区
        remaining = [n for n in self.back_range if n not in back]
        if remaining:
            # 混合策略：热号 + 遗漏号的组合
            if random.random() < 0.5:
                back.append(random.choice(self.hot_back[:4] if self.hot_back else remaining[:4]))
            else:
                remaining_sorted = sorted(remaining, key=lambda x: self.back_missing.get(x, 0), reverse=True)
                back.append(random.choice(remaining_sorted[:4]))
        
        return sorted(back[:2])
    
    def _generate_single(self, max_attempts=300):
        """生成单注"""
        for _ in range(max_attempts):
            front = self._generate_front_with_hot_multi_cover()
            if not self._check_constraints(front):
                continue
            back = self._generate_back_with_missing_trace()
            
            # 检查是否与最近2期完全重复
            recent_front = [set(d.get('front', [])) for d in self.recent[-2:]]
            recent_back = [set(d.get('back', [])) for d in self.recent[-2:]]
            if set(front) in recent_front and set(back) in recent_back:
                continue
            
            return {
                'front': sorted(front),
                'back': sorted(back),
                'sum': sum(front),
                'span': max(front) - min(front),
                'odd_even': (sum(1 for n in front if n % 2 == 1), sum(1 for n in front if n % 2 == 0)),
                'big_small': (sum(1 for n in front if n >= 18), sum(1 for n in front if n < 18))
            }
        
        # 兜底：随机生成
        front = sorted(random.sample(list(self.front_range), 5))
        back = sorted(random.sample(list(self.back_range), 2))
        return {
            'front': front,
            'back': back,
            'sum': sum(front),
            'span': max(front) - min(front),
            'odd_even': (sum(1 for n in front if n % 2 == 1), sum(1 for n in front if n % 2 == 0)),
            'big_small': (sum(1 for n in front if n >= 18), sum(1 for n in front if n < 18))
        }
    
    def predict(self, count=5):
        """生成预测"""
        results = []
        for i in range(count):
            result = self._generate_single()
            result['no'] = i + 1
            results.append(result)
        return results

def save_prediction(issue, predictions, actual=None):
    """保存预测结果到文件"""
    filename = f"lottery_history/prediction_{issue}.json"
    data = {
        'issue': issue,
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'predictions': predictions,
        'actual': actual,
        'model_version': 'V2.0'
    }
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[OK] Prediction saved: {filename}")

# 运行预测
predictor = LottoPredictorV20(RECENT_DRAWS)

print("=" * 70)
print("[B166ER] Super Lotto Prediction V2.0 - 26034")
print("=" * 70)
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Target: 26034 (2026-04-02 Thursday)")
print()
print(f"策略: V2.0 热号多注覆盖 + 后区遗漏追踪 + 冷转热预警")
print()

# 显示近期数据
print("【近15期热号统计】")
print(f"前区热号: {' '.join([f'{n:02d}' for n in predictor.hot_front[:8]])}")
print(f"后区热号: {' '.join([f'{n:02d}' for n in predictor.hot_back])}")
print(f"近3期重复号: {' '.join([f'{n:02d}' for n in predictor.recent_3_front]) if predictor.recent_3_front else '无'}")
print(f"冷转热预警: {' '.join([f'{n:02d}' for n in predictor.cold_to_hot[:5]]) if predictor.cold_to_hot else '无'}")
print()
print(f"【后区遗漏追踪】")
for num in range(1, 13):
    m = predictor.back_missing.get(num, 15)
    bar = '#' * min(m, 10) + '-' * (10 - min(m, 10))
    print(f"  {num:02d}: {bar} ({m}期未出)")
print()

print("5 Predictions (热号多注覆盖):")
print("-" * 70)

predictions = predictor.predict(count=5)

# 保存预测
save_prediction('26034', predictions)

for pred in predictions:
    front_str = ' '.join([f"{n:02d}" for n in pred['front']])
    back_str = ' '.join([f"{n:02d}" for n in pred['back']])
    print(f"注{pred['no']}: 前区[{front_str}] 后区[{back_str}]")
    print(f"      和值:{pred['sum']:3d} 跨度:{pred['span']:2d} 奇偶:{pred['odd_even'][0]}:{pred['odd_even'][1]} 大小:{pred['big_small'][0]}:{pred['big_small'][1]}")
    print()

print("=" * 70)
print("Disclaimer: For entertainment only. Lottery is completely random.")
print("Please play responsibly.")
print("=" * 70)

# 复盘26033期
print()
print("=" * 70)
print("【26033期复盘】")
print("=" * 70)
actual_front = [3, 5, 7, 9, 18]
actual_back = [2, 11]
print(f"实际开奖: 前区{actual_front} 后区{actual_back}")
print()

for pred in predictions:
    front_hit = len(set(pred['front']) & set(actual_front))
    back_hit = len(set(pred['back']) & set(actual_back))
    total = front_hit + back_hit
    
    if total >= 5:
        award = "一等奖"
    elif total == 4 and (front_hit == 4 or (front_hit == 3 and back_hit == 2)):
        award = "二等奖"
    elif total == 4:
        award = "三等奖"
    elif total == 3:
        award = "四等奖"
    elif total == 2:
        award = "五等奖"
    else:
        award = "谢谢参与"
    
    print(f"注{pred['no']}: 前区{front_hit}个 + 后区{back_hit}个 = {total}个 → {award}")

print()
print(f"26033期预测命中: 前区共{sum(len(set(p['front']) & set(actual_front)) for p in predictions)}个, 后区共{sum(len(set(p['back']) & set(actual_back)) for p in predictions)}个")