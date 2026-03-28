# 收益管理 SKILL知识库 V1.0

> **版本**: V1.0
> **日期**: 2026-03-26
> **定位**: AHL数字员工——收益管理模块的完整SKILL知识底座
> **知识来源**: STR/CoStar方法论 · IDeaS/SABRE/Duetto技术白皮书 · 学术文献 · 行业最佳实践
> **字数**: ~18,000字

---

## 一、数学公式体系

### 1.1 核心指标公式

#### 1.1.1 三大基础指标

**ADR（平均每日房价）**
```
公式：ADR = 客房总收入 / 已售客房数
     = Σ(各房型单价 × 售出数量) / 总售出间夜数

英文：Average Daily Rate
来源：STR (Smith Travel Research) 标准定义
```

**OCC（入住率）**
```
公式：OCC% = (已售客房数 / 可售客房数) × 100%
     = (Demand / Supply) × 100%

英文：Occupancy Rate
来源：STR标准定义
```

**RevPAR（每间可售房收入）**
```
公式①：RevPAR = ADR × OCC%
         = (客房总收入 / 已售客房数) × (已售客房数 / 可售客房数)
         = 客房总收入 / 可售客房数

公式②：RevPAR = 客房总收入 / 可售客房数
     = Total Room Revenue / Available Rooms

英文：Revenue Per Available Room
来源：STR标准定义

注意：RevPAR是衡量收益管理效率的核心指标，不受房间规模影响
```

**GOPPAR（每间可售房经营毛利）**
```
公式：GOPPAR = GOP / 可售客房数
     = (总收入 - 经营成本) / 可售客房数

英文：Gross Operating Profit Per Available Room
来源：HOTSTAT标准
```

**TRevPAR（每间可售房总营收）**
```
公式：TRevPAR = 总营业收入 / 可售客房数
     = (客房收入 + 餐饮收入 + 其他收入) / 可售客房数

英文：Total Revenue Per Available Room
```

**计算示例**
```
假设：某酒店100间客房，当日售出75间，客房总收入¥82,500

ADR = 82,500 / 75 = ¥1,100
OCC% = (75 / 100) × 100% = 75%
RevPAR = 1,100 × 75% = ¥825
或 RevPAR = 82,500 / 100 = ¥825
```

#### 1.1.2 STR对标指数体系

**ARI（ADR指数）**
```
公式：ARI = (酒店ADR / 竞争群ADR) × 100

含义：
  ARI > 100：定价能力优于竞争群
  ARI = 100：与竞争群持平
  ARI < 100：定价能力落后于竞争群

英文：ADR Index
来源：STR STAR Report标准
```

**MPI（市场渗透指数）**
```
公式：MPI = (酒店OCC% / 市场OCC%) × 100
     = (酒店已售间夜数 / 酒店可售间夜数) / (市场已售间夜数 / 市场可售间夜数) × 100

含义：
  MPI > 100：市场份额高于市场均值
  MPI = 100：市场份额等于市场均值
  MPI < 100：市场份额低于市场均值

英文：Market Penetration Index
来源：STR标准
```

**RGI（收益生成指数）**
```
公式：RGI = (酒店RevPAR / 竞争群RevPAR) × 100
     = ARI × MPI / 100（简化估算）

含义：
  RGI > 100：综合收益能力优于竞争群
  RGI < 100：综合收益能力落后于竞争群

英文：Revenue Generation Index
来源：STR标准

注：RGI是衡量整体收益管理绩效的核心指数
```

**讨价还价指数（BIS - Booking Integrity Score）**
```
公式：BIS = (确认预订数 / 总询盘数) × 100%

来源：IDeaS方法论
用途：衡量定价合理性和市场需求匹配度
```

#### 1.1.3 收入结构指标

**客房收入占比**
```
公式：客房收入占比 = 客房收入 / 总营业收入 × 100%

中国理想值：55-65%（高端酒店）
```

**非房收入占比**
```
公式：非房收入占比 = (餐饮 + 会议 + 其他) / 总收入 × 100%

中国理想值：35-45%（亚朵高达30%+）
```

**渠道产能占比**
```
公式：渠道产能占比 = 某渠道间夜数 / 总间夜数 × 100%

主要渠道：
  OTA（携程/美团/飞猪）：目标≤30%
  协议/企业客户：目标30-40%
  会员/私域：目标30-40%
  团队/旅行社：目标15-20%
  Walk-in：目标10-15%
```

---

### 1.2 价格优化模型

#### 1.2.1 BAR（最优可售房价）模型

**BAR定义**
```
BAR = Best Available Rate
     = 酒店在公开市场上向任何客户提供的最优公开价格

BAR是收益管理的基础价格标杆，所有渠道价格应围绕BAR设定
```

**BAR定价规则表（基于入住天数）**

| 距入住天数 | 调价幅度（相对BAR） | 说明 |
|-----------|-------------------|------|
| 0-3天 | +20%~+40% | 最后一刻溢价 |
| 4-7天 | +10%~+25% | 短期预订溢价 |
| 8-14天 | +5%~+15% | 正常偏高 |
| 15-30天 | 基准价（±5%） | BAR标准 |
| 31-60天 | -5%~-10% | 提前预订优惠 |
| 60天以上 | -10%~-20% | 超早鸟折扣 |

**BAR调整因子**
```
BAR_adjusted = BAR_base × F_demand × F_competitive × F_event × F_LOS

其中：
  BAR_base    = 基础最优可售房价
  F_demand    = 需求系数（基于预订进度）
  F_competitive = 竞争系数（基于竞品价格）
  F_event     = 事件系数（节假日/展会）
  F_LOS       = 入住夜数系数（连住折扣）
```

#### 1.2.2 动态定价公式

**基础动态定价模型**
```
P(t) = P_base × [1 + α·D(t) + β·C(t) + γ·E(t) + δ·T(t) + ε·LOS(t)]

参数定义：
  P(t)      = t时刻最优价格
  P_base    = 基础价格（成本加成或市场基准）
  D(t)      = 需求系数（需求热度感知）
  C(t)      = 竞争系数（竞品价格差异）
  E(t)      = 事件系数（节假日/展会）
  T(t)      = 时间系数（周内波动）
  LOS(t)    = 入住夜数系数（连住优惠）
  
权重参数（需基于历史数据标定）：
  α = 0.30~0.45  （需求权重）
  β = 0.15~0.25  （竞争权重）
  γ = 0.10~0.20  （事件权重）
  δ = 0.05~0.10  （时间权重）
  ε = -0.05~-0.15（连住折扣，取负）

来源：IDeaS G3 RMS方法论 + 学术文献(Kimes, 1989)
```

**需求系数D(t)计算**
```
D(t) = (当前预订数 / 历史同期预订数) × 预订进度系数

预订进度系数（基于可售天数）：
  距入住>30天：系数=0.8（早期波动大）
  距入住15-30天：系数=1.0
  距入住7-14天：系数=1.2（关键决策期）
  距入住<7天：系数=1.5（高确定性）

需求热度分级：
  D < 0.8：低需求，降价或促销
  D = 0.8~1.0：正常需求，维持或小降
  D = 1.0~1.3：高需求，可小幅提价
  D > 1.3：爆满需求，大幅提价
```

**竞争系数C(t)计算**
```
C(t) = (我店价格 - 竞品价格) / 竞品价格 × 权重系数

场景分析：
  C(t) < -10%：我店价格显著高于竞品 → 降价
  C(t) = -5%~-10%：略高于竞品 → 维持或小幅降价
  C(t) = -5%~+5%：价格持平 → 维持
  C(t) > +5%：我店价格低于竞品 → 可小幅提价

竞争群选择（STR标准）：
  产品竞争群：同档次同区域3-5家
  地理竞争群：同区域不同档次2-3家
  综合竞争群：多维度加权3-7家
```

**事件系数E(t)参考值（中国市场）**

| 事件类型 | 事件系数范围 | 说明 |
|---------|------------|------|
| 春节（正月初一至初三） | ×2.0~3.5 | 最高溢价 |
| 国庆（10月1-3日） | ×1.8~2.5 | 次高溢价 |
| 五一/端午（当日） | ×1.3~1.8 | 中等溢价 |
| 清明/中秋（当日） | ×1.2~1.5 | 轻度溢价 |
| 高考（6月6-8日） | ×1.5~2.0 | 考点周边溢价 |
| 中考（地区不同） | ×1.3~1.6 | 考点周边溢价 |
| 国际展会（广交会/进博会） | ×2.0~4.0 | 展会期间 |
| 国内大型展会 | ×1.5~2.5 | 视规模而定 |
| 周末（周六） | ×1.1~1.3 | 休闲市场 |
| 大型体育赛事 | ×1.5~2.5 | 视赛事级别 |

**连住优惠系数LOS(t)**
```
LOS(t) = -discount_rate × (n - 1)  （n为入住夜数）

示例（discount_rate=5%）：
  1晚：LOS = 0%
  2晚：LOS = -5%（总价97.5折）
  3晚：LOS = -10%（总价90折）
  5晚：LOS = -20%（总价80折）

注：长住折扣需平衡边际收益与客房清理成本
```

#### 1.2.3 希尔顿/万豪定价矩阵模型

**需求-竞争二维定价矩阵**

| 预订进度 / 市场热度 | 低需求（D<0.8） | 正常需求（D=0.8~1.2） | 高需求（D>1.2） |
|-------------------|----------------|---------------------|----------------|
| **低价竞品（C<-10%）** | 降价15-20% | 降价5-10% | 维持，观察 |
| **平价竞品（C=±10%）** | 维持或小降5% | BAR基准价 | 提价10-15% |
| **高价竞品（C>+10%）** | 维持 | 提价5-10% | 提价15-25% |

#### 1.2.4 贡献度定价模型

**边际贡献定价法**
```
边际贡献 = 售价 - 边际成本（边际成本≈客房变动成本）

客房变动成本（经济型酒店参考）：
  清洁用品：¥3-5/间
  一次性用品：¥2-4/间
  布草洗涤：¥3-5/间
  水电能耗：¥5-10/间
  合计：¥13-24/间

最低可售价 = 边际成本 × 安全系数（通常≥1.5）

示例：边际成本¥18，最低可售价 = ¥18 × 1.5 = ¥27
当市场出价>¥27时，接受订单是理性的
```

**GOP贡献模型**
```
某渠道GOP贡献 = 渠道收入 × GOP率 - 渠道佣金 - 渠道获取成本

示例（携程渠道）：
  房价：¥500
  佣金率：15%
  GOP率：60%
  
  贡献 = 500 × 60% - 500 × 15% - 其他成本
       = 300 - 75 = ¥225

对比（直销渠道）：
  房价：¥500
  佣金率：0%
  营销成本率：5%（私域运营摊销）
  
  贡献 = 500 × 60% - 500 × 5% - 其他成本
       = 300 - 25 = ¥275

结论：直销贡献比OTA高约22%
```

#### 1.2.5 价格一致性公式

```
价格差异率 = (渠道价格 - BAR价格) / BAR价格 × 100%

价格一致性标准：
  差异率 < 5%：可接受
  差异率 5-10%：需关注
  差异率 > 10%：必须调整

BAR保护原则：
  BAR价格 ≤ 任何渠道公开价格
  会员价/协议价 < BAR价格（体现会员价值）
  OTA价 = BAR价格（确保OTA竞争力）
```

---

### 1.3 库存管理模型

#### 1.3.1 可售库存计算

**实时可售房（Real Available Rooms）**
```
可售数 = 总房间数 - 占用数 - 预离未走数 - 维修房数 - 预留房数

详细分解：
  可售数 = 总房量 - 已入住 - 预抵未入住 - 维修房 - 团队预留 - 长包房

实时更新频率：建议每5分钟同步PMS数据
```

**净可售（Net Sellable）**
```
Net Avail = Gross Avail - 预期No-show - 预期取消 + 预期提前退房

预期No-show数 = 历史No-show率 × 当日预订数
预期取消数 = 历史取消率 × 当日预订数
预期提前退房 = 历史提前退房率 × 当日入住数
```

