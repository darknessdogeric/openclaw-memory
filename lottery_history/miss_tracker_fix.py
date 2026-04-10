#!/usr/bin/env python3
"""正确计算遗漏值"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from lottery_v5 import HISTORY_DATA

# 正确计算每个号距上次出现的期数
def calc_miss(history):
    front_last = {i: -1 for i in range(1, 36)}
    back_last = {i: -1 for i in range(1, 13)}
    front_miss = {i: 0 for i in range(1, 36)}
    back_miss = {i: 0 for i in range(1, 13)}

    for idx, draw in enumerate(history):
        # 计算当前遗漏
        for n in range(1, 36):
            if front_last[n] >= 0:
                front_miss[n] = idx - front_last[n]
        for n in range(1, 13):
            if back_last[n] >= 0:
                back_miss[n] = idx - back_last[n]

        # 更新最后出现位置
        for n in draw['front']:
            front_last[n] = idx
        for n in draw['back']:
            back_last[n] = idx

    return front_miss, back_miss

fm, bm = calc_miss(HISTORY_DATA)

print("=" * 50)
print("正确遗漏值计算")
print("=" * 50)

print("\n[前区遗漏TOP10]")
for n, m in sorted(fm.items(), key=lambda x: -x[1])[:10]:
    bar = "*" * min(m, 20)
    print(f"  {n:2d}: {m:2d}期 {bar}")

print("\n[后区遗漏]")
for n, m in sorted(bm.items(), key=lambda x: -x[1]):
    bar = "*" * min(m, 20)
    status = "***" if m > 12 else ("**" if m > 8 else "*")
    print(f"  {n:2d}: {m:2d}期 {bar} {status}")

# 热号
from collections import Counter
hot = Counter()
for d in HISTORY_DATA:
    hot.update(d['front'])
print("\n[前区热号TOP10]")
for n, c in hot.most_common(10):
    print(f"  {n:2d}: {c}次")
