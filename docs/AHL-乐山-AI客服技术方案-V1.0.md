# AHL-乐山-AI客服技术方案-V1.0

> **版本**: V1.0  
> **日期**: 2026-03-27  
> **状态**: 起草  
> **负责人**: AHL技术组

---

## 模块3：AI客服SKILL体系

### 乐山落地现状评估

#### 能不能做？—— 可行性分析

**乐山嘉州现状**：

| 维度 | 现状 | 可用性 |
|------|------|--------|
| 携程点评 | 2414条（稳定积累） | ✅ 数据充足 |
| 差评处理 | 未知（可能是人工回复） | ⚠️ 无系统 |
| 回复速度 | 未知 | ⚠️ 无监控 |
| 投诉升级 | 未知 | ❌ 无机制 |
| FAQ知识库 | 无 | ❌ 需新建 |

**为什么AI客服对乐山嘉州很重要？**

```
携程排名权重因素：
├── 点评数量（越多越好）✅ 2414条，基础不错
├── 点评分数（越高越好）⚠️ 未知，需要维护
├── 差评回复率 ⚠️ 未知，但很重要
├── 差评响应速度 ⚠️ 未知，关键指标
└── 差评处理满意度 ⚠️ 未知

携程差评对排名的杀伤力：
├── 1-2星差评直接拉低综合得分
├── 差评超过30天不回复，携程会降低权重
├── 差评回复质量影响"回复率"指标
└── 投诉升级处理不当可能被携程标记

酒店痛点：
├── 前台忙时无法及时回复
├── 夜间无值班，携程咨询无人接
├── 差评回复话术不专业
└── 不知道哪些差评需要优先处理
```

**AI客服能解决的问题**：

| 问题 | AI能做什么 | 局限性 |
|------|-----------|--------|
| 差评发现不及时 | 定时爬取携程，第一时间告警 | 需要网络访问 |
| 差评分类不准确 | NLU自动分类（服务/设施/卫生） | 复杂表达仍需人工判断 |
| 回复话术不专业 | LLM生成+模板库 | 必须人工审核 |
| 投诉升级不及时 | 关键词触发+微信通知 | 需要负责人配合 |
| FAQ重复问题 | 知识库匹配自动回复 | 需要维护知识库 |

#### 需要什么前提？

| 前提条件 | 当前状态 | 行动项 | 优先级 |
|----------|----------|--------|--------|
| 携程账号+EBK权限 | 有（推测） | 确认EBK登录方式 | P0 |
| 携程差评爬取 | 无工具 | 开发爬虫/使用API | P0 |
| 差评回复模板库 | 无 | 建立模板库 | P1 |
| 酒店负责人微信 | 无 | 收集紧急联系方式 | P0 |
| FAQ知识库 | 无 | 整理常见Q&A | P1 |
| 企微/微信通知群 | 无 | 建立预警通知群 | P1 |

---

### SKILL清单

#### SVC-001：差评预警

**规格卡**：

```
┌─────────────────────────────────────────────────────────┐
│ SKILL编号    │ SVC-001                               │
├─────────────────────────────────────────────────────────┤
│ SKILL名称    │ 差评预警与分级                        │
├─────────────────────────────────────────────────────────┤
│ 目标         │ 第一时间发现差评，自动分级并告警       │
├─────────────────────────────────────────────────────────┤
│ 输入         │ 携程酒店页面/EBK后台数据               │
│             │ - 点评列表（含星级/内容/日期）         │
│             │ - 抓取方式：网页爬虫 / EBK API         │
├─────────────────────────────────────────────────────────┤
│ 处理逻辑     │ Step1: 定时抓取（每小时/每日）        │
│             │ Step2: 新旧对比（只处理新增差评）     │
│             │ Step3: 差评分级                        │
│             │   L1（紧急）：1-2星 → 立即告警        │
│             │   L2（普通）：3星 → 当日处理          │
│             │ Step4: 自动归类                        │
│             │   服务差 / 设施差 / 卫生差 / 隔音差   │
│             │   餐饮差 / 位置差 / 其他              │
│             │ Step5: 发送告警通知                   │
├─────────────────────────────────────────────────────────┤
│ 输出         │ 差评预警卡片                          │
│             │ {                                       │
│             │   id: "ctrip_20260327_001",           │
│             │   source: "ctrip",                     │
│             │   star: 2,                            │
│             │   level: "L1",                        │
│             │   category: "服务",                    │
│             │   content: "前台态度不好...",          │
│             │   guest_name: "张**",                 │
│             │   room_type: "江景大床房",            │
│             │   check_in_date: "2026-03-20",       │
│             │   published_at: "2026-03-26 15:30",  │
│             │   replied: false,                     │
│             │   is_new: true,                       │
│             │   suggested_action: "优先处理"        │
│             │ }                                       │
├─────────────────────────────────────────────────────────┤
│ 告警通道     │ - 微信通知群（Webhook）               │
│             │ - 企微消息（指定负责人）              │
│             │ - 短信（紧急升级）                    │
├─────────────────────────────────────────────────────────┤
│ 数据依赖     │ - SQLite: ctrip_reviews.db             │
│             │ - 携程网页/EBK API                    │
│             │ - 微信Webhook                        │
├─────────────────────────────────────────────────────────┤
│ 边界/限制    │ - 抓取频率：每小时1次（避免被封）    │
│             │ - 存储周期：差评永久保留              │
│             │ - 历史差评：仅标记是否已回复          │
└─────────────────────────────────────────────────────────┘
```

**技术原理**：

```
为什么需要"分级"机制？

差评≠同等紧急：
├── 1-2星差评（愤怒/失望）：
│   └── 情绪激动，可能已在发酵
│   └── 24小时内不处理可能升级
│   └── 需要立即响应
└── 3星差评（一般不满）：
    └── 问题存在但情绪较平稳
    └── 24-48小时内处理即可
    └── 重点是解决问题而非速度

为什么需要"归类"？

差评归类帮助酒店找到问题根源：
├── 服务差 → 培训前台/改善话术
├── 设施差 → 报修/翻新预算
├── 卫生差 → 清洁SOP检查/换供应商
├── 隔音差 → 物理隔音改造/房型调整
└── 位置/周边 → 无法改变但需知悉

归类后的数据统计价值：
├── 每月差评类型分布
├── 同比/环比趋势
└── 针对问题投入资源
```

#### SVC-002：差评AI自动回复

**规格卡**：

```
┌─────────────────────────────────────────────────────────┐
│ SKILL编号    │ SVC-002                               │
├─────────────────────────────────────────────────────────┤
│ SKILL名称    │ 差评AI自动回复                        │
├─────────────────────────────────────────────────────────┤
│ 目标         │ 生成专业、个性化、有温度的差评回复   │
├─────────────────────────────────────────────────────────┤
│ 输入         │ 差评内容（SVC-001输出）               │
│             │ - 差评文本                             │
│             │ - 星级                                 │
│             │ - 入住日期                             │
│             │ - 房型                                 │
│             │ - 客人姓名（可选）                     │
├─────────────────────────────────────────────────────────┤
│ 处理流程     │ Step1: NLU分析差评类型                │
│             │ Step2: 选择回复模板                    │
│             │ Step3: LLM生成个性化内容               │
│             │ Step4: 人工审核（必须）               │
│             │ Step5: 发布回复                       │
├─────────────────────────────────────────────────────────┤
│ 回复策略     │ 服务差：                              │
│             │ "亲爱的...感谢您入住并抽出宝贵时间反馈  │
│             │ ...我们高度重视您提到的服务问题...     │
│             │ 已对相关同事进行培训...               │
│             │ 期待您再次光临，为您提供更优质服务"    │
│             │                                          │
│             │ 设施差：                              │
│             │ "亲爱的...感谢您的入住与反馈...        │
│             │ 您提到的设施问题我们已记录...          │
│             │ 已安排工程部检查维修...               │
│             │ 下次入住我们可为您免费升级房型"       │
│             │                                          │
│             │ 卫生差：                              │
│             │ "亲爱的...对您造成的不愉快深表歉意...  │
│             │ 我们已对房间进行深度清洁...          │
│             │ 感谢您帮助我们发现问题...            │
│             │ 下次入住享受免费清洁服务"              │
├─────────────────────────────────────────────────────────┤
│ 输出         │ 回复草稿（待审核）                    │
│             │ 回复记录（已发布/已放弃）             │
├─────────────────────────────────────────────────────────┤
│ 质量控制     │ ⚠️ 必须人工审核后才能发布             │
│             │ 回复长度：50-150字                    │
│             │ 禁止出现：反驳客人/推卸责任/攻击性语言│
│             │ 必须包含：感谢+承认问题+改善承诺       │
├─────────────────────────────────────────────────────────┤
│ 数据依赖     │ - 差评数据库（SVC-001）               │
│             │ - 回复模板库                          │
│             │ - LLM API（Kimi/DeepSeek）            │
│             │ - 携程EBK回复接口                    │
├─────────────────────────────────────────────────────────┤
│ 边界/限制    │ - 同一差评最多生成3版草稿            │
│             │ - 超过3天未回复的差评不生成（超时）  │
│             │ - 涉及人身攻击/违法的差评跳过        │
└─────────────────────────────────────────────────────────┘
```

