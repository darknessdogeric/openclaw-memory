# -*- coding: utf-8 -*-
"""B166ER 大乐透预测 V1.1 - 26033期预测"""
import random
import json
from datetime import datetime
from collections import Counter

# 最新开奖数据（包含26032期）
RECENT_DRAWS = [
    # 26030期 - 2026年3月17日(周一)
    {'front': [7, 14, 22, 28, 35], 'back': [2, 8], 'date': '2026-03-17', 'issue': '26030'},
    # 26031期 - 2026年3月25日(周三) - 需补充
    # {'front': [?, ?, ?, ?, ?], 'back': [?, ?], 'date': '2026-03-25', 'issue': '26031'},
    # 26032期 - 2026年3月28日(周六) - 已开奖
    {'front': [3, 4, 19, 26, 32], 'back': [1, 12], 'date': '2026-03-28', 'issue': '26032'},
]

class LottoPredictorV11:
    """大乐透预测模型 V1.1"""
    
    def __init__(self, recent_draws):
        self.recent = recent_draws
        self.front_range = range(1, 36)
        self.back_range = range(1, 13)
        self._calculate_statistics()
    
    def _calculate_statistics(self):
        front_all = []
        back_all = []
        for draw in self.recent[-30:] if len(self.recent) > 30 else self.recent:
            front_all.extend(draw.get('front', []))
            back_all.extend(draw.get('back', []))
        
        self.front_freq = Counter(front_all)
        self.back_freq = Counter(back_all)
        
        self.hot_front = [n for n, c in self.front_freq.most_common(10)] if self.front_freq else []
        self.cold_front = [n for n in self.front_range if n not in self.hot_front][:10]
        self.hot_back = [n for n, c in self.back_freq.most_common(4)] if self.back_freq else []
        self.cold_back = [n for n in self.back_range if n not in self.hot_back][:4]
    
    def _generate_front_zone_strategy(self):
        zones = {
            0: list(range(1, 8)),
            1: list(range(8, 15)),
            2: list(range(15, 22)),
            3: list(range(22, 29)),
            4: list(range(29, 36))
        }
        
        selected = []
        hot_zones = random.sample([0, 1, 2, 3, 4], 3)
        cold_zones = [z for z in [0, 1, 2, 3, 4] if z not in hot_zones]
        
        for zone_idx in hot_zones:
            zone_nums = zones[zone_idx]
            hot_in_zone = [n for n in zone_nums if n in self.hot_front]
            if hot_in_zone and random.random() < 0.7:
                selected.append(random.choice(hot_in_zone))
            else:
                selected.append(random.choice(zone_nums))
        
        for zone_idx in cold_zones:
            zone_nums = zones[zone_idx]
            cold_in_zone = [n for n in zone_nums if n in self.cold_front]
            if cold_in_zone and random.random() < 0.6:
                selected.append(random.choice(cold_in_zone))
            else:
                selected.append(random.choice(zone_nums))
        
        return sorted(selected)
    
    def _check_constraints(self, front):
        total = sum(front)
        if not (70 <= total <= 130):
            return False
        
        span = max(front) - min(front)
        if not (12 <= span <= 32):
            return False
        
        odd = sum(1 for n in front if n % 2 == 1)
        if odd not in [2, 3]:
            return False
        
        big = sum(1 for n in front if n >= 18)
        if big not in [2, 3]:
            return False
        
        zones_covered = set()
        for n in front:
            zones_covered.add((n-1) // 7)
        if len(zones_covered) < 4:
            return False
        
        consecutive = sum(1 for i in range(4) if front[i+1] - front[i] == 1)
        if consecutive > 1:
            return False
        
        return True
    
    def _generate_back_balanced(self):
        for _ in range(50):
            strategy = random.choice(['odd_even', 'both_odd', 'both_even'])
            
            if strategy == 'odd_even':
                odd_nums = [n for n in self.back_range if n % 2 == 1]
                even_nums = [n for n in self.back_range if n % 2 == 0]
                back = [random.choice(odd_nums), random.choice(even_nums)]
            elif strategy == 'both_odd':
                odd_nums = [n for n in self.back_range if n % 2 == 1]
                back = random.sample(odd_nums, 2)
            else:
                even_nums = [n for n in self.back_range if n % 2 == 0]
                back = random.sample(even_nums, 2)
            
            back = sorted(back)
            recent_backs = [set(d.get('back', [])) for d in self.recent[-3:]]
            if set(back) not in recent_backs:
                return back
        
        return sorted(random.sample(list(self.back_range), 2))
    
    def _generate_single(self, max_attempts=200):
        for _ in range(max_attempts):
            front = self._generate_front_zone_strategy()
            if not self._check_constraints(front):
                continue
            back = self._generate_back_balanced()
            recent_full = [(set(d.get('front', [])), set(d.get('back', []))) for d in self.recent[-5:]]
            if (set(front), set(back)) in recent_full:
                continue
            return {
                'front': front,
                'back': back,
                'sum': sum(front),
                'span': max(front) - min(front),
                'odd_even': (sum(1 for n in front if n % 2 == 1), sum(1 for n in front if n % 2 == 0)),
                'big_small': (sum(1 for n in front if n >= 18), sum(1 for n in front if n < 18))
            }
        
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
        results = []
        for i in range(count):
            result = self._generate_single()
            result['no'] = i + 1
            results.append(result)
        return results

# 运行预测
predictor = LottoPredictorV11(RECENT_DRAWS)

print("=" * 65)
print("[B166ER] Super Lotto Prediction V1.1 - 26033")
print("=" * 65)
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Target: 26033 (2026-03-30 Monday)")
print(f"Strategy: 5-zone coverage + hot/cold balance + sum/span constraints")
print(f"Reference: 26032 Front[03 04 19 26 32] Back[01 12]")
print()
print(f"HOT (Front): {' '.join([f'{n:02d}' for n in predictor.hot_front[:8]])}")
print(f"COLD (Front): {' '.join([f'{n:02d}' for n in predictor.cold_front[:8]])}")
print(f"HOT (Back): {' '.join([f'{n:02d}' for n in predictor.hot_back])}")
print()
print("5 Predictions:")
print("-" * 65)

predictions = predictor.predict(count=5)
for pred in predictions:
    front_str = ' '.join([f"{n:02d}" for n in pred['front']])
    back_str = ' '.join([f"{n:02d}" for n in pred['back']])
    print(f"Set {pred['no']}: Front[{front_str}] Back[{back_str}]")
    print(f"        Sum:{pred['sum']} Span:{pred['span']} Odd/Even:{pred['odd_even'][0]}:{pred['odd_even'][1]} Big/Small:{pred['big_small'][0]}:{pred['big_small'][1]}")
    print()

print("=" * 65)
print("Disclaimer: For entertainment only. Lottery is completely random.")
print("Please play responsibly.")
print("=" * 65)
