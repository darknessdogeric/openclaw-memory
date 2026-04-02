# 科技/AI项目定价策略与模型知识库

> 版本: V1.0
> 创建: 2026-04-01
> 用途: 为AI项目、SaaS产品、科技创业公司提供科学定价策略和模型
> 来源: Baremetrics + Stripe + 行业研究 + 实战经验

---

## 一、核心定价理论框架

### 1.1 定价的本质

```
定价 = 价值捕获的博弈

核心公式:
  价值/价格比 (Value/Price Ratio) = 客户感知价值 ÷ 实际价格

最优目标:
  - 10:1 价值/价格比 → 客户主动传播，口碑获客
  - 5:1 价值/价格比 → 客户满意，长期留存
  - 1:1 价值/价格比 → 客户无感，容易流失
```

**关键洞察** (来源: Baremetrics):
- 定价不仅是成本加利润，而是价值捕获
- SaaS产品成本与客户价值通常不相关
- 定价是业务中最重要但最被低估的增长杠杆

### 1.2 定价决策层次

```
第一层: 定价模式 (Pricing Model) - 怎么收费
第二层: 定价策略 (Pricing Strategy) - 怎么展示
第三层: 价格优化 (Price Optimization) - 如何调整
```

---

## 二、主流定价模式详解

### 2.1 七大SaaS定价模式

| 模式 | 描述 | 适用场景 | 优点 | 缺点 |
|------|------|---------|------|------|
| **1. 扁平制 (Flat-rate)** | 固定价格，无限使用 | 简单工具、 SMB | 简单易理解 | 无法捕获高端客户价值 |
| **2. 用户数制 (Per-user)** | 按账号数量收费 | 协作工具、CRM | 增长与收入同步 | 可能抑制协作 |
| **3. 用量制 (Usage-based)** | 按实际消耗收费 | API服务、通讯 | 降低客户风险 | 收入难预测 |
| **4. 分层制 (Tiered)** | 多个套餐选择 | 通用SaaS | 覆盖不同客户段 | 层级设计复杂 |
| **5. 席位制 (Per-seat)** | 每用户/每房间/每客房 | 酒店PMS、酒店科技 | 与价值直接挂钩 | 中大型客户可能觉得贵 |
| **6. 功能制 (Feature-based)** | 按功能模块收费 | 差异化产品 | 捕获功能溢价 | 可能过于复杂 |
| **7. 混合制 (Hybrid)** | 多种模式组合 | 复杂产品 | 灵活性高 | 定价复杂 |

### 2.2 酒店/客房相关特定模式

| 模式 | 描述 | 适用产品 | 代表厂商 |
|------|------|---------|---------|
| **每间夜** | ¥X / 入住间夜 | OTA渠道费 | 携程、美团 |
| **每房间月** | ¥X / 房间 / 月 | PMS、收益管理 | 石基、众荟 |
| **百分比GMV** | 营收的X% | 分成模式 | 部分代运营 |
| **订阅+交易** | 基础订阅 + 交易费 | 混合模式 | Stripe类 |
| **人头制** | ¥X / 入住人次 | 景区票务 | - |

### 2.3 AI项目特有定价模式

| 模式 | 描述 | 适用产品 | 案例 |
|------|------|---------|------|
| **Token计费** | 按AI调用量收费 | LLM API | OpenAI, Kimi |
| **Agent执行** | 按任务完成收费 | AI管家 | AHL概念 |
| **价值捕获** | 按客户增收比例收费 | 收益管理 | 部分RMS |
| **咨询+软件** | 咨询费 + 软件订阅 | 企业AI | 埃森哲 |

---

## 三、定价策略框架

### 3.1 价值定价策略 (Value-Based Pricing)

**核心思想**: 以客户感知价值定价，而非成本或竞争

**实施步骤**:
```
1. 量化客户价值 (Value Quantification)
   - 增收多少? (Revenue uplift)
   - 成本节约多少? (Cost savings)
   - 效率提升多少? (Efficiency gains)

2. 确定价值/价格比目标
   - 早期: 10:1 快速获客
   - 成长期: 5:1 平衡增长
   - 成熟期: 3:1 最大变现

3. 反推价格
   客户价值 ¥10,000 ÷ 目标比 5:1 = 价格 ¥2,000/月
```

