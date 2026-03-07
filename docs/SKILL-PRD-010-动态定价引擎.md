# SKILL-PRD-009: 动态定价引擎 (Dynamic Pricing Engine)

## 基本信息

| 字段 | 内容 |
|------|------|
**SKILL编号** | REV-001
**SKILL名称** | 动态定价引擎 (Dynamic Pricing Engine)
**所属AGENT** | 收益管理AGENT (Revenue Agent)
**版本** | v1.0
**创建日期** | 2026-03-04
**优先级** | P0 (收益管理核心)
**开发周期** | 6-8周

---

## 1. 价值定位

### 1.1 解决的问题
酒店收益管理面临复杂挑战：

**定价决策困难**
- 影响定价因素多(需求、竞争、事件、天气)，人工难以全面考量
- 价格调整凭经验，缺乏数据支撑
- 不同渠道、不同房型、不同日期价格混乱

**收益机会流失**
- 高峰期价格定低，损失高收益
- 低谷期价格僵化，房间空置
- 临时需求波动无法快速响应

**渠道管理复杂**
- OTA、官网、协议客户等多渠道价格冲突
- 渠道佣金成本差异大，定价策略难统一
- 价格一致性难以维护，引发客户投诉

### 1.2 核心价值
**"让每一间房在正确的时间以正确的价格卖给正确的客人"**

- **需求预测**：AI精准预测未来需求，提前布局定价策略
- **动态调价**：实时监控市场变化，自动/辅助价格调整
- **收益最大化**：科学的优化算法，RevPAR提升15-25%
- **策略自动化**：规则+AI双引擎，减少人工干预

### 1.3 量化收益

| 指标 | 传统模式 | AI动态定价 | 提升幅度 |
|------|---------|-----------|---------|
RevPAR | 基准值 | +15-25% | **显著提升** |
平均房价(ADR) | 基准值 | +10-15% | **旺季更高** |
出租率(OCC) | 基准值 | +5-8pp | **淡季改善** |
价格调整频率 | 1-2次/天 | 实时/小时级 | **提升10倍** |
收益管理人力 | 2-3人 | 0.5-1人 | **节省60%** |

---

## 2. 目标用户

### 2.1 主要用户

| 用户角色 | 使用场景 | 核心痛点 |
|---------|---------|---------|
**收益经理** | 制定定价策略，监控收益指标 | 数据太多看不过来，定价决策压力大 |
**销售总监** | 平衡团队销售与收益目标 | 收益管理限制销售灵活性 |
**前台经理** | 执行Walk-in定价，处理客户议价 | 不知道什么价格合适，怕卖亏或卖不掉 |
**总经理** | 把控整体收益表现 | 收益波动大，难预测难控制 |

### 2.2 用户画像

**典型用户：陈经理，35岁，商务酒店收益经理**
- 每天要花3小时分析数据、调整价格
- 旺季时害怕卖便宜了，淡季时怕房间空置
- 竞争对手突然降价，她经常反应不过来
- 希望能有个系统帮她自动监控、智能建议价格

---

## 3. 功能架构

### 3.1 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    应用层                                    │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ 定价仪表板   │ │ 价格日历    │ │ 竞争监控    │            │
│  │ (核心指标)   │ │ (可视化)    │ │ (市场情报)  │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                    定价引擎层 (核心)                         │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ 需求预测    │ │ 优化定价    │ │ 规则引擎    │            │
│  │ (LSTM/Prophet)│ │ (强化学习) │ │ (业务约束) │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
│  ┌─────────────┐ ┌─────────────┐                            │
│  │ 竞争响应    │ │ 渠道管理    │                            │
│  │ (博弈模型)  │ │ (差异化)    │                            │
│  └─────────────┘ └─────────────┘                            │
└─────────────────────────────────────────────────────────────┘
                              ↕
└─────────────────────────────────────────────────────────────┘
│                    数据层                                    │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ 历史订单    │ │ 市场数据    │ │ 事件数据    │            │
│  │ (PMS/OTA)   │ │ (爬虫/API)  │ │ (节假日等)  │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 核心功能模块

#### 模块1: 多维度需求预测

**预测维度**
```yaml
时间维度:
  - 未来90天每日预测
  - 未来365天周度趋势
  - 未来3年季节性规律

房型维度:
  - 标准间、大床房、套房、行政楼层
  - 每个房型单独预测

渠道维度:
  - OTA (携程/美团/Booking)
  - 官网直销
  - 协议客户
  - Walk-in

细分市场:
  - 商务客、休闲客、团队、长住客
  - 各自需求曲线
```

