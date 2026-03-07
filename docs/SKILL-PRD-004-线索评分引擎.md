# SKILL-PRD-004: 线索评分引擎 (Lead Scoring Engine)

## 基本信息

| 字段 | 内容 |
|------|------|
**SKILL编号** | GRW-016
**SKILL名称** | 线索评分引擎 (Lead Scoring Engine)
**所属AGENT** | 营销增长AGENT (Growth Agent)
**版本** | v1.0
**创建日期** | 2026-03-04
**优先级** | P0 (配套雷达的核心算法)
**开发周期** | 4-6周

---

## 1. 价值定位

### 1.1 解决的问题
酒店销售团队每天面对大量潜在客户线索，面临：

**线索质量参差不齐**
- 销售每天接到20-50条线索，不知道哪些是"真需求"
- 70%的时间浪费在低价值线索上
- 高价值客户被淹没在海量信息中

**评分标准主观随意**
- 不同销售对线索价值判断差异巨大
- 缺乏统一、可量化的评分体系
- "感觉不错"无法支撑资源分配决策

**转化路径不清晰**
- 不知道线索处于购买旅程的哪个阶段
- 不清楚应该采取什么跟进策略
- 缺乏基于数据的最佳行动建议

### 1.2 核心价值
**"让每一条线索都有清晰的'价值身份证'和'行动指南'"**

- **精准分级**：AI多维度评估，95%+准确率识别高价值线索
- **动态更新**：实时响应企业动态变化，评分实时调整
- **行动指导**：不仅告诉销售"值多少分"，更告诉"下一步做什么"
- **持续优化**：基于成交反馈自我学习，模型越用越准

### 1.3 量化收益

| 指标 | 传统模式 | AI评分引擎 | 提升幅度 |
|------|---------|-----------|---------|
高价值线索识别率 | 30-40% | 90%+ | **提升150%** |
销售人效 | 基准值 | +200% | **提升2倍** |
线索转化率 | 5-8% | 15-20% | **提升200%** |
平均成交周期 | 45天 | 28天 | **缩短38%** |
销售满意度 | 60% | 90% | **提升50%** |

---

## 2. 目标用户

### 2.1 主要用户

| 用户角色 | 使用场景 | 核心痛点 |
|---------|---------|---------|
**销售经理** | 每天早上查看今日推荐线索列表 | 不知道从哪开始，怕错过大鱼 |
**销售总监** | 分配线索给团队，监控转化漏斗 | 线索分配不公平，好线索都被"关系户"拿走 |
**CRM系统** | 自动给线索打标签、触发自动化流程 | 标签不准，自动化经常骚扰错误人群 |
**市场部门** | 评估获客渠道ROI | 不知道哪个渠道来的线索质量高 |

### 2.2 用户画像

**典型用户：李经理，33岁，商务酒店销售经理**
- 每天收到30-40条新线索，但只有时间跟进10个
- 上周错过了一个A级客户，被竞品签了协议
- 希望能有个"智能助手"帮他把好线索排到最前面
- 抱怨"系统推的线索很多，但能成交的没几个"

---

## 3. 功能架构

### 3.1 评分维度体系

**四维评分模型**
```
综合得分 = Σ(维度得分 × 权重)
         = 企业价值(25%) + 需求强度(30%) + 匹配度(25%) + 触达难度(20%)
```

#### 维度1: 企业价值 (Firmographic Score) - 权重25%

评估企业本身的规模和价值潜力。