#### 1.3.2 渠道配额分配模型

**基础配额公式**
```
渠道配额 = 总可售数 × 渠道占比目标

标准配额比例（参考）：
  直销/私域：30-40%（最优价格，保护直销）
  协议/企业：20-30%（维护关系，价格适中）
  OTA平台：20-30%（保持市场覆盖）
  Walk-in：10-20%（保留机动，应对溢价需求）
```

**动态配额调整**
```
Q_channel(t) = Q_base × F_demand(t) × F_history(t) × F_strategic(t)

其中：
  Q_base       = 基础配额（总可售数 × 目标占比）
  F_demand(t)  = 当日需求系数
  F_history(t) = 该渠道历史转化率系数
  F_strategic(t) = 战略目标系数（如提升某渠道占比）

配额警戒线：
  某渠道已售/配额 > 90%：即将满额，预警
  某渠道已售/配额 < 50%：利用率不足，考虑释放
```

**收益最大化配额模型（线性规划）**
```
目标函数：Maximize Σ(R_i × Q_i)

约束条件：
  ΣQ_i ≤ Q_total（总可售房限制）
  Q_i ≥ Q_i_min（各渠道最低配额）
  Q_i ≤ Q_i_max（各渠道最高配额）
  Q_i ∈ Z+（整数约束）

其中：
  R_i = 各渠道单价
  Q_i = 各渠道分配间夜数
  Q_total = 总可售间夜数

来源：IDeaS Inventory Allocation Model
```

#### 1.3.3 超额预订（Overbooking）模型

**超售房间数计算**
```
Overbooking = ceil(D × (NoShow_rate + Cancel_rate - EarlyCheckOut_rate) / (1 - NoShow_rate))

简化版：
Overbooking_nums = ceil(预订数 × (No-show率 + 取消率) × 安全系数)

超售风险控制：
  高风险期（展会/节假日）：超售数 = ceil(预期NoShow)
  正常期：超售数 = ceil(预期NoShow × 0.5)
  低风险期（商务区平日）：不建议超售
```

**超售决策矩阵**

| 取消率 | No-show率 | 总风险 | 超售建议 |
|-------|----------|-------|---------|
| <5% | <2% | <7% | 不超售 |
| 5-10% | 2-3% | 7-13% | 超售1-3间 |
| 10-15% | 3-5% | 13-20% | 超售3-5间 |
| >15% | >5% | >20% | 超售5间以上+升舱 |

**超售补偿成本计算**
```
超售成本 = 安置成本 + 补偿成本 + 声誉成本

安置成本（参考）：
  同区域同级别酒店安置：免费入住 + 交通补贴¥50-100
  高于本酒店安置：差价补偿 + 交通补贴
  
补偿成本（行业惯例）：
  协商解决：¥200-500代金券/积分
  强硬拒绝：¥500-1000 + 司法风险

声誉成本（量化困难但真实存在）：
  差评概率提升
  口碑传播负面影响
  企业客户流失风险
```

#### 1.3.4 升舱决策模型

**升舱阈值计算**
```
升舱临界点 = 升舱成本 / 边际收益贡献

升舱成本：
  房型差价：¥50-300/间夜
  边际服务成本：¥10-30/间夜（早餐/迷你吧等）

边际收益贡献：
  口碑提升价值（难以量化）
  未来复购概率提升
  好评率提升

经验法则：
  当预计入住率 < 85%：不考虑升舱
  当预计入住率 85-95%：选择性升舱（高价值客户优先）
  当预计入住率 > 95%：可升舱以优化房间分配
```

#### 1.3.5 入住率预测模型

**基于预订进度的入住率预测**
```
预测OCC(t) = 当前预订数 / 总可售数 × (1 + 潜在Walk-in系数)

潜在Walk-in系数（基于历史数据）：
  商务区平日：×1.05-1.10
  周末/度假区：×1.10-1.20
  展会/节假日：×1.00-1.05（预测性更强）

预订进度参考：
  距入住30天，预订量<40%：低进度，降价
  距入住14天，预订量<60%：偏低，需关注
  距入住7天，预订量<75%：正常
  距入住3天，预订量>85%：良好
  距入住1天，预订量>95%：爆满
```

---

### 1.4 收益管理公式汇总表

#### 核心指标汇总

| 指标名称 | 英文 | 计算公式 | 单位 |
|---------|------|---------|------|
| 平均房价 | ADR | 客房收入/已售间夜 | ¥ |
| 入住率 | OCC | 已售间夜/可售间夜×100% | % |
| 每房收益 | RevPAR | 客房收入/可售间夜 或 ADR×OCC | ¥ |
| 经营毛利 | GOP | 总收入-经营成本 | ¥ |
| 每房毛利 | GOPPAR | GOP/可售间夜 | ¥ |
| 总收入 | TRevPAR | 总收入/可售间夜 | ¥ |
| ADR指数 | ARI | 酒店ADR/竞争群ADR×100 | 指数 |
| 市场渗透指数 | MPI | 酒店OCC%/市场OCC%×100 | 指数 |
| 收益生成指数 | RGI | 酒店RevPAR/竞争群RevPAR×100 | 指数 |

#### 定价系数汇总

| 系数 | 符号 | 取值范围 | 说明 |
|------|------|---------|------|
| 需求系数 | D(t) | 0.5-2.0 | 市场需求热度 |
| 竞争系数 | C(t) | -0.3~+0.3 | 相对竞品价格 |
| 事件系数 | E(t) | 0.8-3.5 | 节假日/展会影响 |
| 时间系数 | T(t) | 0.9-1.2 | 周内/日内波动 |
| 连住系数 | LOS(t) | -0.3~0 | n晚住的折扣 |
| 动态价格 | P(t) | 变量 | 实时最优价格 |

---

## 二、预测模型体系

### 2.1 时序预测模型

#### 2.1.1 移动平均法（Moving Average）

**简单移动平均（SMA）**
```
公式：SMA_n = (X_{t-1} + X_{t-2} + ... + X_{t-n}) / n

参数：n = 移动窗口大小
  小窗口（n=3-7）：对短期波动敏感
  大窗口（n=14-30）：更平滑，但滞后明显

适用场景：需求稳定、无明显趋势/季节性的基础预测
  适用酒店类型：长住型公寓、会议型酒店

优点：简单直观，计算量小
缺点：滞后性严重，无法捕捉趋势和季节性
来源：经典统计方法
```

**加权移动平均（WMA）**
```
公式：WMA_n = Σ(w_i × X_{t-i}) / Σ(w_i)，i=0到n-1

常用权重方案：
  线性递减：w_i = n - i（如n=7，权重=7,6,5,4,3,2,1）
  指数加权：(0.9, 0.09, 0.009...)类似EWMA

适用场景：对近期数据赋予更高权重
```

#### 2.1.2 指数平滑法（Exponential Smoothing）

**简单指数平滑（SES）**
```
公式：S_t = α × X_{t-1} + (1-α) × S_{t-1}

参数：α = 平滑系数，取值0~1
  α值越大：对近期数据越敏感（α>0.5：快响应）
  α值越小：预测越平滑（α<0.3：慢响应）

初始值：S_1 = X_1 或 S_1 = 平均值

预测：F_{t+1} = S_t

适用场景：需求相对稳定的短期预测（7-14天）
优点：计算量小，能快速响应新数据
缺点：无法处理趋势和季节性
来源：Brown (1956)，引用于Kimes (1989)酒店收益管理文献

参数标定建议：
  α = 0.1~0.3（稳定市场）
  α = 0.3~0.5（波动市场）
```

**Holt线性趋势指数平滑（Holt's Linear）**
```
公式：
  Level(t) = α × Y_t + (1-α) × (Level(t-1) + Trend(t-1))
  Trend(t) = β × (Level(t) - Level(t-1)) + (1-β) × Trend(t-1)
  F_{t+k} = Level(t) + k × Trend(t)

参数：
  α = 水平平滑系数（0<α<1）
  β = 趋势平滑系数（0<β<1）
  k = 预测期数

适用场景：有线性趋势但无季节性的数据
  适用：开业3年以上、无明显季节性的商务酒店

来源：Holt (1957), Winters (1960)
```

**Holt-Winters季节指数平滑**
```
公式（加法季节）：
  Level(t) = α × (Y_t - S_{t-s}) + (1-α) × (Level(t-1) + Trend(t-1))
  Trend(t) = β × (Level(t) - Level(t-1)) + (1-β) × Trend(t-1)
  Season(t) = γ × (Y_t - Level(t)) + (1-γ) × S_{t-s}
  F_{t+k} = Level(t) + k × Trend(t) + S_{t-s+k}

公式（乘法季节）：
  Level(t) = α × (Y_t / S_{t-s}) + (1-α) × (Level(t-1) + Trend(t-1))
  Trend(t) = β × (Level(t) - Level(t-1)) + (1-β) × Trend(t-1)
  Season(t) = γ × (Y_t / Level(t)) + (1-γ) × S_{t-s}
  F_{t+k} = (Level(t) + k × Trend(t)) × S_{t-s+k}

参数：
  α = 水平平滑系数
  β = 趋势平滑系数
  γ = 季节平滑系数
  s = 季节周期长度（周数据s=7，月数据s=12）

适用场景：具有明显季节性的酒店需求预测
  适用：度假酒店、景区酒店、婚宴型酒店

乘法 vs 加法选择：
  季节波动幅度不随水平变化 → 加法模型
  季节波动幅度随水平成比例变化 → 乘法模型（更常用）

来源：Winters (1960)，引用于酒店RMS学术文献
```

**ETS（Error-Trend-Seasonality）模型**
```
 statsmodels.tsa.holtwinters.ExponentialSmoothing 的自动版本

模型选择准则（AIC/BIC）：
  加法趋势：Y_t = Level + Trend + Season + Error
  乘法趋势：Y_t = Level × Trend × Season × Error
  阻尼趋势：增加阻尼参数φ防止趋势无限延伸

ETS自动选择流程：
  1. 拟合所有候选模型（5×2×2=20种组合）
  2. 计算各模型AICc值
  3. 选择AICc最低的模型

Python实现：
  from statsmodels.tsa.holtwinters import ExponentialSmoothing
  model = ExponentialSmoothing(y, seasonal_periods=7,
                               trend='add', seasonal='mul').fit()

适用场景：全自动模型选择，减少人工干预
来源：Hyndman & Athanasopoulos (2018)《Forecasting: Principles and Practice》
```

#### 2.1.3 ARIMA / SARIMA模型

**ARIMA(p,d,q)模型**
```
ARIMA = AutoRegressive Integrated Moving Average

公式：
  φ(B)(1-B)^d Y_t = θ(B)ε_t

展开形式（AR(p)部分）：
  Y_t = c + φ_1 Y_{t-1} + φ_2 Y_{t-2} + ... + φ_p Y_{t-p}
        + ε_t + θ_1 ε_{t-1} + ... + θ_q ε_{t-q}

参数：
  p = 自回归项数（AR阶数）
  d = 差分阶数（使序列平稳）
  q = 移动平均项数（MA阶数）

定阶方法：
  AIC/BIC准则：min(AIC) = -2 log(L) + 2k
  ACF/PACF图：识别p和q
  自动搜索：pmdarima.auto_arIMA()

平稳性检验：ADF检验（Augmented Dickey-Fuller）
  ADF统计量 < 临界值 → 拒绝原假设（存在单位根）→ 差分后重做

来源：Box, Jenkins & Reinsel (1970)《Time Series Analysis》
```

