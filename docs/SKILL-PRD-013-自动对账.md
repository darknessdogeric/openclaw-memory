# SKILL-PRD-012: 自动对账 (Automated Reconciliation)

## 基本信息

| 字段 | 内容 |
|------|------|
**SKILL编号** | FIN-001
**SKILL名称** | 自动对账 (Automated Reconciliation)
**所属AGENT** | 财务风控AGENT (Finance Agent)
**版本** | v1.0
**创建日期** | 2026-03-04
**优先级** | P0 (财务效率核心)
**开发周期** | 4-6周

---

## 1. 价值定位

### 1.1 解决的问题
酒店财务对账面临繁重负担：

**数据量大且分散**
- 每日数百笔交易，来源多样(PMS/OTA/POS/银行)
- OTA渠道10+家，每家对账规则不同
- 退改订单频繁，手工核对易出错

**对账效率低下**
- 财务每天花3-4小时手工对账
- 月末集中对账，加班加点
- 差异查找困难，经常需要翻查多系统

**差错风险高**
- 手工操作难免疏漏
- 异常交易发现滞后
- 资金风险难以及时识别

### 1.2 核心价值
**"让对账从'手工苦力'变为'智能监控'，财务专注分析与决策"**

- **自动抓取**：每日自动从各系统抓取交易数据
- **智能匹配**：AI自动匹配订单与流水，准确率99%+
- **异常预警**：实时发现差异，主动推送告警
- **一键核销**：批量处理匹配项，财务只需审核异常

### 1.3 量化收益

| 指标 | 传统模式 | 自动对账 | 提升幅度 |
|------|---------|---------|---------|
对账时间 | 3-4小时/天 | 15分钟/天 | **节省90%** |
对账准确率 | 95% | 99.5% | **提升5%** |
异常发现时间 | 3-7天 | 实时 | **快100倍** |
月末结账周期 | 5-7天 | 1-2天 | **缩短70%** |
财务人员需求 | 3-4人 | 1-2人 | **节省50%** |

---

## 2. 目标用户

### 2.1 主要用户

| 用户角色 | 使用场景 | 核心痛点 |
|---------|---------|---------|
**应收会计** | 每日核对OTA/直销订单与到账 | 订单多、差异多、查找困难 |
**收入审计** | 审核收入确认与成本匹配 | 数据分散，难以全面核对 |
**财务主管** | 监控资金异常，把控风险 | 异常发现滞后，被动应对 |
**财务总监** | 月末结账，出具报表 | 结账周期长，数据准确性难保证 |

### 2.2 用户画像

**典型用户：张会计，32岁，酒店应收会计**
- 每天要从5个OTA后台下载账单，逐笔核对
- 经常有订单金额对不上，需要翻查PMS记录
- 退单、改价的情况很多，手工处理容易漏
- 希望有个系统能自动帮她核对，她只处理异常

---

## 3. 功能架构

### 3.1 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    展示层                                    │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ 对账工作台   │ │ 差异分析    │ │ 报表中心    │            │
│  │ (任务管理)   │ │ (明细查询)  │ │ (统计报表)  │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                    核心引擎层                                │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ 数据抓取    │ │ 匹配引擎    │ │ 差异分析    │            │
│  │ (ETL)       │ │ (AI/规则)   │ │ (根因定位)  │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
│  ┌─────────────┐ ┌─────────────┐                            │
│  │ 核销处理    │ │ 预警监控    │                            │
│  │ (自动/批量) │ │ (异常检测)  │                            │
│  └─────────────┘ └─────────────┘                            │
└─────────────────────────────────────────────────────────────┘
                              ↕
└─────────────────────────────────────────────────────────────┘
│                    数据接入层                                │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ PMS系统     │ │ OTA平台     │ │ 银行/支付   │            │
│  │ (订单数据)  │ │ (渠道账单)  │ │ (资金流水)  │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
│  ┌─────────────┐ ┌─────────────┐                            │
│  │ POS系统     │ │ 会员系统    │                            │
│  │ (餐饮/商品) │ │ (积分/储值) │                            │
│  └─────────────┘ └─────────────┘                            │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 核心功能模块

#### 模块1: 多源数据自动抓取

**数据源配置**
```yaml
PMS系统 (酒店管理系统):
  系统: Opera/Fidelio/千里马
  数据: 订单信息、房价、入住状态
  频率: 每小时同步
  方式: API对接

OTA渠道:
  携程:
    数据: 订单明细、佣金、结算单
    频率: 每日凌晨自动下载
    方式: 开放平台API + EBooking
  
  美团:
    数据: 订单、优惠、结算
    频率: 每日凌晨自动下载
    方式: 美团开放平台
  
  Booking:
    数据: 订单、佣金
    频率: 每日自动同步
    方式: Booking extranet API
  
  飞猪/同程/... (其他渠道)

银行/支付:
  银行流水:
    数据: 到账记录、手续费
    频率: 每日自动下载
    方式: 网银接口/银企直联
  
  微信支付:
    数据: 支付流水、退款
    频率: 实时
    方式: 微信支付API
  
  支付宝:
    数据: 支付流水
    频率: 实时
    方式: 支付宝API
```

