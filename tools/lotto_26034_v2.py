# -*- coding: utf-8 -*-
"""B166ER 大乐透预测 V2.0 - 26034期预测（基于SOP重新生成）"""
import random
from datetime import datetime
from collections import Counter

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

        # 26033期刚出的号（防连续3期）
        self.last_issue_front = set(self.recent[-1].get('front', []))

        # 后区遗漏追踪
        self.back_missing = {}
        for num in self.back_range:
            last_appear = None
            for i, draw in enumerate(reversed(self.recent[-15:])):
                if num in draw.get('back', []):
                    last_appear = i
                    break
            self.back_missing[num] = last_appear if last_appear is not None else 15

        # 前区遗漏追踪
        self.front_missing = {}
        for num in self.front_range:
            last_appear = None
            for i, draw in enumerate(reversed(self.recent[-10:])):
                if num in draw.get('front', []):
                    last_appear = i
                    break
            self.front_missing[num] = last_appear if last_appear is not None else 10

    def _generate_front_v34(self):
        zones = {
            0: list(range(1, 8)),
            1: list(range(8, 15)),
            2: list(range(15, 22)),
            3: list(range(22, 29)),
            4: list(range(29, 36))
        }
        selected = []

        # 策略1: 03已连续2期，本期防反（只选0-1个）
        # 但03是超强热号，完全排除风险大，保留1个
        if 3 in self.hot_front[:6] and random.random() < 0.35:
            selected.append(3)

        # 策略2: 07连续2期，同理防反
        if 7 in self.hot_front[:6] and random.random() < 0.4:
            if 7 not in selected:
                selected.append(7)

        # 策略3: 隔期重号（26032期: 03,04,19,26,32）
        # 03和07已在上文处理，重点关注04,19,26,32
        interval_candidates = [n for n in [4, 19, 26, 32] if n not in selected]
        for cand in interval_candidates[:2]:
            if cand in self.hot_front[:8] and random.random() < 0.5:
                selected.append(cand)
                break

        # 策略4: 冷转热捕捉（遗漏5-8期突然出现）
        cold_to_hot = [n for n in self.front_range
                      if 5 <= self.front_missing.get(n, 10) <= 8
                      and n not in selected
                      and n not in self.last_issue_front]
        if cold_to_hot and random.random() < 0.55:
            selected.append(random.choice(cold_to_hot[:3]))

        # 策略5: 补齐到5个（区域分散）
        while len(selected) < 5:
            zone_idx = len(selected) % 5
            zone_nums = zones[zone_idx]
            hot_in_zone = [n for n in zone_nums if n in self.hot_front[:8] and n not in selected]
            if hot_in_zone and random.random() < 0.5:
                selected.append(random.choice(hot_in_zone))
            else:
                avail = [n for n in zone_nums if n not in selected]
                if avail:
                    selected.append(random.choice(avail))

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

    def _generate_back_v34(self):
        missing_sorted = sorted(self.back_missing.items(), key=lambda x: x[1], reverse=True)
        big_missing = [n for n, m in missing_sorted if m >= 6]

        # 大遗漏号必须选1个
        if big_missing and random.random() < 0.85:
            back = [random.choice(big_missing[:3])]
        else:
            back = [random.choice(list(self.back_range))]

        remaining = [n for n in self.back_range if n not in back]
        if remaining:
            if random.random() < 0.5:
                hot = [n for n in remaining if n in self.back_freq.most_common(4)]
                back.append(random.choice(hot if hot else remaining[:4]))
            else:
                rem_sorted = sorted(remaining, key=lambda x: self.back_missing.get(x, 0), reverse=True)
                back.append(random.choice(rem_sorted[:4]))

        return sorted(back[:2])

    def _generate_single(self, max_attempts=300):
        for _ in range(max_attempts):
            front = self._generate_front_v34()
            if not self._check_constraints(front):
                continue
            back = self._generate_back_v34()

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
            'front': front, 'back': back,
            'sum': sum(front), 'span': max(front) - min(front),
            'odd_even': (sum(1 for n in front if n % 2 == 1), sum(1 for n in front if n % 2 == 0)),
            'big_small': (sum(1 for n in front if n >= 18), sum(1 for n in front if n < 18))
        }

    def predict(self, count=5):
        return [{'no': i+1, **self._generate_single()} for i in range(count)]

def save_prediction(issue, predictions, last_review):
    import json
    filename = f"lottery_history/prediction_{issue}.json"
    data = {
        'issue': issue,
        'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'last_issue_review': last_review,
        'predictions': predictions,
        'model_version': 'V2.0',
        'strategy_note': '26034期: 03/07防反 + 隔期重号 + 冷转热 + 后区大遗漏'
    }
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[OK] Saved: {filename}")

predictor = LottoPredictorV20(RECENT_DRAWS)

print("=" * 70)
print("[B166ER] Super Lotto - 26034 Prediction (SOP V2.0)")
print("=" * 70)
print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Target: 26034 (2026-04-02 Thursday)")
print()

print("[Hot Numbers - Front]")
print(f"  {predictor.hot_front[:8]}")
print()
print("[Back Zone Missing Tracker]")
for num in range(1, 13):
    m = predictor.back_missing.get(num, 15)
    bar = '#' * min(m, 10) + '-' * (10 - min(m, 10))
    print(f"  {num:02d}: {bar} ({m})")
print()

predictions = predictor.predict(count=5)

print("[26034期 Prediction - 5 Sets]")
print("-" * 70)
for pred in predictions:
    print(f"Set{pred['no']}: Front{[f'{n:02d}' for n in pred['front']]} Back{[f'{n:02d}' for n in pred['back']]}")

save_prediction('26034', predictions, {
    'issue': '26033',
    'actual': {'front': [3, 5, 7, 9, 18], 'back': [2, 11]},
    'prizes': '九等奖 x3 (共15元)',
    'key_miss': '遗漏05,09,18 (冷转热)'
})

print()
print("=" * 70)