**SARIMA(p,d,q)(P,D,Q,s)模型**
```
SARIMA = Seasonal ARIMA（加入季节性的ARIMA）

公式：
  φ(B)Φ(B^s)(1-B)^d(1-B^s)^D Y_t = θ(B)Θ(B^s)ε_t

参数（双重阶数）：
  (p,d,q) = 非季节性ARIMA参数
  (P,D,Q,s) = 季节性参数
  s = 季节周期长度
    日数据：s=7（周季节性）
    周数据：s=52（年季节性）
    月数据：s=12（年季节性）

酒店需求预测常用配置：
  SARIMA(1,1,1)(1,1,1,7) —— 周季节性日预测
  SARIMA(2,1,1)(0,1,1,12) —— 年季节性月预测

适用场景：
  商务酒店：SARIMA(1,0,1)(0,1,1,5) —— 工作日/周末周期
  度假酒店：SARIMA(1,1,1)(1,1,1,52) —— 周季节+年季节叠加

来源：Box et al. (1970)，酒店应用参见Weatherford & Kimes (2003)
```

**ARIMA/SARIMA计算示例**
```python
import pmdarima as pm
from statsmodels.tsa.statespace.sarimax import SARIMAX

# 自动定阶（推荐）
model = pm.auto_arima(
    y,                      # 时间序列数据
    seasonal=True,          # 是否考虑季节性
    m=7,                    # 季节周期（7=周季节）
    stepwise=True,          # 逐步搜索（加速）
    suppress_warnings=True
)
print(model.summary())
forecast = model.predict(n_periods=14)  # 预测未来14天

# 手动指定阶数
model = SARIMAX(
    y, order=(1,1,1),
    seasonal_order=(1,1,1,7)
).fit()
forecast = model.forecast(steps=14)
```

#### 2.1.4 Facebook Prophet模型

**Prophet模型结构**
```
公式：Y(t) = g(t) + s(t) + h(t) + ε_t

组件分解：
  g(t) = 趋势函数（growth function）
       = 分段线性 or 逻辑斯蒂增长
       
  s(t) = 季节性函数（seasonality）
       =傅里叶级数叠加（默认：年季节+周季节）
       
  h(t) = 节假日函数（holidays）
       = 各国家法定节假日 + 自定义事件

趋势点：
  changepoint_prior_scale = 0.05（趋势变化灵活度）
  n_changepoints = 25（趋势断点数量）

季节性傅里叶阶数：
  yearly_seasonality：默认10阶（高精度需20-25阶）
  weekly_seasonality：默认3阶

来源：Facebook (2017), Taylor & Letham
GitHub: facebook/prophet
```

**Prophet优缺点分析**

| 优点 | 缺点 |
|------|------|
| 全自动季节性建模 | 对短期趋势预测不如ARIMA |
| 内置节假日效应（中国节假日需自定义） | 需要至少1年历史数据 |
| 对缺失值和异常值鲁棒 | 乘法季节性在大趋势反转时表现差 |
| 组件可解释性强 | 实时更新能力弱 |
| 调参直观 | 计算量较大，预测慢 |

**Prophet适用场景**
```
适用：
  ✓ 节假日效应显著的酒店（婚宴/春节/国庆）
  ✓ 中期预测（14-90天）
  ✓ 有突发事件/展会需要建模
  ✓ 数据有明显的年季节性

不适用：
  ✗ 少于1年历史数据
  ✗ 分钟级/小时级实时预测
  ✗ 开业不足1年的新酒店（无季节基准）
```

**Prophet代码示例**
```python
from prophet import Prophet
import pandas as pd

# 数据准备：ds列为日期，y列为目标值
df = pd.DataFrame({
    'ds': date_range,
    'y': occupancy_rate
})

# 添加中国节假日
holidays = pd.DataFrame({
    'holiday': ['chinese_new_year', 'national_day'],
    'ds': pd.to_datetime(['2026-01-29', '2026-10-01']),
    'lower_window': [-2, -1],
    'upper_window': [2, 3]
})

model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
    holidays=holidays,
    changepoint_prior_scale=0.1  # 提高灵活性
)
model.fit(df)

future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

# 分解查看：趋势+季节性+节假日效应
model.plot_components(forecast)
```

#### 2.1.5 LSTM深度学习模型

**LSTM架构**
```
LSTM = Long Short-Term Memory Network

网络结构（典型配置）：
  Input: [batch_size, time_steps, features]
  LSTM层1: 64-128个隐藏单元 + Dropout(0.2)
  LSTM层2: 32-64个隐藏单元 + Dropout(0.2)
  Dense层: 16-32个神经元
  Output: 预测值（OCC%/ADR/RevPAR）

关键门控机制：
  遗忘门：f_t = σ(W_f · [h_{t-1}, x_t] + b_f)
  输入门：i_t = σ(W_i · [h_{t-1}, x_t] + b_i)
  输出门：o_t = σ(W_o · [h_{t-1}, x_t] + b_o)

来源：Hochreiter & Schmidhuber (1997)
```

**LSTM特征工程**
```
输入特征（X）设计：
  时序特征：
    - 过去7/14/30天的OCC、ADR、RevPAR
    - 滚动平均/滚动最大/滚动最小
    - 同比/环比变化率
    
  外部特征：
    - 天气数据（温度/降雨/空气质量）
    - 节假日标识（是否节假日+距节假日天数）
    - 展会/大型活动（是/否+规模评级）
    - 竞品价格（ADR/RevPAR）
    
  语义特征：
    - 星期几（one-hot，7维）
    - 月份（one-hot，12维）
    - 酒店位置（ embedding 或 one-hot）
    - 房型（embedding）

输出特征（y）：
  单步预测：次日OCC%
  多步预测：未来7天/14天/30天的日OCC%
```

**LSTM代码示例**
```python
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

model = Sequential([
    LSTM(64, activation='relu',
         input_shape=(time_steps, n_features),
         return_sequences=True),
    Dropout(0.2),
    LSTM(32, activation='relu'),
    Dropout(0.2),
    Dense(16, activation='relu'),
    Dense(1)  # 输出：预测OCC%
])

model.compile(optimizer='adam', loss='mse', metrics=['mae'])

# 训练
model.fit(X_train, y_train,
          epochs=100,
          batch_size=32,
          validation_split=0.1,
          callbacks=[tf.keras.callbacks.EarlyStopping(patience=10)])

# 预测
predictions = model.predict(X_test)
```

**LSTM vs 传统模型对比**

| 维度 | ARIMA/SARIMA | Prophet | LSTM |
|------|-------------|---------|------|
| 数据量需求 | 100-500个点 | >365个点 | >1000个点 |
| 季节性 | 需手动指定 | 自动建模 | 需作为特征输入 |
| 训练时间 | 秒级 | 秒-分钟级 | 分钟-小时级 |
| 预测精度（日） | MAPE 8-15% | MAPE 8-18% | MAPE 5-12% |
| 可解释性 | 中等 | 高 | 低 |
| 实时更新 | 支持在线学习 | 需重新训练 | 困难 |
| 外部特征 | 需手动扩展ARIMAX | 支持 | 原生支持 |

---

### 2.2 回归模型

#### 2.2.1 多元线性回归（MLR）

**模型公式**
```
Y = β_0 + β_1 X_1 + β_2 X_2 + ... + β_k X_k + ε

酒店收益预测应用：
RevPAR = β_0 + β_1 × OCC_{lag7} + β_2 × ADR_{lag7}
       + β_3 × 竞品ADR + β_4 × 房价折扣率
       + β_5 × 展会虚拟变量 + β_6 × 周末虚拟变量 + ε

参数估计：最小二乘法（OLS）
  β = (X^T X)^{-1} X^T y

来源：经典统计方法，酒店应用参见Jones & Joy (2002)
```

**模型评估指标**
```
R²（决定系数）：
  R² = 1 - Σ(y_i - ŷ_i)² / Σ(y_i - ȳ)²
  R² > 0.7：模型解释力良好
  R² < 0.5：模型解释力不足

调整R²（考虑变量数）：
  R²_adj = 1 - (1-R²) × (n-1)/(n-k-1)

AIC/BIC（模型选择）：
  AIC = n × ln(RSS/n) + 2k
  BIC = n × ln(RSS/n) + k × ln(n)
  选择AIC/BIC最小的模型

F检验（整体显著性）：
  F = (RSS_reduced - RSS_full) / (df_reduced - df_full)
      / (RSS_full / df_full)
  F > F_critical → 拒绝原假设（模型有效）
```

**适用场景**
```
适用：
  ✓ 解释性优先的分析（如：哪些因素驱动RevPAR）
  ✓ 特征重要性分析（渠道/房型/时间贡献度）
  ✓ 基线预测（快速建立基准模型）
  ✓ 线性关系明显的数据

不适用：
  ✗ 非线性关系（如：需求饱和效应）
  ✗ 特征高度共线性
  ✗ 时序依赖（需用ARIMAX或加时序误差项）
```

#### 2.2.2 泊松回归（Poisson Regression）

**模型公式**
```
log(E[Y]) = β_0 + β_1 X_1 + ... + β_k X_k

或等价形式：
E[Y | X] = exp(β_0 + β_1 X_1 + ... + β_k X_k)

特点：
  - Y为计数数据（非负整数）
  - 方差 = 均值（等离散假设）
  - 对数链接函数保证输出非负

酒店应用：预测日间夜数（Count of Room Nights Sold）
  E[间夜数] = exp(β_0 + β_竞争ADR + β_展会 + β_天气 + ...)

来源：Cameron & Trivedi (1998)《Regression Analysis of Count Data》
```

**过分散处理（Overdispersion）**
```
泊松分布假设 E[Y] = Var[Y]，实际数据往往 Var[Y] > E[Y]

准泊松模型（Quasi-Poisson）：
  在泊松模型基础上引入分散参数 φ
  Var[Y] = φ × E[Y]
  φ由数据估计（φ > 1 表示过分散）

负二项回归（更常用）：
  Var[Y] = E[Y] + α × E[Y]²
  α 为额外分散参数
```

#### 2.2.3 负二项回归（Negative Binomial）

**模型公式**
```
log(E[Y]) = Xβ
Var[Y] = E[Y] + α × E[Y]²

相比泊松的优势：
  - 允许方差 > 均值（更灵活）
  - 估计参数更稳健

酒店应用场景：
  - 预测日间夜数（考虑过度分散）
  - 预测事件发生次数（取消数/No-show数）

来源：Cameron & Trivedi (1998)
```

#### 2.2.4 回归模型计算示例
```python
import statsmodels.api as sm
from statsmodels.discrete.discrete_model import NegativeBinomial

# 多元线性回归
X = sm.add_constant(df[['OCC_lag7', 'ADR_lag7', 'comp_ADR', 'is_weekend']])
y = df['RevPAR']
model = sm.OLS(y, X).fit()
print(model.summary())

# 泊松回归（预测间夜数）
X = sm.add_constant(df[['comp_ADR', 'event_flag', 'temperature']])
y = df['room_nights']
model = sm.GLM(y, X, family=sm.families.Poisson()).fit()

# 负二项回归
model = NegativeBinomial(y, X).fit()
```

---

### 2.3 机器学习模型

#### 2.3.1 逻辑回归（Logistic Regression）

**模型公式**
```
P(Y=1) = 1 / (1 + exp(-(β_0 + β_1 X_1 + ... + β_k X_k)))

或等价形式：
logit(P) = ln(P/(1-P)) = β_0 + β_1 X_1 + ... + β_k X_k

酒店应用场景：
  - 预订是否取消：P(取消=1)
  - 会员是否流失：P(流失=1)
  - 是否高价值客户：P(高价值=1)
  - 某渠道是否有转化：P(转化=1)

来源：Hosmer, Lemeshow & Sturdivant (2013)《Applied Logistic Regression》
```

**模型评估指标**
```
混淆矩阵：
                    预测0    预测1
  实际0（负类）      TN       FP
  实际1（正类）      FN       TP

准确率（Accuracy）：
  ACC = (TP + TN) / (TP + TN + FP + FN)

精确率（Precision）：
  PRE = TP / (TP + FP)

召回率（Recall/Sensitivity）：
  REC = TP / (TP + FN)

F1分数：
  F1 = 2 × PRE × REC / (PRE + REC)

AUC-ROC（AUC > 0.7 表示模型有区分能力）：
  AUC = ROC曲线下面积
  AUC = 0.5（随机）→ AUC = 1.0（完美）
```