**酒店场景示例**:
```
收益管理系统价值量化:
- 假设酒店100间客房，RevPAR ¥300
- AI收益管理提升5% → 增收 ¥150/天 = ¥4,500/月
- 价值/价格比目标 5:1 → 可定价 ¥900/月
- 如果提升10% → 可定价 ¥1,800/月
```

### 3.2 竞争定价策略 (Competitive Pricing)

**三种策略选择**:
| 策略 | 方法 | 适用阶段 | 风险 |
|------|------|---------|------|
| **溢价定价** | 高于竞品 | 差异化强、品牌强 | 需要强价值支撑 |
| **平价定价** | 与竞品相近 | 替代性强 | 价格战风险 |
| **渗透定价** | 低于竞品 | 进入市场、快速扩张 | 低价低质联想 |

### 3.3 客户细分定价策略

**常见客户分层**:
```
早期创业 (Startup):
  - 价格敏感
  - 需要教育
  - 愿意用时间换价格
  - ARPU目标: ¥500-2,000/月

成长企业 (SMB):
  - 有一定预算
  - 追求效率
  - ARPU目标: ¥2,000-10,000/月

中大型企业 (Mid-Market):
  - 预算充足
  - 要求SLA
  - ARPU目标: ¥10,000-50,000/月

大型企业 (Enterprise):
  - 定制化需求
  - 年框合同
  - ARPU目标: ¥50,000+/月
```

---

## 四、房间数/用户数定价模型

### 4.1 房间制 vs 用户制对比

**酒店科技产品常见选择**:

| 维度 | 房间制 | 用户制 |
|------|--------|--------|
| **定价锚点** | 客房数量 | 员工账号 |
| **客户感知** | 与经营规模挂钩 | 与团队大小挂钩 |
| **适用产品** | PMS、收益管理、CRS | 协作工具、培训系统 |
| **大客户挑战** | 房间多=价格高，可能分割采购 | 多部门多账号 |
| **收入可预测性** | 房间数稳定，较高 | 用户流动，较低 |

**推荐原则**:
```
1. 核心运营系统 → 房间制
   (PMS、收益管理、CRS、渠道管理)

2. 协作工具 → 用户制
   (OA、审批、通讯)

3. 混合模式 → 房间制基础 + 用户制附加
   (如: ¥X/房间 + ¥Y/人)
```

### 4.2 房间制定价计算模板

```python
# 酒店科技产品定价计算器

def calculate_room_pricing(
    hotel_rooms: int,
    revpar: float,           # 元/间夜
    improvement_rate: float, # AI带来的提升率 (如0.05)
    target_value_ratio: float, # 目标价值/价格比 (如5.0)
    days_per_month: int = 30
) -> dict:
    """
    基于价值的空间 (Value-Based Room Pricing)
    """

    # 1. 计算客户月度价值增量
    monthly_value = hotel_rooms * revpar * improvement_rate * days_per_month

    # 2. 反推月度可定价空间
    monthly_price = monthly_value / target_value_ratio

    # 3. 房间单价 (如果按房间计费)
    price_per_room = monthly_price / hotel_rooms

    return {
        "monthly_value_increase": round(monthly_value, 2),
        "suggested_monthly_price": round(monthly_price, 2),
        "price_per_room_month": round(price_per_room, 2),
        "annual_price": round(monthly_price * 12 * 0.9, 2)  # 年付9折
    }

# 示例计算
# 100间客房酒店，RevPAR ¥300，AI提升5%，目标5:1价值比
result = calculate_room_pricing(
    hotel_rooms=100,
    revpar=300,
    improvement_rate=0.05,
    target_value_ratio=5.0
)
# 月度价值增量: ¥45,000
# 建议月价格: ¥9,000
# 每房间月均: ¥90
```

### 4.3 分层定价设计