**技术原理**：

```
为什么差评回复必须人工审核？

AI回复的风险：
├── 可能暴露酒店内部信息
├── 可能说错话（如承诺不存在的服务）
├── 可能语气不当（过于官方/过于随意）
├── 可能被客人截图二次传播
└── 一旦发出去无法撤回

人工审核的价值：
├── 审核回复内容的准确性
├── 调整语气以匹配酒店风格
├── 添加个性化元素（如客人特殊纪念日）
├── 把控敏感信息不泄露
└── 最终责任由人承担（非AI）

为什么用LLM而不是纯模板？

纯模板的问题：
├── 机械感强，客人能看出是模板
├── 无法处理复杂/混合投诉
├── 缺乏灵活性
└── 容易出现"答非所问"

LLM+模板的优势：
├── 保留模板的结构（感谢+承认+承诺）
├── LLM填充个性化内容（具体问题具体分析）
├── 语言自然流畅
└── 可以学习酒店的说话风格
```

#### SVC-003：投诉升级处理

**规格卡**：

```
┌─────────────────────────────────────────────────────────┐
│ SKILL编号    │ SVC-003                               │
├─────────────────────────────────────────────────────────┤
│ SKILL名称    │ 投诉升级处理                          │
├─────────────────────────────────────────────────────────┤
│ 目标         │ 识别高风险投诉，自动升级通知负责人    │
├─────────────────────────────────────────────────────────┤
│ 触发条件     │ 满足以下任一条件即触发：             │
│             │ 条件1：连续2条及以上差评（7天内）      │
│             │ 条件2：提及关键词                      │
│             │   - "投诉" / "举报" / "媒体"          │
│             │   - "退款" / "赔偿" / "索赔"          │
│             │   - "12315" / "消协" / "曝光"        │
│             │   - "律师" / "法院" / "起诉"         │
│             │ 条件3：单条差评超过500字（详细投诉）  │
│             │ 条件4：提及具体金额索赔                │
├─────────────────────────────────────────────────────────┤
│ 处理流程     │ Step1: 触发升级检测                   │
│             │ Step2: 生成预警报告                    │
│             │   - 投诉内容摘要                       │
│             │   - 历史入住记录（是否有异常）        │
│             │   - 历史投诉记录（是否有多次）        │
│             │   - 建议处理方案                       │
│             │ Step3: 立即通知（优先级最高）        │
│             │   - 微信通知群（@所有人）             │
│             │   - 企微私发负责人                    │
│             │   - 短信（紧急）                       │
│             │ Step4: 记录升级日志                    │
│             │ Step5: 跟踪处理结果                   │
├─────────────────────────────────────────────────────────┤
│ 输出         │ 升级预警通知                          │
│             │ {                                       │
│             │   id: "escalation_001",               │
│             │   level: "HIGH",                      │
│             │   trigger: "连续差评/关键词/超额索赔",│
│             │   reviews: [差评列表],                │
│             │   guest_history: {                    │
│             │     total_stays: 3,                  │
│             │     avg_rate: 450,                   │
│             │     previous_complaints: 1,          │
│             │     vip_level: "B"                   │
│             │   },                                  │
│             │   suggested_actions: [               │
│             │     "立即联系客人道歉",              │
│             │     "了解详细情况",                  │
│             │     "准备补偿方案",                  │
│             │     "必要时升级至总经理"            │
│             │   ],                                  │
│             │   notified_to: ["前台主管", "店长"], │
│             │   created_at: "2026-03-27 10:00"    │
│             │ }                                       │
├─────────────────────────────────────────────────────────┤
│ 通知通道     │ - 微信群（预警通知）                 │
│             │ - 企微私聊（指定负责人）             │
│             │ - 短信（紧急升级）                   │
├─────────────────────────────────────────────────────────┤
│ 升级路径     │ L1告警 → 前台主管                    │
│             │ L2升级 → 店长/总经理                  │
│             │ L3危机 → 集团总部/法务               │
├─────────────────────────────────────────────────────────┤
│ 数据依赖     │ - 差评数据库（SVC-001）               │
│             │ - 入住历史（guest_private.db）       │
│             │ - 会员等级（PRIV-003）                │
│             │ - 微信Webhook                        │
└─────────────────────────────────────────────────────────┘
```

**技术原理**：

```
为什么需要升级机制？

前台处理的局限性：
├── 权限不够：无法承诺超出政策的赔偿
├── 信息不足：不知道客人的历史背景
├── 经验不足：不知道何时该上报
└── 时间不够：忙于其他工作

升级机制的价值：
├── 确保重大投诉不被延误
├── 借助更高权限和经验处理
├── 保护酒店（留下处理记录）
└── 客人感受被重视

关键词触发的原理：

语义分析比关键词更准确，但关键词是快速可靠的兜底：
├── "退款"：即使语义温和，也可能有风险
├── "投诉"：明确的升级信号
├── "12315"：涉及监管机构
├── "律师"：法律风险
└── 注意：需要处理否定句（如"不投诉"）

连续差评的识别：
├── 不是简单的计数
├── 需要去重（同一人多次投诉算一次）
├── 需要时间窗口（7天内的才关联）
└── 需要结合客人价值（VIP连续差评更危险）
```

#### SVC-004：FAQ自动回复

**规格卡**：

```
┌─────────────────────────────────────────────────────────┐
│ SKILL编号    │ SVC-004                               │
├─────────────────────────────────────────────────────────┤
│ SKILL名称    │ 常见问题自动回复（FAQ Bot）           │
├─────────────────────────────────────────────────────────┤
│ 目标         │ 7x24自动回答常见问题，减轻前台负担   │
├─────────────────────────────────────────────────────────┤
│ 输入         │ 用户提问（微信群/携程问答区）         │
│             │ 触发方式：                             │
│             │ - 关键词匹配（快速）                   │
│             │ - 语义相似度匹配（精确）               │
├─────────────────────────────────────────────────────────┤
│ 覆盖场景     │ 基础信息类：                          │
│             │ Q: 酒店电话 → A: 0833-2096666         │
│             │ Q: 地址/在哪 → A: 乐山市白塔街85号    │
│             │ Q: 入住时间 → A: 14:00后              │
│             │ Q: 退房时间 → A: 14:00前              │
│             │ Q: 停车 → A: 免费停车+充电桩          │
│             │ Q: WiFi → A: 房间密码88888888         │
│             │                                          │
│             │ 预订相关类：                           │
│             │ Q: 取消政策 → A: 当天18:00前免费取消  │
│             │ Q: 早餐 → A: 07:00-10:00，68元/位    │
│             │ Q: 接站/接机 → A: 可付费预约...      │
│             │                                          │
│             │ 特色服务类：                           │
│             │ Q: 宠物 → A: 免费携带，请提前联系     │
│             │ Q: 江景 → A: 推荐江景房...           │
│             │ Q: 早餐 → A: 1楼餐厅，07:00-10:00   │
│             │ Q: 周边景点 → A: 乐山大佛/峨眉山... │
├─────────────────────────────────────────────────────────┤
│ 技术实现     │ 知识库格式：                          │
│             │ [                                       │
│             │   {                                     │
│             │     "id": "FAQ001",                   │
│             │     "keywords": ["电话", "联系", "号码"],│
│             │     "question": "酒店联系电话多少？",  │
│             │     "answer": "📞 酒店电话：0833-2096666",│
│             │     "category": "基础信息",             │
│             │     "confidence": 0.9,                 │
│             │     "active": true                      │
│             │   }                                     │
│             │ ]                                      │
│             │                                          │
│             │ 匹配算法：                             │
│             │ 1. 关键词精确匹配（高优先级）          │
│             │ 2. 关键词模糊匹配（包含任一关键词）    │
│             │ 3. 语义相似度（question embedding）   │
│             │ 4. LLM兜底（理解意图后生成回答）      │
├─────────────────────────────────────────────────────────┤
│ 输出         │ 自动回复内容                          │
│             │ 回复后追加："如有其他问题欢迎随时咨询" │
├─────────────────────────────────────────────────────────┤
│ 质量控制     │ 单一问题匹配单一答案（避免混乱）      │
│             │ 知识库定期更新（季节性内容）           │
│             │ 无法回答时转人工                       │
├─────────────────────────────────────────────────────────┤
│ 数据依赖     │ - FAQ知识库（JSON/Markdown）          │
│             │ - 语义匹配模型（可选）                 │
│             │ - LLM API（可选，用于复杂问题）       │
├─────────────────────────────────────────────────────────┤
│ 边界/限制    │ 单次回复不超过3条FAQ                 │
│             │ 5分钟内相同问题不重复回复             │
│             │ 涉及预订/支付的问题不自动处理         │
└─────────────────────────────────────────────────────────┘
```