#### 2.3.2 决策树（Decision Tree）

**ID3 / C4.5 / CART算法**

| 算法 | 分裂准则 | 输出 |
|------|---------|------|
| ID3 | 信息增益（Information Gain） | 分类 |
| C4.5 | 信息增益率（Gain Ratio） | 分类 |
| CART | 基尼不纯度（Gini Impurity）或MSE | 分类+回归 |

**CART回归树公式**
```
MSE_split = Σ(y_i - ȳ_left)² + Σ(y_i - ȳ_right)²

选择使 MSE_split 最小的特征和分裂点

树结构参数：
  max_depth：最大深度（防止过拟合）
  min_samples_split：分裂所需最小样本数
  min_samples_leaf：叶节点最小样本数
  max_features：每次分裂考虑的最大特征数

来源：Breiman et al. (1984)《Classification and Regression Trees》
```

**决策树可视化示例（收益管理场景）**
```
决策树解释（预订取消预测）：
  根节点：提前天数 > 7天？
  ├─ 是：入住天数 > 3晚？
  │     ├─ 是：取消概率 = 5%（低风险）
  │     └─ 否：距入住 > 3天？
  │           ├─ 是：取消概率 = 15%
  │           └─ 否：取消概率 = 35%
  └─ 否（≤7天）：渠道 = OTA？
                ├─ 是：取消概率 = 8%
                └─ 否：取消概率 = 3%
```

#### 2.3.3 随机森林（Random Forest）

**模型原理**
```
随机森林 = Bootstrap + 决策树 + 集成学习

训练流程（每棵树）：
  1. 有放回抽样（Bootstrap）：从N个样本抽取N个
  2. 随机特征选择：每次分裂随机选m个特征（m = √k）
  3. 训练决策树（不剪枝）

预测流程：
  分类：投票法（少数服从多数）
  回归：平均法（所有树预测值平均）

来源：Breiman (2001) "Random Forests", Machine Learning

关键参数：
  n_estimators：树的数量（100-500，常用200）
  max_features：特征采样比例（回归常用1/3）
  max_depth：每棵树最大深度
  min_samples_leaf：叶节点最小样本
```

**随机森林 vs 单棵决策树**

| 维度 | 决策树 | 随机森林 |
|------|--------|---------|
| 过拟合风险 | 高 | 低（通过集成降低） |
| 预测稳定性 | 低 | 高 |
| 特征重要性 | 有 | 有（可计算） |
| 计算成本 | 低 | 中-高 |
| 可解释性 | 高 | 中（可通过特征重要性解释） |

#### 2.3.4 XGBoost / LightGBM

**XGBoost算法**
```
目标函数：L(φ) = Σl(y_i, ŷ_i) + ΣΩ(f_k)

其中：
  l = 损失函数（ mse 或 logloss）
  Ω(f_k) = 正则项，控制树的复杂度
         = γT + ½λ Σw_j²
         T = 叶节点数，w = 叶节点权重

梯度提升（每轮迭代）：
  1. 计算残差（负梯度）：g_i = ∂l(y_i, ŷ_i) / ∂ŷ_i
  2. 用残差训练新树
  3. 更新预测值：ŷ_i^(t) = ŷ_i^(t-1) + η × f_t(x_i)
     η = 学习率（常用0.01-0.3）

来源：Chen & Guestrin (2016) "XGBoost: A Scalable Tree Boosting System"

核心优势：
  ✓ 正则化防止过拟合
  ✓ 并行计算高效
  ✓ 自动处理缺失值
  ✓ 特征重要性评估
```

**LightGBM算法**
```
LightGBM = Light Gradient Boosting Machine

核心创新：
  1. GOSS（Gradient-based One-Side Sampling）
     - 保留大梯度样本，对小梯度随机抽样
     - 减少计算量同时保持精度
  
  2. EFB（Exclusive Feature Bundling）
     - 将互斥特征合并，减少特征维度
     - 稀疏特征优化

对比XGBoost的优势：
  ✓ 训练速度更快（2-10倍）
  ✓ 内存消耗更低
  ✓ 大规模数据处理能力强
  ✓ 支持类别特征（原生）

来源：Microsoft LightGBM团队 (2017)
GitHub: microsoft/LightGBM
```

**XGBoost / LightGBM参数对照**

| 参数 | XGBoost | LightGBM | 推荐值 |
|------|---------|---------|--------|
| 树数量 | n_estimators | num_leaves/n_estimators | 100-500 |
| 最大深度 | max_depth | max_depth | 5-8 |
| 学习率 | eta/learning_rate | learning_rate | 0.01-0.1 |
| 叶节点数 | min_child_weight | min_data_in_leaf | 10-50 |
| 正则α | alpha | lambda_l1 | 0-1 |
| 正则λ | lambda | lambda_l2 | 0-1 |
| 采样率 | subsample | bagging_fraction | 0.7-0.9 |
| 特征采样 | colsample_bytree | feature_fraction | 0.7-0.9 |

**XGBoost代码示例**
```python
import xgboost as xgb

model = xgb.XGBRegressor(
    n_estimators=300,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    min_child_weight=10,
    reg_alpha=0.1,
    reg_lambda=1.0,
    objective='reg:squarederror',  # 回归
    # objective='binary:logistic'  # 分类
)

model.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    early_stopping_rounds=30,
    verbose=False
)

# 特征重要性
importance = model.feature_importances_
```

**集成模型对比**

| 维度 | 随机森林 | XGBoost | LightGBM |
|------|---------|---------|---------|
| 训练速度 | 中 | 慢 | 快 |
| 预测精度 | 中-高 | 高 | 高 |
| 内存占用 | 高 | 中 | 低 |
| 调参难度 | 低 | 中 | 中 |
| 大数据支持 | 中 | 好 | 极好 |
| 过拟合风险 | 低 | 中 | 中-高 |
| 特征类型 | 数值+类别 | 数值+类别 | 数值+类别+文本 |

---

### 2.4 预测模型选型指南

#### 模型选择决策树

```
第一步：数据量和历史深度
├── 历史数据 < 1年（<365个点）
│   └── 推荐：简单移动平均、指数平滑（SES）
│
├── 历史数据 1-3年
│   └── 第二步：季节性是否存在？
│       ├── 无明显季节性 → ARIMA、SVR、随机森林
│       └── 有明显季节性 → SARIMA、Prophet、Boosting+季节特征
│
└── 历史数据 > 3年
    └── 第三步：精度要求
        ├── 高精度（MAPE<10%）→ LSTM、XGBoost/LightGBM
        ├── 中精度（MAPE 10-15%）→ Prophet、SARIMA
        └── 可解释优先 → 回归模型、决策树
```

#### 不同预测期适用模型

| 预测期 | 推荐模型 | 预期MAPE | 备注 |
|-------|---------|---------|------|
| 1-3天 | ARIMA(1,0,1)、LSTM | 5-8% | 临近日期精度最高 |
| 4-7天 | SARIMA(1,1,1)(1,1,1,7)、Prophet | 7-10% | 加入周季节性 |
| 8-14天 | Prophet、XGBoost | 8-12% | 可加入外部特征 |
| 15-30天 | Prophet+外部特征、XGBoost | 10-15% | 节假日效应需建模 |
| 31-90天 | SARIMA+外部变量、Prophet | 12-18% | 中期精度下降 |
| 91-365天 | 多元回归+季节因子、季节分解 | 15-25% | 年度规划用 |

#### 集成预测策略

**多模型融合（Model Ensemble）**
```
单一模型风险：某模型在特定场景下失效

融合策略：
  1. 简单平均：F_ensemble = (F_1 + F_2 + F_3) / 3
  2. 加权平均：F_ensemble = w_1×F_1 + w_2×F_2 + w_3×F_3
     权重根据验证集表现确定
  3. stacking：训练次级模型（元学习器）组合预测

实践建议：
  - 时序模型（ARIMA/Prophet）+ ML模型（XGBoost）+ 专家规则
  - 权重动态调整：某模型近期表现好则提高权重

来源：酒店RMS实践中IDeaS/Duetto采用类似策略
```

---

## 三、分析方法体系

### 3.1 细分市场分析

#### 3.1.1 细分维度体系

**四大细分维度**
```
1. 客户维度（WHO）
   ├── 客户类型：散客/团队/会议/长住/协议
   ├── 会员等级：黑卡/金卡/银卡/普通
   ├── 客户价值：RFM分层（L高价值/M中价值/R低价值）
   └── 来源渠道：OTA/官网/企微/电话/上门

2. 时间维度（WHEN）
   ├── 预订时间：超早鸟（>60天）/早鸟（30-60天）/标准（14-30天）/短期（<14天）/临时（<3天）
   ├── 入住时间：工作日/周末/节假日
   └── 入住时长：1晚/2-3晚/4-7晚/7晚以上

3. 渠道维度（WHERE）
   ├── OTA：携程/美团/飞猪/去哪儿
   ├── 直销：官网/APP/小程序/电话
   ├── 私域：企业微信/社群/会员
   └── 线下：Walk-in/协议/团队

4. 产品维度（WHAT）
   ├── 房型：标准间/大床/套房/豪华套房
   ├── 餐食：含早/不含早/半餐/全餐
   └── 附加：含升舱/含下午茶/含接送
```

#### 3.1.2 贡献度分析

**Pareto分析（ABC分类）**
```
Pareto法则：80%的收益来自20%的客户/渠道/房型

分析步骤：
  1. 计算各细分的收入贡献
  2. 按贡献降序排列
  3. 计算累计贡献百分比
  4. 识别拐点（贡献达到80%的细分）

贡献度分级：
  A类（关键少数）：累计贡献>80%，重点维护
  B类（重要多数）：累计贡献15-80%，稳定发展
  C类（一般多数）：累计贡献<15%，优化或淘汰

应用示例（渠道贡献度）：
  携程：贡献45% → A类 → 重点投入
  会员：贡献25% → A类 → 重点维护
  协议：贡献18% → B类 → 稳定维护
  美团：贡献7% → C类 → 评估ROI
  Walk-in：贡献5% → C类 → 低优先
```

**贡献度计算公式**
```
某细分贡献率 = 某细分收入 / 总收入 × 100%

边际贡献 = 某细分收入 - 该细分变动成本
边际贡献率 = 边际贡献 / 收入 × 100%

示例（协议客户渠道）：
  协议房价：¥400
  变动成本：¥50（清洁+耗材）
  边际贡献：¥350
  边际贡献率：87.5%

对比（OTA渠道）：
  OTA房价（含佣金）：¥450
  佣金率：15% → 佣金¥67.5
  变动成本：¥50
  边际贡献：450 - 67.5 - 50 = ¥332.5
  边际贡献率：73.9%

结论：协议客户边际贡献率更高（87.5% > 73.9%）
```

#### 3.1.3 价格弹性分析

**需求价格弹性**
```
ε = ΔQ/Q / ΔP/P = (ΔQ/ΔP) × (P/Q)

含义：
  |ε| > 1：需求富有弹性（价格变动→需求大变）
  |ε| = 1：单位弹性
  |ε| < 1：需求缺乏弹性（价格变动→需求小变）

酒店行业经验值：
  散客：ε = -0.8 ~ -1.5（适度弹性）
  团队：ε = -1.5 ~ -3.0（高弹性，议价能力强）
  会议：ε = -0.5 ~ -1.0（低弹性，时间敏感）
  会员：ε = -0.3 ~ -0.8（低弹性，品牌忠诚）

来源：酒店收益管理学术文献+STR数据
```