**预测模型**
```python
class DemandForecaster:
    """需求预测引擎"""
    
    def __init__(self):
        self.models = {
            'lstm': LSTMModel(),
            'prophet': ProphetModel(),
            'xgboost': XGBoostModel(),
            'ensemble': EnsembleModel()
        }
    
    def predict(self, room_type, channel, horizon=90):
        """
        预测未来需求
        
        输入特征:
        - 历史预订数据 (过去2年)
        - 当前预订进度 (Pickup)
        - 季节性因素 (节假日、周末)
        - 特殊事件 (展会、演唱会)
        - 价格弹性历史
        - 竞争对手价格
        - 宏观经济指标
        """
        
        features = self.extract_features(
            room_type=room_type,
            channel=channel,
            history_days=730
        )
        
        # 多模型预测
        predictions = {}
        for name, model in self.models.items():
            if name != 'ensemble':
                predictions[name] = model.predict(features, horizon)
        
        # 模型融合
        ensemble_pred = self.models['ensemble'].combine(predictions)
        
        # 生成置信区间
        confidence_interval = self.calculate_confidence_interval(
            predictions, 
            confidence=0.8
        )
        
        return {
            'point_forecast': ensemble_pred,
            'lower_bound': confidence_interval['lower'],
            'upper_bound': confidence_interval['upper'],
            'model_weights': self.get_model_weights(),
            'accuracy_metrics': self.evaluate_accuracy()
        }
```

**预测准确性**
| 预测期 | MAPE | 业务可用性 |
|--------|------|-----------|
7天内 | <5% | 极高 |
30天内 | <10% | 高 |
90天内 | <15% | 中高 |

**预测可视化**
```
┌─────────────────────────────────────────────────────────────┐
│ 📊 需求预测 - 标准间 - 携程渠道                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  预测准确度: 92% (过去30天MAPE: 6.5%)                       │
│                                                             │
│  需求预测曲线 (未来90天)                                     │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                                                     │   │
│  │    需求                                            │   │
│  │     ↑     ╭─╮  ╭──╮                               │   │
│  │   150 ┤  ╭╯  ╰──╯  ╰──╮  ← 清明假期高峰           │   │
│  │   100 ┤──╯             ╰──╮                       │   │
│  │    50 ┤                    ╰──╮                   │   │
│  │     0 └┬──┬──┬──┬──┬──┬──┬──┬──┬                │   │
│  │       今天 7天 14天 21天 30天 60天 90天          │   │
│  │                                                     │   │
│  │    ─── 点预测                                      │   │
│  │    ═══ 80%置信区间                                  │   │
│  │    ●●● 历史实际                                     │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  📅 关键日期提醒:                                            │
│  ├─ 4月4-6日 (清明): 预测需求 +150%，建议提前锁价         │
│  ├─ 4月15日 (展会): 周边酒店已涨价，建议跟进              │
│  └─ 5月1-5日 (五一): 预测满房，建议关闭折扣渠道           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 模块2: 动态优化定价

**定价模型**
```python
class DynamicPricingOptimizer:
    """动态定价优化器"""
    
    def optimize_price(self, room_type, date, constraints):
        """
        优化单房型单日价格
        
        目标函数: 最大化预期收益
        max E[Revenue] = Price × E[Demand(Price)]
        
        约束条件:
        - 最低价/最高价限制
        - 渠道价格一致性
        - 协议客户价格保护
        """
        
        # 1. 获取需求预测
        demand_forecast = self.forecaster.predict(
            room_type=room_type,
            date=date
        )
        
        # 2. 价格弹性估计
        price_elasticity = self.estimate_elasticity(
            room_type=room_type,
            date=date
        )
        
        # 3. 竞争价格参考
        comp_prices = self.get_competitor_prices(
            room_type=room_type,
            date=date
        )
        
        # 4. 优化求解
        optimal_price = self.solve_optimization(
            demand_function=demand_forecast,
            elasticity=price_elasticity,
            comp_prices=comp_prices,
            constraints=constraints
        )
        
        # 5. 应用业务规则
        final_price = self.apply_business_rules(
            optimal_price,
            room_type=room_type,
            date=date
        )
        
        return {
            'recommended_price': final_price,
            'confidence': self.calculate_confidence(),
            'expected_revenue': self.calculate_expected_revenue(
                final_price, demand_forecast
            ),
            'price_range': {
                'conservative': final_price * 0.95,
                'aggressive': final_price * 1.05
            },
            'reasoning': self.explain_price(final_price)
        }