**技术原理**：

```
FAQ Bot的定位：
├── 不是智能客服（不处理复杂问题）
├── 是快捷工具（快速响应高频问题）
└── 是前台助手（减少重复回答）

为什么不用LLM直接回答？

纯LLM的问题：
├── 可能胡编乱造（如编一个不存在的政策）
├── 无法保证信息准确性
├── 消耗大量token
└── 响应速度慢

知识库+关键词的优势：
├── 答案可控（都在知识库里）
├── 响应快（毫秒级）
├── 准确率高（基于固定答案）
└── 易于维护（更新知识库即可）

语义匹配的作用：

关键词匹配的局限：
├── 用户问："你们家的电话号码是？" → 匹配"电话" ✅
├── 用户问："怎么联系你们啊？" → 匹配"联系" ✅
├── 用户问："有座机吗？" → 不匹配"电话" ❌

语义匹配能处理：
├── 用户说："有座机吗？" → embedding相似 → 匹配"电话" ✅
└── 即使关键词不完全匹配，也能识别意图
```

---

### 技术实现路径

#### Phase 1：差评监控+基础FAQ（1-2周落地）

```
目标：解决差评发现不及时、FAQ重复回答的问题

工具栈：
├── 携程差评爬虫：定时抓取新差评
├── 微信通知：Webhook推送告警
├── FAQ知识库：本地JSON
├── 差评模板库：回复模板

工作流：
[定时抓取携程差评] → [检测新增差评] → [分级+归类]
    → [微信通知负责人] → [人工处理]

[用户提问] → [FAQ知识库匹配] → [自动回复]

预计完成时间：1-2周
预计成本：爬虫开发（约1万元）
```

#### Phase 2：AI回复+投诉升级（1个月后）

```
目标：减少人工回复工作量，建立投诉升级机制

新增能力：
├── LLM生成差评回复（人工审核后发布）
├── 投诉关键词实时监控
├── 客人历史记录关联
├── 差评处理SOP跟踪

工作流变化：
[新增差评] → [LLM生成回复草稿] → [人工审核] → [发布]
                                                      ↓
[触发升级条件] → [自动通知负责人] → [处理记录跟踪]

预计完成时间：1个月
预计成本：LLM API + 开发（约2-3万元）
```

#### Phase 3：全流程AI客服闭环（2-3个月后）

```
目标：7x24 AI客服，覆盖售前售后全流程

完整功能：
├── 售前咨询：AI自动回答预订问题
├── 预订确认：AI+人工协作完成预订
├── 在店服务：AI处理客房服务请求
├── 离店关怀：AI发送离店问卷
├── 差评管理：AI监控+生成回复+升级处理
├── 投诉处理：AI识别+自动升级+SOP跟踪

预计完成时间：2-3个月
预计成本：系统开发+维护（约5-10万元/年）
```

---

### 关键代码框架

#### SVC-001：差评预警

