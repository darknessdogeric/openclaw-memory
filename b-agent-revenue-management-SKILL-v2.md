# B端收益管理SKILL集群 V2.0 (深度扩展版)

> **定位**: B端AI运营官核心能力模块 - 行业顶级版本  
> **版本**: V2.0 (深度扩展)  
> **来源**: 中旅SOP + 国际RMS最佳实践(Duetto/IDeaS/Atomize) + AI/ML前沿算法  
> **层级**: AHL场景SKILL化架构V4.0 - B端AI运营官旗舰模块  
> **目标**: 单体酒店→国际连锁级别的收益管理能力

---

## 版本升级说明

### V1.0 → V2.0 升级亮点

| 维度 | V1.0 (中旅基础版) | V2.0 (国际顶级版) |
|------|------------------|------------------|
| **定价算法** | 简单系数调整 | 机器学习+多维度动态模型 |
| **预测能力** | 14天基础预测 | 365天滚动预测+事件影响建模 |
| **竞争策略** | 被动跟价 | 主动策略+价格锚定+心理定价 |
| **渠道管理** | 静态分配 | 动态优化+佣金效率最大化 |
| **团体评估** | 基础价值计算 | Displacement分析+战略价值量化 |
| **自动化** | 建议+人工确认 | 全自动闭环+异常监控 |
| **KPI体系** | 基础RevPAR | 全维度RGI/GOPPAR/RevPASH |

---

## 一、SKILL集群架构 V2.0

```
B端AI运营官
    └── 收益管理SKILL集群 V2.0 (旗舰版)
            │
            ├── 【核心定价层】
            │   ├── SKILL-RM-01 动态定价引擎 (Dynamic Pricing Engine)
            │   ├── SKILL-RM-02 竞品价格策略 (Competitive Intelligence)
            │   └── SKILL-RM-03 心理定价优化 (Behavioral Pricing)
            │
            ├── 【预测智能层】
            │   ├── SKILL-RM-04 AI需求预测 (AI Demand Forecasting)
            │   ├── SKILL-RM-05 事件影响建模 (Event Impact Modeling)
            │   └── SKILL-RM-06 取消率预测 (Cancellation Prediction)
            │
            ├── 【库存优化层】
            │   ├── SKILL-RM-07 房型库存优化 (Room Type Optimization)
            │   ├── SKILL-RM-08 渠道动态分配 (Channel Optimization)
            │   └── SKILL-RM-09 超额预订策略 (Overbooking Strategy)
            │
            ├── 【团体商务层】
            │   ├── SKILL-RM-10 团体价值评估 (Group Value Analysis)
            │   ├── SKILL-RM-11 Displacement分析 (Displacement Analysis)
            │   └── SKILL-RM-12 长住客管理 (Extended Stay Optimization)
            │
            ├── 【餐饮收益层】
            │   ├── SKILL-RM-13 餐饮收益管理 (F&B Revenue Management)
            │   ├── SKILL-RM-14 宴会定价策略 (Catering Pricing)
            │   └── SKILL-RM-15 RevPASH优化 (RevPASH Optimization)
            │
            └── 【分析决策层】
                ├── SKILL-RM-16 收益数据分析 (Revenue Analytics)
                ├── SKILL-RM-17 RGI对标分析 (RGI Benchmarking)
                └── SKILL-RM-18 自动化决策闭环 (Automated Decision Loop)
```

**总计**: 18个细分SKILL，覆盖收益管理全场景

---

## 二、核心定价层

### SKILL-RM-01 动态定价引擎 V2.0 (Dynamic Pricing Engine)

#### 2.1 核心定价算法 - ML-Based Dynamic Pricing