| 指标 | 数据来源 | 评分规则 | 权重 |
|------|---------|---------|------|
**企业规模** | 企查查/天眼查 | 参保人数分级 | 30% |
- <50人: 20分 | | | 
- 50-200人: 50分 | | |
- 200-500人: 75分 | | |
- >500人: 100分 | | |
**注册资本** | 工商数据 | 注册资本分级 | 20% |
- <100万: 20分 | | |
- 100-500万: 40分 | | |
- 500-2000万: 70分 | | |
- >2000万: 100分 | | |
**行业价值** | 行业模型 | 差旅强度行业分级 | 30% |
- 高频差旅(咨询/金融/科技): 100分 | | |
- 中频差旅(制造/医药): 70分 | | |
- 低频差旅(零售/本地服务): 40分 | | |
**地理距离** | 高德地图 | 距酒店距离 | 20% |
- <1km: 100分 | | |
- 1-3km: 80分 | | |
- 3-5km: 60分 | | |
- >5km: 40分 | | |

#### 维度2: 需求强度 (Intent Score) - 权重30%

评估企业当前产生酒店需求的紧迫程度。

| 信号类型 | 数据来源 | 评分规则 | 时效性 |
|---------|---------|---------|--------|
**招聘信号** | 招聘网站 | 出差相关岗位数量 | 3个月 |
- 发布>10个出差岗位: +30分 | | |
- 发布5-10个: +20分 | | |
- 发布<5个: +10分 | | |
**融资/扩张** | 新闻+工商 | 融资轮次+金额 | 6个月 |
- B轮及以上融资: +25分 | | |
- A轮融资: +15分 | | |
- 天使轮: +10分 | | |
- 新增分支机构: +20分 | | |
**展会/活动** | 10times/Cvent | 参展/办展信息 | 展前30天 |
- 主办大型展会(>1000人): +30分 | | |
- 参展(>500人): +20分 | | |
- 内部年会/发布会: +15分 | | |
**招投标** | 采招网 | 酒店相关招标 | 实时 |
- 会议服务招标: +25分 | | |
- 差旅服务商招标: +25分 | | |
**社交意图** | 抖音/小红书 | 地理标签内容 | 实时 |
- 备婚/会议选址/乔迁: +20分 | | |

**时间衰减函数**
```python
def time_decay(signal_date, half_life_days=30):
    """信号随时间衰减，半衰期30天"""
    days_passed = (today - signal_date).days
    decay_factor = 0.5 ** (days_passed / half_life_days)
    return decay_factor
```

#### 维度3: 匹配度 (Fit Score) - 权重25%

评估企业与酒店产品服务的匹配程度。

| 指标 | 评估逻辑 | 数据来源 |
|------|---------|---------|
**价格匹配** | 企业规模与酒店ADR匹配度 | 行业基准数据 |
- 大型企业→高星级酒店: 100分 | | |
- 中型企业→商务酒店: 80分 | | |
- 小型企业→经济型: 60分 | | |
**设施匹配** | 企业需求与酒店设施匹配 | 设施标签 |
- 需要会议设施→有会议室: +20分 | | |
- 需要餐饮→有宴会厅: +15分 | | |
- 需要长住→有公寓房型: +15分 | | |
**历史偏好** | 相似企业的历史选择 | 行业数据 |
- 同行业企业偏好本酒店: +10分 | | |

#### 维度4: 触达难度 (Accessibility Score) - 权重20%

评估联系关键决策人的难易程度。

| 指标 | 评分规则 | 数据来源 |
|------|---------|---------|
**联系人完整度** | 关键决策人信息完整度 | 企查查/LinkedIn |
- 有行政/采购负责人联系方式: 100分 | | |
- 仅有总机/前台: 40分 | | |
- 无任何联系方式: 0分 | | |
**关系网络** | 是否与酒店已有关系 | CRM数据 |
- 已有联系人引荐: +30分 | | |
- 与现有客户有关联: +20分 | | |
**触达历史** | 过往沟通响应率 | CRM历史 |
- 历史响应率>50%: +20分 | | |
- 历史响应率20-50%: +10分 | | |

### 3.2 AI模型架构