```python
# -*- coding: utf-8 -*-
"""
SVC-001: 差评预警与分级
功能：定时抓取携程差评，自动分级归类并告警
Phase: 1（爬虫+规则引擎）
"""

import sqlite3
import json
import re
import time
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
import requests
from bs4 import BeautifulSoup

# ============================================================
# 配置区
# ============================================================

DB_PATH = "data/ctrip_reviews.db"

# 携程酒店页面（需替换为实际酒店ID）
CTRIP_HOTEL_ID = "XXXXXX"
CTRIP_BASE_URL = f"https://www.ctrip.com/hotel/{CTRIP_HOTEL_ID}.html"

# 抓取配置
FETCH_INTERVAL_MINUTES = 60  # 每小时抓取一次
MAX_REVIEWS_PER_FETCH = 50   # 每次最多处理50条

# 差评等级阈值
STAR_THRESHOLD_L1 = 2   # 1-2星 = L1紧急
STAR_THRESHOLD_L2 = 3   # 3星 = L2普通

# 告警配置
WECHAT_WEBHOOK_URL = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=YOUR_KEY"
NOTIFY_LEVELS = ["L1", "L2"]

# ============================================================
# 数据模型
# ============================================================

@dataclass
class Review:
    """点评数据模型"""
    id: str  # 携程点评ID
    source: str  # ctrip/meituan
    star: int  # 星级 1-5
    level: str  # L1/L2
    category: str  # 服务/设施/卫生/其他
    content: str  # 点评内容
    guest_name: str  # 客人昵称
    room_type: str  # 入住房型
    check_in_date: str  # 入住日期
    published_at: str  # 发布时间
    replied: bool  # 是否已回复
    replied_at: Optional[str]  # 回复时间
    reply_content: Optional[str]  # 回复内容
    is_new: bool  # 是否新增
    fetched_at: str  # 抓取时间
    
    def to_dict(self) -> Dict:
        return asdict(self)


class CtripReviewCrawler:
    """
    携程点评爬虫
    
    注意：携程有反爬机制，Phase 1建议：
    1. 使用携程EBK后台导出
    2. 或使用已登录Cookie爬取
    3. 避免高频率请求
    """
    
    def __init__(self, hotel_id: str):
        self.hotel_id = hotel_id
        self.session = requests.Session()
        
        # 设置UA
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def fetch_reviews(self, page: int = 1, page_size: int = 20) -> List[Dict]:
        """
        抓取点评列表
        
        Phase 1替代方案：
        携程EBK后台 → 数据导出 → CSV导入
        
        这里提供API版本作为参考
        """
        # 实际部署时使用EBK导出或已登录Cookie
        # 这里模拟返回结构
        
        # 模拟数据
        mock_reviews = [
            {
                "id": "review_20260327_001",
                "star": 2,
                "content": "前台服务态度很差，办理入住等了很久，也没有解释。房间设施老旧，空调声音很大。",
                "guest_name": "张**",
                "room_type": "江景大床房",
                "check_in_date": "2026-03-20",
                "published_at": "2026-03-26 15:30:00"
            },
            {
                "id": "review_20260327_002",
                "star": 3,
                "content": "位置不错，但是隔音效果一般，晚上能听到走廊的声音。早餐种类偏少。",
                "guest_name": "李**",
                "room_type": "城景双床房",
                "check_in_date": "2026-03-18",
                "published_at": "2026-03-25 10:20:00"
            },
            {
                "id": "review_20260326_001",
                "star": 5,
                "content": "非常满意！江景超美，前台小姐姐服务热情，下次还来！",
                "guest_name": "王**",
                "room_type": "江景套房",
                "check_in_date": "2026-03-15",
                "published_at": "2026-03-20 18:00:00"
            }
        ]
        
        return mock_reviews
    
    def parse_review(self, raw_review: Dict) -> Review:
        """解析单条点评"""
        return Review(
            id=raw_review.get("id", ""),
            source="ctrip",
            star=int(raw_review.get("star", 3)),
            level=self._classify_level(raw_review.get("star", 3)),
            category=self._classify_category(raw_review.get("content", "")),
            content=raw_review.get("content", ""),
            guest_name=raw_review.get("guest_name", ""),
            room_type=raw_review.get("room_type", ""),
            check_in_date=raw_review.get("check_in_date", ""),
            published_at=raw_review.get("published_at", ""),
            replied=False,
            replied_at=None,
            reply_content=None,
            is_new=True,
            fetched_at=datetime.now().isoformat()
        )
    
    def _classify_level(self, star: int) -> str:
        """差评分级"""
        if star <= STAR_THRESHOLD_L1:
            return "L1"
        elif star <= STAR_THRESHOLD_L2:
            return "L2"
        else:
            return "NORMAL"
    
    def _classify_category(self, content: str) -> str:
        """差评归类"""
        content_lower = content.lower()
        
        # 关键词映射
        category_keywords = {
            "服务": ["服务", "态度", "前台", "服务员", "不热情", "冷脸", "不耐烦"],
            "设施": ["设施", "空调", "电视", "家具", "老旧", "坏了", "不能用"],
            "卫生": ["卫生", "脏", "不干净", "有异味", "异味", "灰尘"],
            "隔音": ["隔音", "吵", "噪音", "声音大", "吵醒"],
            "餐饮": ["早餐", "餐厅", "食物", "难吃", "品种少"],
            "位置": ["位置", "周边", "偏僻", "不方便"]
        }
        
        # 统计各类别关键词命中次数
        category_scores = {}
        for category, keywords in category_keywords.items():
            score = sum(1 for kw in keywords if kw in content_lower)
            category_scores[category] = score
        
        # 返回得分最高的类别
        if max(category_scores.values()) > 0:
            return max(category_scores, key=category_scores.get)
        
        return "其他"
    
    def generate_id(self, content: str, published_at: str) -> str:
        """生成点评唯一ID"""
        raw = f"{content[:50]}_{published_at}"
        return hashlib.md5(raw.encode()).hexdigest()[:16]


class ReviewMonitor:
    """差评监控器"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.init_tables()
    
    def init_tables(self):
        """初始化数据库表"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id TEXT PRIMARY KEY,
                source TEXT,
                star INTEGER,
                level TEXT,
                category TEXT,
                content TEXT,
                guest_name TEXT,
                room_type TEXT,
                check_in_date TEXT,
                published_at TEXT,
                replied INTEGER DEFAULT 0,
                replied_at TEXT,
                reply_content TEXT,
                is_new INTEGER DEFAULT 1,
                fetched_at TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS review_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                review_id TEXT,
                level TEXT,
                notified_at TEXT,
                notified_to TEXT,
                status TEXT DEFAULT 'pending',
                result TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS fetch_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fetched_at TEXT,
                total_count INTEGER,
                new_count INTEGER,
                l1_count INTEGER,
                l2_count INTEGER,
                status TEXT,
                error TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        self.conn.commit()
    
    def save_review(self, review: Review) -> bool:
        """保存点评（如果不存在）"""
        cursor = self.conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR IGNORE INTO reviews 
                (id, source, star, level, category, content, guest_name, 
                 room_type, check_in_date, published_at, replied, fetched_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                review.id, review.source, review.star, review.level,
                review.category, review.content, review.guest_name,
                review.room_type, review.check_in_date, review.published_at,
                0 if review.is_new else review.replied,
                review.fetched_at
            ))
            
            self.conn.commit()
            return cursor.rowcount > 0  # 返回是否是新插入
        
        except Exception as e:
            print(f"保存点评失败: {e}")
            return False
    
    def get_new_bad_reviews(self, days: int = 7) -> List[Review]:
        """获取新增差评"""
        cursor = self.conn.cursor()
        
        since_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT id, source, star, level, category, content, guest_name,
                   room_type, check_in_date, published_at, replied, replied_at,
                   reply_content, is_new, fetched_at
            FROM reviews
            WHERE is_new = 1
            AND star <= ?
            AND published_at >= ?
            ORDER BY published_at DESC
        ''', (STAR_THRESHOLD_L2, since_date))
        
        rows = cursor.fetchall()
        
        reviews = []
        for row in rows:
            reviews.append(Review(
                id=row[0], source=row[1], star=row[2], level=row[3],
                category=row[4], content=row[5], guest_name=row[6],
                room_type=row[7], check_in_date=row[8], published_at=row[9],
                replied=bool(row[10]), replied_at=row[11], reply_content=row[12],
                is_new=bool(row[13]), fetched_at=row[14]
            ))
        
        return reviews
    
    def mark_review_replied(self, review_id: str, reply_content: str):
        """标记已回复"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            UPDATE reviews
            SET replied = 1, replied_at = ?, reply_content = ?, is_new = 0
            WHERE id = ?
        ''', (datetime.now().isoformat(), reply_content, review_id))
        
        self.conn.commit()


class AlertNotifier:
    """告警通知器"""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    def send_review_alert(self, review: Review) -> bool:
        """发送差评告警"""
        if review.level not in NOTIFY_LEVELS:
            return False
        
        # 构建告警消息
        level_emoji = "🔴" if review.level == "L1" else "🟡"
        
        message = {
            "msgtype": "markdown",
            "markdown": {
                "content": f"""## {level_emoji} 携程差评预警 [{review.level}级]

**客人**: {review.guest_name}
**入住**: {review.room_type}（{review.check_in_date}）
**星级**: {"⭐" * review.star}{"☆" * (5 - review.star)}
**类型**: {review.category}

**差评内容**:
{review.content[:200]}{"..." if len(review.content) > 200 else ""}

**发布时间**: {review.published_at}
**处理建议**: {'立即联系客人道歉' if review.level == 'L1' else '今日内处理'}
"""
            }
        }
        
        # 实际发送（Phase 1先打印）
        print("=" * 60)
        print(f"【差评告警】{review.level}级")
        print(f"客人: {review.guest_name}")
        print(f"内容: {review.content[:100]}...")
        print(f"建议: {'立即处理' if review.level == 'L1' else '今日处理'}")
        print("=" * 60)
        
        # 实际发送时启用
        # return self._send_webhook(message)
        
        return True
    
    def send_batch_alert(self, reviews: List[Review]) -> Dict:
        """批量发送告警"""
        results = {"L1": 0, "L2": 0, "sent": 0}
        
        for review in reviews:
            if self.send_review_alert(review):
                results[review.level] = results.get(review.level, 0) + 1
                results["sent"] += 1
        
        return results
    
    def _send_webhook(self, message: Dict) -> bool:
        """发送Webhook"""
        try:
            resp = requests.post(
                self.webhook_url,
                json=message,
                timeout=10
            )
            return resp.status_code == 200
        except Exception as e:
            print(f"Webhook发送失败: {e}")
            return False


def run_review_monitor():
    """运行差评监控主流程"""
    print("=" * 60)
    print("SVC-001: 差评预警系统")
    print("=" * 60)
    
    # 初始化
    monitor = ReviewMonitor(DB_PATH)
    crawler = CtripReviewCrawler(CTRIP_HOTEL_ID)
    notifier = AlertNotifier(WECHAT_WEBHOOK_URL)
    
    # Step 1: 抓取点评
    print("\n📡 Step 1: 抓取携程最新点评...")
    raw_reviews = crawler.fetch_reviews()
    print(f"   抓取到 {len(raw_reviews)} 条点评")
    
    # Step 2: 解析并保存
    print("\n💾 Step 2: 解析并保存...")
    new_count = 0
    l1_count = 0
    l2_count = 0
    new_reviews = []
    
    for raw in raw_reviews:
        review = crawler.parse_review(raw)
        review.id = crawler.generate_id(raw.get("content", ""), raw.get("published_at", ""))
        
        if monitor.save_review(review):
            new_count += 1
            new_reviews.append(review)
            
            if review.level == "L1":
                l1_count += 1
            elif review.level == "L2":
                l2_count += 1
    
    print(f"   新增 {new_count} 条（L1: {l1_count}, L2: {l2_count}）")
    
    # Step 3: 发送告警
    print("\n🔔 Step 3: 发送告警...")
    if new_reviews:
        # 先显示待处理差评
        print("\n新增差评列表:")
        for r in new_reviews:
            level_emoji = "🔴" if r.level == "L1" else "🟡"
            print(f"  {level_emoji} [{r.level}] {r.guest_name}: {r.content[:50]}...")
        
        # 发送告警
        alert_results = notifier.send_batch_alert(new_reviews)
        print(f"\n告警发送结果: L1={alert_results.get('L1', 0)}, L2={alert_results.get('L2', 0)}")
    else:
        print("   无新增差评")
    
    print("\n✅ 监控完成")
    
    return {
        "total_fetched": len(raw_reviews),
        "new_count": new_count,
        "l1_count": l1_count,
        "l2_count": l2_count
    }


# ============================================================
# 主程序
# ============================================================

if __name__ == "__main__":
    result = run_review_monitor()
    
    print("\n" + "=" * 60)
    print("Phase 1 部署建议:")
    print("=" * 60)
    print("""
1. 携程差评获取方案选择：
   方案A（推荐）：联系携程BD，开通EBK数据导出功能
   方案B：手动导出Excel，定时导入
   方案C：爬虫（容易被封，不推荐）

2. 部署定时任务：
   - Linux/Mac: crontab -e
     */60 * * * * python3 svc_001_review_monitor.py
   - Windows: 任务计划程序

3. 微信通知配置：
   - 企业微信群机器人 Webhook
   - 或使用个人微信（通过server酱等转发）

4. 后续优化：
   - LLM分析差评情感倾向
   - 历史投诉关联分析
   - 差评趋势统计
    """)
```