```python
# V2.0 机器学习定价模型
class MLDynamicPricingEngine:
    """
    基于机器学习的动态定价引擎
    集成：随机森林 + XGBoost + 时间序列模型
    """
    
    def calculate_optimal_price(self, pricing_context):
        """
        最优房价计算 - 多模型集成
        """
        # 1. 基础价格 (基于成本+竞争)
        base_price = self.calculate_base_price(pricing_context)
        
        # 2. 需求因子 (ML预测)
        demand_multiplier = self.ml_demand_model.predict(
            date=pricing_context.date,
            historical_bookings=pricing_context.booking_pace,
            market_conditions=pricing_context.market_data,
            events=pricing_context.local_events
        )
        
        # 3. 竞争因子 (竞品响应模型)
        competition_response = self.competition_model.predict(
            competitor_prices=pricing_context.competitor_prices,
            price_positioning=pricing_context.desired_position,
            price_elasticity=pricing_context.elasticity
        )
        
        # 4. 库存压力因子
        inventory_pressure = self.inventory_model.calculate(
            remaining_rooms=pricing_context.remaining_inventory,
            days_to_arrival=pricing_context.lead_time,
            booking_velocity=pricing_context.booking_velocity
        )
        
        # 5. 客户细分因子 (个性化定价)
        segment_adjustment = self.segment_model.calculate(
            customer_segment=pricing_context.customer_segment,
            loyalty_tier=pricing_context.loyalty_tier,
            booking_channel=pricing_context.channel
        )
        
        # 6. 时间衰减因子 (越近越贵/便宜)
        time_decay = self.time_decay_model.calculate(
            lead_time=pricing_context.lead_time,
            demand_curve=pricing_context.demand_curve
        )
        
        # 最终价格计算 (集成学习)
        optimal_price = base_price * (
            demand_multiplier * 0.35 +          # 需求权重35%
            competition_response * 0.25 +       # 竞争权重25%
            inventory_pressure * 0.20 +         # 库存权重20%
            segment_adjustment * 0.15 +         # 细分权重15%
            time_decay * 0.05                   # 时间权重5%
        )
        
        # 约束条件
        optimal_price = self.apply_constraints(
            price=optimal_price,
            min_price=pricing_context.min_price,
            max_price=pricing_context.max_price,
            rate_fences=pricing_context.rate_fences
        )
        
        return OptimalPriceResult(
            price=optimal_price,
            confidence=self.calculate_confidence(),
            factors_breakdown=self.get_factor_breakdown(),
            recommendation=self.generate_recommendation()
        )
```

#### 2.2 定价策略矩阵 (18种策略)

| 策略类型 | 触发条件 | 定价逻辑 | 预期效果 |
|---------|---------|---------|---------|
| **早鸟战略** | 提前>21天，预订<20% | BAR-15%~20% | 锁定远期需求，降低不确定性 |
| **连住激励** | LOS≥3晚 | 每晚递减5% | 提升平均住宿时长，减少换房成本 |
| **尾房清仓** | 入住前<48h，剩余>15% | BAR-25%~35% | 临期去化，减少空房损失 |
| **周末溢价** | 周五/六，需求>80% | BAR+20%~40% | 捕捉休闲需求高峰 |
| **会展锚定** | 大型活动前90天 | 阶梯涨价至BAR+50% | 收益最大化 |
| **会员专享** | 会员身份识别 | BAR-5%~12% | 私域沉淀，提升LTV |
| **企业协议** | 协议客户+提前预订 | BAR-10%~18% | 稳定基础需求 |
| **最后一分钟** | 入住当天，剩余<10间 | BAR+10%~30% | 捕捉紧急需求 |
| **套餐捆绑** | 淡季/工作日 | 房+餐+SPA打包 | 提升综合消费 |
| **动态BAR** | 每4小时重算 | 基于实时预订速度 | 精准响应市场 |
| **竞品跟随** | 竞品降价>10% | 选择性跟降或差异化 | 保持竞争力 |
| **价格锚定** | 新客首次访问 | 展示高价房作为锚点 | 提升BAR转化率 |
| **闪购限量** | 特定时段 | 限量10间，限时4小时 | 制造稀缺性 |
| **淡旺季平滑** | 季节转换期 | 渐进式调价 | 避免需求断崖 |
| **升级诱导** | 低房型库存紧张 | 高房型展示优惠价 | 提升ADR |
| **取消重构** | 高取消率房型 | 预付价+不可退折扣 | 降低NOSHOW风险 |
| **渠道差异化** | 多平台投放 | 各渠道±5%差异 | 佣金效率优化 |
| **预测修正** | 实际偏离预测>15% | 触发紧急调价 | 修正偏差 |

