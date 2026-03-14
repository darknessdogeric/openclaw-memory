# B端收益管理SKILL集群 (Revenue Management SKILL Cluster)

> **定位**: B端AI运营官核心能力模块
> **版本**: V1.0
> **来源**: 基于SM-SOP-RM收益管理标准SOP + HotelAI Growth OS 2.0
> **层级**: AHL场景SKILL化架构V4.0 - B端AI运营官子模块

---

## 一、SKILL集群架构

```
B端AI运营官
    └── 收益管理SKILL群 (Revenue Management Cluster)
            ├── SKILL-RM-01 动态定价策略 (Dynamic Pricing)
            ├── SKILL-RM-02 需求预测分析 (Demand Forecasting)
            ├── SKILL-RM-03 库存优化管理 (Inventory Optimization)
            ├── SKILL-RM-04 渠道库存分配 (Channel Inventory)
            ├── SKILL-RM-05 团体业务评估 (Group Business Evaluation)
            └── SKILL-RM-06 收益数据分析 (Revenue Analytics)
```

---

## 二、细分SKILL详细定义

### SKILL-RM-01 动态定价策略 (Dynamic Pricing Strategy)

#### 核心功能
基于多维度因子计算最优房价，实现收益最大化。

#### 定价公式
```python
最优房价 = 基础房价 × (1 + 需求调整系数 + 竞争调整系数 + 库存调整系数)

其中:
- 需求调整系数 = f(历史同期需求, 预订进度, 市场活动, 本地事件)
- 竞争调整系数 = f(竞品价格, 价格带定位, 品牌溢价)
- 库存调整系数 = f(剩余房量, 销售周期, 房型稀缺性)
```

#### 定价策略类型
| 策略类型 | 触发条件 | 调整幅度 | 适用场景 |
|---------|---------|---------|---------|
| **早鸟优惠** | 提前>14天预订 | -5%~-15% | 淡季获客 |
| **连住优惠** | 入住>2晚 | -8%~-12% | 提升平均住宿时长 |
| **尾房促销** | 入住前<3天且房量>20% | -20%~-35% | 临期去化 |
| **溢价策略** | 需求>80%容量 | +10%~+30% | 旺季/会展期间 |
| **会员专享** | 会员身份识别 | -5%~-10% | 私域沉淀 |

#### 输入参数
```json
{
  "base_price": 500,
  "room_type": "豪华大床房",
  "date": "2026-05-01",
  "current_booking_pace": 0.65,
  "remaining_inventory": 45,
  "competitor_prices": [480, 520, 550],
  "local_events": ["五一假期", "音乐节"],
  "historical_occupancy": 0.88
}
```

#### 输出结果
```json
{
  "recommended_price": 650,
  "price_range": {"min": 580, "max": 720},
  "confidence": 0.85,
  "factors": {
    "demand_impact": +15%,
    "competition_impact": +5%,
    "inventory_impact": +8%
  },
  "strategy": "溢价策略",
  "expected_revenue": 29250
}
```

#### 决策规则
1. **当预订进度<30%且入住<7天** → 启动促销策略
2. **当预订进度>80%且入住>14天** → 启动溢价策略
3. **当竞品价格下调>15%** → 评估跟降或差异化
4. **当大型活动/节假日** → 提前30天启动收益锁定

---

### SKILL-RM-02 需求预测分析 (Demand Forecasting)

#### 核心功能
预测未来特定日期的客房需求量，为定价和库存决策提供数据支撑。

#### 预测模型
```python
预测需求 = 基础需求 × 季节因子 × 事件因子 × 趋势因子 × 随机因子

基础需求 = 过去30天同类型日期的平均需求量
季节因子 = 历史同期需求波动系数
事件因子 = 本地活动/节假日影响系数
趋势因子 = 近期预订增长/下降趋势
随机因子 = 不可预测波动（正态分布，σ=5%）
```

#### 预测维度
| 维度 | 预测周期 | 准确度要求 |
|-----|---------|-----------|
| 日度预测 | 未来14天 | ±5% |
| 周度预测 | 未来4周 | ±8% |
| 月度预测 | 未来3月 | ±12% |
| 季度预测 | 未来1年 | ±15% |

#### 预测因子权重
```
历史同期数据    40%
当前预订进度    25%
市场趋势        15%
本地事件/节假日 15%
竞品动态         5%
```

#### 预测输出示例
```json
{
  "forecast_date": "2026-05-01",
  "predicted_demand": 180,
  "confidence_interval": [165, 195],
  "accuracy_score": 0.88,
  "key_drivers": [
    {"factor": "五一假期", "impact": +35%},
    {"factor": "音乐节", "impact": +12%},
    {"factor": "天气", "impact": +3%}
  ],
  "recommendation": "建议启动溢价策略，提前关闭部分促销渠道"
}
```

---

### SKILL-RM-03 库存优化管理 (Inventory Optimization)

#### 核心功能
优化房型分配策略，平衡不同客源类型的需求，最大化整体收益。