**模型1: 规则引擎 (Baseline)**
```python
class RuleBasedScorer:
    """基于业务规则的评分引擎"""
    
    def calculate_score(self, company_data):
        score = 0
        
        # 企业价值维度 (25%)
        firmographic = (
            self.score_scale(company_data['employees']) * 0.3 +
            self.score_capital(company_data['registered_capital']) * 0.2 +
            self.score_industry(company_data['industry']) * 0.3 +
            self.score_distance(company_data['distance']) * 0.2
        )
        score += firmographic * 0.25
        
        # 需求强度维度 (30%)
        intent = self.calculate_intent_score(company_data['signals'])
        score += intent * 0.30
        
        # 匹配度维度 (25%)
        fit = self.calculate_fit_score(company_data, hotel_profile)
        score += fit * 0.25
        
        # 触达难度维度 (20%)
        accessibility = self.score_accessibility(company_data['contacts'])
        score += accessibility * 0.20
        
        return {
            'total_score': round(score, 1),
            'dimensions': {
                'firmographic': round(firmographic, 1),
                'intent': round(intent, 1),
                'fit': round(fit, 1),
                'accessibility': round(accessibility, 1)
            }
        }
```

**模型2: 机器学习模型 (XGBoost)**
```python
class MLScorer:
    """基于XGBoost的机器学习评分模型"""
    
    def __init__(self):
        self.model = xgboost.XGBClassifier(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1
        )
    
    def feature_engineering(self, company_data):
        """特征工程"""
        features = {
            # 基础特征
            'employee_count': company_data['employees'],
            'capital_million': company_data['registered_capital'] / 10000,
            'distance_km': company_data['distance'],
            
            # 信号特征
            'signal_count_7d': count_signals(company_data, days=7),
            'signal_count_30d': count_signals(company_data, days=30),
            'has_funding_signal': has_signal_type(company_data, 'funding'),
            'has_recruit_signal': has_signal_type(company_data, 'recruit'),
            
            # 时序特征
            'days_since_last_signal': days_since_last(company_data),
            'signal_trend': calculate_trend(company_data),  # 上升/下降
            
            # 行业特征
            'industry_code': encode_industry(company_data['industry']),
            'industry_avg_adr': get_industry_benchmark(company_data['industry']),
            
            # 联系人特征
            'contact_count': len(company_data['contacts']),
            'has_decision_maker': has_decision_maker(company_data),
        }
        return features
    
    def predict_conversion_probability(self, company_data):
        """预测转化概率"""
        features = self.feature_engineering(company_data)
        proba = self.model.predict_proba([features])[0][1]
        return proba
```

**模型3: 深度学习模型 (Wide & Deep)**
```python
class DeepLearningScorer:
    """Wide & Deep Learning模型，处理高维稀疏特征"""
    
    def __init__(self):
        # Wide部分: 处理稀疏特征(行业、地区等)
        self.wide_features = ['industry', 'district', 'company_type']
        
        # Deep部分: 处理连续特征和Embedding
        self.deep_features = ['employees', 'capital', 'distance', 'signal_count']
        
        self.model = self.build_model()
    
    def build_model(self):
        # Wide侧
        wide_input = Input(shape=(len(self.wide_features),))
        wide_output = wide_input
        
        # Deep侧
        deep_input = Input(shape=(len(self.deep_features),))
        x = Dense(128, activation='relu')(deep_input)
        x = Dropout(0.3)(x)
        x = Dense(64, activation='relu')(x)
        x = Dropout(0.3)(x)
        deep_output = Dense(32, activation='relu')(x)
        
        # 合并
        merged = concatenate([wide_output, deep_output])
        output = Dense(1, activation='sigmoid')(merged)
        
        model = Model(inputs=[wide_input, deep_input], outputs=output)
        model.compile(optimizer='adam', loss='binary_crossentropy')
        return model
```