#### 2.3 价格栅栏 (Rate Fences) 设计

```python
# 价格栅栏 - 防止套利，细分客群
RATE_FENCES = {
    "预订条件": {
        "预付价": {"discount": "8-12%", "condition": "全额预付，不可退"},
        "标准价": {"discount": "0%", "condition": "免费取消，到店付"},
        "会员价": {"discount": "5-10%", "condition": "会员登录+积分累积"},
    },
    "入住条件": {
        "连住价": {"discount": "5-8%/晚", "condition": "LOS≥3晚"},
        "周末价": {"premium": "10-20%", "condition": "周五/六入住"},
        "工作日价": {"discount": "5-10%", "condition": "周日-周四"},
    },
    "客群条件": {
        "企业协议": {"discount": "10-20%", "condition": "协议代码+企业邮箱"},
        "政府协议": {"discount": "15-25%", "condition": "公务卡+出差证明"},
        "长住客": {"discount": "20-30%", "condition": "≥7晚，月结"},
    },
    "渠道条件": {
        "直销价": {"discount": "5%", "condition": "官网/小程序/电话"},
        "OTA价": {"premium": "0%", "condition": "携程/美团等平台"},
    }
}
```

---

### SKILL-RM-02 竞品价格策略 (Competitive Intelligence)

#### 2.1 竞品监控体系

```python
class CompetitiveIntelligenceSystem:
    """
    竞品价格智能监控系统
    """
    
    def monitor_competitor_prices(self):
        for competitor in self.competitors:
            prices = self.scrape_prices(competitor)
            price_changes = self.analyze_changes(prices)
            strategy = self.identify_strategy(price_changes)
            
            if price_changes['max_change'] > 0.10:
                self.send_alert({
                    'competitor': competitor.name,
                    'changes': price_changes,
                    'strategy': strategy
                })
```

#### 2.2 价格定位策略

| 定位 | 策略 | 适用场景 |
|------|------|---------|
| **市场领导者** | 竞品最高价+5-10% | 品牌力TOP3，服务差异化明显 |
| **挑战者** | 市场平均+10-15% | 服务有特色，位置/硬件优势 |
| **追随者** | 跟随主要竞品±5% | 标准化产品，无明显短板 |
| **渗透者** | 市场平均-10-20% | 成本优势明显，追求市场份额 |

---

### SKILL-RM-03 心理定价优化 (Behavioral Pricing)

#### 3.1 八大心理定价技巧

| 技巧 | 原理 | 应用 | 示例 |
|------|------|------|------|
| **尾数定价** | 左位效应 | 所有展示价格 | ¥500→¥499 |
| **锚定效应** | 对比效应 | 房型排序 | 先展示¥1200套房 |
| **诱饵效应** | 引导选择 | 三房型策略 | 标准¥500，豪华¥550(目标)，套房¥900 |
| **框架效应** | 损失厌恶 | 会员价展示 | "节省¥100"而非"¥500" |
| **稀缺性** | FOMO心理 | 库存展示 | "仅剩3间，12人浏览" |
| **社会认同** | 从众心理 | 热销标签 | "本周已订87间" |
| **禀赋效应** | 拥有不愿失去 | 免费升级 | "已为您升级，确认?" |
| **价格分割** | 降低感知总价 | 每日价格 | "¥500/晚×2晚" |

---

## 三、预测智能层