```

**定价策略矩阵**
```yaml
需求强度 vs 剩余库存:
  
  高需求 + 低库存 (明星):
    策略: 溢价定价
    动作: 关闭折扣，设置Overbooking
    目标: 最大化收益
  
  高需求 + 高库存 (潜力):
    策略: 渐进提价
    动作: 监控Pickup，阶梯式提价
    目标: 平衡出租率和ADR
  
  低需求 + 低库存 (安全):
    策略: 稳价保收
    动作: 保持当前价格
    目标: 确保基础收益
  
  低需求 + 高库存 (风险):
    策略: 促销清房
    动作: 开放Last-minute折扣
    目标: 减少空置损失
```

**价格调整建议**
```
┌─────────────────────────────────────┐
│ 💡 价格调整建议 - 2026年4月15日      │
├─────────────────────────────────────┤
│                                     │
│  房型: 标准间                       │
│  当前价格: ¥458                     │
│  AI建议: ¥528 (+15%)               │
│  置信度: 85%                        │
│                                     │
│  📊 调整理由:                        │
│  ├─ 需求预测: 150间 (高需求)        │
│  ├─ 剩余库存: 45间 (紧张)           │
│  ├─ 竞品价格: ¥498-568 (我们有空间) │
│  └─ 特殊事件: 国际车展 (需求激增)   │
│                                     │
│  💰 预期效果:                        │
│  ├─ 预期出租率: 92% (-3%)           │
│  ├─ 预期RevPAR: ¥486 (+12%)         │
│  └─ 预期收益: ¥21,870 (+¥2,340)    │
│                                     │
│  [采纳建议] [保持现价] [自定义]     │
│                                     │
└─────────────────────────────────────┘
```

#### 模块3: 竞争情报监控

**竞品价格抓取**
```python
class CompetitorMonitor:
    """竞品价格监控"""
    
    def __init__(self):
        self.scrapers = {
            'ctrip': CtripScraper(),
            'meituan': MeituanScraper(),
            'booking': BookingScraper()
        }
        self.competitors = load_competitor_list()
    
    def monitor_prices(self, date_range):
        """监控竞品价格"""
        
        prices = {}
        
        for competitor in self.competitors:
            prices[competitor.name] = {}
            
            for channel, scraper in self.scrapers.items():
                try:
                    price = scraper.get_price(
                        hotel_name=competitor.name,
                        checkin=date_range['start'],
                        checkout=date_range['end'],
                        room_type='standard'
                    )
                    prices[competitor.name][channel] = price
                except Exception as e:
                    logger.error(f"Failed to get price for {competitor.name}: {e}")
        
        return prices
    
    def detect_price_changes(self, new_prices, old_prices):
        """检测价格变动"""
        
        changes = []
        
        for hotel, channels in new_prices.items():
            for channel, new_price in channels.items():
                old_price = old_prices.get(hotel, {}).get(channel)
                
                if old_price and new_price:
                    change_pct = (new_price - old_price) / old_price * 100
                    
                    if abs(change_pct) > 5:  # 变动超过5%
                        changes.append({
                            'hotel': hotel,
                            'channel': channel,
                            'old_price': old_price,
                            'new_price': new_price,
                            'change_pct': change_pct,
                            'timestamp': datetime.now()
                        })
        
        return changes
```

**竞品分析看板**
```
┌─────────────────────────────────────────────────────────────┐
│ 🔍 竞争情报监控                                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📊 今日价格对比 (标准间)                                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 酒店名称        携程    美团    Booking   价差    │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │ 本酒店         ¥458   ¥448   ¥72      基准    │   │
│  │ 竞品A          ¥498   ¥488   ¥78      +9%    │   │
│  │ 竞品B          ¥428   ¥418   ¥68      -7%    │   │
│  │ 竞品C          ¥478   ¥468   ¥75      +4%    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ⚡ 实时告警                                                 │
│  ├─ 🚨 竞品B降价15% (¥428→¥368)，建议关注                  │
│  ├─ 📈 竞品A涨价10%，我们有提价空间                        │
│  └─ 🆕 新竞争对手"XX酒店"上线，价格¥388                    │
│                                                             │
│  📈 价格趋势 (近7天)                                         │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                                                     │   │
│  │  ¥500 ┤╭─╮                                          │   │
│  │  ¥450 ┤╯  ╰──╮  ← 竞品A                           │   │
│  │  ¥400 ┤      ╰──╮╭─╮  ← 本酒店                   │   │
│  │  ¥350 ┤          ╰╯  ╰──╮  ← 竞品B              │   │
│  │       └┬──┬──┬──┬──┬──┬──┬                      │   │
│  │       -7  -6  -5  -4  -3  -2  -1  今天          │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  💡 策略建议: 竞品B持续降价，可能是促销清房，建议保持    │
│     当前价格，监控其出租率变化。                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 模块4: 渠道差异化定价