```python
def design_tiered_pricing(
    base_price_per_room: float,
    tiers: list
) -> dict:
    """
    分层定价设计

    tiers: [
        {"rooms": (1, 50), "multiplier": 1.2},    # 小酒店溢价
        {"rooms": (51, 200), "multiplier": 1.0}, # 标准
        {"rooms": (201, 500), "multiplier": 0.85}, # 大客户折扣
        {"rooms": (501, float('inf')), "multiplier": 0.7} # 集团折扣
    ]
    """
    pricing_tiers = []

    for tier in tiers:
        min_rooms, max_rooms = tier["rooms"]
        multiplier = tier["multiplier"]

        base_monthly = base_price_per_room * (min_rooms + max_rooms) / 2
        adjusted = base_monthly * multiplier

        pricing_tiers.append({
            "room_range": f"{min_rooms}-{max_rooms if max_rooms != float('inf') else '∞'}",
            "monthly_price": round(adjusted, 2),
            "annual_price": round(adjusted * 12 * 0.9, 2),
            "per_room_avg": round(adjusted / ((min_rooms + max_rooms) / 2), 2)
        })

    return pricing_tiers

# 示例: 基础价格 ¥80/房间
tiers = design_tiered_pricing(
    base_price_per_room=80,
    tiers=[
        {"rooms": (1, 50), "multiplier": 1.2},
        {"rooms": (51, 200), "multiplier": 1.0},
        {"rooms": (201, 500), "multiplier": 0.85},
        {"rooms": (501, float('inf')), "multiplier": 0.7}
    ]
)
```

---

## 五、企业生命周期定价策略

### 5.1 初创期 (0-1)

**目标**: 找到产品-市场匹配 (PMF)

**定价策略**:
```
特点:
- 产品不成熟，需要快速迭代
- 客户数量少，每客户价值高
- 现金流紧张

策略:
- 扁平制定价，简化决策
- 可以提供"创始客户"优惠
- 保持灵活性，允许谈判
- 价格区间: 成本 + 微利 (或补贴获客)

定价公式:
  价格 = 成本 × (1 + 目标利润率) + 客户获取补贴

示例:
  开发成本 ¥50,000/月, 目标10客户 → ¥5,000/客户/月
  或: 成本 ¥5,000, 加价30% → ¥6,500/月
```

### 5.2 成长期 (1-10)

**目标**: 规模化增长，优化单位经济

**定价策略**:
```
特点:
- PMF已确认
- 快速增长是首要目标
- 需要建立销售团队
- ARR成为关键指标

策略:
- 切换到分层定价
- 设计客户升级路径
- 引入年度合同锁定
- 价格区间: ARPU ¥2,000-20,000/月

定价公式:
  参考竞争对手 + 价值差异化溢价

示例 (酒店PMS):
  - 基础版: ¥50/房间/月 (50间起)
  - 专业版: ¥80/房间/月
  - 企业版: ¥120/房间/月 (含定制)
```

### 5.3 规模化期 (10-100)

**目标**: 优化效率，准备进入中大客户市场

**定价策略**:
```
特点:
- 品牌认知建立
- 客户留存重要
- 竞争加剧
- 需要差异化

策略:
- 引入客户成功团队
- 设计客户升级机制
- 年度合同 + 季度续费
- 价格区间: ARPU ¥20,000-100,000/月

定价公式:
  客户生命周期价值 (LTV) > 3倍 CAC
  LTV = ARPU × 毛利率 × 留存月数
```

### 5.4 成熟期 (100+)

**目标**: 市场领导地位，最大化利润

**定价策略**:
```
特点:
- 市场地位稳固
- 品牌溢价能力
- 可能考虑收购
- 二级市场机会

策略:
- 溢价定价策略
- 高端客户定制化
- 生态锁定
- 价格区间: ARPU ¥100,000+/月

定价公式:
  价格 = 竞争对手价格 × (1 + 差异化溢价率)
  差异化溢价率: 20-50%
```

---

## 六、定价实战工具箱

### 6.1 定价计算器