### SKILL-RM-04 AI需求预测 (AI Demand Forecasting)

#### 4.1 多模型集成预测框架

```python
class AIDemandForecaster:
    """
    AI驱动的需求预测系统
    集成：Prophet + LSTM + XGBoost
    """
    
    def forecast_demand(self, target_date, horizon_days=365):
        forecasts = {}
        
        # Prophet模型 - 趋势+季节性
        forecasts['prophet'] = self.models['prophet'].predict(
            periods=horizon_days,
            seasonality_mode='multiplicative'
        )
        
        # LSTM模型 - 长期依赖
        forecasts['lstm'] = self.models['lstm'].predict(
            sequence_length=90,
            features=['bookings', 'cancellations', 'web_traffic']
        )
        
        # XGBoost模型 - 多特征
        forecasts['xgboost'] = self.models['xgboost'].predict(
            features=self.extract_features(target_date)
        )
        
        # 集成加权
        ensemble_weights = {
            'prophet': 0.3,
            'lstm': 0.4,
            'xgboost': 0.3
        }
        
        return self.models['ensemble'].combine(forecasts, ensemble_weights)
```

#### 4.2 预测准确度KPI

| 预测周期 | MAPE目标 | Bias目标 | 评审频率 |
|---------|---------|---------|---------|
| 1-7天 | <5% | ±3% | 每日 |
| 8-30天 | <10% | ±5% | 每周 |
| 31-90天 | <15% | ±8% | 每月 |
| 91-365天 | <20% | ±10% | 每季度 |

---

### SKILL-RM-05 事件影响建模 (Event Impact Modeling)

#### 5.1 事件影响计算

```python
class EventImpactModel:
    """
    本地事件对酒店需求的影响建模
    """
    
    EVENT_MULTIPLIERS = {
        'holiday': 1.5,
        'sports': 1.8,
        'concert': 1.6,
        'exhibition': 1.4,
        'conference': 1.3,
        'weather_bad': 0.7,
        'construction': 0.8
    }
    
    def calculate_event_impact(self, event_info, hotel_profile):
        base = self.EVENT_MULTIPLIERS[event_info['type']]
        distance_factor = max(0.3, 1 - (distance_km / 10))
        scale_factor = min(2.0, 1 + (attendees / 10000))
        match_score = self.calculate_audience_match(hotel_profile, event_info)
        competition_factor = 1 / len(nearby_hotels)
        
        total_impact = base * distance_factor * scale_factor * match_score * competition_factor
        return total_impact
```

---

### SKILL-RM-06 取消率预测 (Cancellation Prediction)

#### 6.1 取消风险因素评分

| 因素 | 高风险信号 | 风险加分 |
|------|-----------|---------|
| 提前期 | >60天 | +0.40 |
| 渠道 | OTA免费取消 | +0.35 |
| 预付状态 | 未预付 | +0.30 |
| 客群 | 新客 | +0.25 |
| 房型 | 高取消率房型 | +0.20 |
| 价格 | 促销价 | +0.15 |

---

## 四、库存优化层

### SKILL-RM-07 房型库存优化 (Room Type Optimization)

#### 7.1 房型升级优化

```python
def optimize_room_upgrades(demand_forecast, inventory_status):
    """
    基于需求和库存的升级优化策略
    """
    strategies = {
        ' sold_out_low': {
            'condition': '低档房型售罄，高档有库存',
            'action': '自动免费升级+道歉补偿',
            'revenue_impact': '保留客户，避免流失'
        },
        'pressure_high': {
            'condition': '高档房型库存压力大',
            'action': '付费升级推荐+小礼品',
            'revenue_impact': 'ADR提升10-20%'
        },
        'balanced': {
            'condition': '各房型库存均衡',
            'action': '维持正常销售',
            'revenue_impact': '标准收益'
        }
    }
```

---

### SKILL-RM-08 渠道动态分配 (Channel Optimization)

#### 8.1 渠道优先级与佣金效率