#### SVC-002：差评AI自动回复

```python
# -*- coding: utf-8 -*-
"""
SVC-002: 差评AI自动回复
功能：基于LLM生成差评回复草稿（人工审核后发布）
Phase: 1-2（模板+LLM）
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional
from dataclasses import dataclass, asdict

# ============================================================
# 配置区
# ============================================================

DB_PATH = "data/ctrip_reviews.db"
TEMPLATE_PATH = "data/reply_templates.json"

# LLM API配置
LLM_API_URL = "https://api.deepseek.com/v1/chat/completions"
LLM_API_KEY = "YOUR_API_KEY"
LLM_MODEL = "deepseek-chat"

# 回复模板
REPLY_TEMPLATES = {
    "服务": {
        "keywords": ["服务", "态度", "前台", "冷", "不耐烦", "不理"],
        "template": """亲爱的{guest_name}您好：

感谢您抽出宝贵时间分享入住体验，对于给您造成的不愉快，我们深表歉意。

您提到的{issue_summary}问题，我们高度重视。{specific_apology}

您反馈的问题已转达给相关部门，我们会对{issue_area}进行专项培训和改进，确保类似情况不再发生。

为了表达我们的诚意，如您下次入住，我们为您准备了一份小礼物，请到店时联系前台领取。

再次感谢您帮助我们改进，期待有机会为您奉上更优质的服务。

祝好！
嘉州宾馆团队"""
    },
    
    "设施": {
        "keywords": ["设施", "空调", "电视", "坏了", "旧", "不能用"],
        "template": """亲爱的{guest_name}您好：

感谢您选择嘉州宾馆并分享真实反馈，对于{issue_summary}给您带来的不便，我们深表歉意。

关于{issue_area}的问题，{specific_explanation}

我们已将此问题记录在案，并已安排工程部门进行{'全面检查' if '空调' in issue_area else '维修维护'}。目前{'已完成维护' if True else '正在处理中'}。

作为补偿，您下次入住时我们将提供{'免费房型升级' if True else '相应折扣'}。

再次感谢您的理解与支持！

嘉州宾馆团队"""
    },
    
    "卫生": {
        "keywords": ["卫生", "脏", "不干净", "异味", "灰尘"],
        "template": """亲爱的{guest_name}您好：

非常抱歉给您留下了不愉快的入住体验，感谢您如实反馈。

关于{issue_summary}的问题，我们深感抱歉。{specific_apology}

您反馈的问题已引起管理层高度重视，我们已对房间进行{'深度清洁' if True else '全面打扫'}，并对清洁流程进行了更严格的规定。

为了感谢您的宝贵意见，下次入住我们将提供{'免费清洁服务' if True else '适当折扣'}。

期待您的再次光临，我们会做得更好！

嘉州宾馆团队"""
    },
    
    "隔音": {
        "keywords": ["隔音", "吵", "噪音", "声音大"],
        "template": """亲爱的{guest_name}您好：

感谢您的入住与反馈，对于{issue_summary}给您带来的困扰，我们深表歉意。

关于隔音问题，{specific_explanation}

我们已经{improvement_plan}，{'并在客房门窗加装了密封条以减少走廊噪音' if True else '将持续关注并改善'}

作为补偿，下次入住我们可为您安排{alternative_room}，或提供适当折扣。

感谢您的理解！

嘉州宾馆团队"""
    },
    
    "其他": {
        "keywords": [],
        "template": """亲爱的{guest_name}您好：

感谢您选择嘉州宾馆并分享入住体验。

对于{issue_summary}给您带来的不便，我们深表歉意。

我们已将您的反馈转达给相关部门，会认真对待并持续改进。

期待有机会为您奉上更好的服务！

嘉州宾馆团队"""
    }
}

# ============================================================
# 数据模型
# ============================================================

@dataclass
class ReviewReplyDraft:
    """回复草稿"""
    review_id: str
    template_used: str
    draft_content: str
    keywords_matched: List[str]
    generated_at: str
    reviewed: bool = False
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[str] = None
    final_content: Optional[str] = None
    status: str = "draft"  # draft/reviewed/approved/rejected/posted
    notes: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)


class ReviewReplyGenerator:
    """差评回复生成器"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
    
    def extract_issue_keywords(self, content: str) -> List[str]:
        """提取差评中的问题关键词"""
        issues = []
        
        issue_patterns = {
            "服务态度差": ["态度", "服务差", "不理", "冷", "不耐烦"],
            "入住等待": ["等很久", "等了", "等待", "办理慢"],
            "空调问题": ["空调", "不制冷", "太热", "太冷"],
            "房间老旧": ["老旧", "旧", "破", "设施差"],
            "隔音差": ["隔音", "太吵", "噪音", "吵"],
            "卫生差": ["脏", "不干净", "异味", "有灰"],
            "早餐不满意": ["早餐", "难吃", "品种少"]
        }
        
        content_lower = content.lower()
        
        for issue, keywords in issue_patterns.items():
            if any(kw in content_lower for kw in keywords):
                issues.append(issue)
        
        return issues if issues else ["综合不满"]
    
    def generate_issue_summary(self, content: str, issues: List[str]) -> str:
        """生成问题摘要"""
        if len(issues) == 1:
            return issues[0]
        elif len(issues) == 2:
            return f"{issues[0]}和{issues[1]}"
        else:
            return f"{issues[0]}等多项问题"
    
    def select_template(self, category: str) -> Dict:
        """选择回复模板"""
        # 精确匹配
        if category in REPLY_TEMPLATES:
            return {
                "type": category,
                "template": REPLY_TEMPLATES[category]["template"]
            }
        
        # 模糊匹配
        category_keywords = {
            "服务": ["服务", "态度", "前台"],
            "设施": ["设施", "空调", "电视"],
            "卫生": ["卫生", "脏", "干净"],
            "隔音": ["隔音", "吵", "噪音"]
        }
        
        for cat, keywords in category_keywords.items():
            if any(kw in category for kw in keywords):
                return {
                    "type": cat,
                    "template": REPLY_TEMPLATES[cat]["template"]
                }
        
        return {
            "type": "其他",
            "template": REPLY_TEMPLATES["其他"]["template"]
        }
    
    def generate_reply_draft(self, review_id: str, review_content: str, 
                           category: str, guest_name: str,
                           room_type: str = "") -> ReviewReplyDraft:
        """
        生成回复草稿
        
        Phase 1: 纯模板填充
        Phase 2: LLM优化内容
        """
        # 提取问题关键词
        issues = self.extract_issue_keywords(review_content)
        issue_summary = self.generate_issue_summary(review_content, issues)
        
        # 选择模板
        template_info = self.select_template(category)
        template_type = template_info["type"]
        template = template_info["template"]
        
        # 填充模板变量
        placeholders = {
            "guest_name": guest_name or "客人",
            "issue_summary": issue_summary,
            "issue_area": issues[0] if issues else "相关",
            "specific_apology": self._get_apology(category),
            "specific_explanation": self._get_explanation(category),
            "improvement_plan": "正在进行客房隔音改造",
            "alternative_room": "远离噪音区域的房型",
            "room_type": room_type
        }
        
        # 替换占位符
        draft_content = template
        for key, value in placeholders.items():
            draft_content = draft_content.replace(f"{{{key}}}", value)
        
        # Phase 2: LLM优化（预留）
        # draft_content = self._llm_refine(draft_content, review_content)
        
        return ReviewReplyDraft(
            review_id=review_id,
            template_used=template_type,
            draft_content=draft_content,
            keywords_matched=issues,
            generated_at=datetime.now().isoformat(),
            status="draft"
        )
    
    def _get_apology(self, category: str) -> str:
        """根据类别生成道歉语句"""
        apologies = {
            "服务": "针对您遇到的前台服务问题，我们诚挚道歉，会加强对员工的培训。",
            "设施": "给您带来的不便，我们深感抱歉。",
            "卫生": "清洁工作是酒店的基础，我们对此失职深感抱歉。",
            "隔音": "隔音问题确实影响入住体验，我们深表歉意。",
            "其他": "感谢您的反馈，我们会持续改进。"
        }
        return apologies.get(category, apologies["其他"])
    
    def _get_explanation(self, category: str) -> str:
        """根据类别生成解释"""
        explanations = {
            "服务": "我们已对当班人员进行了约谈，强调服务标准。",
            "设施": "我们已安排工程部检查维修，将尽快恢复正常使用。",
            "卫生": "我们已对客房进行深度清洁，并加强检查频次。",
            "隔音": "隔音问题受限于建筑结构，但我们已采取加装密封条等措施。",
            "其他": "我们会认真对待每一条反馈。"
        }
        return explanations.get(category, explanations["其他"])
    
    def save_draft(self, draft: ReviewReplyDraft) -> bool:
        """保存草稿到数据库"""
        cursor = self.conn.cursor()
        
        # 创建草稿表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reply_drafts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                review_id TEXT,
                template_used TEXT,
                draft_content TEXT,
                keywords_matched TEXT,
                generated_at TEXT,
                reviewed INTEGER DEFAULT 0,
                reviewed_by TEXT,
                reviewed_at TEXT,
                final_content TEXT,
                status TEXT DEFAULT 'draft',
                notes TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        try:
            cursor.execute('''
                INSERT INTO reply_drafts 
                (review_id, template_used, draft_content, keywords_matched, 
                 generated_at, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                draft.review_id,
                draft.template_used,
                draft.draft_content,
                json.dumps(draft.keywords_matched),
                draft.generated_at,
                draft.status
            ))
            
            self.conn.commit()
            return True
        
        except Exception as e:
            print(f"保存草稿失败: {e}")
            return False
    
    def get_pending_drafts(self, limit: int = 10) -> List[Dict]:
        """获取待审核草稿"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            SELECT id, review_id, template_used, draft_content, 
                   keywords_matched, generated_at, status
            FROM reply_drafts
            WHERE status = 'draft'
            ORDER BY generated_at DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        
        drafts = []
        for row in rows:
            drafts.append({
                "id": row[0],
                "review_id": row[1],
                "template_used": row[2],
                "draft_content": row[3],
                "keywords_matched": json.loads(row[4]),
                "generated_at": row[5],
                "status": row[6]
            })
        
        return drafts
    
    def approve_draft(self, draft_id: int, final_content: str, 
                     reviewer: str = "admin", notes: str = "") -> bool:
        """审核通过草稿"""
        cursor = self.conn.cursor()
        
        cursor.execute('''
            UPDATE reply_drafts
            SET reviewed = 1,
                reviewed_by = ?,
                reviewed_at = ?,
                final_content = ?,
                status = 'approved',
                notes = ?
            WHERE id = ?
        ''', (reviewer, datetime.now().isoformat(), final_content, notes, draft_id))
        
        self.conn.commit()
        
        return cursor.rowcount > 0


def demo_reply_generation():
    """演示差评回复生成"""
    print("=" * 60)
    print("SVC-002: 差评AI自动回复")
    print("=" * 60)
    
    generator = ReviewReplyGenerator(DB_PATH)
    
    # 模拟差评
    test_reviews = [
        {
            "id": "review_20260327_001",
            "content": "前台服务态度很差，办理入住等了很久，也没有解释。房间设施老旧，空调声音很大。",
            "category": "服务",
            "guest_name": "张**",
            "room_type": "江景大床房"
        },
        {
            "id": "review_20260327_002",
            "content": "隔音效果太差了，晚上被走廊的声音吵醒很多次，早上也没睡好。",
            "category": "隔音",
            "guest_name": "李**",
            "room_type": "城景双床房"
        },
        {
            "id": "review_20260327_003",
            "content": "房间卫生不行，床单上有头发，马桶也没刷干净。",
            "category": "卫生",
            "guest_name": "王**",
            "room_type": "江景大床房"
        }
    ]
    
    for review in test_reviews:
        print(f"\n{'='*50}")
        print(f"差评ID: {review['id']}")
        print(f"客人: {review['guest_name']}")
        print(f"内容: {review['content']}")
        print("-" * 50)
        
        # 生成草稿
        draft = generator.generate_reply_draft(
            review_id=review["id"],
            review_content=review["content"],
            category=review["category"],
            guest_name=review["guest_name"],
            room_type=review["room_type"]
        )
        
        print(f"✅ 回复草稿（待审核）:")
        print("-" * 50)
        print(draft.draft_content)
        print("-" * 50)
        print(f"模板类型: {draft.template_used}")
        print(f"匹配关键词: {draft.keywords_matched}")
        
        # 保存草稿
        generator.save_draft(draft)
    
    print("\n" + "=" * 60)
    print("审核流程:")
    print("=" * 60)
    print("""
1. 生成草稿 → SVC-002自动完成
2. 人工审核 → 酒店人员在管理后台审核
3. 发布回复 → 审核通过后复制到携程EBK发布
4. 记录状态 → SVC-002更新数据库

Phase 2 升级:
- LLM直接生成更自然的回复
- 自动关联客人历史入住记录
- 一键发布到携程EBK
    """)


if __name__ == "__main__":
    demo_reply_generation()
```