```python
class SaaSPricingCalculator:
    """SaaS定价计算器"""

    def __init__(self):
        self.cac = 0           # 客户获取成本
        self.cost_to_serve = 0  # 服务成本
        self.target_ltv_cac = 3.0  # LTV/CAC目标
        self.target_margin = 0.7   # 目标毛利率
        self.months_to_payback = 12  # 回收期(月)

    def cost_based_price(self, arpu_target: float) -> float:
        """
        成本加成定价
        基于目标ARPU反推
        """
        cost = self.cost_to_serve + (self.cac / self.months_to_payback)
        price = cost / self.target_margin
        return price

    def value_based_price(self, customer_value: float, value_ratio: float) -> float:
        """
        价值定价
        基于客户价值增量
        """
        return customer_value / value_ratio

    def market_based_price(self, competitor_price: float, differentiation: float) -> float:
        """
        竞争定价
        基于竞品价格和差异化
        """
        # differentiation: 0.0(无差异化) ~ 1.0(完全差异化)
        premium = 1.0 + (differentiation * 0.5)  # 最高溢价50%
        return competitor_price * premium

    def hybrid_price(self, **kwargs) -> dict:
        """
        混合定价建议
        综合多种方法
        """
        prices = {}

        if 'customer_value' in kwargs:
            prices['value_based'] = self.value_based_price(
                kwargs['customer_value'],
                kwargs.get('value_ratio', 5.0)
            )

        if 'competitor_price' in kwargs:
            prices['market_based'] = self.market_based_price(
                kwargs['competitor_price'],
                kwargs.get('differentiation', 0.3)
            )

        if 'arpu_target' in kwargs:
            prices['cost_based'] = self.cost_based_price(
                kwargs['arpu_target']
            )

        # 推荐价格: 中位数
        recommended = sorted(prices.values())[len(prices)//2]

        return {
            "all_prices": prices,
            "recommended": recommended,
            "range": (min(prices.values()), max(prices.values()))
        }

# 使用示例
calc = SaaSPricingCalculator()
calc.cac = 10000
calc.cost_to_serve = 500
calc.months_to_payback = 12

result = calc.hybrid_price(
    customer_value=50000,
    value_ratio=5.0,
    competitor_price=8000,
    differentiation=0.3
)
# 输出推荐定价
```

### 6.2 酒店AI产品定价模板

```python
class HotelAIProductPricing:
    """酒店AI产品定价模板"""

    # 价值量化基准
    VALUE_BENCHMARKS = {
        "revenue_management": {
            "description": "收益管理系统",
            "typical_improvement": 0.05,  # 5% RevPAR提升
            "value_calculation": "rooms * revpar * improvement * 30"
        },
        "channel_manager": {
            "description": "渠道管理器",
            "typical_improvement": 0.02,  # 2%营收增长
            "value_calculation": "revenue * 0.02"
        },
        "guest_engagement": {
            "description": "宾客互动系统",
            "typical_improvement": 0.10,  # 10%复购率提升
            "value_calculation": "revpar * 0.10 * avg_stay * guests"
        },
        "operational_efficiency": {
            "description": "运营效率工具",
            "typical_improvement": 0.15,  # 15%人力成本节约
            "value_calculation": "labor_cost * 0.15"
        }
    }

    @staticmethod
    def calculate_price_by_room(
        product_type: str,
        hotel_rooms: int,
        revpar: float,
        target_value_ratio: float = 5.0,
        days_per_month: int = 30
    ) -> dict:
        """
        按房间计算酒店AI产品定价
        """

        benchmark = HotelAIProductPricing.VALUE_BENCHMARKS.get(product_type)
        if not benchmark:
            return {"error": f"Unknown product type: {product_type}"}

        improvement = benchmark["typical_improvement"]

        # 月度价值增量
        monthly_value = hotel_rooms * revpar * improvement * days_per_month

        # 建议价格
        monthly_price = monthly_value / target_value_ratio
        annual_price = monthly_price * 12 * 0.85  # 年付85折
        price_per_room = monthly_price / hotel_rooms

        return {
            "product_type": benchmark["description"],
            "hotel_size": f"{hotel_rooms}间",
            "monthly_value_increase": f"¥{monthly_value:,.0f}",
            "suggested_monthly_price": f"¥{monthly_price:,.0f}",
            "suggested_annual_price": f"¥{annual_price:,.0f}",
            "price_per_room_month": f"¥{price_per_room:.0f}",
            "value_ratio_achieved": target_value_ratio,
            "improvement_rate_assumption": f"{improvement*100}%"
        }

# 使用示例
pricing = HotelAIProductPricing()

# 收益管理系统定价
result = pricing.calculate_price_by_room(
    product_type="revenue_management",
    hotel_rooms=150,
    revpar=350,
    target_value_ratio=5.0
)
print(result)
```

---

## 七、行业参考价格

### 7.1 酒店PMS系统 (2024-2025市场参考)

| 品牌 | 定价模式 | 价格区间 | 备注 |
|------|---------|---------|------|
| 石基 | 房间+功能 | ¥100-300/房间/月 | 高端市场 |
| 众荟 | 房间制 | ¥50-150/房间/月 | 中高端 |
| 绿云 | 房间+用户 | ¥40-100/房间/月 | 中端 |
| 别样红 | 订阅制 | ¥30-80/房间/月 | SMB |
| 云掌柜 | 房间制 | ¥20-50/房间/月 | 小微 |