| 渠道 | 优先级 | 佣金率 | 策略 |
|------|--------|--------|------|
| 官网/小程序 | P0 | 0% | 优先库存，最佳价格 |
| 会员直销 | P1 | 0% | 专属库存，会员价 |
| 企业协议 | P2 | 5% | B2B专属配额 |
| OTA直销 | P3 | 15-20% | 动态库存，竞争价格 |
| OTA促销 | P4 | 25% | 尾房/淡季释放 |

---

### SKILL-RM-09 超额预订策略 (Overbooking Strategy)

#### 9.1 智能超额预订模型

```python
def calculate_overbooking_level(date, room_type):
    """
    基于历史NOSHOW率的智能超额预订
    """
    base_no_show_rate = get_historical_no_show(date, room_type)
    cancellation_risk = predict_cancellation_risk(date)
    walk_in_probability = predict_walk_ins(date)
    
    # 超额预订房间数
    overbooking_rooms = (
        confirmed_bookings * base_no_show_rate +
        confirmed_bookings * cancellation_risk -
        walk_in_probability
    )
    
    # 风险控制：Walk成本vs空房损失
    walk_cost = overbooking_rooms * cost_per_walk
    spoilage_cost = empty_rooms * adr
    
    return optimize_overbooking_level(walk_cost, spoilage_cost)
```

---

## 五、团体商务层

### SKILL-RM-10 团体价值评估 (Group Value Analysis)

#### 10.1 综合价值评估公式

```
团体总收益 = 客房收入 + 餐饮收入 + 其他收入
团体总成本 = 机会成本 + 增量成本 + 风险成本
净团体价值 = 团体总收益 - 团体总成本 + 战略价值

决策规则:
- 净价值 > 0 → 接受
- 净价值 < 0 → 拒绝或重新谈判
```

---

### SKILL-RM-11 Displacement分析 (Displacement Analysis)

#### 11.1 Displacement成本计算

```python
def calculate_displacement_cost(group_request, forecast_data):
    """
    计算接受团体导致的散客损失
    """
    displaced_demand = min(
        group_request.room_nights,
        forecast_data.predicted_transient_demand
    )
    
    # 被置换的散客价值
    displaced_revenue = (
        displaced_demand * 
        forecast_data.predicted_transient_adr * 
        forecast_data.transient_consumption_multiplier
    )
    
    # 未来影响（散客可能不再预订）
    future_impact = displaced_demand * customer_lifetime_value * 0.1
    
    total_displacement_cost = displaced_revenue + future_impact
    return total_displacement_cost
```

---

## 六、餐饮收益层

### SKILL-RM-13 餐饮收益管理 (F&B Revenue Management)

#### 13.1 餐饮收益指标

| 指标 | 计算方式 | 目标值 |
|------|---------|--------|
| **RevPASH** | 每小时每座位收入 | 持续提升 |
| **座位周转率** | 每日用餐批次 | 2.5-3.5次 |
| **人均消费** | 总营收/用餐人数 | 对标竞品 |
| **上座率** | 实际座位/总座位 | >75% |

---

### SKILL-RM-14 宴会定价策略 (Catering Pricing)

#### 14.1 宴会定价模型

```python
# 宴会定价要素
BANQUET_PRICING = {
    "基础成本": {
        "食材": "菜单成本×人数",
        "人工": "服务费×人数",
        "场地": "场租×时长"
    },
    "溢价因子": {
        "周末": "+10-15%",
        "节假日": "+20-30%",
        "旺季": "+15-25%",
        "知名主厨": "+20%"
    },
    "折扣空间": {
        "大型团体(>20桌)": "5-10%",
        "淡季": "10-15%",
        "预付全款": "3-5%",
        "长期合作": "8-12%"
    }
}
```

---

## 七、分析决策层

### SKILL-RM-16 收益数据分析 (Revenue Analytics)

#### 16.1 核心KPI体系

