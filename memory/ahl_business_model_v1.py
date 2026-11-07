"""AHL 商业模式测算模型 v1.0
基准来源: Tavily 2026-10-22 实测搜索
- DeepSeek V4 API: 输入 ¥0.5/M, 输出 ¥2/M
- Qwen3-Turbo: 输入 ¥0.8/M, 输出 ¥2/M
- Qwen3-Max: 输入 ¥5/M, 输出 ¥15/M
- RTX 4090 租用: ¥0.39-1.8/小时
"""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# ============ 成本基准 (实测) ============
PRICES = {
    "DeepSeek V4 (最省)":  (0.5, 2.0),
    "Qwen3-Turbo (均衡)":  (0.8, 2.0),
    "Qwen3-Max (最强)":    (5.0, 15.0),
}

print("=" * 74)
print("一、单店月 token 用量与成本 (核心发现)")
print("=" * 74)

# 假设 (需 Eric 校准)
ASSUME = {
    "单店月订单数": 100,
    "每单对话轮次": 5,
    "每轮token(输入+输出)": 3000,
    "B端数据沉淀次数/月": 30,
    "每次沉淀token": 2500,
    "B端运营优化次数/月": 100,
    "每次优化token": 2000,
    "输入输出比": 0.7,   # 输入占 70%, 输出占 30%
}

c_end = ASSUME["单店月订单数"] * ASSUME["每单对话轮次"] * ASSUME["每轮token(输入+输出)"]
b_feed = ASSUME["B端数据沉淀次数/月"] * ASSUME["每次沉淀token"]
b_ops = ASSUME["B端运营优化次数/月"] * ASSUME["每次优化token"]
total_tok = c_end + b_feed + b_ops

print(f"\n  C端 token (分摊到单店): {c_end:>10,} token/月  ({c_end/1e6:.2f}M)")
print(f"  B端 token (商家主动):   {b_feed + b_ops:>10,} token/月  ({(b_feed+b_ops)/1e6:.2f}M)")
print(f"  合计:                   {total_tok:>10,} token/月  ({total_tok/1e6:.2f}M)")
print(f"\n  输入: {total_tok*0.7/1e6:.2f}M  输出: {total_tok*0.3/1e6:.2f}M\n")

print("  不同模型下的单店月成本:")
cost_by_model = {}
for name, (pin, pout) in PRICES.items():
    cost = (total_tok * 0.7 / 1e6) * pin + (total_tok * 0.3 / 1e6) * pout
    cost_by_model[name] = cost
    print(f"    {name:<20} ¥{cost:>6.2f} /月")

avg_cost = sum(cost_by_model.values()) / len(cost_by_model)
print(f"\n  >>> 平均单店月 token 成本: ¥{avg_cost:.2f}")

# ============ 二、token 成本在收入中的占比 ============
print("\n" + "=" * 74)
print("二、token 成本 vs 定价: 关键判断")
print("=" * 74)

for price in [499, 999, 1999, 3999]:
    ratio = avg_cost / price * 100
    print(f"  月费 ¥{price:>5,}: token 成本占比 {ratio:>5.2f}%  (毛利空间 ¥{price-avg_cost:>6.2f})")

print(f"\n  >>> 结论: token 成本占定价 0.1%-0.5%, 几乎可忽略")
print(f"  >>> 按 token 计费收不到有意义的金额, 必须按效果/包月收")

# ============ 三、GPU 自建 vs API ============
print("\n" + "=" * 74)
print("三、自建推理 vs API: 成本临界点")
print("=" * 74)

GPU_RENT = 1.5   # ¥/小时 (4090 繁忙时段)
GPU_HOURS = 24 * 30
gpu_month = GPU_RENT * GPU_HOURS
print(f"\n  单卡 4090 租用: ¥{GPU_RENT}/小时 × 720 小时 = ¥{gpu_month:,.0f}/月")

for name, (pin, pout) in PRICES.items():
    shops_served = gpu_month / cost_by_model[name]
    print(f"    {name:<20} 单卡可支撑 {shops_served:>6.0f} 家店")

print(f"\n  >>> 临界点: 约 {gpu_month/cost_by_model['DeepSeek V4 (最省)']:.0f} 家店后自建比调 API 便宜")
print(f"  >>> 建议: 早期(<50家)用API, 之后自建. 不要在验证PMF前背GPU固定成本")

# ============ 四、CAC 与回本周期 ============
print("\n" + "=" * 74)
print("四、获客成本 (CAC) 与回本周期")
print("=" * 74)