**弹性动态计算**
```
短期弹性（<14天预订窗口）：
  ε_short = -1.2 ~ -1.8（临时需求，价格敏感）

中期弹性（14-60天预订窗口）：
  ε_mid = -0.8 ~ -1.3（计划需求）

长期弹性（>60天预订窗口）：
  ε_long = -0.5 ~ -0.9（早鸟客户，忠诚度高）

定价策略应用：
  高弹性（|ε|>1）：降价可增加收入（薄利多销）
  低弹性（|ε|<1）：提价可增加收入（刚需为主）
  弹性=1：价格变动不影响收入（最优定价点）

公式推导（最优价格）：
  收入最大化条件：d(Revenue)/dP = 0
  Revenue = P × Q(P)
  dR/dP = Q + P × dQ/dP = Q(1 + 1/ε) = 0
  最优条件：ε = -1（单位弹性点）
```

**交叉弹性（竞争对手影响）**
```
交叉弹性：ε_AB = ΔQ_A/Q_A / ΔP_B/P_B

含义：
  ε_AB > 0：替代品（A和B同区域竞品）
  ε_AB = 0：无关品
  ε_AB < 0：互补品

酒店应用：
  竞品降价10% → 我店需求下降5%
  交叉弹性 = (-5%)/(-10%) = 0.5

竞争响应矩阵：
  竞品降价<5%：我店维持原价（短期不影响）
  竞品降价5-15%：我店小降2-5%或提升服务
  竞品降价>15%：深度价格战，评估成本底线
```

#### 3.1.4 渠道收益分析

**渠道ROI矩阵**
```
渠道ROI = 渠道净贡献 / 渠道总成本 × 100%

渠道成本构成：
  OTA：佣金（10-15%）+ 平台推广费
  会员：CRM运营成本 + 权益成本 + 触达成本
  协议：销售成本 + 维护成本 + 差旅费
  团队：销售成本 + 运营调整成本

渠道贡献计算模板：
┌────────┬────────┬────────┬────────┬────────┐
│ 渠道   │ 收入   │ 成本   │ 贡献   │ ROI    │
├────────┼────────┼────────┼────────┼────────┤
│ 携程   │ ¥500k  │ ¥75k  │ ¥425k  │ 567%   │
│ 美团   │ ¥200k  │ ¥16k  │ ¥184k  │ 1150%  │
│ 会员   │ ¥300k  │ ¥30k  │ ¥270k  │ 900%   │
│ 协议   │ ¥150k  │ ¥20k  │ ¥130k  │ 650%   │
└────────┴────────┴────────┴────────┴────────┘

结论：美团ROI最高（佣金率8%），携程次之（佣金率15%）
```

---

### 3.2 竞品分析

#### 3.2.1 竞品价格监控方法论

**竞争群组定义（Comp Set）**
```
STR竞争群4P原则：
  1. Product（产品）：同档次（星级/品牌）
  2. Position（位置）：同区域（3公里内或同商圈）
  3. Price（价格）：ADR差异<30%
  4. People（客群）：目标客群相似

竞争群规模：通常3-7家（太少缺乏代表性，太多失去焦点）

竞争群分类：
  核心竞品（直接竞争）：同档次同区域TOP3
  卫星竞品（同区替代）：同区域不同档次
  潜在竞品（未来威胁）：新建酒店/即将开业
```

**竞品数据采集方法**
```
渠道1：OTA平台（实时）
  - 携程/美团/飞猪爬取
  - 房型价格+库存状态
  - 促销标签+活动信息
  - 频率：每小时（旺季）或每4小时（淡季）

渠道2：酒店官网（战略信息）
  - BAR价格
  - 会员价格
  - 套餐产品
  - 频率：每日1次

渠道3：电话调研（补充）
  - 询问当日房价
  - 询问团队价格
  - 询问特殊需求价格
  - 频率：每周1次

来源：STR数据采集方法论
```

**竞品指数计算**
```
竞品价格指数（CPI = Competitive Price Index）
  CPI = (我店价格 / 竞品平均价) × 100

解读：
  CPI > 100：我店价格高于竞品
  CPI = 100：我店价格等于竞品
  CPI < 100：我店价格低于竞品

竞价优势指数（PRI = Price Rate Index）
  基于STR ARI方法
  PRI = 我店加权平均价 / 竞争群加权平均价 × 100
```

#### 3.2.2 市场份额计算

**市场份额指标**
```
绝对市场份额 = 酒店间夜数 / 市场总间夜数 × 100%

相对市场份额（RGI对照）：
  相对份额 = 酒店间夜数 / 竞争群平均间夜数 × 100

来源：STR标准
```

#### 3.2.3 STR数据Benchmark

**STR STAR Report解读**
```
STAR Report内容：
  1. 酒店基本信息：房间数、开业时间、翻新时间
  2. 市场数据：Supply、Demand、Rate
  3. STR指数：ARI、MPI、RGI
  4. 竞争群数据：TOP3竞品的同期对比
  5. 趋势数据：周/月/年趋势

STR数据购买渠道：
  - STR (str.com)：全球酒店数据
  - CoStar：商业地产数据
  - 国内：众数科技、中瑞酒店研究院
```

**STR数据分析维度**

| 分析维度 | 指标 | 诊断 |
|---------|------|------|
| 定价 | ARI vs 100 | ARI>100定价能力优于市场 |
| 客源 | MPI vs 100 | MPI>100市场份额领先 |
| 收益 | RGI vs 100 | RGI>100综合收益能力强 |
| 趋势 | vs 同期 | 同比增长/下降分析 |
| 效率 | RevPAR分解 | ADR贡献 vs OCC贡献 |

---

### 3.3 预算与预测

#### 3.3.1 预算编制方法

**增量预算法**
```
新年度预算 = 上年度实际 × (1 + 增长率假设)

增长率来源：
  - 市场趋势（STR预测）
  - 竞争环境变化
  - 酒店改造/升级计划
  - 整体经济环境

优点：简单易行，保持连续性
缺点：可能固化低效，忽视结构性变化
适用：稳定运营的成熟酒店
```

**零基预算法（ZBB）**
```
零基预算：从零开始论证每个预算项的必要性

步骤：
  1. 确定预算包（每个部门/项目）
  2. 设定产出目标和资源需求
  3. 优先级排序
  4. 资源分配

优点：优化资源配置，识别低效
缺点：工作量大，主观性强
适用：资源紧张需优化配置时
```

**收益导向预算法**
```
基于目标收益倒推预算

目标RevPAR → 推算目标ADR和OCC
           → 推算各细分市场目标
           → 推算各渠道目标
           → 推算营销预算需求

示例：
  目标RevPAR = ¥500（+10%）
  预计OCC = 70%
  目标ADR = ¥500 / 70% = ¥714
  
  按细分拆解：
    散客ADR：¥800，OCC：25% → 贡献¥200
    团队ADR：¥450，OCC：30% → 贡献¥135
    协议ADR：¥550，OCC：15% → 贡献¥82.5
    ...
```

#### 3.3.2 滚动预测

**滚动预测定义**
```
滚动预测 = 持续更新的中短期预测

传统预算：年度目标，季度分解
滚动预测：每月底更新未来12-18个月预测

滚动频率：每月或每季
预测期长：12-18个月
```

**滚动预测流程**
```
1. 每月末收集最新数据
2. 更新模型输入（实际+最新预测）
3. 重新运行预测模型
4. 对比原预测 vs 修订预测
5. 分析偏差原因
6. 输出修订版预测报告
7. 管理层评审
```

#### 3.3.3 偏差分析

**预测偏差指标**
```
绝对百分比误差（APE）：
  APE = |实际值 - 预测值| / 实际值 × 100%

平均绝对百分比误差（MAPE）：
  MAPE = Σ|实际值 - 预测值| / 实际值 × 100% / n

均方根误差（RMSE）：
  RMSE = √(Σ(实际值 - 预测值)² / n)

平均绝对偏差（MAD）：
  MAD = Σ|实际值 - 预测值| / n

偏差率：
  偏差率 = (预测值 - 实际值) / 实际值 × 100%
  正值：预测偏高（低估了市场）
  负值：预测偏低（高估了市场）
```

**MAPE评价标准**
```
MAPE < 5%：预测精度优秀
MAPE = 5-10%：预测精度良好
MAPE = 10-15%：预测精度一般
MAPE = 15-20%：预测精度较差
MAPE > 20%：预测模型需改进

AHL目标：
  7天预测 MAPE < 8%
  14天预测 MAPE < 12%
  30天预测 MAPE < 15%
```

**偏差原因归因分析**
```
偏差来源分解：
  预测偏差 = 趋势偏差 + 季节偏差 + 事件偏差 + 随机误差

趋势偏差：长期趋势判断错误
季节偏差：季节性强度估计错误
事件偏差：展会/节假日影响估计错误
随机误差：不可预测的随机波动

改进方向：
  趋势偏差 → 引入更多宏观经济变量
  季节偏差 → 延长历史数据，重新标定季节因子
  事件偏差 → 建立事件库，量化事件影响系数
```

---

### 3.4 效果评估

#### 3.4.1 收益提升归因分析

**收益变化分解**
```
ΔRevPAR = ΔADR × OCC_new + ADR_old × ΔOCC + ΔADR × ΔOCC

分解为：
  ADR贡献 = (ADR_new - ADR_old) × OCC_new
  OCC贡献 = ADR_old × (OCC_new - OCC_old)
  交叉贡献 = (ADR_new - ADR_old) × (OCC_new - OCC_old)

示例：
  上月：ADR=¥500，OCC=60%，RevPAR=¥300
  本月：ADR=¥520，OCC=65%，RevPAR=¥338
  
  ADR贡献 = (520-500)×65% = ¥13
  OCC贡献 = 500×(65%-60%) = ¥25
  交叉贡献 = (520-500)×(65%-60%) = ¥1
  
  总提升 = ¥13 + ¥25 + ¥1 = ¥39
```

**定价策略效果评估**
```
对照组：未使用动态定价的历史同期
实验组：使用动态定价的当期

提升计算：
  RevPAR提升 = RevPAR_实验组 - RevPAR_对照组
  
控制变量：
  - 同期OCC相近（避免需求差异干扰）
  - 同一市场环境
  - 相同房型结构

统计显著性检验：
  t-test: 检验提升是否显著不为零
  p-value < 0.05：提升具有统计显著性
```

#### 3.4.2 渠道效果评估

**渠道效率指标**
```
渠道产能 = 渠道订单数 / 总订单数 × 100%
渠道转化率 = 渠道成交数 / 渠道访客数 × 100%
渠道CPO = 渠道总成本 / 渠道订单数
渠道ROI = 渠道贡献 / 渠道成本
```

#### 3.4.3 活动效果评估

**促销ROI计算**
```
促销ROI = (活动期间增量收入 - 活动成本) / 活动成本 × 100%

增量收入计算：
  增量收入 = (活动期间实际收入) - (同期基准收入)

活动成本：
  - 佣金减免成本
  - 广告投放成本
  - 赠品/权益成本
  - 运营调整成本

示例（早鸟活动）：
  活动成本：¥5,000（广告投放）
  活动前7天收入：¥80,000（基准）
  活动7天收入：¥105,000（实际）
  
  增量收入 = ¥105,000 - ¥80,000 = ¥25,000
  ROI = (25000 - 5000) / 5000 × 100% = 400%
```

---

## 四、行业最佳实践

### 4.1 主流软件对比

#### 4.1.1 国际主流RMS系统

**IDeaS G3 RMS（行业领导者）**
```
公司：IDeaS Revenue Solutions（SAS子公司）
市场份额：约35%
成立时间：1992年

核心技术：
  - Demand360°：竞争情报数据
  - G3 RMS：核心预测+定价引擎
  - Analytics：高级分析

算法特点：
  - SAS统计引擎+机器学习
  - Demand Fusion（需求融合预测）
  - Attribute Pricing（属性定价）
  - LOS Optimizer（住一付二优化）

集成能力：
  - 107+ PMS/CRS集成
  - Opera、Infor、Sabre等

优点：
  ✓ 行业最成熟，算法权威
  ✓ 全球最大酒店数据池
  ✓ 咨询支持完善
  
缺点：
  ✗ 价格昂贵（年费$10,000-$50,000+）
  ✗ 实施周期长（3-6个月）
  ✗ 对中小酒店不经济

适用规模：100+房间的中大型酒店
参考价格：年收入0.5-2%或固定年费
来源：IDeaS官网 + Gartner评估
```