#### 房型分配策略
```
总库存 = 散客库存 + 团体库存 + 保留库存 + 超额预订库存

分配原则:
- 高需求日期: 团体占比 ≤ 30%
- 中需求日期: 团体占比 ≤ 50%
- 低需求日期: 团体占比 ≤ 70%
- 保留库存: 始终保留 5% 应急/高价值散客
```

#### 房型升级策略
```python
def upgrade_strategy(available_rooms, guest_profile):
    # 免费升级条件
    if guest_profile['loyalty_tier'] == '钻石' and available_rooms['suite'] > 5:
        return "免费升级至套房"
    
    # 付费升级推荐
    if guest_profile['price_sensitivity'] == 'low':
        upgrade_price = calculate_upgrade_price(base_room, target_room)
        return f"推荐付费升级，价格: ¥{upgrade_price}"
    
    return "维持原房型"
```

#### 库存监控预警
| 预警级别 | 触发条件 | 响应动作 |
|---------|---------|---------|
| 🔴 紧急 | 入住前3天且预订<50% | 启动全员促销 |
| 🟠 注意 | 入住前7天且预订<60% | 加大渠道投放 |
| 🟡 关注 | 入住前14天且预订<70% | 评估促销策略 |
| 🟢 正常 | 预订进度符合预期 | 维持当前策略 |

---

### SKILL-RM-04 渠道库存分配 (Channel Inventory Management)

#### 核心功能
在各销售渠道间动态分配库存，优化渠道组合，降低获客成本。

#### 渠道优先级矩阵
```
优先级排序（收益优先级）:
1. 自有渠道（官网/小程序）- 佣金0%
2. 会员直销（企微/电话）- 佣金0%
3. 协议客户（B2B）- 佣金5%
4. OTA直销（携程/美团）- 佣金15-20%
5. OTA促销（限时活动）- 佣金25%
```

#### 渠道库存分配规则
```python
渠道库存分配 = {
    "自有渠道": 总库存 × 0.30,      # 30%预留
    "会员直销": 总库存 × 0.15,      # 15%预留
    "协议客户": 总库存 × 0.20,      # 20%预留
    "OTA常规": 总库存 × 0.30,       # 30%开放
    "OTA促销": 根据去化情况动态释放
}

# 动态调整逻辑
if 预订进度 < 0.6 and 入住前天数 < 7:
    渠道库存分配["OTA促销"] += 总库存 × 0.10
    渠道库存分配["自有渠道"] -= 总库存 × 0.10
```

#### 关房/开房策略
```
关房条件:
- 预订进度 > 90% 且 入住前 < 3天 → 关闭促销渠道
- 预订进度 > 95% 且 入住前 < 7天 → 关闭OTA促销价
- VIP团入住 → 预留整层/整栋

开房条件:
- 预订进度 < 50% 且 入住前 < 3天 → 全面开放所有渠道
- 团体取消 → 即时释放库存至全渠道
```

---

### SKILL-RM-05 团体业务评估 (Group Business Evaluation)

#### 核心功能
评估团体预订请求的价值，辅助决策是否接受及报价策略。

#### 团体价值评分模型
```python
def evaluate_group_value(group_request, forecast_data):
    """
    团体价值 = 直接收入 - 机会成本 + 战略价值 - 风险成本
    """
    
    # 1. 直接收入
    room_revenue = group_request.room_nights * group_request.room_rate
    f_b_revenue = group_request.catering_budget if group_request.has_catering else 0
    other_revenue = group_request.av_revenue + group_request.misc_revenue
    direct_revenue = room_revenue + f_b_revenue + other_revenue
    
    # 2. 机会成本（散客损失）
    displacement_cost = calculate_displacement_cost(
        group_request.dates, 
        group_request.room_nights,
        forecast_data
    )
    
    # 3. 战略价值
    strategic_value = 0
    if group_request.is_key_account:
        strategic_value += 5000  # 关键客户加分
    if group_request.has_repeat_potential:
        strategic_value += 3000  # 复购潜力加分
    if group_request.is_high_profile_event:
        strategic_value += 10000  # 高曝光活动加分
    
    # 4. 风险成本
    risk_cost = 0
    if group_request.cancel_policy == "宽松":
        risk_cost += direct_revenue * 0.15
    if group_request.payment_terms == "账期>30天":
        risk_cost += direct_revenue * 0.05
    
    # 总评分
    total_value = direct_revenue - displacement_cost + strategic_value - risk_cost
    
    return {
        "total_value": total_value,
        "direct_revenue": direct_revenue,
        "displacement_cost": displacement_cost,
        "strategic_value": strategic_value,
        "risk_cost": risk_cost,
        "recommendation": "接受" if total_value > 0 else "拒绝或重新谈判"
    }
```

#### 团体报价策略
| 团体类型 | 底价折扣 | 报价策略 | 谈判空间 |
|---------|---------|---------|---------|
| 企业会议 | 散客价的75-85% | 固定价格 | 5-10% |
| 旅游团队 | 散客价的65-75% | 阶梯价格 | 10-15% |
| 婚宴 | 套餐价 | 全包方案 | 服务内容 |
| 政府/协会 | 散客价的70-80% | 协议价格 | 5-8% |

---

### SKILL-RM-06 收益数据分析 (Revenue Analytics)