**模型融合策略**
```python
class EnsembleScorer:
    """模型融合，综合各模型优势"""
    
    def __init__(self):
        self.rule_scorer = RuleBasedScorer()
        self.ml_scorer = MLScorer()
        self.dl_scorer = DeepLearningScorer()
        
        # 模型权重(基于历史表现动态调整)
        self.weights = {
            'rule': 0.3,
            'ml': 0.4,
            'dl': 0.3
        }
    
    def ensemble_score(self, company_data):
        rule_score = self.rule_scorer.calculate_score(company_data)
        ml_proba = self.ml_scorer.predict_conversion_probability(company_data)
        dl_proba = self.dl_scorer.predict(company_data)
        
        # 融合
        ensemble_score = (
            rule_score['total_score'] * self.weights['rule'] +
            ml_proba * 100 * self.weights['ml'] +
            dl_proba * 100 * self.weights['dl']
        )
        
        return {
            'ensemble_score': round(ensemble_score, 1),
            'rule_score': rule_score,
            'ml_proba': round(ml_proba, 3),
            'dl_proba': round(dl_proba, 3),
            'confidence': self.calculate_confidence()
        }
```

### 3.3 评分等级与行动建议

**等级划分**
```yaml
S级 (90-100分): 战略级客户
  - 描述: 高价值 + 高需求 + 易触达
  - 行动: 销售总监亲自跟进，48小时内拜访
  - 资源投入: 最高优先级

A级 (75-89分): 高价值客户
  - 描述: 高价值 + 中高需求
  - 行动: 资深销售经理跟进，3天内拜访
  - 资源投入: 高优先级

B级 (60-74分): 培育客户
  - 描述: 中等价值，有一定需求信号
  - 行动: 普通销售跟进，电话联系+邮件培育
  - 资源投入: 中等优先级

C级 (40-59分): 观察客户
  - 描述: 价值一般或需求不明确
  - 行动: 纳入培育池，定期监控动态
  - 资源投入: 低优先级，自动化触达

D级 (<40分): 低价值客户
  - 描述: 价值低且需求弱
  - 行动: 暂不跟进，放入冷池
  - 资源投入: 最低优先级
```

**行动建议引擎**
```python
def generate_action_recommendation(company_data, score_result):
    """基于评分结果生成行动建议"""
    
    recommendations = []
    
    # 基于评分等级的基础建议
    level = get_level(score_result['total_score'])
    recommendations.append({
        'type': 'priority',
        'content': f'该线索为{level}级，建议{get_action_by_level(level)}'
    })
    
    # 基于最强信号的具体建议
    top_signal = get_strongest_signal(company_data['signals'])
    if top_signal:
        recommendations.append({
            'type': 'signal_based',
            'content': generate_signal_message(top_signal)
        })
    
    # 基于联系人情况
    if not has_decision_maker(company_data):
        recommendations.append({
            'type': 'contact',
            'content': '建议先通过LinkedIn或前台找到行政/采购负责人'
        })
    
    # 基于历史互动
    if has_previous_contact(company_data):
        recommendations.append({
            'type': 'history',
            'content': '该客户6个月前有过接触，建议提及上次的沟通内容'
        })
    
    return recommendations
```

---

## 4. 技术实现

### 4.1 实时评分流程

```
数据输入 (企业信息+信号数据)
    ↓
特征工程 (实时计算20+维度特征)
    ↓
并行模型计算:
    ├─ 规则引擎 (10ms)
    ├─ XGBoost模型 (50ms)
    └─ Wide&Deep模型 (80ms)
    ↓
模型融合 (加权平均)
    ↓
等级划分 + 行动建议生成
    ↓
结果输出 (总耗时 < 200ms)
```

### 4.2 API设计