**ETL数据处理**
```python
class DataExtractor:
    """数据提取器"""
    
    def extract_from_ota(self, channel, date):
        """从OTA提取账单数据"""
        
        extractors = {
            'ctrip': CtripExtractor(),
            'meituan': MeituanExtractor(),
            'booking': BookingExtractor(),
            'fliggy': FliggyExtractor()
        }
        
        extractor = extractors.get(channel)
        raw_data = extractor.download_bill(date)
        
        # 数据清洗和标准化
        standardized_data = self.standardize(raw_data, channel)
        
        return standardized_data
    
    def standardize(self, raw_data, source):
        """标准化数据格式"""
        
        standard_fields = {
            'order_id': self.extract_order_id(raw_data, source),
            'channel': source,
            'guest_name': self.extract_guest_name(raw_data),
            'checkin_date': self.extract_checkin_date(raw_data),
            'checkout_date': self.extract_checkout_date(raw_data),
            'room_nights': self.extract_room_nights(raw_data),
            'room_amount': self.extract_room_amount(raw_data),
            'commission': self.extract_commission(raw_data),
            'net_amount': self.calculate_net_amount(raw_data),
            'payment_status': self.extract_payment_status(raw_data),
            'transaction_date': self.extract_transaction_date(raw_data)
        }
        
        return standard_fields
```

#### 模块2: 智能匹配引擎

**匹配规则体系**
```python
class ReconciliationMatcher:
    """对账匹配引擎"""
    
    def __init__(self):
        self.match_rules = [
            ExactMatchRule(),      # 精确匹配
            FuzzyMatchRule(),      # 模糊匹配
            PartialMatchRule(),    # 部分匹配
            CompositeMatchRule()   # 组合匹配
        ]
    
    def match(self, pms_records, channel_records):
        """
        执行对账匹配
        
        匹配维度:
        1. 订单号精确匹配
        2. 金额+日期匹配
        3. 客人姓名+日期匹配
        4. 多笔合并匹配(团队订单拆单)
        """
        
        matches = []
        unmatched_pms = []
        unmatched_channel = list(channel_records)
        
        for pms_record in pms_records:
            best_match = None
            best_score = 0
            
            for channel_record in unmatched_channel:
                # 尝试各种匹配规则
                for rule in self.match_rules:
                    score = rule.calculate_match_score(
                        pms_record, 
                        channel_record
                    )
                    
                    if score > best_score and score >= rule.threshold:
                        best_score = score
                        best_match = channel_record
            
            if best_match:
                matches.append({
                    'pms_record': pms_record,
                    'channel_record': best_match,
                    'match_score': best_score,
                    'match_rule': rule.name
                })
                unmatched_channel.remove(best_match)
            else:
                unmatched_pms.append(pms_record)
        
        return {
            'matched': matches,
            'unmatched_pms': unmatched_pms,
            'unmatched_channel': unmatched_channel
        }
```

**匹配规则详解**
```python
class ExactMatchRule:
    """精确匹配规则"""
    
    threshold = 100
    
    def calculate_match_score(self, pms, channel):
        """
        订单号完全匹配
        金额完全匹配
        日期匹配
        """
        score = 0
        
        # 订单号匹配 (权重50%)
        if pms['order_id'] == channel['order_id']:
            score += 50
        
        # 金额匹配 (权重40%)
        if abs(pms['amount'] - channel['amount']) < 0.01:
            score += 40
        
        # 日期匹配 (权重10%)
        if pms['date'] == channel['date']:
            score += 10
        
        return score

class FuzzyMatchRule:
    """模糊匹配规则"""
    
    threshold = 70
    
    def calculate_match_score(self, pms, channel):
        """
        客人姓名相似
        日期相近(±1天)
        金额相近(±5%)
        """
        score = 0
        
        # 姓名相似度 (权重30%)
        name_similarity = self.calculate_name_similarity(
            pms['guest_name'],
            channel['guest_name']
        )
        score += name_similarity * 30
        
        # 日期差 (权重20%)
        date_diff = abs((pms['date'] - channel['date']).days)
        if date_diff <= 1:
            score += 20 * (1 - date_diff)
        
        # 金额差 (权重40%)
        amount_diff_pct = abs(pms['amount'] - channel['amount']) / pms['amount']
        if amount_diff_pct <= 0.05:
            score += 40 * (1 - amount_diff_pct / 0.05)
        
        # 房型匹配 (权重10%)
        if pms['room_type'] == channel['room_type']:
            score += 10
        
        return score
```