**渠道定价策略**
```yaml
渠道定价矩阵:
  
  官网直销:
    价格水平: 基准价 (100%)
    策略: 最低价保证，会员专属优惠
    目标: 提升直销占比，降低佣金成本
  
  OTA (携程/美团):
    价格水平: 基准价 +5~10%
    策略: 参与促销活动，获取流量
    目标: 补充客源，提高知名度
  
  协议客户:
    价格水平: 基准价 -5~15%
    策略: 年度协议价，阶梯折扣
    目标: 稳定基础客源
  
  Walk-in:
    价格水平: 基准价 +0~20%
    策略: 弹性定价，议价空间
    目标: 捕捉即时需求
```

**渠道监控与冲突检测**
```python
class ChannelManager:
    """渠道价格管理"""
    
    def check_price_parity(self):
        """检查价格一致性"""
        
        violations = []
        
        # 获取各渠道价格
        prices = {
            'official': self.get_official_price(),
            'ctrip': self.get_ctrip_price(),
            'meituan': self.get_meituan_price(),
            'booking': self.get_booking_price()
        }
        
        # 检查最低价保证
        for channel, price in prices.items():
            if channel != 'official' and price < prices['official']:
                violations.append({
                    'type': 'price_disparity',
                    'channel': channel,
                    'official_price': prices['official'],
                    'channel_price': price,
                    'severity': 'high' if price < prices['official'] * 0.95 else 'medium'
                })
        
        return violations
    
    def optimize_channel_mix(self):
        """优化渠道组合"""
        
        # 计算各渠道贡献
        channel_contribution = self.calculate_contribution()
        
        # 计算各渠道成本
        channel_cost = {
            'official': 0.03,      # 支付手续费3%
            'ctrip': 0.15,         # 佣金15%
            'meituan': 0.12,       # 佣金12%
            'booking': 0.18        # 佣金18%
        }
        
        # 计算净贡献
        for channel in channel_contribution:
            channel_contribution[channel]['net'] = (
                channel_contribution[channel]['revenue'] * 
                (1 - channel_cost[channel])
            )
        
        # 生成优化建议
        recommendations = []
        
        if channel_contribution['official']['share'] < 0.3:
            recommendations.append({
                'action': 'increase_direct_booking',
                'suggestion': '官网价格比OTA低5%，加大会员推广'
            })
        
        if channel_contribution['booking']['net'] < channel_contribution['booking']['revenue'] * 0.5:
            recommendations.append({
                'action': 'reduce_booking_dependency',
                'suggestion': 'Booking佣金过高，考虑减少库存投放'
            })
        
        return recommendations
```

#### 模块5: 收益管理仪表板