```yaml
# 单企业评分
POST /api/v1/scoring/calculate
请求:
  company_id: string
  company_name: string
  unified_code: string
  signals: [signal_object]
  
响应:
  {
    "score": 87.5,
    "level": "A",
    "confidence": 0.92,
    "dimensions": {
      "firmographic": 85.0,
      "intent": 92.0,
      "fit": 78.0,
      "accessibility": 88.0
    },
    "factors": [
      {"name": "近期融资", "impact": "+15分", "weight": "high"},
      {"name": "距离近", "impact": "+10分", "weight": "medium"}
    ],
    "recommendations": [
      {"type": "priority", "content": "A级线索，建议3天内拜访"},
      {"type": "signal", "content": "对方刚完成B轮融资，可祝贺并切入"}
    ]
  }

# 批量评分
POST /api/v1/scoring/batch
请求:
  companies: [company_object]
  
响应:
  {
    "total": 100,
    "processed": 100,
    "results": [
      {"company_id": "xxx", "score": 87.5, "level": "A"},
      ...
    ],
    "distribution": {
      "S": 5,
      "A": 20,
      "B": 45,
      "C": 25,
      "D": 5
    }
  }

# 评分解释
GET /api/v1/scoring/{company_id}/explain
响应: 详细的评分解释，包括各维度得分、关键影响因素

# 模型反馈
POST /api/v1/scoring/feedback
请求:
  company_id: string
  actual_outcome: "converted" | "not_converted"
  feedback_notes: string
用途: 将实际成交结果反馈给模型，用于持续优化
```

### 4.3 模型训练与优化

**训练数据**
```
正样本: 过去12个月签约的客户 (5000个)
负样本: 跟进超过3次但未成交的线索 (15000个)

特征数据:
- 企业工商数据 (静态)
- 信号数据 (动态，签约前6个月)
- 互动数据 (沟通次数、响应率等)

数据划分:
- 训练集: 70%
- 验证集: 15%
- 测试集: 15%
```

**模型评估指标**
```
准确率 (Accuracy): >85%
精确率 (Precision): >80%
召回率 (Recall): >85%
F1 Score: >82%
AUC-ROC: >0.90

业务指标:
- S/A级线索转化率: >40%
- 高评分线索占比: 20-30%
- 低评分线索误伤率: <10%
```

**持续优化机制**
```python
class ModelOptimizer:
    """模型持续优化"""
    
    def weekly_review(self):
        """每周模型复盘"""
        # 1. 收集上周的成交反馈
        feedback_data = self.collect_feedback()
        
        # 2. 分析模型表现
        performance = self.evaluate_performance(feedback_data)
        
        # 3. 识别问题案例
        false_positives = self.find_false_positives()
        false_negatives = self.find_false_negatives()
        
        # 4. 如果有显著偏差，触发重训练
        if performance['f1_score'] < 0.80:
            self.trigger_retraining()
        
        # 5. 更新特征权重
        self.adjust_feature_weights(performance)
    
    def monthly_retraining(self):
        """每月全量重训练"""
        # 使用最新的3个月数据重新训练
        new_data = self.load_recent_data(months=3)
        self.model.fit(new_data)
        
        # A/B测试验证新模型
        self.run_ab_test(new_model)
        
        # 如果新模型更好，上线
        if self.validate_improvement():
            self.deploy_new_model()
```

---

## 5. 界面设计

### 5.1 销售端界面

**线索评分卡片**
```
┌─────────────────────────────────────┐
│ 🏢 XX科技有限公司        [A级] 87分 │
├─────────────────────────────────────┤
│                                     │
│  📊 评分构成                        │
│  企业价值 ████████░░ 85分 (25%)    │
│  需求强度 █████████░ 92分 (30%) ⭐ │
│  匹配度   ███████░░░ 78分 (25%)    │
│  触达难度 ████████░░ 88分 (20%)    │
│                                     │
│  💡 关键信号                        │
│  ├─ 🎉 3天前完成B轮5000万融资      │
│  ├─ 📢 1周前发布12个销售岗位       │
│  └─ 📅 2周后主办行业展会           │
│                                     │
│  📈 转化概率: 78% (高信心)          │
│                                     │
│  🎯 行动建议:                       │
│  1. 本周内务必拜访                  │
│  2. 切入点: 祝贺融资+差旅解决方案   │
│  3. 联系人: 行政总监 张女士         │
│                                     │
│  [查看详情] [生成开发信] [一键外呼] │
└─────────────────────────────────────┘
```