#### 模块3: 差异分析与根因定位

**差异类型分类**
```python
class DiscrepancyAnalyzer:
    """差异分析器"""
    
    def analyze(self, unmatched_records):
        """分析未匹配记录的原因"""
        
        discrepancy_types = {
            'timing_difference': [],  # 时间性差异
            'amount_difference': [],  # 金额差异
            'missing_record': [],     # 单边记录
            'duplicate_record': [],   # 重复记录
            'data_error': []          # 数据错误
        }
        
        for record in unmatched_records:
            discrepancy_type = self.classify_discrepancy(record)
            discrepancy_types[discrepancy_type].append(record)
        
        # 生成差异报告
        report = self.generate_report(discrepancy_types)
        
        return report
    
    def classify_discrepancy(self, record):
        """分类差异类型"""
        
        # 检查是否为时间性差异
        if self.is_timing_difference(record):
            return 'timing_difference'
        
        # 检查金额差异原因
        if record.get('amount_diff'):
            return self.analyze_amount_difference(record)
        
        # 检查是否为单边记录
        if record.get('single_side'):
            return 'missing_record'
        
        return 'data_error'
    
    def analyze_amount_difference(self, record):
        """分析金额差异原因"""
        
        pms_amount = record['pms_amount']
        channel_amount = record['channel_amount']
        diff = pms_amount - channel_amount
        
        # 可能原因:
        if abs(diff - record.get('commission', 0)) < 0.01:
            return 'commission_not_deducted'
        
        if abs(diff - record.get('promotion_discount', 0)) < 0.01:
            return 'promotion_not_recorded'
        
        if diff > 0:
            return 'room_upgrade_not_synced'
        
        return 'unknown_amount_diff'
```

**差异可视化**
```
┌─────────────────────────────────────────────────────────────┐
│ 📊 2026-03-04 对账差异分析报告                                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  📈 对账概览                                                 │
│  ┌──────────┬──────────┬──────────┬──────────┐            │
│  │ PMS订单  │ OTA账单  │ 已匹配   │ 待处理   │            │
│  │   156    │   154    │   148    │    8     │            │
│  │ ¥68,420  │ ¥67,890  │ ¥65,230  │ ¥3,190   │            │
│  └──────────┴──────────┴──────────┴──────────┘            │
│                                                             │
│  ⚠️ 差异明细 (8笔)                                           │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 类型           数量    金额      建议操作           │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │ 时间性差异      3      ¥1,230    预计明日自动匹配   │   │
│  │ 佣金差异        2      ¥890      需核实佣金比例     │   │
│  │ PMS单边        2      ¥890      需补录订单          │   │
│  │ OTA单边        1      ¥180      可能是测试订单      │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  🔍 详细差异                                                 │
│  ┌─────────────────────────────────────────────────────┐   │
│  │ 订单号      渠道    PMS金额   OTA金额   差异原因   │   │
│  ├─────────────────────────────────────────────────────┤   │
│  │ 20260304001 携程    ¥580     ¥580      时间性差异 │   │
│  │ 20260304015 美团    ¥680     ¥612      佣金差异   │   │
│  │ ...                                                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [批量处理] [导出明细] [发起复核]                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

#### 模块4: 自动核销与凭证生成

**核销流程**
```python
class AutoReconciliation:
    """自动核销处理"""
    
    def process_matches(self, matches, auto_threshold=95):
        """处理匹配记录"""
        
        auto_processed = []
        manual_review = []
        
        for match in matches:
            if match['match_score'] >= auto_threshold:
                # 自动核销
                result = self.auto_write_off(match)
                auto_processed.append(result)
            else:
                # 需要人工审核
                manual_review.append(match)
        
        return {
            'auto_processed': auto_processed,
            'manual_review': manual_review
        }
    
    def auto_write_off(self, match):
        """自动核销"""
        
        # 1. 生成会计凭证
        voucher = self.generate_voucher(match)
        
        # 2. 更新应收/实收记录
        self.update_receivable_record(match)
        
        # 3. 标记对账状态
        self.mark_as_reconciled(match)
        
        # 4. 记录审计日志
        self.log_reconciliation(match, 'auto')
        
        return {
            'status': 'success',
            'voucher_id': voucher['id'],
            'timestamp': datetime.now()
        }
    
    def generate_voucher(self, match):
        """生成会计凭证"""
        
        pms = match['pms_record']
        channel = match['channel_record']
        
        voucher = {
            'voucher_date': channel['transaction_date'],
            'entries': [
                {
                    'account': '银行存款',
                    'debit': channel['net_amount'],
                    'credit': 0,
                    'summary': f"{channel['channel']}订单{channel['order_id']}到账"
                },
                {
                    'account': '销售费用-OTA佣金',
                    'debit': channel['commission'],
                    'credit': 0,
                    'summary': f"{channel['channel']}佣金"
                },
                {
                    'account': '应收账款-OTA',
                    'debit': 0,
                    'credit': pms['amount'],
                    'summary': f"核销{channel['channel']}应收"
                }
            ]
        }
        
        return self.accounting_system.create_voucher(voucher)
