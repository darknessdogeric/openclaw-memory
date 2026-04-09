#!/usr/bin/env python3
"""V5.0回测分析"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import lottery_v5
from lottery_v5 import HISTORY_DATA, MissTracker, InformationTheory, MarkovChain

history = HISTORY_DATA

print("=" * 50)
print("V5.0 系统回测分析")
print("=" * 50)

# 基本统计
sums = [sum(d['front']) for d in history]
mean_sum = sum(sums) / len(sums)
std_sum = (sum((s - mean_sum)**2 for s in sums) / len(sums)) ** 0.5

print(f"\n[基本信息]")
print(f"总历史期数: {len(history)}")
print(f"和值均值: {mean_sum:.1f}")
print(f"和值标准差: {std_sum:.1f}")

# 赫斯特指数
H = InformationTheory.hurst_exponent(sums)
print(f"赫斯特指数: {H:.3f}")
if H < 0.5:
    print("  -> 反持续性，号码趋向均值回归")
elif H > 0.5:
    print("  -> 持续性，号码趋向延续趋势")
else:
    print("  -> 纯随机游走")

# 马尔可夫链
mc = MarkovChain(history[-10:])
last_front = history[-1]['front']
probs = mc.predict_next(last_front, 10)
print(f"\n[马尔可夫预测] 基于{history[-1]['issue']}期{last_front}")
for num, cnt in probs:
    print(f"  {num}: {cnt}次")

# 遗漏追踪
tracker = MissTracker(history)
for _ in range(5):
    tracker.update()
fm = tracker.get_front_miss()
bm = tracker.get_back_miss()

front_cold = sorted(fm.items(), key=lambda x: -x[1])[:5]
back_cold = sorted(bm.items(), key=lambda x: -x[1])[:5]

print(f"\n[前区大遗漏TOP5]")
for num, miss in front_cold:
    print(f"  {num}: {miss}期未出")

print(f"\n[后区大遗漏]")
for num, miss in back_cold:
    status = "***" if miss > 14 else ("**" if miss > 10 else "*")
    print(f"  {num}: {miss}期未出 {status}")

# 热号
hot = tracker.get_hot(8)
print(f"\n[前区热号TOP8]")
for num, cnt in hot:
    print(f"  {num}: {cnt}次")

# 简单回测：最近10期的"热号策略"表现
print(f"\n[简单回测] 热号策略近10期表现")
correct = 0
for i in range(len(history)-11, len(history)-1):
    train = history[:i+1]
    actual = history[i+1]

    # 热号策略：选近5期最热的3个号 + 随机2个
    hot_counter = {}
    for d in train[-5:]:
        for n in d['front']:
            hot_counter[n] = hot_counter.get(n, 0) + 1
    top3 = sorted(hot_counter.items(), key=lambda x: -x[1])[:3]
    hot_nums = [x[0] for x in top3]

    # 随机补2个
    import random
    candidates = [n for n in range(1, 36) if n not in hot_nums]
    rand2 = random.sample(candidates, 2)
    pred = sorted(hot_nums + rand2)

    hit = len(set(pred) & set(actual['front']))
    mark = "OK" if hit >= 2 else "MISS"
    if hit >= 2:
        correct += 1
    print(f"  {actual['issue']}: 预测{hot_nums}+{rand2} -> 命中{hit}个 {mark}")

print(f"\n热号策略命中率: {correct}/10 = {correct*10}%")

print("\n" + "=" * 50)
print("回测完成")
