# SKILL-PRD-011: 智能客服 (AI Guest Service Agent)

## 基本信息

| 字段 | 内容 |
|------|------|
**SKILL编号** | OPS-001
**SKILL名称** | 智能客服 (AI Guest Service Agent)
**所属AGENT** | 核心运营AGENT (Core Ops Agent)
**版本** | v1.0
**创建日期** | 2026-03-04
**优先级** | P0 (客户体验核心)
**开发周期** | 4-6周

---

## 1. 价值定位

### 1.1 解决的问题
酒店客户服务面临多重挑战：

**服务时间受限**
- 人工客服仅覆盖8-12小时，夜间服务真空
- 高峰期咨询量激增，响应延迟
- 节假日人手不足，服务质量下降

**服务一致性差**
- 不同员工回答标准不一，客人困惑
- 新员工培训周期长，服务质量参差
- 复杂问题需要转接多次，体验差

**服务成本高**
- 人力成本逐年上升
- 简单重复问题占用大量人力
- 多语言服务需要专门团队

### 1.2 核心价值
**"让每一位客人都能获得即时、专业、有温度的服务"**

- **7x24小时在线**：AI永不休息，随时响应客人需求
- **秒级响应**：平均响应时间<3秒，告别等待
- **专业一致**：标准化服务，100%执行SOP
- **多语言支持**：自动识别语言，支持20+语种
- **情绪感知**：识别客人情绪，提供共情式服务

### 1.3 量化收益

| 指标 | 传统模式 | AI智能客服 | 提升幅度 |
|------|---------|-----------|---------|
响应时间 | 5-15分钟 | <3秒 | **快100倍** |
服务可用性 | 12小时/天 | 24小时/天 | **+100%** |
问题解决率 | 70-80% | 85-92% | **+15%** |
客户满意度 | 75% | 88% | **+17%** |
客服人力成本 | 100% | 40% | **节省60%** |
多语言覆盖 | 2-3种 | 20+种 | **扩展10倍** |

---

## 2. 目标用户

### 2.1 主要用户

| 用户角色 | 使用场景 | 核心痛点 |
|---------|---------|---------|
**住店客人** | 咨询酒店服务、报修、投诉 | 找不到人、等待时间长、沟通困难 |
**潜在客人** | 预订前咨询 | 问题多、想快速得到准确答案 |
**前台员工** | 处理AI无法解决的复杂问题 | 简单问题占用大量时间 |
**客服主管** | 监控服务质量，优化流程 | 服务质量难监控，数据分散 |

### 2.2 用户画像

**典型用户：王女士，35岁，商务酒店住客**
- 晚上10点想叫客房服务，但不知道菜单
- 打电话到前台占线，等了5分钟才接通
- 想用英文咨询，但值班员工英文不好
- 希望能在微信/APP上快速得到回复

**典型用户：前台小李，前台接待员**
- 每天要接50+个电话，80%是简单咨询
- 经常同时处理多个客人，手忙脚乱
- 希望简单问题能被AI处理，自己专注复杂事务

---

## 3. 功能架构

### 3.1 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    接入层 (多渠道)                           │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ 酒店APP     │ │ 微信小程序   │ │ 酒店官网    │            │
│  │ (原生)      │ │ (H5)        │ │ (WebChat)   │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ 电话语音    │ │ 客房电视    │ │ 智能音箱    │            │
│  │ (IVR+ASR)   │ │ (遥控器)    │ │ (语音)      │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────────────────────────────────────────────────────┘
                              ↕
┌─────────────────────────────────────────────────────────────┐
│                    AI服务层 (核心)                           │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ 意图识别    │ │ 对话管理    │ │ 知识问答    │            │
│  │ (NLU)       │ │ (DST+Policy)│ │ (RAG)       │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ 任务执行    │ │ 情感分析    │ │ 多语言      │            │
│  │ (API调用)   │ │ (情绪识别)  │ │ (翻译)      │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
└─────────────────────────────────────────────────────────────┘
                              ↕
└─────────────────────────────────────────────────────────────┘
│                    支撑层                                    │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐            │
│  │ 知识库      │ │ 客人画像    │ │ 服务工单    │            │
│  │ (FAQ+SOP)   │ │ (CRM数据)   │ │ (工单系统)  │            │
│  └─────────────┘ └─────────────┘ └─────────────┘            │
│  ┌─────────────┐ ┌─────────────┐                            │
│  │ PMS集成     │ │ 数据分析    │                            │
│  │ (房态/订单) │ │ (服务质量)  │                            │
│  └─────────────┘ └─────────────┘                            │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 核心功能模块

