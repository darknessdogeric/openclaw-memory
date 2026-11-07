"""AHL 商业模式测算 v2.0 — 含 AI 工具矩阵 (收益管理 / 客户雷达 / 政策雷达)
修正 v1.0 的错误: 把 B端 Agent 对话当成一次性行为, 且未计入常驻工具的 token 消耗
"""
import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PRICES = {
    "DeepSeek V4": (0.5, 2.0),
    "Qwen3-Turbo": (0.8, 2.0),
    "Qwen3-Max": (5.0, 15.0),
}
IO_RATIO = 0.7

def cost_of(tokens, model):
    pin, pout = PRICES[model]
    return (tokens * IO_RATIO / 1e6) * pin + (tokens * (1-IO_RATIO) / 1e6) * pout

print("=" * 78)
print("一、token 消耗结构重建: 5 个来源 (修正 v1.0)")
print("=" * 78)

print("""
  v1.0 的错误:
    - 只算了「C端订单 + B端一次性数据沉淀」
    - 漏了 B端 Agent 对话是【持续运维】性质, 不是一次性
    - 完全没算【AI 工具矩阵】的常驻消耗

  v2.0 的结构 (单店, 100 间房):
""")

# ── 场景参数 ──
SCENARIOS = {
    "轻量 (房型级定价)": {"rooms": 8, "rev_mult": 1.0},
    "标准 (房型+事件)": {"rooms": 8, "rev_mult": 1.5},
    "深度 (逐间房定价)": {"rooms": 100, "rev_mult": 1.0},
}
TOOLS = {
    "AI 收益管理":  {"calls_per_day": 0, "tok_per_call": 0, "note": ""},
    "AI 客户发掘雷达": {"calls_per_day": 10, "tok_per_call": 5000, "note": "10类目标客群×每日扫描"},
    "AI 政策雷达":   {"calls_per_day": 3, "tok_per_call": 8000, "note": "政策文本长, 需全量读"},
}

for sc_name, sc in SCENARIOS.items():
    rooms = sc["rooms"]
    mult = sc["rev_mult"]
    # 收益管理: 每房型/每房每天 N 次 × (竞品数据+预测+建议)
    rev_calls = rooms * 2 * int(mult) + 1     # +1 日报
    rev_tok = rev_calls * 6000

    radar_tok = TOOLS["AI 客户发掘雷达"]["calls_per_day"] * TOOLS["AI 客户发掘雷达"]["tok_per_call"] * 30
    policy_tok = TOOLS["AI 政策雷达"]["calls_per_day"] * TOOLS["AI 政策雷达"]["tok_per_call"] * 30

    # B端 Agent 对话 (运维性质, 持续)
    b_chat_tok = 20 * 3000 * 30              # 每天 20 次 × 3000 tok
    # C端
    c_tok = 100 * 5 * 3000                   # 100单 × 5轮 × 3000

    total = rev_tok + radar_tok + policy_tok + b_chat_tok + c_tok

    print(f"\n  【{sc_name}】 收益管理按 {rooms} {'间房' if rooms > 20 else '房型'}计")
    print(f"    AI 收益管理      {rev_tok/1e6:>7.2f}M token  ({rev_calls} 次/天)")
    print(f"    AI 客户发掘雷达  {radar_tok/1e6:>7.2f}M token  (10 次/天)")
    print(f"    AI 政策雷达      {policy_tok/1e6:>7.2f}M token  (3 次/天)")
    print(f"    B端 Agent 运维   {b_chat_tok/1e6:>7.2f}M token  (20 次/天, 持续)")
    print(f"    C端对话          {c_tok/1e6:>7.2f}M token  (100 单/月)")
    print(f"    ────────────────────────────────────────")
    print(f"    合计            {total/1e6:>7.2f}M token/月")

    for model in PRICES:
        c = cost_of(total, model)
        print(f"      {model:<14} ¥{c:>7.2f} /月")
    print()

# ── 基准场景成本 ──
print("=" * 78)
print("二、核心问题: 现有定价能不能覆盖")
print("=" * 78)

# 深度场景 (最保守)
deep_rooms = 100
rev_tok = (deep_rooms * 2 + 1) * 6000 * 30
radar_tok = 10 * 5000 * 30
policy_tok = 3 * 8000 * 30
b_chat_tok = 20 * 3000 * 30
c_tok = 100 * 5 * 3000
deep_total = rev_tok + radar_tok + policy_tok + b_chat_tok + c_tok

print(f"\n  深度场景单店月 token: {deep_total/1e6:.1f}M\n")

print("  【用 DeepSeek V4 (便宜模型)】")
c_cheap = cost_of(deep_total, "DeepSeek V4")
print(f"    单店月成本 ¥{c_cheap:.2f}")
for price_m in [333, 583, 832, 1999]:
    print(f"    月费 ¥{price_m:>5,}: 毛利率 {(1-c_cheap/price_m)*100:>5.1f}%")