**SABRE Synxis RMS**
```
公司：Sabre Corporation
市场份额：约20%（GDS延伸）
成立时间：1960年

核心技术：
  - Synxis RMS：原Infor HMS/EasyRMS团队
  - GDS集成：全球最大GDS网络
  - AirRM：航空收益管理（跨行业借鉴）

算法特点：
  - 预测+优化双引擎
  - 多属性定价
  - 团体优化模块

集成能力：
  - Sabre GDS（全球覆盖）
  - Opera PMS
  - Synxis Booking Engine

优点：
  ✓ GDS深度集成，适合全球分销
  ✓ 团体收益管理强
  ✓ 大型连锁经验丰富
  
缺点：
  ✗ 界面相对传统
  ✗ 实施复杂
  ✗ 价格较高

适用规模：200+房间的大型酒店/酒店集团
参考价格：年收入0.5-1.5%
来源：Sabre官网
```

**Duetto（云原生RMS）**
```
公司：Duetto
市场份额：约15%
成立时间：2012年

核心技术：
  - GameChanger：云端RMS
  - BlockBuster：团队优化
  - ScoreBoard：数据分析

算法特点：
  - 开源架构+大数据技术
  - 实时计算能力
  - API优先设计

集成能力：
  - 150+ 云端集成
  - 基于API，无需本地部署

优点：
  ✓ 云原生，部署快
  ✓ 开放API，灵活性高
  ✓ 实时数据分析强
  
缺点：
  ✗ 数据科学家需要自配
  ✗ 部分功能需额外开发
  ✗ 中国市场支持弱

适用规模：50-500房间的中型酒店
参考价格：年收入0.3-1%（竞争性定价）
来源：Duetto官网 + 行业评测
```

**Rainmaker（Lemerond）**
```
公司：Rainmaker
市场份额：约10%
成立时间：1997年

核心技术：
  - Revenue IQ：预测引擎
  - Revcaster：预算+预测
  - Business Forecast：业务预测

算法特点：
  - 奢侈酒店专长
  - 博彩/度假村优化
  - 婚宴/会议特殊模块

优点：
  ✓ 高端度假酒店算法领先
  ✓ 团体/会议优化强
  ✓ 实施相对简单
  
缺点：
  ✗ 中端市场功能一般
  ✗ 非云端为主
  ✗ 全球覆盖有限

适用规模：精品酒店、度假村、博彩酒店
参考价格：年收入0.4-1%
来源：Rainmaker官网
```

**Infor HMS（酒店管理云）**
```
公司：Infor
市场份额：约8%
成立时间：2002年（收购整合）

核心技术：
  - CloudSuite Hospitality：云端ERP
  - Revenue Management：RMS模块
  - Tongji AI：AI助手

算法特点：
  - 云原生+AI
  - 灵活性高
  - 中端市场定位

优点：
  ✓ 云端一体化（PMS+RMS）
  ✓ 成本相对可控
  ✓ 实施周期适中
  
缺点：
  ✗ 算法不如IDeaS权威
  ✗ 集团管理功能有限
  ✗ 高端市场竞争力弱

适用规模：50-200房间的中型酒店
参考价格：年收入0.3-0.8%
来源：Infor官网
```

**OTA Insight（数据分析平台）**
```
公司：OTA Insight
市场份额：数据分析赛道领先
成立时间：2012年

核心功能：
  - Rate 360：竞品价格监控
  - Parity Monitor：价格一致性
  - Revenue Analytics：收益分析
  - Demand360：需求洞察

算法特点：
  - BI工具导向
  - 可视化分析强
  - 实时监控

优点：
  ✓ 竞品数据覆盖广
  ✓ 价格一致性检查强
  ✓ 性价比高
  
缺点：
  ✗ 不是完整RMS（无自动定价）
  ✗ 需配合人工决策
  ✗ 预测功能弱

适用规模：全规模酒店（作为辅助工具）
参考价格：房间数×$2-5/月
来源：OTA Insight官网
```

#### 4.1.2 中国本土系统

**携程RMS（浩华/丽火）**
```
平台：携程
核心功能：
  - 商旅管理
  - 收益顾问服务
  - 数据报告

特点：
  ✓ OTA数据整合优势
  ✓ 中国市场特色（展会/节假日）
  ✓ 低成本/免费服务
  
缺点：
  ✗ 算法相对简单
  ✗ 自动定价能力弱
  ✗ 依赖携程生态
```

**华住自研RMS**
```
平台：华住集团
核心功能：
  - 全链路数字化
  - 实时定价
  - 会员定向优惠

特点：
  ✓ 内部闭环，数据完整
  ✓ 1亿+会员行为数据
  ✓ 极低成本
  
缺点：
  ✗ 仅供华住内部使用
  ✗ 不对外输出
```

#### 4.1.3 主流系统综合对比

| 系统 | 算法权威性 | 云化程度 | 集成能力 | 价格 | 中国市场 | 推荐场景 |
|------|----------|---------|---------|------|---------|---------|
| IDeaS | ⭐⭐⭐⭐⭐ | 中 | ⭐⭐⭐⭐⭐ | 昂贵 | ⭐⭐⭐ | 国际品牌/大型酒店 |
| SABRE | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 较高 | ⭐⭐ | 全球分销/连锁集团 |
| Duetto | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 中等 | ⭐⭐ | 中型酒店/灵活性优先 |
| Rainmaker | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | 中等 | ⭐⭐ | 度假/奢侈/会议 |
| Infor | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 中等 | ⭐⭐⭐ | 中型/一体化需求 |
| OTA Insight | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | 较低 | ⭐⭐⭐ | 全规模/竞品监控 |
| 携程RMS | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 免费 | ⭐⭐⭐⭐⭐ | 中国市场/OTA依赖型 |

---

### 4.2 STR方法论

#### 4.2.1 STR报告解读

**STR STAR Report标准报告内容**
```
报告周期：Daily / Weekly / Monthly / Year-to-Date

数据维度：
  Supply（供给）：
    - 可售房夜数（Available Room Nights）
    - 已售房夜数（Occupied Room Nights）
    - 入住率（OCC%）
    
  Demand（需求）：
    - 已售间夜数
    - 团体间夜占比
    
  Rate（价格）：
    - ADR（平均房价）
    - RevPAR（每房收益）
    
  Index（指数）：
    - ARI（ADR指数）
    - MPI（市场渗透指数）
    - RGI（收益生成指数）

来源：STR (str.com) 标准方法论
```

**STR数据质量标准**
```
数据完整性要求：
  - 最低数据提交：70%的可售房夜需有数据
  - 异常值检测：超出均值3个标准差标记为异常
  - 滞后数据：允许30天内补报

数据校验：
  - 房间数匹配（与STR数据库一致）
  - 房价合理性（ADR > $0 且 < $10,000）
  - 入住率合理性（0% < OCC < 105%，含超售）
```

#### 4.2.2 酒店档次划分标准

**STR Global Patch标准（中国参考）**
```
Luxury（奢华）：
  ADR（中国）：¥1,500+
  特征：地标位置、顶级服务、文化IP

Upper Upscale（高端）：
  ADR（中国）：¥800-1,500
  特征：国际品牌、标准SOP、高端会议

Upscale（中高端）：
  ADR（中国）：¥400-800
  特征：设计感、生活方式、年轻客群

Upper Midscale（中端）：
  ADR（中国）：¥250-400
  特征：标准化、效率、性价比

Midscale（经济中端）：
  ADR（中国）：¥150-250
  特征：干净安全、快速复制

Economy（经济型）：
  ADR（中国）：¥100-150
  特征：极简配置、位置优先

注：STR中国区与中国本地档次定义有差异，需本地化校准
```

#### 4.2.3 基准对标方法

**Benchmark流程**
```
1. 确定竞争群（3-7家）
2. 获取STR数据授权
3. 定期接收STAR Report
4. 分析指数变化
5. 制定改进策略

对标频率：
  日监控：异常波动预警
  周分析：短期策略调整
  月评估：运营复盘
  年规划：战略目标制定
```

---

### 4.3 实施指南

#### 4.3.1 收益管理成熟度评估

**CMM成熟度等级**
```
Level 1（初始级）：
  - 依赖经验定价
  - 无数据记录
  - 无系统支持
  目标：建立基础数据收集

Level 2（基础级）：
  - 有PMS系统
  - 有手工报表
  - 有基础对标
  目标：引入Excel分析工具

Level 3（规范级）：
  - 有RMS系统
  - 有标准流程
  - 有定期复盘
  目标：提高预测精度

Level 4（优化级）：
  - AI辅助决策
  - 实时定价
  - 自动化执行
  目标：追求最优收益

Level 5（卓越级）：
  - 全自动化决策
  - 预测准确率>90%
  - 持续自我优化
  目标：行业领先
```

#### 4.3.2 收益管理实施路径

**Phase 1：基础建设（1-2月）**
```
任务清单：
  □ PMS数据清洗和标准化
  □ 历史数据归档（至少2年）
  □ 竞争群确定
  □ 基础报表体系建立
  □ 核心KPI监控仪表盘

技术要求：
  - 数据准确率 > 95%
  - 每日数据更新
  - 自动化报表生成
```

**Phase 2：预测建模（2-4月）**
```
任务清单：
  □ 时序预测模型部署（Prophet或ARIMA）
  □ 基础动态定价规则设置
  □ 节假日/事件库建立
  □ 预测准确率监控

目标：
  - 7天预测 MAPE < 12%
  - 14天预测 MAPE < 15%
```

**Phase 3：优化决策（4-6月）**
```
任务清单：
  □ ML模型集成（XGBoost/LSTM）
  □ 动态定价引擎上线
  □ 渠道配额自动化
  □ 超售策略优化

目标：
  - RevPAR提升 10-15%
  - 人工决策时间减少 50%
```

**Phase 4：智能决策（6-12月）**
```
任务清单：
  □ 多模型集成预测
  □ 全自动定价决策
  □ 实时竞品响应
  □ 持续学习优化

目标：
  - RevPAR提升 15-25%
  - 人工干预 < 10%
```

#### 4.3.3 组织保障

**收益管理团队配置参考**

| 酒店规模 | 收益管理岗 | 报告对象 | 系统支持 |
|---------|-----------|---------|---------|
| <100间 | 前厅兼职 | 总经理 | Excel+基础报表 |
| 100-300间 | 专职收益经理1人 | 总经理/运营总监 | 中端RMS |
| 300-500间 | 收益经理+助理各1人 | 运营总监 | 高端RMS |
| >500间 | 收益总监+经理2-3人 | 副总经理 | 全套RMS |

---

## 五、SKILL接口定义

### 5.1 SKILL-OTA-001 动态定价计算

**基本信息**
```
SKILL-ID：SKILL-OTA-001
名称：动态定价计算（Dynamic Pricing Engine）
版本：1.0
分类：OTA及收益管理 / 动态定价AGENT
优先级：P0
```

**输入规格（Input Schema）**
```yaml
input:
  type: object
  required:
    - hotel_id
    - room_type
    - checkin_date
    - current_inventory
  
  properties:
    hotel_id:
      type: string
      description: 酒店唯一标识（PMS系统ID）
      example: "HTL_001"
    
    room_type:
      type: string
      description: 房型代码
      example: "STD"  # 标准间
    
    checkin_date:
      type: string (date)
      format: date
      description: 入住日期
      example: "2026-04-15"
    
    current_inventory:
      type: integer
      description: 当前可售房数量
      example: 45
    
    days_to_checkin:
      type: integer
      description: 距入住天数
      example: 7
    
    base_price:
      type: number
      description: 基准价格（元）
      example: 500
    
    historical_adr:
      type: number
      description: 历史同期ADR
      example: 480
    
    competitor_prices:
      type: object
      description: 竞品价格列表
      properties:
        comp_1: { type: number, example: 520 }
        comp_2: { type: number, example: 490 }
        comp_3: { type: number, example: 510 }
    
    demand_factor:
      type: number
      description: 需求系数（0.5-2.0）
      example: 1.2
    
    event_multiplier:
      type: number
      description: 事件系数（节假日/展会）
      example: 1.0
    
    los:
      type: integer
      description: 入住夜数
      example: 2
    
    day_of_week:
      type: integer
      description: 星期几（0=周一，6=周日）
      example: 2
```