```

#### 模块5: 预警监控与异常检测

**异常检测规则**
```python
class AnomalyDetector:
    """异常检测器"""
    
    def __init__(self):
        self.rules = [
            LargeAmountRule(),           # 大额交易
            FrequentRefundRule(),        # 频繁退款
            UnusualCommissionRule(),     # 佣金异常
            DuplicatePaymentRule(),      # 重复支付
            LateSettlementRule()         # 延迟结算
        ]
    
    def scan(self, transactions):
        """扫描异常交易"""
        
        anomalies = []
        
        for transaction in transactions:
            for rule in self.rules:
                if rule.check(transaction):
                    anomalies.append({
                        'transaction': transaction,
                        'rule': rule.name,
                        'severity': rule.severity,
                        'description': rule.get_description(transaction)
                    })
        
        return anomalies

class LargeAmountRule:
    """大额交易预警"""
    
    name = "大额交易"
    severity = "medium"
    
    def check(self, transaction):
        threshold = 10000  # 1万元
        return transaction['amount'] > threshold

class UnusualCommissionRule:
    """佣金率异常"""
    
    name = "佣金异常"
    severity = "high"
    
    def check(self, transaction):
        expected_commission_rate = self.get_expected_rate(
            transaction['channel']
        )
        actual_rate = transaction['commission'] / transaction['amount']
        
        # 佣金率偏差超过2%
        return abs(actual_rate - expected_commission_rate) > 0.02
```

**预警通知**
```
┌─────────────────────────────────────┐
│ 🔔 对账异常预警                      │
├─────────────────────────────────────┤
│                                     │
│  ⚠️ 发现1笔异常交易                  │
│                                     │
│  预警类型: 佣金率异常                │
│  严重程度: 🔴 高                     │
│                                     │
│  交易详情:                          │
│  ├─ 渠道: 携程                      │
│  ├─ 订单: 20260304088               │
│  ├─ 金额: ¥2,580                    │
│  ├─ 佣金: ¥516 (20%)               │
│  └─ 标准佣金率: 15%                 │
│                                     │
│  异常原因: 佣金率高于标准5%，       │
│           可能是特殊促销活动        │
│                                     │
│  建议操作:                          │
│  [核实活动政策] [确认为正常] [标记异常]│
│                                     │
└─────────────────────────────────────┘
```

---

## 4. 技术实现

### 4.1 技术栈

| 层级 | 技术选型 | 说明 |
|------|---------|------|
**数据抓取** | Python + Requests/Selenium | OTA/银行数据抓取 |
**ETL** | Apache Airflow | 数据管道编排 |
**匹配引擎** | Python + Pandas | 数据匹配处理 |
**数据库** | PostgreSQL | 交易数据存储 |
**前端** | React + Ant Design | 对账界面 |
**报表** | ECharts | 数据可视化 |

### 4.2 对账流程自动化

```
每日凌晨2:00
    ↓
自动触发对账任务
    ↓
并行抓取各数据源:
  ├─ 下载OTA账单
  ├─ 同步PMS订单
  ├─ 获取银行流水
  └─ 获取支付流水
    ↓
数据清洗与标准化
    ↓
执行匹配引擎
    ↓
生成对账结果:
  ├─ 自动核销 (匹配度>95%)
  ├─ 待审核 (匹配度70-95%)
  └─ 差异项 (未匹配)
    ↓
生成对账报告
    ↓
推送通知财务人员
    ↓
人工审核异常项 (工作时间)
```

---

## 5. 成功指标

| 指标 | 目标值 | 说明 |
|------|--------|------|
自动匹配率 | >90% | 无需人工干预比例 |
匹配准确率 | >99% | 匹配正确率 |
对账耗时 | <30分钟/天 | 人工处理时间 |
异常发现时间 | 实时 | 从发生到发现 |
月末结账周期 | <2天 | 对比传统5-7天 |

---

## 6. 实施路径

**Phase 1: 单渠道试点 (3周)**
- 选择1个主要OTA(如携程)
- 建立基础匹配规则
- 实现自动抓取

**Phase 2: 多渠道扩展 (3周)**
- 接入所有OTA渠道
- 接入银行/支付数据
- 完善匹配规则

**Phase 3: 智能化 (2周)**
- 异常检测上线
- 自动凭证生成
- 移动端审批

---

**文档版本**: v1.0 | **创建日期**: 2026-03-04