**核心KPI监控**
```
┌─────────────────────────────────────────────────────────────┐
│ 📊 收益管理仪表板                    更新时间: 2026-03-04 14:30 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📈 今日收益表现                                             │
│  ┌──────────┬──────────┬──────────┬──────────┐            │
│  │  RevPAR  │   ADR    │   OCC    │   收入   │            │
│  │  ¥386    │  ¥458    │  84.2%   │ ¥45,680  │            │
│  │  ↑12%    │  ↑8%     │  ↑3pp    │  ↑15%    │            │
│  └──────────┴──────────┴──────────┴──────────┘            │
│                                                             │
│  📅 未来30天展望                                             │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                                                     │   │
│  │  预测RevPAR: ¥412 (+10% vs 上月)                   │   │
│  │                                                     │   │
│  │  关键日期:                                          │   │
│  │  ├─ 3月15-17日 (周末): RevPAR ¥520 (高)            │   │
│  │  ├─ 3月20日 (展会): RevPAR ¥480 (中高)             │   │
│  │  └─ 3月25-31日 (淡季): RevPAR ¥320 (低)            │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ⚠️ 需关注事项                                               │
│  ├─ 下周末需求旺盛，仅剩20间房，建议提价10%               │
│  ├─ 3月25-31日预测OCC仅65%，建议开放促销                  │
│  └─ 竞品A连续3天降价，可能影响我们下周预订                │
│                                                             │
│  💡 AI建议行动                                               │
│  ├─ [立即提价] 本周末价格可上调8-12%                      │
│  ├─ [查看详情] 下周展会期间定价策略                       │
│  └─ [设置规则] 自动调价规则优化                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**价格日历**
```
┌─────────────────────────────────────────────────────────────┐
│ 📅 价格日历 - 标准间 - 2026年3月                             │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  周日   周一   周二   周三   周四   周五   周六             │
│  ┌──┐  ┌──┐  ┌──┐  ┌──┐  ┌──┐  ┌──┐  ┌──┐                │
│  │ 1 │  │ 2 │  │ 3 │  │ 4 │  │ 5 │  │ 6 │  │ 7 │                │
│  │¥428│  │¥428│  │¥458│  │¥458│  │¥488│  │¥528│  │¥528│                │
│  │ 75%│  │ 72%│  │ 80%│  │ 85%│  │ 88%│  │ 95%│  │ 92%│                │
│  └──┘  └──┘  └──┘  └──┘  └──┘  └──┘  └──┘                │
│  ┌──┐  ┌──┐  ┌──┐  ┌──┐  ┌──┐  ┌──┐  ┌──┐                │
│  │ 8 │  │ 9 │  │10 │  │11 │  │12 │  │13 │  │14 │                │
│  │¥458│  │¥428│  │¥428│  │¥458│  │¥488│  │¥528│  │¥528│                │
│  │ 78%│  │ 70%│  │ 68%│  │ 82%│  │ 90%│  │ 98%│  │ 94%│                │
│  └──┘  └──┘  └──┘  └──┘  └──┘  └──┘  └──┘                │
│                                                             │
│  图例: 价格(OCC预测)  🟢高需求  🟡中需求  🔴低需求          │
│                                                             │
│  [批量修改] [导出日历] [设置自动规则]                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. 技术实现

### 4.1 技术栈

| 层级 | 技术选型 | 说明 |
|------|---------|------|
**数据采集** | Python + Scrapy | 竞品价格抓取 |
**预测模型** | Prophet + LSTM | 时间序列预测 |
**优化算法** | OR-Tools + RL | 定价优化求解 |
**规则引擎** | Drools | 业务规则管理 |
**前端** | React + ECharts | 数据可视化 |
**数据库** | PostgreSQL + Redis | 时序数据存储 |

### 4.2 自动化定价流程

```
定时任务 (每2小时)
    ↓
采集最新数据:
  - 当前预订进度
  - 竞品价格变动
  - 市场需求信号
    ↓
运行预测模型:
  - 更新需求预测
  - 评估价格弹性
    ↓
优化定价:
  - 求解最优价格
  - 检查业务规则
    ↓
生成建议:
  - 价格调整建议
  - 置信度评估
    ↓
人工审核/自动执行:
  - 高置信度: 自动调整
  - 中置信度: 推送建议
  - 低置信度: 标记审核
    ↓
同步各渠道
```

---

## 5. 成功指标

| 指标 | 目标值 | 说明 |
|------|--------|------|
RevPAR提升 | 15-25% | 对比去年同期 |
预测准确率(7天) | >90% | MAPE |
价格调整响应时间 | <2小时 | 从市场变化到调价 |
人工干预率 | <30% | 自动定价占比 |
渠道价格一致性 | >95% | 无违规率 |

---

## 6. 实施路径

**Phase 1: 数据基础 (4周)**
- 历史数据清洗
- 竞品价格监控上线
- 基础报表开发

**Phase 2: 预测模型 (4周)**
- 需求预测模型训练
- 预测准确性验证
- 预测可视化上线

**Phase 3: 优化定价 (4周)**
- 定价优化算法上线
- 自动化规则配置
- A/B测试验证效果

**Phase 4: 智能化 (持续)**
- 强化学习优化
- 个性化策略
- 全自动化运营

---

**文档版本**: v1.0 | **创建日期**: 2026-03-04
