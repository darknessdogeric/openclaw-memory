"""
大乐透 V5.2 预测生成器
核心改变: 放弃"热号托底"策略，改为区域均衡+遗漏追踪+热号均衡
"""
import sys, json, random
sys.stdout.reconfigure(encoding='utf-8')

# ============ 基础数据 ============
FRONT_POOL = list(range(1, 36))
BACK_POOL = list(range(1, 13))

# 各号码30期频次（26008-26037）
FREQ = {
    3: 8, 9: 7, 12: 7, 13: 7, 26: 7,
    2: 6, 4: 6, 10: 6, 11: 6, 21: 6, 23: 6,
    5: 5, 8: 5, 16: 5, 18: 5, 6: 5,
    14: 4, 17: 4, 19: 4, 22: 4, 25: 4, 29: 4,
    1: 3, 15: 3, 30: 3, 33: 3, 34: 3,
    7: 2, 28: 2, 29: 2, 35: 2,
    20: 1, 24: 1, 27: 1,
}

# 各号码遗漏期数（从上期26037往前推）
MISS = {
    20: 30, 27: 28, 7: 27, 28: 17, 15: 16,
    32: 16, 24: 14, 1: 13, 11: 12, 8: 10,
    19: 10, 24: 10, 30: 12, 31: 11,
    9: 3, 12: 3, 13: 2, 26: 4, 33: 2,
    2: 4, 4: 5, 10: 9, 21: 6, 23: 6,
    5: 3, 6: 7, 16: 8, 18: 4,
    14: 4, 17: 7, 22: 6, 25: 6, 29: 4,
}

# 区域划分
ZONES = {
    1: list(range(1, 6)),    # 01-05
    2: list(range(6, 11)),  # 06-10
    3: list(range(11, 16)),  # 11-15
    4: list(range(16, 21)), # 16-20
    5: list(range(21, 26)), # 21-25
    6: list(range(26, 31)), # 26-30
    7: list(range(31, 36)), # 31-35
}
ZONE_NAMES = {1:"01-05", 2:"06-10", 3:"11-15", 4:"16-20", 5:"21-25", 6:"26-30", 7:"31-35"}

def get_zone(n): return (n-1)//5 + 1
def is_hot(n): return FREQ.get(n, 0) >= 6
def is_cold(n): return MISS.get(n, 0) >= 10
def sum_value(bet): return sum(bet)

def check_zones(bet):
    """检查号码覆盖的区域数"""
    zones = set(get_zone(n) for n in bet)
    return len(zones)

def check_hot_count(bet):
    """检查热号数量"""
    return sum(1 for n in bet if is_hot(n))

def check_cold_count(bet):
    """检查冷号数量(遗漏>=10期)"""
    return sum(1 for n in bet if is_cold(n))

def score_bet(bet):
    """
    评分函数（V5.2版）
    - 区域均衡：覆盖>=4个区域
    - 热号限制：热号不超过1个
    - 冷号加权：每多1个冷号+5分
    - 极冷加权：每有1个遗漏20+期号码+10分
    - 和值约束：70-110内+5分
    """
    score = 50
    zone_count = check_zones(bet)
    hot_count = check_hot_count(bet)
    cold_nums = [n for n in bet if is_cold(n)]
    very_cold = [n for n in bet if MISS.get(n, 0) >= 20]

    if zone_count >= 5: score += 15
    elif zone_count == 4: score += 10
    elif zone_count == 3: score += 0

    if hot_count == 0: score += 8
    elif hot_count == 1: score += 5
    elif hot_count == 2: score += 0
    else: score -= 10

    score += len(cold_nums) * 5
    score += len(very_cold) * 10

    s = sum_value(bet)
    if 70 <= s <= 110: score += 5
    elif 60 <= s <= 120: score += 0
    else: score -= 5

    return score