#### SVC-003 & SVC-004 代码框架

```python
# -*- coding: utf-8 -*-
"""
SVC-003: 投诉升级处理
SVC-004: FAQ自动回复
功能：投诉升级 + FAQ Bot
Phase: 1-2
"""

import sqlite3
import json
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict

# ============================================================
# 配置区
# ============================================================

DB_PATH = "data/ctrip_reviews.db"
GUEST_DB_PATH = "data/guest_private.db"

# 升级关键词
ESCALATION_KEYWORDS = [
    "投诉", "举报", "曝光", "媒体",
    "退款", "赔偿", "索赔", "赔钱",
    "12315", "消协", "消费者协会",
    "律师", "法院", "起诉", "打官司",
    "自杀", "自残", "危险"  # 高危信号
]

# 连续差评阈值
CONSECUTIVE_BAD_REVIEW_THRESHOLD = 2
CONSECUTIVE_WINDOW_DAYS = 7

# FAQ知识库
FAQ_KNOWLEDGE_BASE = [
    {
        "id": "FAQ001",
        "keywords": ["电话", "联系", "号码", "怎么联系"],
        "question": "酒店联系电话多少",
        "answer": "📞 酒店电话：0833-2096666\n⏰ 24小时服务",
        "category": "基础信息",
        "priority": 1
    },
    {
        "id": "FAQ002",
        "keywords": ["地址", "在哪", "位置", "怎么走"],
        "question": "酒店地址在哪",
        "answer": "📍 地址：乐山市市中区白塔街85号\n🚗 停车：免费停车（酒店地下停车场）",
        "category": "基础信息",
        "priority": 1
    },
    {
        "id": "FAQ003",
        "keywords": ["入住", "几点", "时间"],
        "question": "几点可以入住",
        "answer": "🕐 入住时间：14:00后\n🕐 退房时间：14:00前\n💡 如需延迟入住请提前联系",
        "category": "基础信息",
        "priority": 1
    },
    {
        "id": "FAQ004",
        "keywords": ["停车", "车位", "停车费"],
        "question": "停车怎么收费",
        "answer": "🚗 停车：免费停车\n🔌 充电桩：有（充电收费）\n📍 位置：地下停车场B2层",
        "category": "基础信息",
        "priority": 1
    },
    {
        "id": "FAQ005",
        "keywords": ["wifi", "无线", "网络", "密码"],
        "question": "WiFi密码多少",
        "answer": "📶 WiFi：房间内覆盖\n🔑 密码：88888888（公共区域）\n💡 房间网络在床头柜有独立路由器",
        "category": "基础信息",
        "priority": 1
    },
    {
        "id": "FAQ006",
        "keywords": ["早餐", "吃饭", "几点"],
        "question": "早餐几点",
        "answer": "🍳 早餐时间：07:00-10:00\n💰 价格：68元/位\n📍 地点：1楼嘉州餐厅\n🏷️ 住店客人免费享用",
        "category": "餐饮服务",
        "priority": 1
    },
    {
        "id": "FAQ007",
        "keywords": ["宠物", "狗", "猫", "带宠物"],
        "question": "可以带宠物吗",
        "answer": "🐾 支持宠物入住！\n✅ 宠物免费（无额外费用）\n📞 请提前联系告知我们\n🏠 我们有专属宠物友好房型",
        "category": "特色服务",
        "priority": 1
    },
    {
        "id": "FAQ008",
        "keywords": ["江景", "看江", "景色"],
        "question": "有江景房吗",
        "answer": "🌅 江景房推荐：\n✅ 江景大床房（480元/晚）- 270度江景\n✅ 江景双床房（520元/晚）- 商务首选\n✅ 江景套房（880元/晚）- 豪华体验\n📞 预订请拨打：0833-2096666",
        "category": "房型推荐",
        "priority": 1
    },
    {
        "id": "FAQ009",
        "keywords": ["取消", "退订", "退款", "取消政策"],
        "question": "可以取消预订吗",
        "answer": "📋 取消政策：\n✅ 当天18:00前取消免费\n⚠️ 18:00后取消需支付首晚房费\n⚠️ 特殊节假日（五一/国庆/春节）需提前3天取消\n📞 取消请拨打：0833-2096666",
        "category": "预订相关",
        "priority": 1
    },
    {
        "id": "FAQ010",
        "keywords": ["接送", "接站", "接机", "车站"],
        "question": "有接站服务吗",
        "answer": "🚗 接站服务：\n✅ 乐山高铁站可安排接站\n💰 费用：50元/次\n📞 请提前2小时预约\n📞 预约电话：0833-2096666",
        "category": "特色服务",
        "priority": 2
    },
    {
        "id": "FAQ011",
        "keywords": ["发票", "开票", "税票"],
        "question": "可以开发票吗",
        "answer": "🧾 发票服务：\n✅ 支持增值税普通发票\n✅ 支持专用发票（如需请提前告知）\n📍 开票地点：1楼前台\n💡 离店时可开具或离店后邮寄",
        "category": "基础信息",
        "priority": 2
    },
    {
        "id": "FAQ012",
        "keywords": ["加床", "加枕头", "额外"],
        "question": "可以加床吗",
        "answer": "🛏️ 加床服务：\n✅ 支持加床（1.2m折叠床）\n💰 费用：100元/晚\n📞 请提前1天预约\n📍 前台办理",
        "category": "增值服务",
        "priority": 2
    }
]


# ============================================================
# 数据模型
# ============================================================

@dataclass
class EscalationAlert:
    """升级告警"""
    id: str
    level: str  # HIGH/MEDIUM/LOW
    trigger_type: str  # keyword/consecutive/amount
    trigger_reason: str
    reviews: List[Dict]
    guest_info: Dict
    suggested_actions: List[str]
    notified_to: List[str]
    status: str  # pending/processed/resolved
    created_at: str
    
    def to_dict(self) -> Dict:
        return asdict(self)


class EscalationDetector:
    """投诉升级检测器"""
    
    def __init__(self, db_path: str, guest_db_path: str):
        self.db_path = db_path
        self.guest_db_path = guest_db_path
        self.conn = sqlite3.connect(db_path)
        self.guest_conn = sqlite3.connect(guest_db_path)
    
    def check_keyword_escalation(self, content: str) -> bool:
        """检查是否触发关键词升级"""
        content_lower = content.lower()
        
        for keyword in ESCALATION_KEYWORDS:
            if keyword in content_lower:
                return True
        
        return False
    
    def get_consecutive_bad_reviews(self, guest_phone: str = None, 
                                    guest_name: str = None) -> int:
        """获取连续差评数量"""
        cursor = self.conn.cursor()
        
        since_date = (datetime.now() - timedelta(days=CONSECUTIVE_WINDOW_DAYS)).strftime('%Y-%m-%d')
        
        if guest_phone:
            # 通过手机号关联
            cursor.execute('''
                SELECT COUNT(*) FROM reviews
                WHERE star <= 3
                AND published_at >= ?
            ''', (since_date,))
        else:
            # 通过姓名模糊匹配（不准确，仅预警）
            if guest_name:
                cursor.execute('''
                    SELECT COUNT(*) FROM reviews
                    WHERE star <= 3
                    AND published_at >= ?
                ''', (since_date,))
        
        return cursor.fetchone()[0] if cursor.fetchone() else 0
    
    def get_guest_history(self, guest_name: str = None) -> Dict:
        """获取客人历史信息"""
        # 这个功能需要关联guest_private.db
        # Phase 1简化实现
        
        return {
            "total_stays": 1,
            "avg_rate": 450,
            "previous_complaints": 0,
            "vip_level": "C",
            "note": "需关联guest_private.db获取完整历史"
        }
    
    def detect_escalation(self, review: Dict) -> Optional[EscalationAlert]:
        """
        检测是否需要升级
        """
        alert = None
        
        # 检查1：关键词触发
        if self.check_keyword_escalation(review.get("content", "")):
            alert = EscalationAlert(
                id=f"esc_keyword_{review['id']}",
                level="HIGH",
                trigger_type="keyword",
                trigger_reason="提及敏感关键词",
                reviews=[review],
                guest_info=self.get_guest_history(review.get("guest_name")),
                suggested_actions=[
                    "立即联系客人",
                    "了解具体情况",
                    "准备补偿方案",
                    "必要时升级至总经理"
                ],
                notified_to=["前台主管", "店长"],
                status="pending",
                created_at=datetime.now().isoformat()
            )
        
        # 检查2：连续差评
        consecutive_count = self.get_consecutive_bad_reviews(
            guest_name=review.get("guest_name")
        )
        
        if consecutive_count >= CONSECUTIVE_BAD_REVIEW_THRESHOLD:
            alert = EscalationAlert(
                id=f"esc_consecutive_{review['id']}",
                level="HIGH",
                trigger_type="consecutive",
                trigger_reason=f"7天内连续{consecutive_count}条差评",
                reviews=[review],
                guest_info=self.get_guest_history(review.get("guest_name")),
                suggested_actions=[
                    "查看历史差评",
                    "分析共性问题",
                    "主动联系客人道歉",
                    "制定补偿方案"
                ],
                notified_to=["店长"],
                status="pending",
                created_at=datetime.now().isoformat()
            )
        
        return alert
    
    def send_escalation_alert(self, alert: EscalationAlert) -> bool:
        """发送升级告警"""
        print("=" * 60)
        print(f"🚨 投诉升级告警 [{alert.level}]")
        print("=" * 60)
        print(f"触发类型: {alert.trigger_type}")
        print(f"触发原因: {alert.trigger_reason}")
        print(f"客人信息: {alert.guest_info}")
        print("-" * 60)
        print("建议处理:")
        for action in alert.suggested_actions:
            print(f"  • {action}")
        print("-" * 60)
        print(f"通知对象: {', '.join(alert.notified_to)}")
        print("=" * 60)
        
        # 实际发送时需要调用微信/企微Webhook
        return True


class FAQBot:
    """FAQ自动回复机器人"""
    
    def __init__(self, knowledge_base: List[Dict] = None):
        self.knowledge_base = knowledge_base or FAQ_KNOWLEDGE_BASE
        self.recent_answers = {}  # 用于去重（5分钟内不重复回答）
        self.developing_answers = {}  # 用于跟踪多轮对话
    
    def find_answer(self, question: str) -> Optional[Dict]:
        """
        查找FAQ答案
        
        匹配策略：
        1. 精确关键词匹配
        2. 包含关键词匹配
        3. 语义相似度（Phase 2）
        4. LLM兜底（Phase 2）
        """
        question_lower = question.lower()
        
        # 策略1：精确匹配关键词
        for faq in self.knowledge_base:
            for keyword in faq.get("keywords", []):
                if keyword in question_lower:
                    return faq
        
        # 策略2：部分关键词匹配
        for faq in self.knowledge_base:
            matched = 0
            for keyword in faq.get("keywords", []):
                if keyword in question_lower:
                    matched += 1
            
            if matched >= 2:  # 至少匹配2个关键词
                return faq
        
        # 策略3：返回None，由LLM处理
        return None
    
    def should_auto_reply(self, user_id: str, question: str) -> bool:
        """
        判断是否应该自动回复
        """
        # 检查是否是重复问题
        if user_id in self.recent_answers:
            last_answer = self.recent_answers[user_id]
            time_diff = datetime.now() - last_answer["time"]
            
            if time_diff.total_seconds() < 300:  # 5分钟内
                if question == last_answer["question"]:
                    return False  # 不重复回复
        
        return True
    
    def record_answer(self, user_id: str, question: str, faq_id: str):
        """记录回答历史"""
        self.recent_answers[user_id] = {
            "question": question,
            "faq_id": faq_id,
            "time": datetime.now()
        }
    
    def get_response(self, user_id: str, question: str) -> Optional[str]:
        """
        获取回复内容
        """
        # 检查是否应该自动回复
        if not self.should_auto_reply(user_id, question):
            return None
        
        # 查找答案
        faq = self.find_answer(question)
        
        if faq:
            # 记录回答
            self.record_answer(user_id, question, faq["id"])
            
            # 返回答案
            response = faq["answer"]
            
            # 追加通用结尾
            if faq.get("priority", 1) == 1:
                response += "\n\n如有其他问题欢迎随时咨询！"
            
            return response
        
        # 无法回答
        return None


def demo_escalation_and_faq():
    """演示升级检测和FAQ"""
    print("=" * 60)
    print("SVC-003 & SVC-004: 投诉升级 + FAQ自动回复")
    print("=" * 60)
    
    # 演示FAQ
    print("\n" + "=" * 50)
    print("FAQ Bot 演示")
    print("=" * 50)
    
    faq_bot = FAQBot()
    
    test_questions = [
        "酒店电话多少",
        "我想带狗来，有地方停吗",
        "房间隔音怎么样",
        "可以开发票吗",
        "明天入住，几点能到",
        "我想要退款",
        "你们的地址在哪",
        "早餐几点开始啊",
        "你们这支持宠物入住吗"
    ]
    
    for q in test_questions:
        answer = faq_bot.get_response("test_user", q)
        if answer:
            print(f"\n👤 用户: {q}")
            print(f"🤖 回复: {answer}")
        else:
            print(f"\n👤 用户: {q}")
            print(f"🤖 回复: 这个问题需要转人工处理")
    
    # 演示投诉升级
    print("\n" + "=" * 50)
    print("投诉升级检测 演示")
    print("=" * 50)
    
    detector = EscalationDetector(DB_PATH, GUEST_DB_PATH)
    
    test_reviews = [
        {
            "id": "test_001",
            "content": "太差了，要求退款，否则我要投诉到12315",
            "star": 1,
            "guest_name": "张**"
        },
        {
            "id": "test_002",
            "content": "服务一般，卫生也不太行",
            "star": 3,
            "guest_name": "李**"
        }
    ]
    
    for review in test_reviews:
        print(f"\n检测差评: {review['content'][:30]}...")
        
        if detector.check_keyword_escalation(review["content"]):
            print("  🚨 触发关键词升级！")
            alert = EscalationAlert(
                id=f"esc_{review['id']}",
                level="HIGH",
                trigger_type="keyword",
                trigger_reason="提及退款/投诉",
                reviews=[review],
                guest_info=detector.get_guest_history(review["guest_name"]),
                suggested_actions=["立即联系客人", "准备退款预案"],
                notified_to=["店长"],
                status="pending",
                created_at=datetime.now().isoformat()
            )
            detector.send_escalation_alert(alert)
        else:
            print("  ✅ 正常处理")


if __name__ == "__main__":
    demo_escalation_and_faq()
```