### 7.2 收益管理系统

| 品牌 | 定价模式 | 价格区间 | 说明 |
|------|---------|---------|------|
| IDeaS | % GTV | 0.5-1.5% | 国际品牌 |
| OTA | 订阅+效果 | ¥2000-20000/月 | 按规模 |
| 众荟RMS | 订阅制 | ¥3000-15000/月 | 按酒店星级 |
| 直客通 | 效果分成 | 5-15% GMV | 微信直销 |

### 7.3 AI客服/前台

| 品牌 | 定价模式 | 价格区间 | 说明 |
|------|---------|---------|------|
| 携程AI | 已含在OTA费用 | - | OTA渠道内 |
| 美团AI | 已含在费用 | - | OTA渠道内 |
| 独立SaaS | 订阅+用量 | ¥500-5000/月 | 按消息量 |
| 企业定制 | 项目制 | ¥50,000-500,000 | 按需求 |

---

## 八、定价策略检查清单

### 8.1 上新定价前检查

```
□ 我们的客户是谁? (Customer Profile)
□ 客户的核心痛点是什么? (Pain Points)
□ 我们解决的价值是多少? (Value Quantification)
□ 竞品定价多少? (Competitive Analysis)
□ 我们的差异化是什么? (Differentiation)
□ 目标价值/价格比是多少? (Value/Price Ratio)
□ 价格是否与产品定位匹配? (Positioning)
□ 是否有升级路径? (Upgrade Path)
□ 客户能否算清ROI? (ROI Clarity)
```

### 8.2 定价调整检查

```
□ 为什么要调价? (Reason)
□ 调价时机对吗? (Timing)
□ 现有客户如何处理? (Existing Customers)
  - 全部涨价?
  - 差别对待?
  -  grandfather政策?
□ 如何沟通调价? (Communication)
□ 竞品会如何反应? (Competitive Response)
□ 预期收入影响? (Revenue Impact)
```

---

## 九、附录

### 9.1 关键术语

| 术语 | 定义 |
|------|------|
| ARPU | 平均每用户收入 (Average Revenue Per User) |
| ARR | 年度经常性收入 (Annual Recurring Revenue) |
| MRR | 月度经常性收入 (Monthly Recurring Revenue) |
| LTV | 客户生命周期价值 (Lifetime Value) |
| CAC | 客户获取成本 (Customer Acquisition Cost) |
| GMV | 商品交易总额 (Gross Merchandise Value) |
| GTV | 总交易额 (Gross Transaction Value) |

### 9.2 推荐阅读

1. Baremetrics - SaaS Pricing Models & Strategies Demystified
2. Stripe - Four SaaS Pricing Metrics
3. Price Intelligently - B2B SaaS Pricing Strategies
4. Hubspot - SaaS Pricing Strategy Guide
5. Lincoln Murphy - SaaS Pricing

---

## 九、酒店均价反推模型（OTA/私域 → 真实ADR）

> 新增章节：2026-04-01

### 9.1 价格漏斗模型

```
酒店总收入 = Σ(各渠道收入)
           = Σ(渠道占比 × 渠道价格 × (1-佣金率))

渠道类型:
  - OTA渠道: 携程/美团/飞猪/同程 (有佣金15%)
  - 私域渠道: 会员/企业微信/社群 (无佣金)
  - 协议渠道: 企业协议价 (无佣金)
  - 团队渠道: 旅行社/团队价 (低佣金)
  - 直客渠道: 前台/官网直销 (无佣金)
```

### 9.2 核心公式

```
真实ADR = W1×P1 + W2×P2 + W3×P3 + ...

其中:
W = 渠道占比
P = 渠道净价格

OTA净价 = 挂牌价 × 折扣系数(0.7-0.8) × (1-佣金15%)
私域净价 = 实际价格 × 1.0 (无佣金)
协议净价 = 协议价格 × 1.0 (无佣金)
```

### 9.3 档位折扣系数

| 酒店档次 | OTA折扣系数 | OTA渠道占比 | 说明 |
|---------|------------|-----------|------|
| 经济型 | 0.80 | 55-60% | 挂牌接近实际，OTA为主 |
| 中端型 | 0.75 | 40-50% | 混合渠道 |
| 高端型 | 0.70 | 30-40% | 协议/私域占比高 |
| 奢华型 | 0.65 | 20-30% | 协议/团队为主 |