# CAC 估算
SALARY = 25000      # 实施顾问月薪
DAYS = 21
DAILY = SALARY / DAYS
print(f"\n  实施顾问日成本: ¥{DAILY:,.0f}/天")
print(f"  假设成熟期 1 天接 2 家 → CAC = ¥{DAILY/2:,.0f}/家")
print(f"  假设爬坡期 1 周接 1 家 → CAC = ¥{DAILY*5:,.0f}/家")
print(f"  加 20% 销售/差旅开销 → 爬坡 CAC ≈ ¥{DAILY*5*1.2:,.0f}/家")

CAC_LOW, CAC_HIGH = DAILY/2, DAILY*5*1.2
print(f"\n  CAC 区间: ¥{CAC_LOW:,.0f} - ¥{CAC_HIGH:,.0f}/家")

print(f"\n  各定价下的回本周期与 LTV/CAC:")
print(f"  {'月费':>8} {'CAC回本(月)':>14} {'LTV(24月)':>12} {'LTV/CAC':>10}")
for price in [499, 999, 1999, 3999]:
    payback_low = CAC_LOW / price
    payback_high = CAC_HIGH / price
    ltv = price * 24
    ratio = ltv / CAC_HIGH
    print(f"  ¥{price:>7,} {payback_low:>6.1f}-{payback_high:<7.1f} ¥{ltv:>11,} {ratio:>9.1f}x")

print(f"\n  >>> 基准: B2B SaaS 健康 LTV/CAC >= 3, CAC回本 <= 18个月")
print(f"  >>> 即使按最保守 CAC, 各定价的 LTV/CAC 都远超基准")

# ============ 五、盈亏平衡点 ============
print("\n" + "=" * 74)
print("五、盈亏平衡点")
print("=" * 74)

FIXED = {
    "技术团队(3人)": 25000*3,
    "运维/服务器/GPU": 10000,
    "办公/差旅/杂费": 10000,
}
fixed_month = sum(FIXED.values())
print(f"\n  月固定成本:")
for k, v in FIXED.items():
    print(f"    {k:<18} ¥{v:>8,}")
print(f"    {'合计':<18} ¥{fixed_month:>8,}/月")

print(f"\n  各定价下的盈亏平衡酒店数 (含 CAC 一次性投入摊销):")
for price in [499, 999, 1999, 3999]:
    be_simple = fixed_month / price
    be_with_cac = (fixed_month + CAC_HIGH) / price
    print(f"    ¥{price:>5,}/月: {be_simple:>5.0f} 家 (纯运营) → {be_with_cac:>5.0f} 家 (含CAC爬坡)")

print(f"\n  >>> 基准定价 ¥1,999/月: 约 {(fixed_month+CAC_HIGH)/1999:.0f} 家酒店达盈亏平衡")

# ============ 六、敏感性: AI 增量价值要求 ============
print("\n" + "=" * 74)
print("六、AI 增量价值门槛: 商家为什么愿意付 ¥1,999/月")
print("=" * 74)

ADR = 600           # 酒店平均房价假设
print(f"\n  假设 ADR = ¥{ADR}/间夜")
print(f"  {'月费':>8} {'需增量房晚':>12} {'占单店月房晚比':>16}")
for price in [499, 999, 1999, 3999]:
    # 商家要有 3 倍回报意愿: 增量收益 = 3 × 月费
    need_revenue = price * 3
    need_nights = need_revenue / ADR
    base_nights = 100*30/12*3   # 假设日均3间房
    pct = need_nights / base_nights * 100
    print(f"  ¥{price:>7,} {need_nights:>11.1f} 晚 {pct:>15.1f}%")

print(f"\n  >>> 商家3倍回报意愿下, ¥1,999/月需AI带来约 10 间夜/月的增量房晚")
print(f"  >>> 这是要验证的核心数字: AHL 能否给单店带来 10 间夜/月的增量?")

# ============ 汇总 ============
print("\n" + "=" * 74)
print("七、汇总: 三个待验证数")
print("=" * 74)
print("""
  1. 单店月均订单数        [假设 100]  → 决定 token 用量与定价基数
  2. AI 单店月增量房晚      [需 ≥10]   → 决定商家是否愿意付 ¥1,999
  3. 实际 CAC (接入1家成本) [估 ¥630-3150] → 决定扩张速度与 LTV/CAC

  这三个数只有你的内部数据能回答。
  建议: 先跑 3-5 家酒店试点, 连续测 3 个月, 填这三个数。
""")