---

### 乐山落地行动清单

#### 第一周：差评监控启动

| 序号 | 行动项 | 负责方 | 完成标准 | 优先级 |
|------|--------|--------|----------|--------|
| 1 | 确认携程EBK登录方式 | Eric + 酒店 | 能登录EBK后台 | P0 |
| 2 | 获取携程差评数据（手动导出） | 酒店 | 获取历史差评Excel | P0 |
| 3 | 收集紧急联系人微信 | 酒店 | 至少2个紧急联系人 | P0 |
| 4 | 建立微信预警群 | 酒店 | 群已建立，Webhook配置好 | P1 |
| 5 | 部署SVC-001爬虫/导入脚本 | 技术方 | 差评自动入库 | P1 |

#### 第二周：差评回复机制建立

| 序号 | 行动项 | 负责方 | 完成标准 | 优先级 |
|------|--------|--------|----------|--------|
| 6 | 整理差评回复模板库 | Eric | 5类模板确认 | P0 |
| 7 | 培训前台差评回复流程 | 酒店 | 前台会使用 | P1 |
| 8 | 设置差评回复时效提醒 | 技术方 | 每日提醒 | P2 |
| 9 | FAQ知识库整理 | Eric | 至少20条FAQ | P1 |
| 10 | 部署SVC-004 FAQ Bot | 技术方 | 微信群测试 | P2 |