**输出规格（Output Schema）**
```yaml
output:
  type: object
  
  properties:
    skill_id:
      type: string
      example: "SKILL-OTA-001"
    
    status:
      type: string
      enum: [success, error, fallback]
      example: "success"
    
    recommendation:
      type: object
      
      properties:
        suggested_price:
          type: number
          description: 建议价格（元）
          example: 545
        
        price_range:
          type: object
          properties:
            min: { type: number, example: 520 }
            max: { type: number, example: 580 }
        
        confidence:
          type: number
          description: 建议置信度（0-1）
          example: 0.85
        
        factors:
          type: object
          description: 各因素贡献度分解
          properties:
            base: { type: number, description: "基准贡献", example: 500 }
            demand: { type: number, description: "需求贡献", example: 25 }
            competitive: { type: number, description: "竞争贡献", example: -10 }
            event: { type: number, description: "事件贡献", example: 0 }
            los: { type: number, description: "连住折扣", example: -20 }
            weekday: { type: number, description: "工作日调整", example: 50 }
    
    strategy:
      type: string
      description: 定价策略建议
      enum: [aggressive_up, moderate_up, hold, moderate_down, aggressive_down]
      example: "moderate_up"
    
    urgency:
      type: string
      description: 调整紧迫度
      enum: [immediate, within_hour, within_day]
      example: "within_hour"
    
    alternative_actions:
      type: array
      description: 备选策略
      items:
        type: object
        properties:
          action: { type: string }
          expected_impact: { type: string }
    
    metadata:
      type: object
      properties:
        model_version: { type: string }
        computed_at: { type: string (datetime) }
        cache_ttl: { type: integer, description: "缓存有效期(秒)" }
```

**核心算法逻辑**
```
动态定价计算流程：

1. 基础价格确认
   P_base = input.base_price 或根据历史ADR确定

2. 需求系数计算
   D = compute_demand_factor(days_to_checkin, current_inventory)
   规则：
     - 距入住<7天，库存>70% → D=1.2（高价清库存）
     - 距入住<7天，库存<40% → D=0.9（降价促销）
     - 距入住>14天，库存>60% → D=1.1（正常偏高）

3. 竞争系数计算
   C = compute_competitive_factor(comparator_prices, P_base)
   规则：
     - 我店价格高于竞品均值>10% → C = -0.1（降价信号）
     - 我店价格低于竞品均值>10% → C = +0.1（可小幅提价）

4. 事件系数确认
   E = input.event_multiplier（从事件日历查询）

5. 连住折扣
   LOS = compute_los_discount(los)
   规则：每多一晚减少2-5%（边际递减）

6. 综合价格计算
   P = P_base × (1 + D + C + E) + LOS_adjustment

7. 价格合理性校验
   - P >= P_base × 0.6（不低于成本底线）
   - P <= P_base × 3.0（不超过市场天花板）
   - P <= 竞品最高价 × 1.2（不高于最高竞品20%以上）

8. 策略分类
   - (P - P_base) / P_base > 0.15 → "aggressive_up"
   - (P - P_base) / P_base > 0.05 → "moderate_up"
   - -0.05 <= (P - P_base) / P_base <= 0.05 → "hold"
   - -0.15 <= (P - P_base) / P_base < -0.05 → "moderate_down"
   - (P - P_base) / P_base < -0.15 → "aggressive_down"
```

**Python实现示例**
```python
def skill_ota_001_dynamic_pricing(input_data: dict) -> dict:
    """
    SKILL-OTA-001 动态定价计算
    """
    # 1. 参数提取
    base_price = input_data['base_price']
    demand_factor = input_data['demand_factor']
    competitor_prices = input_data.get('competitor_prices', {})
    event_multiplier = input_data.get('event_multiplier', 1.0)
    los = input_data.get('los', 1)
    
    # 2. 竞争系数
    if competitor_prices:
        comp_avg = sum(competitor_prices.values()) / len(competitor_prices)
        comp_diff = (base_price - comp_avg) / comp_avg
        competitive_factor = -0.05 if comp_diff > 0.1 else (0.05 if comp_diff < -0.1 else 0)
    else:
        competitive_factor = 0
    
    # 3. 连住折扣
    los_discount = -base_price * 0.03 * (los - 1) if los > 1 else 0
    
    # 4. 综合价格
    suggested_price = (
        base_price 
        * (1 + demand_factor - 1)  # 需求相对基准的调整
        * (1 + competitive_factor)
        * event_multiplier
        + los_discount
    )
    
    # 5. 合理性校验
    min_price = base_price * 0.6
    max_price = base_price * 3.0
    suggested_price = max(min_price, min(suggested_price, max_price))
    
    # 6. 策略分类
    price_change = (suggested_price - base_price) / base_price
    if price_change > 0.15:
        strategy = "aggressive_up"
    elif price_change > 0.05:
        strategy = "moderate_up"
    elif price_change < -0.15:
        strategy = "aggressive_down"
    elif price_change < -0.05:
        strategy = "moderate_down"
    else:
        strategy = "hold"
    
    return {
        "skill_id": "SKILL-OTA-001",
        "status": "success",
        "recommendation": {
            "suggested_price": round(suggested_price, 0),
            "price_range": {
                "min": round(suggested_price * 0.95, 0),
                "max": round(suggested_price * 1.1, 0)
            },
            "confidence": 0.85,
            "strategy": strategy
        }
    }
```

**依赖项**
```
SKILL-DATA-003  竞品数据爬取（获取竞品价格）
SKILL-DATA-004  外部数据接入（获取事件日历）
SKILL-DATA-006  特征工程（构建demand_factor）
```

---

### 5.2 SKILL-OTA-002 需求预测

**基本信息**
```
SKILL-ID：SKILL-OTA-002
名称：需求预测（Demand Forecasting）
版本：1.0
分类：OTA及收益管理 / 需求预测AGENT
优先级：P0
```

**输入规格（Input Schema）**
```yaml
input:
  type: object
  required:
    - hotel_id
    - forecast_horizon
    - history_data
  
  properties:
    hotel_id:
      type: string
      description: 酒店唯一标识
      example: "HTL_001"
    
    forecast_horizon:
      type: integer
      description: 预测天数（1-365）
      example: 14
    
    history_data:
      type: array
      description: 历史数据（最少365天，推荐730天+）
      items:
        type: object
        properties:
          date: { type: string (date) }
          occupancy: { type: number (0-1) }
          adr: { type: number }
          revpar: { type: number }
          total_rooms: { type: integer }
          available_rooms: { type: integer }
    
    external_features:
      type: object
      description: 外部特征（可选）
      properties:
        holidays: { type: array, items: { type: string (date) } }
        events: { type: array, description: "展会/大型活动" }
        weather_avg: { type: array, description: "历史天气" }
        competitor_adr: { type: array }
```

**输出规格（Output Schema）**
```yaml
output:
  type: object
  
  properties:
    skill_id:
      type: string
      example: "SKILL-OTA-002"
    
    status:
      type: string
      enum: [success, insufficient_data, error]
    
    forecast:
      type: array
      description: 预测结果（按日期排列）
      items:
        type: object
        properties:
          date: { type: string (date) }
          
          occupancy:
            type: object
            properties:
              predicted: { type: number (0-1), example: 0.78 }
              lower_ci: { type: number, example: 0.70 }
              upper_ci: { type: number, example: 0.86 }
          
          adr:
            type: object
            properties:
              predicted: { type: number, example: 520 }
              lower_ci: { type: number }
              upper_ci: { type: number }
          
          revpar:
            type: object
            properties:
              predicted: { type: number, example: 406 }
              lower_ci: { type: number }
              upper_ci: { type: number }
          
          confidence: { type: number, example: 0.82 }
          
          is_peak: { type: boolean, description: "是否峰值日" }
    
    model_info:
      type: object
      properties:
        model_type: { type: string, example: "LightGBM+Prophet_Ensemble" }
        mape_train: { type: number, description: "训练集MAPE" }
        mape_validation: { type: number, description: "验证集MAPE" }
        features_used: { type: array }
    
    summary:
      type: object
      properties:
        avg_occupancy: { type: number }
        avg_adr: { type: number }
        total_revpar: { type: number }
        peak_dates: { type: array }
```

**预测模型选型建议**
```
数据量 < 30天：简单移动平均（naive baseline）
数据量 30-180天：Holt-Winters季节指数平滑
数据量 180-365天：Prophet（可建模季节性）
数据量 365-730天：SARIMA 或 Prophet
数据量 > 730天 + 外部特征：LightGBM/XGBoost
数据量 > 1000天 + 高精度要求：LSTM 或 模型集成

推荐AHL默认方案：
  短期（1-7天）：LightGBM（高实时性）
  中期（8-30天）：Prophet（季节性建模好）
  集成方案：0.4×LightGBM + 0.4×Prophet + 0.2×SARIMA
```

---

### 5.3 SKILL-OTA-003 渠道配额管理

**基本信息**
```
SKILL-ID：SKILL-OTA-003
名称：渠道配额管理（Channel Inventory Allocation）
版本：1.0
分类：OTA及收益管理 / 库存优化AGENT
优先级：P1
```

**输入规格**
```yaml
input:
  type: object
  required:
    - hotel_id
    - checkin_date
    - total_available
    - channel_performance
  
  properties:
    hotel_id: { type: string }
    checkin_date: { type: string (date) }
    total_available: { type: integer, description: "总可售房数" }
    
    channel_performance:
      type: object
      description: 各渠道历史表现
      properties:
        ota_ctrip:
          type: object
          properties:
            avg_adr: { type: number }
            avg_occ: { type: number }
            conversion_rate: { type: number }
            commission: { type: number }
        ota_meituan:
          type: object
        direct:
          type: object
        corporate:
          type: object
    
    strategic_priority:
      type: object
      description: 战略优先方向（可选）
      properties:
        push_direct: { type: boolean, description: "是否优先推直销" }
        max_ota_ratio: { type: number, description: "OTA最高占比", example: 0.30 }
```

**输出规格**
```yaml
output:
  type: object
  
  properties:
    skill_id: "SKILL-OTA-003"
    status: "success"
    
    allocation:
      type: object
      description: 渠道配额分配
      properties:
        ota_ctrip: { type: integer, example: 15 }
        ota_meituan: { type: integer, example: 8 }
        direct: { type: integer, example: 20 }
        corporate: { type: integer, example: 10 }
        walkin_reserve: { type: integer, example: 5 }
    
    utilization_alert:
      type: array
      description: 配额预警
      items:
        type: object
        properties:
          channel: { type: string }
          status: { type: string, enum: [warning, critical] }
          message: { type: string }
    
    rebalance_suggestions:
      type: array
      description: 配额调整建议
```

---

### 5.4 SKILL-OTA-004 超售计算

**基本信息**
```
SKILL-ID：SKILL-OTA-003
名称：超售风险计算（Overbooking Risk Calculator）
版本：1.0
分类：OTA及收益管理 / 库存优化AGENT
优先级：P1
```

**输入规格**
```yaml
input:
  type: object
  required:
    - hotel_id
    - checkin_date
    - total_bookings
    - historical_noshow_rate
    - historical_cancel_rate
  
  properties:
    hotel_id: { type: string }
    checkin_date: { type: string (date) }
    total_bookings: { type: integer, description: "当前总预订数" }
    total_rooms: { type: integer, description: "总房间数" }
    historical_noshow_rate: { type: number, description: "历史No-show率", example: 0.03 }
    historical_cancel_rate: { type: number, description: "历史取消率", example: 0.08 }
    early_checkout_rate: { type: number, description: "提前退房率", example: 0.02 }
    is_peak_period: { type: boolean, description: "是否高峰期" }
    noshow_confirmation_rate: { type: number, description: "预订确认率（高=低风险）", example: 0.85 }
```