def generate_candidates():
    """
    生成候选注
    V5.2核心策略:
    1. 极冷号(遗漏20+期): 20, 27 必须纳入候选
    2. 区域均衡: 每注覆盖4-5个区域
    3. 热号限制: 最多1个热号
    4. 冷号配置: 至少1个冷号
    """
    candidates = []

    # 极冷号池
    very_cold = [n for n, m in MISS.items() if m >= 20]  # 20, 27
    # 大冷号池
    cold_pool = [n for n, m in MISS.items() if m >= 10 and n not in very_cold]  # 7,15,28,32,8,19,24,30,31
    # 中性号池
    neutral = [n for n in FRONT_POOL if n not in very_cold and not is_cold(n)]
    # 热号池
    hot_pool = [n for n in FRONT_POOL if is_hot(n)]

    # 按区域分组候选
    zone_cold = {z: [n for n in cold_pool if get_zone(n) == z] for z in range(1, 8)}
    zone_hot = {z: [n for n in hot_pool if get_zone(n) == z] for z in range(1, 8)}
    zone_neutral = {z: [n for n in neutral if get_zone(n) == z] for z in range(1, 8)}

    # 生成策略矩阵
    strategies = [
        # [极冷, 大冷区, 中性区1, 中性区2, 热号区]
        [4, 2, 1, 1, 0],  # 策略A: 4冷+1中性
        [2, 1, 1, 1, 0],   # 策略B: 2极冷+2冷+1中性
        [2, 1, 1, 0, 1],   # 策略C: 2极冷+1冷+1中性+1热
        [1, 2, 1, 1, 0],  # 策略D: 1极冷+3冷+1中性
        [1, 1, 1, 1, 1],  # 策略E: 1极冷+2冷+2中性(含1热)
        [2, 2, 0, 1, 0],  # 策略F: 2极冷+2冷+1中性
        [1, 2, 1, 0, 1],  # 策略G: 1极冷+2冷+1中性+1热
    ]

    for strat_idx, (n_very, n_cold, n_neu1, n_neu2, n_hot) in enumerate(strategies):
        attempts = 0
        strat_candidates = []
        while len(strat_candidates) < 2 and attempts < 100:
            attempts += 1
            bet = []
            zones_used = []

            # 极冷号分配
            if n_very > 0:
                avail_zones = [z for z in range(1, 8) if z not in zones_used]
                random.shuffle(avail_zones)
                for z in avail_zones[:min(n_very, len(avail_zones))]:
                    zone_pool = [n for n in very_cold if get_zone(n) == z]
                    if zone_pool:
                        bet.append(random.choice(zone_pool))
                        zones_used.append(z)

            # 大冷号分配
            if n_cold > 0:
                avail_zones = [z for z in range(1, 8) if z not in zones_used]
                random.shuffle(avail_zones)
                for z in avail_zones[:min(n_cold, len(avail_zones))]:
                    zone_pool = zone_cold.get(z, [])
                    if zone_pool:
                        bet.append(random.choice(zone_pool))
                        zones_used.append(z)

            # 中性号1分配
            if n_neu1 > 0:
                avail_zones = [z for z in range(1, 8) if z not in zones_used]
                random.shuffle(avail_zones)
                for z in avail_zones[:min(n_neu1, len(avail_zones))]:
                    zone_pool = zone_neutral.get(z, [])
                    if zone_pool:
                        bet.append(random.choice(zone_pool))
                        zones_used.append(z)

            # 中性号2分配
            if n_neu2 > 0:
                avail_zones = [z for z in range(1, 8) if z not in zones_used]
                random.shuffle(avail_zones)
                for z in avail_zones[:min(n_neu2, len(avail_zones))]:
                    zone_pool = zone_neutral.get(z, [])
                    if zone_pool:
                        bet.append(random.choice(zone_pool))
                        zones_used.append(z)

            # 热号分配
            if n_hot > 0:
                avail_zones = [z for z in range(1, 8) if z not in zones_used and zone_hot.get(z, [])]
                random.shuffle(avail_zones)
                for z in avail_zones[:min(n_hot, len(avail_zones))]:
                    zone_pool = zone_hot.get(z, [])
                    if zone_pool:
                        bet.append(random.choice(zone_pool))
                        zones_used.append(z)

            if len(bet) == 5 and len(set(bet)) == 5:
                strat_candidates.append({
                    'front': sorted(bet),
                    'strategy': chr(65 + strat_idx),
                    'score': score_bet(bet)
                })

        candidates.extend(strat_candidates)

    return candidates