### 9.4 快速估算（仅OTA数据）

```bash
# CLI工具
python hotel_adr_estimator.py quick --price 680 --type mid

# 输出示例:
# Input OTA Listed Price: 680
# Estimated Sold ADR: 559.5
# Estimated Net ADR: 525.08
# Discount to OTA: -25%
```

### 9.5 综合估算（多渠道）

```bash
# CLI工具
python hotel_adr_estimator.py estimate \
    --ota 680 720 650 \
    --private 580 600 \
    --corporate 620 \
    --commission 0.15
```

### 9.6 OTA入住率信号估算

```bash
# CLI工具
python hotel_adr_estimator.py occ --available 5 --rooms 150 --price-increase 20

# 信号规则:
# 仅剩3间 → OCC约90%
# 仅剩5间 → OCC约82%
# 仅剩10间 → OCC约75%
# 仅剩20间 → OCC约60%
```

---

## 十、OCC入住率估算模型

> 新增章节：2026-04-01

### 10.1 可用信号体系

| 信号类型 | 数据来源 | 可靠性 | 说明 |
|---------|---------|--------|------|
| **OTA库存** | 携程/美团/飞猪等"仅剩X间" | ⭐⭐⭐⭐ | 最直接的公开信号 |
| **官网/微信库存** | 官方直销渠道库存展示 | ⭐⭐⭐⭐ | 微信订房/官网直销 |
| OTA价格信号 | 价格涨幅 | ⭐⭐⭐ | 需求旺盛时涨价 |
| 预订进度 | 已预订比例 | ⭐⭐⭐⭐ | 距入住天数vs预订率 |
| 外部事件 | 展会/节假日 | ⭐⭐⭐ | 可量化影响 |
| 历史基线 | 自身数据 | ⭐⭐⭐⭐⭐ | 最可靠 |

### 10.2 OTA库存信号估算表

```
仅剩房间数    入住率估算    信号强度
────────────────────────────────
≤ 3间        90-95%       接近满房
4-5间       85-90%       非常紧张
6-10间      75-80%       紧张
11-20间     60-70%       中等
21-30间     50-60%       充足
> 30间      < 50%        很多空房
```

### 10.3 价格信号估算规则

```
价格涨幅      入住率估算    需求判断
────────────────────────────────
≥ +50%       92%+         极端高峰
≥ +30%       85%+         高峰
≥ +20%       78%+         较高
≥ +10%       72%+         中等偏高
-5% ~ +10%   65%         正常
< -15%       < 55%       低迷
```

### 10.4 事件影响系数

```python
event_impact = {
    "conference": {"small": 0.15, "medium": 0.20, "large": 0.30, "mega": 0.40},
    "exhibition": {"small": 0.20, "medium": 0.25, "large": 0.35, "mega": 0.50},
    "concert":   {"small": 0.10, "medium": 0.15, "large": 0.25, "mega": 0.35},
    "sports":     {"small": 0.15, "medium": 0.20, "large": 0.30, "mega": 0.40},
    "wedding":    {"small": 0.08, "medium": 0.12, "large": 0.18, "mega": 0.25},
    "holiday":    {"small": 0.25, "medium": 0.35, "large": 0.45, "mega": 0.60}
}
```

### 10.5 工具使用

```bash
# OTA库存信号
python hotel_occ_estimator.py inventory --available 5 --rooms 150

# 价格信号
python hotel_occ_estimator.py price --current 850 --baseline-price 650

# 事件信号
python hotel_occ_estimator.py event --type exhibition --scale large --weekend

# 综合多信号
python hotel_occ_estimator.py combined --available 5 --rooms 150 --current 850 --baseline-price 650
```

---

**版本历史**:
- V1.0 (2026-04-01): 初始版本，整合SaaS定价模型、酒店科技定价、企业生命周期定价策略
- V1.1 (2026-04-01): 新增酒店均价反推模型（OTA/私域 → 真实ADR）
- V1.2 (2026-04-01): 新增OCC入住率估算模型（多信号体系）

**下次更新计划**:
- 加入更多AI项目定价案例
- 补充竞价定价模型
- 增加中国本土定价策略洞察