**输出规格**
```yaml
output:
  type: object
  
  properties:
    skill_id: "SKILL-OTA-004"
    status: "success"
    
    overbooking_analysis:
      type: object
      properties:
        expected_arrivals: { type: integer, description: "预期到店人数" }
        expected_noshows: { type: integer, description: "预期No-show数" }
        expected_cancels: { type: integer, description: "预期取消数" }
        expected_early_checkout: { type: integer, description: "预期提前退房" }
        
        risk_level:
          type: string
          enum: [low, medium, high, very_high]
        
        recommended_overbooking:
          type: integer
          description: "建议超售房间数"
        
        max_tolerable_overbooking:
          type: integer
          description: "最大可容忍超售数"
    
    actions:
      type: array
      items:
        type: object
        properties:
          action: { type: string, description: "建议动作" }
          priority: { type: string, enum: [immediate, today, monitoring] }
          expected_cost: { type: number, description: "预估成本（元）" }
    
    alternative_hotels:
      type: array
      description: "安置酒店推荐（当超售发生）"
      items:
        type: object
        properties:
          name: { type: string }
          distance: { type: number, description: "距离(公里)" }
          same_level: { type: boolean }
          contact: { type: string }
```

**超售计算公式**
```
net_risk = total_bookings × (noshow_rate + cancel_rate - early_checkout_rate)

recommended_overbooking = ceil(net_risk × safety_factor)

safety_factor参数：
  正常期：safety_factor = 0.8
  高峰期：safety_factor = 1.0
  极高风险期：safety_factor = 1.2

示例：
  total_bookings = 100
  noshow_rate = 3%, cancel_rate = 8%, early_checkout_rate = 2%
  net_risk = 100 × (0.03 + 0.08 - 0.02) = 9
  
  正常期建议超售：ceil(9 × 0.8) = 7间
  高峰期建议超售：ceil(9 × 1.0) = 9间
  
  但max_tolerable = total_rooms × 5% = 5间
  故最终建议：min(7, 5) = 5间
```

---

### 5.5 SKILL-OTA-005 竞品价格抓取

**基本信息**
```
SKILL-ID：SKILL-OTA-005
名称：竞品价格抓取（Competitor Price Scraping）
版本：1.0
分类：OTA及收益管理 / 竞品监控AGENT
优先级：P0
```

**输入规格**
```yaml
input:
  type: object
  required:
    - competitors
  
  properties:
    competitors:
      type: array
      items:
        type: object
        properties:
          hotel_id: { type: string }
          name: { type: string }
          sources:
            type: array
            items:
              type: object
              properties:
                platform: { type: string, enum: [ctrip, meituan, fliggy, hotel_website] }
                url: { type: string }
                room_types: { type: array, items: { type: string } }
    
    checkin_date: { type: string (date) }
    checkout_date: { type: string (date) }
```

**输出规格**
```yaml
output:
  type: object
  
  properties:
    skill_id: "SKILL-OTA-005"
    status: "success"
    
    scrape_metadata:
      type: object
      properties:
        scraped_at: { type: string (datetime) }
        total_hotels: { type: integer }
        successful_scrapes: { type: integer }
        failed_scrapes: { type: array }
        elapsed_seconds: { type: number }
    
    price_data:
      type: array
      items:
        type: object
        properties:
          hotel_id: { type: string }
          source: { type: string }
          room_type: { type: string }
          price: { type: number }
          currency: { type: string, default: "CNY" }
          availability: { type: string, enum: [available, limited, sold_out] }
          breakfast_included: { type: boolean }
          cancellation_policy: { type: string }
    
    aggregated:
      type: object
      description: "聚合数据（用于直接定价参考）"
      properties:
        min_price: { type: number }
        max_price: { type: number }
        avg_price: { type: number }
        competitor_count: { type: integer }
```

---

### 5.6 SKILL-OTA-006 竞品分析报告

**基本信息**
```
SKILL-ID：SKILL-OTA-006
名称：竞品分析报告（Competitor Analysis Report）
版本：1.0
分类：OTA及收益管理 / 竞品监控AGENT
优先级：P1
```

**输出规格**
```yaml
output:
  type: object
  
  properties:
    skill_id: "SKILL-OTA-006"
    
    report_type:
      type: string
      enum: [daily, weekly, monthly, event_based]
    
    period:
      type: object
      properties:
        start_date: { type: string (date) }
        end_date: { type: string (date) }
    
    summary:
      type: object
      properties:
        total_competitors: { type: integer }
        avg_adr_competitors: { type: number }
        our_adr: { type: number }
        ari: { type: number }
        price_position: { type: string, enum: [above, at, below_market] }
        dominant_competitor: { type: string }
    
    price_trend:
      type: array
      items:
        type: object
        properties:
          date: { type: string (date) }
          our_adr: { type: number }
          comp_avg: { type: number }
    
    strategic_insights:
      type: array
      items:
        type: object
        properties:
          insight: { type: string }
          evidence: { type: string }
          recommendation: { type: string }
          priority: { type: string, enum: [high, medium, low] }
    
    appendices:
      type: object
      properties:
        raw_data_table: { type: string, description: "CSV数据链接" }
        visualization_links: { type: array }
```

---

### 5.7 SKILL-OTA-007 OTA排名诊断与优化

**基本信息**
```
SKILL-ID：SKILL-OTA-007
名称：OTA排名诊断（OTA Ranking Diagnosis）
版本：1.0
分类：OTA及收益管理 / OTA运营AGENT
优先级：P1
```

**输入规格**
```yaml
input:
  type: object
  required:
    - hotel_id
    - platform
  
  properties:
    hotel_id: { type: string }
    platform: { type: string, enum: [ctrip, meituan, fliggy] }
    current_ranking: { type: integer, description: "当前排名" }
    target_ranking: { type: integer, description: "目标排名" }
    history_data:
      type: array
      items:
        type: object
        properties:
          date: { type: string (date) }
          ranking: { type: integer }
          conversion_rate: { type: number }
         曝光量: { type: integer }
          浏览量: { type: integer }
```

**输出规格**
```yaml
output:
  type: object
  
  properties:
    skill_id: "SKILL-OTA-007"
    
    diagnosis:
      type: object
      properties:
        current_position: { type: string, description: "当前位置描述" }
        gap_to_target: { type: integer }
        estimated_days_to_improve: { type: number }
    
    contributing_factors:
      type: array
      items:
        type: object
        properties:
          factor: { type: string }
          current_score: { type: number }
          target_score: { type: number }
          gap: { type: number }
          improvement_suggestion: { type: string }
    
    optimization_checklist:
      type: array
      items:
        type: object
        properties:
          task: { type: string }
          expected_impact: { type: number, description: "预估排名提升位数" }
          effort: { type: string, enum: [low, medium, high] }
          priority: { type: integer, description: "优先级(1最高)" }
    
    expected_outcome:
      type: object
      properties:
        target_ranking: { type: integer }
        confidence: { type: number }
        timeline: { type: string }
```

---

### 5.8 SKILL-OTA-008 差评预警与自动回复

**基本信息**
```
SKILL-ID：SKILL-OTA-008
名称：差评预警与自动回复（Review Alert & Auto-Reply）
版本：1.0
分类：OTA及收益管理 / OTA运营AGENT
优先级：P1
```

**输入规格**
```yaml
input:
  type: object
  required:
    - hotel_id
    - reviews
  
  properties:
    hotel_id: { type: string }
    reviews:
      type: array
      items:
        type: object
        properties:
          review_id: { type: string }
          platform: { type: string, enum: [ctrip, meituan, fliggy, dianping] }
          rating: { type: number, description: "评分(1-5)", example: 3 }
          content: { type: string, description: "点评内容" }
          publish_date: { type: string (datetime) }
          room_type: { type: string }
          reviewer_type: { type: string, enum: [vip, regular, first_time] }
```

**输出规格**
```yaml
output:
  type: object
  
  properties:
    skill_id: "SKILL-OTA-008"
    
    alerts:
      type: array
      description: "需要预警的差评"
      items:
        type: object
        properties:
          review_id: { type: string }
          severity: { type: string, enum: [critical, warning, notice] }
          alert_channels: { type: array, items: { type: string } }
          notify_to: { type: array, items: { type: string } }
          escalation_needed: { type: boolean }
    
    auto_replies:
      type: array
      description: "建议自动回复"
      items:
        type: object
        properties:
          review_id: { type: string }
          sentiment_score: { type: number }
          category: { type: string, description: "差评类型：service/cleanliness/facility/location/price" }
          
          suggested_reply:
            type: object
            properties:
              tone: { type: string, enum: [apologetic, explanatory, grateful, diplomatic] }
              content: { type: string, description: "回复内容" }
              keywords_to_include: { type: array }
              keywords_to_avoid: { type: array }
              length_preference: { type: string, enum: [short, medium, long] }
          
          review_manager_override: { type: boolean, description: "是否需人工审核" }
```

---

## 六、附录

### 6.1 术语表

| 术语 | 全称 | 中文 | 备注 |
|------|------|------|------|
| ADR | Average Daily Rate | 平均每日房价 | 客房收入/已售间夜 |
| ARI | ADR Index | ADR指数 | 酒店ADR/竞争群ADR×100 |
| BAR | Best Available Rate | 最优可售房价 | 收益管理基准价格 |
| GOP | Gross Operating Profit | 经营毛利 | 总收入-经营成本 |
| GOPPAR | GOP Per Available Room | 每房经营毛利 | GOP/可售房数 |
| MAPE | Mean Absolute Percentage Error | 平均绝对百分比误差 | 预测精度指标 |
| MPI | Market Penetration Index | 市场渗透指数 | 酒店OCC%/市场OCC%×100 |
| OCC | Occupancy Rate | 入住率 | 已售/可售×100% |
| RevPAR | Revenue Per Available Room | 每间可售房收入 | 客房收入/可售房 |
| RGI | Revenue Generation Index | 收益生成指数 | 酒店RevPAR/竞争群RevPAR×100 |
| RMS | Revenue Management System | 收益管理系统 | — |
| STR | Smith Travel Research | 酒店数据公司 | — |

### 6.2 参考文献

**学术文献**
1. Kimes, S.E. (1989). "The Basics of Yield Management." Cornell Hotel and Restaurant Administration Quarterly.
2. Weatherford, L.R. & Kimes, S.E. (2003). "A Comparison of Forecasting Methods for Hotel Revenue Management." International Journal of Forecasting.
3. Chen, T. & Guestrin, C. (2016). "XGBoost: A Scalable Tree Boosting System." KDD.
4. Taylor, S.J. & Letham, B. (2017). "Forecasting at Scale." Facebook Research.
5. Box, G.E.P., Jenkins, G.M. & Reinsel, G.C. (2015). "Time Series Analysis." 5th Edition.

**行业资料**
6. STR Global. "STAR Report Methodology." str.com.
7. IDeaS Revenue Solutions. "G3 RMS Technical Whitepaper."
8. Duetto. "GameChanger Product Documentation."
9. Rainmaker. "Revenue IQ Product Overview."

**中文资料**
10. 《收益管理》—— 中国旅游出版社
11. 《酒店管理与旅游研究》—— 国内期刊

---

**版本记录**

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| V1.0 | 2026-03-26 | 初始版本：数学公式体系+预测模型+分析方法+SKILL接口 |

**关联文档**
- `docs/AHL-初期数字员工需求清单-V1.0.md` — 功能需求来源
- `docs/AHL-初期数字员工SKILL体系-V1.0.md` — SKILL接口规范
- `memory/hotel-revenue-management-knowledge-base-v3.md` — 现有知识库参考
- `memory/hotel-industry-knowledge-base-v3.0.md` — 酒店行业知识库