#### 模块1: 全渠道统一接入

**支持渠道**
```yaml
数字渠道:
  - 酒店APP内嵌聊天
  - 微信小程序客服
  - 官网WebChat
  - 短信/邮件回复
  - 第三方OTA消息 (携程/美团)

语音渠道:
  - 电话IVR导航
  - 客房智能音箱
  - 机器人语音交互

线下渠道:
  - 客房电视界面
  - 大堂自助终端
  - 机器人屏幕交互
```

**渠道适配**
```python
class ChannelAdapter:
    """渠道适配器"""
    
    def adapt_message(self, message, channel_type):
        """根据渠道类型适配消息格式"""
        
        adapters = {
            'wechat': WeChatAdapter(),
            'app': AppAdapter(),
            'voice': VoiceAdapter(),
            'sms': SMSAdapter()
        }
        
        adapter = adapters.get(channel_type)
        return adapter.format(message)
    
    def extract_context(self, raw_message, channel_type):
        """提取渠道特定上下文"""
        
        context = {
            'channel': channel_type,
            'timestamp': raw_message.get('timestamp'),
            'guest_id': self.extract_guest_id(raw_message, channel_type),
            'room_number': self.extract_room_number(raw_message),
            'language': self.detect_language(raw_message)
        }
        
        return context
```

#### 模块2: 意图识别与对话管理

**意图分类体系**
```
客人意图:
├── 信息查询 (40%)
│   ├── 酒店设施查询
│   ├── 服务时间查询
│   ├── 周边信息查询
│   └── 政策查询
├── 服务请求 (35%)
│   ├── 客房服务
│   ├── 设施预订 (健身房/泳池)
│   ├── 交通安排
│   └── 物品借用
├── 问题反馈 (15%)
│   ├── 报修 (设施故障)
│   ├── 投诉 (服务不满)
│   └── 建议
├── 交易相关 (8%)
│   ├── 预订/取消
│   ├── 延住/提前离店
│   ├── 账单查询
│   └── 发票开具
└── 其他 (2%)
    ├── 闲聊
    └── 转人工
```

**意图识别模型**
```python
class IntentClassifier:
    """意图分类器"""
    
    def __init__(self):
        self.model = load_model('intent_classifier')
        self.intent_hierarchy = load_intent_tree()
    
    def classify(self, text, context):
        """多级意图分类"""
        
        # 第一层: 大类识别
        primary_intent = self.model.predict_primary(text)
        
        # 第二层: 细分类别
        if primary_intent == 'service_request':
            secondary_intent = self.model.predict_secondary(
                text, 
                parent=primary_intent
            )
        
        # 第三层: 提取实体
        entities = self.extract_entities(text)
        
        return {
            'primary_intent': primary_intent,
            'secondary_intent': secondary_intent,
            'entities': entities,
            'confidence': self.model.get_confidence(),
            'requires_clarification': self.needs_clarification()
        }
```

**对话状态追踪 (DST)**
```python
class DialogueStateTracker:
    """对话状态追踪"""
    
    def __init__(self):
        self.state = {
            'current_intent': None,
            'slots': {},  # 已填槽位
            'missing_slots': [],  # 待填槽位
            'context': [],  # 对话历史
            'guest_info': {},  # 客人信息
            'turn_count': 0
        }
    
    def update(self, user_message, system_response):
        """更新对话状态"""
        
        # 1. 解析用户消息
        intent_result = self.intent_classifier.classify(user_message)
        
        # 2. 更新意图
        if intent_result['confidence'] > 0.8:
            self.state['current_intent'] = intent_result['primary_intent']
        
        # 3. 更新槽位
        for entity in intent_result['entities']:
            self.state['slots'][entity['type']] = entity['value']
        
        # 4. 更新缺失槽位
        required_slots = self.get_required_slots(self.state['current_intent'])
        self.state['missing_slots'] = [
            slot for slot in required_slots 
            if slot not in self.state['slots']
        ]
        
        # 5. 记录对话历史
        self.state['context'].append({
            'user': user_message,
            'system': system_response
        })
        
        self.state['turn_count'] += 1
```

