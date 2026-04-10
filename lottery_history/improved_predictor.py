#!/usr/bin/env python3
"""V5.1 改进预测器 - 基于回测发现"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import lottery_v5
from lottery_v5 import HISTORY_DATA, MissTracker, InformationTheory, MarkovChain, GameTheoryFilter
import random

history = HISTORY_DATA
NEXT_ISSUE = "26037"

print("=" * 50)
print("V5.1 改进预测器")
print("=" * 50)

# ===== 指标计算 =====
sums = [sum(d['front']) for d in history]
mean_sum = sum(sums) / len(sums)  # ~84
std_sum = (sum((s - mean_sum)**2 for s in sums) / len(sums)) ** 0.5

# 遗漏追踪
tracker = MissTracker(history)
for _ in range(5):
    tracker.update()
fm = tracker.get_front_miss()
bm = tracker.get_back_miss()

# 热号
hot = tracker.get_hot(12)
hot_nums = [x[0] for x in hot]
hot_dict = dict(hot)

# 大遗漏号
front_miss_sorted = sorted(fm.items(), key=lambda x: -x[1])
back_miss_sorted = sorted(bm.items(), key=lambda x: -x[1])

# ===== 策略：博弈论 + 均值回归 + 大遗漏 =====
print(f"\n[基础指标]")
print(f"和值均值: {mean_sum:.1f} (范围: {mean_sum-std_sum:.0f}-{mean_sum+std_sum:.0f})")

print(f"\n[前区热号]")
for n, c in hot[:8]:
    print(f"  {n}: {c}次")

print(f"\n[后区大遗漏]")
for n, m in back_miss_sorted[:6]:
    status = "***" if m > 14 else ("**" if m > 10 else "*")
    print(f"  {n}: {m}期 {status}")

# ===== 生成5注 =====
predictions = []

# 策略1: 热号 + 大遗漏 + 均值回归
for i in range(5):
    # 选2个热号
    h = random.sample(hot_nums[:5], 2)
    # 选1个大遗漏号
    cold_candidates = [n for n, _ in front_miss_sorted[:8] if n not in h]
    c = [random.choice(cold_candidates)]
    # 补2个均值区间号
    others = [n for n in range(1, 36) if n not in h and n not in c
              and 15 <= n <= 30]  # 均值区间
    o = random.sample(others, 2)
    front = sorted(h + c + o)

    # 后区: 大遗漏 + 随机
    b1 = back_miss_sorted[0][0]  # 最大遗漏
    b2_candidates = [n for n, _ in back_miss_sorted[:4] if n != b1]
    b2 = random.choice(b2_candidates)
    back = sorted([b1, b2])

    # 博弈论评分
    gt_score = GameTheoryFilter.filter_score(front, fm)

    predictions.append({
        'no': i+1,
        'front': front,
        'back': back,
        'sum': sum(front),
        'gt_score': gt_score,
        'strategy': '热号+大遗漏+均值回归'
    })

# 按博弈分排序
predictions.sort(key=lambda x: x['gt_score'])

print(f"\n[26037期 V5.1预测]")
for p in predictions:
    # 博弈论标签
    birth_penalty = sum(1 for n in p['front'] if n <= 12)
    print(f"注{p['no']}: {p['front']} | {p['back']} | "
          f"和值{p['sum']} | 博弈分{p['gt_score']} | 生日区:{birth_penalty}")

print("\n" + "=" * 50)
print(f"预测完成: {NEXT_ISSUE}")