**评分解释弹窗**
```
┌─────────────────────────────────────┐
│ 评分详情              [✕]           │
├─────────────────────────────────────┤
│                                     │
│  为什么这个线索值87分?              │
│                                     │
│  ✅ 加分项 (+42分)                  │
│  ├─ 近期融资 +15分                  │
│  │   "B轮融资通常意味着团队扩张    │
│  │    和差旅需求增加"              │
│  ├─ 大规模招聘 +12分                │
│  │   "12个销售岗位表明业务扩张"    │
│  ├─ 距离酒店近 +10分                │
│  └─ 有明确联系人 +5分               │
│                                     │
│  ⚠️ 减分项 (-8分)                   │
│  └─ 历史无差旅记录 -8分             │
│     "该行业传统上差旅较少"          │
│                                     │
│  📊 相似企业转化情况:               │
│  过去6个月，87±5分的线索平均:       │
│  - 首次响应率: 65%                  │
│  - 最终转化率: 28%                  │
│  - 平均成交周期: 32天               │
│                                     │
└─────────────────────────────────────┘
```

### 5.2 管理端界面

**评分效果看板**
```
┌─────────────────────────────────────────────────────────────┐
│ 线索评分效果分析                          [本月] [上月]      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📊 线索分布 vs 转化情况                                    │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 等级 │ 线索数 │ 占比  │ 转化数 │ 转化率 │ 贡献度   │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │  S   │   25   │  5%   │   12   │  48%   │  24%    │   │
│  │  A   │   98   │ 20%   │   28   │  29%   │  35%    │   │
│  │  B   │  220   │ 45%   │   22   │  10%   │  28%    │   │
│  │  C   │  125   │ 25%   │    5   │   4%   │   9%    │   │
│  │  D   │   25   │  5%   │    0   │   0%   │   0%    │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  💡 洞察: S+A级线索占总线索25%，贡献59%的转化             │
│                                                             │
│  📈 模型准确率趋势                                          │
│  ┌─────────────────────────────────────────────────────┐   │
│  │                                                     │   │
│  │   准确率: 87% (↑3% vs 上月)                        │   │
│  │   精确率: 82% (↑2% vs 上月)                        │   │
│  │   召回率: 89% (↑4% vs 上月)                        │   │
│  │                                                     │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  ⚠️ 需要关注的问题                                          │
│  ├─ 上周有3个B级线索实际成交，模型评分为C级(低估)         │
│  └─ 建议: 调整"行业差旅强度"权重                         │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## 6. 成功指标

| 指标 | 目标值 | 说明 |
|------|--------|------|
评分准确率 | >85% | 评分等级与实际转化匹配度 |
S/A级转化率 | >35% | 高价值线索的实际转化比例 |
销售人效提升 | >150% | 使用评分后人均产出增长 |
评分响应时间 | <200ms | 单次评分计算耗时 |
模型AUC-ROC | >0.90 | 模型区分能力 |

---

## 7. 迭代计划

**Phase 1: 规则引擎版 (2周)**
- 实现基于业务规则的评分逻辑
- 支持4维度20+特征评分
- 基础等级划分和行动建议

**Phase 2: 机器学习版 (4周)**
- 引入XGBoost模型
- 基于历史成交数据训练
- A/B测试验证效果

**Phase 3: 深度学习版 (4周)**
- 引入Wide&Deep模型
- 支持高维稀疏特征
- 模型融合提升准确率

**Phase 4: 持续优化 (持续)**
- 自动反馈闭环
- 特征工程自动化
- 个性化模型(按酒店类型)

---

**文档版本**: v1.0 | **创建日期**: 2026-03-04
