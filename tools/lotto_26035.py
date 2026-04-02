# -*- coding: utf-8 -*-
"""B166ER 大乐透预测 V2.0 - 26035期预测
基于26030-26033期历史规律分析生成
"""
import random
from datetime import datetime
from collections import Counter

# 历史开奖数据（官网核实）
RECENT_DRAWS = [
    {'front': [7, 14, 22, 28, 35], 'back': [2, 8], 'date': '2026-03-23', 'issue': '26030'},
    {'front': [6, 8, 22, 29, 34], 'back': [5, 7], 'date': '2026-03-25', 'issue': '26031'},
    {'front': [3, 4, 19, 26, 32], 'back': [1, 12], 'date': '2026-03-28', 'issue': '26032'},
    {'front': [3, 5, 7, 9, 18], 'back': [2, 11], 'date': '2026-03-30', 'issue': '26033'},
]

class LottoPredictorV20:
    def __init__(self, recent_draws):
        self.recent = recent_draws
        self.front_range = range(1, 36)
        self.back_range = range(1, 13)
        self._calculate_statistics()
    
    def _calculate_statistics(self):
        front_all = []
        back_all = []
        for draw in self.recent[-10:]:
            front_all.extend(draw.get('front', []))
            back_all.extend(draw.get('back', []))
        
        self.front_freq = Counter(front_all)
        self.back_freq = Counter(back_all)
        self.hot_front = [n for n, c in self.front_freq.most_common(12)]
        self.cold_front = [n for n in self.front_range if n not in self.hot_front[:8]]
        
        # 近3期重复号
        recent_3_front = []
        for draw in self.recent[-3:]:
            recent_3_front.extend(draw.get('front', []))
        self.recent_3_front = set(recent_3_front)
        
        # 近2期重复号（隔期重号重点）
        recent_2_front = []
        for draw in self.recent[-2:]:
            recent_2_front.extend(draw.get('front', []))
        self.recent_2_front = set(recent_2_front)
        
        # 后区遗漏追踪
        self.back_missing = {}
        for num in self.back_range:
            last_appear = None
            for i, draw in enumerate(reversed(self.recent[-15:])):
                if num in draw.get('back', []):
                    last_appear = i
                    break
            self.back_missing[num] = last_appear if last_appear is not None else 15
        
        # 前区遗漏（用于冷转热捕捉）
        self.front_missing = {}
        for num in self.front_range:
            last_appear = None
            for i, draw in enumerate(reversed(self.recent[-10:])):
                if num in draw.get('front', []):
                    last_appear = i
                    break
            self.front_missing[num] = last_appear if last_appear is not None else 10
    
    def _generate_front_v35(self):
        """26035期前区生成策略"""
        zones = {
            0: list(range(1, 8)),
            1: list(range(8, 15)),
            2: list(range(15, 22)),
            3: list(range(22, 29)),
            4: list(range(29, 36))
        }
        
        selected = []
        
        # Strategy 1: Interval repeat (numbers from 26032 may appear in 26035)
        # 26032: 03,04,19,26,32  26033: 03,05,07,09,18
        # 03 appeared 2x consecutively, watch for reversal
        # Focus: 04(1 interval), 19, 26, 32 (2 intervals)
        interval_candidates = [n for n in [4, 19, 26, 32] if n not in [3]]
        if interval_candidates and random.random() < 0.7:
            chosen = random.sample([n for n in interval_candidates if n in self.hot_front[:8]],
                                    min(1, len([n for n in interval_candidates if n in self.hot_front[:8]])))
            if chosen:
                selected.extend(chosen)

        # Strategy 2: Zone0 heat continuation (01-07 zone active for 2 consecutive periods)
        zone0_hot = [n for n in zones[0] if n in self.hot_front[:10] and n not in selected]
        if zone0_hot and random.random() < 0.6:
            selected.append(random.choice(zone0_hot[:3]))

        # Strategy 3: Cold-to-hot capture (numbers missing 5-8 periods suddenly appear)
        cold_to_hot = [n for n in self.front_range if 5 <= self.front_missing.get(n, 10) <= 8 and n not in selected]
        if cold_to_hot and random.random() < 0.5:
            selected.append(random.choice(cold_to_hot[:3]))
        
        # 策略4: 补齐5个（区域分散 + 热号优先）
        while len(selected) < 5:
            zone_idx = len(selected)
            zone_nums = zones[zone_idx]
            hot_in_zone = [n for n in zone_nums if n in self.hot_front[:8] and n not in selected]
            if hot_in_zone and random.random() < 0.55:
                selected.append(random.choice(hot_in_zone))
            else:
                cold_in_zone = [n for n in zone_nums if n not in selected]
                if cold_in_zone:
                    selected.append(random.choice(cold_in_zone))
        
        return sorted(selected[:5])
    
    def _check_constraints(self, front):
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
            zones_covered.add((n-1) // 7)
        if len(zones_covered) < 4:
            return False
        consecutive = sum(1 for i in range(4) if front[i+1] - front[i] == 1)
        if consecutive > 1:
            return False
        return True
    
    def _generate_back_v35(self):
        """26035期后区生成策略"""
        # 按遗漏排序
        missing_sorted = sorted(self.back_missing.items(), key=lambda x: x[1], reverse=True)
        big_missing = [n for n, m in missing_sorted if m >= 6]
        
        # 策略: 大遗漏号必须选1个
        if big_missing and random.random() < 0.85:
            back = [random.choice(big_missing[:3])]
        else:
            back = [random.choice(list(self.back_range))]
        
        # 第2个: 混合策略
        remaining = [n for n in self.back_range if n not in back]
        if remaining:
            # 50%概率选热号，50%概率选遗漏号
            if random.random() < 0.5:
                hot = [n for n in remaining if n in self.back_freq.most_common(4)]
                if hot:
                    back.append(random.choice(hot))
                else:
                    back.append(random.choice(remaining[:4]))
            else:
                remaining_sorted = sorted(remaining, key=lambda x: self.back_missing.get(x, 0), reverse=True)
                back.append(random.choice(remaining_sorted[:4]))
        
        return sorted(back[:2])
    
    def _generate_single(self, max_attempts=300):
        for _ in range(max_attempts):
            front = self._generate_front_v35()
            if not self._check_constraints(front):
                continue
            back = self._generate_back_v35()
            
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

def save_prediction(issue, predictions, last_issue_review=None):
    import json
    filename = f"lottery_history/prediction_{issue}.json"
    data = {
        'issue': issue,
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'last_issue_review': last_issue_review,
        'predictions': predictions,
        'model_version': 'V2.0',
        'strategy_note': '26035期: 隔期重号捕捉 + Zone0热延续 + 后区大遗漏追踪'
    }
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[OK] Saved: {filename}")

# 运行预测
predictor = LottoPredictorV20(RECENT_DRAWS)

print("=" * 70)
print("[B166ER] Super Lotto Prediction V2.0 - 26035")
print("=" * 70)
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Target: 26035 (2026-04-04 Saturday)")
print()

# 显示分析
print("【26030-26033期规律分析】")
print(f"前区热号(近10期): {' '.join([f'{n:02d}' for n in predictor.hot_front[:8]])}")
print(f"近3期重复号: {' '.join([f'{n:02d}' for n in predictor.recent_3_front])}")
print(f"隔期重号候选(26032期): 04 19 26 32")
print()

print("【后区遗漏追踪】")
for num in range(1, 13):
    m = predictor.back_missing.get(num, 15)
    bar = '#' * min(m, 10) + '-' * (10 - min(m, 10))
    print(f"  {num:02d}: {bar} ({m}期未出)")
print()

print("【26035期预测 - 5注】")
print("-" * 70)

predictions = predictor.predict(count=5)
save_prediction('26035', predictions)

for pred in predictions:
    front_str = ' '.join([f"{n:02d}" for n in pred['front']])
    back_str = ' '.join([f"{n:02d}" for n in pred['back']])
    print(f"注{pred['no']}: 前区[{front_str}] 后区[{back_str}]")
    print(f"      和值:{pred['sum']:3d} 跨度:{pred['span']:2d} 奇偶:{pred['odd_even'][0]}:{pred['odd_even'][1]} 大小:{pred['big_small'][0]}:{pred['big_small'][1]}")
    print()

print("=" * 70)
print("Note: 26034期(4月2日)尚未开奖，本预测基于26030-26033期规律")
print("Disclaimer: For entertainment only. Lottery is completely random.")
print("Please play responsibly.")
print("=" * 70)