| KPI | 计算方式 | 基准 | 优秀 |
|-----|---------|------|------|
| **RevPAR** | 总客房收入/可售房数 | 行业平均 | 高于竞品15% |
| **ADR** | 总客房收入/售出房数 | 市场平均 | 高于市场10% |
| **OCC** | 售出房数/可售房数 | 65-70% | >80% |
| **GOPPAR** | 经营毛利/可售房数 | 30-40% | >50% |
| **RGI** | 酒店RevPAR/市场RevPAR | 100 | >110 |
| **MPI** | 酒店OCC/市场OCC | 100 | >105 |
| **ARI** | 酒店ADR/市场ADR | 100 | >105 |

---

### SKILL-RM-17 RGI对标分析 (RGI Benchmarking)

#### 17.1 竞争力指数解读

```
RGI = (酒店RevPAR / 竞争群RevPAR) × 100

RGI > 110: 收益表现优秀，市场领先
RGI 100-110: 收益表现良好，符合市场
RGI 90-100: 收益表现一般，需要优化
RGI < 90: 收益表现落后，急需改进
```

---

### SKILL-RM-18 自动化决策闭环 (Automated Decision Loop)

#### 18.1 全自动收益管理流程

```
数据采集 → AI预测 → 策略生成 → 自动执行 → 效果监控 → 模型优化
    │         │         │         │         │         │
    ▼         ▼         ▼         ▼         ▼         ▼
  PMS/OTA   ML模型    决策引擎   RMS系统   仪表板    反馈学习
```

#### 18.2 自动化决策规则

| 场景 | 触发条件 | 自动动作 | 人工复核条件 |
|------|---------|---------|-------------|
| 紧急降价 | 预订<50%且<3天入住 | 自动降价15% | 降价>25%需确认 |
| 溢价锁定 | 预订>90% | 关闭促销渠道 | 关闭直销需确认 |
| 房型超售 | 预测NOSHOW>5% | 自动超售3% | 超售>5%需确认 |
| 竞品跟进 | 主要竞品降价>10% | 选择性跟降5% | 跟降>8%需确认 |

---

## 八、实施路线图

### Phase 1: 基础能力 (Month 1-2)
- [ ] 部署动态定价引擎V2.0
- [ ] 集成竞品价格监控
- [ ] 接入PMS实时数据

### Phase 2: 预测能力 (Month 3-4)
- [ ] 上线AI需求预测模型
- [ ] 部署事件影响建模
- [ ] 取消率预测系统

### Phase 3: 优化能力 (Month 5-6)
- [ ] 库存优化自动化
- [ ] 团体Displacement分析
- [ ] 渠道动态分配

### Phase 4: 智能化 (Month 7-9)
- [ ] 全自动决策闭环
- [ ] 餐饮收益管理
- [ ] RGI对标系统

### Phase 5: 成熟运营 (Month 10-12)
- [ ] 全自动化运营
- [ ] 异常检测与预警
- [ ] 持续模型优化

---

## 九、预期效果

### 业务效果

| 指标 | 基准 | 6个月 | 12个月 |
|------|------|-------|--------|
| RevPAR提升 | - | +12% | +20% |
| 定价决策准确率 | - | >85% | >92% |
| 预测准确率(30天) | - | ±7% | ±5% |
| 人工干预率 | 100% | <30% | <10% |
| RGI指数 | 100 | 105 | 112 |

### 运营效率

- 定价决策时间：从小时级→分钟级→秒级
- 预测更新频率：从日级→小时级→实时
- 人工审核比例：从100%→30%→10%

---

**文档版本**: V2.0 深度扩展版  
**创建日期**: 2026-03-06  
**基于**: 中旅SOP + Duetto/IDeaS/Atomize国际最佳实践 + AI/ML算法  
**归属**: AHL场景SKILL化架构V4.0 - B端AI运营官旗舰模块  
**目标**: 让单体酒店拥有国际连锁级别的收益管理能力