def generate_back():
    """生成后区"""
    # 基于遗漏的后区
    back_miss = {1: 4, 2: 3, 3: 11, 4: 15, 5: 5, 6: 5, 7: 5, 8: 2, 9: 12, 10: 3, 11: 2, 12: 2}
    # 最冷: 4(15期), 9(12期), 3(11期)
    # 上期: 6, 8
    # 策略: 1个极冷 + 1个温号/上期邻号
    back_options = [
        [4, 9],   # 极冷组合
        [4, 3],   # 极冷+大冷
        [9, 3],   # 大冷组合
        [4, 6],   # 极冷+上期号
        [9, 8],   # 大冷+上期号
        [6, 8],   # 上期重现
        [4, 11],  # 极冷+温号
    ]
    return random.choice(back_options)

def main():
    print("=" * 70)
    print("大乐透 V5.2 预测生成")
    print("=" * 70)

    candidates = generate_candidates()
    candidates.sort(key=lambda x: -x['score'])

    print(f"\n策略原则:")
    print("  1. 区域均衡: 每注覆盖4-5个区域")
    print("  2. 热号限制: 最多1个热号(频次>=6)")
    print("  3. 冷号配置: 至少1个大冷号(遗漏>=10期)")
    print("  4. 极冷号: 20(30期), 27(28期)优先纳入")
    print("  5. 和值约束: 70-110范围")

    print(f"\n候选注数: {len(candidates)}")
    print("\n候选详情:")
    for c in candidates[:10]:
        zones = sorted(set(get_zone(n) for n in c['front']))
        zone_str = '/'.join(ZONE_NAMES[z] for z in zones)
        hot_n = [n for n in c['front'] if is_hot(n)]
        cold_n = [n for n in c['front'] if is_cold(n)]
        very_cold_n = [n for n in c['front'] if MISS.get(n, 0) >= 20]
        print(f"  [{c['strategy']}] {c['front']} | 和={sum(c['front'])} | 区={zone_str} | 热={hot_n} | 冷={cold_n} | 极冷={very_cold_n} | 分={c['score']}")

    # 选择Top5 + 区域多样性
    candidates.sort(key=lambda x: -x['score'])
    selected = []
    used_zone_combos = set()

    for c in candidates:
        if len(selected) >= 5:
            break
        zones_key = tuple(sorted(set(get_zone(n) for n in c['front'])))
        # 保证区域多样性：前3注必须区域组合不同
        if len(selected) < 3:
            if zones_key in used_zone_combos:
                continue
        selected.append(c)
        used_zone_combos.add(zones_key)

    print("\n" + "=" * 70)
    print("26038期 V5.2 最终预测")
    print("=" * 70)

    results = []
    for i, c in enumerate(selected):
        back = generate_back()
        zones = sorted(set(get_zone(n) for n in c['front']))
        print(f"\n注{i+1}: {c['front']} + {back} | 和={sum(c['front'])} | 区={zones} | 策略={c['strategy']}")
        results.append({
            "no": i+1,
            "front": c['front'],
            "back": back,
            "sum": sum(c['front']),
            "strategy": c['strategy'],
            "zones": [ZONE_NAMES[z] for z in zones],
            "score": c['score']
        })

    # 保存
    output = {
        "issue": "26038",
        "model_version": "V5.2",
        "date": "2026-04-09",
        "key_change": "放弃热号托底，改用区域均衡+遗漏追踪+热号均衡",
        "predictions": results,
        "strategy_summary": {
            "very_cold_numbers": [20, 27],
            "hot_numbers_limit": "最多1个/注",
            "zone_coverage": "4-5区域/注",
            "sum_range": "70-110"
        }
    }

    with open('C:/Users/ericz/.openclaw/workspace/lottery_history/prediction_26038_v52.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n已保存: prediction_26038_v52.json")

if __name__ == '__main__':
    random.seed(42)  # 可重复
    main()