**对话策略 (Policy)**
```python
class DialoguePolicy:
    """对话策略决策"""
    
    def decide_action(self, state):
        """根据对话状态决定下一步动作"""
        
        # 1. 检查是否有未完成的槽位
        if state['missing_slots']:
            return {
                'action': 'ask_slot',
                'slot': state['missing_slots'][0],
                'message': self.generate_slot_question(state['missing_slots'][0])
            }
        
        # 2. 检查是否需要确认
        if not state.get('confirmed', False):
            return {
                'action': 'confirm',
                'message': self.generate_confirmation(state['slots'])
            }
        
        # 3. 执行任务
        if state['current_intent'] == 'service_request':
            return {
                'action': 'execute_service',
                'service': state['secondary_intent'],
                'parameters': state['slots']
            }
        
        elif state['current_intent'] == 'information_query':
            return {
                'action': 'retrieve_answer',
                'query': state['slots']
            }
        
        # 4. 默认回复
        return {
            'action': 'fallback',
            'message': '抱歉，我需要更多信息来帮您'
        }
```

#### 模块3: 知识库问答 (RAG)

**知识库结构**
```
知识库:
├── FAQ (常见问题)
│   ├── 入住退房政策
│   ├── 早餐时间地点
│   ├── 停车收费
│   ├── WiFi密码
│   └── 周边景点
│
├── SOP (标准流程)
│   ├── 客房服务流程
│   ├── 报修处理流程
│   ├── 投诉处理流程
│   └── 紧急情况处理
│
├── 酒店信息
│   ├── 设施介绍
│   ├── 营业时间
│   ├── 服务价格
│   └── 房型说明
│
└── 周边信息
    ├── 交通指南
    ├── 餐饮推荐
    ├── 购物娱乐
    └── 紧急服务
```

**RAG检索增强**
```python
class KnowledgeRAG:
    """知识库RAG问答"""
    
    def __init__(self):
        self.embedding_model = load_embedding_model()
        self.vector_store = load_vector_store()
        self.llm = load_llm()
    
    def answer(self, query, context):
        """回答问题"""
        
        # 1. 查询嵌入
        query_embedding = self.embedding_model.encode(query)
        
        # 2. 检索相关文档
        relevant_docs = self.vector_store.similarity_search(
            query_embedding,
            top_k=5
        )
        
        # 3. 构建Prompt
        prompt = f"""
        基于以下参考资料回答问题:
        
        参考资料:
        {chr(10).join([doc.content for doc in relevant_docs])}
        
        客人问题: {query}
        
        客人信息: {context['guest_info']}
        
        请用友好、专业的语气回答。如果资料中没有相关信息，
        请礼貌地告知需要进一步确认。
        """
        
        # 4. 生成回答
        answer = self.llm.generate(prompt)
        
        return {
            'answer': answer,
            'sources': [doc.source for doc in relevant_docs],
            'confidence': self.calculate_confidence(answer, relevant_docs)
        }
```

#### 模块4: 任务执行与工单系统

**服务任务类型**
```python
class TaskExecutor:
    """任务执行器"""
    
    def execute(self, intent, slots, guest_info):
        """执行服务任务"""
        
        task_handlers = {
            'room_service': self.handle_room_service,
            'housekeeping': self.handle_housekeeping,
            'maintenance': self.handle_maintenance,
            'wake_up_call': self.handle_wake_up_call,
            'taxi_booking': self.handle_taxi_booking,
            'facility_booking': self.handle_facility_booking
        }
        
        handler = task_handlers.get(intent)
        if handler:
            return handler(slots, guest_info)
        else:
            return self.create_manual_ticket(intent, slots, guest_info)
    
    def handle_room_service(self, slots, guest_info):
        """处理客房服务请求"""
        
        # 1. 创建工单
        ticket = {
            'type': 'room_service',
            'room_number': guest_info['room_number'],
            'guest_name': guest_info['name'],
            'items': slots.get('items', []),
            'special_requests': slots.get('special_requests', ''),
            'timestamp': datetime.now(),
            'status': 'pending'
        }
        
        # 2. 推送到餐饮系统
        result = self.room_service_api.create_order(ticket)
        
        # 3. 返回确认
        if result['success']:
            return {
                'success': True,
                'message': f'已为您下单，预计{result["eta"]}分钟送达',
                'order_id': result['order_id']
            }
        else:
            return {
                'success': False,
                'message': '下单失败，已为您转接人工服务',
                'escalate': True
            }
```