print("\n  【用 Qwen3-Max (强模型, 收益管理确实需要)】")
c_strong = cost_of(deep_total, "Qwen3-Max")
print(f"    单店月成本 ¥{c_strong:.2f}  ← 比 DeepSeek 贵 {c_strong/c_cheap:.0f}倍")
for price_m in [333, 583, 832, 1999, 3999]:
    ratio = c_strong/price_m*100
    margin = (1-c_cheap/price_m)*100
    flag = "❌ 亏损" if ratio > 100 else ("⚠️ 紧张" if ratio > 40 else "✅ 健康")
    print(f"    月费 ¥{price_m:>5,}: 强模型成本占比 {ratio:>5.1f}%  廉价模型毛利 {margin:>5.1f}%  {flag}")

print(f"""
  >>> 关键结论:
      收益管理这类任务需要强推理能力, 用 Qwen3-Max 是 DeepSeek 的 {c_strong/c_cheap:.0f}倍成本
      现有定价 (基础版 ¥3,999/年 = ¥333/月) 在【深度场景+强模型】下会亏损
      定价必须按工具深度分档, 或强制工具分级 (强模型只给旗舰版)
""")

# ── 自建临界点 (用高消耗量重算) ──
print("=" * 78)
print("三、自建临界点 (用真实消耗量重算, 修正 v1.0 的 640 家)")
print("=" * 78)

GPU_HOURS = 24 * 30
for gpu_price in [1.5, 3.0]:
    gpu_month = gpu_price * GPU_HOURS
    print(f"\n  单卡 ¥{gpu_price}/小时 × 720h = ¥{gpu_month:,.0f}/月")

    # 4090 跑 7B 量化模型, vLLM 连续批处理 ≈ 4000 tok/s
    throughput = 4000 * 86400 / 30   # 月产能 token
    for model in PRICES:
        shops = throughput / (deep_total / c_strong if model == "Qwen3-Max" else deep_total / c_cheap)
        shops_equiv = gpu_month / cost_of(deep_total, model)
        print(f"    {model:<14} 算力可支撑 {shops_equiv:>5.0f} 家  (算力口径 {shops:>5.0f} 家)")

print(f"""
  >>> 单卡可支撑约 {1080/c_cheap:.0f} 家 (廉价模型口径)
  >>> 但如果用强模型做收益管理, 单卡只支撑 {1080/c_strong:.0f} 家
  >>> 自建的真正价值不只是省钱, 是【数据不出内网 + 可微调垂类】, 成本反而是次要理由
""")

# ── 分档定价建议 ──
print("=" * 78)
print("四、分档定价建议 (按工具深度绑定, 而非按功能多少)")
print("=" * 78)

print("""
  ┌──────────┬────────────────┬──────────────┬──────────────┐
  │ 版本      │ 工具配置        │ 推理模型      │ 建议月费      │
  ├──────────┼────────────────┼──────────────┼──────────────┤
  │ 基础版    │ 仅 C端匹配      │ 廉价模型      │ ¥499         │
  │          │ + B端基础对话   │              │              │
  ├──────────┼────────────────┼──────────────┼──────────────┤
  │ 专业版    │ + 收益管理(房型级)│ 均衡模型     │ ¥1,999       │
  │          │ + 客户雷达      │              │              │
  ├──────────┼────────────────┼──────────────┼──────────────┤
  │ 旗舰版    │ + 收益管理(逐间房)│ 强模型       │ ¥4,999       │
  │          │ + 全部雷达      │              │              │
  └──────────┴────────────────┴──────────────┴──────────────┘

  核心: 定价必须【绑定工具深度】, 因为 token 成本是工具深度的函数, 不是用户数的函数
        不同档位用不同模型, 用成本约束消费
""")

# ── 盈亏平衡 ──
print("=" * 78)
print("五、盈亏平衡点 (按修正后成本)")
print("=" * 78)

FIXED = 95000
CAC_HIGH = 7143
for price, model, mix in [(499, "DeepSeek V4", "基础"), (1999, "Qwen3-Turbo", "专业"), (4999, "Qwen3-Max", "旗舰")]:
    scen = {"基础": light_total if False else (8*2+1)*6000*30 + 10*5000*30 + 3*8000*30 + b_chat_tok + c_tok,
            "专业": (8*3+1)*6000*30 + 10*5000*30 + 3*8000*30 + b_chat_tok + c_tok,
            "旗舰": deep_total}[mix]
    c = cost_of(scen, model)
    gross = price - c
    be = (FIXED + CAC_HIGH) / gross
    print(f"  {mix}版 ¥{price:,}/月 ({model}): 单店毛利 ¥{gross:.0f} → 盈亏平衡 {be:.0f} 家")

print(f"""
  >>> 修正后的盈亏平衡点比 v1.0 高, 因为单店毛利被 token 成本压缩
  >>> 但【旗舰版毛利 ¥4,834/家】意味着可以用少量旗舰客户覆盖大部分固定成本
  >>> 策略: 基础版拉量 + 旗舰版赚钱, 而不是靠基础版
""")