#### 核心功能
提供收益管理相关的数据分析、报表生成和洞察建议。

#### 核心指标监控
```python
核心KPI = {
    "RevPAR": 客房总收入 / 可售房晚数,
    "ADR": 客房总收入 / 实际售出房晚数,
    "OCC": 实际售出房晚数 / 可售房晚数,
    "Yield": 实际RevPAR / 潜在最大RevPAR,
    "渠道占比": {
        "自有渠道": 自有渠道收入 / 总收入,
        "OTA": OTA收入 / 总收入,
        "协议": 协议客户收入 / 总收入
    },
    "价格实现率": 实际ADR / 挂牌价
}
```

#### 日报模板
```markdown
# 收益日报 - [日期]

## 核心指标
- RevPAR: ¥XXX (↑X% 同比)
- ADR: ¥XXX (↑X% 同比)
- OCC: XX% (↑X% 同比)

## 渠道表现
| 渠道 | 间夜数 | 收入 | 占比 | 环比 |
|-----|-------|-----|-----|-----|
| 官网 | XX | ¥XX | XX% | ↑X% |
| 携程 | XX | ¥XX | XX% | ↓X% |
| 美团 | XX | ¥XX | XX% | →0% |

## 未来14天预测
- 高需求日: X天 (建议溢价)
- 中需求日: X天 (维持策略)
- 低需求日: X天 (建议促销)

## 行动建议
1. [具体建议1]
2. [具体建议2]
3. [具体建议3]
```

#### 竞品对标分析
```python
def competitor_benchmark(our_hotel, competitors):
    analysis = {
        "price_position": our_hotel.adr / avg([c.adr for c in competitors]),
        "ranking": sort_by_adr([our_hotel] + competitors).index(our_hotel) + 1,
        "gap_analysis": {
            "premium_rooms": our_hotel.premium_pct - avg_competitor.premium_pct,
            "service_score": our_hotel.service_score - avg_competitor.service_score
        },
        "recommendation": generate_pricing_recommendation()
    }
    return analysis
```

---

## 三、SKILL间协作流程

### 典型工作流: 每日收益管理晨会决策

```
┌─────────────────────────────────────────────────────────────┐
│                      每日6:00 自动执行                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 1: 需求预测SKILL                                      │
│  - 预测未来14天每日需求                                     │
│  - 识别高/中/低需求日                                       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 2: 动态定价SKILL                                      │
│  - 基于预测结果计算最优价格                                 │
│  - 生成价格调整建议                                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 3: 库存优化SKILL                                      │
│  - 评估当前库存分配合理性                                   │
│  - 生成房型/渠道调整建议                                    │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 4: 数据分析SKILL                                      │
│  - 生成收益日报                                             │
│  - 提供决策建议汇总                                         │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  STEP 5: B端AI运营官决策                                    │
│  - 审核自动化建议                                           │
│  - 确认或调整策略                                           │
│  - 一键执行或转人工复核                                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 四、与其他SKILL的协作关系

```
收益管理SKILL群
    │
    ├──→ 市场营销SKILL群
    │      └── 提供: 价格策略指导促销方案
    │      └── 接收: 营销活动对需求的影响预测
    │
    ├──→ 前厅运营SKILL群
    │      └── 提供: 房型升级策略、超额预订控制
    │      └── 接收: 实际入住率、No-show数据
    │
    ├──→ 客房管理SKILL群
    │      └── 提供: 房型维修/停用对库存的影响评估
    │      └── 接收: 可用房量实时数据
    │
    └──→ 财务自动化SKILL群
           └── 提供: 收益预测用于现金流预测
           └── 接收: 实际收入数据用于模型校准
```

---

## 五、实施路线图

### Phase 1: 基础能力 (Month 1-2)
- [ ] 部署动态定价SKILL基础版
- [ ] 接入PMS实时库存数据
- [ ] 建立竞品价格监控

### Phase 2: 预测能力 (Month 3-4)
- [ ] 上线需求预测SKILL
- [ ] 历史数据模型训练
- [ ] 预测准确率验证

### Phase 3: 优化能力 (Month 5-6)
- [ ] 部署库存优化SKILL
- [ ] 团体业务评估上线
- [ ] 渠道库存自动化

### Phase 4: 智能化 (Month 7+)
- [ ] 全自动化决策闭环
- [ ] 异常检测与预警
- [ ] 持续学习与模型优化

---

## 六、KPI与效果评估

| 指标 | 基准值 | 目标值 | 达成标准 |
|-----|-------|-------|---------|
| RevPAR提升 | - | +10-15% | 6个月 |
| 定价决策准确率 | - | >80% | 3个月 |
| 预测准确率(14天) | - | ±5% | 4个月 |
| 人工干预率 | 100% | <20% | 6个月 |
| 系统响应时间 | - | <2秒 | 1个月 |

---

**文档版本**: V1.0  
**创建日期**: 2026-03-06  
**基于**: SM-SOP-RM收益管理标准SOP + HotelAI Growth OS 2.0  
**归属**: AHL场景SKILL化架构V4.0 - B端AI运营官模块