**工单流转**
```
客人请求
    ↓
AI客服理解意图
    ↓
判断处理类型:
    ├─ 自动处理 → 直接执行 → 反馈结果
    ├─ 需确认 → 人工审核 → 执行 → 反馈
    └─ 复杂问题 → 创建工单 → 分配部门 → 跟踪处理
```

#### 模块5: 情感分析与情绪管理

**情感识别**
```python
class EmotionAnalyzer:
    """情感分析器"""
    
    def analyze(self, text, context):
        """分析客人情绪状态"""
        
        # 1. 文本情感分析
        sentiment = self.sentiment_model.predict(text)
        
        # 2. 情绪分类
        emotions = self.emotion_model.predict(text)
        
        # 3. 紧急程度评估
        urgency = self.assess_urgency(text, context)
        
        return {
            'sentiment': sentiment,  # positive/neutral/negative
            'emotions': emotions,    # {angry: 0.8, frustrated: 0.6}
            'urgency': urgency,      # low/medium/high/critical
            'satisfaction_score': self.calculate_satisfaction()
        }
```

**情绪应对策略**
```python
class EmotionResponseStrategy:
    """情绪应对策略"""
    
    def get_response_strategy(self, emotion_analysis):
        """根据情绪状态选择应对策略"""
        
        urgency = emotion_analysis['urgency']
        sentiment = emotion_analysis['sentiment']
        
        if urgency == 'critical':
            return {
                'strategy': 'immediate_escalation',
                'action': '立即转接人工客服',
                'message': '非常抱歉给您带来不好的体验，我立即为您转接专属客服经理'
            }
        
        elif sentiment == 'negative' and emotion_analysis['emotions'].get('angry', 0) > 0.7:
            return {
                'strategy': 'empathy_first',
                'action': '先共情安抚，再解决问题',
                'message_template': [
                    '我完全理解您的不满，这确实让人沮丧',
                    '让我马上为您处理这个问题',
                    '作为补偿，我可以为您...'
                ]
            }
        
        elif sentiment == 'positive':
            return {
                'strategy': 'enthusiastic_service',
                'action': '热情服务，适时推荐',
                'message_template': [
                    '很高兴为您服务！',
                    '如果您需要其他帮助，随时告诉我'
                ]
            }
        
        else:
            return {
                'strategy': 'standard_service',
                'action': '标准专业服务'
            }
```

---

## 4. 技术实现

### 4.1 技术栈

| 层级 | 技术选型 | 说明 |
|------|---------|------|
**NLP** | DeepSeek-V3 / GPT-4o | 意图理解、回答生成 |
**RAG** | LangChain + Milvus | 知识检索增强 |
**对话管理** | Rasa / 自研 | 对话状态追踪 |
**语音** | ASR(讯飞) + TTS(百度) | 语音识别与合成 |
**消息推送** | WebSocket + 第三方 | 实时消息 |
**数据库** | MongoDB + Redis | 对话记录、缓存 |

### 4.2 API设计

```yaml
# 发送消息
POST /api/v1/chat/send
参数:
  channel: string (wechat/app/voice)
  guest_id: string
  message: string
  context: object
返回:
  reply: string
  intent: string
  confidence: float
  action: object (如有执行任务)

# 获取对话历史
GET /api/v1/chat/history/{guest_id}
返回:
  messages: [message_object]

# 转接人工
POST /api/v1/chat/transfer
参数:
  guest_id: string
  reason: string
  context: object
返回:
  transfer_id: string
  queue_position: int

# 知识库查询
POST /api/v1/kb/query
参数:
  query: string
  top_k: int
返回:
  answers: [answer_object]
  sources: [source_object]
```

---

## 5. 成功指标

| 指标 | 目标值 | 说明 |
|------|--------|------|
首次响应时间 | <3秒 | 客人发送消息到AI回复 |
意图识别准确率 | >90% | 正确理解客人意图 |
问题解决率 | >85% | 无需转人工独立解决 |
客户满意度 | >4.2/5 | 对话结束后评分 |
转人工率 | <15% | 需要人工介入比例 |
多语言准确率 | >85% | 非中文咨询处理 |

---

## 6. 实施路径

**Phase 1: MVP版 (4周)**
- 基础FAQ问答
- 微信公众号接入
- 简单意图识别

**Phase 2: 增强版 (4周)**
- 多轮对话管理
- RAG知识检索
- 工单系统集成

**Phase 3: 智能版 (4周)**
- 情感分析
- 多语言支持
- 语音交互

---

**文档版本**: v1.0 | **创建日期**: 2026-03-04