#### 第三周：升级机制测试

| 序号 | 行动项 | 负责方 | 完成标准 | 优先级 |
|------|--------|--------|----------|--------|
| 11 | 定义升级关键词 | Eric + 酒店 | 关键词列表确认 | P0 |
| 12 | 配置升级通知 | 技术方 | 微信通知测试成功 | P1 |
| 13 | 培训紧急联系人处理流程 | 酒店 | 紧急联系人会处理 | P1 |
| 14 | 首次真实升级演练 | 双方 | 模拟升级通知发出 | P2 |

#### 第四周及以后

| 序号 | 行动项 | 负责方 | 完成标准 | 优先级 |
|------|--------|--------|----------|--------|
| 15 | 差评数据分析（按月统计） | 技术方 | 月度差评报告 | P2 |
| 16 | 回复模板迭代优化 | Eric | 模板优化2-3版 | P2 |
| 17 | Phase 2规划 | 技术方 | LLM回复方案确定 | P3 |
| 18 | SOP文档完善 | 双方 | 客服SOP v1.0 | P2 |

---

### 关键成功指标（KPI）

| 阶段 | 指标 | 目标值 | 测量方式 |
|------|------|--------|----------|
| Phase 1 | 差评发现时间 | <2小时 | 从发布到告警 |
| Phase 1 | 差评回复率 | >90% | 已回复差评/总差评 |
| Phase 1 | 差评48小时内回复率 | >70% | 48小时内回复/总差评 |
| Phase 1 | FAQ自动回复准确率 | >85% | 正确回复/总咨询 |
| Phase 2 | LLM回复采用率 | >60% | AI草稿直接采用/总草稿 |
| Phase 2 | 升级处理满意度 | >4.0分 | 升级处理后客人评分 |

---

### 风险与应对

| 风险 | 可能性 | 影响 | 应对措施 |
|------|--------|------|----------|
| 携程限制数据导出 | 中 | 高 | EBK手动导出；尝试API申请 |
| 爬虫被封 | 中 | 中 | 控制频率；使用Cookie |
| 差评回复质量差 | 中 | 高 | 必须人工审核；严格模板 |
| 升级通知无人响应 | 中 | 高 | 多通道通知；设置超时升级 |
| FAQ回复错误信息 | 中 | 中 | 知识库审核流程；高频Q&A优先 |

---

### 四大SKILL协作流程

```
携程新差评发布
        │
        ▼
┌─────────────────┐
│  SVC-001 差评预警 │
│                  │
│ • 检测新增差评   │
│ • 自动分级      │
│   L1（紧急）    │
│   L2（普通）    │
│ • 自动归类      │
│   服务/设施/卫生 │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ SVC-003 升级检测 │
│                  │
│ 触发条件：        │
│ • 关键词命中     │
│ • 连续2条差评    │
│ • 提及索赔       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  微信通知        │
│  @紧急联系人    │
│  告警级别标注    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  SVC-002 回复生成 │
│                  │
│ • LLM生成草稿    │
│ • 模板填充       │
│ • 人工审核       │
│ • 发布携程       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ SVC-004 FAQ Bot │
│                  │
│ 用户提问微信群   │
│ • 知识库匹配    │
│ • 自动回复      │
│ • 复杂问题转人工 │
└─────────────────┘
```

---

**文档状态**: ✅ V1.0完成
**下一步**: 确认携程EBK权限 + 整理FAQ知识库 + 部署SVC-001差评监控
